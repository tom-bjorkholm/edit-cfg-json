#! /usr/bin/env python3
"""Tests for example e05_old_format_config.

What this example adds is saying that reading the file changed it, so what is
asserted here is which members the editor marks and what it says about the
file. The class that can report its older keys and the class that cannot are
both run over the same file, because the point of the example is that the marks
are the same either way and only the explanation differs.

The file in the current shape is asserted as well, and it matters at least as
much: an editor that remarked on every file would be teaching its user to
ignore the remark.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import json
import pytest
from edit_cfg_json import EditModel, LoadPolicy, load_config
from example import e05_old_format_config
from example.e05_old_format_config import CURRENT_FORMAT, NoHookConfig, \
    OldFormatConfig
from .helpers import DUMP_TAIL, TEXT_LINE, WHOLE_LINE, data_file, dump, \
    head, input_tail, open_tk_ui, refused, textual_titles

OLD_FILE = 'e05_old_format.json'
"""Input file written by an older version of this example's application."""

CURRENT_FILE = 'e05_current.json'
"""Input file in the shape that this example writes today."""

HEAD = head(OldFormatConfig())
"""The lines that every dump of this example begins with."""

LOAD_MARK = ' (changed by the load)'
"""Mark that follows a value that reading the input file put there."""

CHANGED_LINE = 'Reading this file changed it'
"""Beginning of what the editor says about a file that reading changed."""

OLDER_KEYS_LINE = ('This file is in an older format. It was read with these '
                   'older keys: debug_trace, title')
"""What the class that takes the hook says about the keys of that file."""

DROPPED_LINE = ('This file holds keys that this configuration does not use, '
                'and saving leaves them out: debug_trace, title')
"""What the class that takes no hook says about the same two keys."""

SUPPLIED_LINE = ('These values were supplied because this file is in an older '
                 'format: format_version')
"""What the class that takes the hook says about the value it supplied."""

MIGRATED_ROWS = [f'format_version = {CURRENT_FORMAT}{LOAD_MARK}', WHOLE_LINE,
                 f'report_name = monthly-summary{LOAD_MARK}', TEXT_LINE,
                 f'owner = Ada Lovelace{LOAD_MARK}', TEXT_LINE,
                 'refresh_seconds = 900', WHOLE_LINE]
"""Every row of that file as read, with the mark of each changed member.

The row that matters most is the one for `refresh_seconds`: the file holds that
value under that name and nothing happened to it, so it carries no mark. What
each row says below it is the kind of value it holds, which is what the editor
knows about every member of every configuration without being told anything.
"""


def _dump(capsys: pytest.CaptureFixture[str], *settings: str) -> str:
    """Run this example with `--ui dump` and return what it printed."""
    return dump(e05_old_format_config.main, capsys, *settings)


def _text_of(config_type: type[OldFormatConfig], name: str) -> str:
    """Return the model of one class on one input file, as text.

    The class that takes no hook is not the one the example runs, so it is
    reached the way the docstring of the example reaches it: by handing the
    class to the editor, which is what the program of the core does.

    Args:
        config_type: Class to read the file with.
        name: File name inside the data folder of the examples.

    Returns:
        What the editor says about the load of that file.
    """
    loaded = load_config(config=config_type(), in_file=data_file(name))
    return EditModel(loaded.config, loaded.report).load_message


def test_older_file_marked(capsys: pytest.CaptureFixture[str]) -> None:
    """Test every member that reading the older file changed is marked.

    One of them was renamed into, one was supplied by the rules and one was
    rewritten by a validator, and the fourth is left alone because the file
    holds it as it stands.
    """
    printed = _dump(capsys, '-i', data_file(OLD_FILE))
    assert printed.startswith(HEAD)
    assert '\n'.join(MIGRATED_ROWS) in printed
    assert CHANGED_LINE in printed


def test_older_keys_named(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the class that takes the hook names the older keys of the file."""
    printed = _dump(capsys, '-i', data_file(OLD_FILE))
    assert OLDER_KEYS_LINE in printed
    assert SUPPLIED_LINE in printed
    assert DROPPED_LINE not in printed


def test_without_the_hook() -> None:
    """Test the class that takes no hook says what it can see for itself.

    It is the same file and the same rules, so the values and their marks are
    the same. What it cannot do is say that one of those two keys was renamed
    and the other removed, and it says the honest less instead.
    """
    said = _text_of(NoHookConfig, OLD_FILE)
    assert CHANGED_LINE in said
    assert DROPPED_LINE in said
    assert OLDER_KEYS_LINE not in said
    assert SUPPLIED_LINE not in said


def test_current_file_silent(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a file in the current shape is read without a word about it."""
    printed = _dump(capsys, '-i', data_file(CURRENT_FILE))
    assert 'report_name = monthly-summary\n' in printed
    assert LOAD_MARK not in printed
    assert CHANGED_LINE not in printed
    assert printed.endswith(input_tail(CURRENT_FILE))


@pytest.mark.parametrize('config_type', [OldFormatConfig, NoHookConfig])
def test_current_file_by_both(config_type: type[OldFormatConfig]) -> None:
    """Test neither class has anything to say about the current shape.

    Args:
        config_type: Class to read the file with.
    """
    assert _text_of(config_type, CURRENT_FILE) == ''


def test_defaults_are_silent(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a session on the declared defaults says nothing about a load."""
    printed = _dump(capsys)
    assert printed.startswith(HEAD)
    assert printed.endswith(DUMP_TAIL)
    assert CHANGED_LINE not in printed


def test_migrating_save(tmp_path: Path,
                        capsys: pytest.CaptureFixture[str]) -> None:
    """Test saving the older file writes it in the shape of today.

    This is what the whole report is a warning about, and it is also what
    makes the editor a way of migrating a file: what is written is what was
    shown, so the older keys are gone and the supplied value is there.
    """
    out_file = tmp_path / 'current.json'
    printed = _dump(capsys, '-i', data_file(OLD_FILE), '-o', str(out_file),
                    '--save')
    assert 'validation: valid' in printed
    assert json.loads(out_file.read_text(encoding='UTF-8')) == {
        'format_version': CURRENT_FORMAT, 'owner': 'Ada Lovelace',
        'refresh_seconds': 900, 'report_name': 'monthly-summary'}


def test_strict_reads_older(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the strict policy opens the older file and still reports it.

    The rules for an older format run while the file is parsed and before its
    keys are checked, so the file is complete by the time the policy has
    anything to say about it. Nothing was filled in from the declared
    defaults, and the report says so by not saying otherwise.
    """
    printed = _dump(capsys, '-i', data_file(OLD_FILE), '--policy', 'strict')
    assert OLDER_KEYS_LINE in printed
    assert 'filled in from the defaults' not in printed
    assert ' (filled from default)' not in printed


@pytest.mark.parametrize('policy', [policy.name.lower().replace('_', '-')
                                    for policy in LoadPolicy])
def test_every_policy(policy: str, capsys: pytest.CaptureFixture[str]) -> None:
    """Test the older file is read and reported under every policy.

    Args:
        policy: The `--policy` value of this run.
        capsys: The pytest fixture that captured the output.
    """
    printed = _dump(capsys, '-i', data_file(OLD_FILE), '--policy', policy)
    assert '\n'.join(MIGRATED_ROWS) in printed
    assert OLDER_KEYS_LINE in printed


def test_unknown_member(capsys: pytest.CaptureFixture[str]) -> None:
    """Test setting a member that this configuration does not have."""
    error = refused(e05_old_format_config.main, capsys, '--ui', 'dump',
                    '--set', 'title=an older key')
    assert 'title is not a member' in error


def test_tk_ui_opens(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui tk builds the window and returns when it is closed."""
    open_tk_ui(e05_old_format_config.main, monkeypatch, '-i',
               data_file(OLD_FILE))


def test_textual_ui_opens(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui textual starts the application named after the class."""
    assert textual_titles(e05_old_format_config.main, monkeypatch, '-i',
                          data_file(OLD_FILE)) == ['OldFormatConfig']
