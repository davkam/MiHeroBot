import discord

class AboutView(discord.ui.View):
    def __init__(self, page: int = None):
        super().__init__(timeout=60)
        self.page = page or 1

        self.set_buttons()

    def set_buttons(self):
        from interface.buttons.about_buttons import FirstButton, PreviousButton, NextButton, LastButton
        self.add_item(FirstButton(about_view=self))
        self.add_item(PreviousButton(about_view=self))
        self.add_item(NextButton(about_view=self))
        self.add_item(LastButton(about_view=self))