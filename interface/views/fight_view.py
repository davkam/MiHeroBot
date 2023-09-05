from data.database import Database
from discord import Interaction
from discord.ui import View
from users.users import User

class FightView(View):
    def __init__(self, user: User, db: Database):
        super().__init__(timeout=60)
        self.sender_user: User = user
        self.receiver_user: User = None
        self.db: Database = db
        self.success: bool = False
        self.select_type: str = None

        from interface.selects.fight_selects import FightSelect
        self.add_item(item=FightSelect(self))

    async def interaction_check(self, interaction: Interaction):
        if interaction.user.id == self.sender_user.user_id:
            return True
        return False
    
class FightButtonView(View):
    def __init__(self, fight_view: FightView, user: User):
        super().__init__()

        from interface.buttons.fight_buttons import GreenFightButton, RedFightButton
        self.add_item(GreenFightButton(fight_view=fight_view, user=user))
        self.add_item(RedFightButton(fight_view=fight_view, user=user))