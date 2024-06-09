import dotenv
import logging
import os

from loggers.loggers import Loggers

TOKEN_FILE = "bot/token/.env"

class Token():
    def __init__(self) -> None:
        self.key: str = None
        self.file_path: str = TOKEN_FILE
        self.logger: logging.Logger = Loggers.bot

        self.set_token()
        
    def set_token(self) -> None:
        if os.path.exists(self.file_path):
            dotenv.load_dotenv()
            self.key = os.getenv("API_TOKEN")

            self.logger.info(msg=f"Successfully retrieved token key from file. FILE: '{self.file_path}'")
        else:
            self.logger.warning(msg=f"Failed to retrieve token key from file, no file found. FILE: '{self.file_path}'")
            self.create_token()

    def create_token(self) -> None:
        try:
            key_input = input("\n> ENTER NEW TOKEN KEY: ")
            self.key = key_input

            with open(self.file_path, "w") as api_key:
                api_key.write(f"API_TOKEN='{self.key}'")

            self.logger.info(msg=f"Successfully saved new token key to file. FILE: '{self.file_path}'")
        except Exception as exception:
            self.logger.error(msg=f"Failed to create new token to file. EXCEPTION: {str(exception)[10:]}")
            exit()