#! /usr/bin/env python3
"""Tests for example e01_flat_config."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest
from example import e01_flat_config
from .helpers import dump, open_tk_ui, refused, textual_titles

VALID_LINE = 'validation: valid'
"""Line that `--ui dump` ends with for a buffer the example accepts."""

EXPECTED_DUMP = f'name = Flat example\nanswer = 42\n{VALID_LINE}'
"""Text that `--ui dump` is expected to print for the default values."""


def _dump(capsys: pytest.CaptureFixture[str], *settings: str) -> str:
    """Run this example with `--ui dump` and return what it printed."""
    return dump(e01_flat_config.main, capsys, *settings)


def _refused(capsys: pytest.CaptureFixture[str], *arguments: str) -> str:
    """Run this example, expect it to refuse, and return its error text."""
    return refused(e01_flat_config.main, capsys, *arguments)


def test_dump(capsys: pytest.CaptureFixture[str]) -> None:
    """Test --ui dump prints both members with their default values."""
    assert _dump(capsys) == EXPECTED_DUMP


def test_ui_is_required(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the example refuses to run without a selected user interface."""
    assert '--ui' in _refused(capsys)


def test_unknown_ui(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the example refuses a user interface it does not have."""
    assert 'curses' in _refused(capsys, '--ui', 'curses')


@pytest.mark.parametrize('option', ['-i', '--input', '-o', '--output'])
def test_files_refused(option: str,
                       capsys: pytest.CaptureFixture[str]) -> None:
    """Test the file options are refused until a later step implements them."""
    assert 'not supported yet' in _refused(capsys, '--ui', 'dump', option,
                                           'some.json')


def test_set_members(capsys: pytest.CaptureFixture[str]) -> None:
    """Test --set edits the buffer and marks what the user changed."""
    assert _dump(capsys, '--set', 'name=Other', '--set', 'answer=7') == \
        f'name = Other (edited)\nanswer = 7 (edited)\n{VALID_LINE}'


def test_set_same_value(capsys: pytest.CaptureFixture[str]) -> None:
    """Test setting a member to the value it has is not an edit."""
    assert _dump(capsys, '--set', 'name=Flat example') == EXPECTED_DUMP


def test_set_empty_value(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a member can be set to an empty field."""
    assert _dump(capsys, '--set', 'name=') == \
        f'name =  (edited)\nanswer = 42\n{VALID_LINE}'


def test_set_not_a_number(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a number member keeps text that is not a number yet."""
    assert _dump(capsys, '--set', 'answer=not-a-number') == \
        ('name = Flat example\nanswer = not-a-number (edited)\n'
         'validation: invalid\n'
         'Invalid configuration: Value for answer is not of type int.')


def test_dump_refused_bool(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a true or false typed into a number member is refused.

    A `bool` is an `int` in Python, so a range check on its own would accept
    it. The example declares the type of the member as well, which is what
    `config_as_json` has `ValueTypeValidator` for.
    """
    assert _dump(capsys, '--set', 'answer=true') == \
        ('name = Flat example\nanswer = true (edited)\n'
         'validation: invalid\n'
         'Invalid configuration: Value for answer must not be of type bool.')


def test_dump_refused_value(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a value outside the allowed range is refused, and why."""
    assert _dump(capsys, '--set', 'answer=500') == \
        ('name = Flat example\nanswer = 500 (edited)\n'
         'validation: invalid\nInvalid configuration: '
         'Value 500 for answer is greater than maximum 100.')


def test_dump_rewritten_value(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a value that a validator rewrote is shown as rewritten.

    A validation pass is not read only, and this is what makes that visible
    without a display: the value shown is the one the validator stored back
    and not the one that was typed.
    """
    assert _dump(capsys, '--set', 'name=other') == \
        ('name = Other (edited) (changed by validator)\n'
         f'answer = 42\n{VALID_LINE}')


def test_set_unknown_member(capsys: pytest.CaptureFixture[str]) -> None:
    """Test setting a member that does not exist is refused."""
    error = _refused(capsys, '--ui', 'dump', '--set', 'missing=1')
    assert 'missing is not a member' in error


def test_set_without_value(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a --set that names no value at all is refused."""
    error = _refused(capsys, '--ui', 'dump', '--set', 'name')
    assert '--set needs member=value' in error


def test_tk_ui_opens(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui tk builds the window and returns when it is closed."""
    open_tk_ui(e01_flat_config.main, monkeypatch)


def test_textual_ui_opens(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui textual starts the application named after the class."""
    assert textual_titles(e01_flat_config.main, monkeypatch) == ['FlatConfig']


def test_textual_ui_edited(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui textual shows an edit that --set made before it started."""
    assert textual_titles(e01_flat_config.main, monkeypatch, '--set',
                          'answer=7') == ['FlatConfig *']
