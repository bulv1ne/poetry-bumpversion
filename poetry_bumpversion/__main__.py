import argparse
import re
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from subprocess import call

RE_VERSION = re.compile(r'version = "(?P<version>\d+\.\d+(\.\d+)?)"')
RE_REPOSITORY = re.compile(r'^repository = "(?P<repository>.*)"$', re.MULTILINE)


@dataclass
class Project:
    project_dir: Path

    @property
    def pyproject(self):
        return self.project_dir / "pyproject.toml"

    @property
    def changelog(self):
        return self.project_dir / "CHANGELOG.md"

    def get_version(self) -> str:
        match = RE_VERSION.search(self.pyproject.read_text())
        if not match:
            raise argparse.ArgumentTypeError(
                f"Could not find version in {self.pyproject}"
            )
        return match.group("version")

    def set_version(self, version_number: str):
        file_text = self.pyproject.read_text()
        new_file_text = RE_VERSION.sub(f'version = "{version_number}"', file_text)
        self.pyproject.write_text(new_file_text)

    def get_repository(self) -> str:
        match = RE_REPOSITORY.search(self.pyproject.read_text())
        if not match:
            raise argparse.ArgumentTypeError(
                f"Could not find repository in {self.pyproject}"
            )
        return match.group("repository")

    def update_changelog(self, old_version_number: str, version_number: str):
        if not self.changelog.exists():
            print("CHANGELOG.md not found")
            return
        file_text = self.changelog.read_text()
        file_text = file_text.replace(
            "## [Unreleased]",
            f"## [Unreleased]\n\n## [{version_number}] - {datetime.now():%Y-%m-%d}",
        )
        repository = self.get_repository()

        if re.search(r"^\[Unreleased\]:.*$", file_text, flags=re.MULTILINE):
            file_text = re.sub(
                r"^\[Unreleased\]:.*$",
                "\n".join(
                    [
                        f"[Unreleased]: {repository}compare/v{version_number}...HEAD",
                        f"[{version_number}]: {repository}compare/v{old_version_number}...v{version_number}",
                    ]
                ),
                file_text,
                flags=re.MULTILINE,
            )
        else:
            file_text = "\n\n".join(
                [
                    file_text,
                    f"[Unreleased]: {repository}compare/v{version_number}...HEAD",
                ]
            )

        self.changelog.write_text(file_text)


class VersionPart(Enum):
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"

    def __str__(self):
        return self.value


def increase_version_number(version_number: str, version_part: VersionPart) -> str:
    version_split = list(map(int, version_number.split(".")))

    if len(version_split) == 2:
        version_split.append(0)

    if version_part is VersionPart.PATCH:
        version_split[2] += 1
    elif version_part is VersionPart.MINOR:
        version_split[1] += 1
        version_split[2] = 0
    elif version_part is VersionPart.MAJOR:
        version_split[0] += 1
        version_split[1] = 0
        version_split[2] = 0

    return ".".join(map(str, version_split))


def run_command(name, *args, **kwargs):
    exit_code = call(args, **kwargs)

    if exit_code > 0:  # pragma: no cover
        raise argparse.ArgumentTypeError(
            f"'{name}' command exited with exit code {exit_code}"
        )


def cli(project_dir: Path, version_part: VersionPart, dry_run: bool):
    project = Project(project_dir)
    old_version = project.get_version()
    version = increase_version_number(old_version, version_part)

    print(f"Bumping version from v{old_version} to v{version}")
    if not dry_run:
        project.set_version(version)
        project.update_changelog(old_version, version)

        run_command("git add", "git", "add", ".", cwd=project_dir)
        run_command(
            "git commit",
            "git",
            "commit",
            # "-p",
            "-m",
            f"Bump version from v{old_version} to v{version}",
            cwd=project_dir,
        )

        run_command("git tag", "git", "tag", f"v{version}", cwd=project_dir)


def directory_path(value) -> Path:
    directory = Path(value).resolve().absolute()
    if not directory.exists():
        raise argparse.ArgumentTypeError("Directory path doesn't exist")
    if not directory.is_dir():
        raise argparse.ArgumentTypeError(f"{directory} is not a directory")
    pyproject_file = directory / "pyproject.toml"
    if not pyproject_file.exists():
        raise argparse.ArgumentTypeError(f"{pyproject_file} file doesn't exist")

    return directory


parser = argparse.ArgumentParser(
    description="Bumps the version in pyproject.toml and creates a git commit + tag",
)
parser.add_argument(
    "version_part",
    nargs="?",
    choices=list(VersionPart),
    default=VersionPart("patch"),
    type=VersionPart,
)
parser.add_argument(
    "--project-dir", "-d", nargs="?", default=Path("."), type=directory_path
)
parser.add_argument(
    "--dryrun",
    dest="dry_run",
    action="store_true",
    help="Don't executy any git command or change any file",
)


def main():  # pragma: no cover
    args = parser.parse_args()
    cli(args.project_dir, args.version_part, args.dry_run)


if __name__ == "__main__":  # pragma: no cover
    main()
