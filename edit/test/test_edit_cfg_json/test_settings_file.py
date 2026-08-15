#! /usr/bin/env python3
"""Tests of where a program of this library reads its own settings from.

The lookup is five steps in a fixed order, and what the tests are really about
is the order and the one asymmetry in it: a file that was *named* must be
there, and a file that was *looked for* need not be.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import pytest
from edit_cfg_json import ConfigLoadError, SETTINGS_VARIABLE, \
    SHARED_SETTINGS, Settings, load_settings, settings_file

OWN_SETTINGS = '.edit-cfg-json-test.cfg'
"""Name a program of these tests has for its own file in the home folder."""

SUFFIX_FORM = '{{"backup_suffix": "{suffix}"}}'
"""A settings file naming one thing, which is what such a file is for."""


@pytest.fixture(name='home')
def _home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Return an empty home folder that the lookup will really look in.

    It is this test's own folder rather than the one that `conftest.py` gives
    every test, because a test that writes a settings file must not leave it
    where the next test finds it. `Path.home` is patched rather than the
    environment, for the reason that fixture gives.

    Args:
        tmp_path: Folder of this test.
        monkeypatch: What the patching is undone by.

    Returns:
        The folder that `Path.home()` answers with while this test runs.
    """
    folder = tmp_path / 'home'
    folder.mkdir()
    monkeypatch.setattr(Path, 'home', lambda: folder)
    return folder


def _written(folder: Path, name: str, suffix: str) -> Path:
    """Write one settings file, and return where it was written.

    Args:
        folder: Folder to write it in.
        name: Name of the file.
        suffix: What the file says the kept file is called, which is how each
            test tells the file it found from the ones it did not.

    Returns:
        The file that was written.
    """
    path = folder / name
    path.write_text(SUFFIX_FORM.format(suffix=suffix), encoding='UTF-8')
    return path


def test_nothing_found(home: Path) -> None:
    """Test a lookup that finds no file at all uses the editor's answers."""
    assert settings_file(home_settings=OWN_SETTINGS) is None
    assert load_settings(home_settings=OWN_SETTINGS) == Settings()
    assert not list(home.iterdir())


def test_shared_home_file(home: Path) -> None:
    """Test the file that every program of this library reads is found."""
    shared = _written(home, SHARED_SETTINGS, '.shared')
    assert settings_file(home_settings=OWN_SETTINGS) == shared
    assert load_settings(home_settings=OWN_SETTINGS).backup_suffix == '.shared'


def test_own_beats_shared(home: Path) -> None:
    """Test a program's own file is read before the shared one.

    That is what lets a user whose window and terminal editors want different
    answers write one file each, and a user who wants one answer write only
    the shared file.
    """
    _written(home, SHARED_SETTINGS, '.shared')
    own = _written(home, OWN_SETTINGS, '.own')
    assert settings_file(home_settings=OWN_SETTINGS) == own
    assert load_settings(home_settings=OWN_SETTINGS).backup_suffix == '.own'


def test_no_own_file(home: Path) -> None:
    """Test a program with no file of its own reads the shared one.

    That is the backend which prints once and returns: what the two editors
    differ about is their keys and their questions, and it has neither.
    """
    _written(home, OWN_SETTINGS, '.own')
    shared = _written(home, SHARED_SETTINGS, '.shared')
    assert settings_file() == shared
    assert load_settings().backup_suffix == '.shared'


def test_variable_beats_home(home: Path,
                             monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the environment names a file that is read before either of them."""
    _written(home, OWN_SETTINGS, '.own')
    named = _written(home.parent, 'from_environment.cfg', '.environment')
    monkeypatch.setenv(SETTINGS_VARIABLE, str(named))
    assert settings_file(home_settings=OWN_SETTINGS) == named
    assert load_settings(home_settings=OWN_SETTINGS).backup_suffix == \
        '.environment'


def test_named_beats_all(home: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the file the command line names is read before every other."""
    _written(home, OWN_SETTINGS, '.own')
    monkeypatch.setenv(SETTINGS_VARIABLE,
                       str(_written(home.parent, 'other.cfg', '.other')))
    named = _written(home.parent, 'named.cfg', '.named')
    assert settings_file(named=named, home_settings=OWN_SETTINGS) == named
    assert load_settings(named=named,
                         home_settings=OWN_SETTINGS).backup_suffix == '.named'


@pytest.mark.parametrize('from_environment', [False, True])
def test_named_must_be_there(home: Path, from_environment: bool,
                             monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a file that was named and is not there is refused.

    Running with other settings than the ones that were asked for is the one
    thing a lookup must not do quietly, and the file of the home folder is
    deliberately not fallen back on: it is the step of a lookup that was not
    reached rather than a second answer to the question that was put.
    """
    _written(home, SHARED_SETTINGS, '.shared')
    missing = home.parent / 'no_settings_here.cfg'
    named = None
    if from_environment:
        monkeypatch.setenv(SETTINGS_VARIABLE, str(missing))
    else:
        named = missing
    with pytest.raises(ConfigLoadError) as refusal:
        settings_file(named=named, home_settings=OWN_SETTINGS)
    assert str(missing) in str(refusal.value)


def test_empty_variable(home: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a variable that is set to nothing names no file.

    Emptying a variable is how a shell takes one back, so it says the same as
    a variable that was never set rather than naming a file called nothing.
    """
    shared = _written(home, SHARED_SETTINGS, '.shared')
    monkeypatch.setenv(SETTINGS_VARIABLE, '')
    assert settings_file(home_settings=OWN_SETTINGS) == shared


def test_folder_is_no_file(home: Path) -> None:
    """Test a name that is a folder is refused rather than read."""
    folder = home.parent / 'a_folder.cfg'
    folder.mkdir()
    with pytest.raises(ConfigLoadError):
        settings_file(named=folder)


def test_file_is_no_settings(home: Path) -> None:
    """Test a file that cannot be read as settings is refused, and named.

    The refusal names the file, because the lookup may have found it rather
    than been told it, and a message about a settings file the user did not
    name would otherwise say nothing about which file to correct.
    """
    broken = home / SHARED_SETTINGS
    broken.write_text('this is not JSON', encoding='UTF-8')
    with pytest.raises(ConfigLoadError) as refusal:
        load_settings()
    assert str(broken) in str(refusal.value)


def test_partial_file(home: Path) -> None:
    """Test a settings file may name one thing and keep the rest.

    It is read with the policy that fills in what a file leaves out, because a
    settings file is written by hand to change one or two things.
    """
    _written(home, SHARED_SETTINGS, '.old')
    assert load_settings() == Settings(backup_suffix='.old')
