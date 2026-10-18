#! /usr/bin/env python3
"""Tests for example e18_declared_types.

What this example adds is the declaration of a member as a source of its type,
so what is asserted here is the two things a value cannot say: what a member
that holds nothing is for, and that a whole number written as the default of a
member holding a number does not make it a whole number member. The rest is
choosing between the types a member is declared to allow: the pair of states
an optional member has, that the two of them really are two different files,
and a member that may hold a number or a text.
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

INFERRED = ('    The type is taken from the value, because nothing declared '
            'says one the editor can use.')
"""What it says below that member about the type shown on its row."""

MAY_HOLD_NOTHING = '    Declared as str | None.\n'
"""What it says below a member declared `Optional[str]` about its type."""

MAY_BE_OMITTED = ('    Declared as str | None. It may be left out of the '
                  'file.\n')
"""What it says below such a member that is also left out of the file."""

DATA_NAME = 'e18_report.json'
"""Input file of this example, holding the mirror of the declared values."""


def _dump(capsys: pytest.CaptureFixture[str], *settings: str) -> str:
    """Run this example with `--ui dump` and return what it printed.

    The explanations are left showing, because the line that says what a
    member is declared as is one of them and is what this example is about.
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
    assert printed.startswith(f'{HEAD}\ntitle: str = Quarterly report')
    assert printed.endswith(f'validation: valid\n{DUMP_TAIL}')


def test_declared_number(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a member declared to hold a number says so, whatever it holds.

    Its default is written `0`, which is a whole number, so the type on its
    row is what the value on its own gets wrong.
    """
    assert '\nthreshold: float = 0\n' in _dump(capsys)


def test_nothing_says_kind(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a member holding nothing says what it would hold, and no more.

    Its row says the `None` it holds now and nothing else, and the line below
    it says the declaration that allows a text as well, which is the last
    thing said about it before the next member.
    """
    printed = _dump(capsys)
    assert '\nsubtitle: None\n' in printed
    assert f'{MAY_HOLD_NOTHING}footer: ' in printed


def test_two_kinds_optional(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a member left out of the file says so after its declaration.

    A member left out of the file is a member holding nothing, written the
    way that class writes it, so it is declared the same way as the other
    kind of optional member and only the sentence after that differs.
    """
    assert MAY_BE_OMITTED in _dump(capsys)


def test_nothing_gets_value(capsys: pytest.CaptureFixture[str]) -> None:
    """Test choosing `str` gives such a member the empty text."""
    printed = _dump(capsys, '--set-type', 'subtitle=str')
    assert 'subtitle: str =  (edited)' in printed


def test_value_gets_cleared(capsys: pytest.CaptureFixture[str]) -> None:
    """Test choosing `None` puts a member holding a value back to nothing."""
    printed = _dump(capsys, '--set-type', 'footer=None')
    assert 'footer: None (edited)' in printed
    assert 'validation: valid' in printed


def test_two_states_two_files(capsys: pytest.CaptureFixture[str],
                              tmp_path: Path) -> None:
    """Test the two states of one member reach the file differently.

    This is the whole reason for telling them apart, and it is the open
    question that design section 4.2 of `doc/detailed_design.md` left open
    until now.
    """
    holding_nothing = _saved(capsys, tmp_path / 'nothing.json')
    holding_empty = _saved(capsys, tmp_path / 'empty.json', '--set-type',
                           'subtitle=str')
    assert holding_nothing['subtitle'] is None
    assert holding_empty['subtitle'] == ''


def test_omitted_is_cleared(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the member the file leaves out has the same two states.

    Which of the two kinds of optional a member is decides what a save writes
    and what the line under the member says, and it decides nothing about the
    types offered: the row stays where it is either way.
    """
    assert 'note: str = Draft, do not circulate' in _dump(capsys)
    assert 'note: None (edited)' in _dump(capsys, '--set-type', 'note=None')


def test_omitted_leaves_file(capsys: pytest.CaptureFixture[str],
                             tmp_path: Path) -> None:
    """Test clearing such a member writes a file with no key for it.

    That is the difference between the two kinds of optional, and it is the
    only difference: `subtitle` cleared is `null` in the file and `note`
    cleared is no key at all.
    """
    written = _saved(capsys, tmp_path / 'no_note.json', '--set-type',
                     'note=None')
    assert 'note' not in written
    assert written['subtitle'] is None


@pytest.mark.parametrize('settings, expected',
                         [(('--set', 'width=5'), 'width: int = 5 (edited)'),
                          (('--set-type', 'width=str'),
                           'width: str = 80 (edited)'),
                          (('--set-type', 'width=str', '--set', 'width=auto'),
                           'width: str = auto (edited)'),
                          (('--set-type', 'width=str', '--set-type',
                            'width=int'), 'width: int = 80\n')])
def test_two_types(capsys: pytest.CaptureFixture[str],
                   settings: tuple[str, ...], expected: str) -> None:
    """Test a member of two types reads its text by the type chosen.

    Switching keeps what still fits: the number `80` is the text `80` and
    back again, and a text that is no number is not one once `int` is chosen.
    The options are applied in the order the user would work in, so every
    `--set-type` comes before every `--set`.
    """
    assert expected in _dump(capsys, *settings)


def test_pass_says_type(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a text typed while `int` is chosen is shown as text after a pass.

    Typing does not choose a type, and the application decides what it
    accepts: `config_as_json` checks no value against its annotation, so the
    pass accepts the text and the editor shows the type it was given.
    """
    printed = _dump(capsys, '--set', 'width=auto')
    assert 'width: str = auto (edited)' in printed
    assert 'validation: valid' in printed


def test_type_reaches_file(capsys: pytest.CaptureFixture[str],
                           tmp_path: Path) -> None:
    """Test the type chosen is the type the file holds the value as."""
    assert _saved(capsys, tmp_path / 'number.json')['width'] == 80
    assert _saved(capsys, tmp_path / 'text.json', '--set-type',
                  'width=str')['width'] == '80'


def test_typed_element_added(capsys: pytest.CaptureFixture[str]) -> None:
    """Test an empty list grows by what the type of its elements says."""
    printed = _dump(capsys, '--add', 'tags', '--set', 'tags.0=urgent')
    assert 'tags: list[str], 1 element (edited)' in printed
    assert '    0: str = urgent (edited)' in printed


def test_no_annotation(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the member with no annotation is still one nothing can be added to.

    It is the one way left to reach that state with a member a JSON file can
    hold, which is the moral of this whole example: annotate the members of a
    configuration class. The type on its row is the one taken from the empty
    list it holds, and the line below the row says so.
    """
    printed = _dump(capsys)
    assert '\nspare: list, 0 elements\n' in printed
    assert f'{INFERRED}\n{NO_ANNOTATION}' in printed
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
    assert 'validation: valid' in _dump(capsys, '--set-type', 'footer=None')


def test_file_holds_states(capsys: pytest.CaptureFixture[str]) -> None:
    """Test both states of an optional member survive a round trip.

    The file holds the mirror of what the class declares, so the empty text
    and the nothing at all have changed places. The member the file does not
    hold at all comes back holding nothing, which is the state that a file
    with no key for it means, and it has a row to say so on. The member of two
    types holds the one the file holds a value of.
    """
    printed = _dump(capsys, '-i', data_file(DATA_NAME))
    assert 'subtitle: str = \n' in printed
    assert '\nfooter: None\n' in printed
    assert '\nnote: None\n' in printed
    assert '\nwidth: str = auto\n' in printed


def test_tk_shows_it(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the Tk backend opens on this example without failing."""
    open_tk_ui(e18_declared_types.main, monkeypatch, '--set-type',
               'subtitle=str')


def test_textual_shows_it(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the Textual backend opens on this example and can be left."""
    titles = textual_titles(e18_declared_types.main, monkeypatch, '--set-type',
                            'footer=None')
    assert titles == ['ReportConfig *']
