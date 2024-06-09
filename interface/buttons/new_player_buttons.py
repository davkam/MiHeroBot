import discord

from interface.views.new_player_view import NewPlayerView

class PreviousButton(discord.ui.Button):
    def __init__(self, new_player_view: NewPlayerView):
        super().__init__(style=discord.ButtonStyle.gray, label="\U000023EA PREVIOUS")
        self.new_player_view: NewPlayerView = new_player_view

    async def callback(self, interaction: discord.Interaction):
        if await self.new_player_view.interaction_check(interaction=interaction):
            if self.new_player_view.character > 1:
                self.new_player_view.character -= 1
                self.new_player_view.stop()

                await interaction.response.defer()
            else:
                self.new_player_view.character = 4
                self.new_player_view.stop()

                await interaction.response.defer()
        else:
            await interaction.response.defer()

class NextButton(discord.ui.Button):
    def __init__(self, new_player_view: NewPlayerView):
        super().__init__(style=discord.ButtonStyle.gray, label="NEXT \U000023E9")
        self.new_player_view: NewPlayerView = new_player_view

    async def callback(self, interaction: discord.Interaction):
        if await self.new_player_view.interaction_check(interaction=interaction):
            if self.new_player_view.character < 4:
                self.new_player_view.character += 1
                self.new_player_view.stop()

                await interaction.response.defer()
            else:
                self.new_player_view.character = 1
                self.new_player_view.stop()

                await interaction.response.defer()
        else:
            await interaction.response.defer()

class SelectButton(discord.ui.Button):
    def __init__(self, new_player_view: NewPlayerView):
        super().__init__(style=discord.ButtonStyle.green, label="SELECT \U00002714")
        self.new_player_view: NewPlayerView = new_player_view

    async def callback(self, interaction: discord.Interaction):
        if await self.new_player_view.interaction_check(interaction=interaction):
            self.new_player_view.selected = True
            self.new_player_view.stop()

            await interaction.response.defer()
        else:
            await interaction.response.defer()

class CancelButton(discord.ui.Button):
    def __init__(self, new_player_view: NewPlayerView):
        super().__init__(style=discord.ButtonStyle.red, label="CANCEL \U0000274C")
        self.new_player_view: NewPlayerView = new_player_view

    async def callback(self, interaction: discord.Interaction):
        if await self.new_player_view.interaction_check(interaction=interaction):
            self.new_player_view.canceled = True
            self.new_player_view.stop()
            
            await interaction.response.defer()
        else:
            await interaction.response.defer()