from typing import Any
from discord.interactions import Interaction
from discord.ui import Select
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
            if user != self.trade_view.user:
                user: User = user
                self.add_option(label=f"{user.player.get_name()}", value=str(user.user_id), description=f"Send trade request to {user.player.get_name()}")

    async def callback(self, interaction: Interaction):
        if await self.trade_view.interaction_check(interaction=interaction):

            await interaction.response.edit_message(content=f"**```arm\r\n{self.trade_view.user.player.name} !Trade\r\n```**", view=None)
        else:
            await interaction.response.defer()

class TradeItemSelect(Select):
    def __init__(self, trade_view: TradeView):
        super().__init__(placeholder="\U0001F9F0 Select Item to Trade!")
        self.trade_view: TradeView = trade_view

        self.set_options()
    
    def set_options(self):
        self.add_option(label="\U00002694\uFE0F TRADE WEAPON", value="TW", description="Trade a weapon from inventory.")
        self.add_option(label="\U0001F6E1\uFE0F TRADE ARMOR", value="TA", description="Trade an armor from inventory.")
        self.add_option(label="\U00002697\uFE0F TRADE POTION", value="TP", description="Trade a potion from inventory.")
        self.add_option(label="\U0001F6E0\uFE0F TRADE KIT", value="TK", description="Trade a kit from inventory.")
        self.add_option(label="\U0001F642 TRADE DECORATOR", value="TD", description="Trade a decorator from inventory.")

    async def callback(self, interaction: Interaction):
        if await self.trade_view.interaction_check(interaction=interaction):
            if self.values[0] == "TW":
                pass
            elif self.values[0] == "TA":
                pass
            elif self.values[0] == "TP":
                pass
            elif self.values[0] == "TK":
                pass
            elif self.values[0] == "TD":
                pass
        else:
            await interaction.response.defer()

class TradeWeaponSelect(Select):
    pass

class TradeArmorSelect(Select):
    pass

class TradePotionSelect(Select):
    pass

class TradeKitSelect(Select):
    pass

class TradeDecoratorSelect(Select):
    pass