from bot.client import Client
from loggers.loggers import Loggers

VERSION_NR = "v1.0.0"

def main():
    print(f"\n- MIHEROBOT {VERSION_NR} -")

    print("\n[INITIATING LOGGERS...]")
    Loggers.set_loggers()

    print("\n[ESTABLISHING CONNECTION...]")
    bot_client = Client()
    bot_client.run()

if __name__ == "__main__":
    main()