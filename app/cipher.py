import time

from menu.menu import Menu


class Cipher:
    def __init__(self):
        self.menu = Menu()
        self._run = True
        #self.buffer = []

    def run(self):
        self.menu.load_buffers()
        while self._run:
            self.menu.show()
            response, task = self.response()
            if response:
                if not task:
                    self._run = False


    def response(self) -> tuple:
        try:
            user_response = int(input("> "))
        except ValueError:
            print("This option is unavailable!")
        else:
            return user_response, self.menu.options.get(user_response, "Error")[1]()

        return ()

