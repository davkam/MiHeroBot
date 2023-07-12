from users.users import User

# Database(): Database()-object containing User()-objects in a dictionary.
class Database():
    instance = None # Static attribute of a Database()-instance.

    # __new__(): Instantiates through singleton pattern, only one instance allowed.
    #            Instantiated at bot.ready_respond() and assigned to Database.instance.
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.users = dict()     # Dictionary of User() objects, KEY: -> author.id; VALUE: -> User().

    # new_user(): Adds new User() to dictionary.
    async def add_user(self, user: User):
        self.users[user.user_id] = user

    # del_user(): Removes existing User() from dictionary.
    async def rem_user(self, user: User):
        del self.users[user.user_id]

    # get_user(): Gets existing User() from dictionary.
    async def get_user(self, user_id: int):
        return self.users[user_id]

    # contains_user(): Checks if dictionary contains user, returns bool.
    async def contains_user(self, user_id: int):
        if user_id in self.users.keys():
            return True
        else:
            return False
        
    async def load_users(self):
        pass

    async def save_users(self):
        pass