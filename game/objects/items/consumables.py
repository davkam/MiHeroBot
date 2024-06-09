from enum import Enum
from game.objects.items.items import Item

class ConsumableTier(Enum):
    REGULAR = 1
    SUPER = 2
    DIVINE = 3

class PotionType(Enum):
    ATTACK = 1
    DEFENSE = 2
    HEALTH = 3

class KitType(Enum):
    WEAPON = 1
    SHIELD = 2
    HEAD_ARMOR = 3
    BODY_ARMOR = 4
    AMULET = 5

class Consumable(Item):
    def __init__(self, id: int = None, name: str = None, value: int = None, tier: ConsumableTier = None):
        super().__init__(id=id, name=name, value=value)
        self.tier: ConsumableTier = tier or ConsumableTier.REGULAR

class Potion(Consumable):
    def __init__(self, id: int = None, name: str = None, value: int = None, consumable_class: ConsumableTier = None, type: PotionType = None):
        super().__init__(id=id, name=name, value=value, tier=consumable_class)
        self.type: PotionType = type

class Kit(Item):
    def __init__(self, id: int = None, name: str = None, value: int = None, consumable_class: ConsumableTier = None, type: PotionType = None):
        super().__init__(id=id, name=name, value=value, consumable_class=consumable_class)
        self.type: KitType = type