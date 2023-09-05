from typing import Optional
import json
import os

class FileHandler:
    DIR_PATH = "files"

    def __init__(self):
        self._name_file: Optional[str] = None
        self.content = None

    @property
    def name_file(self):
        return self._name_file

    @name_file.setter
    def name_file(self, value: str):
        self._name_file = f"{value}.json" if not value.endswith('.json') else value

    def open(self):
        if not self.name_file:
            name_file = input("Please, write the name file\n>")
            self.name_file = name_file

        try:
            file = open(os.path.join(FileHandler.DIR_PATH, self.name_file))
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
