from typing import List, Dict
from .text import Text

class Buffer:
    def __init__(self):
        self.data = []

    def add(self, text: Text):
        self.data.append(text)

    def add_list_of_dict(self, arr: List[Dict[str, str]]):
        for text in arr:
            self.add(Text(**text))

    def convert_to_arr_of_dicts(self) -> List[Dict[str, str]]:
        """ Function convert Buffer to dict """
        return [text.__dict__ for text in self.data]

    def print_buffer(self) -> None:
        for idx, text in enumerate(self.data, start=1):
            print(idx, text, sep=': ')
        print()

