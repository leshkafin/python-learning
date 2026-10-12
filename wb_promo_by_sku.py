import json
import pandas as pd
from collections import defaultdict


# Загружаем карточки
with open("wb_cards.json", "r", encoding="utf-8") as f:
    cards = json.load(f)

print(f"Карточек: {len(cards)}")
print(f"Пример первой:")

# Выводим ключи первого элемента списка
print(cards[0].keys())

# Связываем nmID / vendorCode в отдельный словарь
nm_to_vendor = {}
for card in cards:
    nm_to_vendor[card["nmID"]] = card["vendorCode"]

print(f"Связей: {len(nm_to_vendor)}")
for nm, vc in list(nm_to_vendor.items())[:11]:
    print(f"  {nm} → {vc}")

# Загружаем данные по рекламе WB
with open("wb_promo_stats.json", "r", encoding="utf-8") as f:
    promo = json.load(f)

print(f"Кампаний: {len(promo)}")

# Копилка уникальных nmID （WB item number）
promo_by_nm = defaultdict(float)
for camp in promo:
    days = camp.get("days", [])
    for day in days:
        apps = day.get("apps", [])
        for app in apps:
            nms = app.get("nms", [])
            for nm in nms:
                nm_id = nm["nmId"]
                cost = nm.get("sum", 0)
                promo_by_nm[nm_id] += cost

print(f"Уникальных nmId: {len(promo_by_nm)}")
print(f"Общая сумма: {sum(promo_by_nm.values()):,.2f} ₽")

print(f"\n=== Содержимое promo_by_nm ===")
for nm_id in promo_by_nm:
    amount = promo_by_nm[nm_id]
    vendor = nm_to_vendor.get(nm_id, "?")
    print(f"  {nm_id} ({vendor}): {amount:>10,.2f} ₽")
    

# Копилка по артикулу
promo_by_vendor = defaultdict(float)

# Проходим по всем nm_id
for nm_id in promo_by_nm:
    amount_rub = promo_by_nm[nm_id]
    vendor = nm_to_vendor.get(nm_id, "UNKNOWN")
    promo_by_vendor[vendor] += amount_rub

# Сортируем
items = list(promo_by_vendor.items())
items.sort(key=lambda x: x[1], reverse=True)

# Выводим
print(f"\n=== Реклама по артикулам ===")
RATE = 12
for vendor, amount_rub in items:
    amount_cny = amount_rub / RATE
    print(f"  {vendor}: {amount_rub:>10,.2f} ₽  →  {amount_cny:>8,.2f} ¥")