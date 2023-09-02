import json
import os

class FileHandler:
    def __init__(self):
        self.path: str = "save_files"
        self._name_file: str = ""
        self.content= None

    @property
    def name_file(self):
        return self._name_file

    @name_file.setter
    def name_file(self, name):
        self._name_file = name +'.json'

    def open(self):
        if not self.name_file:
            name_file = input("Please write name file to save\n>")
            self.name_file = name_file

        try:
            file = open(os.path.join(self.path, self.name_file))
        except FileNotFoundError:
            print("File doesn't exist!")
        else:
            self.content = json.load(file)
            file.close()
            return self.content

    def save(self, buffers):
        if not self.name_file:
            name_file = input("Please write name file to save\n>")
            self.name_file = name_file

        file = open(os.path.join(self.path, self.name_file), "w")
        json.dump(buffers, file)
        file.close()
