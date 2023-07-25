import discord
from .commands.commands import Commands
from data.database import Database
from discord.message import Message
from game.decorators.decorators import DecoratorList
from images.image_links import ImageLinks
from log.logger import Logger
from .token.token import Token

# Bot object containing attributes required to instatiate and run bot.
# Instantiated as a single instance module-level object (at main.py).
# Communicates with commands object through "message_respond" method.
class Bot():
    _instance = None

    # Instantiates through singleton pattern, only one instance created.
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # Initializes with new instances of discord intents, discord client, token, and logger objects.
    def __init__(self):
        # New discord intents instance with default settings.
        self.intents = discord.Intents.default()
        self.intents.message_content = True

        # New discord client instance setup.
        self.client = discord.Client(intents = self.intents)

        # New token instance, configurates on initialization.
        self.token = Token()

        self.log: Logger = Logger.bot_logger

    # Executes discord bot client.
    def run(self):
        print("\n[ESTABLISHING BOT CONNECTION...]")
        self.client.run(self.token.get_value())

    # Called from "on_ready" event (at main.py) and runs when client is connected and ready.
    async def ready_respond(self):
        await self.log.write_log(log_data='Bot has successfully logged in as: {0.user}'.format(self.client))
        await self.log.write_log(log_data='Bot ID: {0}'.format(self.client.application_id))

        print("\n[LOADING DATA FILES...]")
        # Database instantiation (single instance).
        db = Database()
        await db.load_data()
        await db.load_temp_data()

        # Image links instantiation (single instance).
        img_links = ImageLinks()
        await img_links.load_images()

        # Decorator list instantiation (single instance).
        dec_list = DecoratorList()
        await dec_list.load_decorators()

        print("\n> Connected to following guilds:")
        async for guild in self.client.fetch_guilds():
            print(f"    - {guild.name}")
        
        print()

    # Called from "on_message" event (at main.py) and runs when client receives a message.
    # Redirects message with user and message objects to commands object for execution.
    async def message_respond(self, msg: Message):
        if msg.author == self.client.user:
            return
        
        if msg.content.startswith("!"):
            # New commands instance initialized with current message and current user.
            commands = Commands(msg)
            user = await commands.set_user()

            # Checks user permission and returns if false.
            if user.permit_interaction == False: return

            message = msg.content.lower()

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