from game.objects.characters import Player

class User():
    def __init__(self, user_id = None, username = None):
        self.user_id: int = user_id             # Discord userID (author.id).
        self.username: str = username           # Discord username (author.name).
        self.player: Player = None              # Player() object.
        self.permit_interaction: bool = True    # Boolean, true is user is allowed interaction with bot. False if user is in e.g. fight instance. 

    async def new_player(self):
        self.player = Player(name=self.username)

    async def del_player(self):
        self.player = None