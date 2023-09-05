import discord
import logging

from .commands.commands import Commands
from data.database import Database
from discord.message import Message
from emoticons.emoticons import Emoticons
from images.img_links.image_links import ImageLinks
from logger.logger import Logger
from .token.token import Token

class Client(discord.Client):
    _instance = None

    # Instantiate through singleton pattern.
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.token = Token()
        self.logger: logging.Logger = Logger.bot

    def run(self):
        return super().run(self.token.key, root_logger=True)

    # On ready event listener, run when bot client is ready and connected.
    async def on_ready(self):
        self.logger.info(msg=f"Bot client connected. USER: {self.user} (ID: {self.user.id})")

        print("\n> Connected to following guilds:")
        async for guild in self.fetch_guilds():
            print(f"    - {guild.name}")

        print("\n[LOADING DATA FILES...]")
        await Database.load_databases(client=self)

        print("> Loading image links and emoticons...")
        img_links = ImageLinks()
        await img_links.load_images()
        emoticons = Emoticons()
        await emoticons.load_emoticons()
        print()

    # On message event listener, run when client receives a message.
    # Redirect message with user to commands object for execution.
    async def on_message(self, message: Message):
        if message.author == self.user:
            return
        
        if message.content.startswith("!"):
            commands = Commands(msg=message, db_id=message.guild.id)
            user = await commands.set_user()

            # Check user interaction permission, return if false.
            if user.permit_interaction == False: return

            msg = message.content.lower() 

            if msg.startswith("!help"):
                await commands.help()
            elif msg.startswith("!about"):
                await commands.about()
            elif msg.startswith("!new"):
                await commands.new()
            elif msg.startswith("!delete"):
                await commands.delete()
            elif msg.startswith("!fight"):
                await commands.fight()
            elif msg.startswith("!stake"):
                await commands.stake()
            elif msg.startswith("!inv"):
                await commands.inventory()
            elif msg.startswith("!trade"):
                await commands.trade()
            elif msg.startswith("!shop"):
                await commands.shop()
            elif msg.startswith("!stats"):
                await commands.stats()
            elif msg.startswith("!board"):
                await commands.board()
            elif msg.startswith("!save"):
                await commands.save()
            elif msg.startswith("!load"):
                await commands.load()
            elif msg.startswith("!test"):
                await commands.test()
            else:
                pass

            # Remove object reference for garbage collection. (NOT REQUIRED!)
            commands = None