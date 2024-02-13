# -*- coding: ISO-8859-15 -*-

import asyncio
from data.database import Database
from discord.message import Message
from game.logic.trade import Trade
from game.objects.characters import MonsterClass
from interface.embeds.fight_embed import FightEmbed
from interface.embeds.inventory_embed import InventoryEmbed
from interface.views.fight_view import FightView
from interface.views.inventory_view import InventoryView
from interface.views.trade_view import TradeView
from users.users import User

import discord

class Commands():
    def __init__(self, msg: Message, db_id: int):
        self.db: Database = Database.instances[db_id]
        self.msg: Message = msg                       
        self.user: User = None 
        self.user_inDb: bool = False

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

    # NYI: Add admin commands!
    async def help(self):
        with open ('txt/commands.txt') as help:
            help = help.read()
        await self.msg.channel.send(content=help, silent=True)

    async def about(self):
        with open ('txt/about.txt') as about:
            about = about.read()
        await self.msg.channel.send(content=about, silent=True)

    async def new(self):
        if self.user_inDb:
            await self.msg.channel.send(content=f"**```arm\r\nMiHero !New\r\n```**`You already have a hero` **{self.user.player.get_name()}**.\n`To start fighting use command !Fight.`", silent=True)
        else:
            await self.db.add_user(user=self.user)
            await self.db.save_temp_data(user=self.user)

            await self.msg.channel.send(content=f"**```arm\r\nMiHero !New\r\n```**`Created new hero` **{self.user.player.get_name()}**.\n`To start fighting use command !Fight.`", silent=True)

    async def delete(self):
        if self.user_inDb:
            player_name = self.user.player.get_name()
            await self.db.rem_user(user = self.user)
            await self.db.save_temp_data(user=self.user, rem_user=True)

            await self.msg.channel.send(content = f"**```arm\r\nMiHero !Delete\r\n```**`Your hero` **{player_name}** `was deleted`.\n`To create a new hero use command !New.`", silent=True)
        else:
            await self.msg.channel.send(content = "**```arm\r\nMiHero !Delete\r\n```**`You haven't created a hero yet.`\n`To create a new hero use command !New.`", silent=True)

    async def fight(self):
        if self.user_inDb:
            fight_view = FightView(user=self.user, db=self.db)
            msg = await self.msg.channel.send(content = "**```arm\r\nMiHero !Fight\r\n```**\n", view = fight_view, silent=True)
            
            # Wait for view interaction to finish (by timing out or calling stop) to continue with response.
            await fight_view.wait()

            # If view interaction is successful.
            if fight_view.success:
                self.user.permit_interaction = False # Set interaction permission to false during fight simulation.
                if fight_view.select_type == "Player":
                    log = await self.user.player.fight_player(fight_view.receiver_user.player)

                elif fight_view.select_type.startswith("Monster"):
                    if fight_view.select_type == "MonsterLight":
                        log = await self.user.player.fight_monster(monster_class = MonsterClass.LIGHT)
                    elif fight_view.select_type == "MonsterMedium":
                        log = await self.user.player.fight_monster(monster_class = MonsterClass.MEDIUM)
                    elif fight_view.select_type == "MonsterHeavy":
                        log = await self.user.player.fight_monster(monster_class = MonsterClass.HEAVY)
                else: # TBD: More options!
                    pass 

                # New fight embed to run fight simulation in response to interaction.
                fight_embed = FightEmbed(msg = msg, log = log)
                await fight_embed.run_embed()
                fight_embed = None
                self.user.permit_interaction = True
            else:
                await msg.edit(content = "**```arm\r\nMiHero !Fight\r\n```**`Interaction timed out!`", view = None)

            await self.db.save_temp_data(user=self.user)
            fight_view = None
        else:
            await self.msg.channel.send(content = "**```arm\r\nMiHero !Fight\r\n```**`You haven't created a hero yet.`\n`To create a new hero use command !New.`", silent=True)

    async def stake(self):
        pass

    async def inventory(self):
        if self.user_inDb:
            embed_msg = await self.msg.channel.send(content=f"**```arm\r\n{self.user.player.name} !Inventory\r\n```**", silent=True)

            inventory_embed = InventoryEmbed(msg=embed_msg, user=self.user)
            inventory_view = InventoryView(user=self.user)

            await inventory_embed.run_embed()
            view_msg = await self.msg.channel.send(view=inventory_view, silent=True)

            # Wait for view interaction to finish (by timing out or calling stop) to continue with response.
            await inventory_view.wait()

            # Empty message to edit as a response to interaction.
            response_msg = await self.msg.channel.send(content="\u200b", silent=True)

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
            
            await self.db.save_temp_data(user=self.user)
        else:
            await self.msg.channel.send(content="**```arm\r\nMiHero !Inventory\r\n```**`You haven't created a hero yet.`\n`To create a new hero use command !New.`", silent=True)

    async def trade(self):
        if self.user_inDb:
            await self.msg.channel.send(content=f"**```arm\r\nMiHero !Trade\r\n```**", silent=True)

            trade = Trade(msg=self.msg, db=self.db, sender_trader=self.user)
            await trade.run_trade()
        else:
            await self.msg.channel.send(content="**```arm\r\nMiHero !Trade\r\n```**`You haven't created a hero yet.`\n`To create a new hero use command !New.`", silent=True)

    async def shop(self):
        if self.user_inDb:
            await self.msg.channel.send(content=f"**```arm\r\nMiHero !Shop\r\n```**", silent=True)

            await self.msg.channel.send(content="`This feature isn't available yet.`")
        else:
            await self.msg.channel.send(content="**```arm\r\nMiHero !Trade\r\n```**`You haven't created a hero yet.`\n`To create a new hero use command !New.`", silent=True)

    async def stats(self):
        if self.user_inDb:
            log = await self.user.player.get_stats()
            await self.msg.channel.send(content=log, silent=True)
        else:
            await self.msg.channel.send(content="**```arm\r\nMiHero !Stats\r\n```**`You haven't created a hero yet.`\n`To create a new hero use command !New.`", silent=True)
    
    async def board(self):
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
            from bot.client import uploaded_image_urls
            ### EMBED - URL IMAGES TEST ###
            # image_links = [
            #     "https://cdn.iconscout.com/icon/free/png-256/free-notion-2296040-1911999.png?f=webp",
            #     "https://icons.iconarchive.com/icons/paomedia/small-n-flat/256/sign-check-icon.png",
            #     "https://static-00.iconduck.com/assets.00/website-icon-256x256-80g4o143.png",
            #     "https://i.pinimg.com/474x/a8/ff/45/a8ff459c578816b95ac2ea8b576da4ef.jpg",
            #     "https://ps.w.org/new-social-media-widget/assets/icon-256x256.png?rev=2142539",
            #     "https://www.iconsdb.com/icons/preview/red/warning-xxl.png"
            # ]

            # embed = discord.Embed(title="[INSERT TITLE]")

            # msg = await self.msg.channel.send(embed=embed)

            # for image in image_links:
            #     embed.set_image(url=image)
            #     await msg.edit(embed=embed)
            #     await asyncio.sleep(0.1)

            # embed = discord.Embed(title="[INSERT TITLE]")
            # await msg.edit(embed=embed)
            
            # for image in image_links:
            #     embed.set_image(url=image)
            #     await msg.edit(embed=embed)
            #     await asyncio.sleep(1)



            ### EMBED - LOCAL IMAGES TEST ###
            image_files = [
                "images/pvm/pvm_idle.png",
                "images/pvm/pvm_hitA.png",
                "images/pvm/pvm_idle.png",
                "images/pvm/pvm_hitB.png",
                "images/pvm/pvm_idle.png",
                "images/pvm/pvm_hitA.png",
                "images/pvm/pvm_idle.png",
                "images/pvm/pvm_hitB.png",
                "images/pvm/pvm_idle.png",
                "images/pvm/pvm_hitA.png",
                "images/pvm/pvm_idle.png",
                "images/pvm/pvm_hitB.png",
                "images/pvm/pvm_idle.png",
                "images/pvm/pvm_deadA.png",
                "images/pvm/pvm_idle.png",
                "images/pvm/pvm_deadB.png",
                "images/pvm/pvm_idle.png",
            ]

            uploaded_image_urls = []

            

            for file in image_files:
                with open(file, 'rb') as f:
                    uploaded_image = await self.client.get_channel(1044019028009689158).send(file=discord.File(f))
                    uploaded_image_urls.append(uploaded_image.attachments[0].url)

            # images = [discord.File(fp=file, filename=file.split('/')[-1]) for file in image_files]

            embed = discord.Embed()
            embed.add_field(name=f"PLAYER A", value=f"`LVL: 10`\n`ATT: 10`\n`\U0001F6E1\uFE0F DEF: 10`\n`HP: 100`", inline=True)
            embed.add_field(name="`|||||| STATUS ||||||`", value=f"`- PREPARING FIGHT  -`\n`- DECIDING TURN... -`", inline=True)
            embed.add_field(name=f"PLAYER B", value=f"`LVL: 10`\n`ATT: 10`\n`\U0001F6E1\uFE0F DEF: 10`\n`HP: 100`", inline=True)
            embed.add_field(name="IIIIIIIIIIIIIIIIIIII`100%`", value=f"`00`\n`00`", inline=True)
            embed.add_field(name="", value="", inline=True)
            embed.add_field(name="IIIIIIIIIIIIIIIIIIII`100%`", value=f"`00`\n`00`", inline=True)
            embed.set_image(url=uploaded_image_urls[0])

            # embed.set_image(url=f"attachment://{images[0].filename}")
            # msg = await self.msg.channel.send(embed=embed, file=images[0])

            embed_msg = await self.msg.channel.send(embed=embed, silent=True)
            # file_msg = await self.msg.channel.send(file=images[0], silent=True)

            # for image in images[1:]:
            #     await file_msg.edit(attachments=[image])
            #     await asyncio.sleep(1)

            for image in uploaded_image_urls[1:]:
                embed.set_image(url=image)
                await embed_msg.edit(embed=embed)
                await asyncio.sleep(1)


            ### STAT BOOSTER TEST ###
            # await self.user.player.inventory.add_slots(quantity=40)

            # log = await self.user.player.loot_generator(loot_index=1)
            # await self.msg.channel.send(content=log, silent=True)

            # log = await self.user.player.xp_gainer(xp_index=1)
            # await self.msg.channel.send(content=log, silent=True)

            # log = await self.user.player.loot_generator(loot_index=2)
            # await self.msg.channel.send(content=log, silent=True)

            # log = await self.user.player.xp_gainer(xp_index=2)
            # await self.msg.channel.send(content=log, silent=True)

            # log = await self.user.player.loot_generator(loot_index=3)
            # await self.msg.channel.send(content=log, silent=True)

            # log = await self.user.player.xp_gainer(xp_index=3)
            # await self.msg.channel.send(content=log, silent=True)
        else:   
            pass