from typing import List, Dict
from .text import Text

from textwrap import shorten


class Buffer:
    def __init__(self):
        self.data: List[Text] = []

    def add(self, text: Text) -> None:
        if isinstance(text, Text):
            self.data.append(text)

    def add_list_of_dict(self, arr: List[Dict[str, str]]) -> None:
        for text in arr:
            try:
                t = Text(**text)
            except TypeError:
                continue

            self.add(t)

    def convert_to_arr_of_dicts(self) -> List[Dict[str, str]]:
        """ Function convert Buffer to dict """
        return [text.__dict__ for text in self.data]

    def print_buffer(self) -> None:
        """ The function shows all data"""
        if self.data:
            print(f"{'idx':<4}| {'text':<100}| {'rot_type':<10}| {'status':<15}")
            for idx, text in enumerate(self.data, start=1):
                print(f"{idx:<4}  {shorten(text.text, width=100):<100}  {text.rot_type:<10}  {text.status:<15}")
            print()
        else:
            print("Buffer is empty.\n")

