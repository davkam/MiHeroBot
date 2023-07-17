import json
import os.path

# Token() object required for Bot() instance, only one instance created (instatiated with Bot() instance).
# Contains attributes for discord token key and file path to token save file location.
class Token():
    def __init__(self):
        self.value = None
        self.file_path = "bot/token/token.json"
        self.set_token()
        
    # Sets token value from file path, if exception occurs it creates token instead.
    def set_token(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r") as token_file:
                    get_token = json.load(token_file)
                    self.value = get_token["TOKEN"]
                print(f'> Token file successfully loaded from file "{self.file_path}".')
            else:
                print(f'> Token file "{self.file_path}" could not be found.')
                self.create_token()
        except Exception as exception:
            print(f'> Failed to retrieve token from file "{self.file_path}".\n' + str(exception))
            self.create_token()
    
    # Creates new token, sets token value and creates new .json-file to file path location.
    def create_token(self):
        try:
            key_input = input("> Enter new token value: ")
            self.value = key_input
            new_token = {"TOKEN": key_input}
            
            with open(self.file_path, "w+") as token_file:
                json.dump(new_token, token_file, indent = 4)
        except Exception as exception:
            print(str(exception))
            exit()

    # Returns token value.
    def get_value(self):
        return self.value