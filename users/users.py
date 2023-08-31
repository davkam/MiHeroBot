from game.objects.characters import Player

class User():
    def __init__(self, user_id = None, username = None):
        self.user_id: int = user_id
        self.username: str = username
        self.player: Player = None
        self.permit_interaction: bool = True

    async def new_player(self):
        self.player = Player(name=self.username)

    async def del_player(self):
        self.player = None