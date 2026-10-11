import os
import time
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("WB_API_TOKEN")
headers = {"Authorization": token}

advert_ids = [
    33794542, 34065804, 34290844, 34354064, 34699343, 35360661,
    35361420, 35361427, 35418265, 37279995, 37316580, 37317285,
    37317516, 37385505, 37389967, 37420214, 37651118, 37656485,
    37658919, 37811233, 37811285, 38371157, 38371160, 38371162,
    38371164, 38840240,
]
ids_str = ",".join(str(i) for i in advert_ids)

start = datetime.now() - timedelta(days=365)
end = datetime.now()

url = "https://advert-api.wildberries.cn/adv/v3/fullstats"

total_spent = 0
all_data = []

chunk_start = start
while chunk_start < end:
    chunk_end = min(chunk_start + timedelta(days=30), end)
    d_from = chunk_start.strftime("%Y-%m-%d")
    d_to = chunk_end.strftime("%Y-%m-%d")
    
    params = {"ids": ids_str, "beginDate": d_from, "endDate": d_to}
    
    # Retry при 429
    for attempt in range(5):
        resp = requests.get(url, headers=headers, params=params, timeout=60)
        if resp.status_code == 429:
            print(f"  429, ждём 65 сек...")
            time.sleep(65)
            continue
        break
    
    print(f"{d_from} — {d_to}: status {resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()
        if data:
            all_data.extend(data)
            for camp in data:
                for day in camp.get("days", []):
                    total_spent += day.get("sum", 0)
    else:
        print(f"  Ошибка: {resp.text[:200]}")
    
    # Пауза между чанками (лимит ~1 запрос/мин)
    print("  Ждём 65 сек...")
    time.sleep(65)
    
    chunk_start = chunk_end

print(f"\n=== ИТОГО ПОТРАЧЕНО НА ПРОДВИЖЕНИЕ: {total_spent:,.2f} ¥ ===")

with open("wb_promo_stats.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)
print("Сохранено: wb_promo_stats.json")