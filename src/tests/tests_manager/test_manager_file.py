import json
import pytest
from unittest.mock import patch, call

from manager import FileHandler


@pytest.fixture
def get_sample_json_file():
    json_file = [
        {"text": "Vgv hv fjov", "rot_type": "rot47", "status": "encrypted"},
        {"text": "Nyn zn xbgn5", "rot_type": "rot13", "status": "encrypted"},
    ]

    return json_file


@pytest.fixture
def create_temp_directory(tmp_path):
    d = tmp_path / "test"
    d.mkdir()

    return d


class TestFileHandler:
    @pytest.mark.parametrize("file_name", [(""), ("  "), ("    ")])
    def test_property_when_namefile_is_empty_expect_namefile_empty(self, file_name):
        file_handler = FileHandler()
        file_handler.name_file = file_name

        assert not file_handler.name_file

    @pytest.mark.parametrize(
        "file_name, expected",
        [
            ("test", "test.json"),
            (" test ", "test.json"),
            ("    test.json", "test.json"),
        ],
    )
    def test_property_when_set_namefile_expect_namefile_should_be_set(
        self, file_name, expected
    ):
        file_handler = FileHandler()
        file_handler.name_file = file_name

        assert file_handler.name_file

    def test_get_file_name_from_user_valid_input(self, mocker):
        mocker.patch("manager.manager_file.input", return_value="name_file")

        fh = FileHandler()
        actual = fh.get_file_name_from_user()

        assert fh.name_file == "name_file.json"
        assert actual

    def test_get_file_name_from_user_invalid_input(self, mocker, capsys):
        mocker.patch("builtins.input", return_value="")

        fh = FileHandler()
        actual = fh.get_file_name_from_user()

        capsys.readouterr()
        assert not actual

    def test_open_file_when_file_exist(self, mocker, tmp_path, get_sample_json_file):
        expect = json.dumps(get_sample_json_file)

        d = tmp_path / "test"
        d.mkdir()

        p = d / "test.json"
        p.write_text(expect)

        fh = FileHandler()
        fh.name_file = "test.json"

        mocker.patch.object(FileHandler, "DIR_PATH", d)

        actual = fh.open()

        assert actual == json.loads(expect)

    def test_open_file_when_file_does_not_exist(self, mocker, tmp_path):
        d = tmp_path / "test"
        d.mkdir()

        fh = FileHandler()
        fh.name_file = "test.json"

        mocker.patch.object(FileHandler, "DIR_PATH", d)

        actual = fh.open()

        assert not actual

    def test_open_file_when_file_does_not_exist_with_info(
        self, mocker, tmp_path, capsys
    ):
        d = tmp_path / "test"
        d.mkdir()

        fh = FileHandler()
        fh.name_file = "test.json"

        mocker.patch.object(FileHandler, "DIR_PATH", d)

        with patch("builtins.print") as mock:
            actual = fh.open()

        mock.assert_has_calls([call("File doesn't exist!")])

        capsys.readouterr()
        assert not actual

    def test_save_when_buffer_is_set(
        self, mocker, tmp_path, capsys, get_sample_json_file
    ):
        fh = FileHandler()
        fh.name_file = "test.json"
        buffer = get_sample_json_file

        d = tmp_path / "test"
        d.mkdir()

        mocker.patch.object(FileHandler, "DIR_PATH", d)

        fh.save(buffer)
        capsys.readouterr()
        assert len(list(tmp_path.iterdir())) == 1

    def test_save_when_file_exist_then_overwrite_it(
        self, mocker, tmp_path, capsys, create_temp_directory, get_sample_json_file
    ):
        expect = json.dumps(get_sample_json_file, indent=4)

        fh = FileHandler()
        fh.name_file = "test.json"
        buffer = get_sample_json_file

        d = create_temp_directory
        old_file = d / "test.json"

        old_file.write_text("Test old file.")

        mocker.patch.object(FileHandler, "DIR_PATH", create_temp_directory)

        fh.save(buffer)

        capsys.readouterr()
        assert len(list(tmp_path.iterdir())) == 1
        assert old_file.read_text() == expect

    def test_save_when_buffer_is_set_then_call_info(
        self, mocker, tmp_path, get_sample_json_file, create_temp_directory
    ):
        fh = FileHandler()
        fh.name_file = "test.json"
        buffer = get_sample_json_file

        mocker.patch.object(FileHandler, "DIR_PATH", create_temp_directory)

        with patch("builtins.print") as mock:
            fh.save(buffer)

        mock.assert_has_calls([call("Saved. \n")])
