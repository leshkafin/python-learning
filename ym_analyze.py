import os
import requests
import json
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
token = os.getenv("YM_API_TOKEN")
CAMPAIGN_ID = 149117084

url = f"https://api.partner.market.yandex.ru/v2/campaigns/{CAMPAIGN_ID}/stats/orders"
headers = {"Api-Key": token}

# === 1. Собираем заказы чанками по 60 дней ===
all_orders = []

end = datetime.now()
start = end - timedelta(days=180)

chunk_start = start
while chunk_start < end:
    chunk_end = min(chunk_start + timedelta(days=60), end)
    date_from = chunk_start.strftime("%Y-%m-%d")
    date_to = chunk_end.strftime("%Y-%m-%d")
    
    print(f"\n--- Период: {date_from} — {date_to} ---")
    
    page_token = None
    while True:
        payload = {"dateFrom": date_from, "dateTo": date_to}
        params = {"limit": 200}
        if page_token:
            params["pageToken"] = page_token
        
        resp = requests.post(url, headers=headers, params=params, json=payload, timeout=60)
        if resp.status_code != 200:
            print(f"Ошибка: {resp.status_code}")
            print(resp.text[:300])
            break
        
        data = resp.json()
        orders = data.get("result", {}).get("orders", [])
        all_orders.extend(orders)
        print(f"Получено: {len(orders)}, всего: {len(all_orders)}")
        
        next_token = data.get("result", {}).get("paging", {}).get("nextPageToken")
        if not next_token:
            break
        page_token = next_token
    
    chunk_start = chunk_end

with open("ym_orders_all.json", "w", encoding="utf-8") as f:
    json.dump(all_orders, f, ensure_ascii=False, indent=2)
print(f"\nВСЕГО заказов: {len(all_orders)}")

# === 2. Разбираем позиции ===
rows = []
for order in all_orders:
    status = order["status"]
    if status in ("CANCELLED_BEFORE_PROCESSING", "CANCELLED_IN_PROCESSING"):
        continue
    
    for item in order["items"]:
        item_returned = any(
            d.get("itemStatus") == "RETURNED"
            for d in item.get("details", [])
        )
        
        marketplace_total = 0
        for price in item["prices"]:
            if price["type"] == "MARKETPLACE":
                marketplace_total = price["total"]
        
        rows.append({
            "order_id": order["id"],
            "date": order["creationDate"],
            "status": status,
            "shopSku": item["shopSku"],
            "count": item["count"],
            "marketplace_total": marketplace_total,
            "returned": item_returned,
        })

df = pd.DataFrame(rows)
print(f"\nПозиций: {len(df)}")
print(f"\nСтатусы:")
print(df["status"].value_counts())

# === 3. Комиссии ===
comm_rows = []
for order in all_orders:
    for comm in order.get("commissions", []):
        comm_rows.append({
            "order_id": order["id"],
            "type": comm["type"],
            "amount": comm["actual"],
        })

comm_df = pd.DataFrame(comm_rows)
if not comm_df.empty:
    print("\n=== Комиссии по типам (CNY) ===")
    print(comm_df.groupby("type")["amount"].agg(["sum", "count"]).round(2))

# === 4. Subsidies (компенсации) ===
subs_rows = []
for order in all_orders:
    accrual = sum(
        s["amount"] for s in order.get("subsidies", [])
        if s["operationType"] == "ACCRUAL" and s["type"] == "SUBSIDY"
    )
    deduction = sum(
        s["amount"] for s in order.get("subsidies", [])
        if s["operationType"] == "DEDUCTION" and s["type"] == "SUBSIDY"
    )
    subs_rows.append({
        "order_id": order["id"],
        "subs_net": accrual - deduction,
    })

subs_df = pd.DataFrame(subs_rows)
if not subs_df.empty:
    print(f"\n=== Subsidies net (CNY) ===")
    print(f"Всего: {subs_df['subs_net'].sum():,.2f} ¥")

# === 5. Себестоимость ===
cost_df = pd.read_csv("cost_cny.csv")
merged = pd.merge(df, cost_df, left_on="shopSku", right_on="supplierArticle", how="left")
merged["cost_cny"] = merged["cost_cny"].fillna(0)
merged["total_cost"] = merged["cost_cny"] * merged["count"]

# Присоединяем subsidies
if not subs_df.empty:
    merged = pd.merge(merged, subs_df, on="order_id", how="left")
    merged["subs_net"] = merged["subs_net"].fillna(0)
else:
    merged["subs_net"] = 0

# === 6. Итоги ===
marketplace_sum = merged["marketplace_total"].sum()
subs_sum = merged["subs_net"].sum()
total_income = merged["marketplace_total"].sum()
total_commissions = comm_df["amount"].sum() if not comm_df.empty else 0
total_cost = merged["total_cost"].sum()

net_profit = total_income - total_commissions - total_cost

print(f"\n=== ИТОГ YM за 180 дней (CNY) ===")
print(f"MARKETPLACE (база):       {marketplace_sum:>12,.2f} ¥")
print(f"Subsidies (net):          {subs_sum:>12,.2f} ¥")
print(f"{'─' * 42}")
print(f"Реальный доход:           {total_income:>12,.2f} ¥")
print(f"Комиссии YM:             -{total_commissions:>12,.2f} ¥")
print(f"Себестоимость:           -{total_cost:>12,.2f} ¥")
print(f"{'─' * 42}")
print(f"ЧИСТАЯ ПРИБЫЛЬ:           {net_profit:>12,.2f} ¥")

# === 7. По SKU ===
print(f"\n=== По SKU (CNY) ===")
by_sku = merged.groupby("shopSku").agg({
    "marketplace_total": "sum",
    "subs_net": "sum",
    "count": "sum",
    "total_cost": "sum",
}).round(2)
by_sku["income"] = by_sku["marketplace_total"] + by_sku["subs_net"]
by_sku["margin"] = by_sku["income"] - by_sku["total_cost"]
by_sku = by_sku.sort_values("margin", ascending=False)
print(by_sku)