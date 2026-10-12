import pandas as pd

df = pd.read_csv("wb_payments.csv", sep=";")

print(f"Строк: {len(df)}")
print(f"Колонки: {df.columns.tolist()}")

print(f"\n=== По источникам списания ===")
summary = df.groupby("Источник списания")["Сумма"].sum()
print(summary)

print(f"\n=== Всего строк: {len(df)} ===")
print(f"Общая сумма: {df['Сумма'].sum():,.2f} ₽")