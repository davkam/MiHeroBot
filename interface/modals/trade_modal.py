import discord
from discord.interactions import Interaction

from discord.ui import Modal, TextInput
from interface.views.trade_view import TradeView
from users.users import User

class TradeModal(Modal):
    def __init__(self, trade_view: TradeView, trade):
        super().__init__(title=f"Submit Gold Offer!", timeout=120)
        from game.logic.trade import Trade
        self.trade_view: TradeView = trade_view
        self.trade: Trade = trade

        self.set_modal()

    def set_modal(self):
        self.gold_amount = TextInput(label=f"GOLD OFFER: (AVAILABLE GOLD: {self.trade_view.user.player.gold} GOLD)", placeholder="Enter gold amount... (only a number below available gold)")
        self.add_item(item=self.gold_amount)

    async def on_submit(self, interaction: discord.Interaction):
        if self.trade_view.user == self.trade.sender_trader:
            try:
                gold = int(self.gold_amount.value)
            except:
                await interaction.response.defer()
                return
            
            if self.trade_view.user.player.gold > gold:
                self.trade.sender_gold_offer = gold

                self.trade_view.stop()
                await interaction.response.defer()
            else:
                await interaction.response.defer()
        else:
            try:
                gold = int(self.gold_amount.value)
            except:
                await interaction.response.defer()
                return
            
            if self.trade_view.user.player.gold > gold:
                self.trade.receiver_gold_offer = gold
                
                self.trade_view.stop()
                await interaction.response.defer()
            else:
                await interaction.response.defer()

    async def on_error(self, interaction: Interaction, error: Exception):
        return await super().on_error(interaction, error)