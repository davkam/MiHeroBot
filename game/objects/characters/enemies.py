from enum import Enum
from game.logic.stats import Attack, Defense, Health
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