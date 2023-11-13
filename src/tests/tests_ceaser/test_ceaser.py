from string import ascii_uppercase

import pytest

from ceaser import ceaser


class TestCaesarCipher:
    def test_check_constant_alpha(self):
        assert ceaser.ALPHA_UPPER[0] == "A"
        assert ceaser.ALPHA_UPPER[-1] == "Z"
        assert ceaser.LEN_ALPHA == 26

    def test_check_constant_digits(self):
        assert ceaser.DIGITS[0] == "0"
        assert ceaser.DIGITS[-1] == "9"
        assert ceaser.LEN_DIGITS == 10

    def test_should_set_rot_type_when_correct_value(self):
        exc = [25, 16]
        base = [25, 16]

        c = ceaser.CaesarCipher(base)

        assert c.rot_types == exc

    def test_should_not_set_rot_type_when_list_of_str(self):
        base = ["t", "e"]

        c = ceaser.CaesarCipher(base)
        assert c.rot_types == []

    def test_change_lower_letter_in_right(self):
        c = ceaser.CaesarCipher([1])

        base = "a"
        exp = "b"

        response = c.change_letter(base, 1, False)

        assert response == exp

    def test_change_upper_letter_in_right(self):
        c = ceaser.CaesarCipher([1])

        base = "A"
        exp = "B"

        response = c.change_letter(base, 1, False)

        assert response == exp

    def test_change_upper_letter_in_left(self):
        c = ceaser.CaesarCipher([1])

        base = "A"
        exp = "Z"
        num_rot = -1
        response = c.change_letter(base, num_rot, False)

        assert response == exp

    def test_change_lower_letter_in_left(self):
        c = ceaser.CaesarCipher([1])

        base = "a"
        exp = "z"
        num_rot = -1
        response = c.change_letter(base, num_rot, False)

        assert response == exp

    def test_change_num_in_left(self):
        c = ceaser.CaesarCipher([1])

        base = "1"
        exp = "0"
        num_rot = -1
        response = c.change_letter(base, num_rot, True)

        assert response == exp

    def test_change_num_in_right(self):
        c = ceaser.CaesarCipher([1])

        base = "1"
        exp = "2"
        num_rot = 1
        response = c.change_letter(base, num_rot, True)

        assert response == exp

    def test_encode_should_return_rot_47(self):
        c = ceaser.CaesarCipher([47])

        base = "Test"
        base_status = "test_enc"
        exp = "Ozno"
        response = c.code_encoder_decoder(base, 47, base_status)

        assert response["text"] == exp
        assert response["rot_type"] == "rot47"
        assert response["status"] == base_status

    def test_encode_should_return_rot_13(self):
        c = ceaser.CaesarCipher([13])

        base = "Test"
        base_status = "test_enc"
        exp = "Grfg"
        response = c.code_encoder_decoder(base, 13, base_status)

        assert response["text"] == exp
        assert response["rot_type"] == "rot13"
        assert response["status"] == base_status
        assert isinstance(response, dict)

    def test_encode_should_return_rot_47_new(self):
        c = ceaser.CaesarCipher([13])

        base = ascii_uppercase
        base_status = "test_enc"
        exp = "nopqrstuvwxyzabcdefghijklm".upper()
        response = c.code_encoder_decoder(base, 13, base_status)

        assert response["text"] == exp
        assert response["rot_type"] == "rot13"
        assert response["status"] == base_status
