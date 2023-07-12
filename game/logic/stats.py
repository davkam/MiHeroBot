from game.features.features import Features

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
        self._lvl = round(lvl, 2)
        self.update_xp()
    
    def update_lvl(self):
        self._lvl = round((self._xp / 100) ** (1/3), 2)

    async def get_progress(self) -> str:
        prog = self._lvl - self.get_lvl()
        prog_bar = await Features.get_bar(act_val = prog, max_val = 100)

        return prog_bar

class Attack(Stats):
    pass

class Defense(Stats):
    pass

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

    def update_lvl(self):        
        self._lvl = round((self._attack._lvl + self._defense._lvl + self._health._lvl) / 3, 2)