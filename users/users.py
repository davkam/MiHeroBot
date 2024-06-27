from discord import User
from game.objects.characters.players import Player, PlayerColor
from tools.tools import StringManager

class User(User):
    def __init__(self, id: int = None, name: str = None):
        self.id: int = id
        self.name: str = name
        self.player: Player = None
        self.permit: bool = True

    async def new_player(self, color: PlayerColor):
        player_name = await StringManager.remove_special_characters(input_string=self.name)
        self.player = Player(name=player_name, color=color)

    async def del_player(self):
        self.player = None