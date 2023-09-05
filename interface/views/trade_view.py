from data.database import Database
from discord import Interaction
from discord.ui import View
from users.users import User

class TradeView(View):
    def __init__(self, db: Database, trade, user: User):
        super().__init__(timeout=120)
        from game.logic.trade import Trade
        self.db: Database = db
        self.trade: Trade = trade
        self.user: User = user

    async def set_initial_items(self):
        from interface.selects.trade_selects import TradePlayerSelect
        self.player_select = TradePlayerSelect(trade_view=self)
        self.add_item(item=self.player_select)

    async def set_followup_items(self):
        from interface.selects.trade_selects import TradeItemSelect
        item_select = TradeItemSelect(trade_view=self)

        self.clear_items()
        self.add_item(item=item_select)

        await self.add_button_items()

    async def add_button_items(self):
        from interface.buttons.trade_buttons import AcceptTradeButton, DeclineTradeButton, GoldTradeButton

        gold_button = GoldTradeButton(trade_view=self, trade=self.trade)
        accept_button = AcceptTradeButton(trade_view=self, trade=self.trade)
        decline_button = DeclineTradeButton(trade_view=self, trade=self.trade)
        
        self.add_item(item=gold_button)
        self.add_item(item=accept_button)
        self.add_item(item=decline_button)

    async def interaction_check(self, interaction: Interaction):
        if interaction.user.id == self.user.user_id:
            return True
        return False