#! /usr/bin/env python3
"""Tests for example e09_nested_config.

What this example adds is the nested configuration object as a node of its
own, so most of what is asserted here is a block of lines: what the row of
such an object says, what its own class says below it, and what is indented
under it.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import json
import pytest
from edit_cfg_json import EditModel
from example import e09_nested_config
from example.e09_nested_config import CourseExportConfig, DESCRIPTIONS, \
    OUTPUT_FORMATS, SAME_FILE_REFUSAL, TableOutputConfig
from .helpers import DUMP_TAIL, TEXT_LINE, data_file, dump, head, \
    input_tail, open_tk_ui, refused, textual_titles

HEAD = head(CourseExportConfig())
"""The lines that every dump of this example begins with."""

OWN_VALID = ' [valid on its own]'
"""What an object that is a configuration on its own says.

Every dump of an example validates the buffer before it prints it, so every
nested object of a dump has been asked about itself. It is written out here
rather than read from the core, in the same way as every other text these
tests expect.
"""

OWN_REFUSED = ' [refused on its own]'
"""What an object that its own class refuses says instead."""

AUDIT_FILE = 'advanced-participants.csv'
"""The file name that both outputs are given, to be refused for it."""

OUTPUT_DOC = EditModel(TableOutputConfig()).docstring
"""The whole docstring of the nested class, as an open object shows it."""

OUTPUT_SUMMARY = EditModel(TableOutputConfig()).summary
"""The one line of it that a folded object shows instead."""

ABOUT_PARTICIPANT = DESCRIPTIONS[('participant_output',)]
"""What this example says about its mandatory nested object."""

ABOUT_FILE_NAME = DESCRIPTIONS[('participant_output', 'file_name')]
"""What it says about one member inside that object."""

ABOUT_AUDIT = DESCRIPTIONS[('audit_output',)]
"""What it says about its optional nested object."""

PARTICIPANT_LINES = [
    f'participant_output: TableOutputConfig{OWN_VALID}',
    f'    {ABOUT_PARTICIPANT}',
    *[f'    {line}'.rstrip() for line in OUTPUT_DOC.split('\n')],
    '    file_name = participants.csv', f'        {ABOUT_FILE_NAME}',
    f'    {TEXT_LINE}', '    output_format = CSV', f'    {TEXT_LINE}',
    '    encoding = utf-8', f'    {TEXT_LINE}']
"""Every line that the mandatory nested object of this example is shown as.

The row says the class and not how many entries the dict has, and then what it
is on its own, which is what asking that object about its own values found.
What the application said about the object comes first below it, the docstring
of that class comes after that, and then its own members in the order that
class declares them rather than the sorted order the file has.
"""

FOLDED_PARTICIPANT = [
    f'participant_output: TableOutputConfig (folded){OWN_VALID}',
    f'    {ABOUT_PARTICIPANT}', f'    {OUTPUT_SUMMARY}']
"""What the same object says when it is folded away.

The summary of its class rather than the whole docstring, because an object
that is showing less of itself says less about itself.
"""

MISSING_AUDIT = 'audit_output: no TableOutputConfig'
"""How a declared member that holds no object at all is shown."""


def _dump(capsys: pytest.CaptureFixture[str], *settings: str) -> str:
    """Run this example with `--ui dump` and return what it printed."""
    return dump(e09_nested_config.main, capsys, *settings)


def _refused(capsys: pytest.CaptureFixture[str], *arguments: str) -> str:
    """Run this example, expect it to refuse, and return its error text."""
    return refused(e09_nested_config.main, capsys, *arguments)


def test_descriptions_real() -> None:
    """Test every selector of this example addresses something it has."""
    declared = set(vars(CourseExportConfig()))
    assert {path[0] for path in DESCRIPTIONS} <= declared


def test_nested_is_a_node(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a nested object is shown as its class with its own members."""
    printed = _dump(capsys)
    assert printed.startswith(f'{HEAD}\ncourse_name = python-intro')
    assert '\n'.join(PARTICIPANT_LINES) in printed
    assert printed.endswith(f'validation: valid\n{DUMP_TAIL}')


def test_folded_says_summary(capsys: pytest.CaptureFixture[str]) -> None:
    """Test folding a nested object leaves the summary of its class."""
    printed = _dump(capsys, '--fold', 'participant_output')
    assert '\n'.join(FOLDED_PARTICIPANT) in printed
    assert 'file_name = participants.csv' not in printed


def test_fold_key_folds_all(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the fold key reaches a nested object like any other node."""
    printed = _dump(capsys, '--toggle-fold')
    assert f'participant_output: TableOutputConfig (folded){OWN_VALID}' \
        in printed
    assert 'output_format' not in printed


def test_missing_object(capsys: pytest.CaptureFixture[str]) -> None:
    """Test an optional member holding no object says which class is gone."""
    printed = _dump(capsys)
    assert MISSING_AUDIT in printed
    assert f'{MISSING_AUDIT}\n    {ABOUT_AUDIT}' in printed


def test_missing_not_edited(capsys: pytest.CaptureFixture[str]) -> None:
    """Test no text can be typed into a member that holds no object."""
    error = _refused(capsys, '--ui', 'dump', '--set', 'audit_output=x')
    assert 'audit_output is not a value that can be edited' in error


def test_object_not_edited(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a nested object is edited through its rows and not as one."""
    error = _refused(capsys, '--ui', 'dump', '--set', 'participant_output={}')
    assert 'participant_output is not a value that can be edited' in error


def test_edit_inside_object(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a member of a nested object is edited by the path to it."""
    printed = _dump(capsys, '--set', 'participant_output.encoding=latin-1')
    assert f'participant_output: TableOutputConfig (edited){OWN_VALID}' \
        in printed
    assert '    encoding = latin-1 (edited)' in printed
    assert 'validation: valid' in printed


def test_nested_validator(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a validator of the nested class rewrites what was typed.

    The plan that ran is the nested class's own, because that is the class
    that owns the value, and the rewrite is marked at the member and at the
    object holding it.
    """
    printed = _dump(capsys, '--set', 'participant_output.output_format=txt')
    assert '    output_format = TXT (edited) (changed by validator)' in printed
    assert 'participant_output: TableOutputConfig (edited) ' \
        f'(changed by validator){OWN_VALID}' in printed


def test_nested_refusal(capsys: pytest.CaptureFixture[str]) -> None:
    """Test what a validator of the nested class refuses is shown at it.

    Asking that object about its own values is what reaches the member, which
    reading the whole configuration cannot: a nested object validates itself
    while the configuration around it is parsed, and there is then no object
    left to ask which of its members was refused.
    """
    printed = _dump(capsys, '--set', 'participant_output.output_format=xml')
    assert f'participant_output: TableOutputConfig (edited){OWN_REFUSED}' \
        in printed
    assert 'validation: invalid, see participant_output.output_format' \
        in printed
    # The refusal is on the line below that member, indented under it, which
    # is where what is wrong with a member is shown.
    assert '    output_format = xml (edited)\n        ' in printed
    assert ', '.join(OUTPUT_FORMATS) in printed


def test_valid_object_refused(capsys: pytest.CaptureFixture[str]) -> None:
    """Test an object valid on its own inside a configuration that is not.

    This is what the two states are kept apart for, and it is the one way a
    badge could be misread: the rule that refuses this configuration is about
    both outputs and therefore about neither, so each of them is a perfectly
    good `TableOutputConfig` while the file cannot be written at all.
    """
    printed = _dump(capsys, '-i', data_file('e09_with_audit.json'), '--set',
                    f'audit_output.file_name={AUDIT_FILE}')
    assert printed.count(OWN_VALID) == 2
    assert OWN_REFUSED not in printed
    assert 'validation: invalid' in printed
    assert SAME_FILE_REFUSAL.format(name=AUDIT_FILE) in printed


def test_read_file(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a file that holds the optional object fills it with rows."""
    printed = _dump(capsys, '-i', data_file('e09_with_audit.json'))
    assert f'audit_output: TableOutputConfig{OWN_VALID}\n' in printed
    assert '    file_name = advanced-audit.txt' in printed
    assert MISSING_AUDIT not in printed
    assert printed.endswith(input_tail('e09_with_audit.json'))


def test_save_inside_object(tmp_path: Path,
                            capsys: pytest.CaptureFixture[str]) -> None:
    """Test a value edited inside a nested object reaches the file."""
    out_file = tmp_path / 'out.json'
    _dump(capsys, '-o', str(out_file), '--save', '--set',
          'participant_output.file_name=other.csv')
    written = json.loads(out_file.read_text(encoding='UTF-8'))
    assert written['participant_output']['file_name'] == 'other.csv'
    assert written['audit_output'] is None


def test_tk_ui_opens(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui tk builds the window and returns when it is closed."""
    open_tk_ui(e09_nested_config.main, monkeypatch)


def test_textual_ui_opens(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui textual starts the application named after the class."""
    assert textual_titles(e09_nested_config.main,
                          monkeypatch) == ['CourseExportConfig']
