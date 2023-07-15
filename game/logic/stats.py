from game.features.additions import Additions

class Stats():
    def __init__(self, xp: int = 100, lvl: float = 1):
        self._xp: int = xp
        self._lvl: float = lvl

    def get_xp(self):
        return self._xp
    
    def set_xp(self, value: int):
        self._xp = int(value)
        self.update_lvl()

    def add_xp(self, value: int):
        self._xp += int(value)
        self.update_lvl()

    def update_xp(self):
        self._xp = round(100 * (self._lvl ** 3))
    
    def get_lvl(self):
        return int(self._lvl)
    
    def set_lvl(self, lvl: float):
        if lvl >= 100: 
            self._lvl = 100
            return
        self._lvl = round(lvl, 2)
        self.update_xp()
    
    def update_lvl(self):
        lvl = round((self._xp / 100) ** (1/3), 2)
        if lvl >= 100: self._lvl = 100
        else: self._lvl = lvl

    async def progress_bar(self) -> str: # TBD: REDEFINE! Not correct according to xp formula.
        prog = (self._lvl - self.get_lvl()) * 100
        prog_bar = await Additions.get_bar(act_val = prog, max_val = 100)

        return prog_bar
    
    async def progress_perc(self) -> int: # TBD: REDEFINE! Not correct according to xp formula.
        prog_perc = (self._lvl - self.get_lvl()) * 100

        return int(prog_perc)

class Attack(Stats):
    def __init__(self):
        Stats.__init__(self)

class Defense(Stats):
    def __init__(self):
        Stats.__init__(self)

class Health(Stats):
    def __init__(self, xp: int = 100, lvl: float = 1, health: int = 100):
        Stats.__init__(self, xp, lvl)
        self.health = health

    def get_hp(self):
        return self.get_lvl() * 100

class TotalLevel(Stats):
    def __init__(self, attack: Attack, defense: Defense, health: Health):
        Stats.__init__(self)
        self._attack: Attack = attack
        self._defense: Defense = defense
        self._health: Health = health

    def get_lvl(self):
        self.update_lvl()
        return int(self._lvl)

    def update_lvl(self):        
        self._lvl = round((self._attack._lvl + self._defense._lvl + self._health._lvl) / 3, 2)