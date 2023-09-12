from typing import Optional, List, Dict, Union
import json
import os


class FileHandler:
    DIR_PATH: str = "files"

    def __init__(self):
        self._name_file: Optional[str] = None
        self.content: Optional[Dict[str, str]] = None

    @property
    def name_file(self):
        return self._name_file

    @name_file.setter
    def name_file(self, value: str):
        value = value.rstrip()
        if value:
            self._name_file = f"{value}.json" if not value.endswith('.json') else value

    def get_file_name_from_user(self) -> None:

        while not self.name_file:
            name_file = input("Type the file name and press enter.\n>")
            self.name_file = name_file

            if not name_file:
                print("The file name can't be empty!")

    def open(self) -> Union[List[Dict[str, str]], None]:
        """
        The function opens file. Return:
            None - the file doesn't exist
            List of dicts
        """
        if not self.name_file:
            self.get_file_name_from_user()

        try:
            with open(os.path.join(FileHandler.DIR_PATH, self.name_file)) as file:
                self.content = json.load(file)
        except FileNotFoundError:
            print("File doesn't exist!")
            return

    def save(self, buffer: List[Dict[str, str]]) -> None:
        """
        The function save buffer to the file.
        """
        if not self.name_file:
            self.get_file_name_from_user()

        with open(os.path.join(self.DIR_PATH, self.name_file), "w") as file:
            json.dump(buffer, file, indent=4)
        print("Saved. \n")
