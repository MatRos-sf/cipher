from src.buffer.buffer import Buffer
from src.buffer.text import Text

import pytest
from unittest.mock import patch, call
from textwrap import shorten


@pytest.fixture
def get_sample_text_obj():
    return Text("test", "rot47", "encoded")


@pytest.fixture
def get_dict_of_str():
    text = {"text": "test", "rot_type": "rot47", "status": "encoded"}
    return text


class TestBuffer:
    def test_add_should_add_text_when_correct_obj_text(self, get_sample_text_obj):
        text = get_sample_text_obj

        b = Buffer()
        b.add(text)

        assert b.data

    @pytest.mark.parametrize("text", [(1), ("")])
    def test_add_should_not_add_text_when_obj_is_different_type_than_text(self, text):
        b = Buffer()
        b.add(text)

        assert not b.data

    def test_add_list_of_dict_when_arg_is_valid(self, get_dict_of_str):
        arr_text = [get_dict_of_str, get_dict_of_str]

        b = Buffer()
        b.add_list_of_dict(arr_text)

        assert len(b.data) == 2

    @pytest.mark.parametrize(
        "arr", [([1, 2, 3]), (["t", "e", "s", "t"]), ([dict(), dict(), dict()])]
    )
    def test_add_list_of_dict_when_arg_is_invalid(self, arr):
        b = Buffer()
        b.add_list_of_dict(arr)

        assert not b.data

    def test_convert_to_arr_of_dict_should_return_list_of_dict_when_data_is_list_of_text(
        self, get_dict_of_str, get_sample_text_obj
    ):
        expected = [get_dict_of_str]

        b = Buffer()
        b.add(get_sample_text_obj)

        assert b.convert_to_arr_of_dicts() == expected

    def test_convert_to_arr_of_dict_should_return_empty_list_when_data_is_empty(self):
        b = Buffer()
        actual = b.convert_to_arr_of_dicts()

        assert not actual

    def test_print_buffer_should_print_info_when_data_is_empty(self):
        with patch("builtins.print") as mock:
            b = Buffer()
            b.print_buffer()

        mock.assert_has_calls([call("Buffer is empty.\n")])

    def test_print_buffer_should_print_all_buffer_when_buffer_is(
        self, mocker, get_sample_text_obj
    ):
        b = Buffer()

        mocker.patch.object(b, "data", [get_sample_text_obj])

        with patch("builtins.print") as mock:
            b.print_buffer()

        data = b.data[0]

        mock.assert_has_calls(
            [
                call(f"{'idx':<4}| {'text':<100}| {'rot_type':<10}| {'status':<15}"),
                call(
                    f"{'1':<4}  {shorten(data.text, width=100):<100}  {data.rot_type:<10}  {data.status:<15}"
                ),
                call(),
            ]
        )
