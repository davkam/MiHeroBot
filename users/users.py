from game.objects.characters import Player

class User():
    def __init__(self, username = None, user_id = None) -> None:
        self.username: str = username   # Discord username (author.name).
        self.user_id: int = user_id     # Discord userID (author.id).
        self.player: Player = None      # Player() object.

    async def new_player(self):
        self.player = Player(self.username)

    async def del_player(self):
        self.player = None