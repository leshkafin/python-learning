with open("numbers.txt", "w") as f:
    f.write("15\n")
    f.write("3\n")
    f.write("27\n")
    f.write("8\n")
    f.write("42\n")    

with open("numbers.txt", "r") as f:
    content = f.read().splitlines()
    print(f"Числа из файла, как str: {content}")

#Преобразование строк в числа через цикл
#numbers = []
#with open("numbers.txt", "r") as f:
#   for line in f:
#        numbers.append(int(line.strip()))


with open("numbers.txt", "r") as f:
    numbers = [int(line.strip()) for line in f]

print(f"Числа из файла, как int: {numbers}")

#Сумма через копилку:
#total = 0
#for number in numbers:
    #total += number
#print(f"Сумма: {total}")

print(f"Сумма: {sum(numbers)}")
print(f"Максимум: {max(numbers)}")
print(f"Минимум: {min(numbers)}")