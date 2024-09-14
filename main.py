from bot.client import Client
from loggers.loggers import Loggers

VERSION_NR = "v1.0.0"

def main():
    """
    The main function of the MiHeroBot program.
    It initializes the loggers, establishes a connection, and runs the bot client.
    """
    print(f"\n- MIHEROBOT {VERSION_NR} -")

    print("\n[INITIATING LOGGERS...]")
    Loggers.set_loggers()

    print("\n[ESTABLISHING CONNECTION...]")
    bot_client = Client()
    bot_client.run()

if __name__ == "__main__":
    main()

### TO DO!
### Check string concatenation!
### Check escaping references!
###     - Minimize the use of global variables.
###     - Be cautious with closures and ensure they do not capture unnecessary variables.
###     - Avoid using mutable default arguments.
###     - Regularly review and profile your code to identify and address memory leaks.