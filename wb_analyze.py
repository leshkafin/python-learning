import pandas as pd

df = pd.read_json("wb_sales.json")

# print(df.head())       # первые 5 строк
# print(df.shape)        # (строк, колонок)
# print(df.columns)      # названия колонок

# df["finishedPrice"]           # одна колонка
# df["finishedPrice"].sum()     # сумма всех значений
# df["finishedPrice"].mean()    # среднее
# df["finishedPrice"].max()     # максимум
# df["finishedPrice"].min()     # минимум
# df["finishedPrice"].count()   # сколько значений


print("Выручка:", df["finishedPrice"].sum())
print("Средний чек:", df["finishedPrice"].mean())
print("Максимальный чек:", df["finishedPrice"].max())
print("Продаж:", df["finishedPrice"].count())


print("\nК перечислению (forPay):", df["forPay"].sum())
print("Комиссия WB:", df["finishedPrice"].sum() - df["forPay"].sum())

print("\nВыручка по артикулам:")
grouped = df.groupby("supplierArticle")["finishedPrice"].sum().sort_values(ascending=False)
print(grouped)

print("\nКоличество продаж по артикулам:")
grouped_count = df.groupby("supplierArticle")["finishedPrice"].count().sort_values(ascending=False)
print(grouped_count)

print("\nСредняя цена по артикулам:")
avg = df.groupby("supplierArticle")["finishedPrice"].mean().sort_values(ascending=False)
print(avg)

# Загружаем себестоимость
cost_df = pd.read_csv("cost.csv")

# Соединяем продажи и себестоимость
merged = pd.merge(df, cost_df,on="supplierArticle",how="left")

# Смотрим, что получилось
print("\nКолонки после merge:")
print(merged.columns.tolist())

# Считаем прибыль по строкам
merged["profit"] = merged["forPay"] - merged["cost_rub"]

# Общая прибыль
print("\nОбщая прибыль:", merged["profit"].sum())

print("\nПрибыль по артикулам:")
grouped_profit = merged.groupby("supplierArticle")["profit"].sum().sort_values(ascending=False)
print(grouped_profit)


# Маржа по артикулам (%)
merged["margin"] = (merged["profit"] / merged["forPay"]) * 100

print("\nМаржа по артикулам (%):")
margin = merged.groupby("supplierArticle")["margin"].mean().sort_values(ascending=False)
print(margin.round(1))