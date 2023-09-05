from typing import Any
from discord import ButtonStyle
from discord.interactions import Interaction
from discord.ui import Button
from interface.modals.trade_modal import TradeModal
from interface.views.trade_view import TradeView
from users.users import User

class AcceptTradeButton(Button):
    def __init__(self, trade_view: TradeView, trade):
        super().__init__(style=ButtonStyle.green, label="ACCEPT")
        from game.logic.trade import Trade
        self.trade_view: TradeView = trade_view
        self.trade: Trade = trade

    async def callback(self, interaction: Interaction):
        if await self.trade_view.interaction_check(interaction=interaction):
            if self.trade_view.user == self.trade.sender_trader:
                self.trade.sender_trade_status = True
            else:
                self.trade.receiver_trade_status = True

            self.trade_view.stop()
            await interaction.response.defer()
        else:
            await interaction.response.defer()

class DeclineTradeButton(Button):
    def __init__(self, trade_view: TradeView, trade):
        super().__init__(style=ButtonStyle.red, label="DECLINE")
        from game.logic.trade import Trade
        self.trade_view: TradeView = trade_view
        self.trade: Trade = trade

    async def callback(self, interaction: Interaction):
        if await self.trade_view.interaction_check(interaction=interaction):
            if self.trade_view.user == self.trade.sender_trader:
                self.trade.sender_trade_status = False
            else:
                self.trade.receiver_trade_status = False

            self.trade_view.stop()
            await interaction.response.defer()
        else:
            await interaction.response.defer()

class GoldTradeButton(Button):
    def __init__(self, trade_view: TradeView, trade):
        super().__init__(style=ButtonStyle.gray, label="SUBMIT GOLD")
        from game.logic.trade import Trade
        self.trade_view: TradeView = trade_view
        self.trade: Trade = trade
    
    async def callback(self, interaction: Interaction):
        if await self.trade_view.interaction_check(interaction=interaction):
            trade_modal = TradeModal(trade_view=self.trade_view, trade=self.trade)
            
            await interaction.response.send_modal(trade_modal)
        else:
            await interaction.response.defer()
