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

**A file of an earlier release is read, and the run says so.** What such a file
does not hold is supplied by the rules of `SettingsConfig` rather than refused,
and a run that needed those rules tells the user which file it was and how to
write it again, because a compatibility path is something a future version may
take away. It says that the rules were needed rather than that an earlier
version wrote the file, because a file trimmed by hand needs them as well. The
words are printed here and not by a
`config_as_json.MigrateCfgWarnHook`: a hook prints while the file is parsed,
and `load_config` collects what a parse says into diagnostics that it shows
only when the load failed, so a hook's warning about a load that succeeded
would never reach anybody.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional, TextIO
import os
import sys
from config_as_json import PathOrStr
from edit_cfg_json.loading import ConfigLoadError, LoadPolicy, LoadedConfig, \
    load_config
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

OLDER_SETTINGS = (
    'Reading the settings file {name} needed the compatibility rules for a '
    'file of an earlier version of this editor, so what it holds is not all '
    'that was used. It was accepted, and a future version may stop accepting '
    'it.\nWrite it in the current format by opening it in one of the editors '
    'and saving it:\n'
    '    edit-cfg-json-tk --edit-settings -i {name}\n'
    '    edit-cfg-json-textual --edit-settings -i {name}')
"""What a run says about a settings file that those rules were needed for.

It says that the rules were needed and not that an earlier version wrote the
file, because those are not the same statement: a file somebody trimmed by hand
needs them too, and telling such a user where their file came from would be
telling them something untrue. What follows is the same either way, which is
that saving the file writes every value this version has.

It names the file because the lookup has five steps and the user who sees this
did not necessarily choose the one that answered. It asks for the file to be
opened and saved rather than for a migration command of its own, because saving
is what writes those values and the editor is what the two programs are.
"""


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


def _warn_if_older(loaded: LoadedConfig, found: Path,
                   stderr_file: TextIO) -> None:
    """Say that the rules for an older file were needed, where they were.

    The hook of the configuration object is what those rules recorded into, and
    it holds nothing at all for a file they had no work to do on. So it is
    asked, rather than a version compared that a settings file does not carry.

    Args:
        loaded: The settings object, and what its load did beyond reading it.
        found: File that the lookup read the settings from.
        stderr_file: Stream used for user-facing diagnostics.
    """
    if loaded.config.auto_change_hook().has_changes():
        print(OLDER_SETTINGS.format(name=found), file=stderr_file)


def load_settings(named: Optional[PathOrStr] = None,
                  home_settings: Optional[str] = None,
                  stderr_file: TextIO = sys.stderr) -> Settings:
    """Return the settings that one program runs with.

    Args:
        named: File that `-c/--cfg` named, or None when it named none.
        home_settings: Name of this program's own file in the home folder, or
            None for a program that has none.
        stderr_file: Stream that a file of an earlier release is reported on.

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
    _warn_if_older(loaded=loaded, found=found, stderr_file=stderr_file)
    assert isinstance(loaded.config, SettingsConfig)
    return loaded.config.as_settings()
