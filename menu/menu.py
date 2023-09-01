class Executor:
    pass


class Menu:

    def __init__(self):
        self.executor = Executor()
        self.options = {
            1: "Encryption",
            2: "Decrypting",
            3: "Exit"
        }

    def show_menu(self):

        menu = [f"{key}: {value}" for key, value in self.options.items()]
        choice = input("\n".join(menu))
        print(choice)

    def execute(self, choice: int) -> None:
        #self.executor.get(choice, self.show_error)()

    def show_error(self):
        print()

