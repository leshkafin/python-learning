def print_tasks(tasks):
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task}")

tasks = []

tasks.append(input("Введите задачу: "))
tasks.append(input("Введите задачу: "))
tasks.append(input("Введите задачу: "))

print("Твой список задач:")

print_tasks(tasks)

tasks.remove(input("Какую задачу удалить?: "))

print("Обновленный список:")

print_tasks(tasks)

    