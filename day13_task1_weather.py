import os
import requests
from dotenv import load_dotenv

load_dotenv()                           # ← читает .env
api_key = os.getenv("WEATHER_API_KEY")  # ← берёт значение

city = input("Введите город: ")

url = "https://api.openweathermap.org/data/2.5/weather"
params = {
    "q": city,
    "appid": api_key,
    "units": "metric",
    "lang": "ru"
}

response = requests.get(url, params=params) # отправляем запрос по ссылке
data = response.json()  # сохраняем ответ

# Проверь статус
if response.status_code == 200:
    # print(json.dumps(data, indent=2, ensure_ascii=False))  # для отладки формат. JSON
    temp = data["main"]["temp"]
    feels = data["main"]["feels_like"]
    desc = data["weather"][0]["description"]
    name = data["name"]
    print(f"Погода в {name}:")
    print(f"Температура: {temp}°C")
    print(f"Ощущается как: {feels}°C")
    print(f"Описание: {desc}")
elif response.status_code == 404:
    print(f"Город '{city}' не найден")
elif response.status_code == 401:
    print("Проблема с API-ключом")
else:
    print(f"Ошибка: {response.status_code}")
    print(data)