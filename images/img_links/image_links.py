import logging
import os.path

from logger.logger import Logger

# Image links object containing image links used in fight embed instance.
# TBD: Use local image files! E.g;
#      file = discord.File("path/to/image.png", filename="image.png")
#      embed.set_image(url="attachment://image.png")
#      await channel.send(file=file, embed=embed)
class ImageLinks():
    instance = None # Static class attribute for object reference.

    # Instantiate through singleton pattern.
    # Assign to static attribute for object access. 
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.file_path: str = "images/img_links/image_links.txt"
        self.links: list[str] = list()
        self.logger: logging.Logger = Logger.data

    # Load image links from '.txt'-file and assign it to attribute.
    async def load_images(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r") as token_file:
                    self.links = token_file.readlines()

                self.logger.info(msg=f"Loaded image links from file. FILE: '{self.file_path}'")
            else:
                self.logger.warning(msg=f"Failed to load image links from file. File not found. FILE: '{self.file_path}'")
        except Exception as exception:
            self.logger.error(msg=f"Failed to load image links from file. EXCEPTION: {str(exception)}")