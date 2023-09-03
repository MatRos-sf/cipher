import json
import string


class CaesarCipher:
    alpha_upper = list('AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUWYZŹŻ')
    size_alpha = len(alpha_upper)
    #
    # def __init__(self, value) -> None:
    #     self._text: str = value


    @property
    def encrypt(self):
        text_rot13: str = ""
        for letter in self._text:
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

    def cipher(self, rot_type: int, status: str) -> dict:

        if status == "decrypted":
            rot_type *= -1

        new_text: str = ""
        for letter in self.text:
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
