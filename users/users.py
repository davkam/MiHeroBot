from discord import User
from game.objects.characters.players import Player, PlayerColor
from tools.tools import StringManager

class User(User):
    __slots__ = ['id', 'name', 'player', 'permit']

    def __init__(self, id: int = None, name: str = None):
        self.id: int = id
        self.name: str = name
        self.player: Player = None
        self.permit: bool = True

    # TODO: Implement the following properties.
    # @property
    # def id(self) -> int:
    #     return self._id

    # @id.setter
    # def id(self, value: int):
    #     self._id = value

    # @property
    # def name(self) -> str:
    #     return self._name

    # @name.setter
    # def name(self, value: str):
    #     self._name = value

    async def new_player(self, color: PlayerColor):
        """
        Create a new player with the given color.

        Args:
            color (PlayerColor): The color of the new player.
        """
        player_name = await StringManager.remove_special_characters(input_string=self.name)
        self.player = Player(name=player_name, color=color)

    async def del_player(self):
        """
        Delete the current player.
        """
        self.player = None