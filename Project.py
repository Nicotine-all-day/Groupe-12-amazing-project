import random
import time

# Base Character class
class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power
    
    def take_damage(self, damage):
        self.health -= damage
        print(f"{self.name} took {damage} damage. Health left: {self.health}")
        if self.health <= 0:
            print(f"{self.name} has been defeated!")
            return True
        return False

# HammerBro as player
class HammerBro(Character):
    def __init__(self):
        super().__init__(name="Hammer Bro", health=100, attack_power=15)
    
    def throw_hammer(self, enemy):
        damage = random.randint(5, self.attack_power)
        print(f"Hammer Bro throws a hammer at {enemy.name}!")
        defeated = enemy.take_damage(damage)
        return defeated

# Enemy Characters with specific difficulties
class Enemy(Character):
    def __init__(self, name, health, attack_power, attack_pattern):
        super().__init__(name, health, attack_power)
        self.attack_pattern = attack_pattern
    
    def attack(self, player):
        if random.choice(self.attack_pattern):
            damage = random.randint(5, self.attack_power)
            print(f"{self.name} attacks Hammer Bro!")
            defeated = player.take_damage(damage)
            return defeated
        else:
            print(f"{self.name} missed the attack!")
            return False

# Game Levels
class Level:
    def __init__(self, enemies):
        self.enemies = enemies
    
    def play_level(self, player):
        for enemy in self.enemies:
            print(f"\nA wild {enemy.name} appears!")
            while enemy.health > 0 and player.health > 0:
                defeated = player.throw_hammer(enemy)
                if defeated:
                    break
                if enemy.attack(player):
                    return False  # Player defeated
        return True

# Game setup
def setup_game():
    # Define the enemies
    toad = Enemy(name="Toad", health=30, attack_power=10, attack_pattern=[True, False, False])
    peach = Enemy(name="Peach", health=40, attack_power=12, attack_pattern=[True, True, False])
    luigi = Enemy(name="Luigi", health=60, attack_power=15, attack_pattern=[True, True, False])
    mario = Enemy(name="Mario", health=100, attack_power=20, attack_pattern=[True, True, True])

    # Define levels with increasing difficulty
    level1 = Level(enemies=[toad])
    level2 = Level(enemies=[peach])
    level3 = Level(enemies=[luigi])
    final_boss_level = Level(enemies=[mario])

    return [level1, level2, level3, final_boss_level]

# Main Game Loop
def main_game():
    print("Welcome to 'The Revenge of the Hammer Bros: Power of Vengeance'")
    hammer_bro = HammerBro()
    levels = setup_game()

    for i, level in enumerate(levels):
        print(f"\n--- Starting Level {i + 1} ---")
        level_completed = level.play_level(hammer_bro)
        if not level_completed:
            print("Hammer Bro has been defeated. Game Over.")
            return
        print(f"Level {i + 1} completed!\n")
        time.sleep(1)

    print("Congratulations! You completed all levels and claimed your revenge on Mario!")

# Run the game
if __name__ == "__main__":
    main_game()
