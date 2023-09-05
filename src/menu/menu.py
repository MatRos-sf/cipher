from functools import partial
from typing import Dict, Tuple, Union

from ceaser import CaesarCipher
from buffer import Buffer, Text
from manager import FileHandler

class Executor:
    def __init__(self):
        self.caesar = CaesarCipher([13, 47])
        self.buffer = Buffer()
        self.file_handler = FileHandler()

    def encrypt(self) -> Dict[str, str] | None:
        text_to_encrypt = input("Write text to encrypt\n>")
        print("Which type do you want to use? ")
        print(*self.caesar.rot_types, sep='\n')

        try:
            chose_type = int(input("> "))
        except TypeError:
            print("I'm sorry this type is unavailable.\n\n")
            return

        if chose_type not in self.caesar.rot_types or chose_type < 0:
            print("I'm sorry this type is unavailable.\n\n")
            return

        encrypt_text = self.caesar.code_encoder_decoder(text_to_encrypt, chose_type, 'encrypted')

        self.buffer.add(Text(**encrypt_text))

        return encrypt_text

    def decrypt(self) -> Dict[str, str] | None:
        text_to_encrypt = input("Write text to decrypt\n>")
        print("Which type do you want to use? ")
        print(*self.caesar.rot_types, sep='\n')

        try:
            chose_type = int(input("> "))
        except TypeError:
            print("I'm sorry this type is unavailable.\n\n")
            return

        if chose_type not in self.caesar.rot_types or chose_type < 0:
            print("I'm sorry this type is unavailable.\n\n")
            return

        encrypt_text = self.caesar.code_encoder_decoder(text_to_encrypt, -chose_type, 'decrypted')

        self.buffer.add(Text(**encrypt_text))

        return encrypt_text

    def check_changes(self) -> bool:
        """Function checks changes in read file and buffer"""
        return self.buffer.convert_to_arr_of_dicts() == self.file_handler.content

    def exit(self) -> None:
        if not self.check_changes():
            self.buffer_save()
        return

    def buffer_save(self) -> None:
        response = input("Do you want save all actions? [yes/no]\n> ")
        if response.upper() == "YES":
            self.read_file.save(self.buffer.convert_to_arr_of_dicts())

    def load_file(self):
        name_file = input("Please, enter the file name:\n> ")
        self.file_handler.name_file = name_file

        content = self.file_handler.open()
        self.buffer.add_list_of_dict(content)

    def save_to_file(self):

        if not self.file_handler.name_file:
            name_file = input("Please, enter the name of the file\n> ")
            self.file_handler.name_file = name_file
        else:
            name_file = input(f"Do you want to append content to: {self.file_handler.name_file}?[yes/no]\n> ")
            if name_file.upper() == "NO":
                name_file = input("Please, enter the name of the file\n> ")
                self.file_handler.name_file = name_file

        self.file_handler.save(self.buffer.convert_to_arr_of_dicts())
        print("Saved. \n")

class Menu:
    def __init__(self) -> None:
        self.executor = Executor()
        self.options: Dict[int, Tuple[str, partial]] = {
            1: ("Encryption", partial(self.executor.encrypt)),
            2: ("Decryption", partial(self.executor.decrypt)),
            3: ("Load file", partial(self.executor.load_file)),
            4: ("Save", partial(self.executor.save_to_file)),
            5: ("Exit", partial(self.executor.exit))
        }

    def show(self) -> None:
        self.executor.buffer.print_buffer()
        menu = [f"{key}: {value[0]}" for key, value in self.options.items()]
        print(*menu, sep='\n')

    def execute(self, choice: int):
        exe = self.options.get(choice)
        if not exe:
            self.__show_error()
            return
        return exe[1]()

    def __show_error(self) -> None:
        """ Function informs user about wrong choice."""
        print("This option doesn't exist.\n")
        return

    def is_exit(self, key: int):
        check_exit = self.options.get(key, None)
        return check_exit and check_exit[0] == 'Exit'

