with open("hello.txt", "w") as f:
    f.write("Привет\n")
    f.write("Это мой первый файл\n")
    f.write("Python рулит\n")           

with open("hello.txt", "r") as f:
    content = f.read()
    print(f"Так выглядит файл одной строкой:\n{content}")

with open("hello.txt", "r") as f:
    content = f.read().splitlines()
    print(f"Так выглядит файл разбитый в список:\n{content}\n")

with open("hello.txt", "a") as f:
    f.write("И это добавлено позже\n")

with open("hello.txt", "r") as f:
    content = f.read().splitlines()
    for i, data in enumerate(content,start=1):
        print(f"{i}. {data}")
