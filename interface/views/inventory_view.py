from discord import Interaction
from discord.ui import View
from users.users import User

class InventoryView(View):
    def __init__(self, user: User):
        super().__init__(timeout=60)
        self.user: User = user
        self.response: str = None
        self.success: bool = False
        self.close_view: bool = False

        from interface.selects.inventory_selects import InventorySelect
        self.add_item(item=InventorySelect(self))

    async def interaction_check(self, interaction: Interaction):
        if interaction.user.id == self.user.user_id:
            return True
        return False