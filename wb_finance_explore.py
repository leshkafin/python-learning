import pandas as pd
import json

# Загружаем данные
with open("wb_finance_year.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Тип: {type(data)}")
print(f"Записей: {len(data)}")

# Превращаем в DataFrame
df = pd.DataFrame(data)

print(f"\nВсе колонки:")
for i, col in enumerate(df.columns):
    print(f"  [{i}] {col}")

print("\n=== Причины удержаний (bonusTypeName) ===")
print(df["bonusTypeName"].value_counts())

promo = df[df["bonusTypeName"] == "Provision of «WB Promotion» services"]

print(promo[["bonusTypeName", "forPay", "penalty", "deduction", "additionalPayment"]])

print(f"Записей: {len(promo)}")
print(f"\nСуммы по полям:")
for col in ["forPay", "penalty", "deduction", "additionalPayment"]:
    print(f"  {col}: {promo[col].tolist()}")


print("\n=== Всё, что в deduction != 0 ===")
ded = df[df["deduction"] != "0"][["bonusTypeName", "deduction", "sellerOperName"]]
print(ded.to_string())    

row = df[df["deduction"] == "489"]
print(row[["dateFrom", "dateTo", "sellerOperName", "deduction", 
           "forPay", "deliveryService", "penalty", "additionalPayment"]])
print(f"\nВсе колонки этой строки:")
for col in df.columns:
    val = row.iloc[0][col]
    if val != "0" and val != "" and pd.notna(val):
        print(f"  {col}: {val}")