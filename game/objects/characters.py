from enum import Enum
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
    def __init__ (self, name: str = None, monster_class: MonsterClass = MonsterClass.Light, attack: Attack = None, defense: Defense = None, health: Health = None):
        Character.__init__(self, name = name, attack = attack, defense = defense, health = health)
        self.monster_class: MonsterClass = monster_class
    
    # generate_monster(): Initializes monster with randomized attributes depending on arguments monster_class and lvl.
    async def generate_monster(self, monster_class: MonsterClass, lvl: int):
        # Assigns a randomized self.lvl depending on monster_class option and lvl.
        if monster_class == MonsterClass.Light:
            self.name = "LIGHT MONSTER"
            low = 750; high = 1250
        elif monster_class == MonsterClass.Medium:
            self.name = "MEDIUM MONSTER"
            low = 1000; high = 1500
        elif monster_class == MonsterClass.Heavy:
            self.name = "HEAVY MONSTER"
            low = 1500; high = 2000

        # Returns with default values if lvl = 1.
        if lvl == 1:
            return

        self.monster_class = monster_class
        m_lvl = lvl * (random.randint(low, high) / 1000)
        
        # Distributes 75% of m_lvl value evenly to m_att, m_def, m_hp.
        m_att = m_lvl * 0.75
        m_def = m_lvl * 0.75
        m_hp = m_lvl * 0.75

        # Distributes remaining 25% of m_lvl value randomly to m_att, m_def, m_hp
        lvl_left = (m_lvl * 0.25) * 3
        rng = random.randint(1, 3)
        if rng == 1: # First: m_att        
            rng = random.randint(0, 100) / 100
            m_att += lvl_left * rng
            lvl_left -= lvl_left * rng
            rng = random.randint(1, 2)
            if rng == 1: # Second: m_def, Third: m_hp
                rng = random.randint(0, 100) / 100
                m_def += lvl_left * rng
                lvl_left -= lvl_left * rng
                m_hp += lvl_left
            elif rng == 2: # Second: m_hp, Third: m_def
                rng = random.randint(0, 100) / 100
                m_hp += lvl_left * rng
                lvl_left -= lvl_left * rng
                m_def += lvl_left
        elif rng == 2: # First: m_def
            rng = random.randint(0, 100) / 100
            m_def += lvl_left * rng
            lvl_left -= lvl_left * rng
            rng = random.randint(1, 2)
            if rng == 1: # Second: m_att, Third: m_hp
                rng = random.randint(0, 100) / 100
                m_att += lvl_left * rng
                lvl_left -= lvl_left * rng
                m_hp += lvl_left
            elif rng == 2: # Second: m_hp, Third: m_att 
                rng = random.randint(0, 100) / 100
                m_hp += lvl_left * rng
                lvl_left -= lvl_left * rng
                m_att += lvl_left
        elif rng == 3: # First: m_hp
            rng = random.randint(0, 100) / 100
            m_hp += lvl_left * rng
            lvl_left -= lvl_left * rng
            rng = random.randint(1, 2)
            if rng == 1: # Second: m_att, Third: m_def
                rng = random.randint(0, 100) / 100
                m_att += lvl_left * rng
                lvl_left -= lvl_left * rng
                m_def += lvl_left
            elif rng == 2: # Second: m_def, Third: m_att
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
        self.gold: int = gold
        self.weapon: Weapon = Weapon()
        self.armor: Armor = Armor()
        self.gold: int = gold

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
        await monster.generate_monster(monster_class = monster_class, lvl = self.lvl.get_lvl())

        combat = Combat(objA = self, objB = monster)
        await combat.set_stats()
        await combat.run_combat()
        log = combat.log

        monster = None
        combat = None
        return log