import pytest
from unittest.mock import patch, call

from src.manager import FileHandler

@pytest.fixture
def get_sample_json_file():
    json_file = [
            {
            "text": "Vgv hv fjov",
            "rot_type": "rot47",
            "status": "encrypted"
        },
        {
            "text": "Nyn zn xbgn5",
            "rot_type": "rot13",
            "status": "encrypted"
        }
    ]

    return json_file


class TestFileHandler:

    @pytest.mark.parametrize("file_name, expected", [("", None), ("  ", None), ("    ", None)])
    def test_property_when_namefile_is_empty_expect_namefile_empty(self, file_name, expected):

        file_handler = FileHandler()
        file_handler.name_file = file_name

        assert not file_handler.name_file

    @pytest.mark.parametrize("file_name, expected", [("test", "test.json"), (" test ", "test.json"), ("    test.json", "test.json")])
    def test_property_when_set_namefile_expect_namefile_should_be_set(self, file_name, expected):

        file_handler = FileHandler()
        file_handler.name_file = file_name

        assert file_handler.name_file

    def test_get_file_name_from_user_valid_input(self, mocker):

        mocker.patch("src.manager.manager_file.input", return_value="name_file")

        fh = FileHandler()
        fh.get_file_name_from_user()

        assert fh.name_file == "name_file.json"

    #?????
    #input False
    #print call False
    def test_get_file_name_from_user_invalid_input(self, mocker):

        mocker.patch("src.manager.manager_file.input", return_value="")

        fh = FileHandler()
        fh.get_file_name_from_user()

        assert not fh.name_file

    def test_get_file_name_from_user_should_call_information(self):
        with patch('builtins.input') as mock:
            FileHandler().get_file_name_from_user()

        mock.assert_has_calls([
            call("Type the file name and press enter.\n>")
        ])

    # czy tworzyć nowy katalog z jakimś przykładem kóry by otwierał
    def test_open_should_open_file_when_file_exist(self, mocker, get_sample_json_file):
        mocker.patch("src.manager.manager_file.open", return_value=get_sample_json_file)
        mocker.patch("json.load", return_value=get_sample_json_file)
        fh = FileHandler()
        fh.name_file = "test"

        assert fh.content

    # save mam sprawdzić czy utworzył plik?
    def test_save(self):
        pass