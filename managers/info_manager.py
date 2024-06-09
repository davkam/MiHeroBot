import discord

from interface.views.about_view import AboutView
from interface.renderers.info_renderer import InfoRenderer

class InfoManager():
    def __init__(self, cmd):
        from bot.commands.commands import Commands
        self.cmd: Commands = cmd

    async def help(self):
        help_file = discord.File(fp=InfoRenderer.HELP_PATH)

        await self.cmd.msg.channel.send(content=f"**```arm\r\nMiHero !Help\r\n```** ", silent=True)
        await self.cmd.msg.channel.send(file=help_file)

    async def about(self):
        about_file = discord.File(fp=InfoRenderer.ABOUT_PATH % 1)
        about_view = AboutView()

        await self.cmd.msg.channel.send(content=f"**```arm\r\nMiHero !About\r\n```** ", silent=True)
        edit_msg = await self.cmd.msg.channel.send(file=about_file, view=about_view)
        
        while not await about_view.wait():
            about_file = discord.File(fp=InfoRenderer.ABOUT_PATH % about_view.page)
            about_view = AboutView(page=about_view.page)

            await edit_msg.edit(attachments=[about_file], view=about_view)
        
        await edit_msg.delete()