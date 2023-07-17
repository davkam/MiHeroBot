import os.path

class DecoratorList():
    instance = None # Class attribute of Database() instance.

    # Instantiated through singleton pattern, only one instance created.
    # Instantiated at bot.ready_respond() and assigned to Database.instance attribute.
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.file_path: str = "game/decorators/unicode_emoticons.txt"
        self.tier1: list[str] = list()
        self.tier2: list[str] = list()
        self.tier3: list[str] = list()

    async def load_decorators(self):
        try:
            if os.path.exists(self.file_path):
                with open(file=self.file_path, mode="r") as decorator:
                    decorator_list = decorator.readlines()

                print("> Decorator list successfully loaded from file.")
            else:
                print(f'> Decorator list file "{self.file_path}" could not be found.')
                return
        except Exception as exception:
            print(f'> Failed to retrieve decorator list from "{self.file_path}"\n' + str(exception))
            return
        
        await self.sort_decorators(dec_list=decorator_list)
        
    async def sort_decorators(self, dec_list: list):
        dec_list: list[str] = dec_list
        sort_list: list[str] = list()
        
        i = 0
        for decorator in dec_list:
            if decorator.startswith("#"):
                if i == 1:
                    self.tier1 = sort_list
                elif i == 2:
                    self.tier2 = sort_list
                elif i == 3:
                    self.tier3 = sort_list
                i += 1 
                sort_list = list()
            else:
                converted_decorator = bytes(decorator, "UTF-8").decode("unicode_escape")
                sort_list.append(converted_decorator.strip())