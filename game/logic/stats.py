

class Stat():
    def __init__(self, xp: int = 100, lvl: float = 1):
        self._xp: int = xp
        self._lvl: float = lvl

    def get_xp(self) -> int:
        return self._xp
    
    def set_xp(self, value: int):
        self._xp = int(value)
        self.set_lvl()

    def add_xp(self, value: int):
        self._xp += int(value)
        self.set_lvl()

    # def update_xp(self):
    #     self._xp = round(100 * (self._lvl ** 3))
    
    def get_lvl(self) -> int:
        return int(self._lvl)
    
    # def set_lvl(self, lvl: float):
    #     if lvl >= 100: 
    #         self._lvl = 100
    #         return
    #     self._lvl = round(lvl, 2)
    #     self.update_xp()
    
    def set_lvl(self):
        lvl = round((self._xp / 100) ** (1 / 3), 2)
        if lvl >= 100: self._lvl = 100
        else: self._lvl = lvl

    async def get_progress(self) -> int:
        """
        Get the xp progress to the next level.
        Returns the percentage value of the progress.
        """
        lvl = self.get_lvl()
        if lvl < 100:
            xp_diff = (100 * ((lvl + 1) ** 3)) - (100 * (lvl ** 3)) # Get the xp difference between current and next level xp limits. 
            xp_prog = self._xp - (100 * (lvl ** 3)) # Get the xp progress through the difference between current xp, and current level xp limit.

            return round((xp_prog / xp_diff) * 100)
        else:
            return 100
        
class Attack(Stat):
    def __init__(self, xp: int = 100, lvl: float = 1):
        super().__init__(xp=xp, lvl=lvl)

class Defense(Stat):
    def __init__(self, xp: int = 100, lvl: float = 1):
        super().__init__(xp=xp, lvl=lvl)

class Health(Stat):
    def __init__(self, xp: int = 100, lvl: float = 1, health: int = 100):
        super().__init__(xp=xp, lvl=lvl)
        self.health = health

class Level(Stat):
    def __init__(self, attack: Attack, defense: Defense, health: Health):
        super().__init__()
        self._attack: Attack = attack
        self._defense: Defense = defense
        self._health: Health = health

    def get_xp(self) -> int:
        return int(self._xp)

    def set_xp(self):
        att_xp = self._attack.get_xp()
        def_xp = self._defense.get_xp()
        hp_xp = self._health.get_xp()

        if att_xp > 100_000_000:
            att_xp = 100_000_000
        if def_xp > 100_000_000:
            def_xp = 100_000_000
        if hp_xp > 100_000_000:
            hp_xp = 100_000_000

        self._xp = round((att_xp + def_xp + hp_xp) / 3) 

    def get_lvl(self):
        self.set_xp()
        self.set_lvl()
        return int(self._lvl)
    
    # def set_lvl(self):        
    #     self._lvl = round((self._attack._lvl + self._defense._lvl + self._health._lvl) / 3, 2) 