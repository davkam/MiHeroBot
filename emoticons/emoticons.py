from log.logger import Logger
import os.path

class Emoticons():
    instance = None # Static class attribute for object reference.

    # Instantiated through singleton pattern, only one instance created.
    # Instantiated at bot's "ready_respond" method and assigned to static class attribute.
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.file_path: str = "emoticons/unicode_emoticons.txt"
        self.tier1: list[str] = list()
        self.tier2: list[str] = list()
        self.tier3: list[str] = list()
        self.log: Logger = Logger.data_logger

    # Loads emoticons from file.
    async def load_emoticons(self):
        try:
            if os.path.exists(self.file_path):
                with open(file=self.file_path, mode="r") as emoticon:
                    emoticon_list = emoticon.readlines()

                await self.log.write_log(log_data=f'Loaded emoticons from file. FILE: "{self.file_path}"')
            else:
                await self.log.write_log(log_data=f'Failed to load emoticons from file, file not found. FILE: "{self.file_path}"')
        except Exception as exception:
            await self.log.write_log(log_data=f'Failed to load emoticons from file. FILE: "{self.file_path}"\nEXCEPTION: {str(exception)}')
        
        await self.sort_emoticons(emoticon_list=emoticon_list)
        
    # Sorts emoticons from file into tier lists.
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