import pandas as pd
import json

# Открываем файл для чтения, и записываем его как json в словарь data
with open("wb_finance_year.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Конструктор pd.DataFrame() принимает на вход данные и возвращает объект DataFrame. 
df = pd.DataFrame(data)

# Вывод всех колонок
for i, col in enumerate(df.columns,start=1): 
    print(f"{i}. {col}")  

# Создаёт новый DataFrame, который содержит те же строки, что и df, но только столбцы в указанном порядке: 
# Остальные столбцы исходного DataFrame будут отброшены.
df = df[["vendorCode", "forPay", "deliveryService", 
         "paidStorage", "deduction", "penalty", "quantity"]]

# Создаем список с колонками для преобразования в числа
cols_to_convert = ["forPay", "deliveryService", "paidStorage", "deduction", "penalty", "quantity"]
# Функция pd.to_numeric() преобразует значения колонки в числовой тип.
# errors="coerce" - что не число будет заменено на NaN
# .fillna(0) заменяет все полученные NaN на ноль
for col in cols_to_convert:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# Группируем значения по "vendorCode" - это артикул товара на WB
grouped = df.groupby("vendorCode").sum()

# Читаем файл cost_cny.csv и делаем список cost_df
cost_df = pd.read_csv("cost_cny.csv")

# Склеиваем 2 таблицы, флаг - индекс 1й таблицы совпадает с supplierArticle 2й таблицы
merged = pd.merge(grouped, cost_df, left_index=True, right_on="supplierArticle", how="left")
# Делаем из колонки supplierArticle - индекс
merged = merged.set_index("supplierArticle")
#Сортируем по алфавиту
merged = merged.sort_index()

# Удаляем пустые строки
merged = merged[merged.index != ""]

print(merged)

# Полный себес = цена за штуку × количество
merged["total_cost"] = merged["cost_cny"] * merged["quantity"]

# Прибыль = доход − все расходы
merged["profit"] = (
    merged["forPay"]
    - merged["deliveryService"]
    - merged["paidStorage"]
    - merged["deduction"]
    - merged["penalty"]
    - merged["total_cost"]
)

# Вывод: артикул + ключевые метрики
print("\nВывод: артикул + ключевые метрики")
print(merged[["forPay", "total_cost", "profit"]])
print(f"\nОбщая прибыль (без рекламы): {merged['profit'].sum():,.2f} ¥")

# Реальные расходы на рекламу (списания со СЧЁТА из ЛК WB)
REAL_PROMO_RUB = 116163
RATE = 12
real_promo_cny = REAL_PROMO_RUB / RATE

print(f"\n=== ФИНАЛ ===")
print(f"Прибыль (с deduction): {merged['profit'].sum():,.2f} ¥")
print(f"Списано со счёта: {REAL_PROMO_RUB:,.0f} ₽ = {real_promo_cny:,.2f} ¥")
final = merged['profit'].sum() - real_promo_cny
print(f"ЧИСТАЯ ПРИБЫЛЬ: {final:,.2f} ¥")
print(f"Маржа: {final / merged['forPay'].sum() * 100:.2f} %")