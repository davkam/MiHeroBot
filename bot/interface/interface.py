from data.database import Database
from discord.ui import View, Select, Button
from users.users import User
import discord

class FightView(View):
    def __init__(self, user: User):
        super().__init__(timeout = 60)
        self.sender_user: User = user
        self.receiver_user: User = None
        self.success: bool = False
        self.select_type: str = None
        self.add_item(item = FightSelect(self))

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.sender_user.user_id:
            return True
        return False

class FightSelect(Select):
    def __init__(self, fight_view: FightView):
        super().__init__(placeholder = "Select Fight!")
        self.fight_view: FightView = fight_view
        self.set_options()

    def set_options(self):
        self.add_option(label = "FIGHT MONSTER", value = "FM", description = "Fight a light, medium or heavy monster.")
        self.add_option(label = "FIGHT PLAYER", value = "FP", description = "Fight a player from users.")

    async def callback(self, interaction: discord.Interaction):
        if await self.fight_view.interaction_check(interaction = interaction):
            if self.values[0] == "FM":
                monster_select = MonsterSelect(fight_view = self.fight_view)
                self.fight_view.clear_items()
                self.fight_view.add_item(item = monster_select)

                await interaction.response.edit_message(content = "**```arm\r\nMiHero !Fight\r\n```**\n", view = self.fight_view)
            if self.values[0] == "FP":
                player_select = PlayerSelect(fight_view = self.fight_view)
                self.fight_view.clear_items()
                self.fight_view.add_item(item = player_select)

                await interaction.response.edit_message(content = "**```arm\r\nMiHero !Fight\r\n```**\n", view = self.fight_view)
        else:
            await interaction.response.defer()

class PlayerSelect(Select): # TBD: Display player name.
    def __init__(self, fight_view: FightView):
        super().__init__(placeholder = "Select Player!")
        self.fight_view: FightView = fight_view
        self.set_options()
                
    def set_options(self): # TBD: Pre-set options, alphabetically!
        db = Database.instance
        for user in db.users.values():
            if user != self.fight_view.sender_user:
                user: User = user
                self.add_option(label = f"{user.username.upper()}", value = str(user.user_id), description = f"LVL: {user.player.lvl.get_lvl()} ATT: {user.player.attack.get_lvl()} DEF: {user.player.defense.get_lvl()}")

    async def callback(self, interaction: discord.Interaction):
        db = Database.instance
        if await self.fight_view.interaction_check(interaction = interaction):
            id = int(self.values[0])
            self.fight_view.receiver_user: User = await db.get_user(user_id = id)

            button_view = ButtonView(fight_view = self.fight_view, user = self.fight_view.receiver_user)
            message = f"**```arm\r\nMiHero !Fight\r\n```**\n**{str(interaction.user).upper()}** `challenges` **{self.fight_view.receiver_user.username.upper()}** `to a battle.`"

            await interaction.response.edit_message(content = message, view = button_view)
        else:
            await interaction.response.defer()

class MonsterSelect(Select): # TBD: Display player name.
    def __init__(self, fight_view: FightView):
        super().__init__(placeholder = "Select Monster!")
        self.fight_view: FightView = fight_view
        self.set_options()

    def set_options(self):
        self.add_option(label = "LIGHT MONSTER", value = "LM", description = f"Fight a light monster.")
        self.add_option(label = "MEDIUM MONSTER", value = "MM", description = f"Fight a medium monster.")
        self.add_option(label = "HEAVY MONSTER", value = "HM", description = f"Fight a heavy monster.")

    async def callback(self, interaction: discord.Interaction):
        if await self.fight_view.interaction_check(interaction = interaction):
            if self.values[0] == "LM":
                self.fight_view.select_type = "MonsterLight"
                self.fight_view.clear_items()
                message = f"**```arm\r\nMiHero !Fight\r\n```**\n**{interaction.user.name.upper()}** `encounters a light monster.`"

                await interaction.response.edit_message(content = message, view = self.fight_view)
            if self.values[0] == "MM":
                self.fight_view.select_type = "MonsterMedium"
                self.fight_view.clear_items()
                message = f"**```arm\r\nMiHero !Fight\r\n```**\n**{interaction.user.name.upper()}** `encounters a medium monster.`"

                await interaction.response.edit_message(content = message, view = self.fight_view)
            if self.values[0] == "HM":
                self.fight_view.select_type = "MonsterHeavy"
                self.fight_view.clear_items()
                message = f"**```arm\r\nMiHero !Fight\r\n```**\n**{interaction.user.name.upper()}** `encounters a heavy monster.`"

                await interaction.response.edit_message(content = message, view = self.fight_view)

            self.fight_view.success = True
            self.fight_view.stop()
        else:
            await interaction.response.defer()

class ButtonView(View):
    def __init__(self, fight_view: FightView, user: User):
        super().__init__()
        self.add_item(GreenButton(fight_view = fight_view, user = user))
        self.add_item(RedButton(fight_view = fight_view, user = user))

class GreenButton(Button): # TBD: Display player name.
    def __init__(self, fight_view: FightView, user: User):
        super().__init__(label = "ACCEPT", style = discord.ButtonStyle.green)
        self.fight_view: FightView = fight_view
        self.user: User = user

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id == self.user.user_id:
            self.fight_view.clear_items()
            message = f"**```arm\r\nMiHero !Fight\r\n```**\n**{interaction.user.name.upper()}** `accepts the challenge and prepares for battle...`"

            await interaction.response.edit_message(content = message, view = self.fight_view)

            self.fight_view.success = True
            self.fight_view.select_type = "Player"
            self.fight_view.stop()
        else:
            await interaction.response.defer()

class RedButton(Button): # TBD: Display player name.
    def __init__(self, fight_view: FightView, user: User):
        super().__init__(label = "DECLINE", style = discord.ButtonStyle.red)
        self.fight_view: FightView = fight_view
        self.user: User = user

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id == self.user.user_id:
            self.fight_view.clear_items()
            message = f"**```arm\r\nMiHero !Fight\r\n```**\n**{interaction.user.name.upper()}** `declines the challenge and runs away!`"

            await interaction.response.edit_message(content = message, view = self.fight_view)
            
            self.fight_view.success = True
            self.fight_view.stop()
        else:
            await interaction.response.defer()