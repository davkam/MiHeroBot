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

class Weapon(Item): # TBD: Add names!
    def __init__ (self, weapon_class: ItemClass = None, attack: Attack = None):
        self.weapon_class: ItemClass = weapon_class or ItemClass.Bronze
        self.attack: Attack = attack or Attack()

class Armor(Item): # TBD: Add names!
    def __init__ (self, armor_class: ItemClass = None, defense: Defense = None):
        self.armor_class: ItemClass = armor_class or ItemClass.Bronze
        self.defense: Defense = defense or Defense()

class Potions(Item):
    pass

class Kits(Item):
    pass

class Decorators(Item):
    pass