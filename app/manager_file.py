import json
import os

class FileHandler:
    def __init__(self):
        self.path: str = "../save_files"
        self._name_file: str = ""
        self.content= None

    @property
    def name_file(self):
        return self._name_file

    @name_file.setter
    def name_file(self, name):
        self._name_file = name

    def open(self):
        try:
            file = open(os.path.join(self.path, self.name_file))
        except FileNotFoundError:
            print("File doesn't exist!")
        else:
            self.content = json.load(file)
            file.close()
            print(self.content['glossary'])


