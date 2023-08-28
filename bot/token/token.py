from log.logger import Logger
import asyncio
import json
import os.path

# Token object required for bot instance, only one instance created (instatiated with bot instance).
# Contains attributes for discord token key, file path to token save file location, and a logger.
class Token():
    def __init__(self):
        self.value = None
        self.file_path = "bot/token/token.json"
        self.log: Logger = Logger.bot_logger

        self.set_token()
        
    # Sets token value from file path. If exception or file not found occurs, it creates a new token instead.
    def set_token(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r") as token_file:
                    get_token = json.load(token_file)
                    self.value = get_token["TOKEN"]

                asyncio.run(self.log.write_log(log_data=f'Loaded token from file. FILE: "{self.file_path}"'))
            else:
                asyncio.run(self.log.write_log(log_data=f'Failed to load token from file, file not found. FILE: "{self.file_path}"'))
                self.create_token()
        except Exception as exception:
            asyncio.run(self.log.write_log(log_data=f'Failed to load token from file. FILE: "{self.file_path}"\nEXCEPTION: {str(exception)}'))
            self.create_token()
    
    # Creates new token, sets token value and creates new .json-file to file path location.
    def create_token(self):
        try:
            key_input = input("> Enter new token value: ")
            self.value = key_input
            new_token = {"TOKEN": key_input}
            
            with open(self.file_path, "w+") as token_file:
                json.dump(new_token, token_file, indent = 4)

            asyncio.run(self.log.write_log(log_data=f'Created and saved new token to file "{self.file_path}".'))
        except Exception as exception:
            asyncio.run(self.log.write_log(log_data=f'Failed to create new token.\n{str(exception)}'))
            exit()

    # Returns token value.
    def get_value(self):
        return self.value