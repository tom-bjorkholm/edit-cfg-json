#! /usr/bin/env python3
"""Tests for example e04_validated_config.

What this example adds is saying which member of a configuration is wrong, so
what is asserted here is *where* each message appears and not only that it
appears at all. The one rule that has no member to appear at is asserted the
same way, because that it stays in the block below the members is as much a
decision as the rest of it.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import json
import pytest
from example import e04_validated_config
from example.e04_validated_config import DESCRIPTIONS, LONGEST_RUN, \
    MOST_RETRIES, ValidatedConfig
from .helpers import DUMP_TAIL, TEXT_LINE, WHOLE_LINE, data_file, dump, \
    head, input_tail, open_tk_ui, refused, textual_titles

VALID_LINE = 'validation: valid'
"""Line that `--ui dump` ends with for a buffer the example accepts."""

VALID_END = f'{VALID_LINE}\n{DUMP_TAIL}'
"""How a dump of an accepted buffer with no output file ends."""

HEAD = head(ValidatedConfig())
"""The lines that every dump of this example begins with."""

ABOUT_NAME = DESCRIPTIONS[('job_name',)]
"""What this example says about the member its own validator is about."""

ABOUT_RETRIES = DESCRIPTIONS[('retries',)]
"""What this example says about the first of its two numbers."""

SPACED_NAME = 'Invalid configuration: job_name may not contain a space.'
"""What the validator this application wrote says when it refuses."""

TOO_MANY = ('Invalid configuration: Value 9 for retries is greater than '
            f'maximum {MOST_RETRIES}.')
"""What a validator `config_as_json` ships says about too many retries."""

TOO_LONG = ('Invalid configuration: Value 2400 for longest run is greater '
            f'than maximum {LONGEST_RUN}.')
"""What the rule that is about no single member says when it refuses.

Six attempts of 400 seconds is 2400 seconds, and neither `retries` nor
`timeout_seconds` is outside its own range at those two values.
"""


def _dump(capsys: pytest.CaptureFixture[str], *settings: str) -> str:
    """Run this example with `--ui dump` and return what it printed."""
    return dump(e04_validated_config.main, capsys, *settings)


def _refused(capsys: pytest.CaptureFixture[str], *arguments: str) -> str:
    """Run this example, expect it to refuse, and return its error text."""
    return refused(e04_validated_config.main, capsys, *arguments)


def test_defaults_accepted(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the declared defaults satisfy every rule of this example."""
    printed = _dump(capsys)
    assert printed.startswith(HEAD)
    assert printed.endswith(VALID_END)


def test_own_validator(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a validator this application wrote is attributed to its member.

    `config_as_json` has never heard of `NoSpacesValidator`, and the editor
    recognises no validator by type, so what it says is put beside its member
    exactly as what a validator of the library says is.
    """
    printed = _dump(capsys, '--set', 'job_name=nightly backup')
    assert (f'job_name = nightly backup (edited)\n    {ABOUT_NAME}\n'
            f'{TEXT_LINE}\n    {SPACED_NAME}') in printed
    assert 'validation: invalid, see job_name' in printed


def test_library_validator(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a validator the library ships is attributed the same way."""
    printed = _dump(capsys, '--set', 'retries=9')
    assert (f'retries = 9 (edited)\n    {ABOUT_RETRIES}\n'
            f'{WHOLE_LINE}\n    {TOO_MANY}') in printed
    assert 'validation: invalid, see retries' in printed


def test_every_bad_member(capsys: pytest.CaptureFixture[str]) -> None:
    """Test both refused members are named and carry their own sentence.

    `Config.validate()` stops at the first step that refuses, so a user who
    was told only what that step said would correct one member per run. This
    is the whole gain of walking the plan a second time.
    """
    printed = _dump(capsys, '--set', 'job_name=a b', '--set', 'retries=9')
    assert f'    {SPACED_NAME}' in printed
    assert f'    {TOO_MANY}' in printed
    assert 'validation: invalid, see job_name, retries\n' in printed


def test_rule_about_no_member(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the rule about two members stays in the block below them.

    Both values are ones their own validators accept, so there is no member
    this refusal could honestly be shown beside.
    """
    printed = _dump(capsys, '--set', 'retries=5', '--set',
                    'timeout_seconds=400')
    assert f'validation: invalid\n{TOO_LONG}' in printed
    assert SPACED_NAME not in printed
    assert TOO_MANY not in printed


def test_whole_rule_waits(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the rule about all of them is not applied while one is refused.

    `Config.validate()` would have stopped at the member before it, so an
    editor that reported that rule anyway would be reporting something the
    application never did.
    """
    printed = _dump(capsys, '--set', 'retries=9', '--set',
                    'timeout_seconds=400')
    assert f'    {TOO_MANY}' in printed
    assert 'longest run' not in printed


def test_read_file(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a file whose values satisfy every rule opens and is accepted."""
    printed = _dump(capsys, '-i', data_file('e04_complete.json'))
    assert 'job_name = weekly-archive' in printed
    assert VALID_LINE in printed
    assert printed.endswith(input_tail('e04_complete.json'))


def test_refused_not_saved(tmp_path: Path,
                           capsys: pytest.CaptureFixture[str]) -> None:
    """Test a buffer with a refused member is not written to the file.

    The member says why it was refused and the saving says that nothing was
    written, which are two different things and are both worth saying.
    """
    out_file = tmp_path / 'out.json'
    printed = _dump(capsys, '-o', str(out_file), '--set', 'retries=9',
                    '--save')
    assert f'    {TOO_MANY}' in printed
    assert 'cannot be saved' in printed
    assert not out_file.exists()


def test_corrected_saved(tmp_path: Path,
                         capsys: pytest.CaptureFixture[str]) -> None:
    """Test the same buffer with the member corrected is written."""
    out_file = tmp_path / 'out.json'
    printed = _dump(capsys, '-o', str(out_file), '--set', 'retries=4',
                    '--save')
    assert VALID_LINE in printed
    assert json.loads(out_file.read_text(encoding='UTF-8')) == {
        'job_name': 'nightly-backup', 'retries': 4, 'timeout_seconds': 120}


def test_unknown_member(capsys: pytest.CaptureFixture[str]) -> None:
    """Test setting a member that does not exist is still refused."""
    error = _refused(capsys, '--ui', 'dump', '--set', 'missing=1')
    assert 'missing is not a member' in error


def test_tk_ui_opens(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui tk builds the window and returns when it is closed."""
    open_tk_ui(e04_validated_config.main, monkeypatch)


def test_textual_ui_opens(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui textual starts the application named after the class."""
    assert textual_titles(e04_validated_config.main,
                          monkeypatch) == ['ValidatedConfig']


def test_textual_ui_edited(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui textual shows an edit that --set made before it started."""
    assert textual_titles(e04_validated_config.main, monkeypatch, '--set',
                          'retries=3') == ['ValidatedConfig *']
