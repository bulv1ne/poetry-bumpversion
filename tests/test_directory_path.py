import argparse

import pytest

from poetry_bumpversion.__main__ import directory_path


def test_directory_path_doesnt_exist(tmp_path):
    with pytest.raises(
        argparse.ArgumentTypeError, match="^Directory path doesn't exist$"
    ):
        directory_path(str(tmp_path / "does not exist"))


def test_directory_path_file(tmp_path):
    file_path = tmp_path / "file1.txt"
    file_path.write_text("Hello world")
    with pytest.raises(argparse.ArgumentTypeError, match=r".* is not a directory$"):
        directory_path(str(file_path))


def test_directory_path_toml_doesnt_exist(tmp_path):
    with pytest.raises(
        argparse.ArgumentTypeError, match=r".*pyproject\.toml file doesn't exist$"
    ):
        directory_path(str(tmp_path))


def test_directory_ok(tmp_path):
    (tmp_path / "pyproject.toml").write_text("")
    assert directory_path(str(tmp_path)) == tmp_path
