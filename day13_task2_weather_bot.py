import os
import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("WEATHER_API_KEY")

session = AiohttpSession(proxy="http://127.0.0.1:10090")
bot = Bot(token=TOKEN, session=session)


# Прокси для requests (погода)
os.environ["HTTP_PROXY"] = "http://127.0.0.1:10090"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:10090"

# Прокси для aiogram (Telegram)
session = AiohttpSession(proxy="http://127.0.0.1:10090")
bot = Bot(token=TOKEN, session=session)
dp = Dispatcher()


def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }
    proxies = {
        "http": "http://127.0.0.1:10090",
        "https": "http://127.0.0.1:10090"
    }
    response = requests.get(url, params=params, proxies=proxies, timeout=10)


    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        name = data["name"]
        return f"Погода в {name}: {temp}°C, {desc}"
    elif response.status_code == 404:
        return f"Город '{city}' не найден"
    else:
        return f"Ошибка: {response.status_code}"

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Напиши город, и я скажу погоду.")

@dp.message()
async def handle_city(message: types.Message):
    city = message.text
    result = get_weather(city)
    await message.answer(result)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())