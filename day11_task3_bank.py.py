class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if amount <= self.balance:
             self.balance -= amount
             return True  
        return False

    def __str__(self):
        return f"Счёт {self.owner}: {self.balance} руб."

account1 = BankAccount("Алексей")
account2 = BankAccount("Мария", 5000)


print(account1)

account1.deposit(1000)

print(account1)

account1.deposit(-5)

print(account1)

account1.withdraw(300)

print(account1)

account1.withdraw(10000)

print(account1)

print(account2)