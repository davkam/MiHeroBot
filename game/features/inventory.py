from extras.tools import Tools
from game.objects.items import Item, Weapon, Armor, Potion, Kit, Decorator
import uuid

class Inventory():
    def __init__(self):
        self.items: list[Item] = list()
        self.slots: int = 10
        self.max_slots: int = 50

    async def add_item(self, item: Item):
        self.items.append(item)

    async def rem_item(self, item: Item):
        self.items.remove(item)

    async def find_item(self, uuid: uuid) -> Item:
        for item in self.items:
            if item.uuid == uuid:
                return item
        return None

    async def get_items(self, string_format: bool) -> list[str] or list[Item]:
        self.items.sort(key=lambda item: (Tools.item_sortkey(item=item), item.name))
        if string_format == True:
            items: list[str] = list()
            for item in self.items:
                items.append(item.name)

            if len(items) == 0: return None
            else: return items          
        else:
            return self.items         
    
    async def get_weapons(self, string_format: bool) -> list[str] or list[Weapon]:
        if string_format == True:
            weapons: list[str] = list()
            for item in self.items:
                if isinstance(item, Weapon):
                    weapons.append(item.name)

            if len(weapons) == 0: return None
            else: return weapons          
        else:
            weapons: list[Weapon] = list()
            for item in self.items:
                if isinstance(item, Weapon):
                    weapons.append(item)

            if len(weapons) == 0: return None
            else: return weapons      
    
    async def get_armors(self, string_format: bool) -> list[str] or list[Armor]:
        if string_format == True:
            armors: list[str] = list()
            for item in self.items:
                if isinstance(item, Armor):
                    armors.append(item.name)

            if len(armors) == 0: return None
            else: return armors 
        else:
            armors: list[Armor] = list()
            for item in self.items:
                if isinstance(item, Armor):
                    armors.append(item)

            if len(armors) == 0: return None
            else: return armors  
    
    async def get_potions(self, string_format: bool) -> list[str] or list[Potion]:
        if string_format == True:
            potions: list[str] = list()
            for item in self.items:
                if isinstance(item, Potion):
                    potions.append(item.name)

            if len(potions) == 0: return None
            else: return potions 
        else:
            potions: list[Potion] = list()
            for item in self.items:
                if isinstance(item, Potion):
                    potions.append(item)

            if len(potions) == 0: return None
            else: return potions  
    
    async def get_kits(self, string_format: bool) -> list[str] or list[Kit]:
        if string_format == True:
            kits: list[str] = list()
            for item in self.items:
                if isinstance(item, Kit):
                    kits.append(item.name)

            if len(kits) == 0: return None
            else: return kits
        else:
            kits: list[Kit] = list()
            for item in self.items:
                if isinstance(item, Kit):
                    kits.append(item)

            if len(kits) == 0: return None
            else: return kits          
    
    async def get_decorators(self, string_format: bool) -> list[str] or list[Decorator]:
        if string_format == True:
            decorators: list[str] = list()
            for item in self.items:
                if isinstance(item, Decorator):
                    decorators.append(item.name)

            if len(decorators) == 0: return None
            else: return decorators
        else:
            decorators: list[Decorator] = list()
            for item in self.items:
                if isinstance(item, Decorator):
                    decorators.append(item)

            if len(decorators) == 0: return None
            else: return decorators 

    async def check_inv(self) -> bool:
        if len(self.items) >= self.slots:
            return True
        else:
            return False
        
    async def add_slots(self, quantity: int):
        if self.slots + quantity <= self.max_slots:
            self.slots += quantity