

savings = float(input("Cколько откладываешь в месяц?: "))
months = int(input("На сколько месяцев?: "))
percent = float(input("Какая ставка в %?: "))

total = 0
month_percent = percent / 12 / 100

for i in range(1, months + 1):
    total += savings
    total += total * month_percent
    print(f"Месяц {i}: {total:.2f}$")

print(f"\nИтого накопится: {total:.2f}$")
    