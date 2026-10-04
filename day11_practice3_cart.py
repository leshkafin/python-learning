class ShoppingCart:
    def __init__(self, owner):
        self.owner = owner
        self.items = []

    def add_item(self, name, price):
        if price > 0:
            self.items.append({"name": name, "price": price})
            return True
        return False 
            

    def remove_item(self, name):
        for i, item in enumerate(self.items):
            if item["name"] == name:
                self.items.pop(i)
                return True
        return False

    def total(self):
        total = 0
        for item in self.items:
            total += item["price"]
        return total

    def count(self):
        return len(self.items)

    def __str__(self):
        if not self.items:
            return f"Корзина {self.owner} пуста"
        return f"Корзина {self.owner}: {len(self.items)} товара на {self.total()} руб."


cart1 = ShoppingCart("Мария")

print(cart1)
print("\nДобавляю товары...")

cart1.add_item("Хлеб", 50)
cart1.add_item("Молоко", 80)
cart1.add_item("Сыр", 200)

for item in cart1.items:
    print(f"Добавлен: {item['name']}")

print(f"\n{cart1}")

cart1.add_item("Гречка", -10)

cart1.remove_item("Молоко")

print(f"\n{cart1}")

print(cart1.items)

cart1.remove_item("Пиво")

print(cart1.items)

print(f"\nИтого: {cart1.total()}")

print(f"\nТоваров: {cart1.count()}")