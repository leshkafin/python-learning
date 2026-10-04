def maximum(a, b):
    if a > b:
        return a
    else:
        return b

def minimum(a, b):
    if a > b:
        return b
    else:
        return a

def average(a, b):
    return (a + b) / 2

a = int(input("Введите число 1: "))
b = int(input("Введите число 2: "))

print(maximum(a, b))
print(minimum(a, b))
print(average(a, b))