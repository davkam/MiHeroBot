from .commands.commands import Commands
from data.database import Database
from discord.ext import commands
from discord.message import Message
from emoticons.emoticons import Emoticons
from images.image_links import ImageLinks
from log.logger import Logger
from .token.token import Token
import discord

# Client object containing attributes in bot instantiation, and methods for bot execution and operation.
# Instantiated as a single instance module-level object (at main.py).
# Communicates with commands object through "on_message" method.
class Client(discord.Client):
    _instance = None

    # Instantiation through singleton pattern.
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # Initialization with new instances of discord intents (default settings), token and logger.
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.intents.message_content = True

        # Assigns a token object, initialized in constructor.
        self.token = Token()
        self.log: Logger = Logger.bot_logger

    def run(self):
        print("\n[ESTABLISHING BOT CONNECTION...]")
        return super().run(self.token.get_value())

    # On ready method, called when bot client is connected and ready.
    async def on_ready(self):
        await self.log.write_log(log_data='Bot has successfully logged in as: {0.user}'.format(self))
        await self.log.write_log(log_data='Bot ID: {0}'.format(self.application_id))

        print("\n[LOADING DATA FILES...]")
        # Instantiates new databases (guild unique) and loads their respective data through method.
        await Database.load_databases(client=self)

        # Instantiates image links (single instance) and loads images for use in combat simulation.
        img_links = ImageLinks()
        await img_links.load_images()

        # Instantiates emoticons (single instance) and loads unicodes for use as decorators.
        emoticons = Emoticons()
        await emoticons.load_emoticons()

        print("\n> Connected to following guilds:")
        async for guild in self.fetch_guilds():
            print(f"    - {guild.name}")
        
        print()

    # On message method, called when client receives a message.
    # Redirects message with user to commands object for execution.
    async def on_message(self, message: Message):
        if message.author == self.user:
            return
        
        if message.content.startswith("!"):
            # New commands instance initialized with current message and current user.
            commands = Commands(msg=message, db_id=message.guild.id)
            user = await commands.set_user()

            # Checks user permission and returns if false.
            if user.permit_interaction == False: return

            message = message.content.lower()

            if message.startswith("!help"):
                await commands.help()
            elif message.startswith("!about"):
                await commands.about()
            elif message.startswith("!new"):
                await commands.new()
            elif message.startswith("!delete"):
                await commands.delete()
            elif message.startswith("!fight"):
                await commands.fight()
            elif message.startswith("!inv"):
                await commands.inventory()
            elif message.startswith("!trade"):
                await commands.trade()
            elif message.startswith("!shop"):
                await commands.shop()
            elif message.startswith("!stats"):
                await commands.stats()
            elif message.startswith("!score"):
                await commands.score()
            elif message.startswith("!save"):
                await commands.save()
            elif message.startswith("!load"):
                await commands.load()
            elif message.startswith("!test"):
                await commands.test()
            else:
                pass

            # Removing object reference for garbage collection. (NOT REQUIRED!)
            commands = None