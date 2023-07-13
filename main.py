from bot.bot import Bot

# Main module for code execution.
# Communicates with Bot() instance (at bot.py) through event listeners.

# Bot() instantiation (single instance).
bot = Bot()

# Event listener for "on_ready()", runs when client is ready and connected.
@bot.client.event
async def on_ready():
    await bot.ready_respond()

# Event listener for "on_message()", runs when a message is created in discord channel.
@bot.client.event
async def on_message(msg):
    await bot.message_respond(msg)

# Bot client execution.
bot.run()