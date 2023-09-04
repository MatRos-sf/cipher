import json
import string
from typing import List


class CaesarCipher:
    alpha_upper = list(string.ascii_uppercase)
    size_alpha = len(alpha_upper)

    def __init__(self, rot_types: List[int]):
        self._rot_types = rot_types

    @property
    def rot_type(self):
        return self._rot_types


    def encrypt(self, text):
        text_rot13: str = ""
        for letter in text:
            if letter.isalpha():
                new_letter = self.change_letter(letter.upper(), 13)
                text_rot13 += new_letter
            else:
                text_rot13 += letter

        data = {
            "text": text_rot13,
            "rot_type": "rot13",
            "status": "encrypted"
        }
        return data

    @property
    def decrypt(self):
        text_rot13_decrypt: str = ""
        for letter in self.text:
            if letter.isalpha():
                new_letter = self.change_letter(letter.upper(), -13)
                text_rot13_decrypt += new_letter
            else:
                text_rot13_decrypt += letter

        data = {
            "text": text_rot13_decrypt,
            "rot_type": "rot13",
            "status": "decrypted"
        }
        return data

    @staticmethod
    def change_letter(letter: str, num_rot: int) -> str:

        index = CaesarCipher.alpha_upper.index(letter)
        new_index = index + num_rot

        if new_index > 0 and new_index < CaesarCipher.size_alpha:
            return CaesarCipher.alpha_upper[new_index]

        return CaesarCipher.alpha_upper[new_index % CaesarCipher.size_alpha]

    def code_encoder_decoder(self, text: str, rot_type: int, status: str) -> dict:

        new_text: str = ""
        for letter in text:
            if letter.isalpha():
                new_letter = self.change_letter(letter.upper(), rot_type)
                new_text += new_letter
            else:
                new_text += letter

        data = {
            "text": new_text,
            "rot_type": "rot" + str(rot_type),
            "status": status
        }
        return data
