from typing import Dict, Tuple, List
from functools import partial

from app.caesar import CaesarCipher
from app.buffer import Buffer
from app.manager_file import FileHandler


class Executor:
    def __init__(self):
        self.caesar = CaesarCipher()
        self.buffers: List[Buffer] = []
        self.read_file = FileHandler()

    def encrypt(self):
        text_to_encrypt = input("Write text to encrypt\n>")

        self.caesar.text = text_to_encrypt
        encrypt_text = self.caesar.encrypt

        self.buffers.append(Buffer(**encrypt_text))

        return encrypt_text

    def decrypt(self):
        text_to_encrypt = input("Write text to decrypt\n>")

        self.caesar.text = text_to_encrypt
        decrypt_text = self.caesar.decrypt

        self.buffers.append(Buffer(**decrypt_text))

        return decrypt_text

    def check_changes(self) -> bool:
        """Function checks changes in read file and buffer"""
        if self.convert_buffers() == self.read_file.content:
            return True
        return False
    def exit(self) -> None:
        if not self.check_changes():
            self.buffer_save()
        return

    def buffer_save(self) -> None:
        response = input("Do you want save all actions? [yes/no]\n> ")
        if response.upper() == "YES":
            self.read_file.save(self.convert_buffers())

    def convert_buffers(self) -> List[Dict[str, str]]:
        """ Function convert Buffer to dict """
        return [buffer.__dict__ for buffer in self.buffers]

    def add_to_buffers(self, buffers: List[dict]):

        for buffer in buffers:
            self.buffers.append(Buffer(**buffer))


class Menu:

    def __init__(self) -> None:
        self.executor = Executor()
        #self.options: Dict[int, Tuple[str, Executor]]
        self.options = {
            1: ("Encryption", partial(self.executor.encrypt)),
            2: ("Decryption", partial(self.executor.decrypt)),
            3: ("Exit", partial(self.executor.exit))
        }

    def show(self) -> None:
        self.show_buffers()
        menu = [f"{key}: {value[0]}" for key, value in self.options.items()]
        print("\n".join(menu))

    def execute(self, choice: int) -> None:
        self.options.get(choice, self.show_error)
        print()

    def show_buffers(self):
        for buffer in self.executor.buffers:
            print(buffer)

    def show_error(self):
        print('Error')

    def load_buffers(self) -> None:
        response = input("Do you want load file?[yes/no]\n>  ")
        if response.upper() == 'YES':
            buffers = self.executor.read_file.open()
            self.executor.add_to_buffers(buffers)
