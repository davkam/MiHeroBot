from game.objects.items import Weapon, Armor, Potion, Kit, Decorator
from users.users import User
import json
import os.path

# Database() object containing User() objects in a dictionary.
class Database():
    instance = None # Class attribute of Database() instance.

    # Instantiated through singleton pattern, only one instance created.
    # Instantiated at bot.ready_respond() and assigned to Database.instance attribute.
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.users: dict[int, User] = dict() # Dictionary of User() objects; KEY: -> author.id; VALUE: -> User().
        self.file_path: str = "data/db_users.json"

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
        
    async def save_users(self):
        if len(self.users) == 0: return
        try:
            with open(self.file_path, "w") as user_data:
                write_data = await self.encode_data()
                json.dump(write_data, user_data, indent = 4, sort_keys = True)
                print(f'> User data successfully saved to file "{self.file_path}".')
        except Exception as exception:
            print(f'> Failed to save user data to file "{self.file_path}".\n' + str(exception))
        
    async def load_users(self):
        try:
            if os.path.exists(path=self.file_path):
                with open(self.file_path, "r") as user_data:
                    read_data = json.load(user_data)
                    await self.decode_data(data=read_data)
                    print(f'> User data successfully loaded from file "{self.file_path}".')
            else:
                print(f'> User data file "{self.file_path}" could not be found.')
        except Exception as exception:
            print(f'> Failed to retrieve user data from file "{self.file_path}".\n' + str(exception))

    # Encodes complex data for json dump. Used in save_data()
    async def encode_data(self):
        encoded_data = dict()
        for id in self.users.keys():
            u = self.users[id]
            data_string = f"{u.username},{u.user_id}:"
            data_string += f"{u.player.name},{u.player.attack.get_xp()},{u.player.defense.get_xp()},{u.player.health.get_xp()},{u.player.lvl.get_xp()},{u.player.gold}:"
            data_string += f"{u.player.weapon.weapon_class.name},{u.player.weapon.attack.get_xp()},{u.player.armor.armor_class.name},{u.player.armor.defense.get_xp()}:"
            data_string += f"{u.player.inventory.slots};"

            for item in u.player.inventory.items:
                if isinstance(item, Weapon):
                    data_string += f"Weapon,{item.weapon_class.name},{item.attack.get_xp()};"
                elif isinstance(item, Armor):
                    data_string += f"Armor,{item.armor_class.name},{item.defense.get_xp()};"
                elif isinstance(item, Potion):
                    data_string += f"Potion,{item.potion_type.name},{item.potion_quality};"
                elif isinstance(item, Kit):
                    data_string += f"Kit,{item.kit_type.name},{item.kit_quality};"
                elif isinstance(item, Decorator):
                    data_string += f"Decorator,{item.emoji},{item.tier};"

            if u.player.decorator != None:
                data_string +=f":{u.player.decorator.emoji},{u.player.decorator.tier}:"

            encoded_data[id] = data_string 

        return encoded_data
    
    async def decode_data(self, data):
        pass