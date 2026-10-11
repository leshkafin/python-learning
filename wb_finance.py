import os
import requests
import json
from dotenv import load_dotenv
from datetime import datetime, timedelta


load_dotenv()
token = os.getenv("WB_API_TOKEN")

# Новый URL для финансового отчета
url = "https://finance-api.wildberries.cn/api/finance/v1/sales-reports/detailed"

# Заголовки с токеном
headers = {"Authorization": token}

# Параметры теперь передаются в теле запроса (POST)
# Указываем период, например, последние 30 дней
date_from = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
date_to = datetime.now().strftime("%Y-%m-%d")

# Тело запроса
payload = {
    "dateFrom": date_from,
    "dateTo": date_to,
    "limit": 100000  # Максимальное количество строк
}

# Выполняем POST-запрос
response = requests.post(url, headers=headers, json=payload, timeout=60)

# Проверяем статус ответа
if response.status_code == 200:
    finance_data = response.json()
    
    # Сохраняем данные в файл
    with open("wb_finance.json", "w", encoding="utf-8") as f:
        json.dump(finance_data, f, ensure_ascii=False, indent=2)
    print("Данные успешно сохранены в wb_finance.json")
    print(f"Получено записей: {len(finance_data)}")
else:
    print(f"Ошибка: {response.status_code}")
    print(response.text)