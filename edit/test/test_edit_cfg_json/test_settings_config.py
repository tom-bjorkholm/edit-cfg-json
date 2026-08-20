#! /usr/bin/env python3
"""Tests of the settings of the editor written as a configuration class.

What is asked of it is what is asked of any configuration class this library
edits, and two things beyond that: that it says the same as `Settings` about
every setting there is, and that a file which names one thing keeps the
editor's own answer for everything else.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from dataclasses import fields
from pathlib import Path
import json
import sys
import pytest
from config_as_json import InvalidConfiguration
from edit_cfg_json import ActionSettings, EditModel, SETTINGS_DESCRIPTIONS, \
    Settings, SettingsConfig, declared_actions, described_below, \
    model_as_text, row_description
from edit_cfg_json.settings_config import ACTION_DESCRIPTIONS, \
    ADDED_ACTIONS, EVERY_ACTION
from edit_cfg_json.tree import EVERY_ELEMENT
from .model_helpers import row_at, written

BAD_FILES = (('{"file_extension": "..."}', 'not a file name extension'),
             ('{"backup_suffix": " "}', 'not a backup file name suffix'),
             ('{"backup_count": 0}', 'backup_count'),
             ('{"actions": {"save": ["ctrl+q"]}}', 'both quit and save'))
"""Settings files that this class refuses, and a word of each refusal."""

MEMBER_IDS = ('extension', 'suffix', 'count', 'keys')
"""Names of those cases, so a failure says which file it was."""

WRONG_TYPES = ('{"backup_count": "soon"}', '{"file_extension": 5}',
               '{"priority_keys": "yes"}', '{"actions": {"save": "ctrl+w"}}',
               '{"actions": {"save": [5]}}')
"""Settings files whose values are of a type no setting of the editor has."""


def _parsed(text: str) -> SettingsConfig:
    """Return one settings file read as this class reads a settings file.

    Args:
        text: The whole text of a settings file.

    Returns:
        The settings that the file holds, with the defaults of the editor
        filling in whatever it left out.
    """
    config = SettingsConfig()
    config.parse_json(text, ok_to_use_defaults=True, stderr_file=sys.stderr)
    return config


def test_declares_settings() -> None:
    """Test the class declares one member per attribute of `Settings`.

    A setting that this class did not declare could not be written in a file
    at all, and one it declared and `Settings` did not could not reach the
    editor, so the two lists have to be the same one.
    """
    assert _members(SettingsConfig()) == {field.name
                                          for field in fields(Settings())}


def _members(config: SettingsConfig) -> set[str]:
    """Return the names of the settings that one object of the class holds.

    Args:
        config: Object to read.

    Returns:
        The public attributes of it, which are what `config_as_json` counts
        as the members of a configuration.
    """
    return {name for name in vars(config) if not name.startswith('_')}


def test_declares_actions() -> None:
    """Test the key combinations are the ones `ActionSettings` declares."""
    assert set(declared_actions()) == {field.name
                                       for field in fields(ActionSettings())}
    assert declared_actions() == {name: list(getattr(ActionSettings(), name))
                                  for name in declared_actions()}


def test_declared_defaults() -> None:
    """Test a settings file that says nothing says what the editor decides."""
    assert SettingsConfig().as_settings() == Settings()


def test_round_trip() -> None:
    """Test what this class writes it reads back as the same settings."""
    chosen = Settings(file_extension='.cfg', extension_enforced=True,
                      backup_suffix='.old', backup_count=3,
                      priority_keys=False, confirm_overwrite=False,
                      actions=ActionSettings(save=('ctrl+w',)))
    config = SettingsConfig()
    config.parse_json(json.dumps(_as_data(chosen)), stderr_file=sys.stderr)
    assert config.as_settings() == chosen


def _as_data(settings: Settings) -> dict[str, object]:
    """Return one `Settings` as the data a settings file holds.

    Args:
        settings: What an application decided about the editor.

    Returns:
        One entry per member of `SettingsConfig`.
    """
    data: dict[str, object] = {
        field.name: getattr(settings, field.name)
        for field in fields(settings) if field.name != 'actions'}
    data['actions'] = {name: list(getattr(settings.actions, name))
                       for name in declared_actions()}
    return data


def test_partial_file() -> None:
    """Test a file naming one thing keeps the editor's answer for the rest.

    A settings file is written by hand to change one or two things, and the
    `actions` member is the one where that is not free: it is one dict, and a
    file naming one action would leave the editor holding that one alone
    without the validator that completes it.
    """
    config = _parsed('{"actions": {"save": ["ctrl+w"]}, "backup_count": 4}')
    assert config.backup_count == 4
    assert config.backup_suffix == Settings().backup_suffix
    assert config.actions['save'] == ['ctrl+w']
    assert config.actions['quit'] == list(ActionSettings().quit)
    assert set(config.actions) == set(declared_actions())
    assert config.as_settings() == Settings(
        actions=ActionSettings(save=('ctrl+w',)), backup_count=4)


def test_extension_dot() -> None:
    """Test an extension without its dot is given one, as `Settings` does."""
    assert _parsed('{"file_extension": "cfg"}').file_extension == '.cfg'
    assert _parsed('{"file_extension": ".cfg"}').file_extension == '.cfg'


def test_suffix_kept() -> None:
    """Test a backup suffix is taken exactly as it was written.

    Unlike the extension, because a suffix that begins with a dot and one that
    does not are both shapes an application asks for.
    """
    assert _parsed('{"backup_suffix": "~"}').backup_suffix == '~'


@pytest.mark.parametrize('text, word', BAD_FILES, ids=MEMBER_IDS)
def test_refuses_bad_values(text: str, word: str) -> None:
    """Test this class refuses exactly what `Settings` itself refuses."""
    with pytest.raises(InvalidConfiguration) as refusal:
        _parsed(text)
    assert word in str(refusal.value)


@pytest.mark.parametrize('text', WRONG_TYPES)
def test_refuses_wrong_type(text: str) -> None:
    """Test a value of a type no setting has is refused rather than kept.

    `config_as_json` checks the declared type of a member only where the class
    asks it to, so a settings file could otherwise say that four backups are
    called `soon`.
    """
    with pytest.raises(InvalidConfiguration):
        _parsed(text)


def test_unknown_action() -> None:
    """Test an action name this editor does not have is refused.

    It is `config_as_json` that refuses it, because a dict member is matched
    against the keys its class declares while the file is parsed, so a
    misspelled action name is a mistake reported where it was made.
    """
    with pytest.raises(KeyError):
        _parsed('{"actions": {"quitt": ["ctrl+w"]}}')


def test_describes_members() -> None:
    """Test the class says what each of its members is for.

    A member with nothing said about it would be shown with the kind of value
    it holds and nothing else, which is the least this class of all classes
    should get away with.
    """
    described = {path[0] for path in SETTINGS_DESCRIPTIONS}
    assert described == _members(SettingsConfig())


def test_describes_actions() -> None:
    """Test each action says what it does, and any other is still described."""
    assert set(ACTION_DESCRIPTIONS) == set(declared_actions())
    assert SETTINGS_DESCRIPTIONS[('actions', EVERY_ELEMENT)] == EVERY_ACTION
    model = EditModel(SettingsConfig(), descriptions=SETTINGS_DESCRIPTIONS)
    for name, text in ACTION_DESCRIPTIONS.items():
        assert row_description(model, row_at(model, ('actions', name))) == text


def test_described_below() -> None:
    """Test an application putting this inside its own configuration.

    A description addresses the whole path to what it is about, so a class
    that holds a `SettingsConfig` as one member describes that member's
    members with its own path in front of every one of them.
    """
    moved = described_below(('editor',))
    assert set(moved) == {('editor',) + path for path in SETTINGS_DESCRIPTIONS}
    assert moved[('editor', 'backup_count')] == \
        SETTINGS_DESCRIPTIONS[('backup_count',)]


def test_editable_class() -> None:
    """Test the editor shows this class as it shows any configuration."""
    model = EditModel(SettingsConfig(), descriptions=SETTINGS_DESCRIPTIONS)
    model.open_all(no_more_folding=True)
    shown = model_as_text(model)
    assert 'backup_suffix = .bak' in shown
    assert 'ctrl+q' in shown


def test_edited_value() -> None:
    """Test a value typed into this class reaches it through a pass.

    Editing the settings of the editor in the editor is what `--edit-settings`
    is for, so what a user types has to be validated the way any value is.

    This setting is declared `Optional[str]` and holds nothing until it is
    asked to hold something, so it is given a value before one is typed into
    it, exactly as the user gives it one with the control on its row.
    """
    model = EditModel(SettingsConfig(), descriptions=SETTINGS_DESCRIPTIONS)
    model.add_element(('file_extension',))
    model.set_text(('file_extension',), 'cfg')
    assert model.validate().valid
    assert row_at(model, ('file_extension',)).value == '.cfg'


def test_refusal_at_member() -> None:
    """Test what one setting is refused for is said at that setting."""
    model = EditModel(SettingsConfig(), descriptions=SETTINGS_DESCRIPTIONS)
    model.set_text(('backup_count',), '0')
    verdict = model.validate()
    assert not verdict.valid
    assert ('backup_count',) in verdict.refused


def test_saved_read_back(tmp_path: Path) -> None:
    """Test a settings file the editor wrote is one it reads as settings."""
    out_file = tmp_path / 'written.cfg'
    model = EditModel(SettingsConfig(), descriptions=SETTINGS_DESCRIPTIONS)
    model.set_text(('backup_suffix',), '.old')
    model.set_out_file(out_file)
    assert model.save().saved
    assert _parsed(json.dumps(written(out_file))).as_settings() == \
        Settings(backup_suffix='.old')


def _old_shape_text() -> str:
    """Return a settings file as a release before the added actions wrote one.

    It is what this version writes with the actions of `ADDED_ACTIONS` taken
    out of it again, rather than a file written out here: a settings file is
    written by the editor saving one, so a file of an earlier release is that
    file without what the release did not have.

    Returns:
        The whole text of such a file.
    """
    data = json.loads(SettingsConfig().as_json_string(stderr_file=sys.stderr))
    assert isinstance(data, dict)
    actions = data['actions']
    for name in ADDED_ACTIONS:
        del actions[name]
    return json.dumps(data)


def test_added_are_actions() -> None:
    """Test every action said to be added is an action this editor has.

    An action named there and nowhere else would be supplied into a file as a
    key that `SettingsConfig` does not declare, and the file would then be
    refused for holding it.
    """
    assert set(ADDED_ACTIONS) <= set(declared_actions())


def test_reads_old_shape() -> None:
    """Test a file of a release before the added actions is read.

    The keys of a dict member are matched against the ones the class declares
    before any validator of the class is asked anything, and that happens
    whatever policy the parse was given. So without rules for an older file
    every settings file written before an action existed would be refused.
    """
    config = SettingsConfig()
    config.parse_json(_old_shape_text(), ok_to_use_defaults=False,
                      stderr_file=sys.stderr)
    assert set(config.actions) == set(declared_actions())
    for name in ADDED_ACTIONS:
        assert config.actions[name] == declared_actions()[name]
    assert config.as_settings() == Settings()


def test_old_shape_recorded() -> None:
    """Test reading such a file is recorded as the automatic change it is.

    What the file holds and what the editor shows are not the same values, and
    the hook of the configuration object is where that is found out.
    """
    config = SettingsConfig()
    config.parse_json(_old_shape_text(), ok_to_use_defaults=False,
                      stderr_file=sys.stderr)
    assert config.auto_change_hook().has_changes()
    assert not SettingsConfig().auto_change_hook().has_changes()


def test_named_action_kept() -> None:
    """Test a file that names an added action keeps what it says about it.

    The values are supplied only where the file holds nothing at that path,
    which is what makes these rules safe to keep for good.
    """
    config = _parsed('{"actions": {"find": ["ctrl+l"]}}')
    assert config.actions['find'] == ['ctrl+l']
    assert config.actions['find_next'] == list(ActionSettings().find_next)


def test_other_gaps_refused() -> None:
    """Test the rules rescue an older file and no other incomplete one.

    They supply two entries of one member, so a file that leaves a member out
    is refused as it was before they existed. That is what keeps a settings
    block inside an application's own configuration read whole.
    """
    data = json.loads(_old_shape_text())
    assert isinstance(data, dict)
    del data['file_extension']
    text = json.dumps(data)
    with pytest.raises(KeyError):
        SettingsConfig().parse_json(text, ok_to_use_defaults=False,
                                    stderr_file=sys.stderr)
