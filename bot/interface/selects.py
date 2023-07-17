from typing import Any
from discord.interactions import Interaction
from bot.interface.views import FightView, FightButtonView, InventoryView
from data.database import Database
from discord.ui import Select
from game.objects.items import Item, Weapon, Armor, Potion, Kit, Decorator
from users.users import User
import discord
import uuid

class FightSelect(Select):
    def __init__(self, fight_view: FightView):
        super().__init__(placeholder = "\U0001F94A Select Fight!")
        self.fight_view: FightView = fight_view
        self.set_options()

    def set_options(self):
        self.add_option(label="\U0001F47E FIGHT MONSTER", value="FM", description="Fight a light, medium or heavy monster.")
        self.add_option(label="\U0001F642 FIGHT PLAYER", value="FP", description="Fight a player from users.")

    async def callback(self, interaction: Interaction):
        if await self.fight_view.interaction_check(interaction=interaction):
            if self.values[0] == "FM":
                monster_select = MonsterSelect(fight_view=self.fight_view)
                self.fight_view.clear_items()
                self.fight_view.add_item(item=monster_select)

                await interaction.response.edit_message(content="**```arm\r\nMiHero !Fight\r\n```**\n", view=self.fight_view)
            elif self.values[0] == "FP":
                player_select = PlayerSelect(fight_view=self.fight_view)
                self.fight_view.clear_items()
                self.fight_view.add_item(item=player_select)

                await interaction.response.edit_message(content="**```arm\r\nMiHero !Fight\r\n```**\n", view=self.fight_view)
        else:
            await interaction.response.defer()

class PlayerSelect(Select): # TBD: Display player name.
    def __init__(self, fight_view: FightView):
        super().__init__(placeholder = "\U0001F642 Select Player!")
        self.fight_view: FightView = fight_view
        self.set_options()
                
    def set_options(self): # TBD: Pre-set options, alphabetically!
        db = Database.instance
        for user in db.users.values():
            if user != self.fight_view.sender_user:
                user: User = user
                self.add_option(label = f"{user.player.get_name()}", value = str(user.user_id), description = f"LVL: {user.player.lvl.get_lvl()} ATT: {user.player.attack.get_lvl()} DEF: {user.player.defense.get_lvl()}")

    async def callback(self, interaction: Interaction):
        db = Database.instance
        if await self.fight_view.interaction_check(interaction = interaction):
            id = int(self.values[0])
            self.fight_view.receiver_user: User = await db.get_userbyId(user_id = id)

            button_view = FightButtonView(fight_view = self.fight_view, user = self.fight_view.receiver_user)
            message = f"**```arm\r\nMiHero !Fight\r\n```** **{str(interaction.user).upper()}** `challenges` **{self.fight_view.receiver_user.username.upper()}** `to a battle.`"

            await interaction.response.edit_message(content = message, view = button_view)
        else:
            await interaction.response.defer()

class MonsterSelect(Select): # TBD: Display player name.
    from bot.interface.views import FightView
    def __init__(self, fight_view: FightView):
        super().__init__(placeholder = "\U0001F47E Select Monster!")
        self.fight_view: FightView = fight_view
        self.set_options()

    def set_options(self):
        self.add_option(label = "\U0001F47E LIGHT MONSTER", value = "LM", description = f"Fight a light monster.")
        self.add_option(label = "\U0001F47E MEDIUM MONSTER", value = "MM", description = f"Fight a medium monster.")
        self.add_option(label = "\U0001F47E HEAVY MONSTER", value = "HM", description = f"Fight a heavy monster.")

    async def callback(self, interaction: discord.Interaction):
        if await self.fight_view.interaction_check(interaction = interaction):
            if self.values[0] == "LM":
                self.fight_view.select_type = "MonsterLight"
                self.fight_view.clear_items()
                message = f"**```arm\r\nMiHero !Fight\r\n```** **{interaction.user.name.upper()}** `encounters a light monster.`"

                await interaction.response.edit_message(content = message, view = self.fight_view)
            if self.values[0] == "MM":
                self.fight_view.select_type = "MonsterMedium"
                self.fight_view.clear_items()
                message = f"**```arm\r\nMiHero !Fight\r\n```** **{interaction.user.name.upper()}** `encounters a medium monster.`"

                await interaction.response.edit_message(content = message, view = self.fight_view)
            if self.values[0] == "HM":
                self.fight_view.select_type = "MonsterHeavy"
                self.fight_view.clear_items()
                message = f"**```arm\r\nMiHero !Fight\r\n```** **{interaction.user.name.upper()}** `encounters a heavy monster.`"

                await interaction.response.edit_message(content = message, view = self.fight_view)

            self.fight_view.success = True
            self.fight_view.stop()
        else:
            await interaction.response.defer()

class InventorySelect(Select):
    def __init__(self, inventory_view: InventoryView):
        super().__init__(placeholder="\U0001F9F0 Use Item!")
        self.inventory_view: InventoryView = inventory_view
        self.set_options()

    def set_options(self):
        self.add_option(label="\U00002694\uFE0F EQUIP WEAPON", value="EW", description="Equip a weapon from inventory.")
        self.add_option(label="\U0001F6E1\uFE0F EQUIP ARMOR", value="EA", description="Equip an armor from inventory.")
        self.add_option(label="\U00002697\uFE0F USE POTION", value="UP", description="Use a potion from inventory.")
        self.add_option(label="\U0001F6E0\uFE0F USE KIT", value="UK", description="Use a kit from inventory.")
        self.add_option(label="\U0001F642 USE DECORATOR", value="UD", description="Use a decorator from inventory.")
        self.add_option(label="\U0001F4BC CLOSE INVENTORY", value="CI", description="Closes inventory.")

    async def callback(self, interaction: Interaction):
        if await self.inventory_view.interaction_check(interaction=interaction):
            if self.values[0] == "EW":
                weapon_select = WeaponSelect(inventory_view=self.inventory_view)
                await weapon_select.set_options()

                self.inventory_view.clear_items()
                self.inventory_view.add_item(item=weapon_select)

                await interaction.response.edit_message(view=self.inventory_view)
            elif self.values[0] == "EA":
                armor_select = ArmorSelect(inventory_view=self.inventory_view)
                await armor_select.set_options()

                self.inventory_view.clear_items()
                self.inventory_view.add_item(item=armor_select)

                await interaction.response.edit_message(view=self.inventory_view)
            elif self.values[0] == "UP":
                potion_select = PotionSelect(inventory_view=self.inventory_view)
                await potion_select.set_options()

                self.inventory_view.clear_items()
                self.inventory_view.add_item(item=potion_select)

                await interaction.response.edit_message(view=self.inventory_view)
            elif self.values[0] == "UK":
                kit_select = KitSelect(inventory_view=self.inventory_view)
                await kit_select.set_options()

                self.inventory_view.clear_items()
                self.inventory_view.add_item(item=kit_select)

                await interaction.response.edit_message(view=self.inventory_view)
            elif self.values[0] == "UD":
                decorator_select = DecoratorSelect(inventory_view=self.inventory_view)
                await decorator_select.set_options()

                self.inventory_view.clear_items()
                self.inventory_view.add_item(item=decorator_select)

                await interaction.response.edit_message(view=self.inventory_view)
            elif self.values[0] == "CI":
                self.inventory_view.success = True
                self.inventory_view.close_view = True
                self.inventory_view.stop()
                
                await interaction.response.edit_message(content="`Inventory closed, to re-open inventory use command !Inv.`", view=None)
        else:
            await interaction.response.defer()
class WeaponSelect(Select):
    def __init__(self, inventory_view: InventoryView):
        super().__init__(placeholder="\U00002694\uFE0F Equip Weapon!")
        self.inventory_view: InventoryView = inventory_view

    async def set_options(self):
        weapons: list[Weapon] = await self.inventory_view.user.player.inventory.get_weapons(string_format=False)
        
        if weapons == None:
            self.add_option(label="\U0001F448 GO BACK", value="GB", description="Go back to main.")
            self.add_option(label="\U0001F4BC CLOSE INVENTORY", value="CI", description="Close inventory.")
            return
        else:
            for weapon in weapons:
                self.add_option(label=weapon.name, value=str(weapon.uuid), description=f"Equip {weapon.name.lower()}.")
            
            self.add_option(label="\U0001F448 GO BACK", value="GB", description="Go back to main.")
            self.add_option(label="\U0001F4BC CLOSE INVENTORY", value="CI", description="Close inventory.")

    async def callback(self, interaction: Interaction):
        if await self.inventory_view.interaction_check(interaction=interaction):
            if self.values[0] == "GB":
                self.inventory_view.success = True
                self.inventory_view.stop()

                await interaction.response.defer()
            elif self.values[0] == "CI":
                self.inventory_view.success = True
                self.inventory_view.close_view = True
                self.inventory_view.stop()
                
                await interaction.response.edit_message(content="`Inventory closed, to re-open inventory use command !Inv.`", view=None)
            else:
                item_uuid = uuid.UUID(self.values[0])
                item: Item = await self.inventory_view.user.player.inventory.find_item(uuid=item_uuid)

                if item != None: 
                    log = await item.use_item(player=self.inventory_view.user.player)

                self.inventory_view.response = log
                self.inventory_view.success = True
                self.inventory_view.stop()
                
                await interaction.response.defer() 
        else:
            await interaction.response.defer()   

class ArmorSelect(Select):
    def __init__(self, inventory_view: InventoryView):
        super().__init__(placeholder="\U0001F6E1\uFE0F Equip Armor!")
        self.inventory_view: InventoryView = inventory_view

    async def set_options(self):
        armors: list[Armor] = await self.inventory_view.user.player.inventory.get_armors(string_format=False)
        
        if armors == None:
            self.add_option(label="\U0001F448 GO BACK", value="GB", description="Go back to main.")
            self.add_option(label="\U0001F4BC CLOSE INVENTORY", value="CI", description="Close inventory.")
            return
        else:
            for armor in armors:
                self.add_option(label=armor.name, value=str(armor.uuid), description=f"Equip {armor.name.lower()}.")

            self.add_option(label="\U0001F448 GO BACK", value="GB", description="Go back to main.") 
            self.add_option(label="\U0001F4BC CLOSE INVENTORY", value="CI", description="Close inventory.")

    async def callback(self, interaction: Interaction):
        if await self.inventory_view.interaction_check(interaction=interaction):
            if self.values[0] == "GB":
                self.inventory_view.success = True
                self.inventory_view.stop()

                await interaction.response.defer()
            elif self.values[0] == "CI":
                self.inventory_view.success = True
                self.inventory_view.close_view = True
                self.inventory_view.stop()

                await interaction.response.edit_message(content="`Inventory closed, to re-open inventory use command !Inv.`", view=None)
            else:
                item_uuid = uuid.UUID(self.values[0])
                item: Item = await self.inventory_view.user.player.inventory.find_item(uuid=item_uuid)

                if item != None: 
                    log = await item.use_item(player=self.inventory_view.user.player)

                self.inventory_view.response = log
                self.inventory_view.success = True
                self.inventory_view.stop()
                
                await interaction.response.defer() 
        else:
            await interaction.response.defer()   

class PotionSelect(Select):
    def __init__(self, inventory_view: InventoryView):
        super().__init__(placeholder="\U00002697\uFE0F Use Potion!")
        self.inventory_view: InventoryView = inventory_view

    async def set_options(self):
        potions: list[Potion] = await self.inventory_view.user.player.inventory.get_potions(string_format=False)
        
        if potions == None:
            self.add_option(label="\U0001F448 GO BACK", value="GB", description="Go back to main.")
            self.add_option(label="\U0001F4BC CLOSE INVENTORY", value="CI", description="Close inventory.")
            return
        else:
            for potion in potions:
                self.add_option(label=potion.name, value=str(potion.uuid), description=f"Use {potion.name.lower()}.")

            self.add_option(label="\U0001F448 GO BACK", value="GB", description="Go back to main.")
            self.add_option(label="\U0001F4BC CLOSE INVENTORY", value="CI", description="Close inventory.")  

    async def callback(self, interaction: Interaction):
        if await self.inventory_view.interaction_check(interaction=interaction):
            if self.values[0] == "BACK": 
                self.inventory_view.success = True
                self.inventory_view.stop()

                await interaction.response.defer()
            elif self.values[0] == "CI":
                self.inventory_view.success = True
                self.inventory_view.close_view = True
                self.inventory_view.stop()

                await interaction.response.edit_message(content="`Inventory closed, to re-open inventory use command !Inv.`", view=None)
            else:
                item_uuid = uuid.UUID(self.values[0])
                item: Item = await self.inventory_view.user.player.inventory.find_item(uuid=item_uuid)

                if item != None: 
                    log = await item.use_item(player=self.inventory_view.user.player)

                self.inventory_view.response = log
                self.inventory_view.success = True
                self.inventory_view.stop()
                
                await interaction.response.defer() 
        else:
            await interaction.response.defer() 

class KitSelect(Select):
    def __init__(self, inventory_view: InventoryView):
        super().__init__(placeholder="\U0001F6E0\uFE0F Use Kit!")
        self.inventory_view: InventoryView = inventory_view

    async def set_options(self):
        kits: list[Kit] = await self.inventory_view.user.player.inventory.get_kits(string_format=False)

        if kits == None:
            self.add_option(label="\U0001F448 GO BACK", value="GB", description="Go back to main.")
            self.add_option(label="\U0001F4BC CLOSE INVENTORY", value="CI", description="Close inventory.")
            return
        else:
            for kit in kits:
                self.add_option(label=kit.name, value=str(kit.uuid), description=f"Use {kit.name.lower()}.")
            
            self.add_option(label="\U0001F448 GO BACK", value="GB", description="Go back to main.")
            self.add_option(label="\U0001F4BC CLOSE INVENTORY", value="CI", description="Close inventory.")  

    async def callback(self, interaction: Interaction):
        if await self.inventory_view.interaction_check(interaction=interaction):
            if self.values[0] == "GB":
                self.inventory_view.success = True
                self.inventory_view.stop()

                await interaction.response.defer()
            elif self.values[0] == "CI":
                self.inventory_view.success = True
                self.inventory_view.close_view = True
                self.inventory_view.stop()

                await interaction.response.edit_message(content="`Inventory closed, to re-open inventory use command !Inv.`", view=None)
            else:
                item_uuid = uuid.UUID(self.values[0])
                item: Item = await self.inventory_view.user.player.inventory.find_item(uuid=item_uuid)

                if item != None: 
                    log = await item.use_item(player=self.inventory_view.user.player)

                self.inventory_view.response = log
                self.inventory_view.success = True
                self.inventory_view.stop()
                
                await interaction.response.defer() 
        else:
            await interaction.response.defer() 

class DecoratorSelect(Select):
    def __init__(self, inventory_view: InventoryView):
        super().__init__(placeholder="\U0001F642 Use Decorator!")
        self.inventory_view: InventoryView = inventory_view

    async def set_options(self):
        decorators: list[Decorator] = await self.inventory_view.user.player.inventory.get_decorators(string_format=False)

        if decorators == None:
            self.add_option(label="\U0001F448 GO BACK", value="GB", description="Go back to main.")
            self.add_option(label="\U0001F4BC CLOSE INVENTORY", value="CI", description="Close inventory.")
            return
        else:
            for decorator in decorators:
                self.add_option(label=decorator.name, value=str(decorator.uuid), description=f"Use {decorator.name.lower()}.")
            
            self.add_option(label="\U0001F448 GO BACK", value="GB", description="Go back to main.")
            self.add_option(label="\U0001F4BC CLOSE INVENTORY", value="CI", description="Close inventory.")  

    async def callback(self, interaction: Interaction):
        if await self.inventory_view.interaction_check(interaction=interaction):
            if self.values[0] == "GB":
                self.inventory_view.success = True
                self.inventory_view.stop()

                await interaction.response.defer()
            elif self.values[0] == "CI":
                self.inventory_view.success = True
                self.inventory_view.close_view = True
                self.inventory_view.stop()

                await interaction.response.edit_message(content="`Inventory closed, to re-open inventory use command !Inv.`", view=None)
            else:
                item_uuid = uuid.UUID(self.values[0])
                item: Item = await self.inventory_view.user.player.inventory.find_item(uuid=item_uuid)

                if item != None: 
                    log = await item.use_item(player=self.inventory_view.user.player)
                    
                self.inventory_view.response = log
                self.inventory_view.success = True
                self.inventory_view.stop()

                await interaction.response.defer() 
        else:
            await interaction.response.defer() 