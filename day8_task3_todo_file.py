def load_tasks(filename):
    # Читает файл, возвращает список задач
    try:
        with open(filename, "r") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return []          # файла нет — вернём пустой список

def save_tasks(tasks, filename):
    # Сохраняет список задач в файл
    with open(filename, "w") as f:
        f.write("\n".join(tasks))

def print_tasks(tasks):
    if not tasks:
        print("\n**Задач нет**")
        return
    print("\nСписок задач: ")    
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task}")


FILENAME = "tasks.txt"
tasks = load_tasks(FILENAME)

while True:
    print("\n--- МЕНЮ ---")
    print("1. Показать задачи")
    print("2. Добавить задачу")
    print("3. Удалить задачу")
    print("4. Выход")
    
    choice = input("Выбери пункт: ")
    
    if choice == "1":
   
        print_tasks(tasks)

    elif choice == "2":
        task = input("Введи задачу: ")
        tasks.append(task)
        save_tasks(tasks, FILENAME)
        print(f"\n✅ Добавлено: {task}")

    elif choice == "3":
        removing_task = input("Какую задачу удалить?: ")
        if removing_task in tasks:
            tasks.remove(removing_task)
            save_tasks(tasks, FILENAME)
            print(f"\n🗑 Удалено: {removing_task}")
        else:
            print("\n**Такой задачи нет**")

    elif choice == "4":
        print("Пока!")
        break
    else:
        print("Неверный пункт, попробуй снова")