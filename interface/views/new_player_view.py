import discord

from users.users import User

class NewPlayerView(discord.ui.View):
    def __init__(self, user: User, character: int = None):
        super().__init__(timeout=60)
        self.user: User = user
        self.character: int = character or 1
        self.selected: bool = False
        self.canceled: bool = False

        self.set_buttons()

    def set_buttons(self):
        from interface.buttons.new_player_buttons import PreviousButton, NextButton, SelectButton, CancelButton
        self.add_item(PreviousButton(new_player_view=self))
        self.add_item(NextButton(new_player_view=self))
        self.add_item(SelectButton(new_player_view=self))
        self.add_item(CancelButton(new_player_view=self))

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.user.id:
            return True
        return False