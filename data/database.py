from game.objects.characters import Player
from game.objects.items import *
from log.logger import Logger
from users.users import User
import discord
import json
import os.path

# Database object containing user dictionaries, file paths, and a logger.
# Logic for user related data is composed of two types, a temporary data (used during runtime for changes in a user object) and a permanent data (stored data of all users).
class Database():
    instances: dict = dict()    # Satic class dictionary of all database instances as values, accessed through guild(channel) ID as key. 
    
    def __init__(self, db_id: int):
        self.db_id: int = db_id                                         # Database ID, unique for each database, represents guild(channel) ID.
        self.users: dict[int, User] = dict()                            # Dictionary of user objects; KEY -> User ID, VALUE -> User object.
        self.temp_data: dict[int, User] = dict()                        # Temporary dictionary used in loading temporary save data.
        self.save_file: str = f"data/saves/save_{db_id}.json"
        self.temp_file: str = f"data/saves/temp/tempsave_{db_id}.txt"
        self.log: Logger = Logger.data_logger

    # Static class method.
    # Creates new instances of databases according to guilds(channels) connected to client.
    @classmethod
    async def load_databases(cls, client: discord.Client):
        async for guild in client.fetch_guilds():
            cls.instances[guild.id] = Database(db_id=guild.id)
            db: Database = cls.instances[guild.id]

            # Loads data for each database.
            await db.log.write_log(log_data=f"Loading databases for {guild.name} (ID={guild.id})")
            await db.load_data()
            await db.load_temp_data()
            print()

    # Adds new user object to dictionary.
    async def add_user(self, user: User):
        self.users[user.user_id] = user
        await user.new_player()

        await self.log.write_log(log_data=f"Added user to database (ID={self.db_id}). USER ID: {user.user_id}, USERNAME: {user.username}")

    # Removes existing user object from dictionary.
    async def rem_user(self, user: User):
        del self.users[user.user_id]
        await user.del_player()

        await self.log.write_log(log_data=f"Removed user from database (ID={self.db_id}). USER ID: {user.user_id}, USERNAME: {user.username}")

    # Gets existing user object from dictionary by id, returns user.
    async def get_user_by_id(self, user_id: int) -> User:
        return self.users[user_id]

    # Checks if dictionary contains user by id, returns bool.
    async def contains_user(self, user_id: int) -> bool:
        if user_id in self.users.keys():
            return True
        else:
            return False
        
    # Saves all users data to json save file.
    async def save_data(self):
        if len(self.users) == 0: 
            with open(self.save_file, 'w') as save_data:
                save_data.truncate(0)
        try:
            with open(self.save_file, "w") as user_data:
                write_data = await self.encode_save_data()
                json.dump(write_data, user_data, indent = 4, sort_keys = True)

            await self.log.write_log(log_data=f'Saved user data to database. DATABASE ID: {self.db_id}, FILE: "{self.save_file}"')
        except Exception as exception:
            await self.log.write_log(log_data=f'Failed to save user data to database. DATABASE ID: {self.db_id}, FILE: "{self.save_file}"\nEXCEPTION: {str(exception)}\n')

    # Saves temporary user data to temporary save file. Used during runtime to save any changes to a user object. 
    async def save_temp_data(self, user: User, rem_user: bool = False): # TBD: Add automatic temp data save.
        try:
            with open(self.temp_file, "a") as user_data:
                if rem_user:
                    user_data.write("REMOVE USER:" + str(user.user_id) + "\n")
                else:  
                    write_data = await self.encode_temp_data(user=user)
                    user_data.write(write_data + "\n")
            await self.log.write_log(log_data=f'Saved temporary user data (USER={user.username}) to database. DATABASE ID: {self.db_id}, FILE: "{self.temp_file}"')
        except Exception as exception:
            await self.log.write_log(log_data=f'Failed to save temporary user data (USER={user.username}) to database. DATABASE ID: {self.db_id}, FILE: "{self.temp_file}"\nEXCEPTION: {str(exception)}\n')

        # if len(self.temp_data) > 500: await self.merge_data()

    # Loads all users from json save file.    
    async def load_data(self):
        try:
            if os.path.exists(path=self.save_file):
                with open(self.save_file, "r") as user_data:
                    read_data = json.load(user_data)
                    if read_data:
                        await self.decode_save_data(saved_data=read_data)
                        await self.log.write_log(log_data=f'Loaded user data from database. DATABASE ID: {self.db_id}, FILE: "{self.save_file}"')
                    else:
                        await self.log.write_log(log_data=f'No user data loaded from database, no data found. DATABASE ID: {self.db_id}, FILE: "{self.save_file}"')
            else:
                await self.log.write_log(log_data=f'Failed to load user data from database, no file found. DATABASE ID: {self.db_id}, FILE: "{self.save_file}"')
        except Exception as exception:
            await self.log.write_log(log_data=f'Failed to load user data from database. DATABASE ID: {self.db_id}, FILE: "{self.save_file}"\nEXCEPTION: {str(exception)}\n')

    # Loads temporary user data from temporary save file.
    async def load_temp_data(self):
        try:
            if os.path.exists(path=self.temp_file):
                with open(self.temp_file, "r") as temp_data:
                    read_data = temp_data.readlines()
                    if read_data:
                        await self.decode_temp_data(temp_data=read_data)
                        await self.log.write_log(log_data=f'Loaded temporary user data from database. DATABASE ID: {self.db_id}, FILE: "{self.temp_file}"')
                        await self.merge_data()
                    else:
                        await self.log.write_log(log_data=f'No temporary user data loaded from database, no data found. DATABASE ID: {self.db_id}, FILE: "{self.temp_file}"')
            else:
                await self.log.write_log(log_data=f'Failed to load temporary user data from database, no file found. DATABASE ID: {self.db_id}, FILE: "{self.temp_file}"')
        except Exception as exception:
            await self.log.write_log(log_data=f'Failed to load temporary user data from database. DATABASE ID: {self.db_id}, FILE: "{self.temp_file}"\nEXCEPTION: {str(exception)}\n')

    # Merges temporary user data to permanent user data, and clears temporary data.
    async def merge_data(self):
        # Merges temporary data to permanent data.
        for key, value in self.temp_data.items():
            if value == None:
                del self.users[key]
                continue
            self.users[key] = value

        # Clears temporary save file.
        with open(self.temp_file, 'w') as temp_data:
            temp_data.truncate(0)
        
        await self.log.write_log(log_data=f'Merged temporary user data to database, temporary data cleared. DATABASE ID: {self.db_id}, FILE: "{self.temp_file}"')

        # Creates new empty dictionary.
        self.temp_data = dict()

        # Saves changes to permanent store.
        await self.save_data()

    # Encodes user dictionary to a dictionary of strings to make it json writeable. Returns dictionary; KEY -> User ID, VALUE -> User data (string)
    async def encode_save_data(self):
        encoded_data: dict[int, str] = dict()

        for key, value in self.users.items():
            encoded_data[key] = await self.encoder(user=value)

        return encoded_data

    # Encodes user object to a string to make it json writeable. Returns string of user data.
    async def encode_temp_data(self, user: User) -> str:
        return await self.encoder(user=user)
    
    # Decodes saved data (string dictionary) to user dictionary.
    async def decode_save_data(self, saved_data: dict[str, str]):
        for key, value in saved_data.items():
            self.users[int(key)] = await self.decoder(data=value)
    
    # Decodes temporary data (string list) to temporary dictionary.
    async def decode_temp_data(self, temp_data: list[str]):
        for data in temp_data:
            if data.startswith("REMOVE USER:"):
                split_data = data.split(":")
                self.temp_data[int(split_data[1])] = None
                continue
            split_data = data.split(":")
            user_info = split_data[0].split(",")
            self.temp_data[int(user_info[0])] = await self.decoder(data=data)
    
    # Encodes user object data to a string. Returns string of user data.
    async def encoder(self, user: User) -> str:
        encoded_string = f"{user.user_id},{user.username}:"
        encoded_string += f"{user.player.name},{user.player.attack.get_xp()},{user.player.defense.get_xp()},{user.player.health.get_xp()},{user.player.lvl.get_xp()},{user.player.gold}:"
        encoded_string += f"{user.player.weapon.weapon_class.name},{user.player.weapon.attack.get_xp()},{user.player.armor.armor_class.name},{user.player.armor.defense.get_xp()}:"
        encoded_string += f"{user.player.inventory.slots}"

        for item in user.player.inventory.items:
            if isinstance(item, Weapon):
                encoded_string += f";Weapon,{item.weapon_class.name},{item.attack.get_xp()}"
            elif isinstance(item, Armor):
                encoded_string += f";Armor,{item.armor_class.name},{item.defense.get_xp()}"
            elif isinstance(item, Potion):
                encoded_string += f";Potion,{item.potion_type.name},{item.potion_quality}"
            elif isinstance(item, Kit):
                encoded_string += f";Kit,{item.kit_type.name},{item.kit_quality}"
            elif isinstance(item, Decorator):
                encoded_string += f";Decorator,{item.emoji},{item.tier}"

        if user.player.decorator != None:
            encoded_string +=f":{user.player.decorator.emoji},{user.player.decorator.tier}"

        return encoded_string 
    
    # Decodes string of user data to a user object. Returns user object.
    async def decoder(self, data: str) -> User:
        data = data.strip()
        data_split: list[str] = data.split(":")
        user_data: list[str] = data_split[0].split(",")
        player_data: list[str] = data_split[1].split(",")
        gear_data: list[str] = data_split[2].split(",")
        inv_data: list[str] = data_split[3].split(";")

        # Assigns user data.
        user = User()
        user.player = Player(player_data[0])
        user.user_id = int(user_data[0])
        user.username = user_data[1]

        # Assigns player data.
        user.player.attack.set_xp(value=int(player_data[1]))
        user.player.defense.set_xp(value=int(player_data[2]))
        user.player.health.set_xp(value=int(player_data[3]))
        user.player.lvl.set_xp(value=int(player_data[4]))
        user.player.gold = int(player_data[5])

        # Assigns player gear.
        user.player.weapon.weapon_class = GearType[gear_data[0]]
        user.player.weapon.attack.set_xp(value=int(gear_data[1]))
        user.player.armor.armor_class = GearType[gear_data[2]]
        user.player.armor.defense.set_xp(value=int(gear_data[3]))

        # Assigns player inventory.
        user.player.inventory.slots = int(inv_data[0])

        for i in range(1, len(inv_data), 1):
            data = inv_data[i].split(",")
            item: Item = None

            if data[0].startswith("Weapon"):
                item = Weapon()
                item.weapon_class = GearType[data[1]]
                item.attack.set_xp(int(data[2]))

                await item.set_name()
            elif data[0].startswith("Armor"):
                item = Armor()
                item.armor_class = GearType[data[1]]
                item.defense.set_xp(int(data[2]))

                await item.set_name()
            elif data[0].startswith("Potion"):
                item = Potion()
                item.potion_type = PotionType[data[1]]
                item.potion_quality = int(data[2])

                await item.set_name()
            elif data[0].startswith("Kit"):
                item = Kit()
                item.kit_type = KitType[data[1]]
                item.kit_quality = int(data[2])

                await item.set_name()
            elif data[0].startswith("Decorator"):
                item = Decorator()
                item.emoji = data[1]
                item.tier = int(data[2])

                await item.set_name()

            if item != None:
                await user.player.inventory.add_item(item=item)
            item = None

        # Assigns player decorator, if decorator exists.
        if len(data_split) > 4:
            decorator_data = data_split[4](",")

            user.player.decorator = Decorator()
            user.player.decorator.emoji = decorator_data[0]
            user.player.decorator.tier = int(decorator_data[1])

            await user.player.decorator.set_name()
        
        return user