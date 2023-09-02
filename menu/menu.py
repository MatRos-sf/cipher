from typing import Dict, Tuple,List
from functools import partial


class Executor:

    def encrypt(self):
        code = input("Write text to encrypt\n>")
        return "BLabla"

    def exit(self):
        return

class Menu:

    def __init__(self):
        self.executor = Executor()
        #self.options: Dict[int, Tuple[str, Executor]]
        self.options = {
            1: ("Encryption", partial(self.executor.encrypt)),
            2: ("Exit", partial(self.executor.exit))
        }

    def show(self):

        menu = [f"{key}: {value[0]}" for key, value in self.options.items()]
        print("\n".join(menu))

    def response_menu(self):
        key: List[int] = [k for k in self.options.keys()]
        try:
            user_response = input('> ')
        except ValueError:
            print("This option is unavailable!")
        else:
            self.execute(user_response)
    def execute(self, choice: int) -> None:
        a = self.options.get(choice, self.show_error)
        print(a[0])



    def show_error(self):
        print('Error')

