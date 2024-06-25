import random

from enum import Enum
from game.logic.stats import Attack, Defense, Health, Level
from game.objects.characters.characters import Character

class EnemyRank(Enum):
    LIGHT = 2
    MEDIUM = 6
    HEAVY = 10
    BOSS = 14

class Enemy(Character):
    def __init__ (self, name: str = None, attack: Attack = None, defense: Defense = None, health: Health = None, rank: EnemyRank = None):
        super().__init__(name=name, attack=attack, defense=defense, health=health)
        self.rank: EnemyRank = rank or EnemyRank.LIGHT

class Boss(Enemy):
    def __init__ (self, name: str = None, attack: Attack = None, defense: Defense = None, health: Health = None, rank: EnemyRank = None):
        super().__init__(name=name, attack=attack, defense=defense, health=health, rank=rank)

class Monster(Enemy):
    def __init__ (self, name: str = None, attack: Attack = None, defense: Defense = None, health: Health = None, rank: EnemyRank = None):
        super().__init__(name=name, attack=attack, defense=defense, health=health, rank=rank)

    async def generate_monster(self, rank: EnemyRank, level: Level) -> None:
        # Assign name to monster and rng attributes according to rank
        if rank == EnemyRank.LIGHT:
            self.name = "LIGHT MONSTER"
            low = 750; high = 1250
        elif rank == EnemyRank.MEDIUM:
            self.name = "MEDIUM MONSTER"
            low = 1000; high = 1500
        elif rank == EnemyRank.HEAVY:
            self.name = "HEAVY MONSTER"
            low = 1500; high = 2000

        self.rank = rank

        # Return with default values if argument level is 1
        if level.get_lvl() == 1:
            return
        
        # Set monster level based on argument level and rng attributes
        if level.get_lvl() < 100:
            monster_level = level.get_lvl() * (random.randint(low, high) / 1000)
        else:
            monster_level = 100

        # Distrubute 75% of monster level evenly to attack, defense and health
        monster_attack = monster_level * 0.75
        monster_defense = monster_level * 0.75
        monster_health = monster_level * 0.75

        # Distrubute remaining 25% of monster level randomly to attack, defense and health based on an rng priority
        level_remaining = (monster_level * 0.25) * 3
        rng = random.randint(1, 3)
        if rng == 1:       
            rng = random.randint(0, 100) / 100
            monster_attack += level_remaining * rng
            level_remaining -= level_remaining * rng

            rng = random.randint(1, 2)
            if rng == 1:
                rng = random.randint(0, 100) / 100
                monster_defense += level_remaining * rng
                level_remaining -= level_remaining * rng
                monster_health += level_remaining
            elif rng == 2:
                rng = random.randint(0, 100) / 100
                monster_health += level_remaining * rng
                level_remaining -= level_remaining * rng
                monster_defense += level_remaining

        elif rng == 2:
            rng = random.randint(0, 100) / 100
            monster_defense += level_remaining * rng
            level_remaining -= level_remaining * rng

            rng = random.randint(1, 2)
            if rng == 1:
                rng = random.randint(0, 100) / 100
                monster_attack += level_remaining * rng
                level_remaining -= level_remaining * rng
                monster_health += level_remaining
            elif rng == 2:
                rng = random.randint(0, 100) / 100
                monster_health += level_remaining * rng
                level_remaining -= level_remaining * rng
                monster_attack += level_remaining

        elif rng == 3:
            rng = random.randint(0, 100) / 100
            monster_health += level_remaining * rng
            level_remaining -= level_remaining * rng

            rng = random.randint(1, 2)
            if rng == 1:
                rng = random.randint(0, 100) / 100
                monster_attack += level_remaining * rng
                level_remaining -= level_remaining * rng
                monster_defense += level_remaining
            elif rng == 2:
                rng = random.randint(0, 100) / 100
                monster_defense += level_remaining * rng
                level_remaining -= level_remaining * rng
                monster_attack += level_remaining
        
        self.level.set_lvl(monster_level)
        self.attack.set_lvl(monster_attack)
        self.defense.set_lvl(monster_defense)
        self.health.set_lvl(monster_health) 