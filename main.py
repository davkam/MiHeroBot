from bot.client import Client
from logger.logger import Logger

def main():
    Logger.set_loggers()

    print("[ESTABLISHING BOT CONNECTION...]")
    bot_client = Client()
    bot_client.run()

if __name__ == "__main__":
    main()