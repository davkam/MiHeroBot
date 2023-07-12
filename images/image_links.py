import os.path

class ImageLinks():
    instance = None # Static attribute of a ImageLinks()-instance.

    # __new__(): Instantiates through singleton pattern, only one instance allowed.
    #            Instantiated at bot.ready_respond() and assigned to Database.instance.
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.file_path: str = "images/image_links.txt"
        self.links: list[str] = list()

    def load_images(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r") as token_file:
                    self.links = token_file.readlines()
            else:
                print(f'> Image links file "{self.file_path}" could not be found.')
        except Exception as exception:
            print(f'> Failed to retrieve links from "{self.file_path}"\n' + str(exception))