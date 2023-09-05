from typing import Any
from discord.interactions import Interaction
from discord.ui import Select
from game.objects.items import *
from interface.buttons.trade_buttons import *
from interface.embeds.trade_embed import TradeEmbed
from interface.views.trade_view import TradeView
from users.users import User

class TradePlayerSelect(Select):
    def __init__(self, trade_view: TradeView):
        super().__init__(placeholder="\U0001F4BC\uFE0F Select Player to Trade!")
        self.trade_view: TradeView = trade_view

        self.set_options()

    def set_options(self):
        db = self.trade_view.db
        for user in db.users.values():
            if user != self.trade_view.trade.sender_trader:
                user: User = user
                self.add_option(label=f"{user.player.get_name()}", value=str(user.user_id), description=f"Send trade request to {user.player.get_name()}")

    async def callback(self, interaction: Interaction):
        if await self.trade_view.interaction_check(interaction=interaction):
            self.trade_view.trade.receiver_trader = await self.trade_view.db.get_user_by_id(user_id=int(self.values[0]))
            self.trade_view.stop()

            sender_user = self.trade_view.trade.sender_trader
            receiver_user = self.trade_view.trade.receiver_trader

            await interaction.response.edit_message(content=f"**{sender_user.player.get_name()}** `initiated trade with `**{receiver_user.player.get_name()}**", view=None)
        else:
            await interaction.response.defer()

class TradeItemSelect(Select):
    def __init__(self, trade_view: TradeView):
        super().__init__(placeholder=f"\U0001F9F0 Select Item to Trade!")
        self.trade_view: TradeView = trade_view

        self.set_options()
    
    def set_options(self):
        self.add_option(label="\U00002694\uFE0F TRADE WEAPON", value="TW", description="Trade a weapon from inventory (add or remove offer).")
        self.add_option(label="\U0001F6E1\uFE0F TRADE ARMOR", value="TA", description="Trade an armor from inventory (add or remove offer).")
        self.add_option(label="\U00002697\uFE0F TRADE POTION", value="TP", description="Trade a potion from inventory (add or remove offer).")
        self.add_option(label="\U0001F6E0\uFE0F TRADE KIT", value="TK", description="Trade a kit from inventory (add or remove offer).")
        self.add_option(label="\U0001F642 TRADE DECORATOR", value="TD", description="Trade a decorator from inventory (add or remove offer).")

    async def callback(self, interaction: Interaction):
        if await self.trade_view.interaction_check(interaction=interaction):
            if self.values[0] == "TW":
                trade_weapon = TradeWeaponSelect(trade_view=self.trade_view)
                await trade_weapon.set_options()

                self.trade_view.clear_items()
                self.trade_view.add_item(item=trade_weapon)
                await self.trade_view.add_button_items()

                await interaction.response.edit_message(view=self.trade_view)
            elif self.values[0] == "TA":
                trade_armor = TradeArmorSelect(trade_view=self.trade_view)
                await trade_armor.set_options()

                self.trade_view.clear_items()
                self.trade_view.add_item(item=trade_armor)
                await self.trade_view.add_button_items()

                await interaction.response.edit_message(view=self.trade_view)
            elif self.values[0] == "TP":
                trade_potion = TradePotionSelect(trade_view=self.trade_view)
                await trade_potion.set_options()

                self.trade_view.clear_items()
                self.trade_view.add_item(item=trade_potion)
                await self.trade_view.add_button_items()

                await interaction.response.edit_message(view=self.trade_view)
            elif self.values[0] == "TK":
                trade_kit = TradeKitSelect(trade_view=self.trade_view)
                await trade_kit.set_options()

                self.trade_view.clear_items()
                self.trade_view.add_item(item=trade_kit)
                await self.trade_view.add_button_items()

                await interaction.response.edit_message(view=self.trade_view)
            elif self.values[0] == "TD":
                trade_decorator = TradeDecoratorSelect(trade_view=self.trade_view)
                await trade_decorator.set_options()

                self.trade_view.clear_items()
                self.trade_view.add_item(item=trade_decorator)
                await self.trade_view.add_button_items()

                await interaction.response.edit_message(view=self.trade_view)
        else:
            await interaction.response.defer()

class TradeWeaponSelect(Select):
    def __init__(self, trade_view: TradeView):
        super().__init__(placeholder="\U00002694\uFE0F Trade Weapon!")
        self.trade_view: TradeView = trade_view

    async def set_options(self):
        weapons: list[Weapon] = await self.trade_view.user.player.inventory.get_weapons(string_format=False)
        
        if weapons != None:
            for weapon in weapons:
                self.add_option(label=weapon.name, value=str(weapon.uuid), description=f"Trade {weapon.name.lower()} (add or remove offer).")

        self.add_option(label="\U0001F448 GO BACK", value="GB", description="Go back to item select.")
        self.add_option(label="\U0001F4BC CLOSE TRADE", value="CT", description="Close trading window.")

    async def callback(self, interaction: Interaction):
        if await self.trade_view.interaction_check(interaction=interaction):
            if self.values[0] == "GB":
                await self.trade_view.set_followup_items()

                await interaction.response.edit_message(view=self.trade_view)
            elif self.values[0] == "CT":
                self.trade_view.stop()
                
                await interaction.response.edit_message(content="`Trade closed!`", view=None)
            else:
                item_uuid = uuid.UUID(self.values[0])
                item = await self.trade_view.user.player.inventory.find_item(uuid=item_uuid)

                if item != None: 
                    if self.trade_view.user == self.trade_view.trade.sender_trader:
                        if item not in self.trade_view.trade.sender_items_offer:
                            self.trade_view.trade.sender_items_offer.append(item)
                        else:
                            self.trade_view.trade.sender_items_offer.remove(item)
                    else:
                        if item not in self.trade_view.trade.receiver_items_offer:
                            self.trade_view.trade.receiver_items_offer.append(item)
                        else:
                            self.trade_view.trade.receiver_items_offer.remove(item)

                self.trade_view.stop()
                await interaction.response.defer()
        else:
            await interaction.response.defer()   

class TradeArmorSelect(Select):
    def __init__(self, trade_view: TradeView):
        super().__init__(placeholder="\U0001F6E1\uFE0F Trade Armor!")
        self.trade_view: TradeView = trade_view

    async def set_options(self):
        armors: list[Armor] = await self.trade_view.user.player.inventory.get_armors(string_format=False)
        
        if armors != None:
            for armor in armors:
                self.add_option(label=armor.name, value=str(armor.uuid), description=f"Trade {armor.name.lower()} (add or remove offer).")

        self.add_option(label="\U0001F448 GO BACK", value="GB", description="Go back to item select.")
        self.add_option(label="\U0001F4BC CLOSE TRADE", value="CT", description="Close trading window.")

    async def callback(self, interaction: Interaction):
        if await self.trade_view.interaction_check(interaction=interaction):
            if self.values[0] == "GB":
                await self.trade_view.set_followup_items()

                await interaction.response.edit_message(view=self.trade_view)
            elif self.values[0] == "CT":
                self.trade_view.stop()
                
                await interaction.response.edit_message(content="`Trade closed!`", view=None)
            else:
                item_uuid = uuid.UUID(self.values[0])
                item = await self.trade_view.user.player.inventory.find_item(uuid=item_uuid)

                if item != None: 
                    if self.trade_view.user == self.trade_view.trade.sender_trader:
                        if item not in self.trade_view.trade.sender_items_offer:
                            self.trade_view.trade.sender_items_offer.append(item)
                        else:
                            self.trade_view.trade.sender_items_offer.remove(item)
                    else:
                        if item not in self.trade_view.trade.receiver_items_offer:
                            self.trade_view.trade.receiver_items_offer.append(item)
                        else:
                            self.trade_view.trade.receiver_items_offer.remove(item)

                self.trade_view.stop()
                await interaction.response.defer()
            pass
        else:
            await interaction.response.defer()   

class TradePotionSelect(Select):
    def __init__(self, trade_view: TradeView):
        super().__init__(placeholder="\U00002697\uFE0F Trade Potion!")
        self.trade_view: TradeView = trade_view

    async def set_options(self):
        potions: list[Potion] = await self.trade_view.user.player.inventory.get_potions(string_format=False)
        
        if potions != None:
            for potion in potions:
                self.add_option(label=potion.name, value=str(potion.uuid), description=f"Trade {potion.name.lower()} (add or remove offer).")

        self.add_option(label="\U0001F448 GO BACK", value="GB", description="Go back to item select.")
        self.add_option(label="\U0001F4BC CLOSE TRADE", value="CT", description="Close trading window.")

    async def callback(self, interaction: Interaction):
        if await self.trade_view.interaction_check(interaction=interaction):
            if self.values[0] == "GB":
                await self.trade_view.set_followup_items()

                await interaction.response.edit_message(view=self.trade_view)
            elif self.values[0] == "CT":
                self.trade_view.stop()
                
                await interaction.response.edit_message(content="`Trade closed!`", view=None)
            else:
                item_uuid = uuid.UUID(self.values[0])
                item = await self.trade_view.user.player.inventory.find_item(uuid=item_uuid)

                if item != None: 
                    if self.trade_view.user == self.trade_view.trade.sender_trader:
                        if item not in self.trade_view.trade.sender_items_offer:
                            self.trade_view.trade.sender_items_offer.append(item)
                        else:
                            self.trade_view.trade.sender_items_offer.remove(item)
                    else:
                        if item not in self.trade_view.trade.receiver_items_offer:
                            self.trade_view.trade.receiver_items_offer.append(item)
                        else:
                            self.trade_view.trade.receiver_items_offer.remove(item)

                self.trade_view.stop()
                await interaction.response.defer()
            pass
        else:
            await interaction.response.defer()  

class TradeKitSelect(Select):
    def __init__(self, trade_view: TradeView):
        super().__init__(placeholder="\U0001F6E0\uFE0F Trade Kit!")
        self.trade_view: TradeView = trade_view

    async def set_options(self):
        kits: list[Kit] = await self.trade_view.user.player.inventory.get_kits(string_format=False)
        
        if kits != None:
            for kit in kits:
                self.add_option(label=kit.name, value=str(kit.uuid), description=f"Trade {kit.name.lower()} (add or remove offer).")

        self.add_option(label="\U0001F448 GO BACK", value="GB", description="Go back to item select.")
        self.add_option(label="\U0001F4BC CLOSE TRADE", value="CT", description="Close trading window.")

    async def callback(self, interaction: Interaction):
        if await self.trade_view.interaction_check(interaction=interaction):
            if self.values[0] == "GB":
                await self.trade_view.set_followup_items()

                await interaction.response.edit_message(view=self.trade_view)
            elif self.values[0] == "CT":
                self.trade_view.stop()
                
                await interaction.response.edit_message(content="`Trade closed!`", view=None)
            else:
                item_uuid = uuid.UUID(self.values[0])
                item = await self.trade_view.user.player.inventory.find_item(uuid=item_uuid)

                if item != None: 
                    if self.trade_view.user == self.trade_view.trade.sender_trader:
                        if item not in self.trade_view.trade.sender_items_offer:
                            self.trade_view.trade.sender_items_offer.append(item)
                        else:
                            self.trade_view.trade.sender_items_offer.remove(item)
                    else:
                        if item not in self.trade_view.trade.receiver_items_offer:
                            self.trade_view.trade.receiver_items_offer.append(item)
                        else:
                            self.trade_view.trade.receiver_items_offer.remove(item)

                self.trade_view.stop()
                await interaction.response.defer()
            pass
        else:
            await interaction.response.defer()   

class TradeDecoratorSelect(Select):
    def __init__(self, trade_view: TradeView):
        super().__init__(placeholder="\U0001F642 Trade Decorator!")
        self.trade_view: TradeView = trade_view

    async def set_options(self):
        decorators: list[Decorator] = await self.trade_view.user.player.inventory.get_decorators(string_format=False)
        
        if decorators != None:
            for decorator in decorators:
                self.add_option(label=decorator.name, value=str(decorator.uuid), description=f"Trade {decorator.name.lower()} (add or remove offer).")

        self.add_option(label="\U0001F448 GO BACK", value="GB", description="Go back to item select.")
        self.add_option(label="\U0001F4BC CLOSE TRADE", value="CT", description="Close trading window.")

    async def callback(self, interaction: Interaction):
        if await self.trade_view.interaction_check(interaction=interaction):
            if self.values[0] == "GB":
                await self.trade_view.set_followup_items()

                await interaction.response.edit_message(view=self.trade_view)
            elif self.values[0] == "CT":
                self.trade_view.stop()
                
                await interaction.response.edit_message(content="`Trade closed!`", view=None)
            else:
                item_uuid = uuid.UUID(self.values[0])
                item = await self.trade_view.user.player.inventory.find_item(uuid=item_uuid)

                if item != None: 
                    if self.trade_view.user == self.trade_view.trade.sender_trader:
                        if item not in self.trade_view.trade.sender_items_offer:
                            self.trade_view.trade.sender_items_offer.append(item)
                        else:
                            self.trade_view.trade.sender_items_offer.remove(item)
                    else:
                        if item not in self.trade_view.trade.receiver_items_offer:
                            self.trade_view.trade.receiver_items_offer.append(item)
                        else:
                            self.trade_view.trade.receiver_items_offer.remove(item)

                self.trade_view.stop()
                await interaction.response.defer()
            pass
        else:
            await interaction.response.defer()   