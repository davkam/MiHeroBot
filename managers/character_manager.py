import discord

from game.objects.characters.players import PlayerColor
from interface.views.new_player_view import NewPlayerView

class CharacterManager():
    def __init__(self, cmd):
        from bot.commands.commands import Commands
        self.cmd: Commands = cmd

    async def new_player_manager(self):
        if self.cmd.existing_user:
            await self.cmd.msg.channel.send(content=f"**```arm\r\nMiHero !New\r\n```**`You already have a hero` **{self.cmd.user.player.get_name()}**.\n`To start fighting use command !Fight.`", silent=True)
            return

        new_player_path = "game/assets/menus/new_%s.gif"
        new_player_file = discord.File(fp=new_player_path % "1")
        new_player_view = NewPlayerView(user=self.cmd.user)

        await self.cmd.msg.channel.send(content=f"**```arm\r\nMiHero !New\r\n```** ", silent=True)
        edit_msg = await self.cmd.msg.channel.send(file=new_player_file, view=new_player_view)

        while not await new_player_view.wait():
            if new_player_view.selected or new_player_view.canceled:
                break

            new_player_file = discord.File(fp=new_player_path % f"{new_player_view.character}")
            new_player_view = NewPlayerView(user=self.cmd.user, character=new_player_view.character)

            await edit_msg.edit(attachments=[new_player_file], view=new_player_view)

        if new_player_view.selected:
            await self.cmd.user.new_player(color=PlayerColor(new_player_view.character))
            await self.cmd.db.add_user(user=self.cmd.user)

            await edit_msg.delete()
            await self.cmd.msg.channel.send(content=f"`Created new hero` **{self.cmd.user.player.get_name()}**.\n`To start fighting use command !Fight.`")
        elif new_player_view.canceled:
            await edit_msg.delete()
            await self.cmd.msg.channel.send(content="`Create new hero canceled!`\n`To create a new hero use command !New.`")
        else:
            await edit_msg.delete()
            await self.cmd.msg.channel.send(content="`Create new hero timed out!`\n`To create a new hero use command !New.`")

    async def del_player_manager(self):
        if self.cmd.existing_user:
            await self.cmd.msg.channel.send(content = "**```arm\r\nMiHero !Delete\r\n```**`You haven't created a hero yet.`\n`To create a new hero use command !New.`", silent=True)
            return