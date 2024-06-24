from discord import Interaction
from discord.ui import Select
from interface.views.fight_view import FightView, FightButtonView
from users.users import User

class FightSelect(Select):
    def __init__(self, fight_view: FightView):
        super().__init__(placeholder="SELECT FIGHT")
        self.fight_view: FightView = fight_view

        self.set_options()

    def set_options(self):
        self.add_option(label="FIGHT MONSTER", value="FM", description="- Fight a light, medium or heavy monster.")
        self.add_option(label="FIGHT PLAYER", value="FP", description="- Fight a player from active users.")

    async def callback(self, interaction: Interaction):
        if await self.fight_view.interaction_check(interaction=interaction):
            if self.values[0] == "FM":
                monster_select = MonsterSelect(fight_view=self.fight_view)
                self.fight_view.clear_items()
                self.fight_view.add_item(item=monster_select)

                await interaction.response.edit_message(view=self.fight_view)
            elif self.values[0] == "FP":
                player_select = PlayerSelect(fight_view=self.fight_view)
                self.fight_view.clear_items()
                self.fight_view.add_item(item=player_select)

                await interaction.response.edit_message(view=self.fight_view)
        else:
            await interaction.response.defer()

class PlayerSelect(Select):
    def __init__(self, fight_view: FightView):
        super().__init__(placeholder="SELECT PLAYER")
        self.fight_view: FightView = fight_view

        self.set_options()
                
    def set_options(self): # TBD: Pre-set options, alphabetically!
        db = self.fight_view.db
        for user in db.users.values():
            if user != self.fight_view.sender_user:
                user: User = user # Assign type object for access to User-object
                self.add_option(label=f"{user.player.get_name()} (LVL {user.player.level.get_lvl()})", value=str(user.id))

        self.add_option(label="GO BACK", value="GB", description="- Go back to fight selection.")

    async def callback(self, interaction: Interaction):
        db = self.fight_view.db
        if await self.fight_view.interaction_check(interaction=interaction):
            if self.values[0] == "GB":
                fight_select = FightSelect(fight_view=self.fight_view)
                self.fight_view.clear_items()
                self.fight_view.add_item(item=fight_select)

                await interaction.response.edit_message(view=self.fight_view)
            else:
                id = int(self.values[0])
                self.fight_view.receiver_user = await db.get_user(id=id)

                button_view = FightButtonView(fight_view=self.fight_view, user=self.fight_view.receiver_user)
                message = f"**{self.fight_view.sender_user.player.get_name()}** `challenges` **{self.fight_view.receiver_user.player.get_name()}** `to a battle.`"

                await interaction.response.edit_message(content=message, view=button_view)
        else:
            await interaction.response.defer()

class MonsterSelect(Select):
    def __init__(self, fight_view: FightView):
        super().__init__(placeholder="SELECT MONSTER")
        self.fight_view: FightView = fight_view
        self.set_options()

    def set_options(self):
        self.add_option(label="LIGHT MONSTER", value="LM")
        self.add_option(label="MEDIUM MONSTER", value="MM")
        self.add_option(label="HEAVY MONSTER", value="HM")
        self.add_option(label="GO BACK", value="GB", description="- Go back to fight selection.")

    async def callback(self, interaction: Interaction):
        if await self.fight_view.interaction_check(interaction=interaction):
            if self.values[0] == "GB":
                fight_select = FightSelect(fight_view=self.fight_view)
                self.fight_view.clear_items()
                self.fight_view.add_item(item=fight_select)
                
                await interaction.response.edit_message(view=self.fight_view)
                return
            elif self.values[0] == "LM":
                self.fight_view.select_type = "MonsterLight"
                self.fight_view.clear_items()
                message = f"**{self.fight_view.sender_user.player.get_name()}** `encounters a light monster.`"

                await interaction.response.edit_message(content=message, view=self.fight_view)
            elif self.values[0] == "MM":
                self.fight_view.select_type = "MonsterMedium"
                self.fight_view.clear_items()
                message = f"**{self.fight_view.sender_user.player.get_name()}** `encounters a medium monster.`"

                await interaction.response.edit_message(content=message, view=self.fight_view)
            elif self.values[0] == "HM":
                self.fight_view.select_type = "MonsterHeavy"
                self.fight_view.clear_items()
                message = f"**{self.fight_view.sender_user.player.get_name()}** `encounters a heavy monster.`"

                await interaction.response.edit_message(content=message, view=self.fight_view)

            self.fight_view.stop()
        else:
            await interaction.response.defer()