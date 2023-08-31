import logging
import os.path

from logger.logger import Logger

class Emoticons():
    instance = None # Static class attribute for object reference

    # Instantiate through singleton pattern
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.file_path: str = "emoticons/unicode_emoticons.txt"
        self.tier1: list[str] = list()
        self.tier2: list[str] = list()
        self.tier3: list[str] = list()
        self.logger: logging.Logger = Logger.data

    # Load emoticons from '.txt'-file
    async def load_emoticons(self):
        try:
            if os.path.exists(self.file_path):
                with open(file=self.file_path, mode="r") as emoticon:
                    emoticon_list = emoticon.readlines()

                self.logger.info(msg=f'Loaded emoticons from file. FILE: "{self.file_path}"')
            else:
                self.logger.warning(msg=f'Failed to load emoticons from file. No file found. FILE: "{self.file_path}"')
        except Exception as exception:
            self.logger.error(msg=f'Failed to load emoticons from file. EXCEPTION: {str(exception)}')
        
        await self.sort_emoticons(emoticon_list=emoticon_list)
        
    # Sort emoticons from file into their respective tier list
    async def sort_emoticons(self, emoticon_list: list):
        emoticon_list: list[str] = emoticon_list
        sort_list: list[str] = list()
        
        i = 0
        for emoticon in emoticon_list:
            if emoticon.startswith("#"):
                if i == 1:
                    self.tier1 = sort_list
                elif i == 2:
                    self.tier2 = sort_list
                elif i == 3:
                    self.tier3 = sort_list
                i += 1 
                sort_list = list()
            else:
                converted_emoticon = bytes(emoticon, "UTF-8").decode("unicode_escape")
                sort_list.append(converted_emoticon.strip())