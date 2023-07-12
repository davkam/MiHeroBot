#!/usr/bin/python
# -*- coding: ISO-8859-15 -*-

from bot.interface.interface import FightView
from data.database import Database
from discord.message import Message
from game.objects.characters import MonsterClass
from bot.interface.embeds import FightEmbed
from users.users import User
#import discord

# Commands(): Commands()-object containing attributes for discord.message.Message(), User() and a boolean.
#             Also contains setup()-command and all command methods for further execution (initiated at Bot.message_respond()).
class Commands():
    def __init__(self, msg: Message):
        self.db: Database = Database.instance
        self.msg: Message = msg                 # discord.message.Message()-instance.                          
        self.user: User = None                  # User()-instance.
        self.user_inDb: bool = False            # Boolean, true if user exists in database (db).

    # setup(): Sets self.user to current user of self.msg, runs from Bot.message_respond().
    async def set_user(self):
        if await self.db.contains_user(user_id = self.msg.author.id):
            self.user = await self.db.get_user(user_id = self.msg.author.id)
            self.user_inDb = True
        else:
            self.user = User()
            self.user.user_id = self.msg.author.id
            self.user.username = self.msg.author.name
            self.user_inDb = False

    # Command methods.
    async def help(self):
        with open ('txt/commands.txt') as help:
            help = help.read()
        await self.msg.channel.send(content = help)

    async def about(self):
        with open ('txt/about.txt') as about:
            about = about.read()
        await self.msg.channel.send(content = about)

    async def new(self):
        if self.user_inDb:
            await self.msg.channel.send(content = f"**```arm\r\nMiHero !New\r\n```**\n`You already have a hero` **{self.user.username.upper()}**\n`To start fighting use command !Fight.`")
        else:
            await self.db.add_user(user = self.user)
            await self.user.new_player()
            await self.msg.channel.send(content = f"**```arm\r\nMiHero !New\r\n```**\n`Created new hero` **{self.user.username.upper()}**\n`To start fighting use command !Fight.`")

    async def delete(self):
        if self.user_inDb:
            await self.db.rem_user(user = self.user)
            await self.user.del_player()
            await self.msg.channel.send(content = f"**```arm\r\nMiHero !Delete\r\n```**\n`Your hero was deleted` **{self.user.username.upper()}**\n`To create a new hero use command !New.`")
        else:
            await self.msg.channel.send(content = "**```arm\r\nMiHero !Delete\r\n```**\n`You haven't created a hero yet.`\n`To create a new hero use command !New.`")

    async def fight(self):
        if self.user_inDb:
            fight_view = FightView(user = self.user)
            msg = await self.msg.channel.send(content = "**```arm\r\nMiHero !Fight\r\n```**\n", view = fight_view)
            
            await fight_view.wait()

            if fight_view.success:
                if fight_view.select_type == "Player":
                    log = self.user.player.fight_player(fight_view.receiver_user.player)

                elif fight_view.select_type.startswith("Monster"):
                    if fight_view.select_type == "MonsterLight":
                        log = await self.user.player.fight_monster(monster_class = MonsterClass.Light)
                    elif fight_view.select_type == "MonsterMedium":
                        log = await self.user.player.fight_monster(monster_class = MonsterClass.Medium)
                    elif fight_view.select_type == "MonsterHeavy":
                        log = await self.user.player.fight_monster(monster_class = MonsterClass.Heavy)
                else:
                    pass
            else:
                await msg.edit(content = "**```arm\r\nMiHero !Fight\r\n```**\n`Interaction timed out!`", view = None)
            
            fight_embed = FightEmbed(msg = msg, log = log)
            await fight_embed.run_embed()

            # Removing object reference for garbage collection. (NOT REQUIRED!)
            fight_embed = None
            fight_view = None
        else:
            await self.msg.channel.send(content = "**```arm\r\nMiHero !Fight\r\n```**\n`You haven't created a hero yet.`\n`To create a new hero use command !New.`")

    async def inventory(self):
        if self.user_inDb:
            pass
        else:
            pass

    async def trade(self):
        if self.user_inDb:
            pass
        else:
            pass

    async def shop(self):
        if self.user_inDb:
            pass
        else:
            pass

    async def stats(self):
        if self.user_inDb:
            pass
        else:
            pass
    
    async def score(self):
        pass

    async def load(self):
        pass

    async def save(self):
        pass