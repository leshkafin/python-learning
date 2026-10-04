def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b
 
def integer_divide(a, b):
    return a // b

def modulo(a, b):
    return a % b

def power(a, b):
    return a ** b

try:
    a = int(input("Введите число 1: "))
    b = int(input("Введите число 2: "))    
except ValueError:
    print("Это не число")
    exit()

print(add(a,b))
print(subtract(a,b))
print(multiply(a,b))
print(power(a,b))

try:
    print(divide(a,b))
    print(integer_divide(a,b))
    print(modulo(a,b))
except ZeroDivisionError:
    print("На ноль делить нельзя - /, //, %")  

