from discord.interactions import Interaction
from discord.ui import View
from users.users import User

class FightView(View):
    def __init__(self, user: User):
        from game.interface.selects import FightSelect
        super().__init__(timeout=60)
        self.sender_user: User = user
        self.receiver_user: User = None
        self.success: bool = False
        self.select_type: str = None
        self.add_item(item=FightSelect(self))

    async def interaction_check(self, interaction: Interaction):
        if interaction.user.id == self.sender_user.user_id:
            return True
        return False
    
class FightButtonView(View):
    def __init__(self, fight_view: FightView, user: User):
        from game.interface.buttons import GreenButton, RedButton
        super().__init__()
        self.add_item(GreenButton(fight_view=fight_view, user=user))
        self.add_item(RedButton(fight_view=fight_view, user=user))

class InventoryView(View):
    def __init__(self, user: User):
        from game.interface.selects import InventorySelect
        super().__init__(timeout=60)
        self.user: User = user
        self.response: str = None
        self.success: bool = False
        self.close_view: bool = False
        self.add_item(item=InventorySelect(self))

    async def interaction_check(self, interaction: Interaction):
        if interaction.user.id == self.user.user_id:
            return True
        return False

