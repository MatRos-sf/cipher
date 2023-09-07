from typing import Optional, List, Dict, Union
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
        if value.rstrip():
            self._name_file = f"{value}.json" if not value.endswith('.json') else value

    def is_name_file_exist(self) -> bool:
        if not self.name_file:
            name_file = input("Please, enter the name file\n>")
            self.name_file = name_file
            if not self.name_file:
                print("The name file can't be empty.")
                return False
        return True

    def open(self) -> Union[List[Dict[str, str]], None]:

        if not self.is_name_file_exist():
            return

        try:
            file = open(os.path.join(FileHandler.DIR_PATH, self.name_file))
        except FileNotFoundError:
            print("File doesn't exist!")
        else:
            self.content = json.load(file)
            file.close()
            return self.content

    def save(self, buffer: List[Dict[str, str]]) -> None:

        if not self.is_name_file_exist():
            return

        if not self.name_file:
            name_file = input("Please write name file to save\n>")
            try:
                self.name_file = name_file
            except NameError:
                print("The name can't be empty.")
                return

        with open(os.path.join(self.DIR_PATH, self.name_file), "w") as file:
            json.dump(buffer, file, indent=4)
        print("Saved. \n")
