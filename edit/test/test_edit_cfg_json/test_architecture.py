#! /usr/bin/env python3
"""Tests that the layering between the three packages is kept.

Separate wheels do not enforce the layering on their own, because all three
packages are installed into the same virtual environment when the tests run.
These tests are what actually keeps the core free of user interface imports
and keeps the backends on the public API of the core.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import ast
import importlib.util
import subprocess
import sys
import pytest

CORE_PACKAGE = 'edit_cfg_json'
"""Import name of the user interface agnostic core package."""

BACKEND_PACKAGES = ('edit_cfg_json_tk', 'edit_cfg_json_textual')
"""Import names of the two user interface backend packages."""

NO_UI_SCRIPT = '\n'.join(["import sys",
                          "sys.modules['tkinter'] = None",
                          "sys.modules['textual'] = None",
                          "import edit_cfg_json",
                          "print(edit_cfg_json.EditModel.__name__)"])
"""Script importing the core with both user interface libraries blocked.

An entry of `None` in `sys.modules` makes importing that name raise
`ImportError`, which is how the two libraries are made unavailable without
uninstalling them. The script runs in a separate process so that the blocked
entries cannot affect the rest of the test session.
"""


def test_core_needs_no_ui() -> None:
    """Test the core imports with tkinter and textual made unavailable."""
    done = subprocess.run([sys.executable, '-c', NO_UI_SCRIPT], check=False,
                          capture_output=True, text=True)
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == 'EditModel'


def _package_folder(package_name: str) -> Path:
    """Return the folder that holds the installed source of one package."""
    spec = importlib.util.find_spec(package_name)
    assert spec is not None
    locations = spec.submodule_search_locations
    assert locations is not None
    return Path(list(locations)[0])


def _imported_modules(source_file: Path) -> set[str]:
    """Return the names of the modules that one Python file imports."""
    tree = ast.parse(source_file.read_text(encoding='utf-8'))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            names.add(node.module)
    return names


@pytest.mark.parametrize('package_name', BACKEND_PACKAGES)
def test_backend_uses_public(package_name: str) -> None:
    """Test a backend imports only the top level of the core package."""
    source_files = sorted(_package_folder(package_name).glob('*.py'))
    assert source_files
    for source_file in source_files:
        for name in _imported_modules(source_file):
            parts = name.split('.')
            internal = parts[0] == CORE_PACKAGE and len(parts) > 1
            assert not internal, f'{source_file.name} imports {name}'
