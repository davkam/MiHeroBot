import dotenv
import logging
import os

from logger.logger import Logger

class Token():
    def __init__(self):
        self.key: str = None
        self.file_path: str = "bot/token/.env"
        self.logger: logging.Logger = Logger.bot

        self.set_token()
        
    def set_token(self):
        if os.path.exists(self.file_path):
            dotenv.load_dotenv()
            self.key = os.getenv("API_TOKEN")

            self.logger.info(msg=f"Retrieved token key from '.env'-file. FILE: '{self.file_path}'")
        else:
            self.logger.warning(msg=f"Failed to retrieve token key from '.env'-file. No file found. FILE: '{self.file_path}'")
            self.create_token()

    def create_token(self):
        try:
            key_input = input("> Enter new token key: ")
            self.key = key_input

            with open(self.file_path, "w") as api_key:
                api_key.write(f"API_TOKEN='{self.key}'")

            self.logger.info(msg=f"Saved new token key to '.env'-file. FILE: '{self.file_path}'")
        except Exception as exception:
            self.logger.error(msg=f"Failed to create new token to '.env'-file. EXCEPTION: {str(exception)}")
            exit()