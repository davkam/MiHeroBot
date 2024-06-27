from discord import Interaction, ButtonStyle
from discord.ui import Button
from interface.views.fight_view import FightView
from users.users import User

class GreenFightButton(Button):
    def __init__(self, fight_view: FightView, user: User):
        super().__init__(label="ACCEPT", style=ButtonStyle.green)
        self.fight_view: FightView = fight_view
        self.user: User = user

    async def callback(self, interaction: Interaction):
        if interaction.user.id == self.user.id:
            self.fight_view.clear_items()
            self.fight_view.stop()
            self.fight_view.select_type = "Player"

            message = f"**{self.user.player.get_name()}** `accepts the challenge and prepares for battle...`"
            await interaction.response.edit_message(content=message, view=self.fight_view)
        else:
            await interaction.response.defer()

class RedFightButton(Button):
    def __init__(self, fight_view: FightView, user: User):
        super().__init__(label="DECLINE", style=ButtonStyle.red)
        self.fight_view: FightView = fight_view
        self.user: User = user

    async def callback(self, interaction: Interaction):
        if interaction.user.id == self.user.id:
            self.fight_view.clear_items()
            self.fight_view.stop()

            message = f"**{self.user.player.get_name()}** `declines the challenge and runs away!`"
            await interaction.response.edit_message(content=message, view=self.fight_view)      
        else:
            await interaction.response.defer()