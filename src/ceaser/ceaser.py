import string
from typing import List

ALPHA_UPPER = list(string.ascii_uppercase)
DIGITS = list(string.digits)
LEN_DIGITS = len(DIGITS)
LEN_ALPHA = len(ALPHA_UPPER)


class CaesarCipher:
    alpha_upper = list(string.ascii_uppercase)
    size_alpha = len(alpha_upper)

    def __init__(self, rot_types: List[int]):
        self._rot_types = rot_types

    @property
    def rot_types(self):
        return self._rot_types

    @staticmethod
    def change_letter(letter: str, num_rot: int, is_digit: bool = False) -> str:

        index = ALPHA_UPPER.index(letter.upper()) if not is_digit else DIGITS.index(letter)
        new_index = index + num_rot

        if not is_digit and new_index > 0 and new_index < LEN_ALPHA:
            new_letter = ALPHA_UPPER[new_index]
            return new_letter if letter.isupper() else new_letter.lower()

        elif is_digit and new_index > 0 and new_index < LEN_DIGITS:
            return DIGITS[new_index]

        elif is_digit:
            return DIGITS[new_index % LEN_DIGITS ]

        new_letter = ALPHA_UPPER[new_index % LEN_ALPHA]
        return new_letter if letter.isupper() else new_letter.lower()


    def code_encoder_decoder(self, text: str, rot_type: int, status: str) -> dict:

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
            "rot_type": "rot" + (str(-rot_type) if status == 'decrypted' else str(rot_type)),
            "status": status
        }
        return data
