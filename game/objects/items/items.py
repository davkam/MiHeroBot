

class Item():
    def __init__(self, id: int = None, name: str = None, value: int = None):
        self.id: int = id
        self.name: str = name
        self.value: int = value

    def set_name(self, name: str = None):
        self.name = name