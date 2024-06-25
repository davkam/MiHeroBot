# -*- coding: ISO-8859-15 -*-

from discord.message import Message
from interaction.character_interaction import CharacterInteraction
from interaction.fight_interaction import FightInteraction
from interaction.info_interaction import InfoInteraction
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

    # NYI: Add admin commands!
    async def help(self):
        info_interaction = InfoInteraction(cmd=self)
        await info_interaction.help_interaction()

    async def about(self):
        info_interaction = InfoInteraction(cmd=self)
        await info_interaction.about_interaction()

    async def new(self):
        character_interaction = CharacterInteraction(cmd=self)
        await character_interaction.new_player_interaction()
            
    async def delete(self):
        character_interaction = CharacterInteraction(cmd=self)
        await character_interaction.del_player_interaction()

    async def fight(self):
        fight_interaction = FightInteraction(cmd=self)
        await fight_interaction.run_interaction()

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

        from game.objects.items.equipables import Sword, Shield, HeadArmor, BodyArmor, Amulet, Ring, EquipmentTier
        self.user.player.equipment.sword = Sword(tier=EquipmentTier.ADAMANT)
        self.user.player.equipment.shield = Shield(tier=EquipmentTier.ADAMANT)
        self.user.player.equipment.head = HeadArmor(tier=EquipmentTier.ADAMANT)
        self.user.player.equipment.body = BodyArmor(tier=EquipmentTier.ADAMANT)
        self.user.player.equipment.amulet = Amulet(tier=EquipmentTier.ADAMANT)
        self.user.player.equipment.ring = Ring(tier=EquipmentTier.ADAMANT)

        self.user.player.equipment.sword.level.set_lvl(lvl=100)
        self.user.player.equipment.shield.level.set_lvl(lvl=100)
        self.user.player.equipment.head.level.set_lvl(lvl=100)
        self.user.player.equipment.body.level.set_lvl(lvl=100)
        self.user.player.equipment.amulet.level.set_lvl(lvl=100)
        self.user.player.equipment.ring.level.set_lvl(lvl=100)

