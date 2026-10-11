# ym_campaigns.py
import os
import requests
import json
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Загружаем переменные из .env
load_dotenv()
# Присваиваем токен к переменной
token = os.getenv("YM_API_TOKEN")

url = "https://api.partner.market.yandex.ru/v2/campaigns"
headers = {"Api-Key": token}

response = requests.get(url, headers=headers, timeout=30)
print(f"Status: {response.status_code}")

data = response.json()
print(json.dumps(data, indent=2, ensure_ascii=False))

# Найди в ответе campaigns[].id (campaignId) и campaigns[].business.id (businessId)