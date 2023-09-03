from typing import List, Dict
from .text import Text

class Buffer:
    def __init__(self):
        self.data = []


    def add(self, text: Text):
        self.data.append(text)

    def convert_to_arr_of_dicts(self) -> List[Dict[str, str]]:
        """ Function convert Buffer to dict """
        return [text.__dict__ for text in self.data]

    def print_buffer(self):
        for idx, text in enumerate(self.data, start=1):
            print(text)

