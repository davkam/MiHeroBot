from enum import Enum
from game.logic.stats import *

class ItemClass(Enum):
    Bronze = 2
    Iron = 4
    Steel = 6
    Mithril = 8
    Adamant = 10
    Rune = 12

class Item():
    def __init__(self):
        pass

class Inventory(Item):
    pass

class Weapon(Item):
    def __init__ (self, weapon_class: ItemClass = ItemClass.Bronze, attack: Attack = Attack()):
        self.weapon_class: ItemClass = weapon_class
        self.attack: Attack = attack

class Armor(Item):
    def __init__ (self, armor_class: ItemClass = ItemClass.Bronze, defense: Defense = Defense()):
        self.armor_class: ItemClass = armor_class
        self.defense: Defense = defense

class Potions(Item):
    pass

class Kits(Item):
    pass

class Decorators(Item):
    pass