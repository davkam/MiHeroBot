from users.users import User
import json
import os.path

# Database() object containing User() objects in a dictionary.
class Database():
    instance = None # Static attribute of Database() instance.

    # Instantiated through singleton pattern, only one instance created.
    # Instantiated at bot.ready_respond() and assigned to Database.instance attribute.
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.users = dict() # Dictionary of User() objects; KEY: -> author.id; VALUE: -> User().

    # Adds new User() to dictionary.
    async def add_user(self, user: User):
        self.users[user.user_id] = user

    # Removes existing User() from dictionary.
    async def rem_user(self, user: User):
        del self.users[user.user_id]

    # Gets existing User() from dictionary by id, returns User().
    async def get_userbyId(self, user_id: int) -> User:
        return self.users[user_id]

    # Checks if dictionary contains user by id, returns bool.
    async def contains_user(self, user_id: int) -> bool:
        if user_id in self.users.keys():
            return True
        else:
            return False
        
    async def load_users(self):
        pass

    async def save_users(self):
        pass