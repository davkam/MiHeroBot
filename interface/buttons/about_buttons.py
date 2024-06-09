import discord

from interface.views.about_view import AboutView

class FirstButton(discord.ui.Button):
    def __init__(self, about_view: AboutView):
        super().__init__(style=discord.ButtonStyle.gray, label="\U000023EE FIRST")
        self.about_view: AboutView = about_view

    async def callback(self, interaction: discord.Interaction):
        if self.about_view.page != 1:
            self.about_view.page = 1
            self.about_view.stop()

            await interaction.response.defer()
        else:
            await interaction.response.defer()

class PreviousButton(discord.ui.Button):
    def __init__(self, about_view: AboutView):
        super().__init__(style=discord.ButtonStyle.gray, label="\U000023EA PREVIOUS")
        self.about_view: AboutView = about_view

    async def callback(self, interaction: discord.Interaction):
        if not self.about_view.page <= 1:
            self.about_view.page -= 1
            self.about_view.stop()

            await interaction.response.defer()
        else:
            await interaction.response.defer()

class NextButton(discord.ui.Button):
    def __init__(self, about_view: AboutView):
        super().__init__(style=discord.ButtonStyle.gray, label="NEXT \U000023E9")
        self.about_view: AboutView = about_view

    async def callback(self, interaction: discord.Interaction):
        if not self.about_view.page >= 5:
            self.about_view.page += 1
            self.about_view.stop()

            await interaction.response.defer()
        else:
            await interaction.response.defer()

class LastButton(discord.ui.Button):
    def __init__(self, about_view: AboutView):
        super().__init__(style=discord.ButtonStyle.gray, label="LAST \U000023ED")
        self.about_view: AboutView = about_view

    async def callback(self, interaction: discord.Interaction):
        if self.about_view.page != 5:
            self.about_view.page = 5
            self.about_view.stop()

            await interaction.response.defer()
        else:
            await interaction.response.defer()