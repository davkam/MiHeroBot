import logging
import os.path

bot_log_file = "logger/logs/bot_info.log"
data_log_file = "logger/logs/data_info.log"
game_log_file = "logger/logs/game_info.log"

class Logger():
    bot: logging.Logger = None
    data: logging.Logger = None
    game: logging.Logger = None

    def get_logger(name: str, file_path: str, level: int = 0):
        logger = logging.getLogger(name=name)

        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(filename=file_path, encoding="utf-8")

        stream_formatter = logging.Formatter("%(levelname)-10s - %(name)-15s : %(message)s")
        file_formatter = logging.Formatter("%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s")

        stream_handler.setFormatter(stream_formatter)
        file_handler.setFormatter(file_formatter)
   
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)
        logger.setLevel(level=level)
        logger.propagate = False

        return logger

    @classmethod
    def set_loggers(cls):
        if not os.path.exists(path="logger/logs"):
            os.mkdir(path="logger/logs")

        if not os.path.exists(path=bot_log_file):
            with open(bot_log_file, 'w') as file:
                file.write('')

            print(f'ERROR      - log             : File not found "{bot_log_file}", new file created!')

        if not os.path.exists(path=data_log_file):
            with open(data_log_file, 'w') as file:
                file.write('')

            print(f'ERROR      - log             : File not found "{data_log_file}", new file created!')

        if not os.path.exists(path=game_log_file):
            with open(game_log_file, 'w') as file:
                file.write('')

            print(f'ERROR      - log             : File not found "{game_log_file}", new file created!')

        cls.bot = cls.get_logger(name="discord", file_path=bot_log_file, level=logging.INFO)
        cls.data = cls.get_logger(name="data", file_path=data_log_file, level=logging.INFO)
        cls.game = cls.get_logger(name="game", file_path=game_log_file, level=logging.INFO)

        print(f'INFO       - log             : Loggers successfully initialized!')