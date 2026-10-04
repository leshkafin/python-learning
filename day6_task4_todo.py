tasks = []

while True:
    print("\n--- МЕНЮ ---")
    print("1. Показать задачи")
    print("2. Добавить задачу")
    print("3. Удалить задачу")
    print("4. Выход")
    
    choice = input("Выбери пункт: ")
    
    if choice == "1":
        print("\nСписок задач: ")
        if not tasks:
            print("**Задач нет**")
        else:
            for i, task in enumerate(tasks,start=1):
                print(f"{i}. {task}")

    elif choice == "2":
        task = input("Введи задачу: ")
        tasks.append(task)
        print(f"\n✅ Добавлено: {task}")

    elif choice == "3":
        removing_task = input("Какую задачу удалить?: ")
        if removing_task in tasks:
            tasks.remove(removing_task)
            print(f"\n🗑 Удалено: {removing_task}")
        else:
            print("\n**Такой задачи нет**")

    elif choice == "4":
        print("Пока!")
        break
    else:
        print("Неверный пункт, попробуй снова")