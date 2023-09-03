from functools import partial

from ceaser import CaesarCipher
from buffer import Buffer, Text
from manager import FileHandler

class Executor:
    def __init__(self):
        self.caesar = CaesarCipher()
        self.buffer = Buffer()
        # self.buffers: List[Buffer] = []
        self.file_handler = FileHandler()

    def encrypt(self):
        text_to_encrypt = input("Write text to encrypt\n>")

        self.caesar.text = text_to_encrypt
        encrypt_text = self.caesar.encrypt

        self.buffer.add(Text(**encrypt_text))

        return encrypt_text

    def decrypt(self):
        text_to_encrypt = input("Write text to decrypt\n>")

        self.caesar.text = text_to_encrypt
        decrypt_text = self.caesar.decrypt

        self.buffer.add(Text(**decrypt_text))

        return decrypt_text

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


class Menu:
    def __init__(self) -> None:
        self.executor = Executor()
        self.options = {
            1: ("Encryption", partial(self.executor.encrypt)),
            2: ("Decryption", partial(self.executor.decrypt)),
            3: ("Exit", partial(self.executor.exit))
        }

    def show(self) -> None:
        self.executor.buffer.print_buffer()
        menu = [f"{key}: {value[0]}" for key, value in self.options.items()]
        print(*menu, sep='\n')

    def execute(self, choice: int) -> None:
        self.options.get(choice, self.__show_error)
        print()

    def __show_error(self):
        print('Error')

    # def load_buffers(self) -> None:
    #     response = input("Do you want load file?[yes/no]\n>  ")
    #     if response.upper() == 'YES':
    #         buffers = self.executor.read_file.open()
    #         if buffers:
    #             self.executor.add_to_buffers(buffers)
