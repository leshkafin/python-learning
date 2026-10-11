import pandas as pd

df = pd.read_json("wb_finance.json")

print("Строк:", len(df))
print("Уникальных srid:", df["srid"].nunique())
print("Колонки:", df.columns.tolist())
print("\nТипы операций:")
print(df["sellerOperName"].value_counts())
print("\nВалюты:")
print(df["currency"].value_counts())


# Сколько уникальных заказов
print("Уникальных srid:", df["srid"].nunique())

# Смотрим по одному примеру каждого типа
for op in df["sellerOperName"].unique():
    print(f"\n=== {op} ===")
    sample = df[df["sellerOperName"] == op].iloc[0]
    print(f"  forPay: {sample['forPay']}")
    print(f"  deliveryService: {sample['deliveryService']}")
    print(f"  retailAmount: {sample['retailAmount']}")
    print(f"  paidStorage: {sample['paidStorage']}")
    print(f"  penalty: {sample['penalty']}")
    print(f"  deduction: {sample['deduction']}")
    print(f"  quantity: {sample['quantity']}")


# Группируем по srid: суммируем все суммы
grouped = df.groupby("srid").agg({
    "forPay": "sum",
    "deliveryService": "sum",
    "deduction": "sum",
    "penalty": "sum",
    "paidStorage": "sum",
    "retailAmount": "sum"
}).reset_index()

# Считаем чистую прибыль (без себестоимости)
grouped["net_before_cost"] = (
    grouped["forPay"]
    - grouped["deliveryService"]
    - grouped["deduction"]
    - grouped["penalty"]
    - grouped["paidStorage"]
)

print("Заказов:", len(grouped))
print(f"Общий доход (forPay):      {grouped['forPay'].sum():.2f} CNY")
print(f"Общая логистика:           {grouped['deliveryService'].sum():.2f} CNY")
print(f"Общие удержания:           {grouped['deduction'].sum():.2f} CNY")
print(f"Чистая (без себеса):       {grouped['net_before_cost'].sum():.2f} CNY")


# 1. Достаём vendorCode для каждого srid
vendor_map = df.groupby("srid")["vendorCode"].first().reset_index()
grouped = pd.merge(grouped, vendor_map, on="srid", how="left")

# 2. Загружаем себестоимость
cost_df = pd.read_csv("cost.csv")

# 3. Соединяем
final = pd.merge(grouped, cost_df, left_on="vendorCode", right_on="supplierArticle", how="left")

# 4. Курс: 1 CNY ≈ 12 RUB
RATE = 12

# 5. Считаем в рублях
final["forPay_rub"] = final["forPay"] * 12.5
final["delivery_rub"] = final["deliveryService"] * 12.5
final["deduction_rub"] = final["deduction"] * 12.5

final["net_profit_rub"] = (
    final["forPay_rub"]
    - final["delivery_rub"]
    - final["deduction_rub"]
    - final["cost_rub"]
)

print(f"\nЧистая прибыль: {final['net_profit_rub'].sum():.2f} RUB")
print(f"Чистая прибыль: {final['net_profit_rub'].sum() / RATE:.2f} CNY")


# Проверка одного заказа
sample = final[final["srid"] == "ebG.rd148896def89453d8c665804b8ab743f.0.0"]
print(sample[["srid", "vendorCode", "forPay", "deliveryService", "cost_rub", "net_profit_rub"]])

# Заказы без продажи (только доставка/удержание)
has_sale = df[df["sellerOperName"] == "销售"]["srid"].unique()
no_sale = grouped[~grouped["srid"].isin(has_sale)]
print(f"Заказов без продажи: {len(no_sale)}")

# Исключаем их из расчёта
grouped_with_sale = grouped[grouped["srid"].isin(has_sale)]
print(f"Заказов с продажей: {len(grouped_with_sale)}")

# 1. Оставляем только заказы С продажей
has_sale = df[df["sellerOperName"] == "销售"]["srid"].unique()
final_clean = final[final["srid"].isin(has_sale)].copy()

print(f"Заказов с продажей: {len(final_clean)}")
print(f"Чистая прибыль (только продажи): {final_clean['net_profit_rub'].sum():.2f} RUB")

# 2. Смотрим 36 заказов без продажи
no_sale = final[~final["srid"].isin(has_sale)]
print(f"\nЗаказов без продажи: {len(no_sale)}")
print(f"Их общий убыток: {no_sale['net_profit_rub'].sum():.2f} RUB")
print(f"Из них удержания: {no_sale['deduction'].sum() * 12.5:.2f} RUB")

# 3. Топ-5 убыточных заказов с продажей
print("\nТоп-5 убыточных:")
print(final_clean.nsmallest(5, "net_profit_rub")[["vendorCode", "forPay", "cost_rub", "net_profit_rub"]])