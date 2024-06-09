import logging
import os.path

LOG_DIR = "loggers/logs"
BOT_LOG_FILE = "loggers/logs/bot_info.log"
DATA_LOG_FILE = "loggers/logs/data_info.log"
GAME_LOG_FILE = "loggers/logs/game_info.log"
RENDERER_LOG_FILE = "loggers/logs/renderer_info.log"

class Loggers():
    bot: logging.Logger = None
    data: logging.Logger = None
    game: logging.Logger = None
    renderer: logging.Logger = None

    @classmethod
    def set_loggers(cls) -> None:
        if not os.path.exists(path=LOG_DIR):
            os.makedirs(name=LOG_DIR)
            print(f"WARNING    - logger          : Directory not found '{LOG_DIR}', new directory created!")

        try:
            cls.bot = cls.get_logger(name="discord", file_path=BOT_LOG_FILE)
            cls.data = cls.get_logger(name="data", file_path=DATA_LOG_FILE)
            cls.game = cls.get_logger(name="game", file_path=GAME_LOG_FILE)
            cls.renderer = cls.get_logger(name="renderer", file_path=RENDERER_LOG_FILE)

            print(f"INFO       - logger          : Loggers successfully instatiated.")
        except Exception as exception:
            print(f"ERROR      - logger          : {str(exception)[10:]}")
            exit()

    @staticmethod
    def get_logger(name: str, file_path: str, level: int = logging.INFO) -> logging.Logger:
        logger = logging.getLogger(name=name)

        # Logger handlers for stream and file
        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(filename=file_path, encoding="utf-8")

        # Handler formatters for stream and file
        stream_formatter = logging.Formatter("%(levelname)-10s - %(name)-15s : %(message)s")
        file_formatter = logging.Formatter("%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s")

        stream_handler.setFormatter(stream_formatter)
        file_handler.setFormatter(file_formatter)
   
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)
        logger.setLevel(level=level)
        logger.propagate = False

        return logger