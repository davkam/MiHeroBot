import json
import os.path

# class Token(): Token object required for Bot() instance.
#                Contains attributes token (discord token key) and file_path (token.json save file location)
class Token():
    def __init__(self):
        self.value = None
        self.file_path = "bot/token/token.json"
        self.set_token()
        
    # set_token(): Sets token value from file_path, if exception occurs -> create_token().
    def set_token(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r") as token_file:
                    get_token = json.load(token_file)
                    self.value = get_token["TOKEN"]
            else:
                print(f'> Token file "{self.file_path}" could not be found.')
                self.create_token()
        except Exception as exception:
            print(f'> Failed to retrieve token from "{self.file_path}"\n' + str(exception))
            self.create_token()
    
    # create_token(): Creates new token, sets token value and saves new .json to file_path.
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

    # get_token(): Returns token value.
    def get_value(self):
        return self.value