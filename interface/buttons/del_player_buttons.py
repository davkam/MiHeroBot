import discord

from interface.views.del_player_view import DelPlayerView

class InfoButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.gray, label="DELETE CHARACTER:")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

class ConfirmButton(discord.ui.Button):
    def __init__(self, del_player_view: DelPlayerView):
        super().__init__(style=discord.ButtonStyle.green, label="CONFIRM \U00002714")
        self.del_player_view: DelPlayerView = del_player_view

    async def callback(self, interaction: discord.Interaction):
        if await self.del_player_view.interaction_check(interaction=interaction):
            self.del_player_view.confirm = True
            self.del_player_view.stop()

            await interaction.response.defer()
        else:
            await interaction.response.defer()

class CancelButton(discord.ui.Button):
    def __init__(self, del_player_view: DelPlayerView):
        super().__init__(style=discord.ButtonStyle.red, label="CANCEL \U0000274C")
        self.del_player_view: DelPlayerView = del_player_view

    async def callback(self, interaction: discord.Interaction):
        if await self.del_player_view.interaction_check(interaction=interaction):
            self.del_player_view.cancel = True
            self.del_player_view.stop()
            
            await interaction.response.defer()
        else:
            await interaction.response.defer()