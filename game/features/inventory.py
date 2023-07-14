from game.features.additions import Additions
from game.objects.items import Item, Weapon, Armor, Potion, Kit, Decorator

class Inventory():
    def __init__(self):
        self.items: list[Item] = list()
        self.slots: int = 10
        self.max_slots: int = 50

    async def add_item(self, item: Item):
        self.items.append(item)

    async def rem_item(self, item: Item):
        self.items.remove(item)

    async def get_items(self) -> str:
        self.items.sort(key=lambda item: (Additions.item_sortkey(item=item), item.name))

        log: str = ""
        for item in self.items:
            log += f"`{item.name}`\n"

        if log == "": log = "`NONE`"
        return log
    
    async def get_weapons(self) -> str:
        log: str = ""
        for item in self.items:
            if isinstance(item, Weapon):
                log += f"`{item.name}`\n"

        if log == "": log = "`NONE`"
        return log
    
    async def get_armors(self) -> str:
        log: str = ""
        for item in self.items:
            if isinstance(item, Armor):
                log += f"`{item.name}`\n"

        if log == "": log = "`NONE`"
        return log
    
    async def get_potions(self) -> str:
        log: str = ""
        for item in self.items:
            if isinstance(item, Potion):
                log += f"`{item.name}`\n"

        if log == "": log = "`NONE`"
        return log
    
    async def get_kits(self) -> str:
        log: str = ""
        for item in self.items:
            if isinstance(item, Kit):
                log += f"`{item.name}`\n"

        if log == "": log = "`NONE`"
        return log
    
    async def get_decorators(self) -> str:
        log: str = ""
        for item in self.items:
            if isinstance(item, Decorator):
                log += f"`{item.name}`\n"

        if log == "": log = "`NONE`"
        return log
    
    async def check_inv(self) -> bool:
        if len(self.items) >= self.slots:
            return True
        else:
            return False
        
    async def add_slots(self, quantity: int):
        if self.slots + quantity < self.max_slots:
            self.slots += quantity