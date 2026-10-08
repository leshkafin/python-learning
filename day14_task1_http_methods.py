import requests


url = "https://httpbin.org"
proxies = {"http": "http://127.0.0.1:10090", "https": "http://127.0.0.1:10090"}
data = {"name": "Алексей", "age": 27}

try:
    response = requests.post(f"{url}/post", json=data, proxies=proxies, timeout=10)
    print(f"POST: {response.json()['json']}")

    response = requests.put(f"{url}/put", json={"name": "Обновлённый Алексей"}, proxies=proxies, timeout=10)
    print(f"PUT: {response.json()['json']}")

    response = requests.delete(f"{url}/delete", proxies=proxies, timeout=10)
    print(f"DELETE: {response.status_code}")

except requests.exceptions.ConnectionError:
    print("Нет соединения — проверь интернет или прокси")
except requests.exceptions.Timeout:
    print("Таймаут — сервер не отвечает")
except Exception as e:
    print(f"Ошибка: {e}")