#! /usr/bin/env python3
"""Tests for example e19_omitted_members.

What this example adds is the members a class leaves out of the file
altogether. Nothing at all is written for one of them while it holds nothing,
so what is asserted here is first that every one of them has a row, and then
what each of them offers: a text and a list are given a value, a nested
configuration object is built, and a dict says why it cannot be.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import pytest
from example import e19_omitted_members
from example.e19_omitted_members import ReportConfig
from .helpers import DUMP_TAIL, data_file, dump, head, open_tk_ui, \
    refused, saved_members, textual_titles

HEAD = head(ReportConfig())
"""The lines that every dump of this example begins with."""

NO_DICT = ('    A dict written for a member that holds none is refused by the '
           'configuration class itself, which matches it against the dict the '
           'member holds. So this member cannot be given one.')
"""What it says below the one member that cannot be given a value.

It is written out here rather than read from an internal module of the core, in
the same way as every other text these tests expect.
"""

MAY_BE_OMITTED = 'It may be left out of the file.'
"""What the type of every member of this class but the title says."""

DATA_NAME = 'e19_report.json'
"""Input file of this example, which holds nothing but the title."""

MEMBERS = ['title', 'note', 'audit', 'extra_hosts', 'limits', 'legacy']
"""The members of this configuration, in the order the class declares them."""


def _dump(capsys: pytest.CaptureFixture[str], *settings: str) -> str:
    """Run this example with `--ui dump` and return what it printed.

    The explanations are left showing, because the line that says why a member
    cannot be given a value is one of them.
    """
    return dump(e19_omitted_members.main, capsys, *settings)


def _saved(capsys: pytest.CaptureFixture[str], out_file: Path,
           *settings: str) -> dict[str, object]:
    """Run this example, save it, and return what reached the file."""
    return saved_members(e19_omitted_members.main, capsys, out_file,
                         'ReportConfig', *settings)


def test_every_member_a_row(capsys: pytest.CaptureFixture[str]) -> None:
    """Test every member left out of the file has a row all the same.

    That is the whole of this example: a member the file holds no key for is
    one the editor asks the configuration object about, and a member with no
    row could never be given a value.
    """
    printed = _dump(capsys)
    assert printed.startswith(f'{HEAD}\ntitle = Quarterly report')
    for name in MEMBERS[1:]:
        assert f'\n{name}' in printed
    assert printed.count(MAY_BE_OMITTED) == len(MEMBERS) - 1


def test_starts_as_nothing(capsys: pytest.CaptureFixture[str]) -> None:
    """Test each of those members starts in the state that holds nothing."""
    printed = _dump(capsys)
    assert 'note: no value' in printed
    assert 'audit: no AuditConfig' in printed
    assert 'extra_hosts: no value' in printed
    assert 'validation: valid' in printed
    assert printed.endswith(f'validation: valid\n{DUMP_TAIL}')


def test_object_from_class(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the member holding no object is given one of the declared class.

    This is the case that had no row at all before, so it is the one worth
    asserting all of: the row becomes the class, the members of that class
    appear below it, and the object says that it is valid on its own.
    """
    printed = _dump(capsys, '--add', 'audit')
    assert 'audit: AuditConfig (edited) [valid on its own]' in printed
    assert '    destination = audit.log' in printed
    assert '    retries = 2' in printed


def test_object_cleared_again(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the same member is put back to holding no object."""
    printed = _dump(capsys, '--add', 'audit', '--remove', 'audit')
    assert 'audit: no AuditConfig' in printed
    assert '    destination' not in printed
    assert 'validation: valid' in printed


def test_list_two_presses(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a member holding no list is given one, and then an element.

    The first press is the two states of the member and the second is the
    ordinary growing of a list, which is why it is two presses and not a rule
    of its own.
    """
    once = _dump(capsys, '--add', 'extra_hosts')
    assert 'extra_hosts: 0 elements (edited)' in once
    twice = _dump(capsys, '--add', 'extra_hosts', '--add', 'extra_hosts',
                  '--set', 'extra_hosts.0=build-01')
    assert 'extra_hosts: 1 element (edited)' in twice
    assert '    0 = build-01 (edited)' in twice


def test_dict_says_why_not(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the member holding no dict says why it cannot be given one.

    `Config.check_dict_parse` refuses a dict written for a member that holds
    none, so the control would be one that produces a refusal and there is no
    control at all instead.
    """
    assert NO_DICT in _dump(capsys)
    refusal = refused(e19_omitted_members.main, capsys, '--ui', 'dump',
                      '--add', 'limits')
    assert 'Nothing can be added to limits' in refusal


def test_no_annotation_field(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the member with no annotation is an ordinary field showing null.

    Nothing says what it would hold, so it has one state rather than two and
    no control to move between them. It is not left unreachable by that: the
    field takes a value and takes `null` back again.
    """
    printed = _dump(capsys)
    assert 'legacy = null' in printed
    refusal = refused(e19_omitted_members.main, capsys, '--ui', 'dump',
                      '--add', 'legacy')
    assert 'Nothing can be added to legacy' in refusal
    assert 'legacy = kept (edited)' in _dump(capsys, '--set', 'legacy=kept')


def test_two_states_two_files(capsys: pytest.CaptureFixture[str],
                              tmp_path: Path) -> None:
    """Test the file is where the difference between the two states is.

    A member that holds nothing is no key of the file at all, which is what
    `_omit_none_from_json()` means and the whole reason the row has to exist
    without one.
    """
    without = _saved(capsys, tmp_path / 'without.json')
    assert list(without) == ['title']
    with_object = _saved(capsys, tmp_path / 'with.json', '--add', 'audit')
    assert with_object['audit'] == {'destination': 'audit.log', 'retries': 2}


def test_bare_file_read(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a file holding nothing but the title opens with every row.

    It is the same state the declared values start in, reached from a file
    instead, which is what says that the rows come from the configuration
    object and not from what the file happened to hold.
    """
    printed = _dump(capsys, '-i', data_file(DATA_NAME))
    assert 'title = Monthly report' in printed
    assert 'note: no value' in printed
    assert 'audit: no AuditConfig' in printed
    assert 'validation: valid' in printed


def test_application_refuses(capsys: pytest.CaptureFixture[str]) -> None:
    """Test an object the editor made is validated as one from a file is.

    `AuditConfig` refuses more than five retries whoever built the object, so
    what the editor added is no more trusted than what a file held.
    """
    printed = _dump(capsys, '--add', 'audit', '--set', 'audit.retries=9')
    assert 'validation: invalid, see audit.retries' in printed


def test_tk_shows_it(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the Tk backend opens on this example without failing."""
    open_tk_ui(e19_omitted_members.main, monkeypatch, '--add', 'audit')


def test_textual_shows_it(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the Textual backend opens on this example and can be left."""
    titles = textual_titles(e19_omitted_members.main, monkeypatch, '--add',
                            'extra_hosts')
    assert titles == ['ReportConfig *']
