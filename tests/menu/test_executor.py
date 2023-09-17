import pytest
from unittest.mock import patch, call, Mock
import sys
import json
from string import ascii_lowercase, ascii_uppercase

from src.menu.menu import Executor
from buffer import Text
from manager import FileHandler
from tests.manager.test_manager_file import get_sample_json_file, create_temp_directory
from tests.buffer.test_buffer import get_sample_text_obj


@pytest.fixture
def turn_off_output(capsys):
    return capsys.readouterr()


TEST_PASS_DATA = [
    ("grfg", "13", {"text": "test", "rot_type": "rot13", "status": "decrypted"}),
    ("", "13", {"text": "", "rot_type": "rot13", "status": "decrypted"}),
    ("ozno", "47", {"text": "test", "rot_type": "rot47", "status": "decrypted"}),
]

TEST_DECRYPT_FAIL_DATA = [
    ("grfg", "", None),
    ("", "13a", None),
    ("ozno", "-47", None),
    ("test", "14", None),
    ("test", "48", None),
    ("", "", None),
]


TEST_LIST_PASS_DATA_DECRYPT = [
    ("grfg", "13", "test"),
    ("", "13", ""),
    ("a a" * 10, "13", "n n" * 10),
    ("nopqrstuvwxyzabcdefghijklm", "13", ascii_lowercase),
    ("ozno", "47", "test"),
    ("", "47", ""),
    ("a a." * 10, "47", "f f." * 10),
    ("VWXYZABCDEFGHIJKLMNOPQRSTU", "47", ascii_uppercase),
]
TEST_LIST_INVALID_DATA_DECRYPT = [
    ("a", "12"),
    ("", "14"),
    ("", "48"),
    ("", "46"),
    ("", "-15"),
    ("", "75522222"),
]


class TestExecutor:
    def test_when_call_executor_should_have_default_rot_type(self):
        executor = Executor()

        expected = [13, 47]
        actual = executor.caesar.rot_types

        assert expected == actual

    def test_encrypt_when_user_type_some_text_should_return_dict(self, capsys):
        executor = Executor()
        expected = {"text": "grfg", "rot_type": "rot13", "status": "encrypted"}
        input_text_to_encrypt = "test"
        input_chose_type = "13"

        with patch(
            "builtins.input", side_effect=[input_text_to_encrypt, input_chose_type]
        ):
            text = executor.encrypt()

        captured = capsys.readouterr()

        assert text == expected

    def test_encrypt_when_user_type_some_text_should_add_new_buffer(self, capsys):
        executor = Executor()
        input_text_to_encrypt = "test"
        input_chose_type = "13"
        expected = 1

        with patch(
            "builtins.input", side_effect=[input_text_to_encrypt, input_chose_type]
        ):
            executor.encrypt()

        buffer_data = executor.buffer.data

        captured = capsys.readouterr()

        assert len(buffer_data) == expected

    def test_encrypt_when_user_type_empty_text_should_return_dict(self, capsys):
        executor = Executor()
        input_text_to_encrypt = ""
        input_chose_type = "47"
        expected = {"text": "", "rot_type": "rot47", "status": "encrypted"}

        with patch(
            "builtins.input", side_effect=[input_text_to_encrypt, input_chose_type]
        ):
            result = executor.encrypt()

        capsys.readouterr()

        assert result == expected

    def test_encrypt_when_user_type_wrong_rot_type_should_return_none(self, capsys):
        executor = Executor()
        input_text_to_encrypt = ""
        input_chose_type = "99"

        with patch(
            "builtins.input", side_effect=[input_text_to_encrypt, input_chose_type]
        ):
            result = executor.encrypt()

        capsys.readouterr()
        assert not result

    def test_encrypt_when_user_not_type_rot_type_should_return_none(self, capsys):
        executor = Executor()
        input_text_to_encrypt = ""
        input_chose_type = ""

        with patch(
            "builtins.input", side_effect=[input_text_to_encrypt, input_chose_type]
        ):
            result = executor.encrypt()

        capsys.readouterr()

        assert not result

    def test_encrypt_when_user_type_right_data_should_call_info(self, mocker):
        executor = Executor()
        input_text_to_encrypt = "test"
        input_chose_type = "13"

        mock_print = Mock()

        with patch(
            "builtins.input", side_effect=[input_text_to_encrypt, input_chose_type]
        ), patch("builtins.print", new=mock_print):
            result = executor.encrypt()

        expected_calls = [
            call("Which type do you want to use? "),
            call(*executor.caesar.rot_types, sep="\n"),
            call(Text(**result), "Text is in the clipboard.", sep="\n"),
        ]

        mock_print.assert_has_calls(expected_calls)

    def test_encrypt_when_user_type_invalid_rot_type_should_call_info(self, mocker):
        executor = Executor()
        input_text_to_encrypt = "test"
        input_chose_type = "a"

        mock_print = Mock()

        with patch(
            "builtins.input", side_effect=[input_text_to_encrypt, input_chose_type]
        ), patch("builtins.print", new=mock_print):
            result = executor.encrypt()

        expected_calls = [
            call("Which type do you want to use? "),
            call(*executor.caesar.rot_types, sep="\n"),
            call("I'm sorry this type is unavailable.\n"),
        ]

        mock_print.assert_has_calls(expected_calls)

    def test_encrypt_when_user_type_unavailable_rot_type_should_call_info(self, mocker):
        executor = Executor()
        input_text_to_encrypt = "test"
        input_chose_type = "55"

        mock_print = Mock()

        with patch(
            "builtins.input", side_effect=[input_text_to_encrypt, input_chose_type]
        ), patch("builtins.print", new=mock_print):
            result = executor.encrypt()

        expected_calls = [
            call("Which type do you want to use? "),
            call(*executor.caesar.rot_types, sep="\n"),
            call("I'm sorry this type is unavailable.\n"),
        ]

        mock_print.assert_has_calls(expected_calls)

    @pytest.mark.parametrize("text, rot_typ, expected", TEST_PASS_DATA)
    def test_decrypt_when_user_type_some_text_should_return_dict(
        self, text, rot_typ, expected, capsys
    ):
        executor = Executor()
        input_text_to_encrypt = text
        input_chose_type = rot_typ

        with patch(
            "builtins.input", side_effect=[input_text_to_encrypt, input_chose_type]
        ):
            text = executor.decrypt()

        capsys.readouterr()
        assert text == expected

    @pytest.mark.parametrize("text, rot_type, expected", TEST_DECRYPT_FAIL_DATA)
    def test_decrypt_when_user_type_invalid_data_should_return_dict(
        self, text, rot_type, expected, capsys
    ):
        executor = Executor()
        input_text_to_encrypt = text
        input_chose_type = rot_type

        with patch(
            "builtins.input", side_effect=[input_text_to_encrypt, input_chose_type]
        ):
            result = executor.encrypt()

        capsys.readouterr()

        assert result == expected

    @pytest.mark.parametrize(
        "input_text, input_type, expected_text", TEST_LIST_PASS_DATA_DECRYPT
    )
    def test_decrypt_when_user_type_right_data_should_call_info(
        self, input_text, input_type, expected_text, mocker, capsys
    ):
        executor = Executor()
        input_text_to_encrypt = input_text
        input_chose_type = input_type
        decrypt_text = expected_text
        expected = Text(decrypt_text, f"rot{str(input_chose_type)}", "decrypted")

        mock_print = Mock()
        mocker.patch("src.menu.menu.Buffer.add", return_value="")

        with patch(
            "builtins.input", side_effect=[input_text_to_encrypt, input_chose_type]
        ), patch("builtins.print", new=mock_print):
            executor.decrypt()

        expected_calls = [
            call("Which type do you want to use? "),
            call(*executor.caesar.rot_types, sep="\n"),
            call(expected, "\n"),
        ]

        mock_print.assert_has_calls(expected_calls)
        capsys.readouterr()

    @pytest.mark.parametrize("input_text, input_type", TEST_LIST_INVALID_DATA_DECRYPT)
    def test_decrypt_when_user_type_invalid_data_should_call_info(
        self, input_text, input_type
    ):
        executor = Executor()
        input_text_to_encrypt = input_text
        input_chose_type = input_type

        mock_print = Mock()

        with patch(
            "builtins.input", side_effect=[input_text_to_encrypt, input_chose_type]
        ), patch("builtins.print", new=mock_print):
            executor.decrypt()

        expected_calls = [
            call("Which type do you want to use? "),
            call(*executor.caesar.rot_types, sep="\n"),
            call("I'm sorry this type is unavailable."),
        ]

        mock_print.assert_has_calls(expected_calls)

    def test_load_file_when_data_correct_should_set_buffer(
        self, mocker, get_sample_json_file
    ):
        executor = Executor()

        mocker.patch("builtins.input", return_value="test")
        mocker.patch(
            "src.menu.menu.FileHandler.open", return_value=get_sample_json_file
        )

        executor.load_file()

        assert executor.buffer.data

    @pytest.mark.parametrize("load_data", [([]), ([{"test": None}]), ("")])
    def test_load_file_when_data_incorrect_should_not_set_buffer(
        self, load_data, mocker
    ):
        executor = Executor()

        mocker.patch("builtins.input", return_value="test")
        mocker.patch("src.menu.menu.FileHandler.open", return_value=load_data)

        executor.load_file()

        assert not executor.buffer.data

    def test_load_file_when_data_correct_should_set_buffer_and_print_info(
        self, mocker, get_sample_json_file
    ):
        executor = Executor()

        mocker.patch("builtins.input", return_value="test")
        mocker.patch(
            "src.menu.menu.FileHandler.open", return_value=get_sample_json_file
        )
        with patch("builtins.print") as mock:
            executor.load_file()

        mock.assert_has_calls([call("Loaded:", *get_sample_json_file, sep="\n")])

    @pytest.mark.parametrize(
        "answer_user", [("Yes"), ("yes"), ("y"), ("ab2"), ("o"), ("n")]
    )
    def test_save_to_file_should_save_to_exist_file(
        self,
        answer_user,
        mocker,
        tmp_path,
        create_temp_directory,
        get_sample_json_file,
        capsys,
    ):
        executor = Executor()
        executor.file_handler.name_file = "test.json"
        expected = get_sample_json_file

        mocker.patch(
            "src.menu.menu.Buffer.convert_to_arr_of_dicts", return_value=expected
        )
        mocker.patch.object(FileHandler, "DIR_PATH", create_temp_directory)
        mocker.patch("builtins.input", return_value=answer_user)

        d = create_temp_directory
        f = d / "test.json"
        f.write_text("Hello")

        executor.save_to_file()
        capsys.readouterr()

        assert f.read_text() == json.dumps(expected, indent=4)

    @pytest.mark.parametrize("answer_user", [("no"), ("No"), ("NO"), ("nO")])
    def test_save_to_file_should_save_to_new_file(
        self, answer_user, mocker, tmp_path, get_sample_json_file, capsys
    ):
        executor = Executor()
        executor.file_handler.name_file = "test.json"
        expected = get_sample_json_file

        d = tmp_path / "test"
        d.mkdir()

        mocker.patch(
            "src.menu.menu.Buffer.convert_to_arr_of_dicts", return_value=expected
        )
        mocker.patch.object(FileHandler, "DIR_PATH", d)

        with patch("builtins.input", side_effect=[answer_user, "new_test.json"]):
            executor.save_to_file()

        created_file = d / "new_test.json"

        capsys.readouterr()

        assert len(list(d.iterdir())) == 1
        assert created_file.read_text() == json.dumps(expected, indent=4)

    def test_print_buffer_when_buffer_empty_then_call_info(self):
        executor = Executor()

        with patch("builtins.print") as mock:
            executor.print_buffer()

        mock.assert_has_calls([call("History is empty!")])

    def test_print_buffer_when_buffer_is_then_call_mock_info(
        self, mocker, get_sample_text_obj
    ):
        mocker.patch("src.menu.menu.Buffer.print_buffer")

        executor = Executor()
        executor.buffer.data = [get_sample_text_obj]

        with patch("builtins.print") as mock:
            executor.print_buffer()
        mock.assert_not_called()
