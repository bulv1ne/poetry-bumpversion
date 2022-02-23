import pytest

from poetry_bumpversion.__main__ import VersionPart, increase_version_number


@pytest.mark.parametrize(
    ["test_input", "expected"],
    [
        ("1.0", "1.0.1"),
        ("1.0.0", "1.0.1"),
        ("1.1", "1.1.1"),
        ("1.1.0", "1.1.1"),
        ("1.0.9", "1.0.10"),
    ],
)
def test_increase_version_patch(test_input, expected):
    assert increase_version_number(test_input, VersionPart.PATCH) == expected


@pytest.mark.parametrize(
    ["test_input", "expected"],
    [
        ("1.0", "1.1.0"),
        ("1.0.0", "1.1.0"),
        ("1.1", "1.2.0"),
        ("1.1.0", "1.2.0"),
        ("1.0.9", "1.1.0"),
        ("1.9.5", "1.10.0"),
    ],
)
def test_increase_version_minor(test_input, expected):
    assert increase_version_number(test_input, VersionPart.MINOR) == expected


@pytest.mark.parametrize(
    ["test_input", "expected"],
    [
        ("1.0", "2.0.0"),
        ("1.0.0", "2.0.0"),
        ("1.1", "2.0.0"),
        ("1.1.0", "2.0.0"),
        ("1.0.9", "2.0.0"),
        ("1.9.5", "2.0.0"),
    ],
)
def test_increase_version_major(test_input, expected):
    assert increase_version_number(test_input, VersionPart.MAJOR) == expected
