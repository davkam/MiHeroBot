import datetime

class Logger():
    # Static class attributes for object access.
    bot_logger = None           # Contains bot connect related logs.
    data_logger = None          # Contains database related logs.
    user_logger = None          # Contains player related logs.
    combat_logger = None        # Contains combat related logs.
    transaction_logger = None   # Contains transaction related logs.

    def __init__(self, file):
        self.file: str = file

    # Static class method.
    # Instantiates new logger objects, assigns to static class attribute.
    @classmethod 
    def new_loggers(cls):
        cls.bot_logger = Logger(file="log/logs/bot_logs.txt")
        cls.data_logger = Logger(file="log/logs/data_logs.txt")
        cls.user_logger = Logger(file="log/logs/user_logs.txt")
        cls.combat_logger = Logger(file="log/logs/combat_logs.txt")
        cls.transaction_logger = Logger(file="log/logs/transaction_logger.txt")

    # Writes (appends) log to file.
    async def write_log(self, log_data: str):
        # Gets current date and time for log appendage.
        date_time = str(datetime.datetime.now())[:-7]

        with open(self.file, "a") as log:
            log.write(f"[{date_time}]: {log_data}\n")

        print(f"> {log_data}")