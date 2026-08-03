#! /usr/bin/env python3
"""Tests for example e02_enum_config.

The example declares no validator at all, so everything asserted here is
the checking that comes with declaring a member as an enum and telling
`config_as_json` how to read one back.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from io import StringIO
import json
import pytest
from example import e02_enum_config
from example.e02_enum_config import AvailableCompetence, EnumConfig, \
    NeededCompetence
from .helpers import DUMP_TAIL, data_file, dump, head, input_tail, \
    open_tk_ui, refused, textual_titles

VALID_LINE = 'validation: valid'
"""Line that `--ui dump` ends with for a buffer the example accepts."""

VALID_END = f'{VALID_LINE}\n{DUMP_TAIL}'
"""How a dump of an accepted buffer with no output file ends."""

FILLED_LINE = ('This file did not hold every value. What it left out was '
               'filled in from the defaults, and is marked.')
"""What the example says about a file that leaves a value out."""

HEAD = head(EnumConfig())
"""The lines that every dump of this example begins with."""

EDITED_HEAD = head(EnumConfig(), edited=True)
"""The same lines while the buffer holds something worth saving."""

NAMES_LINE = '    One of: MECHANICAL, ELECTRICAL, ELECTRONIC.'
"""The names of the enum, which the editor reads from the enum class.

Both enums of this example have the same three names, so one line does for
either of them. It is indented, because it belongs to the member above it.
"""

NEEDED_ABOUT = ('    The competence that a task needs, as an ordinary enum.\n'
                f'{NAMES_LINE}')
"""What the editor says about the first member, from its enum class alone.

This example passes no description mapping at all, so every line below a
member is read from the type of that member.
"""

AVAILABLE_ABOUT = ('    The competence that is available, as an int enum.\n'
                   f'{NAMES_LINE}')
"""What the editor says about the second member, from its enum class."""

NEEDED_LINES = f'needed = {{value}}\n{NEEDED_ABOUT}'
"""How the first member of this example is shown, with its value filled in."""

AVAILABLE_LINES = f'available = {{value}}\n{AVAILABLE_ABOUT}'
"""How the second member is shown, with its value filled in."""

EXPECTED_DUMP = (f'{HEAD}\n{NEEDED_LINES.format(value="ELECTRICAL")}\n'
                 f'{AVAILABLE_LINES.format(value="MECHANICAL")}\n'
                 f'{VALID_END}')
"""Text that `--ui dump` is expected to print for the default values."""

REFUSAL_FORM = '    {text} is not one of: MECHANICAL, ELECTRICAL, ELECTRONIC'
"""What the editor says about text that names no member of the enum.

It is the sentence the conversion of that one member raised, below that one
member, and nothing else. What `config_as_json` prints around it is about
JSON that could not be loaded, which is right for a program reading a file
and wrong for a person editing a field.
"""

REFUSED_VERDICT = 'validation: invalid, see {member}'
"""What the verdict says when one member was refused and named."""

WRITTEN_TEXT = '{"needed": "ELECTRONIC", "available": "ELECTRICAL"}'
"""A configuration file of this example, as its two names."""

REFUSED_SETTINGS = [('ambiguous prefix', 'needed=ELECT'),
                    ('no such member', 'needed=HYDRAULIC'),
                    ('number instead of name', 'available=2'),
                    ('empty field', 'needed=')]
"""Every way of typing something that names no member of the enum.

The first item of each is the name of the case, which pytest uses to
identify it. The ambiguous prefix is the interesting one: `ELECTRICAL` and
`ELECTRONIC` both begin with `ELECT`, so it names two members and therefore
none.
"""


def _dump(capsys: pytest.CaptureFixture[str], *settings: str) -> str:
    """Run this example with `--ui dump` and return what it printed."""
    return dump(e02_enum_config.main, capsys, *settings)


def _refused(capsys: pytest.CaptureFixture[str], *arguments: str) -> str:
    """Run this example, expect it to refuse, and return its error text."""
    return refused(e02_enum_config.main, capsys, *arguments)


def test_dump(capsys: pytest.CaptureFixture[str]) -> None:
    """Test --ui dump shows both enums as the names of their members."""
    assert _dump(capsys) == EXPECTED_DUMP


def test_set_enum(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a full member name is accepted and leaves nothing to explain."""
    assert _dump(capsys, '--set', 'needed=ELECTRONIC') == (
        f'{EDITED_HEAD}\n{NEEDED_LINES.format(value="ELECTRONIC (edited)")}\n'
        f'{AVAILABLE_LINES.format(value="MECHANICAL")}\n{VALID_END}')


@pytest.mark.parametrize('typed, whole',
                         [('MECH', 'MECHANICAL'),
                          ('mechanical', 'MECHANICAL'),
                          ('electro', 'ELECTRONIC')])
def test_completed(typed: str, whole: str,
                   capsys: pytest.CaptureFixture[str]) -> None:
    """Test text that is enough to name one member is completed to it.

    The completed name is marked as changed by a validator, because the
    buffer no longer holds what was typed into it.
    """
    shown = f'{whole} (edited) (changed by validator)'
    assert _dump(capsys, '--set', f'needed={typed}') == \
        (f'{EDITED_HEAD}\n{NEEDED_LINES.format(value=shown)}\n'
         f'{AVAILABLE_LINES.format(value="MECHANICAL")}\n{VALID_END}')


def test_set_int_enum(capsys: pytest.CaptureFixture[str]) -> None:
    """Test an int enum member is edited exactly like an ordinary enum."""
    shown = 'ELECTRONIC (edited) (changed by validator)'
    assert _dump(capsys, '--set', 'available=electronic') == \
        (f'{EDITED_HEAD}\n{NEEDED_LINES.format(value="ELECTRICAL")}\n'
         f'{AVAILABLE_LINES.format(value=shown)}\n{VALID_END}')


@pytest.mark.parametrize('case, setting', REFUSED_SETTINGS)
def test_refused_name(case: str, setting: str,
                      capsys: pytest.CaptureFixture[str]) -> None:
    """Test text naming no member is refused, and the text is kept."""
    printed = _dump(capsys, '--set', setting)
    member, _, text = setting.partition('=')
    assert f'{member} = {text} (edited)' in printed, case
    assert REFUSAL_FORM.format(text=text) in printed, case
    assert REFUSED_VERDICT.format(member=member) in printed, case
    assert 'failed to load JSON' not in printed, case


def test_int_enum_written() -> None:
    """Test the int enum reaches the file as its name and not its number.

    This is the case the write-side conversion of `config_as_json` exists
    for. An `IntEnum` member is an `int`, so Python's own JSON encoder would
    write `1` here, and no reader of the file could tell that number from a
    number that was only ever a number.
    """
    written = json.loads(EnumConfig().as_json_string(stderr_file=StringIO()))
    assert written['available'] == 'MECHANICAL'


def test_parse_gives_enum() -> None:
    """Test the name in the file becomes an enum member and not a string.

    This is what `parse_converters()` is declared for. Without it the load
    would succeed just as quietly and leave the text in the attribute.
    """
    config = EnumConfig(from_json_data_text=WRITTEN_TEXT)
    assert config.needed is NeededCompetence.ELECTRONIC
    assert config.available is AvailableCompetence.ELECTRICAL


def test_read_enum_names(capsys: pytest.CaptureFixture[str]) -> None:
    """Test both enum members are read from a file as their names."""
    assert _dump(capsys, '-i', data_file('e02_complete.json')) == (
        f'{HEAD}\n{NEEDED_LINES.format(value="MECHANICAL")}\n'
        f'{AVAILABLE_LINES.format(value="ELECTRONIC")}\n{VALID_LINE}\n'
        f'{input_tail("e02_complete.json")}')


def test_enum_filled_in(capsys: pytest.CaptureFixture[str]) -> None:
    """Test an enum member the file leaves out gets its declared default."""
    filled = 'MECHANICAL (filled from default)'
    assert _dump(capsys, '-i', data_file('e02_incomplete.json')) == (
        f'{HEAD}\n{FILLED_LINE}\n{NEEDED_LINES.format(value="ELECTRONIC")}\n'
        f'{AVAILABLE_LINES.format(value=filled)}\n{VALID_LINE}\n'
        f'{input_tail("e02_incomplete.json")}')


def test_bad_enum_in_file(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a name that is no enum member makes the file unopenable.

    This is where a load differs from an edit. The same `ELECT` typed into a
    field is kept, because a name is not a name of a member for most of the
    time it takes to type it. In a file nothing is half typed, so the file
    cannot be read as configuration at all.
    """
    error = _refused(capsys, '--ui', 'dump', '-i',
                     data_file('e02_bad_enum.json'))
    assert 'does not hold configuration that can be read' in error
    assert 'ELECT is not one of: MECHANICAL, ELECTRICAL, ELECTRONIC' in error


def test_tk_ui_opens(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui tk builds the window and returns when it is closed."""
    open_tk_ui(e02_enum_config.main, monkeypatch)


def test_textual_ui_opens(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui textual starts the application named after the class."""
    assert textual_titles(e02_enum_config.main, monkeypatch) == ['EnumConfig']


def test_textual_ui_edited(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui textual shows an edit that --set made before it started."""
    assert textual_titles(e02_enum_config.main, monkeypatch, '--set',
                          'needed=MECHANICAL') == ['EnumConfig *']
