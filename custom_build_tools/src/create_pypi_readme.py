#! /usr/bin/env python3
"""Start README_pypi.md generation with Python from the project venv."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import subprocess
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from build_spec import BuildInformation, BuildSpec

GENERATOR_FILE = 'create_pypi_readme_venv.py'


def get_project_root(
        build_information: Optional['BuildInformation'] = None) -> Path:
    """Return project root from build information or this script path."""
    if build_information is not None:
        return build_information['project_root']
    return Path(__file__).resolve().parents[2]


def get_venv_python(project_root: Path) -> Path:
    """Return the Python executable path inside the project venv."""
    windows_python = project_root / 'venv' / 'Scripts' / 'python.exe'
    if windows_python.exists():
        return windows_python
    return project_root / 'venv' / 'bin' / 'python'


def get_generator_path() -> Path:
    """Return the generator script that is run in the project venv."""
    return Path(__file__).with_name(GENERATOR_FILE).resolve()


def run_in_venv_python(project_root: Path) -> None:
    """Run the README generator with Python from the project venv."""
    command = [str(get_venv_python(project_root)), str(get_generator_path())]
    subprocess.run(command, check=True, cwd=project_root)


def create_pypi_readme_cmd(
        build_spec: Optional['BuildSpec'] = None,
        build_information: Optional['BuildInformation'] = None) -> None:
    """Run README generation with the project venv Python."""
    _ = build_spec
    run_in_venv_python(get_project_root(build_information))


if __name__ == '__main__':
    create_pypi_readme_cmd()
