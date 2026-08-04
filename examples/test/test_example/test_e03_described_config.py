#! /usr/bin/env python3
"""Tests for example e03_described_config.

What this example adds is text about the configuration and about its members,
so most of what is asserted here is the whole dump: that is how a member the
mapping deliberately says nothing about is shown to have nothing under it.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest
from example import e03_described_config
from example.e03_described_config import DESCRIPTIONS, DescribedConfig
from .helpers import DUMP_TAIL, TEXT_LINE, WHOLE_LINE, data_file, dump, \
    head, input_tail, open_tk_ui, refused, textual_titles

VALID_LINE = 'validation: valid'
"""Line that `--ui dump` ends with for a buffer the example accepts."""

VALID_END = f'{VALID_LINE}\n{DUMP_TAIL}'
"""How a dump of an accepted buffer with no output file ends."""

HEAD = head(DescribedConfig())
"""The lines that every dump of this example begins with."""

EDITED_HEAD = head(DescribedConfig(), edited=True)
"""The same lines while the buffer holds something worth saving."""

SUMMARY = 'A configuration that explains itself to whoever edits it.'
"""The first paragraph of the docstring of the class of this example.

It is written out rather than read from the class, because it is what has to
be left when the rest of the explanatory text is hidden, and a test that read
it from the same place the code does could not tell the summary from the whole
docstring.
"""

ABOUT_NAME = DESCRIPTIONS[('project_name',)]
"""What this example says about its first member."""

ABOUT_ITEMS = DESCRIPTIONS[('max_items',)]
"""What this example says about its number member."""

ABOUT_PRIORITY = DESCRIPTIONS[('priority',)]
"""What this example says about its enum member."""

PRIORITY_TYPE = ['    How urgent the work described by a configuration is.',
                 '    One of: LOW, ROUTINE, URGENT.']
"""What the *type* of the enum member says about it, below what the
application says.

The names come from the enum class, which is a fact about the type of that
member and not a constraint read out of a validator. That is the difference
between this member and `max_items`, whose range lives inside a validator and
is therefore explained by the application in words.
"""

VALUE_LINES = ['project_name = Example project', f'    {ABOUT_NAME}',
               TEXT_LINE, 'report_file = report.md', TEXT_LINE,
               'max_items = 20', f'    {ABOUT_ITEMS}', WHOLE_LINE,
               'priority = ROUTINE', f'    {ABOUT_PRIORITY}', *PRIORITY_TYPE]
"""Every line that the default values of this example are shown as.

`report_file` has nothing below it from the mapping of this example, which says
nothing about that member, and it still says what kind of value it holds: that
is the one thing the editor knows about every member without being told. The
enum member says the names it accepts instead, because they say what kind of
value it holds and say it better.
"""

HIDDEN_LINES = ['project_name = Example project', 'report_file = report.md',
                'max_items = 20', 'priority = ROUTINE']
"""The same lines with the explanations hidden."""


def _dump(capsys: pytest.CaptureFixture[str], *settings: str) -> str:
    """Run this example with `--ui dump` and return what it printed."""
    return dump(e03_described_config.main, capsys, *settings)


def _refused(capsys: pytest.CaptureFixture[str], *arguments: str) -> str:
    """Run this example, expect it to refuse, and return its error text."""
    return refused(e03_described_config.main, capsys, *arguments)


def test_dump() -> None:
    """Test the description mapping of this example describes real members.

    A selector that names no member of the configuration would describe
    nothing at all, and nothing would say so: the editor never refuses one,
    because a wrong description is a cosmetic mistake. This is what makes
    sure the example itself has none.
    """
    declared = {(name,) for name in vars(DescribedConfig())}
    assert set(DESCRIPTIONS) <= declared
    assert ('report_file',) not in DESCRIPTIONS


def test_described_dump(capsys: pytest.CaptureFixture[str]) -> None:
    """Test --ui dump explains the configuration and each described member."""
    lines = '\n'.join(VALUE_LINES)
    assert _dump(capsys) == f'{HEAD}\n{lines}\n{VALID_END}'


def test_hidden_dump(capsys: pytest.CaptureFixture[str]) -> None:
    """Test --toggle-explain leaves the summary and takes the rest away.

    That is what the explain key does in the two graphical backends, and the
    summary is one line for the whole configuration, so it stays.
    """
    lines = '\n'.join(HIDDEN_LINES)
    assert _dump(capsys, '--toggle-explain') == (
        f'DescribedConfig - {SUMMARY}\n{lines}\n{VALID_END}')


def test_edit_described(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a described member is edited exactly like any other member."""
    printed = _dump(capsys, '--set', 'max_items=5')
    assert printed.startswith(EDITED_HEAD)
    assert f'max_items = 5 (edited)\n    {ABOUT_ITEMS}\n{WHOLE_LINE}' in \
        printed
    assert VALID_LINE in printed


def test_refused_value(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the range that the description explains is really enforced.

    The description says the range in words and the validation plan enforces
    it, and the editor turns neither of them into the other. What the
    application refused is below both of them, because the description says
    what the member is for and the refusal is the thing to act on.
    """
    printed = _dump(capsys, '--set', 'max_items=500')
    assert (f'max_items = 500 (edited)\n    {ABOUT_ITEMS}\n{WHOLE_LINE}\n'
            '    Invalid configuration: Value 500 for max_items is greater '
            'than maximum 100.') in printed
    assert 'validation: invalid, see max_items' in printed


def test_names_from_the_type(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the names of the enum are listed under what the application says.

    The application deliberately does not list them: they are the type of
    that member, so the editor reads them from the enum class, and writing
    them in two places is how one of the two comes to be wrong.
    """
    lines = '\n'.join(['priority = ROUTINE', f'    {ABOUT_PRIORITY}',
                       *PRIORITY_TYPE])
    assert lines in _dump(capsys)
    assert 'LOW, ROUTINE, URGENT' not in ABOUT_PRIORITY


def test_refused_enum(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a name that no member of the enum has is refused at that member.

    `HI` begins none of the three names, so it means nothing at all, and the
    conversion of that one member is what says so. The message is the one the
    conversion raised and not the one about JSON that could not be loaded.
    """
    printed = _dump(capsys, '--set', 'priority=HI')
    assert '    HI is not one of: LOW, ROUTINE, URGENT' in printed
    assert 'validation: invalid, see priority' in printed
    assert 'failed to load JSON' not in printed


def test_completed_enum(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the enum member is completed and marked, and still described."""
    printed = _dump(capsys, '--set', 'priority=URG')
    assert 'priority = URGENT (edited) (changed by validator)' in printed
    assert f'    {ABOUT_PRIORITY}' in printed


def test_undescribed_member(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a member the mapping says nothing about says what it holds.

    That is all it says, because the mapping of this example describes three of
    its four members and the editor does not invent a fourth description. What
    it does know is the kind of every value, and it says that.
    """
    printed = _dump(capsys)
    assert f'report_file = report.md\n{TEXT_LINE}\nmax_items' in printed
    assert ABOUT_NAME not in printed.split('report_file')[1]


def test_read_file(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the values of a file are shown with the same descriptions.

    A description is text about a member and not part of it, so a file of
    this example holds exactly what a file of any other example holds.
    """
    printed = _dump(capsys, '-i', data_file('e03_complete.json'))
    assert printed.startswith(HEAD)
    assert f'project_name = From a file\n    {ABOUT_NAME}\n{TEXT_LINE}' in \
        printed
    assert 'priority = URGENT' in printed
    assert printed.endswith(input_tail('e03_complete.json'))


def test_unknown_member(capsys: pytest.CaptureFixture[str]) -> None:
    """Test setting a member that does not exist is still refused."""
    error = _refused(capsys, '--ui', 'dump', '--set', 'missing=1')
    assert 'missing is not a member' in error


def test_tk_ui_opens(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui tk builds the window and returns when it is closed."""
    open_tk_ui(e03_described_config.main, monkeypatch)


def test_textual_ui_opens(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui textual starts the application named after the class."""
    assert textual_titles(e03_described_config.main,
                          monkeypatch) == ['DescribedConfig']


def test_textual_ui_hidden(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --toggle-explain reaches the editor before it is shown."""
    assert textual_titles(e03_described_config.main, monkeypatch,
                          '--toggle-explain') == ['DescribedConfig']
