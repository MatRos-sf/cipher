from typing import Union, Tuple

from menu.menu import Menu


class Cipher:
    def __init__(self):
        self.menu = Menu()
        self._run = True

    def run(self) -> None:
        # self.menu.load_buffers()
        while self._run:
            self.menu.show()
            response, task = self.response()
            if response:
                if not task and self.menu.is_exit(response):
                    self._run = False

    def response(self) -> Union[Tuple[None, None], Tuple[int, None], Tuple[int, dict]]:
        try:
            user_response = int(input("> "))
        except ValueError:
            print("This option is unavailable!\n")
        else:
            return user_response, self.menu.execute(user_response)

        return None, None

