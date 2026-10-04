import random

r_number = random.randint(1,100)
counter = 0

print("Я загадал число..")
while True:
    if counter >= 10:
        print(f"Ты проиграл, было число {r_number}")
        break

    a = int(input("Угадай какое?: "))

    if a < 1 or a > 100:
        print("Не в диапазоне")
        continue
    
    counter += 1

    if a > r_number:
        print("Загаданное меньше!")

    elif a < r_number:
        print("Загаданное больше!")

    else: 
        print("Угадал!")
        break
print(f"Количество попыток: {counter}")