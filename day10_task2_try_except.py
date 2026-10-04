
try:
    num1 = float(input("Введите число 1: "))
    num2 = float(input("Введите число 2: "))
    print(num1 / num2)
except ValueError:
    print("Это не число")
except ZeroDivisionError:
    print("На ноль делить нельзя")