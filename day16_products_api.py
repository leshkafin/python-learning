from fastapi import FastAPI

app = FastAPI()

# "База данных" — пока список словарей
products = [
    {"nm_id": 123456, "name": "Футболка", "price": 1500},
    {"nm_id": 234567, "name": "Джинсы", "price": 3500},
    {"nm_id": 345678, "name": "Кроссовки", "price": 5000},
    {"nm_id": 456789, "name": "Куртка", "price": 8000},
    {"nm_id": 567890, "name": "Шапка", "price": 800},
]  

@app.get("/products/{nm_id}")
def get_product(nm_id: int):
    for product in products:
        if product["nm_id"] == nm_id:
            return product
    return "Error: Товар не найден"

@app.get("/products")
def list_products(min_price: int = 0, max_price: int = 100000, limit: int = 10):
    filtered = [p for p in products if min_price <= p["price"] <= max_price]     # фильтр
    return filtered[:limit]                      # срез