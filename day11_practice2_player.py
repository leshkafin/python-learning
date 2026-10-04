class Player:
    def __init__(self, name, hp=100, attack=10):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.max_hp = hp
    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            return True
        return False 
    def heal(self, amount):
        if self.is_alive():
            self.hp += amount
            if self.hp > self.max_hp:
                self.hp = self.max_hp
        else:
            return False

    def is_alive(self):
        return self.hp > 0
        

    def __str__(self):
        return f"Игрок {self.name}: HP {self.hp}/{self.max_hp} (атака {self.attack})"
        
player1 = Player("Алексей")

print(player1)

player1.take_damage(30)
print(f"\nПосле атаки на 30: \n{player1}")

player1.take_damage(50)
print(f"\nПосле атаки на 50: \n{player1}")


player1.heal(15)
print(f"\nПосле лечения на 15: \n{player1}")

player1.heal(200)
print(f"\nПосле лечения на 200: \n{player1}")

player1.take_damage(150)
print(f"\nПосле атаки на 150: \n{player1}")

player1.heal(50)
print(f"\nПопытка лечить мертвого: \n{player1}")

print(f"Жив: {player1.is_alive()}")


player2 = Player("Маг", hp=50, attack=30)

print(player2)

player2.take_damage(30)
print(player2)
player2.take_damage(50)
print(player2)
