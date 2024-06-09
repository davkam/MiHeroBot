from game.objects.characters.players import Player, PlayerColor

class User():
    def __init__(self, id: int = None, name: str = None):
        self.id: int = id
        self.name: str = name
        self.player: Player = None
        self.permit: bool = True

    async def new_player(self, color: PlayerColor):
        self.player = Player(name=self.name, color=color)

    async def del_player(self):
        self.player = None