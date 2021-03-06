import argparse
from datetime import datetime
from pathlib import Path

import pytest

from poetry_bumpversion.__main__ import Project, VersionPart, cli, run_command

PYPROJECT_CONTENTS = """
[tool.poetry]
name = "example-proj"
version = "{version}"
repository = "https://github.com/user/example-proj/"
""".strip()

PYPROJECT_CONTENTS_NO_VERSION = """
[tool.poetry]
name = "example-proj"
repository = "https://github.com/user/example-proj/"
""".strip()

PYPROJECT_CONTENTS_NO_REPO = """
[tool.poetry]
name = "example-proj"
version = "0.1.0"
""".strip()

CHANGELOG_CONTENTS_FIRST = """
# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]
### Added
- First version
""".strip()

CHANGELOG_CONTENTS_SECOND = """
# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

## [0.1.1] - 2022-01-01
### Added
- First version

[Unreleased]: https://github.com/user/example-proj/compare/v0.1.1...HEAD"
""".strip()


def setup_project(path: Path, pyproject_text, changelog_text):
    pyproject = path / "pyproject.toml"
    pyproject.write_text(pyproject_text)
    changelog = path / "CHANGELOG.md"
    changelog.write_text(changelog_text)
    run_command("git init", "git", "init", cwd=path)
    run_command("git add", "git", "add", ".", cwd=path)
    run_command("git commit", "git", "commit", "-m", "'First version'", cwd=path)

    cli(path, VersionPart.PATCH, False)


def test_cli_first_version(tmp_path):
    setup_project(
        tmp_path, PYPROJECT_CONTENTS.format(version="0.1.0"), CHANGELOG_CONTENTS_FIRST
    )

    changelog_text = (tmp_path / "CHANGELOG.md").read_text()
    assert "## [Unreleased]" in changelog_text
    assert f"## [0.1.1] - {datetime.now():%Y-%m-%d}" in changelog_text
    assert "### Added" in changelog_text
    assert "- First version" in changelog_text
    assert (
        "[Unreleased]: https://github.com/user/example-proj/compare/v0.1.1...HEAD"
        in changelog_text
    )


def test_cli_second_version(tmp_path):
    setup_project(
        tmp_path, PYPROJECT_CONTENTS.format(version="0.1.1"), CHANGELOG_CONTENTS_SECOND
    )

    changelog_text = (tmp_path / "CHANGELOG.md").read_text()
    assert "## [Unreleased]" in changelog_text
    assert f"## [0.1.2] - {datetime.now():%Y-%m-%d}" in changelog_text
    assert (
        "[Unreleased]: https://github.com/user/example-proj/compare/v0.1.2...HEAD"
        in changelog_text
    )
    assert (
        "[0.1.2]: https://github.com/user/example-proj/compare/v0.1.1...v0.1.2"
        in changelog_text
    )


def test_no_version_in_pyproject(tmp_path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(PYPROJECT_CONTENTS_NO_VERSION)
    with pytest.raises(argparse.ArgumentTypeError, match="^Could not find version in"):
        Project(tmp_path).get_version()


def test_no_repo_in_pyproject(tmp_path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(PYPROJECT_CONTENTS_NO_REPO)
    with pytest.raises(
        argparse.ArgumentTypeError, match="^Could not find repository in"
    ):
        Project(tmp_path).get_repository()
