import string
from typing import List, Optional, Dict

ALPHA_UPPER: List[str] = list(string.ascii_uppercase)
DIGITS: List[str] = list(string.digits)
LEN_DIGITS = len(DIGITS)
LEN_ALPHA = len(ALPHA_UPPER)


class CaesarCipher:
    def __init__(self, rot_types: List[int]):
        if all(isinstance(i, int) for i in rot_types):
            self._rot_types = rot_types
        else:
            self._rot_types = []

    @property
    def rot_types(self):
        return self._rot_types

    @rot_types.setter
    def rot_types(self, value: int) -> None:
        if value not in self.rot_types and isinstance(value, int):
            self._rot_types.append(value)

    @staticmethod
    def change_letter(letter: str, num_rot: int, is_digit: bool = False) -> str:
        """The method change letter according to Caesar tests_cipher rule."""
        index = (
            ALPHA_UPPER.index(letter.upper()) if not is_digit else DIGITS.index(letter)
        )
        new_index = index + num_rot

        if not is_digit and 0 < new_index < LEN_ALPHA:
            new_letter = ALPHA_UPPER[new_index]
            return new_letter if letter.isupper() else new_letter.lower()

        elif is_digit and 0 < new_index < LEN_DIGITS:
            return DIGITS[new_index]

        elif is_digit:
            return DIGITS[new_index % LEN_DIGITS]

        new_letter = ALPHA_UPPER[new_index % LEN_ALPHA]
        return new_letter if letter.isupper() else new_letter.lower()

    def code_encoder_decoder(
        self, text: str, rot_type: int, status: str
    ) -> Dict[str, str]:
        """The method encode/ decode some text."""
        new_text: str = ""
        for letter in text:
            if letter.isdigit():
                new_letter = self.change_letter(letter, rot_type, True)
                new_text += new_letter
            elif letter.isalpha():
                new_letter = self.change_letter(letter, rot_type)
                new_text += new_letter
            else:
                new_text += letter

        data = {
            "text": new_text,
            "rot_type": "rot"
            + (str(-rot_type) if status == "decrypted" else str(rot_type)),
            "status": status,
        }
        return data
