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
            self._name_file = f"{value}.json" if not value.endswith(".json") else value

    def get_file_name_from_user(self) -> bool:
        i = 0
        while not self.name_file:
            name_file = input("Type the file name and press enter.\n>")
            self.name_file = name_file

            if not self.name_file:
                print("The file name can't be empty!")
                if i == 4:
                    print("Too many attempts!")
                    return False
            i += 1
        return True

    def open(self) -> Union[List[Dict[str, str]], None]:
        """
        The function opens file. Return:
            None - the file doesn't exist
            List of dicts
        """
        if not self.name_file:
            if not self.get_file_name_from_user():
                print("The file was not opened.")
                return
        try:
            with open(os.path.join(FileHandler.DIR_PATH, self.name_file)) as file:
                content = json.load(file)
        except FileNotFoundError:
            print("File doesn't exist!")
            return
        return content

    def save(self, buffer: List[Dict[str, str]]) -> None:
        """
        The method save tests_buffer to the file.
        """
        if not self.name_file:
            if not self.get_file_name_from_user():
                print("The file was not saved.")
                return

        with open(os.path.join(self.DIR_PATH, self.name_file), "w") as file:
            json.dump(buffer, file, indent=4)
        print("Saved. \n")
