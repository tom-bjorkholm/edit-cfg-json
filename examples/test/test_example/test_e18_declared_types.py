#! /usr/bin/env python3
"""Tests for example e18_declared_types.

What this example adds is the declaration of a member as a source of its type,
so what is asserted here is the two things a value cannot say: what a member
that holds nothing is for, and that a whole number written as the default of a
member holding a number does not make it a whole number member. The rest is
the pair of states an optional member has, and that the two of them really are
two different files.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import pytest
from example import e18_declared_types
from example.e18_declared_types import ReportConfig
from .helpers import DUMP_TAIL, data_file, dump, head, open_tk_ui, \
    refused, saved_members, textual_titles

HEAD = head(ReportConfig())
"""The lines that every dump of this example begins with."""

NO_ANNOTATION = ('    Nothing says what an element of this member would be: '
                 'this class declares no element for it, it holds none, and '
                 'its declared type names nothing the editor can make one '
                 'of.')
"""What it says below the one member that has no annotation.

It is written out here rather than read from an internal module of the core,
in the same way as every other text these tests expect.
"""

MAY_HOLD_NOTHING = 'Text. It may hold nothing at all.'
"""What the type of a member declared `Optional[str]` says about it."""

MAY_BE_OMITTED = 'Text. It may be left out of the file.'
"""What the type of such a member that is also left out of the file says."""

DATA_NAME = 'e18_report.json'
"""Input file of this example, holding the mirror of the declared values."""


def _dump(capsys: pytest.CaptureFixture[str], *settings: str) -> str:
    """Run this example with `--ui dump` and return what it printed.

    The explanations are left showing, because the line that says what kind
    of value a member holds is one of them and is what this example is
    about.
    """
    return dump(e18_declared_types.main, capsys, *settings)


def _saved(capsys: pytest.CaptureFixture[str], out_file: Path,
           *settings: str) -> dict[str, object]:
    """Run this example, save it, and return what reached the file."""
    return saved_members(e18_declared_types.main, capsys, out_file,
                         'ReportConfig', *settings)


def test_starts_as_declared(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the example says what it holds before anything is changed."""
    printed = _dump(capsys)
    assert printed.startswith(f'{HEAD}\ntitle = Quarterly report')
    assert printed.endswith(f'validation: valid\n{DUMP_TAIL}')


def test_declared_number(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a member declared to hold a number says so, whatever it holds.

    Its default is written `0`, which is a whole number, so this is the line
    that the value on its own gets wrong.
    """
    assert 'threshold = 0\n' in _dump(capsys)
    assert '    A number.' in _dump(capsys)


def test_nothing_says_kind(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a member holding nothing says what it would hold, and no more."""
    printed = _dump(capsys)
    assert 'subtitle: no value' in printed
    assert MAY_HOLD_NOTHING in printed


def test_two_kinds_optional(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a member left out of the file says that rather than the other.

    A member left out of the file is a member holding nothing, written the
    way that class writes it, so saying both would say the same thing twice.
    """
    assert MAY_BE_OMITTED in _dump(capsys)


def test_nothing_gets_value(capsys: pytest.CaptureFixture[str]) -> None:
    """Test such a member is given the empty value of the kind declared."""
    printed = _dump(capsys, '--add', 'subtitle')
    assert 'subtitle =  (edited)' in printed


def test_value_gets_cleared(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a member holding a value is put back to holding nothing."""
    printed = _dump(capsys, '--remove', 'footer')
    assert 'footer: no value (edited)' in printed
    assert 'validation: valid' in printed


def test_two_states_two_files(capsys: pytest.CaptureFixture[str],
                              tmp_path: Path) -> None:
    """Test the two states of one member reach the file differently.

    This is the whole reason for telling them apart, and it is the open
    question that design section 4.2 of `doc/detailed_design.md` left open
    until now.
    """
    holding_nothing = _saved(capsys, tmp_path / 'nothing.json')
    holding_empty = _saved(capsys, tmp_path / 'empty.json', '--add',
                           'subtitle')
    assert holding_nothing['subtitle'] is None
    assert holding_empty['subtitle'] == ''


def test_omitted_is_cleared(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the member the file leaves out has the same two states.

    Which of the two kinds of optional a member is decides what a save writes
    and what the line under the member says, and it decides nothing about the
    controls: the row stays where it is either way.
    """
    assert 'note = Draft, do not circulate' in _dump(capsys)
    assert 'note: no value (edited)' in _dump(capsys, '--remove', 'note')


def test_omitted_leaves_file(capsys: pytest.CaptureFixture[str],
                             tmp_path: Path) -> None:
    """Test clearing such a member writes a file with no key for it.

    That is the difference between the two kinds of optional, and it is the
    only difference: `subtitle` cleared is `null` in the file and `note`
    cleared is no key at all.
    """
    written = _saved(capsys, tmp_path / 'no_note.json', '--remove', 'note')
    assert 'note' not in written
    assert written['subtitle'] is None


def test_typed_element_added(capsys: pytest.CaptureFixture[str]) -> None:
    """Test an empty list grows by what the type of its elements says."""
    printed = _dump(capsys, '--add', 'tags', '--set', 'tags.0=urgent')
    assert 'tags: 1 element (edited)' in printed
    assert '    0 = urgent (edited)' in printed


def test_no_annotation(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the member with no annotation is still one nothing can be added to.

    It is the one way left to reach that state with a member a JSON file can
    hold, which is the moral of this whole example: annotate the members of a
    configuration class.
    """
    assert NO_ANNOTATION in _dump(capsys)
    refusal = refused(e18_declared_types.main, capsys, '--ui', 'dump', '--add',
                      'spare')
    assert 'Nothing can be added' in refusal


def test_application_refuses(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the rules of the application reach both states of a member.

    `OptionalMemberValidator` lets nothing through and applies the rule
    inside it to every other value, so a two character footer is refused
    while no footer at all is accepted.
    """
    assert 'validation: invalid, see footer' in _dump(capsys, '--set',
                                                      'footer=ab')
    assert 'validation: valid' in _dump(capsys, '--remove', 'footer')


def test_file_holds_states(capsys: pytest.CaptureFixture[str]) -> None:
    """Test both states of an optional member survive a round trip.

    The file holds the mirror of what the class declares, so the empty text
    and the nothing at all have changed places. The member the file does not
    hold at all comes back holding nothing, which is the state that a file
    with no key for it means, and it has a row to say so on.
    """
    printed = _dump(capsys, '-i', data_file(DATA_NAME))
    assert 'subtitle = \n' in printed
    assert 'footer: no value' in printed
    assert '\nnote: no value' in printed


def test_tk_shows_it(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the Tk backend opens on this example without failing."""
    open_tk_ui(e18_declared_types.main, monkeypatch, '--add', 'subtitle')


def test_textual_shows_it(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the Textual backend opens on this example and can be left."""
    titles = textual_titles(e18_declared_types.main, monkeypatch, '--remove',
                            'footer')
    assert titles == ['ReportConfig *']
