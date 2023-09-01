class Cipher:
    def __init__(self):
        self.menu = Menu()
        self._run = True
    def run(self):

        while self._run:
            self.menu.show()