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




task1 = Task("купить хлеб", "высокий")
task2 = Task("позвонить маме") # — без приоритета, будет "средний"
task3 = Task("сделать зарядку", "низкий")

print("=== Все задачи ===")
print(task1)
print(task2)
print(task3)

task1.mark_done()

print("=== После mark_done на первой ===")
print(task1)
print(task2)
print(task3)

task1.unmark_done()

print("=== После unmark_done на первой ===")
print(task1)
print(task2)
print(task3)