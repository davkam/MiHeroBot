from data.database import Database
from discord import Interaction
from discord.ui import View, TextInput
from users.users import User

class TradeView(View):
    def __init__(self, user: User, db: Database):
        super().__init__(timeout=60)
        self.user: User = user
        self.db: Database = db
        
        self.set_items()

    def set_items(self):
        from interface.selects.trade_selects import TradePlayerSelect, TradeItemSelect
        self.add_item(item=TradePlayerSelect(trade_view=self))
        self.add_item(item=TradeItemSelect(trade_view=self))
        #self.add_item(item=TextInput(label="GOLD", placeholder="Enter gold amount..."))

    async def interaction_check(self, interaction: Interaction):
        if interaction.user.id == self.user.user_id:
            return True
        return False