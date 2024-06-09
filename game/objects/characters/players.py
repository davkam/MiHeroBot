from enum import Enum
from game.features.equipment import Equipment
from game.features.inventory import Inventory
from game.logic.stats import Attack, Defense, Health
from game.objects.characters.characters import Character

class PlayerColor(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4

class Player(Character):
    def __init__ (self, name: str, attack: Attack = None, defense: Defense = None, health: Health = None, gold: int = 0, color: PlayerColor = None):
        super().__init__(name=name, attack=attack, defense=defense, health=health)
        self.equipment: Equipment = Equipment()
        self.inventory: Inventory = Inventory()
        self.gold: int = gold
        self.color: PlayerColor = color or PlayerColor.RED