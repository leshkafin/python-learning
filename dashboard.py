import streamlit as st
import pandas as pd
import json
from collections import defaultdict
import plotly.express as px

st.set_page_config(page_title="WB Аналитика", layout="wide")

st.title("📊 Аналитика продаж на WB")
st.write("Данные о прибыли по каждому SKU за год (с учётом рекламы)")


@st.cache_data
def load_data():
    # === 1. Финансовый отчёт ===
    with open("wb_finance_year.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    df = df[["vendorCode", "forPay", "deliveryService", "paidStorage",
             "deduction", "penalty", "quantity"]]
    
    for col in ["forPay", "deliveryService", "paidStorage", "deduction", "penalty", "quantity"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    
    grouped = df.groupby("vendorCode").sum()
    grouped = grouped[grouped.index != ""]
    
    # === 2. Себес ===
    cost_df = pd.read_csv("cost_cny.csv")
    merged = pd.merge(grouped, cost_df, left_index=True, right_on="supplierArticle", how="left")
    merged = merged.set_index("supplierArticle")
    merged = merged.sort_index()
    
    merged["total_cost"] = merged["cost_cny"] * merged["quantity"]
    merged["profit"] = (
        merged["forPay"]
        - merged["deliveryService"]
        - merged["paidStorage"]
        - merged["deduction"]
        - merged["penalty"]
        - merged["total_cost"]
    )
    
    # === 3. Реклама: nmId → vendorCode ===
    with open("wb_cards.json", "r", encoding="utf-8") as f:
        cards = json.load(f)
    
    nm_to_vendor = {}
    for card in cards:
        nm_to_vendor[card["nmID"]] = card["vendorCode"]
    
    with open("wb_promo_stats.json", "r", encoding="utf-8") as f:
        promo = json.load(f)
    
    promo_by_nm = defaultdict(float)
    for camp in promo:
        for day in camp.get("days", []):
            for app in day.get("apps", []):
                for nm in app.get("nms", []):
                    promo_by_nm[nm["nmId"]] += nm.get("sum", 0)
    
    promo_by_vendor = defaultdict(float)
    for nm_id in promo_by_nm:
        vendor = nm_to_vendor.get(nm_id, "UNKNOWN")
        promo_by_vendor[vendor] += promo_by_nm[nm_id]
    
    # === 4. Реклама: распределяем реальные расходы со счёта ===
    # Из wb_payments.csv:
    #   Счёт:         116 163 ₽  ← твои деньги (вычитаем)
    #   Баланс:         5 414 ₽  ← уже в deduction (не вычитаем)
    #   Промо бонусы: 120 000 ₽  ← подарок WB (не вычитаем)
    REAL_PROMO_RUB = 116163
    RATE = 12
    
    merged["promo_rub"] = merged.index.map(promo_by_vendor).fillna(0)
    
    # Пропорционально делим счёт между SKU
    total_promo = merged["promo_rub"].sum()
    if total_promo > 0:
        merged["promo_cny"] = (merged["promo_rub"] / total_promo) * (REAL_PROMO_RUB / RATE)
    else:
        merged["promo_cny"] = 0
    
    # === 5. Финальная прибыль ===
    merged["final_profit"] = merged["profit"] - merged["promo_cny"]
    
    return merged


df = load_data()

# === МЕТРИКИ ===
st.subheader("Ключевые метрики")

col1, col2, col3, col4 = st.columns(4)

total_revenue = df["forPay"].sum()
total_profit_before = df["profit"].sum()
total_promo = df["promo_cny"].sum()
total_profit_after = df["final_profit"].sum()
margin = total_profit_after / total_revenue * 100
total_qty = int(df["quantity"].sum())

col1.metric("Выручка", f"{total_revenue:,.0f} ¥")
col2.metric("Прибыль до рекламы", f"{total_profit_before:,.0f} ¥")
col3.metric("Реклама (свой счёт)", f"-{total_promo:,.0f} ¥")
col4.metric("Чистая прибыль", f"{total_profit_after:,.0f} ¥", f"маржа {margin:.1f}%")

st.caption(f"Продано: {total_qty:,} шт")

# === ТАБЛИЦА ===
st.subheader("Данные по SKU")

display_df = df[["forPay", "profit", "promo_cny", "final_profit", "quantity", "cost_cny"]].copy()

st.dataframe(
    display_df,
    width="stretch",
    column_config={
        "forPay": st.column_config.NumberColumn("Выручка", format="%.0f ¥"),
        "profit": st.column_config.NumberColumn("Прибыль до рекламы", format="%.0f ¥"),
        "promo_cny": st.column_config.NumberColumn("Реклама", format="%.0f ¥"),
        "final_profit": st.column_config.NumberColumn("Чистая прибыль", format="%.0f ¥"),
        "quantity": st.column_config.NumberColumn("Кол-во", format="%d"),
        "cost_cny": st.column_config.NumberColumn("Себес/шт", format="%.2f ¥"),
    }
)

# === Сноска ===
st.caption(
    f"Реклама = реальные расходы со счёта (116 163 ₽), распределены пропорционально "
    f"расходам кампаний. Баланс (5 414 ₽) уже в deduction, промо-бонусы WB (120 000 ₽) не считаем. "
    f"Курс: 12 ₽ = 1 ¥"
)



# === ГРАФИК ===
st.subheader("Чистая прибыль по SKU")

# Копируем только нужное и делаем индекс обычной колонкой
chart_df = df[["final_profit"]].copy()
chart_df = chart_df.reset_index()
chart_df = chart_df.rename(columns={"supplierArticle": "SKU"})

# Сортируем по убыванию
chart_df = chart_df.sort_values("final_profit", ascending=False)

fig = px.bar(
    chart_df,
    x="SKU",
    y="final_profit",
    text="final_profit",         # подписи значений над столбцами
    color="final_profit",        # цвет по значению
    color_continuous_scale="Greens",  # зелёная палитра
)

fig.update_traces(
    texttemplate='%{text:,.0f}',  # формат подписей
    textposition='outside',       # подписи над столбцами
)

fig.update_layout(
    height=500,                   # высота графика
    showlegend=False,
    xaxis_title=None,             # убрать "SKU" внизу
    yaxis_title=None,             # убрать "final_profit" слева
    coloraxis_showscale=False,    # убрать шкалу цвета
    margin=dict(t=20, b=20, l=20, r=20),  # убрать поля
)

st.plotly_chart(fig, use_container_width=True)