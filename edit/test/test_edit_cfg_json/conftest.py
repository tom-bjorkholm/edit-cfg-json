#! /usr/bin/env python3
"""What every test of the core is given before it runs.

A program of this library reads its own settings from the home folder before
it does anything the command line asked for, so a test run that used the home
folder of whoever is running it would pass or fail according to what that
person had configured. Every test here is therefore given an empty one.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Iterator
import pytest
from edit_cfg_json import SETTINGS_VARIABLE


@pytest.fixture(autouse=True)
def _no_settings_of_the_user(tmp_path_factory: pytest.TempPathFactory,
                             monkeypatch: pytest.MonkeyPatch
                             ) -> Iterator[None]:
    """Give one test a home folder with no settings file in it.

    `Path.home` is patched rather than the environment, because which variable
    it reads differs between the platforms this library runs on and the lookup
    is the same on all of them. A test that wants a settings file writes one
    into the folder this made.
    """
    folder = tmp_path_factory.mktemp('home')
    monkeypatch.setattr(Path, 'home', lambda: folder)
    monkeypatch.delenv(SETTINGS_VARIABLE, raising=False)
    yield
