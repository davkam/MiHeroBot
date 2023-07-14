from enum import Enum
from game.logic.stats import *
import asyncio
import random

class GearType(Enum):
    BRONZE = 2
    IRON = 4
    STEEL = 6
    MITHRIL = 8
    ADAMANT = 10
    RUNE = 12

class PotionType(Enum):
    ATTACK = 1
    DEFENSE = 2
    HEALTH = 3

class KitType(Enum):
    WEAPON = 1
    ARMOR = 2

class Item():
    def __init__(self, name: str = None, value: int = None):
        self.name: str = name
        self.value: int = value

    async def randomize_item(self, item_index: int, gear_allowed: bool, avg_stats: float = None):
        random_item = None

        if gear_allowed == True:
            rng = random.randint(1, 2)
            if rng == 1: 
                random_item = Weapon()
                await random_item.randomize_weapon(weapon_index=item_index, avg_stats=avg_stats)
                return random_item
            else: # rng == 2:
                random_item = Armor()
                await random_item.randomize_armor(armor_index=item_index, avg_stats=avg_stats)
                return random_item
        
        if item_index == 1 or item_index == 2:
            rng = random.randint(1, 2)
            if rng == 1:
                random_item = Potion()
                await random_item.randomize_potion(potion_index=item_index)
            else: # rng == 2:
                random_item = Kit()
                await random_item.randomize_kit(item_index)
        else: # item_index == 3:
            rng = random.randint(0, 100)
            if rng < 45:
                random_item = Potion()
                await random_item.randomize_potion(potion_index=item_index)
            elif rng >= 45 and rng < 90:
                random_item = Kit()
                await random_item.randomize_kit(kit_index=item_index)
            else:
                random_item = Decorator()
                await random_item.randomize_decorator(decorator_index=item_index)

        return random_item
    
    

class Weapon(Item): # TBD: Change attack attribute name to level and type to Stats()?
    def __init__ (self, weapon_class: GearType = None, attack: Attack = None):
        Item.__init__(self)
        self.weapon_class: GearType = weapon_class or GearType.BRONZE
        self.attack: Attack = attack or Attack()
        self.name: str = f"LVL.{self.attack.get_lvl()} {self.weapon_class.name} WEAPON"
        
    async def set_name(self):
        self.name: str = f"LVL.{self.attack.get_lvl()} {self.weapon_class.name} WEAPON"

    async def randomize_weapon(self, weapon_index: int, avg_stats: float):
        # Sets rng variables based on weapon index.
        if weapon_index == 1:
            var_1 = 0; var_2 = 10; var_3 = 50; var_4 = 250; var_5 = 500
            var_A = 50; var_B = 150
        if weapon_index == 2:
            var_1 = 10; var_2 = 50; var_3 = 100; var_4 = 500; var_5 = 1000
            var_A = 75; var_B = 175
        if weapon_index == 3:
            var_1 = 50; var_2 = 100; var_3 = 250; var_4 = 1000; var_5 = 0
            var_A = 100; var_B = 200

        # Sets gear type randomly based on rng variables.
        rng = random.randint(0, 1000)
        if rng < var_1: self.weapon_class = GearType.RUNE
        elif rng < var_2: self.weapon_class = GearType.ADAMANT
        elif rng < var_3: self.weapon_class = GearType.MITHRIL
        elif rng < var_4: self.weapon_class = GearType.STEEL
        elif rng < var_5: self.weapon_class = GearType.IRON
        else: self.weapon_class = GearType.BRONZE

        # Sets weapon attack level based on rng variables.
        level = round(avg_stats * (random.randint(var_A, var_B) / 100), 2)
        self.attack.set_lvl(lvl=level)
        await self.set_name()

    async def upgrade_weapon(self):
        pass

    async def value_weapon(self):
        pass

class Armor(Item): # TBD: Change defense attribute name to level and type to Stats()?
    def __init__ (self, armor_class: GearType = None, defense: Defense = None):
        Item.__init__(self)
        self.armor_class: GearType = armor_class or GearType.BRONZE
        self.defense: Defense = defense or Defense()
        self.name: str = f"LVL.{self.defense.get_lvl()} {self.armor_class.name} ARMOR"
    
    async def set_name(self):
        self.name: str = f"LVL.{self.defense.get_lvl()} {self.armor_class.name} ARMOR"

    async def randomize_armor(self, armor_index: int, avg_stats: float):
        # Sets rng variables based on armor index.
        if armor_index == 1:
            var_1 = 0; var_2 = 10; var_3 = 50; var_4 = 250; var_5 = 500
            var_A = 50; var_B = 150
        if armor_index == 2:
            var_1 = 10; var_2 = 50; var_3 = 100; var_4 = 500; var_5 = 1000
            var_A = 75; var_B = 175
        if armor_index == 3:
            var_1 = 50; var_2 = 100; var_3 = 250; var_4 = 1000; var_5 = 0
            var_A = 100; var_B = 200

        # Sets gear type randomly based on rng variables.
        rng = random.randint(0, 1000)
        if rng < var_1: self.armor_class = GearType.RUNE
        elif rng < var_2: self.armor_class = GearType.ADAMANT
        elif rng < var_3: self.armor_class = GearType.MITHRIL
        elif rng < var_4: self.armor_class = GearType.STEEL
        elif rng < var_5: self.armor_class = GearType.IRON
        else: self.armor_class = GearType.BRONZE

        # Sets armor defense level based on rng variables.
        level = round(avg_stats * (random.randint(var_A, var_B) / 100), 2)
        self.defense.set_lvl(lvl=level)
        await self.set_name()   

    async def upgrade_armor(self):
        pass

    async def value_armor(self):
        pass

class Potion(Item):
    def __init__(self, potion_type: PotionType = None, potion_quality: int = None):
        super().__init__(self)
        self.potion_type: PotionType = potion_type
        self.potion_quality: int = potion_quality   # Represents regular, super or divine potion (1, 2 or 3 respectively).

    async def set_name(self):
        if self.potion_quality == 1:
            self.name = f"{self.potion_type.name} XP POTION"
        elif self.potion_quality == 2:
            self.name = f"SUPER {self.potion_type.name} XP POTION"
        else: #self.potion_quality == 3:
            self.name = f"DIVINE {self.potion_type.name} XP POTION"

    async def randomize_potion(self, potion_index: int):
        rng = random.randint(1, 3)
        if rng == 1: self.potion_type = PotionType.ATTACK
        elif rng == 2: self.potion_type = PotionType.DEFENSE
        else: self.potion_type = PotionType.HEALTH

        if potion_index == 1:
            varA = 0; varB = 25
        elif potion_index == 2:
            varA = 10; varB = 50
        else:
            varA = 25; varB = 100

        rng = random.randint(0, 100)
        if rng < varA: self.potion_quality = 3
        elif rng < varB: self.potion_quality = 2
        else: self.potion_quality = 1

        await self.set_name()

    async def use_potion(self, player):
        from game.objects.characters import Player
        pass

    async def value_potion(self):
        pass

class Kit(Item):
    def __init__(self, kit_type: PotionType = None, kit_quality: int = None):
        super().__init__(self)
        self.kit_type: KitType = kit_type
        self.kit_quality: int = kit_quality   # Represents regular, super or divine kit (1, 2 or 3 respectively).

    async def set_name(self):
        if self.kit_quality == 1:
            self.name = f"{self.kit_type.name} KIT"
        elif self.kit_quality == 2:
            self.name = f"SUPER {self.kit_type.name} KIT"
        else: #self.kit_quality == 3:
            self.name = f"DIVINE {self.kit_type.name} KIT"

    async def randomize_kit(self, kit_index: int):
        rng = random.randint(1, 2)
        if rng == 1: self.kit_type = KitType.WEAPON
        else: self.kit_type = KitType.ARMOR

        if kit_index == 1:
            varA = 0; varB = 25
        elif kit_index == 2:
            varA = 10; varB = 50
        else:
            varA = 25; varB = 100

        rng = random.randint(0, 100)
        if rng < varA: self.kit_quality = 3
        elif rng < varB: self.kit_quality = 2
        else: self.kit_quality = 1

        await self.set_name()

    async def use_kit(self, player):
        from game.objects.characters import Player
        pass

    async def value_kit(self):
        pass

class Decorator(Item):
    tier1_decorators = list[str]
    tier2_decorators = list[str]
    tier3_decorators = list[str]

    def __init__(self, emoji: str = None, tier: int = None):
        super().__init__(self)
        self.emoji: str = emoji
        self.tier: int = tier   # Represents decorator tiers (1, 2 or 3)

    async def set_name(self):
        self.name = f"TIER {self.tier}. DECORATOR: {self.emoji}"

    async def randomize_decorator(self, decorator_index: int):
        # if decorator_index == 3:
        #     varA = 10; varB = 25

        # rng = random.randint(0, 100)
        # if rng < varA: self.tier = 3
        # elif rng < varB: self.tier = 2
        # else: self.tier = 1

        # if self.tier == 1:
        #     last_index = len(Decorator.tier1_decorators) - 1
        #     rng = random.randint(0, last_index)
        #     self.emoji = Decorator.tier1_decorators[rng]
        # elif self.tier == 2:
        #     last_index = len(Decorator.tier2_decorators) - 1
        #     rng = random.randint(0, last_index)
        #     self.emoji = Decorator.tier2_decorators[rng]
        # else:
        #     last_index = len(Decorator.tier3_decorators) - 1
        #     rng = random.randint(0, last_index)
        #     self.emoji = Decorator.tier3_decorators[rng]

        await self.set_name()

    async def use_decorator(self, player):
        from game.objects.characters import Player
        pass

    async def value_decorator(self):
        pass