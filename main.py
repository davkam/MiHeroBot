from bot.bot import Bot
from log.logger import Logger

# Main module for code execution.
# Communicates with bot instance through event listeners.

def run_bot():
    print("> Booting up MiHeroBot...")

    # Instantiates new loggers.
    Logger.new_loggers()

    # Bot instantiation (single instance).
    bot = Bot()

    # Event listener "on_ready", runs when client is ready and connected.
    @bot.client.event
    async def on_ready():
        await bot.ready_respond()

    # Event listener "on_message", runs when a message is created in discord channel.
    @bot.client.event
    async def on_message(msg):
        await bot.message_respond(msg)

    # Bot client execution.
    bot.run()

if __name__ == "__main__":
    run_bot()