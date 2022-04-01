# poetry-bumpversion

[![Python application](https://github.com/bulv1ne/poetry-bumpversion/actions/workflows/python-app.yml/badge.svg)](https://github.com/bulv1ne/poetry-bumpversion/actions/workflows/python-app.yml)
[![Coverage Status](https://coveralls.io/repos/github/bulv1ne/poetry-bumpversion/badge.svg?branch=main)](https://coveralls.io/github/bulv1ne/poetry-bumpversion?branch=main)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=bulv1ne_poetry-bumpversion&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=bulv1ne_poetry-bumpversion)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Features

- Bumps the version in pyproject.toml
- Updates the CHANGELOG.md file

## Install

```sh
pip install git+https://github.com/bulv1ne/poetry-bumpversion
# Or
pipx install git+https://github.com/bulv1ne/poetry-bumpversion
```

## Usage

```sh
pipx run --spec git+https://github.com/bulv1ne/poetry-bumpversion poetry-bumpversion --help
```

## GitHub Actions

Copy the files [version-bump.yml](https://github.com/bulv1ne/poetry-bumpversion/blob/main/.github/workflows/version-bump.yml) and [version-tag.yml](https://github.com/bulv1ne/poetry-bumpversion/blob/main/.github/workflows/version-tag.yml) to your own `.github/workflows/` folder.

**version-bump.yml** is a manually triggered GitHub Action Workflow to bump the version. It will create a "release" branch with the version code changes and create a Pull Request.

**version-tag.yml** will be triggered automatically when the Pull Request is merged. The only requirement is that the commit message contains "Bump version from vA.B.C to vX.Y.Z", it will take the 6th word in that line to create a tag.
