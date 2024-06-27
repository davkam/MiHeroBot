import asyncio
import discord

from discord.message import Message
from game.logic.fight import Fight
from game.logic.rewards import Rewards
from game.objects.characters.characters import Character
from game.objects.characters.enemies import Monster, EnemyRank
from game.objects.characters.players import Player
from game.objects.items.items import Item
from interface.renderers.fight_renderer import FightRenderer
from interface.renderers.reward_renderer import RewardRenderer
from interface.views.fight_view import FightView

class FightInteraction():
    def __init__(self, cmd):
        from bot.commands.commands import Commands
        self.cmd: Commands = cmd
        self.top_msg: Message = None
        self.bot_msg: Message = None

    async def run_interaction(self):
        if not self.cmd.existing_user:
            await self.cmd.msg.channel.send(content="**```arm\r\nMiHero !Fight\r\n```**`You haven't created a hero yet.`\n`To create a new hero use command !New.`", silent=True)
            return
        
        self.cmd.user.permit = False # Set sender user interaction permission to false during fight

        fight_view = FightView(user=self.cmd.user, db=self.cmd.db)

        await self.cmd.msg.channel.send(content="**```arm\r\nMiHero !Fight\r\n```**\n", silent=True)
        self.top_msg = await self.cmd.msg.channel.send(view=fight_view, silent=True)
            
        # Wait for view interaction, return true if time-out or false if normal finish
        interaction_timeout = await fight_view.wait()

        self.bot_msg = await self.cmd.msg.channel.send(content = "\u200b", silent=True)

        if not interaction_timeout:
            if fight_view.select_type == "Player":
                fight_view.receiver_user.permit = False # Set receiver user interaction permission to false during fight

                await self.run_fight(fighter_a=self.cmd.user.player, fighter_b=fight_view.receiver_user.player)
                await self.cmd.db.update_user(user=fight_view.receiver_user)

                fight_view.receiver_user.permit = True

            elif fight_view.select_type.startswith("Monster"):
                if fight_view.select_type == "MonsterLight":
                    monster = Monster()
                    await monster.generate_monster(rank=EnemyRank.LIGHT, level=fight_view.sender_user.player.level)

                elif fight_view.select_type == "MonsterMedium":
                    monster = Monster()
                    await monster.generate_monster(rank=EnemyRank.MEDIUM, level=fight_view.sender_user.player.level)

                elif fight_view.select_type == "MonsterHeavy":
                    monster = Monster()
                    await monster.generate_monster(rank=EnemyRank.HEAVY, level=fight_view.sender_user.player.level)

                await self.run_fight(fighter_a=fight_view.sender_user.player, fighter_b=monster)

            else: # TBD: Boss option!
                pass

            await self.cmd.db.update_user(user=self.cmd.user) 
        else:
            await self.top_msg.edit(content="`Fight interaction timed out!`", view=None)

        self.cmd.user.permit = True

    async def run_fight(self, fighter_a: Player, fighter_b: Character) -> None:
        fight = Fight(fighter_a=fighter_a, fighter_b=fighter_b)
        fight_renderer = FightRenderer(fighter_one=fighter_a, fighter_two=fighter_b)

        await self.pre_fight(fight=fight, fight_renderer=fight_renderer)
        await self.main_fight(fight=fight, fight_renderer=fight_renderer)
        await self.post_fight(fight=fight)

        await fight_renderer.del_image_folder()

        fight = None
        fight_renderer = None

    async def pre_fight(self, fight: Fight, fight_renderer: FightRenderer) -> None:
        await fight.set_stats()
        await fight.set_turn()

        await fight_renderer.render_fight()
        await fight_renderer.render_stats()

        idle_image = await fight_renderer.get_fight_image(image_index=0, image_type="idle")
        stats_image = await fight_renderer.get_stats_image()

        idle_file = discord.File(fp=idle_image)
        stats_file = discord.File(fp=stats_image)

        await asyncio.sleep(delay=2)

        await self.top_msg.edit(content=None, attachments=[idle_file])
        await self.bot_msg.edit(attachments=[stats_file])

        for i in range(4):
            countdown_image = await fight_renderer.get_fight_image(image_index=0, image_type="countdown", image_info=str(3 - i))
            countdown_file = discord.File(fp=countdown_image)
            await self.top_msg.edit(attachments=[countdown_file])

            await asyncio.sleep(delay=1)
    
    async def main_fight(self, fight: Fight, fight_renderer: FightRenderer) -> None:
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

            await self.top_msg.edit(attachments=[fight_file])
            await self.bot_msg.edit(attachments=[stats_file])

            await asyncio.sleep(delay=1)

            if fight.fighter_a.hp < 0 or fight.fighter_b.hp < 0:
                break

            idle_image = await fight_renderer.get_fight_image(image_index=0, image_type="idle")
            idle_file = discord.File(fp=idle_image)

            await self.top_msg.edit(attachments=[idle_file])

            await asyncio.sleep(delay=1)

        if fight.fighter_a.hp > 0:
            fight_image = await fight_renderer.get_fight_image(image_index=5, image_type="winner", image_info="left")
        else:
            fight_image = await fight_renderer.get_fight_image(image_index=6, image_type="winner", image_info="right")

        fight_file = discord.File(fp=fight_image)

        await self.top_msg.edit(attachments=[fight_file])

    async def post_fight(self, fight: Fight):
        winner: Character = None
        loser: Character = None

        if fight.fighter_a.hp > 0:
            winner = fight.fighter_a.character
            loser = fight.fighter_b.character
        else:
            winner = fight.fighter_b.character
            loser = fight.fighter_a.character

        rewards = Rewards(winner=winner, loser=loser)
        reward_renderer = RewardRenderer(winner=winner, loser=loser)

        xp_gain: list[int] = list()
        loot_gain: list[Item] = list()
        gold_lost = int()

        if isinstance(fight.fighter_b.character, Monster):
            xp_gain, loot_gain, gold_lost = await rewards.pvm_rewards()
        else:
            await rewards.pvp_rewards()

        await asyncio.sleep(delay=1)

        if xp_gain:
            await reward_renderer.render_reward()
            xp_gain_image = await reward_renderer.get_xp_reward_image()
            xp_gain_file = discord.File(fp=xp_gain_image)

            await self.bot_msg.edit(attachments=[xp_gain_file])

            await asyncio.sleep(delay=0.5)

            for i in range(4):
                if i != 3:
                    xp_gain_image = await reward_renderer.get_xp_reward_image(image_type=i, image_info=xp_gain[i])
                else:
                    xp_gain_image = await reward_renderer.get_xp_reward_image(image_type=i)
                
                xp_gain_file = discord.File(fp=xp_gain_image)

                await self.bot_msg.edit(attachments=[xp_gain_file])
                await asyncio.sleep(delay=0.5)

        if loot_gain:
            pass

        if gold_lost > 0:
            pass