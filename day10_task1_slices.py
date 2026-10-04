numbers = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

print(f"Первые 3: {numbers[:3]}")
print(f"Последние 3: {numbers[-3:]}")
print(f"С 3-го по 6-й: {numbers[2:6]}")
print(f"Каждый второй: {numbers[::2]}")
print(f"Развёрнутый: {numbers[::-1]}")

text = "Python — это круто"

print(f"Первые 6 символов: {text[:6]}")
print(f"Последние 5 символов: {text[-5:]}")
print(f"Развёрнутая строка: {text[::-1]}")