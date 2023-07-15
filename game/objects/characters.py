from enum import Enum
from game.features.inventory import Inventory
from game.logic.stats import *
from game.objects.items import *
import random

class MonsterClass(Enum):
    Light = 2
    Medium = 6
    Heavy = 10

class Character():
    def __init__ (self, name: str = None, attack: Attack = None, defense: Defense = None, health: Health = None):
        self.name: str = name
        self.attack: Attack = attack or Attack()
        self.defense: Defense = defense or Defense()
        self.health: Health = health or Health()
        self.lvl: TotalLevel = TotalLevel(attack = self.attack, defense = self.defense, health = self.health)

class Monster(Character):
    def __init__ (self, name: str = None, monster_class: MonsterClass = None, attack: Attack = None, defense: Defense = None, health: Health = None):
        Character.__init__(self, name = name, attack = attack, defense = defense, health = health)
        self.monster_class: MonsterClass = monster_class or MonsterClass.Light
    
    # Initializes monster with randomized attributes based on parameters.
    async def randomize_monster(self, monster_class: MonsterClass, lvl: int):
        # Assigns name to monster and rng attributes based on monster class.
        if monster_class == MonsterClass.Light:
            self.name = "LIGHT MONSTER"
            low = 750; high = 1250
        elif monster_class == MonsterClass.Medium:
            self.name = "MEDIUM MONSTER"
            low = 1000; high = 1500
        elif monster_class == MonsterClass.Heavy:
            self.name = "HEAVY MONSTER"
            low = 1500; high = 2000

        # Returns with default values if argument level is 1.
        if lvl == 1:
            return

        # Sets monster class and level depending on previously defined rng attributes.
        self.monster_class = monster_class
        m_lvl = lvl * (random.randint(low, high) / 1000)
        
        # Distributes 75% of monster level value evenly to monster attack, defense, and health.
        m_att = m_lvl * 0.75
        m_def = m_lvl * 0.75
        m_hp = m_lvl * 0.75

        # Distributes remaining 25% of monster level value randomly to monster attack, defense, and health based on rng priority.
        lvl_left = (m_lvl * 0.25) * 3
        rng = random.randint(1, 3)
        if rng == 1:       
            rng = random.randint(0, 100) / 100
            m_att += lvl_left * rng
            lvl_left -= lvl_left * rng
            rng = random.randint(1, 2)
            if rng == 1:
                rng = random.randint(0, 100) / 100
                m_def += lvl_left * rng
                lvl_left -= lvl_left * rng
                m_hp += lvl_left
            elif rng == 2:
                rng = random.randint(0, 100) / 100
                m_hp += lvl_left * rng
                lvl_left -= lvl_left * rng
                m_def += lvl_left
        elif rng == 2:
            rng = random.randint(0, 100) / 100
            m_def += lvl_left * rng
            lvl_left -= lvl_left * rng
            rng = random.randint(1, 2)
            if rng == 1:
                rng = random.randint(0, 100) / 100
                m_att += lvl_left * rng
                lvl_left -= lvl_left * rng
                m_hp += lvl_left
            elif rng == 2:
                rng = random.randint(0, 100) / 100
                m_hp += lvl_left * rng
                lvl_left -= lvl_left * rng
                m_att += lvl_left
        elif rng == 3:
            rng = random.randint(0, 100) / 100
            m_hp += lvl_left * rng
            lvl_left -= lvl_left * rng
            rng = random.randint(1, 2)
            if rng == 1:
                rng = random.randint(0, 100) / 100
                m_att += lvl_left * rng
                lvl_left -= lvl_left * rng
                m_def += lvl_left
            elif rng == 2:
                rng = random.randint(0, 100) / 100
                m_def += lvl_left * rng
                lvl_left -= lvl_left * rng
                m_att += lvl_left

        self.lvl.set_lvl(m_lvl)
        self.attack.set_lvl(m_att)
        self.defense.set_lvl(m_def)
        self.health.set_lvl(m_hp)  

class Player(Character):
    def __init__ (self, name: str, attack: Attack = None, defense: Defense = None, health: Health = None, gold: int = 0):
        Character.__init__(self, name = name.upper(), attack = attack, defense = defense, health = health)  
        self.weapon: Weapon = Weapon()
        self.armor: Armor = Armor()
        self.decorator: Decorator = None
        self.inventory: Inventory = Inventory()
        self.gold: int = gold

    def get_name(self):
        if self.decorator != None:
            return f"{self.decorator.emoji} {self.name.upper()}"
        else:
            return self.name.upper()

    async def fight_player(self, player) -> str:
        from game.logic.combat import Combat

        combat = Combat(objA = self, objB = player)
        await combat.set_stats()
        await combat.run_combat()
        log = combat.log

        combat = None
        return log
    
    async def fight_monster(self, monster_class: MonsterClass) -> str:
        from game.logic.combat import Combat

        monster = Monster()
        await monster.randomize_monster(monster_class = monster_class, lvl = self.lvl.get_lvl())

        combat = Combat(objA = self, objB = monster)
        await combat.set_stats()
        await combat.run_combat()
        log = combat.log

        monster = None
        combat = None
        return log
    
    async def xp_gainer(self, xp_index: int) -> str:
        # Sets rng variables according to xp index.
        if xp_index == 1: min = 1000; max = 2500; multiplier = 10
        elif xp_index == 2: min = 2500; max = 5000; multiplier = 25
        else: min = 5000; max = 10000; multiplier = 50

        # Sets experience gains randomly according to rng variables.
        lvl = self.lvl.get_lvl()
        rng_xp = random.randint(min, max)
        att_gain = int(rng_xp + (lvl ** 1.5) * multiplier)
        rng_xp = random.randint(min, max)
        def_gain = int(rng_xp + (lvl ** 1.5) * multiplier)
        rng_xp = random.randint(min, max)
        hp_gain = int(rng_xp + (lvl ** 1.5) * multiplier)

        self.attack.add_xp(value=att_gain)
        self.defense.add_xp(value=def_gain)
        self.health.add_xp(value=hp_gain)
        self.lvl.update_lvl()

        att_bar = await self.attack.progress_bar()
        def_bar = await self.defense.progress_bar()
        hp_bar = await self.health.progress_bar()
        lvl_bar = await self.lvl.progress_bar()

        att_perc = await self.attack.progress_perc()
        def_perc = await self.defense.progress_perc()
        hp_perc = await self.health.progress_perc()
        lvl_perc = await self.lvl.progress_perc()

        # Sets xp gainer log for return.
        log = f"**```arm\r\n{self.get_name()} !XPGainer\r\n```**"
        log += f"||||| `ATTACK GAIN:`**`{att_gain}`**`experience points. ATTACK:`**`{self.attack.get_lvl()}`** **{att_bar}** **`({att_perc}%)`**\n"
        log += f"||||| `DEFENSE GAIN:`**`{def_gain}`**`experience points. DEFENSE:`**`{self.defense.get_lvl()}`** **{def_bar}** **`({def_perc}%)`**\n"
        log += f"||||| `HEALTH GAIN:`**`{hp_gain}`**`experience points. HEALTH:`**`{self.health.get_hp()}`** **{hp_bar}** **`({hp_perc}%)`**\n"
        log += f"||||| `AVERAGE LEVEL:`**`{self.lvl.get_lvl()}`** **{lvl_bar}** **`({lvl_perc}%)`**\r\n"

        return log

    async def loot_generator(self, loot_index: int) -> str:
        loot_roll = None    # Determines amount of times to roll for loot.
        loot_gear = None    # Determines amount of gear (weapon/armor) allowed in loot rolls.
        # Sets loot variables and gold according to loot index.
        if loot_index == 1:
            gold = random.randint(500, 1000)
            loot_roll = random.randint(1, 3)
            loot_gear = 1
        elif loot_index == 2:
            gold = random.randint(1000, 2000)
            loot_roll = random.randint(2, 4)
            loot_gear = random.randint(1, 2)
        elif loot_index == 3:
            gold = random.randint(2000, 4000)
            loot_roll = random.randint(3, 5)
            loot_gear = random.randint(1, 3)

        self.gold += gold
        attack = self.attack.get_lvl()
        defense = self.defense.get_lvl()
        health = self.health.get_lvl()
        avg_stats = (attack + defense + health) / 3

        if await self.inventory.check_inv(): inv_full = True
        else: inv_full = False

        loot_items: list[Item] = list()
        item = Item()
        while loot_roll > 0 and inv_full == False:
            if loot_gear > 0:
                gear_enabled = True
                loot_gear -= 1
            else:
                gear_enabled = False

            random_item = await item.randomize_item(item_index=loot_index, gear_allowed=gear_enabled, avg_stats=avg_stats)
            loot_items.append(random_item)
            loot_roll -= 1

        log = f"**```arm\r\n{self.name} !LootGenerator\r\n```**"
        if inv_full == False:
            for item in loot_items:
                log += f"||||| `LOOT ITEM:`**`{item.name}`**\n"
                await self.inventory.add_item(item=item)
        else: log += "`Inventory full, no loot rewarded!`\n`Please free up space or buy more inventory space.`\n"
        
        log += f"**----------------------------------------**\n"
        log += f"||||| `GOLD LOOT:`**`{gold}`**`gold coins.`\n"
        log += f"||||| `TOTAL GOLD:`**`{self.gold}`**`gold coins.`\n"

        if await self.inventory.check_inv() and inv_full == False: 
            log += "`Inventory full, please free up space before next encounter to be able to receive rewards.`\n"

        return log