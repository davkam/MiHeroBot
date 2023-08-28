# -*- coding: ISO-8859-15 -*-

from discord.embeds import Embed
from discord.message import Message
from users.users import User

class InventoryEmbed(Embed):
    def __init__(self, msg: Message, user: User):
        super().__init__()
        self.msg: Message = msg
        self.user: User = user

    async def run_embed(self):
        items = await self.user.player.inventory.get_items(string_format=True)
        weapons = ""; armors = ""; potions = ""; kits = ""; decorators = ""
        inventory = f"{len(self.user.player.inventory.items)}/{self.user.player.inventory.slots}"

        if items != None:
            for item in items:
                if item.endswith("WEAPON"):
                    weapons += f"`{item}`\n"
                elif item.endswith("ARMOR"):
                    armors += f"`{item}`\n"
                elif item.endswith("POTION"):
                    potions += f"`{item}`\n"
                elif item.endswith("KIT"):
                    kits += f"`{item}`\n"
                elif item.startswith("TIER"):
                    decorators += f"`{item}`\n"
        
        if weapons == "": weapons = "`NONE`"
        if armors == "": armors = "`NONE`"
        if potions == "": potions = "`NONE`"
        if kits == "": kits = "`NONE`"
        if decorators == "": decorators = "`NONE`"

        self.clear_fields()
        self.add_field(name="\U00002694\uFE0F  WEAPONS", value=f"{weapons}", inline=True)
        self.add_field(name="\U0001F4B0  GOLD", value=f"`{self.user.player.gold} COINS`", inline=True)
        self.add_field(name="\U0001F6E1  ARMORS", value=f"{armors}", inline=True)
        self.add_field(name="\U00002697\uFE0F  POTIONS", value=f"{potions}", inline=True)
        self.add_field(name="\U0001F6E0  KITS", value=f"{kits}", inline=True)
        self.add_field(name="\U0001F642  DECORATORS", value=f"{decorators}", inline=True)
        self.set_footer(text=f"\U0001F4BC  INVENTORY: {inventory}")

        await self.msg.edit(content=f"**```arm\r\n{self.user.player.name} !Inventory\r\n```**", embed=self)