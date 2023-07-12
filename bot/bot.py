import discord
from .commands.commands import Commands
from data.database import Database
from discord.message import Message
from images.image_links import ImageLinks
from .token.token import Token

# Bot(): Bot()-object containing attributes for discord.Intents(), discord.Client() and Token().
#        Instantiates (single instance) as a module-level object (at bot.py).
#        Communicates with Commands()-instance through message_respond()-method.
class Bot():
    _instance = None

    # __new__(): Instantiates through singleton pattern, only one instance allowed.
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # __init__(): Initializes with new instances of discord.Intents(), discord.Client() and Token() as attributes.
    def __init__(self):
        # New discord.Intents() instance with settings.
        self.intents = discord.Intents.default()
        self.intents.message_content = True

        # New discord.Client() instance setup.
        self.client = discord.Client(intents = self.intents)

        # New Token() instance, configurates upon initialization.
        self.token = Token()

    # run(): Executes discord bot client.
    def run(self):
        self.client.run(self.token.get_value())

    # ready_respond(): Called from client event "on_ready" (at main.py) and runs when client is connected and ready.
    async def ready_respond(self):
        print('> Bot has successfully logged in as: {0.user}'.format(self.client))
        print('> Bot ID: {0}'.format(self.client.application_id))

        # Database() instantiation (single instance).
        db = Database()

        # Database() instantiation (single instance).
        img_links = ImageLinks()
        img_links.load_images()

    # message_respond(): Called from client event "on_message" (at main.py) and runs when client receives a message.
    #                    Redirects message with "user" and "msg" to Commands() for execution.
    async def message_respond(self, msg: Message):
        if msg.author == self.client.user:
            return
        
        if msg.content.startswith("!"):
            # New Commands()-instance initialized with current discord.message.Message() and current User().
            commands = Commands(msg)
            await commands.set_user()

            message = msg.content.lower()

            if message.startswith("!help"):
                await commands.help()
            if message.startswith("!about"):
                await commands.about()
            if message.startswith("!new"):
                await commands.new()
            if message.startswith("!delete"):
                await commands.delete()
            if message.startswith("!fight"):
                await commands.fight()
            if message.startswith("!shop"):
                await commands.shop()
            if message.startswith("!inv"):
                await commands.inventory()
            if message.startswith("!stats"):
                await commands.stats()
            if message.startswith("!score"):
                await commands.score()
            if message.startswith("!load"):
                await commands.load()
            if message.startswith("!save"):
                await commands.save()

            # Removing object reference for garbage collection. (NOT REQUIRED!)
            commands = None