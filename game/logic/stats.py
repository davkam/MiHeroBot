class Stat():
    def __init__(self, xp: int = 100, lvl: float = 1) -> None:
        self._xp: int = xp
        self._lvl: float = lvl

    def get_xp(self) -> int:
        return self._xp
    
    def set_xp(self, value: int) -> None:
        self._xp = int(value)
        self.update_lvl()

    def add_xp(self, value: int) -> None:
        self._xp += int(value)
        self.update_lvl()

    def update_xp(self) -> None:
        self._xp = round(100 * (self._lvl ** 3))
    
    def get_lvl(self) -> int:
        return int(self._lvl)
    
    def set_lvl(self, lvl: float) -> None:
        lvl = round(lvl, 2)
        self._lvl = min(lvl, 100)
        self.update_xp()
    
    def update_lvl(self) -> None:
        lvl = round((self._xp / 100) ** (1 / 3), 2)
        self._lvl = min(lvl, 100)

    async def get_progress(self) -> int:
        """
        Get xp progress to next level.
        
        Returns:
            int: Progress in percentage.
        """

        lvl = self.get_lvl()
        if lvl < 100:
            xp_diff = (100 * ((lvl + 1) ** 3)) - (100 * (lvl ** 3)) # Get xp difference between current and next level xp limits 
            xp_prog = self._xp - (100 * (lvl ** 3)) # Get progressed xp from current level xp limit to current xp

            # Return quotient of progressed xp by xp difference in percentage
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
        self._health = health

    def set_lvl(self, lvl: float) -> None:
        super().set_lvl(lvl=lvl)
        self.update_health()
    
    def update_lvl(self) -> None:
        super().update_lvl()
        self.update_health()

    def get_health(self) -> int:
        self.update_health()
        return self._health
    
    def update_health(self) -> None:
        self._health = self.get_lvl() * 100

class Level(Stat):
    def __init__(self, attack: Attack, defense: Defense, health: Health):
        super().__init__()
        self._attack: Attack = attack
        self._defense: Defense = defense
        self._health: Health = health

    def get_lvl(self) -> int:
        self.update_lvl()
        return int(self._lvl)
    
    def update_lvl(self) -> None:
        self._lvl = round((self._attack._lvl + self._defense._lvl + self._health._lvl) / 3, 2) 
        self.update_xp()