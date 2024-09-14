from enum import Enum
from game.logic.stats import Stat
from game.objects.items.items import Item

class EquipmentTier(Enum):
    BRONZE = 2
    IRON = 4
    STEEL = 6
    MITHRIL = 8
    ADAMANT = 10
    RUNE = 12
    DRAGON = 16

class Equipable(Item):
    def __init__(self, name: str = None, value: int = None, tier: EquipmentTier = None, level: Stat = None):
        super().__init__(name=name, value=value)
        self.tier: EquipmentTier = tier or EquipmentTier.BRONZE
        self.level: Stat = level or Stat()

    def set_name(self, type: str = "EQUIPMENT"):
        super().set_name(name=f"LVL.{self.level.get_lvl()} {self.tier.name} {type}")

    async def get_random_equipable(self, equip_index: int, avg_stats: int):
        pass

class Sword(Equipable):
    def __init__ (self, name: str = None, value: int = None, tier: EquipmentTier = None, level: Stat = None):
        super().__init__(name=name, value=value, tier=tier, level=level)
        self.set_name()

    def set_name(self):
        super().set_name(type="SWORD")

class Shield(Equipable):
    def __init__ (self, name: str = None, value: int = None, tier: EquipmentTier = None, level: Stat = None):
        super().__init__(name=name, value=value, tier=tier, level=level)
        self.set_name()

    def set_name(self):
        super().set_name(type="SHIELD")

class HeadArmor(Equipable):
    def __init__ (self, name: str = None, value: int = None, tier: EquipmentTier = None, level: Stat = None):
        super().__init__(name=name, value=value, tier=tier, level=level)
        self.set_name()

    def set_name(self):
        super().set_name(type="HEAD")

class BodyArmor(Equipable):
    def __init__ (self, name: str = None, value: int = None, tier: EquipmentTier = None, level: Stat = None):
        super().__init__(name=name, value=value, tier=tier, level=level)
        self.set_name()

    def set_name(self):
        super().set_name(type="BODY")

class Amulet(Equipable): # TBD: SPECIAL EFFECT AMULETS/DECORATOR
    def __init__ (self, name: str = None, value: int = None, tier: EquipmentTier = None, level: Stat = None):
        super().__init__(name=name, value=value, tier=tier, level=level)
        self.set_name()

    def set_name(self):
        super().set_name(type="AMULET")

class Ring(Equipable): # TBD: SPECIAL EFFECT RINGS/DECORATOR
    def __init__ (self, name: str = None, value: int = None, tier: EquipmentTier = None, level: Stat = None):
        super().__init__(name=name, value=value, tier=tier, level=level)
        self.set_name()

    def set_name(self):
        super().set_name(type="RING")