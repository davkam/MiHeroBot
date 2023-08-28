class StatChangeEvent():
    instance = None

    def __new__(cls):
        if cls.instance == None:
            cls.instance = super().__new__(cls)
        else:
            return cls.instance
        
    def __init__(self):
        self.callback = list()

    def add_callback(self, callback):
        self.callback.append(callback)

    def remove_callback(self, callback):
        self.callback.remove(callback)

    def trigger_event(self, *args, **kwargs):
        for callback in self.callback:
            callback(*args, **kwargs)

class InventoryChangeEvent():
    instance = None

    def __new__(cls):
        if cls.instance == None:
            cls.instance = super().__new__(cls)
        else:
            return cls.instance
        
    def __init__(self):
        self.callback = list()

    def add_callback(self, callback):
        self.callback.append(callback)

    def remove_callback(self, callback):
        self.callback.remove(callback)

    def trigger_event(self, *args, **kwargs):
        for callback in self.callback:
            callback(*args, **kwargs)