# -*- coding: ISO-8859-15 -*-

from data.database import Database
from discord.message import Message
from game.objects.characters import MonsterClass
from game.interface.embeds import FightEmbed, InventoryEmbed
from game.interface.views import FightView, InventoryView, TradeView
from users.users import User

# Commands() object containing attributes and methods involved in further executing the command chain. 
# Instance instatiated at Bot.message_respond() and indirectly responds to an event "on_message()" (at main.py).
class Commands():
    def __init__(self, msg: Message, db_id: int):
        self.db: Database = Database.instances[db_id]   # Database instance for access to registered users.
        self.msg: Message = msg                         # discord message instance to respond to interactions.                         
        self.user: User = None                          # User instance representing the "owner/creator" of the instance. 
        self.user_inDb: bool = False                    # Boolean, true if user exists in database.

    # Sets self.user to current user of self.msg instance, runs from Bot.message_respond().
    # Returns user for checking interaction permisssion.
    async def set_user(self) -> User:
        if await self.db.contains_user(user_id = self.msg.author.id):
            self.user = await self.db.get_user_by_id(user_id = self.msg.author.id)
            self.user_inDb = True
        else:
            self.user = User()
            self.user.user_id = self.msg.author.id
            self.user.username = self.msg.author.name
            self.user_inDb = False

        return self.user

    # Command methods for further execution in interaction chain. 
    # NYI: Add admin commands!
    async def help(self):
        with open ('txt/commands.txt') as help:
            help = help.read()
        await self.msg.channel.send(content=help)

    async def about(self):
        with open ('txt/about.txt') as about:
            about = about.read()
        await self.msg.channel.send(content=about)

    async def new(self):
        if self.user_inDb:
            await self.msg.channel.send(content=f"**```arm\r\nMiHero !New\r\n```**`You already have a hero` **{self.user.player.get_name()}**.\n`To start fighting use command !Fight.`")
        else:
            await self.db.add_user(user=self.user)

            await self.msg.channel.send(content=f"**```arm\r\nMiHero !New\r\n```**`Created new hero` **{self.user.player.get_name()}**.\n`To start fighting use command !Fight.`")

    async def delete(self):
        if self.user_inDb:
            player_name = self.user.player.get_name()
            await self.db.rem_user(user = self.user)

            await self.msg.channel.send(content = f"**```arm\r\nMiHero !Delete\r\n```**`Your hero` **{player_name}** `was deleted`.\n`To create a new hero use command !New.`")
        else:
            await self.msg.channel.send(content = "**```arm\r\nMiHero !Delete\r\n```**`You haven't created a hero yet.`\n`To create a new hero use command !New.`")

    async def fight(self):
        if self.user_inDb:
            fight_view = FightView(user=self.user, db=self.db)
            msg = await self.msg.channel.send(content = "**```arm\r\nMiHero !Fight\r\n```**\n", view = fight_view)
            
            # Waits for view interaction to finish (by timing out or calling stop) to continue with response.
            await fight_view.wait()

            # If view interaction is fulfilled, success == True.
            if fight_view.success:
                self.user.permit_interaction = False # Sets interaction permission to false during fight simulation.
                if fight_view.select_type == "Player":
                    log = await self.user.player.fight_player(fight_view.receiver_user.player)

                elif fight_view.select_type.startswith("Monster"):
                    if fight_view.select_type == "MonsterLight":
                        log = await self.user.player.fight_monster(monster_class = MonsterClass.LIGHT)
                    elif fight_view.select_type == "MonsterMedium":
                        log = await self.user.player.fight_monster(monster_class = MonsterClass.MEDIUM)
                    elif fight_view.select_type == "MonsterHeavy":
                        log = await self.user.player.fight_monster(monster_class = MonsterClass.HEAVY)
                else:
                    # TBD: More options!
                    pass 

                # New FightEmbed() instance to run fight simulation in response to interaction.
                fight_embed = FightEmbed(msg = msg, log = log)
                await fight_embed.run_embed()
                fight_embed = None
                self.user.permit_interaction = True
            else:
                await msg.edit(content = "**```arm\r\nMiHero !Fight\r\n```**`Interaction timed out!`", view = None)

            fight_view = None
        else:
            await self.msg.channel.send(content = "**```arm\r\nMiHero !Fight\r\n```**`You haven't created a hero yet.`\n`To create a new hero use command !New.`")

    async def inventory(self):
        if self.user_inDb:
            embed_msg = await self.msg.channel.send(content=f"**```arm\r\n{self.user.player.name} !Inventory\r\n```**")

            inventory_embed = InventoryEmbed(msg=embed_msg, user=self.user)
            inventory_view = InventoryView(user=self.user)

            await inventory_embed.run_embed()
            view_msg = await self.msg.channel.send(view=inventory_view)

            # Waits for view interaction to finish (by timing out or calling stop) to continue with response.
            await inventory_view.wait()
            # Empty message to edit as a response to interaction.
            response_msg = await self.msg.channel.send(content="\u200b")

            run_inv = True
            while run_inv:
                if inventory_view.success and inventory_view.close_view == False:
                    if inventory_view.response != None:
                        await response_msg.edit(content=inventory_view.response)

                    inventory_view = None
                    inventory_view = InventoryView(user=self.user)

                    await inventory_embed.run_embed()
                    await view_msg.edit(view=inventory_view)
                elif inventory_view.success and inventory_view.close_view:
                    run_inv = False

                    await response_msg.delete()
                    await embed_msg.edit(content=f"**```arm\r\n{self.user.player.name} !Inventory\r\n```**", embed=None)      
                else:
                    run_inv = False

                    await response_msg.delete()
                    await embed_msg.edit(content=f"**```arm\r\n{self.user.player.name} !Inventory\r\n```**", embed=None)
                    await view_msg.edit(content=f"`Interaction timed out, inventory closed!`", view=None)
                
                await inventory_view.wait()
        else:
            await self.msg.channel.send(content="**```arm\r\nMiHero !Inventory\r\n```**`You haven't created a hero yet.`\n`To create a new hero use command !New.`")

    async def trade(self):
        if self.user_inDb:
            # trade_view = TradeView(user=self.user)
            # await self.msg.channel.send(view=trade_view)
            from game.interface.modals import TradeModal
            trade_modal = TradeModal()
            await self.msg.channel.send(view=trade_modal)
        else:
            pass

    async def shop(self):
        if self.user_inDb:
            pass
        else:
            pass

    async def stats(self):
        if self.user_inDb:
            log = await self.user.player.get_stats()
            await self.msg.channel.send(content=log)
        else:
            await self.msg.channel.send(content="**```arm\r\nMiHero !Stats\r\n```**`You haven't created a hero yet.`\n`To create a new hero use command !New.`")
    
    async def score(self):
        pass

    async def load(self):
        if self.msg.channel.guild.owner is not None and self.msg.author.top_role == self.msg.channel.guild.owner:
            await self.db.load_data()
        else:
            pass

    async def save(self):
        if self.msg.channel.guild.owner is not None and self.msg.author.top_role == self.msg.channel.guild.owner:
            await self.db.save_data()
        else:
            pass

    async def test(self):
        if self.user_inDb:
            # await self.user.player.inventory.add_slots(quantity=40)
            # log = await self.user.player.loot_generator(loot_index=3)

            # await self.msg.channel.send(content=log)
            pass
        else:   
            pass