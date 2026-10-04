class Task:
    def __init__(self, name, priority="средний"):
        self.name = name
        self.priority = priority
        self.done = False

    def __str__(self):
        status = "[✓]" if self.done else "[ ]"
        return f"{status} {self.name} ({self.priority})"

    def mark_done(self):
        self.done = True

    def unmark_done(self):
        self.done = False



class TodoList:
    def __init__(self, owner, filename="tasks.txt"):
        self.owner = owner
        self.tasks = []
        self.filename = filename
        self.load()                              # ← загружаем сразу

    def add(self, name, priority="средний"):
        if self.find(name) is not None:
            return False
        self.tasks.append(Task(name, priority))
        self.save()                    # ← сохранить после изменения
        return True

    def find(self, name):
        for task in self.tasks:
            if task.name == name:
                return task
        return None     

    def remove(self, name):
        task = self.find(name)
        if task is None:
            return False
        self.tasks.remove(task)
        self.save()                    # ← сохранить после изменения
        return True

    def mark_done(self, name):
        task = self.find(name)
        if task is None:
            return False
        task.mark_done()
        self.save()                    # ← сохранить после изменения
        return True

    def count(self):
        return len(self.tasks)

    def count_done(self):
        return sum(1 for task in self.tasks if task.done)

    def unmark_done(self, name):
        task = self.find(name)
        if task is None:
            return False
        task.unmark_done()
        self.save()   
        return True

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            for task in self.tasks:
                f.write(f"{task.name}|{task.priority}|{task.done}\n")

    def load(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                for line in f:
                    name, priority, done = line.strip().split("|")
                    task = Task(name, priority)
                    task.done = done == "True"
                    self.tasks.append(task)
        except FileNotFoundError:
            pass

    def __str__(self):
        if not self.tasks:
            return f"\nСписок задач {self.owner} пуст"
        lines = []
        for i, task in enumerate(self.tasks,start=1):
            lines.append(f"{i}. {task}")
        return "\n".join(lines)

owner1 = TodoList("Алексей")

while True:
    print("\n--- МЕНЮ ---")
    print("1. Показать задачи")
    print("2. Добавить задачу")
    print("3. Удалить задачу")
    print("4. Выход")
    
    choice = input("Выбери пункт: ")
    
    if choice == "1":
        print(owner1)

    elif choice == "2":
        name = input("\nВведи название задачи: ")
        if owner1.add(name):
            print(f"\n✅ Добавлено: {name}")
        else:
            print(f"\n❌ Задача '{name}' уже есть")

    elif choice == "3":
        name = input("\nВведи название задачи: ")
        if owner1.remove(name):
            print(f"\n🗑 Удалено: {name}")
        else:
            print(f"\n❌ Не найдено: {name}")

    elif choice == "4":
        print("Пока!")
        break
    else:
        print("Неверный пункт, попробуй снова")



