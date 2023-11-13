from typing import Union, Tuple

from menu.menu import Menu


class Cipher:
    def __init__(self):
        self.menu: Menu = Menu()
        self._run: bool = True

    def run(self) -> None:
        """Main method who run whole app."""
        print("Welcome to the Caesar tests_cipher app's.")
        while self._run:
            self.menu.show()
            response, result = self.response()

            if response:
                if not result and self.menu.is_exit(response):
                    self._run = False
                    print("See you soon.")

    def response(self) -> Union[Tuple[None, None], Tuple[int, None], Tuple[int, dict]]:
        """
        The method that waits for user input and check its.There are three ways to return this function :
            [None, None] If the user selects the wrong type in the tests_menu
            [int, None] If the user selects correct type but something was wrong e.x. this option doesn't exist
            [int, dict] If everything is ok
        """

        try:
            user_response = int(input("> "))
        except ValueError:
            print("This option is unavailable!\n")
        else:
            return user_response, self.menu.execute(user_response)

        return None, None
