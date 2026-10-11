import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
token = os.getenv("WB_API_TOKEN")

url = "https://finance-api.wildberries.cn/api/finance/v1/sales-reports/detailed"
headers = {"Authorization": token}

# Период: последние 90 дней
date_from = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
date_to = datetime.now().strftime("%Y-%m-%d")

print(f"Период: {date_from} — {date_to}")

payload = {
    "dateFrom": date_from,
    "dateTo": date_to,
    "limit": 100000
}

response = requests.post(url, headers=headers, json=payload, timeout=120)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"Тип ответа: {type(data)}")
    print(f"Записей: {len(data)}")
    
    with open("wb_finance_year.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    print("Сохранено в wb_finance_year.json")
else:
    print(response.text[:500])