from game.logic.stats import Attack, Defense, Health, Level

class Character():
    def __init__ (self, name: str = None, attack: Attack = None, defense: Defense = None, health: Health = None):
        self.name: str = name
        self.attack: Attack = attack or Attack()
        self.defense: Defense = defense or Defense()
        self.health: Health = health or Health()
        self.level: Level = Level(attack=self.attack, defense=self.defense, health=self.health)

    def get_name(self):
        return self.name.upper()