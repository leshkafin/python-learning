import os
import requests
import json
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Загружаем переменные из .env
load_dotenv()
# Присваиваем токен к переменной
token = os.getenv("WB_API_TOKEN")



# Дата 7 дней назад в формате "ГГГГ-ММ-ДД"
date_from = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
print(date_from)

# URL для заказов
url = "https://statistics-api.wildberries.cn/api/v1/supplier/sales"

# Заголовки
headers = {"Authorization": token}

# Параметры (dateFrom)
params = {"dateFrom": date_from}

response = requests.get(url, headers=headers, params=params, timeout=30)
print(response.status_code)

print(len(response.json()))

print(response.text[:500])

with open("wb_sales.json", "w", encoding="utf-8") as f:
    json.dump(response.json(), f, ensure_ascii=False, indent=2)
print("Сохранено в wb_sales.json")