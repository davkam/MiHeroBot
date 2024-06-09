import logging
import os
import pickle

from database.sql_db import SQLDatabase
from loggers.loggers import Loggers
from users.users import User

class UserData():
    instances: dict = dict() # Dictionary of guild unique instances, uses guild id as key 

    def __init__(self, id: int):
        self.id: int = id
        self.file: str = f"users/userdata/data/db_{id}.db"
        self.sql: SQLDatabase = SQLDatabase(path=self.file) # SQL database, handles queries to permanent database
        self.users: dict[int, User] = dict()
        self.logger: logging.Logger = Loggers.data

    async def add_user(self, user: User):
        self.users[user.id] = user
        await self.save_user(user=user)

        self.logger.info(msg=f"Added user to database (DATABASE ID: {self.id}). USERNAME: {user.name} (USER ID: {user.id})")

    async def rem_user(self, user: User):
        del self.users[user.id]
        await self.del_user(user=user)

        self.logger.info(msg=f"Removed user from database (DATABASE ID: {self.id}). USERNAME: {user.name} (USER ID: {user.id})")

    async def get_user(self, id: int) -> User:
        if id in self.users.keys():
            return self.users[id]
        else:
            return None
        
    async def save_user(self, user: User):
        player = pickle.dumps(obj=user.player) # Serialize player object

        await self.sql.execute("INSERT INTO Users (id, username, player) VALUES (?, ?, ?)", user.id, user.name, player)

    async def load_users(self):
        all_users = await self.sql.execute("SELECT * FROM Users")

        try:
            for user in all_users:
                new_user = User()
                new_user.id = user[0]
                new_user.name = user[1]
                new_user.player = pickle.loads(user[2]) # Deserialize player object
                self.users[new_user.id] = new_user

            self.logger.info(msg=f"Loaded users from guild database. ID: {self.id}")
        except Exception as exception:
            self.logger.error(msg=f"Failed to load users from guild database. ID: {self.id} EXCEPTION: {str(exception)[10:]}")

    async def update_user(self, user: User):
        player = pickle.dumps(obj=user.player)

        await self.sql.execute("UPDATE Users SET player = ? WHERE id = ?", player, user.id)

    async def del_user(self, user: User):
        await self.sql.execute("DELETE FROM Users WHERE id = ?", user.id)
        
    async def create_database(self):
        if not os.path.exists(path="users/userdata/data"):
            os.makedirs(name="users/userdata/data")

            self.logger.warning(msg=f"No directory found 'users/userdata/data', new directory created!")
        try:
            await self.sql.execute("""CREATE TABLE IF NOT EXISTS Users (
                                id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL,
                                player BLOB
            )""")

            self.logger.info(msg=f"Created new guild database. ID: {self.id}")
        except Exception as exception:
            self.logger.error(msg=f"Failed to create new guild database. ID: {self.id} EXCEPTION: {str(exception)}")

    @classmethod
    async def new_database(cls, id: int):
        cls.instances[id] = UserData(id=id)
        db: UserData = cls.instances[id]

        # If database exists, load users from existing database. If not, set new database
        if os.path.exists(path=db.file):
            await db.load_users()
        else:
            await db.create_database()