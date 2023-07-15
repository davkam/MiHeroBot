import discord
from .commands.commands import Commands
from data.database import Database
from discord.message import Message
from images.image_links import ImageLinks
from .token.token import Token

# Bot() object containing attributes required to instatiate and run bot.
# Instantiated as a single instance at module-level (main.py).
# Communicates with Commands() object through message_respond() method.
class Bot():
    _instance = None

    # Instantiates through singleton pattern, only one instance created.
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # Initializes with new instances of discord.Intents(), discord.Client() and Token() as attributes.
    def __init__(self):
        # New discord.Intents() instance with default settings.
        self.intents = discord.Intents.default()
        self.intents.message_content = True

        # New discord.Client() instance setup.
        self.client = discord.Client(intents = self.intents)

        # New Token() instance, configurates on initialization.
        self.token = Token()

    # Executes discord bot client.
    def run(self):
        self.client.run(self.token.get_value())

    # Called from event "on_ready() (at main.py) and runs when client is connected and ready.
    async def ready_respond(self):
        print('> Bot has successfully logged in as: {0.user}'.format(self.client))
        print('> Bot ID: {0}'.format(self.client.application_id))

        # Database() instantiation (single instance).
        db = Database()

        # Database() instantiation (single instance).
        img_links = ImageLinks()
        img_links.load_images()

    # Called from client event "on_message()" (at main.py) and runs when client receives a message.
    # Redirects message with User() and Message() instances to Commands() object for execution.
    async def message_respond(self, msg: Message):
        if msg.author == self.client.user:
            return
        
        if msg.content.startswith("!"):
            # New Commands() instance initialized with current discord.message.Message() and current User().
            commands = Commands(msg)
            user = await commands.set_user()

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