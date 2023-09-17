import pytest
from unittest.mock import patch

from src.cipher.cipher import Cipher


@pytest.fixture
def mock_executor_without_exit(mocker):
    mocker.patch("src.cipher.cipher.Menu.execute", return_value={"t": "test"})


class TestCipher:
    def test_constructor_when_call_obj_should_set_attributes(self):
        cipher = Cipher()

        assert cipher.menu
        assert cipher._run

    @pytest.mark.parametrize("value", ["a", "f", "o"])
    def test_response_when_user_response_is_invalid_then_should_return_tuple_of_none(
        self, value, mocker, capsys
    ):
        cipher = Cipher()
        expected = (None, None)
        mocker.patch("builtins.input", return_value=value)

        result = cipher.response()

        capsys.readouterr()

        assert result == expected

    @pytest.mark.parametrize("value", [1, 2])
    def test_some_when_user_response_is_1_or_2_then_should_execute_func(
        self, value, mocker
    ):
        mocker.patch("src.cipher.cipher.Menu.execute", return_value={"t": "test"})
        mocker.patch("builtins.input", return_value=value)

        cipher = Cipher()

        actual = cipher.response()

        assert isinstance(actual[0], int)
        assert isinstance(actual[1], dict)

    @pytest.mark.parametrize("value", [3, 4, 5, 6])
    def test_some_when_user_response_is_from_3_to_6_then_should_execute_and_return_int_and_none(
        self, value, mocker
    ):
        mocker.patch("src.cipher.cipher.Menu.execute", return_value=None)
        mocker.patch("builtins.input", return_value=value)

        cipher = Cipher()

        actual = cipher.response()

        assert isinstance(actual[0], int)
        assert not actual[1]

    def test_run_when_user_type_exit(self, mocker, capsys):
        mocker.patch("src.cipher.cipher.Cipher.response", return_value=(True, False))
        mocker.patch("src.cipher.cipher.Menu.is_exit", return_value=True)

        cipher = Cipher()
        cipher.run()

        capsys.readouterr()

        assert not cipher._run

    def test_run_when_user_type_exit_should_call_info(self, mocker, capsys):
        mocker.patch("src.cipher.cipher.Cipher.response", return_value=(True, False))
        mocker.patch("src.cipher.cipher.Menu.is_exit", return_value=True)
        mocker.patch("src.cipher.cipher.Menu.show", return_value=None)

        with patch("builtins.print") as mock:
            cipher = Cipher()
            cipher.run()

        calls = mock.call_count
        assert calls == 2

    def test_bandit(self):
        pass
