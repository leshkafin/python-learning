# Python Learning Journey

Мои проекты и упражнения по Python. Учусь с нуля.

## Что здесь

- `day4_*` — циклы, `while`, `for`, `break`, `continue`
- `day5_*` — функции, `return`, рефакторинг
- `day6_*` — списки, To-Do в консоли
- `day7_*` — словари, телефонная книга
- `day8_*` — работа с файлами, сохранение данных
- `day9_*` — модули, `pip`, работа с API (`requests`)
- `day10_*` — срезы, `try/except`
- `day11_*` — ООП: классы, методы, `__str__`, `TodoList` с сохранением

## Стек

- Python 3.14
- `requests` для API
- Git для версионирования

## WB Analytics

Для запуска нужны:
1. `WB_API_TOKEN` в `.env`
2. Запустить `wb_orders.py`, `wb_sales.py`, `wb_cards.py` — создадут JSON-файлы
3. Создать `cost.csv` со своими себестоимостями:
supplierArticle,cost_rub
YOUR-SKU-1,1000
YOUR-SKU-2,500
4. Запустить `wb_analyze.py`
