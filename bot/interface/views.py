from bot.interface.buttons import GreenButton, RedButton
from discord.ui import View
from users.users import User
import discord

class FightView(View):
    def __init__(self, user: User):
        from bot.interface.selects import FightSelect
        super().__init__(timeout = 60)
        self.sender_user: User = user
        self.receiver_user: User = None
        self.success: bool = False
        self.select_type: str = None
        self.add_item(item = FightSelect(self))

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.sender_user.user_id:
            return True
        return False
    
class ButtonView(View):
    def __init__(self, fight_view: FightView, user: User):
        super().__init__()
        self.add_item(GreenButton(fight_view = fight_view, user = user))
        self.add_item(RedButton(fight_view = fight_view, user = user))
