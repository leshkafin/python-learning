import requests
import json
response = requests.get("https://api.github.com/users/torvalds")

data = response.json()

print(f"Статус: {response.status_code}")
print(f"Имя: {data['name']}")
print(f"Публичных репозитариев: {data['public_repos']}")
print(f"Подписчиков: {data['followers']}")

print(json.dumps(data, indent=2, ensure_ascii=False))