class CaesarCipher:
    alpha_upper = list('AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUWYZŹŻ')
    size_alpha = len(alpha_upper)

    def __init__(self, text: str) -> None:
        self.text = text.upper()

    @property
    def encrypt(self):
        text_rot13: str = ""
        for letter in self.text:
            if letter.isalpha():
                new_letter = self.change_letter(letter, 13)
                text_rot13 += new_letter
            else:
                text_rot13 += letter

        return text_rot13

    @staticmethod
    def change_letter(letter: str, num_rot: int) -> str:

        index = CaesarCipher.alpha_upper.index(letter)
        new_index = index + num_rot

        if new_index < CaesarCipher.size_alpha:
            return CaesarCipher.alpha_upper[new_index]

        return CaesarCipher.alpha_upper[new_index % CaesarCipher.size_alpha]




