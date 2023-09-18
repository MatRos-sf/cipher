import pytest
from unittest.mock import patch, call
from random import randint


from menu.menu import Menu


class TestMenu:
    def test_constructor_should_set_when_call_object(self):
        menu = Menu()

        assert menu.executor
        assert menu.options
        assert isinstance(menu.options, dict)
        assert len(menu.options.get(1)) == 2

    def test_show_when_you_set_fake_options_should_print_fake_options(self):
        fake_options = {1: ("Fake_Encryption"), 2: ("Fake_Decryption")}

        menu = Menu()
        menu.options = fake_options
        expected = [f"{key}: {value[0]}" for key, value in fake_options.items()]

        with patch("builtins.print") as mock:
            menu.show()

        mock.assert_has_calls([call("\nMenu: "), call(*expected, sep="\n")])

    @pytest.mark.parametrize("option", [1, 2, 3, 4, 5, 6])
    def test_executor_when_user_chose_correct_options(self, option, mocker):
        def empty_fun():
            return True

        mocker.patch("menu.menu.partial", return_value=empty_fun)

        menu = Menu()
        expected = menu.execute(option)

        assert expected

    @pytest.mark.parametrize("option", [-1, 0, 7, "1", "2", 2321])
    def test_executor_when_user_chose_incorrect_options(self, option, mocker, capsys):
        def empty_fun():
            return True

        mocker.patch("menu.menu.partial", return_value=empty_fun)

        menu = Menu()
        expected = menu.execute(option)

        capsys.readouterr()
        assert not expected

    @pytest.mark.parametrize("option", [-1, 0, 7, "1", "2", 2321])
    def test_executor_when_user_chose_incorrect_options(self, option, mocker, capsys):
        def empty_fun():
            return True

        mocker.patch("menu.menu.partial", return_value=empty_fun)

        menu = Menu()
        expected = menu.execute(option)

        capsys.readouterr()
        assert not expected

    @pytest.mark.parametrize("option", [-1, 0, 7, "1", "2", 2321])
    def test_executor_when_user_chose_incorrect_options_should_call_info(
        self, option, mocker, capsys
    ):
        def empty_fun():
            return True

        mocker.patch("menu.menu.partial", return_value=empty_fun)

        with patch("builtins.print") as mock:
            menu = Menu()
            expected = menu.execute(option)

        mock.assert_has_calls([call("This option doesn't exist.\n")])

    @pytest.mark.parametrize("option", [1, 2, 3, 4, 5, 6])
    def test_executor_when_user_chose_correct_options_should_not_call(
        self, option, mocker
    ):
        def empty_fun():
            return True

        mocker.patch("menu.menu.partial", return_value=empty_fun)

        with patch("builtins.print") as mock:
            menu = Menu()
            expected = menu.execute(option)

        mock.assert_not_called()

    def test_is_exit_should_true_when_value_equal_exit(self):
        sample_option = {
            1: ("not_exit", None),
            2: ("not_exit", None),
            3: ("Exit", None),
        }

        menu = Menu()
        menu.options = sample_option

        assert menu.is_exit(3)

    @pytest.mark.parametrize("key", [-1, 4, 1, 2, "", randint(4, 100), "a", "z", None])
    def test_is_exit_should_false_when_value_is_not_exit_or_value_not_exist(self, key):
        sample_option = {
            1: ("not_exit", None),
            2: ("not_exit", None),
            3: ("Exit", None),
        }

        menu = Menu()
        menu.options = sample_option

        assert not menu.is_exit(key)
