import asyncio
import discord

from discord.message import Message
from game.logic.fight import Fight
from game.objects.characters.characters import Character
from game.objects.characters.enemies import Monster, EnemyRank
from game.objects.characters.players import Player
from interface.renderers.fight_renderer import FightRenderer
from interface.views.fight_view import FightView

class FightInteraction():
    def __init__(self, cmd):
        from bot.commands.commands import Commands
        self.cmd: Commands = cmd

    async def run_interaction(self):
        if not self.cmd.existing_user:
            await self.cmd.msg.channel.send(content="**```arm\r\nMiHero !Fight\r\n```**`You haven't created a hero yet.`\n`To create a new hero use command !New.`", silent=True)
            return
        
        fight_view = FightView(user=self.cmd.user, db=self.cmd.db)
        await self.cmd.msg.channel.send(content="**```arm\r\nMiHero !Fight\r\n```**\n", silent=True)
        edit_msg = await self.cmd.msg.channel.send(view=fight_view, silent=True)
            
        # Wait for view interaction, return true if time-out or false if normal finish
        interaction_timeout = await fight_view.wait()

        if not interaction_timeout:
            self.cmd.user.permit = False # Set sender user interaction permission to false during fight

            if fight_view.select_type == "Player":
                fight_view.receiver_user.permit = False # Set receiver user interaction permission to false during fight

                await asyncio.sleep(delay=2)
                await edit_msg.delete()
                await self.run_fight(fighter_a=self.cmd.user.player, fighter_b=fight_view.receiver_user.player)

                fight_view.receiver_user.permit = True

            elif fight_view.select_type.startswith("Monster"):
                if fight_view.select_type == "MonsterLight":
                    monster = Monster()
                    await monster.generate_monster(rank=EnemyRank.LIGHT, level=fight_view.sender_user.player.level)

                    await asyncio.sleep(delay=2)
                    await edit_msg.delete()
                    await self.run_fight(fighter_a=fight_view.sender_user.player, fighter_b=monster)
                elif fight_view.select_type == "MonsterMedium":
                    monster = Monster()
                    await monster.generate_monster(rank=EnemyRank.MEDIUM, level=fight_view.sender_user.player.level)

                    await asyncio.sleep(delay=2)
                    await edit_msg.delete()
                    await self.run_fight(fighter_a=fight_view.sender_user.player, fighter_b=monster)

                elif fight_view.select_type == "MonsterHeavy":
                    monster = Monster()
                    await monster.generate_monster(rank=EnemyRank.HEAVY, level=fight_view.sender_user.player.level)

                    await asyncio.sleep(delay=2)
                    await edit_msg.delete()
                    await self.run_fight(fighter_a=fight_view.sender_user.player, fighter_b=monster)

            else: # TBD: Boss option!
                pass 

            self.cmd.user.permit = True
        else:
            await edit_msg.edit(content="`Fight interaction timed out!`", view=None)

        # NYI: Save users!

    async def run_fight(self, fighter_a: Player, fighter_b: Character) -> None:
        fight = Fight(fighter_a=fighter_a, fighter_b=fighter_b)
        fight_renderer = FightRenderer(fighter_one=fighter_a, fighter_two=fighter_b)

        top_msg, bot_msg = await self.pre_fight(fight=fight, fight_renderer=fight_renderer)
        await self.main_fight(fight=fight, fight_renderer=fight_renderer, top_msg=top_msg, bot_msg=bot_msg)

        await fight_renderer.del_images()

    async def pre_fight(self, fight: Fight, fight_renderer: FightRenderer) -> tuple[Message, Message]:
        await fight.set_stats()
        await fight.set_turn()

        await fight_renderer.render_fight()
        await fight_renderer.render_stats()

        idle_image = await fight_renderer.get_fight_image(image_index=0, image_type="idle")
        stats_image = await fight_renderer.get_stats_image()

        idle_file = discord.File(fp=idle_image)
        stats_file = discord.File(fp=stats_image)

        top_msg = await self.cmd.msg.channel.send(file=idle_file, silent=True)
        bot_msg = await self.cmd.msg.channel.send(file=stats_file, silent=True)

        stats_file = discord.File(fp=stats_image)
        await bot_msg.edit(attachments=[stats_file])  

        for i in range(4):
            countdown_image = await fight_renderer.get_fight_image(image_index=0, image_type="countdown", image_info=str(3 - i))
            countdown_file = discord.File(fp=countdown_image)
            await top_msg.edit(attachments=[countdown_file])

            await asyncio.sleep(delay=1)

        return top_msg, bot_msg
    
    async def main_fight(self, fight: Fight, fight_renderer: FightRenderer, top_msg: Message, bot_msg: Message) -> None:
        while True:
            if fight.turn == True: # Fighter A
                is_hit, hit_dmg = await fight.roll_fight()

                if is_hit:
                    fight_image = await fight_renderer.get_fight_image(image_index=1, image_info=str(hit_dmg), image_variant=is_hit)
                else:
                    fight_image = await fight_renderer.get_fight_image(image_index=2, image_info=str(hit_dmg), image_variant=is_hit)
            else:
                is_hit, hit_dmg = await fight.roll_fight()

                if is_hit:
                    fight_image = await fight_renderer.get_fight_image(image_index=3, image_info=str(hit_dmg), image_variant=is_hit)
                else:
                    fight_image = await fight_renderer.get_fight_image(image_index=4, image_info=str(hit_dmg), image_variant=is_hit)

            stats_image = await fight_renderer.get_stats_image(health_left_a=fight.fighter_a.hp, health_left_b=fight.fighter_b.hp)

            fight_file = discord.File(fp=fight_image)
            stats_file = discord.File(fp=stats_image)

            await top_msg.edit(attachments=[fight_file])
            await bot_msg.edit(attachments=[stats_file])

            await asyncio.sleep(delay=1)

            if fight.fighter_a.hp < 0 or fight.fighter_b.hp < 0:
                break

            idle_image = await fight_renderer.get_fight_image(image_index=0, image_type="idle")
            idle_file = discord.File(fp=idle_image)

            await top_msg.edit(attachments=[idle_file])

            await asyncio.sleep(delay=1)

        if fight.fighter_a.hp > 0:
            fight_image = await fight_renderer.get_fight_image(image_index=5, image_type="winner", image_info="left")
        else:
            fight_image = await fight_renderer.get_fight_image(image_index=6, image_type="winner", image_info="right")

        fight_file = discord.File(fp=fight_image)

        await top_msg.edit(attachments=[fight_file])