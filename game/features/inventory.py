from game.objects.items.items import *

class Inventory():
    def __init__(self):
        self.items: list[Item] = list()
        self.slots: int = 10
        self.max_slots: int = 50