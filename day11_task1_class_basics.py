class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def info(self):
        return f"Книга: {self.title}, автор: {self.author}, год: {self.year}"
    
    def is_modern(self):
        return self.year >= 2000

book1 = Book("Норвежский лес", "Мураками", 2001)
book2 = Book("Титан", "Драйзер", 1914)
book3 = Book("Большая грудь", "Мо Янь", 2007)

print(book1.info())
print(f"Современная: {book1.is_modern()}")

print(book2.info())
print(f"Современная: {book2.is_modern()}")

print(book3.info())
print(f"Современная: {book3.is_modern()}")
