from bot.client import Client
from loggers.loggers import Loggers

VERSION_NR = "v1.0.0"

def initialize_loggers():
    """
    Initializes the loggers for the MiHeroBot program.
    """
    print("\n[INITIATING LOGGERS...]")
    Loggers.set_loggers()

def establish_connection():
    """
    Establishes the connection for the MiHeroBot client.
    """
    print("\n[ESTABLISHING CONNECTION...]")
    bot_client = Client()
    bot_client.run()

def main():
    """
    The main function of the MiHeroBot program.
    It initializes the loggers, establishes a connection, and runs the bot client.
    """
    print(f"\n- MIHEROBOT {VERSION_NR} -")
    initialize_loggers()
    establish_connection()

if __name__ == "__main__":
    main()

### TO DO!
### Check string concatenation!
### Check escaping references!
###     - Minimize the use of global variables.
###     - Be cautious with closures and ensure they do not capture unnecessary variables.
###     - Avoid using mutable default arguments.
###     - Regularly review and profile your code to identify and address memory leaks.