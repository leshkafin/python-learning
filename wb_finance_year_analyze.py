import pandas as pd

# Загружаем
df = pd.read_json("wb_finance_year.json")

# Группируем по srid
grouped = df.groupby("srid").agg({
    "forPay": "sum",
    "deliveryService": "sum",
    "deduction": "sum",
    "penalty": "sum",
    "paidStorage": "sum",
    "retailAmount": "sum",
    "vendorCode": "first"
}).reset_index()

# Флаг: есть ли продажа
has_sale = df[df["sellerOperName"] == "销售"]["srid"].unique()
grouped["has_sale"] = grouped["srid"].isin(has_sale)

# Загружаем себес (в юанях)
cost_df = pd.read_csv("cost_cny.csv")
merged = pd.merge(grouped, cost_df, left_on="vendorCode", right_on="supplierArticle", how="left")
merged["cost_cny"] = merged["cost_cny"].where(merged["has_sale"], 0).fillna(0)

# Комиссия WB
merged["commission_cny"] = merged["retailAmount"] - merged["forPay"]

# Корректировка возвратов (в коде они прибавляются, а должны вычитаться — разница ×2)
returns_sum = df[df["sellerOperName"] == "退货"]["forPay"].sum()
CORRECTION = returns_sum * 2

# Итоговые цифры (с корректировкой)
income       = merged["forPay"].sum() - CORRECTION
logistics    = merged["deliveryService"].sum()
deductions   = merged["deduction"].sum()
penalties    = merged["penalty"].sum()
costs        = merged["cost_cny"].sum()
incoming     = income - logistics - deductions - penalties
net_profit   = incoming - costs

# Вывод
print(f"\n=== ИТОГ ЗА ГОД (в юанях) ===")
print(f"Выручка покупателей:  {merged['retailAmount'].sum():>10,.0f} ¥")
print(f"Комиссия WB:         -{merged['commission_cny'].sum():>10,.0f} ¥")
print(f"{'─' * 45}")
print(f"К перечислению:       {income:>10,.0f} ¥")
print(f"Логистика:           -{logistics:>10,.0f} ¥")
print(f"Удержания:           -{deductions:>10,.0f} ¥")
print(f"Штрафы:              -{penalties:>10,.0f} ¥")
print(f"{'─' * 45}")
print(f"На счёт юрлица:       {incoming:>10,.0f} ¥")
print(f"Себестоимость:       -{costs:>10,.0f} ¥")
print(f"{'─' * 45}")
print(f"ЧИСТАЯ ПРИБЫЛЬ:       {net_profit:>10,.0f} ¥")

# Проверка возвратов
print(f"\n=== ВОЗВРАТЫ ===")
print(f"Всего возвратов: {len(df[df['sellerOperName'] == '退货'])}")
print(f"Сумма корректировки: −{CORRECTION:.0f} ¥")

# Сверка с выводами
print(f"\n=== СВЕРКА С ВЫВОДАМИ ===")
withdrawn = 133818  # твои выводы за 7 месяцев, в юанях
print(f"На счёт (расчёт):     {incoming:>10,.0f} ¥")
print(f"Выведено:             {withdrawn:>10,.0f} ¥")
print(f"Остаток на WB:        {incoming - withdrawn:>10,.0f} ¥")