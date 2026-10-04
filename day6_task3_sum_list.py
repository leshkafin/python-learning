def maximum_number(numbers):
    maximum = numbers[0]
    for number in numbers:
        if number > maximum:
            maximum = number
    return maximum

def minimum_number(numbers):
    minimum = numbers[0]
    for number in numbers:
        if number < minimum:
            minimum = number
    return minimum

def sum_numbers(numbers):
    total = 0
    for number in numbers:
        total += number
    return total

def sort_numbers(numbers):
    numbers.sort()

def rsort_numbers(numbers):
    numbers.reverse()

numbers = [15, 3, 27, 8, 42, 1, 19]


minimum = minimum_number(numbers)
maximum = maximum_number(numbers)


total = sum_numbers(numbers)

print(f"Все числа: {numbers}")
print(f"Сумма: {total}")
print(f"Максимум: {maximum}")
print(f"Минимум: {minimum}")

sort_numbers(numbers)
print(f"Отсортировано: {numbers}")

rsort_numbers(numbers)
print(f"Обратный порядок: {numbers}")