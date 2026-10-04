person = {
    "name": "Aleksei", "age": 27, "city": "Ningbo", "hobby": "entrepreneurship"
}

print(f"Name: {person['name']}")
print(f"Age: {person['age']}")
print(f"City: {person['city']}")
print(f"Hobby: {person['hobby']}")

person["email"] = "alex@gmail.com"

print(f"Email: {person['email']}")

person["age"] += 1


print("\nВсе поля:")

for key, value in person.items():
    print(f"{key}: {value}")

print(f"\nВсего полей: {len(person)}")