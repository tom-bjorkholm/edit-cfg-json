#! /usr/bin/env python3
"""Tests for what the application around the editor has decided.

The rules about a file name are tested here on the two functions that hold
them, and again through the model and the loading, because these tests say
what the rule is and those say that the editor really follows it.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from dataclasses import FrozenInstanceError, fields
from typing import Optional
import pytest
from edit_cfg_json import ActionSettings, Settings
from edit_cfg_json.settings import RESERVED_KEYS, checked_file, \
    chosen_file, current_settings

CFG = Settings(file_extension='.cfg')
"""Settings of an application whose extension is a default."""

ENFORCED = Settings(file_extension='.cfg', extension_enforced=True)
"""Settings of an application that enforces its extension."""


def test_default_keys() -> None:
    """Test the defaults are the keys the editor chose for itself."""
    actions = ActionSettings()
    assert actions.quit == ('ctrl+q',)
    assert actions.validate == ('ctrl+r', 'f5')
    assert actions.save == ('ctrl+s',)
    assert actions.save_as == ('ctrl+shift+s', 'f12')
    assert actions.cancel == ('escape',)
    assert actions.explain == ('f1', 'ctrl+g')


def test_no_opinion() -> None:
    """Test an application that says nothing has no opinion at all.

    Two of these are not "nothing": an application that says nothing about
    the file it overwrites gets the one thing the editor would have chosen
    anyway, which is one kept file and a question before it is written.
    """
    settings = Settings()
    assert settings.actions == ActionSettings()
    assert settings.file_extension is None
    assert not settings.extension_enforced
    assert settings.backup_suffix == '.bak'
    assert settings.backup_count == 1
    assert settings.confirm_overwrite


def test_every_action_named() -> None:
    """Test every action of the editor is an attribute of its own."""
    names = {field.name for field in fields(ActionSettings)}
    assert names == {'quit', 'validate', 'save', 'save_as', 'cancel',
                     'explain', 'fold'}


def test_reserved_keys_free() -> None:
    """Test no default of the editor takes a key that is reserved.

    An action added later is an added attribute and breaks no application,
    but a key that moved would break every user who had learnt it. So the
    keys that a search will want are kept free from the start rather than
    taken back afterwards.
    """
    actions = ActionSettings()
    taken = {key.lower() for field in fields(actions)
             for key in getattr(actions, field.name)}
    assert taken.isdisjoint(RESERVED_KEYS)
    assert 'ctrl+f' in RESERVED_KEYS


@pytest.mark.parametrize('keys', [('ctrl+w',), (), ('ctrl+w', 'f9')])
def test_one_action_set(keys: tuple[str, ...]) -> None:
    """Test one action can be changed while the others keep their keys."""
    actions = ActionSettings(save=keys)
    assert actions.save == keys
    assert actions.quit == ActionSettings().quit


@pytest.mark.parametrize('changes', [{'save': ('ctrl+q',)},
                                     {'save': ('CTRL+Q',)},
                                     {'quit': ('f2',), 'validate': ('f2',)}])
def test_shared_key_refused(changes: dict[str, tuple[str, ...]]) -> None:
    """Test one key combination given to two actions is refused.

    The settings are built inside the test and not by the parametrization,
    because a refusal that happened while the parameters were collected
    would end the whole test module rather than pass one test.
    """
    with pytest.raises(ValueError, match='is set for both'):
        ActionSettings(**changes)


def test_repeated_key_allowed() -> None:
    """Test one action may name the same combination more than once."""
    assert ActionSettings(save=('ctrl+s', 'ctrl+s')).save == ('ctrl+s',
                                                              'ctrl+s')


def test_settings_frozen() -> None:
    """Test the editor cannot change what the application decided."""
    settings = Settings()
    with pytest.raises(FrozenInstanceError):
        settings.file_extension = '.cfg'  # type: ignore[misc]


@pytest.mark.parametrize('given, expected', [('.cfg', '.cfg'),
                                             ('cfg', '.cfg'),
                                             ('.tar.gz', '.tar.gz'),
                                             (None, None)])
def test_extension_dot(given: Optional[str], expected: Optional[str]) -> None:
    """Test an extension is normalized to begin with its dot."""
    assert Settings(file_extension=given).file_extension == expected


@pytest.mark.parametrize('given', ['', '.', '..', '   '])
def test_no_extension_refused(given: str) -> None:
    """Test text that names no extension is refused as one."""
    with pytest.raises(ValueError, match='not a file name extension'):
        _ = Settings(file_extension=given)


@pytest.mark.parametrize('given', ['.bak', '.old', '~', '.tmp~', None])
def test_backup_suffix_kept(given: Optional[str]) -> None:
    """Test a backup suffix is taken exactly as the application gave it.

    Unlike the extension, which is normalized to begin with its dot: a
    suffix that is not an extension at all is one of the shapes an
    application asks for, and `~` is the one every editor knows.
    """
    assert Settings(backup_suffix=given).backup_suffix == given


@pytest.mark.parametrize('given', ['', '.', '..', '   '])
def test_no_suffix_refused(given: str) -> None:
    """Test text that would add nothing to a name is refused as a suffix."""
    with pytest.raises(ValueError, match='not a backup file name suffix'):
        _ = Settings(backup_suffix=given)


@pytest.mark.parametrize('given', [0, -1])
def test_no_backups_refused(given: int) -> None:
    """Test keeping fewer than one file is refused where it is asked for.

    Keeping none is what an empty `backup_suffix` says, and two ways of
    saying one thing are two answers that can disagree with each other.
    """
    with pytest.raises(ValueError, match='not a number of backup files'):
        _ = Settings(backup_count=given)


def test_settings_themselves() -> None:
    """Test settings that are handed over are the settings that are used."""
    settings = Settings(file_extension='.cfg')
    assert current_settings(settings) is settings


def test_callable_asked() -> None:
    """Test a callable is asked every time the settings are wanted."""
    asked: list[int] = []

    def answer() -> Settings:
        """Answer with a different extension every time."""
        asked.append(1)
        return Settings(file_extension=f'.c{len(asked)}')
    assert current_settings(answer).file_extension == '.c1'
    assert current_settings(answer).file_extension == '.c2'
    assert len(asked) == 2


@pytest.mark.parametrize('name, settings, refused', [
    ('a.cfg', Settings(), False), ('a.json', Settings(), False),
    ('a', Settings(), False),
    ('a.cfg', CFG, False), ('a.json', CFG, False), ('a', CFG, False),
    ('a.cfg', ENFORCED, False), ('a.CFG', ENFORCED, False),
    ('a.json', ENFORCED, True), ('a', ENFORCED, True)])
def test_checked_file(name: str, settings: Settings, refused: bool) -> None:
    """Test a file name is refused only by an extension that is enforced."""
    checked = checked_file(name=name, settings=settings)
    assert checked.name == name
    assert bool(checked.message) is refused


@pytest.mark.parametrize('name, settings, expected', [
    ('a', Settings(), 'a'), ('a', CFG, 'a.cfg'), ('a', ENFORCED, 'a.cfg'),
    ('a.cfg', CFG, 'a.cfg'), ('a.json', CFG, 'a.json'),
    ('a.CFG', ENFORCED, 'a.CFG')])
def test_chosen_file(name: str, settings: Settings, expected: str) -> None:
    """Test a chosen name gets the extension when it has none of its own."""
    chosen = chosen_file(name=name, settings=settings)
    assert chosen.name == expected
    assert not chosen.message


def test_chosen_file_refused() -> None:
    """Test a chosen name with another extension is refused when enforced."""
    chosen = chosen_file(name='a.json', settings=ENFORCED)
    assert chosen.name == 'a.json'
    assert '.cfg' in chosen.message
