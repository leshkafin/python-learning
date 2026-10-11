import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()
token = os.getenv("WB_API_TOKEN")

url = "https://content-api.wildberries.cn/content/v2/get/cards/list"
headers = {"Authorization": token}


all_cards = []
cursor = {"limit": 20}

while True:
    data = {"settings": {"cursor": cursor, "filter": {"withPhoto": -1}}}
    response = requests.post(url, headers=headers, json=data, timeout=30)
    result = response.json()
    
    cards = result.get("cards", [])
    all_cards.extend(cards)
    print(f"Получено: {len(cards)}, всего: {len(all_cards)}")
    
    # Курсор для следующей порции
    next_cursor = result.get("cursor", {})
    if not next_cursor.get("updatedAt"):
        break
    
    cursor = {
        "limit": 20,
        "updatedAt": next_cursor["updatedAt"],
        "nmID": next_cursor["nmID"]
    }

print(f"\nВсего товаров: {len(all_cards)}")
for c in all_cards:
    print(f"  {c['nmID']} — {c['title'][:50]}")

with open("wb_cards.json", "w", encoding="utf-8") as f:
    json.dump(all_cards, f, ensure_ascii=False, indent=2)
print("\nСохранено в wb_cards.json")