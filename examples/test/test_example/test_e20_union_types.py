#! /usr/bin/env python3
"""Tests for example e20_union_types.

What this example adds is choosing between two containers in the pull-down of
the type of a row, so what is asserted here is the complaint it answers: an
entry that may hold a list of text or a list of lists of text holds the type
its value is, a new entry is given the type the user chooses, and what its own
control then adds is an element of that type. The rest is what switching
does to what an entry held, and the types a file says by its values alone.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import pytest
from example import e20_union_types
from example.e20_union_types import ExportConfig
from .helpers import DUMP_TAIL, data_file, dump, head, open_tk_ui, \
    saved_members, textual_titles

HEAD = head(ExportConfig())
"""The lines that every dump of this example begins with."""

DECLARED = '        Declared as list[str] | list[list[str]].\n'
"""What it says below every entry of the map about its type."""

LISTS = 'list[list[str]]'
"""The second type an entry of the map may hold, as Python spells it."""

NEW_ENTRY = ('--add', 'jira_column_map=Status', '--set-type',
             f'jira_column_map.Status={LISTS}')
"""The command line that adds a column and makes it a list of paths."""

DATA_NAME = 'e20_export.json'
"""Input file of this example, whose entries say their types by value."""


def _dump(capsys: pytest.CaptureFixture[str], *settings: str) -> str:
    """Run this example with `--ui dump` and return what it printed."""
    return dump(e20_union_types.main, capsys, *settings)


def test_value_says_type(capsys: pytest.CaptureFixture[str]) -> None:
    """Test each entry holds the type its value is, and says what it may.

    The column shows the type an entry holds, and the line below it says the
    whole of what it is declared as, because there is more than one.
    """
    printed = _dump(capsys)
    assert printed.startswith(f'{HEAD}\njira_column_map: dict[str, '
                              f'list[str] | {LISTS}], 2 entries\n')
    assert '    Created: list[str], 1 element\n' in printed
    assert f'    People: {LISTS}, 2 elements\n' in printed
    assert printed.count(DECLARED) == 2
    assert printed.endswith(f'validation: valid\n{DUMP_TAIL}')


def test_new_entry_copied(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a new column is a copy of the first, a `list[str]`.

    It is the dict that holds it that is edited, which is what its row says.
    """
    printed = _dump(capsys, '--add', 'jira_column_map=Status')
    assert '3 entries (edited)\n' in printed
    assert '    Status: list[str], 1 element\n' in printed
    assert '        0: str = created\n' in printed


def test_complaint_answered(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a new column is made a list of paths, and given one.

    Choosing the other list gives it the empty list, and its own control then
    adds the empty list of text that an element of a list of lists is.
    """
    chosen = _dump(capsys, *NEW_ENTRY)
    assert f'    Status: {LISTS}, 0 elements (edited)\n' in chosen
    grown = _dump(capsys, *NEW_ENTRY, '--add', 'jira_column_map.Status',
                  '--add', 'jira_column_map.Status.0', '--set',
                  'jira_column_map.Status.0.0=status')
    assert f'    Status: {LISTS}, 1 element (edited)\n' in grown
    assert '        0: list[str], 1 element (edited)\n' in grown
    assert '            0: str = status (edited)\n' in grown
    assert 'validation: valid' in grown


def test_switch_empties(capsys: pytest.CaptureFixture[str]) -> None:
    """Test choosing the other list keeps nothing of what was held."""
    printed = _dump(capsys, '--set-type', 'jira_column_map.People=list[str]')
    assert '    People: list[str], 0 elements (edited)\n' in printed
    assert 'assignee' not in printed


def test_choice_saved(capsys: pytest.CaptureFixture[str],
                      tmp_path: Path) -> None:
    """Test the type chosen is the shape the file is written with."""
    saved = saved_members(e20_union_types.main, capsys, tmp_path / 'out.json',
                          'ExportConfig', *NEW_ENTRY, '--add',
                          'jira_column_map.Status')
    columns = saved['jira_column_map']
    assert isinstance(columns, dict) and columns['Status'] == [[]]


def test_file_says_types(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a file's values say the types its entries hold.

    One path written as a list of paths is a list of lists, and the empty list
    is a value of both and holds the first type the declaration writes.
    """
    printed = _dump(capsys, '-i', data_file(DATA_NAME))
    assert f'    Labels: {LISTS}, 1 element\n' in printed
    assert '    Watchers: list[str], 0 elements\n' in printed
    assert 'separator: str =  / ' in printed


def test_application_refuses(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a value the class refuses is refused, whatever was offered."""
    printed = _dump(capsys, '--set', 'separator=')
    assert 'validation: invalid, see separator' in printed


def test_tk_shows_it(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the Tk backend opens on this example without failing."""
    open_tk_ui(e20_union_types.main, monkeypatch, *NEW_ENTRY)


def test_textual_shows_it(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the Textual backend opens on this example and can be left."""
    titles = textual_titles(e20_union_types.main, monkeypatch, *NEW_ENTRY)
    assert titles == ['ExportConfig *']
