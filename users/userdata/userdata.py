import logging
import os
import pickle

from database.sql_db import SQLDatabase
from loggers.loggers import Loggers
from typing import Optional
from users.users import User

DATA_DIR = "users/userdata/data"

class UserData:
    """
    Manages user data for a specific guild.
    """
    instances: dict[int, 'UserData'] = {}  # Dictionary of guild unique instances, uses guild id as key

    __slots__ = ['id', 'file', 'sql', 'users', 'logger']

    def __init__(self, id: int):
        """
        Initializes a UserData instance for a specific guild.
        """
        self.id: int = id
        self.file: str = f"{DATA_DIR}/db_{id}.db"
        self.sql: SQLDatabase = SQLDatabase(path=self.file)  # SQL database, handles queries to permanent database
        self.users: dict[int, User] = {} # Dictionary of users, uses user id as key
        self.logger: logging.Logger = Loggers.data

    async def add_user(self, user: User) -> None:
        """
        Adds a user to the database and saves the user data.
        """
        self.users[user.id] = user
        await self.save_user(user=user)

        self.logger.info(f"Added user to database (DATABASE ID: {self.id}). USERNAME: {user.name} (USER ID: {user.id})")

    async def rem_user(self, user: User) -> None:
        """
        Removes a user from the database.
        """
        if user.id in self.users:
            del self.users[user.id]
            await self.del_user(user=user)

            self.logger.info(f"Removed user from database (DATABASE ID: {self.id}). USERNAME: {user.name} (USER ID: {user.id})")
        else:
            self.logger.warning(f"Attempted to remove non-existent user (USER ID: {user.id}) from database (DATABASE ID: {self.id})")

    async def get_user(self, id: int) -> Optional[User]:
        """
        Retrieves a user from the database by ID.
        """
        return self.users.get(id)

    async def save_user(self, user: User) -> None:
        """
        Saves a user's data to the database.
        """
        player = pickle.dumps(obj=user.player)  # Serialize player object
        await self.sql.execute("INSERT OR REPLACE INTO Users (id, username, player) VALUES (?, ?, ?)", user.id, user.name, player)

    async def load_users(self) -> None:
        """
        Loads all users from the database.
        """
        all_users = await self.sql.execute("SELECT * FROM Users")
        try:
            for user in all_users:
                new_user = User()
                new_user.id = user[0]
                new_user.name = user[1]
                new_user.player = pickle.loads(user[2])  # Deserialize player object
                self.users[new_user.id] = new_user
            self.logger.info(f"Loaded users from guild database. ID: {self.id}")
        except Exception as exception:
            self.logger.error(f"Failed to load users from guild database. ID: {self.id} EXCEPTION: {str(exception)}")

    async def update_user(self, user: User) -> None:
        """
        Updates a user's data in the database.
        """
        player = pickle.dumps(obj=user.player)
        await self.sql.execute("UPDATE Users SET player = ? WHERE id = ?", player, user.id)

    async def del_user(self, user: User) -> None:
        """
        Deletes a user from the database.
        """
        await self.sql.execute("DELETE FROM Users WHERE id = ?", user.id)

    async def create_database(self) -> None:
        """
        Creates the user database if it does not exist.
        """
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            self.logger.warning(f"No directory found '{DATA_DIR}', new directory created!")
        try:
            await self.sql.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    player BLOB
                )
            """)
            self.logger.info(f"Created new guild database. ID: {self.id}")
        except Exception as exception:
            self.logger.error(f"Failed to create new guild database. ID: {self.id} EXCEPTION: {str(exception)}")

    @classmethod
    async def new_database(cls, id: int) -> None:
        """
        Creates a new UserData instance for a guild and loads or creates the database.
        """
        cls.instances[id] = UserData(id=id)
        db: UserData = cls.instances[id]

        # If database exists, load users from existing database. If not, set new database
        if os.path.exists(db.file):
            await db.load_users()
        else:
            await db.create_database()