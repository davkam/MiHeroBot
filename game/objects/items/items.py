import random
import uuid

class Item():
    def __init__(self, name: str = None, value: int = None):
        self.id: uuid.UUID = uuid.uuid4()
        self.name: str = name
        self.value: int = value

    def get_name(self) -> str:
        self.set_name()
        return self.name
    
    def set_name(self, name: str = None):
        self.name = name

    async def get_random_item(self, item_index: int, equips_allowed: bool, avg_stats: float = None):
        random_item = None

        if equips_allowed == True:
            from game.objects.items.equipables import Equipable
            random_item = Equipable()
            random_item.get_random_equipable(equip_index=item_index, avg_stats=avg_stats)
        else:
            from game.objects.items.consumables import Consumable
            random_item = Consumable()
            random_item.get_random_item()
        
        # if item_index == 1:
        #     rng = random.randint(1, 2)
        #     if rng == 1:
        #         random_item = Potion()
        #         await random_item.randomize_potion(potion_index=item_index)
        #     else:
        #         random_item = Kit()
        #         await random_item.randomize_kit(item_index)
        # else:
        #     rng = random.randint(0, 100)
        #     if rng < 40:
        #         random_item = Potion()
        #         await random_item.randomize_potion(potion_index=item_index)
        #     elif rng >= 40 and rng < 80:
        #         random_item = Kit()
        #         await random_item.randomize_kit(kit_index=item_index)
        #     else:
        #         random_item = Decorator()
        #         await random_item.randomize_decorator(decorator_index=item_index)

        return random_item
    
    # async def use_item(self, player) -> str:
    #     if isinstance(self, Weapon):
    #         weapon: Weapon = self
    #         log = await weapon.equip_weapon(player=player)
    #     elif isinstance(self, Armor):
    #         armor: Armor = self
    #         log = await armor.equip_armor(player=player)
    #     elif isinstance(self, Potion):
    #         potion: Potion = self
    #         log = await potion.use_potion(player=player)
    #     elif isinstance(self, Kit):
    #         kit: Kit = self
    #         log = await kit.use_kit(player=player)
    #     elif isinstance(self, Decorator):
    #         decorator: Decorator = self
    #         log = await decorator.use_decorator(player=player)

    #     return log