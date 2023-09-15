from functools import partial
from typing import Dict, Tuple, List, Union
import pyperclip

from ceaser import CaesarCipher
from buffer import Buffer, Text
from manager import FileHandler


class Executor:
    def __init__(self) -> None:
        self.caesar: CaesarCipher = CaesarCipher([13, 47])
        self.buffer: Buffer = Buffer()
        self.file_handler: FileHandler = FileHandler()

    def encrypt(self) -> Dict[str, str] | None:
        text_to_encrypt = input("Write text to encrypt\n> ")
        print("Which type do you want to use? ")
        print(*self.caesar.rot_types, sep='\n')

        try:
            chose_type = int(input("> "))
        except ValueError:
            print("I'm sorry this type is unavailable.\n")
            return

        if chose_type not in self.caesar.rot_types or chose_type < 0:
            print("I'm sorry this type is unavailable.\n")
            return

        encrypt_text = self.caesar.code_encoder_decoder(text_to_encrypt, chose_type, 'encrypted')

        text = Text(**encrypt_text)
        self.buffer.add(text)
        print(text, "Text is in the clipboard.", sep="\n")
        pyperclip.copy(text.text)

        return encrypt_text

    def decrypt(self) -> Dict[str, str] | None:
        text_to_encrypt = input("Write text to decrypt\n> ")
        print("Which type do you want to use? ")
        print(*self.caesar.rot_types, sep='\n')

        try:
            chose_type = int(input("> "))
        except ValueError:
            print("I'm sorry this type is unavailable.")
            return

        if chose_type not in self.caesar.rot_types or chose_type < 0:
            print("I'm sorry this type is unavailable.")
            return

        encrypt_text = self.caesar.code_encoder_decoder(text_to_encrypt, -chose_type, 'decrypted')

        text = Text(**encrypt_text)
        self.buffer.add(text)
        print(text, '\n')

        return encrypt_text

    def check_changes(self) -> bool:
        """Function checks changes in read file and buffer"""
        return self.buffer.convert_to_arr_of_dicts() == self.file_handler.content

    def exit(self) -> None:
        if not self.check_changes():
            pass
        return

    def load_file(self) -> None:

        self.file_handler._name_file = None

        if not self.file_handler.get_file_name_from_user():
            return

        content: List[Dict[str, str]] = self.file_handler.open()

        if content:
            self.buffer.add_list_of_dict(content)
            print("Loaded:", *content, sep='\n')

    def save_to_file(self) -> None:

        if self.file_handler.name_file:
            name_file = input(f"Do you want to append content to: {self.file_handler.name_file}?[yes/no]\n> ")
            if name_file.upper() == "NO":
                self.file_handler._name_file = None

        self.file_handler.save(self.buffer.convert_to_arr_of_dicts())

    def print_buffer(self) -> None:
        if not self.buffer.data:
            print("History is empty!")
            return
        self.buffer.print_buffer()


class Menu:
    def __init__(self) -> None:
        self.executor = Executor()
        self.options: Dict[int, Tuple[str, partial]] = {
            1: ("Encryption", partial(self.executor.encrypt)),
            2: ("Decryption", partial(self.executor.decrypt)),
            3: ("Load file", partial(self.executor.load_file)),
            4: ("Save", partial(self.executor.save_to_file)),
            5: ("History", partial(self.executor.print_buffer)),
            6: ("Exit", partial(self.executor.exit))
        }

    def show(self) -> None:
        """ The show displays menu."""
        menu = [f"{key}: {value[0]}" for key, value in self.options.items()]
        print("\nMenu: ")
        print(*menu, sep='\n')

    def execute(self, choice: int) -> Union[None | Dict[str, str]]:
        """
        The executor chooses what should be executed.
        If the 'choice' does not exist, an error message will be displayed, and None will be returned.
        """
        exe = self.options.get(choice)
        if not exe:
            self.__show_error()
            return
        return exe[1]()

    def __show_error(self) -> None:
        """ The method informs user about wrong choice."""
        print("This option doesn't exist.\n")
        return

    def is_exit(self, key: int) -> bool:
        """The method checks, if the value of the key is equal to 'Exit'"""
        check_exit = self.options.get(key, None)
        return check_exit and check_exit[0] == 'Exit'

