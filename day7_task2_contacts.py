def print_contacts(contacts):
    print("\nВаши контакты: ")
    for i, contact in enumerate(contacts, start=1):
        print(f"{i}. {contact['name']}, {contact['phone']}")

def add_contact(contacts):
    new_contact = {
        "name": input("Введите имя: "), 
        "phone": input("Введите телефон: ")
    }
    contacts.append(new_contact)
    print("\n**Контакт успешно добавлен!**")

def find_contacts(contacts):
    find_who = input("Кого нужно найти? ")
    for contact in contacts:
        if contact["name"] == find_who:
            print("\n**Контакт найден!**")
            print(f"{contact['name']}, {contact['phone']}")
            break
    else:
        print("\n**Контакт не найден**")
            
def remove_contacts(contacts):
    remove_who = input("Кого нужно удалить?: ")

    # Ищем контакт
    found = None
    for contact in contacts:
          if contact["name"] == remove_who:
              found = contact
              break
    if found is None:
        print("\n**Контакт не найден**")
        return
    
    # Показываем, кого нашли
    print(f"Найден: {found['name']}, {found['phone']}")

    # Спрашиваем подтверждение  
    confirmation = input("Точно удаляем? Y/N: ")
    if confirmation.lower() == "y":
        contacts.remove(found)
        print("\n**Контакт удалён**")
    else:
        print("\n**Контакт не удален**")


contacts = [
    {"name": "Алексей", "phone": "+79991112233"},
    {"name": "Мария",   "phone": "+79994445566"},
    {"name": "Иван",    "phone": "+79997778899"}
]

while True:
    print("\n--- МЕНЮ ---")
    print("1. Показать контакты")
    print("2. Добавить контакт")
    print("3. Найти контакт")
    print("4. Удалить контакт")
    print("5. Выход")
      
    choice = input("Выбери пункт: ")

    if choice == "1":
        print_contacts(contacts)
    elif choice == "2":
        add_contact(contacts)
    elif choice == "3":
        find_contacts(contacts)
    elif choice == "4":
        remove_contacts(contacts)
    elif choice == "5":
        print("Пока!")
        break
    else:
        print("Неверный пункт, попробуй снова")
        




            

