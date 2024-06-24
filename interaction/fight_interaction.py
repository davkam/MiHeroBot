import asyncio
import discord

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
                    pass
                elif fight_view.select_type == "MonsterMedium":
                    pass
                elif fight_view.select_type == "MonsterHeavy":
                    pass
            else: # TBD: Boss option!
                pass 

            self.cmd.user.permit = True
        else:
            await edit_msg.edit(content="`Fight interaction timed out!`", view=None)

        # NYI: Save users!

    async def run_fight(self, fighter_a: Player, fighter_b: Character) -> None:
        fight = Fight(fighter_a=fighter_a, fighter_b=fighter_b)
        await fight.set_stats()
        await fight.set_turn()

        fight_renderer = FightRenderer(fighter_one=fighter_a, fighter_two=fighter_b)
        await fight_renderer.render_fight()
        await fight_renderer.render_stats()

        idle_image = await fight_renderer.get_fight_images(image=0, image_info="idle")
        fight_image = await fight_renderer.get_fight_images(image=0, image_info="countdown")
        stats_image = await fight_renderer.get_stats_image()

        idle_file = discord.File(fp=idle_image[0])
        fight_file = discord.File(fp=fight_image[0])
        stats_file = discord.File(fp=stats_image)

        fight_msg = await self.cmd.msg.channel.send(file=idle_file, silent=True)
        stats_msg = await self.cmd.msg.channel.send(file=stats_file, silent=True)

        stats_file = discord.File(fp=stats_image)
        await stats_msg.edit(attachments=[stats_file])  

        for image in fight_image:
            fight_file = discord.File(fp=image)
            await fight_msg.edit(attachments=[fight_file])

            await asyncio.sleep(delay=1)

        while fight.fighter_a.hp > 0 and fight.fighter_b.hp > 0:
            hit, dmg = await fight.fight_turn()

            if fight.turn == False: # Fighter A
                if hit:
                    fight_image = await fight_renderer.get_fight_images(image=1, image_info=str(dmg), image_variant=hit)
                else:
                    fight_image = await fight_renderer.get_fight_images(image=2, image_info=str(dmg), image_variant=hit)
            else:
                if hit:
                    fight_image = await fight_renderer.get_fight_images(image=3, image_info=str(dmg), image_variant=hit)
                else:
                    fight_image = await fight_renderer.get_fight_images(image=4, image_info=str(dmg), image_variant=hit)

            stats_image = await fight_renderer.get_stats_image(remaining_left_health=fight.fighter_a.hp, remaining_right_heath=fight.fighter_b.hp)

            fight_file = discord.File(fp=fight_image[0])
            stats_file = discord.File(fp=stats_image)

            await fight_msg.edit(attachments=[fight_file])
            await stats_msg.edit(attachments=[stats_file])

            await asyncio.sleep(delay=1)

            if fight.fighter_a.hp < 0 or fight.fighter_b.hp < 0:
                break

            idle_file = discord.File(fp=idle_image[0])
            await fight_msg.edit(attachments=[idle_file])

            await asyncio.sleep(delay=1)

        if fight.fighter_a.hp > 0:
            winner = fighter_a
            loser = fighter_b

            fight_image = await fight_renderer.get_fight_images(image=5, image_info="winnerleft")
        else:
            winner = fighter_b
            loser = fighter_a

            fight_image = await fight_renderer.get_fight_images(image=6, image_info="winnerright")

        fight_file = discord.File(fp=fight_image[0])
        await fight_msg.edit(attachments=[fight_file])

        await fight_renderer.del_images()