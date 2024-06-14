import discord

from users.users import User

class DelPlayerView(discord.ui.View):
    def __init__(self, user: User):
        super().__init__(timeout=60)
        self.user: User = user
        self.confirm: bool = False
        self.cancel: bool = False

        self.set_buttons()

    def set_buttons(self):
        from interface.buttons.del_player_buttons import InfoButton, ConfirmButton, CancelButton
        self.add_item(InfoButton())
        self.add_item(ConfirmButton(del_player_view=self))
        self.add_item(CancelButton(del_player_view=self))

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.user.id:
            return True
        return False