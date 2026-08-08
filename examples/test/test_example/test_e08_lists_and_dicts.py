#! /usr/bin/env python3
"""Tests for example e08_lists_and_dicts.

What this example adds is the tree of rows that a list or a dict becomes, so
most of what is asserted here is a block of lines rather than one: what a
container says about itself, and what is indented below it.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest
from example import e08_lists_and_dicts
from example.e08_lists_and_dicts import ContainerConfig, DESCRIPTIONS, \
    LABEL_COUNT, LONGEST_DELAY
from .helpers import DUMP_TAIL, TEXT_LINE, WHOLE_LINE, data_file, dump, head, \
    input_tail, open_tk_ui, refused, textual_titles

HEAD = head(ContainerConfig())
"""The lines that every dump of this example begins with."""

ABOUT_DELAYS = DESCRIPTIONS[('retry_delays',)]
"""What this example says about its list of numbers."""

ABOUT_ONE_DELAY = DESCRIPTIONS[('retry_delays', '[')]
"""What it says about every element of that list, once, for all of them."""

ABOUT_PORTS = DESCRIPTIONS[('ports',)]
"""What it says about its dict of numbers."""

ABOUT_HTTPS = DESCRIPTIONS[('ports', 'https')]
"""What it says about one value inside that dict."""

DELAY_LINES = ['retry_delays: 3 elements', f'    {ABOUT_DELAYS}',
               '    0 = 1', f'        {ABOUT_ONE_DELAY}',
               f'    {WHOLE_LINE}', '    1 = 5',
               f'        {ABOUT_ONE_DELAY}', f'    {WHOLE_LINE}',
               '    2 = 15', f'        {ABOUT_ONE_DELAY}',
               f'    {WHOLE_LINE}']
"""Every line that the list of numbers of this example is shown as.

The description of one element is under each of them, because one selector
with the `'['` step reaches every element of the list. What kind of value it
is follows, indented as everything below a node is, once more for the
container it is inside.
"""

PORT_LINES = ['ports: 2 entries', f'    {ABOUT_PORTS}', '    http = 80',
              f'    {WHOLE_LINE}', '    https = 443',
              f'        {ABOUT_HTTPS}', f'    {WHOLE_LINE}']
"""Every line that the dict of this example is shown as.

Its keys are in the order the file has them, which is the sorted one: a
dictionary key has no declaration to be read from, and the order a save
writes is the order that is shown.
"""

FOLDED_LABELS = f'many_labels: {LABEL_COUNT} elements (folded)'
"""How the long list of this example is shown when the editor opens.

It is folded because opening it would add more rows than a window can spare,
and the line says so: this rendering has no control for the user to press.
"""


def _dump(capsys: pytest.CaptureFixture[str], *settings: str) -> str:
    """Run this example with `--ui dump` and return what it printed."""
    return dump(e08_lists_and_dicts.main, capsys, *settings)


def _refused(capsys: pytest.CaptureFixture[str], *arguments: str) -> str:
    """Run this example, expect it to refuse, and return its error text."""
    return refused(e08_lists_and_dicts.main, capsys, *arguments)


def test_descriptions_real() -> None:
    """Test every selector of this example addresses something it has.

    A selector that addresses nothing would describe nothing and nothing
    would say so, because the editor never refuses one.
    """
    declared = set(vars(ContainerConfig()))
    assert {path[0] for path in DESCRIPTIONS} <= declared


def test_dump_is_a_tree(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a list and a dict are shown as the trees of rows they are."""
    printed = _dump(capsys)
    assert printed.startswith(f'{HEAD}\nproject_name = Example project')
    assert '\n'.join(DELAY_LINES) in printed
    assert '\n'.join(PORT_LINES) in printed
    assert printed.endswith(f'validation: valid\n{DUMP_TAIL}')


def test_long_list_folded(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the long list of this example opens folded, and says so."""
    printed = _dump(capsys)
    assert FOLDED_LABELS in printed
    assert 'label-0' not in printed


def test_open_the_long_list(capsys: pytest.CaptureFixture[str]) -> None:
    """Test `--fold` opens a container that started folded.

    The control is a toggle and does whatever the container is not, which is
    what one option for both of them means.
    """
    printed = _dump(capsys, '--fold', 'many_labels')
    assert f'many_labels: {LABEL_COUNT} elements\n    0 = label-0' in printed


def test_fold_one_container(capsys: pytest.CaptureFixture[str]) -> None:
    """Test `--fold` hides what is inside one container and nothing else."""
    printed = _dump(capsys, '--fold', 'ports')
    assert 'ports: 2 entries (folded)' in printed
    assert 'http = 80' not in printed
    assert '0 = 1' in printed


def test_fold_key_folds_all(capsys: pytest.CaptureFixture[str]) -> None:
    """Test `--toggle-fold` stands in for the key that folds everything."""
    printed = _dump(capsys, '--toggle-fold')
    assert 'retry_delays: 3 elements (folded)' in printed
    assert 'ports: 2 entries (folded)' in printed
    assert 'http = 80' not in printed


def test_fold_key_opens_all(capsys: pytest.CaptureFixture[str]) -> None:
    """Test pressing that key twice opens every container, folded or not."""
    printed = _dump(capsys, '--toggle-fold', '--toggle-fold')
    assert '(folded)' not in printed
    assert 'label-0' in printed


def test_edit_inside_a_list(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a value inside a list is edited by the whole path to it."""
    printed = _dump(capsys, '--set', 'retry_delays.0=2')
    assert 'retry_delays: 3 elements (edited)' in printed
    assert '    0 = 2 (edited)' in printed
    assert 'validation: valid' in printed


def test_edit_inside_a_dict(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a value inside a dict is edited by the whole path to it."""
    printed = _dump(capsys, '--set', 'ports.https=8443')
    assert 'ports: 2 entries (edited)' in printed
    assert '    https = 8443 (edited)' in printed


def test_refused_at_container(capsys: pytest.CaptureFixture[str]) -> None:
    """Test what a validator of a list refused is shown at that member.

    A member validator is given the whole member, so what it refuses is
    about the whole member and never about one value inside it.
    """
    printed = _dump(capsys, '--set', f'retry_delays.1={LONGEST_DELAY + 1}')
    assert 'validation: invalid, see retry_delays' in printed
    assert f'is greater than maximum {LONGEST_DELAY}' in printed


def test_validator_shortens(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the de-duplicating validator leaves one row fewer than it got.

    A validation pass is not read only, and this is the clearest case of it:
    the list comes back shorter than the one that was typed into.
    """
    printed = _dump(capsys, '--set', 'report_formats.0=json')
    assert 'report_formats: 1 element (edited) (changed by validator)' in \
        printed
    assert '    0 = json (edited)' in printed
    assert '    1 = ' not in printed.split('report_formats')[1]


def test_read_file(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the values of a file fill the same tree of rows."""
    printed = _dump(capsys, '-i', data_file('e08_complete.json'))
    assert 'ports: 2 entries\n' in printed
    assert '    http = 8080' in printed
    assert 'many_labels: 2 elements\n    0 = from-a-file-1' in printed
    assert printed.endswith(input_tail('e08_complete.json'))


def test_short_list_opens(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a file whose long member is short opens every container."""
    printed = _dump(capsys, '-i', data_file('e08_short_list.json'))
    assert '(folded)' not in printed
    assert 'many_labels: 1 element\n    0 = only-one' in printed


def test_unknown_path(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a path that addresses nothing at all is refused."""
    error = _refused(capsys, '--ui', 'dump', '--set', 'ports.ftp=21')
    assert 'ports.ftp is not part of' in error


def test_fold_needs_a_list(capsys: pytest.CaptureFixture[str]) -> None:
    """Test folding something that holds nothing is refused."""
    error = _refused(capsys, '--ui', 'dump', '--fold', 'project_name')
    assert 'project_name is not a list or a dict' in error


def test_container_not_edited(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a container cannot be typed into, because it holds no value."""
    error = _refused(capsys, '--ui', 'dump', '--set', 'ports={}')
    assert 'ports is not a value that can be edited' in error


def test_undescribed_member(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a value nothing is said about still says what kind it is."""
    printed = _dump(capsys)
    assert f'project_name = Example project\n{TEXT_LINE}' in printed


def test_tk_ui_opens(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui tk builds the window and returns when it is closed."""
    open_tk_ui(e08_lists_and_dicts.main, monkeypatch)


def test_textual_ui_opens(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui textual starts the application named after the class."""
    assert textual_titles(e08_lists_and_dicts.main,
                          monkeypatch) == ['ContainerConfig']
