#! /usr/bin/env python3
"""Where a program of this library reads its own settings from.

An application that calls `edit` knows its own settings and passes them. A
*program* has no application around it to ask, so it reads them from a file,
and this is the order it looks in: the file the command line names, the file
the environment names, the file of that program in the home folder, the file
of this library in the home folder, and finally no file at all.

**A file that was named must be there, and a file that was looked for need not
be.** `-c/--cfg` and the environment variable are somebody saying which file to
use, so a name that no file answers to is a mistake worth stopping for: running
with other settings than the ones that were asked for is the one thing a lookup
must not do quietly. The two files of the home folder are the lookup itself,
and a step of a lookup that finds nothing is the lookup working.

The file is read with `LoadPolicy.DEFAULTS`, because a settings file is
something somebody writes by hand to change one or two things, and what it does
not name is what the editor would have chosen anyway.

**A file that names nothing is the last step written down**, which follows from
that and is what a program has instead of an option for ignoring the lookup:
naming one is how a run asks for the values the editor would have chosen
anyway, past a file of the home folder that says something else.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional
import os
from config_as_json import PathOrStr
from edit_cfg_json.loading import ConfigLoadError, LoadPolicy, load_config
from edit_cfg_json.settings import Settings
from edit_cfg_json.settings_config import SettingsConfig

SETTINGS_VARIABLE = 'CFG_EDIT_CFG_JSON'
"""Environment variable naming the settings file of every program here.

It is one variable for all of them rather than one each, because what it is for
is a machine or a session that has decided how this editor behaves, and an
answer that had to be given three times would come to be given twice.
"""

SHARED_SETTINGS = '.edit-cfg-json.cfg'
"""File of the home folder that every program of this library reads.

It is the last step of the lookup, so a user who wants one answer for the
window and for the terminal writes it once here, and a user who wants the two
to differ writes the file of one of them beside it.
"""

NO_SETTINGS_FILE = 'The settings file {name} cannot be read.'
"""Message of the refusal of a named settings file that is not there."""

SETTINGS_REFUSED = 'The settings file {name} cannot be used.'
"""Message of the refusal of a settings file that cannot be read as one."""


def _named_file(name: PathOrStr) -> Path:
    """Return one settings file that was named, or refuse to run.

    Args:
        name: File that the command line or the environment named.

    Returns:
        That file.

    Raises:
        ConfigLoadError: No file of that name is there to read.
    """
    path = Path(name)
    if not path.is_file():
        raise ConfigLoadError(NO_SETTINGS_FILE.format(name=name))
    return path


def _home_file(name: Optional[str]) -> Optional[Path]:
    """Return one file of the home folder, or None when there is none.

    Args:
        name: Name of the file in the home folder, or None for a program that
            has no file of its own.

    Returns:
        That file where it exists, and None where it does not.
    """
    if name is None:
        return None
    path = Path.home() / name
    return path if path.is_file() else None


def settings_file(named: Optional[PathOrStr] = None,
                  home_settings: Optional[str] = None) -> Optional[Path]:
    """Return the file that one program reads its settings from.

    Args:
        named: File that `-c/--cfg` named, or None when it named none.
        home_settings: Name of this program's own file in the home folder, or
            None for a program that has none. A backend that prints once and
            returns is such a program: the settings that differ between the two
            editors are their keys and their questions, and it has neither.

    Returns:
        The file to read the settings from, and None where the lookup found no
        file and the defaults of the editor are what is used.

    Raises:
        ConfigLoadError: A file was named and is not there.
    """
    if named is not None:
        return _named_file(named)
    from_environment = os.environ.get(SETTINGS_VARIABLE)
    if from_environment:
        return _named_file(from_environment)
    return _home_file(home_settings) or _home_file(SHARED_SETTINGS)


def load_settings(named: Optional[PathOrStr] = None,
                  home_settings: Optional[str] = None) -> Settings:
    """Return the settings that one program runs with.

    Args:
        named: File that `-c/--cfg` named, or None when it named none.
        home_settings: Name of this program's own file in the home folder, or
            None for a program that has none.

    Returns:
        What the settings file says, or the defaults of the editor where the
        lookup found no file.

    Raises:
        ConfigLoadError: A file was named and is not there, or the file the
            lookup found cannot be read as settings of this editor.
    """
    found = settings_file(named=named, home_settings=home_settings)
    if found is None:
        return Settings()
    try:
        loaded = load_config(config=SettingsConfig(), in_file=found,
                             policy=LoadPolicy.DEFAULTS)
    except ConfigLoadError as error:
        raise ConfigLoadError(SETTINGS_REFUSED.format(name=found),
                              str(error)) from error
    assert isinstance(loaded.config, SettingsConfig)
    return loaded.config.as_settings()
