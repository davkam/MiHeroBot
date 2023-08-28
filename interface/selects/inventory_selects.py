from discord import Interaction
from discord.ui import Select
from game.objects.items import Item, Weapon, Armor, Potion, Kit, Decorator
from interface.views.inventory_view import InventoryView
import uuid

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
            self.add_option(label="\U0001F448 GO BACK", value="GB", description="Go back to item select.")
            self.add_option(label="\U0001F4BC CLOSE INVENTORY", value="CI", description="Close inventory.")
            return
        else:
            for weapon in weapons:
                self.add_option(label=weapon.name, value=str(weapon.uuid), description=f"Equip {weapon.name.lower()}.")
            
            self.add_option(label="\U0001F448 GO BACK", value="GB", description="Go back to item select.")
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
            self.add_option(label="\U0001F448 GO BACK", value="GB", description="Go back to item select.")
            self.add_option(label="\U0001F4BC CLOSE INVENTORY", value="CI", description="Close inventory.")
            return
        else:
            for armor in armors:
                self.add_option(label=armor.name, value=str(armor.uuid), description=f"Equip {armor.name.lower()}.")

            self.add_option(label="\U0001F448 GO BACK", value="GB", description="Go back to item select.") 
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
            self.add_option(label="\U0001F448 GO BACK", value="GB", description="Go back to item select.")
            self.add_option(label="\U0001F4BC CLOSE INVENTORY", value="CI", description="Close inventory.")
            return
        else:
            for potion in potions:
                self.add_option(label=potion.name, value=str(potion.uuid), description=f"Use {potion.name.lower()}.")

            self.add_option(label="\U0001F448 GO BACK", value="GB", description="Go back to item select.")
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
            self.add_option(label="\U0001F448 GO BACK", value="GB", description="Go back to item select.")
            self.add_option(label="\U0001F4BC CLOSE INVENTORY", value="CI", description="Close inventory.")
            return
        else:
            for kit in kits:
                self.add_option(label=kit.name, value=str(kit.uuid), description=f"Use {kit.name.lower()}.")
            
            self.add_option(label="\U0001F448 GO BACK", value="GB", description="Go back to item select.")
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
            self.add_option(label="\U0001F448 GO BACK", value="GB", description="Go back to item select.")
            self.add_option(label="\U0001F4BC CLOSE INVENTORY", value="CI", description="Close inventory.")
            return
        else:
            for decorator in decorators:
                self.add_option(label=decorator.name, value=str(decorator.uuid), description=f"Use {decorator.name.lower()[:-2]}.")
            
            self.add_option(label="\U0001F448 GO BACK", value="GB", description="Go back to item select.")
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