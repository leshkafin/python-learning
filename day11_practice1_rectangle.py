class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def is_square(self):
        return self.width == self.height

    def scale(self, factor):
        self.width *= factor
        self.height *= factor
        return self

    def __str__(self):
        if self.width == self.height:
            return f"Квадрат {self.width}x{self.height}"
        else:
            return f"Прямоугольник {self.width}x{self.height}"


rect1 = Rectangle(10, 5)

print(rect1)
print(f"Площадь: {rect1.area()}")
print(f"Периметр: {rect1.perimeter()}")
print(f"Является ли квадратом: {rect1.is_square()}")

print("\nПосле scale(2):")
print(rect1.scale(2))

print("\nПосле scale(3) через цепочку:")
print(rect1.scale(3))

rect2 = Rectangle(7, 7)

print(f"\n{rect2}")
print(f"Площадь: {rect2.area()}")
print(f"Является ли квадратом: {rect2.is_square()}")
