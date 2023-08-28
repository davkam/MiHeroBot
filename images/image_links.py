from log.logger import Logger
import os.path

# Image links object containing image links used in fight embed instance.
class ImageLinks():
    instance = None # Static class attribute for object reference.

    # New instance instantiated through singleton pattern at bot's "ready_respond" method,
    # Assigned to static attribute "instance" for object access. 
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.file_path: str = "images/image_links.txt"
        self.links: list[str] = list()
        self.log: Logger = Logger.data_logger

    # Loads image links from .txt-file and assigns it to instanced attribute "links".
    async def load_images(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r") as token_file:
                    self.links = token_file.readlines()

                await self.log.write_log(log_data=f'Loaded image links from file. FILE: "{self.file_path}"')
            else:
                await self.log.write_log(log_data=f'Failed to load image links from file, file not found. FILE: "{self.file_path}"')
        except Exception as exception:
            await self.log.write_log(log_data=f'Failed to load image links from file. FILE: "{self.file_path}"\nEXCEPTION: {str(exception)}')