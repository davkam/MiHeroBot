import os.path

# ImageLinks()-Object class containing image links used in FightEmbed().
class ImageLinks():
    instance = None # Class attribute of an ImageLinks()-instance.

    # New instance instantiated through singleton pattern at bot.ready_respond(),
    # assigned to static attribute "instance" for access. 
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.file_path: str = "images/image_links.txt"
        self.links: list[str] = list()

    # Loads image links from .txt-file and assigns it to instanced attribute "self.links: list[str]".
    async def load_images(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r") as token_file:
                    self.links = token_file.readlines()
                print("> Image links successfully loaded from file.")
            else:
                print(f'> Image links file "{self.file_path}" could not be found.')
        except Exception as exception:
            print(f'> Failed to retrieve links from "{self.file_path}"\n' + str(exception))