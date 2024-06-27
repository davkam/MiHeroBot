import discord

from game.objects.characters.players import PlayerColor
from handlers.temp_img_handler import TempImageHandler
from interface.renderers.stats_renderer import StatsRenderer
from interface.views.del_player_view import DelPlayerView
from interface.views.new_player_view import NewPlayerView

class CharacterInteraction():
    NEW_PLAYER_PATH = "game/assets/menus/new_%s.gif"

    def __init__(self, cmd):
        from bot.commands.commands import Commands
        self.cmd: Commands = cmd

    async def new_player_interaction(self):
        if self.cmd.existing_user:
            await self.cmd.msg.channel.send(content=f"**```arm\r\nMiHero !New @{self.cmd.user.name}\r\n```**`You already have a hero.`\n`To start fighting use command !Fight.`", silent=True)
            return
        
        self.cmd.user.permit = False # Set sender user interaction permission to false during fight

        new_player_file = discord.File(fp=CharacterInteraction.NEW_PLAYER_PATH % "1")
        new_player_view = NewPlayerView(user=self.cmd.user)

        await self.cmd.msg.channel.send(content=f"**```arm\r\nMiHero !New @{self.cmd.user.name}\r\n```** ", silent=True)
        edit_msg = await self.cmd.msg.channel.send(file=new_player_file, view=new_player_view)

        while not await new_player_view.wait():
            if new_player_view.selected or new_player_view.canceled:
                break

            new_player_file = discord.File(fp=CharacterInteraction.NEW_PLAYER_PATH % f"{new_player_view.character}")
            new_player_view = NewPlayerView(user=self.cmd.user, character=new_player_view.character)

            await edit_msg.edit(attachments=[new_player_file], view=new_player_view)

        if new_player_view.selected:
            await self.cmd.user.new_player(color=PlayerColor(new_player_view.character))
            await self.cmd.db.add_user(user=self.cmd.user)

            renderer = StatsRenderer(user=self.cmd.user)
            await renderer.render_stats()
            player_stats_path = await renderer.get_stats_image()
            
            new_player_file = discord.File(fp=player_stats_path)

            await edit_msg.delete()
            await self.cmd.msg.channel.send(file=new_player_file, silent=True)
            await self.cmd.msg.channel.send(content="`Created new hero! To start fighting use command !Fight.`", silent=True)

            await renderer.del_image_folder()
        elif new_player_view.canceled:
            await edit_msg.delete()
            await self.cmd.msg.channel.send(content="`Create new hero cancelled! To create a new hero use command !New.`", silent=True)
        else:
            await edit_msg.delete()
            await self.cmd.msg.channel.send(content="`Create new hero timed out! To create a new hero use command !New.`", silent=True)

        self.cmd.user.permit = True

    async def del_player_interaction(self):
        if not self.cmd.existing_user:
            await self.cmd.msg.channel.send(content=f"**```arm\r\nMiHero !Delete @{self.cmd.user.name}\r\n```**`You haven't created a hero yet.`\n`To create a new hero use command !New.`", silent=True)
            return
        
        self.cmd.user.permit = False # Set sender user interaction permission to false during fight
        
        renderer = StatsRenderer(user=self.cmd.user)
        await renderer.render_stats()
        player_stats_path = await renderer.get_stats_image()

        del_player_file = discord.File(fp=player_stats_path)
        del_player_view = DelPlayerView(user=self.cmd.user)

        await self.cmd.msg.channel.send(content=f"**```arm\r\nMiHero !Delete @{self.cmd.user.name}\r\n```** ", silent=True)
        edit_msg = await self.cmd.msg.channel.send(file=del_player_file, view=del_player_view)

        await del_player_view.wait()
        await renderer.del_image_folder()

        if del_player_view.confirm:
            await self.cmd.user.del_player()
            await self.cmd.db.rem_user(user=self.cmd.user)

            await edit_msg.delete()
            await self.cmd.msg.channel.send(content="`Your hero was deleted! To create a new hero use command !New.`", silent=True)
        elif del_player_view.cancel:
            await edit_msg.delete()
            await self.cmd.msg.channel.send(content="`Delete hero cancelled! To delete hero use command !Del.`", silent=True)
        else:
            await edit_msg.delete()
            await self.cmd.msg.channel.send(content="`Delete hero timed out! To delete hero use command !Del.`", silent=True)

        self.cmd.user.permit = True