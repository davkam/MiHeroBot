# -*- coding: ISO-8859-15 -*-

from discord.message import Message
from managers.info_manager import InfoManager
from managers.character_manager import CharacterManager
from users.userdata.userdata import UserData
from users.users import User

class Commands():
    def __init__(self, msg: Message, db_id: int):
        self.db: UserData = UserData.instances[db_id]
        self.msg: Message = msg                       
        self.user: User = None 
        self.existing_user: bool = False

    async def set_user(self) -> User:
        # Get user from database, returns None if no user is found
        user = await self.db.get_user(id=self.msg.author.id)
        if user:
            self.user = user
            self.existing_user = True
        else:
            self.user = User(
                id=self.msg.author.id,
                name=self.msg.author.name
            )
            self.existing_user = False

        return self.user

    # NYI: Add admin commands and bug report command!
    async def help(self):
        info_manager = InfoManager(cmd=self)
        await info_manager.help()

    async def about(self):
        info_manager = InfoManager(cmd=self)
        await info_manager.about()

    async def new(self):
        character_manager = CharacterManager(cmd=self)
        await character_manager.new_player_manager()
            
    async def delete(self):
        if self.existing_user:
            await self.user.del_player()
            await self.db.rem_user(user=self.user)

            await self.msg.channel.send(content = f"**```arm\r\nMiHero !Delete\r\n```**`Your hero` **{self.user.name.upper()}** `was deleted`.\n`To create a new hero use command !New.`", silent=True)
        else:
            await self.msg.channel.send(content = "**```arm\r\nMiHero !Delete\r\n```**`You haven't created a hero yet.`\n`To create a new hero use command !New.`", silent=True)

    async def fight(self):
        await self.msg.channel.send(content = f"**```arm\r\nMiHero !Fight\r\n```**`This function is not yet implemented!`", silent=True)

    async def roulette(self):
        await self.msg.channel.send(content = f"**```arm\r\nMiHero !Roulette\r\n```**`This function is not yet implemented!`", silent=True)

    async def inventory(self):
        await self.msg.channel.send(content = f"**```arm\r\nMiHero !Inventory\r\n```**`This function is not yet implemented!`", silent=True)

    async def trade(self):
        await self.msg.channel.send(content = f"**```arm\r\nMiHero !Trade\r\n```**`This function is not yet implemented!`", silent=True)

    async def shop(self):
        await self.msg.channel.send(content = f"**```arm\r\nMiHero !Shop\r\n```**`This function is not yet implemented!`", silent=True)

    async def stats(self):
        await self.msg.channel.send(content = f"**```arm\r\nMiHero !Stats\r\n```**`This function is not yet implemented!`", silent=True)

    async def leaderboard(self):
        await self.msg.channel.send(content = f"**```arm\r\nMiHero !Leaderboard\r\n```**`This function is not yet implemented!`", silent=True)

    async def bug(self):
        await self.msg.channel.send(content = f"**```arm\r\nMiHero !Bug\r\n```**`This function is not yet implemented!`", silent=True)