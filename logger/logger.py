import logging

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
        cls.bot = cls.get_logger(name="discord", file_path="logger/logs/bot_info.log", level=logging.INFO)
        cls.data = cls.get_logger(name="data", file_path="logger/logs/data_info.log", level=logging.INFO)
        cls.game = cls.get_logger(name="game", file_path="logger/logs/game_info.log", level=logging.INFO)