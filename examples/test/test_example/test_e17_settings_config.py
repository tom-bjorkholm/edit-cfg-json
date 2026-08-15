#! /usr/bin/env python3
"""Tests for example e17_settings_config.

What this example adds is the settings of the editor as a configuration class:
one member of an application's own configuration that holds a whole
`edit_cfg_json.SettingsConfig`. So what is asserted here is that it is a node
of the tree like any other nested object, that this library's own descriptions
reach it under the member that holds it, that its own rules refuse what
`ActionSettings` refuses, and that what it holds becomes the `Settings` the
editor really runs with.

Every one of these runs `--ui dump`, except the two that check the example
opens in each of the two editors. What a user does with those — pressing the
fold control on the `editor` row, adding a combination to an action — is the
editors' own and is tested where it exists.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import json
import pytest
from edit_cfg_json import SETTINGS_DESCRIPTIONS, Settings, described_below
from example import e17_settings_config
from example.e17_settings_config import DESCRIPTIONS, ToolConfig
from .helpers import data_file, dump, head, input_tail, open_tk_ui, \
    saved_tail, textual_titles

HEAD = head(ToolConfig())
"""The lines that every dump of this example begins with."""

DATA_NAME = 'e17_tool.json'
"""Input file of this example, which holds a whole settings block."""

NESTED_ROW = 'editor: SettingsConfig'
"""What the row of the member holding the settings of the editor says."""

REFUSED_KEYS = 'validation: invalid, see editor.actions'
"""What the verdict says when two actions were given one combination."""


def _dump(capsys: pytest.CaptureFixture[str], *settings: str) -> str:
    """Run this example with `--ui dump` and return what it printed."""
    return dump(e17_settings_config.main, capsys, *settings)


def test_settings_are_a_node(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the settings of the editor are shown as a nested object.

    A row saying its class, with its own members below it and a badge saying
    what it is on its own, is what any nested configuration object gets. There
    is nothing special about this one, which is the point of the example.
    """
    shown = _dump(capsys, '--fold', 'editor')
    assert shown.startswith(HEAD)
    assert f'{NESTED_ROW} [valid on its own]' in shown
    assert 'backup_suffix = .bak' in shown


def test_library_describes(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the settings say what they are for under the member holding them.

    The application describes its own two members and lets this library
    describe every path of the settings, which is what `described_below` is
    for.
    """
    assert set(DESCRIPTIONS) == {('report_folder',), ('verbose',),
                                 ('editor',)} | \
        set(described_below(('editor',)))
    shown = _dump(capsys, '--fold', 'editor')
    assert SETTINGS_DESCRIPTIONS[('backup_count',)] in shown


def test_actions_are_rows(capsys: pytest.CaptureFixture[str]) -> None:
    """Test every action of the editor is a row with its combinations below.

    That is what makes the combinations editable: a list is a container with a
    row per element, and a container of a settings file is one the user adds
    to and takes from like any other.
    """
    shown = _dump(capsys, '--fold', 'editor', '--fold', 'editor.actions')
    for name in ('quit', 'validate', 'save', 'save_as', 'cancel', 'explain',
                 'fold'):
        assert f'    {name}: ' in shown
    assert '0 = ctrl+s' in shown


def test_file_is_read(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the input file holds a whole settings block and is opened."""
    shown = _dump(capsys, '-i', data_file(DATA_NAME), '--fold', 'editor')
    assert 'report_folder = /srv/tool/reports' in shown
    assert 'backup_suffix = .old' in shown
    assert shown.endswith(input_tail(DATA_NAME))


def test_own_rules_refuse(capsys: pytest.CaptureFixture[str]) -> None:
    """Test what the settings refuse is refused, and said at their member.

    The class holding them declares no rule at all about them:
    `config_as_json` runs the plan of every nested object while it reads the
    buffer, so a combination given to two actions is refused by
    `edit_cfg_json.ActionSettings` itself.
    """
    shown = _dump(capsys, '--fold', 'editor', '--fold', 'editor.actions',
                  '--set', 'editor.actions.save.0=ctrl+q')
    assert REFUSED_KEYS in shown
    assert 'both quit and save' in shown


def test_block_read_whole(capsys: pytest.CaptureFixture[str],
                          tmp_path: Path) -> None:
    """Test a settings block that leaves a member out cannot be opened.

    A nested configuration object is read whole whatever policy the parse
    around it was given, which is why the data file of this example is as long
    as it is. A settings *file* of its own is a different thing and may name
    one setting, which is what `edit_cfg_json.load_settings` reads.
    """
    partial = tmp_path / 'partial.json'
    partial.write_text(json.dumps({'report_folder': '/tmp/r',
                                   'verbose': False,
                                   'editor': {'backup_count': 3}}),
                       encoding='UTF-8')
    with pytest.raises(SystemExit) as ended:
        e17_settings_config.main(['--ui', 'dump', '--policy', 'defaults',
                                  '-i', str(partial)])
    assert ended.value.code != 0
    assert 'actions' in capsys.readouterr().err


def test_editor_runs_with() -> None:
    """Test the object in the configuration is what the editor is given.

    `as_settings()` is the whole bridge between a configuration class and the
    frozen object every entry point of this library takes.
    """
    assert ToolConfig().editor.as_settings() == Settings()
    from_file = ToolConfig(from_json_filename=data_file(DATA_NAME))
    settings = from_file.editor.as_settings()
    assert settings.backup_suffix == '.old'
    assert settings.backup_count == 3
    assert settings.file_extension == '.cfg'
    assert settings.actions.save == ('ctrl+w',)


def test_saved_round_trip(capsys: pytest.CaptureFixture[str],
                          tmp_path: Path) -> None:
    """Test a changed setting reaches the file and is read back from it."""
    out_file = tmp_path / 'written.json'
    shown = _dump(capsys, '-i', data_file(DATA_NAME), '-o', str(out_file),
                  '--set', 'editor.backup_count=5', '--save')
    assert shown.endswith(saved_tail(out_file, ToolConfig.__name__))
    written = ToolConfig(from_json_filename=str(out_file))
    assert written.editor.as_settings().backup_count == 5


def test_opens_in_tk(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the Tkinter editor opens on this example without a refusal."""
    open_tk_ui(e17_settings_config.main, monkeypatch, '-i',
               data_file(DATA_NAME))


def test_opens_in_textual(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the Textual editor opens on this example without a refusal.

    The example hands the editor the settings its own configuration holds, and
    the input file gives `save` another combination, so the key that ends this
    editor is the one that file names.
    """
    titles = textual_titles(e17_settings_config.main, monkeypatch, '-i',
                            data_file(DATA_NAME))
    assert titles == [ToolConfig.__name__]
