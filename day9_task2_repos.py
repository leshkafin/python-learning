import requests
import json

username = input("Введите имя пользователя GitHub (например, torvalds): ")

url = f"https://api.github.com/users/{username}/repos"

response = requests.get(url)

data = response.json()

if response.status_code == 200:
    for i, repo in enumerate(data[:5], start=1):
        print(f"{repo['name']} - ⭐ {repo['stargazers_count']}")
elif response.status_code == 404:
    print("Пользователь не найден")
else:
    print(f"Ошибка: код {response.status_code}")

#print(json.dumps(data, indent = 2, ensure_ascii=False))


