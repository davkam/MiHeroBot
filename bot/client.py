import discord
import logging

from .commands.commands import Commands
from discord.message import Message
from interface.renderers.info_renderer import InfoRenderer
from loggers.loggers import Loggers
from .token.token import Token
from users.userdata.userdata import UserData

class Client(discord.Client):
    _instance = None

    # Instantiate through singleton pattern
    def __new__(cls) -> discord.Client:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.all())
        self.token = Token()
        self.logger: logging.Logger = Loggers.bot

    def run(self):
        return super().run(self.token.key, root_logger=True)

    async def on_ready(self) -> None:
        """
        On ready event listener, run when client is ready and connected.
        Call on start-up methods for further initialization.
        """

        self.logger.info(msg=f"Bot client connected. USER: {self.user} (ID: {self.user.id})")

        print("\n[PREPARING USER DATA...]")
        connected_guilds: str = str()
        async for guild in self.fetch_guilds():
            await UserData.new_database(id=guild.id)

            connected_guilds += f"    - {guild.name} (ID: {guild.id})\n"

        print("\n[RENDERING IMAGES...]")
        renderer = InfoRenderer()
        await renderer.render_help()
        await renderer.render_about()

        print(f"\n> GUILDS CONNECTED:\n {connected_guilds}")

    async def on_message(self, message: Message) -> None:
        """
        On message event listener, run when client receive a message.
        Redirect message and user to commands class for further execution.
        """

        # Check if client is message author, return if true
        if message.author == self.user:
            return
        
        if message.content.startswith("!"):
            commands = Commands(msg=message, db_id=message.guild.id)
            user = await commands.set_user()

            # Check user permission, return if false
            if user.permit == False: return

            msg = message.content.lower() 

            if msg.startswith("!help"):
                await commands.help()
            elif msg.startswith("!about"):
                await commands.about()
            elif msg.startswith("!new"):
                await commands.new()
            elif msg.startswith("!del"):
                await commands.delete()
            elif msg.startswith("!fight"):
                await commands.fight()
            elif msg.startswith("!roul"):
                await commands.roulette()
            elif msg.startswith("!inv"):
                await commands.inventory()
            elif msg.startswith("!trade"):
                await commands.trade()
            elif msg.startswith("!shop"):
                await commands.shop()
            elif msg.startswith("!stats"):
                await commands.stats()
            elif msg.startswith("!board"):
                await commands.leaderboard()
            elif msg.startswith("!bug"):
                await commands.bug()
            else:
                pass

            # Remove object reference for garbage collection
            commands = None