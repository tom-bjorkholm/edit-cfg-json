#! /usr/bin/env python3
"""Tests for example e10_config_containers.

What this example adds is the repeated configuration object: a list whose
elements are objects and a dict whose values are objects. So what is asserted
here is what one selector with the `'['` step reaches, what each of those
objects says about itself, and that a rule of the class holding them refuses
the export while every object in it is still a configuration on its own.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import json
import pytest
from example import e10_config_containers
from example.e10_config_containers import CourseReportsConfig, DESCRIPTIONS, \
    FEWEST_ROWS, REPEAT_REFUSAL, ReportOutputConfig
from .helpers import DUMP_TAIL, TEXT_LINE, WHOLE_LINE, data_file, dump, head, \
    input_tail, open_tk_ui, refused, textual_titles

HEAD = head(CourseReportsConfig())
"""The lines that every dump of this example begins with."""

REPORT_CLASS = ReportOutputConfig.__name__
"""What the row of one report says instead of a value."""

OWN_VALID = ' [valid on its own]'
"""What an object that is a configuration on its own says."""

OWN_REFUSED = ' [refused on its own]'
"""What an object that its own class refuses says instead."""

INSIDE_VALID = ' [valid inside]'
"""What a container of objects says when every one of them passes.

A list or a dict is no configuration and says nothing about itself, so what it
says is about the objects it holds. That is what a folded container leaves on
the screen, where every object it is about is hidden.
"""

INSIDE_REFUSED = ' [refused inside]'
"""What such a container says when one of the objects it holds is refused."""

ABOUT_ONE_REPORT = DESCRIPTIONS[('reports', '[')]
"""What this example says about every element of the list, once."""

ABOUT_ONE_FILE = DESCRIPTIONS[('reports', '[', 'file_name')]
"""What it says about one member of every element of the list, once."""

ABOUT_ANY_ROWS = DESCRIPTIONS[('reports_by_id', '[', 'max_rows')]
"""What it says about one member of every value of the dict, once."""

ABOUT_AUDIT_ROWS = DESCRIPTIONS[('reports_by_id', 'audit', 'max_rows')]
"""What it says about that one member of that one value of the dict."""

LIST_REPORTS = 3
"""How many objects the list of this example holds."""

DICT_REPORTS = 2
"""How many objects its dict holds, which is few enough to open open."""

FOLDED_REPORTS = f'reports: {LIST_REPORTS} elements (folded)'
"""How the list of this example is shown when the editor opens.

Three objects of three members each is more rows than a window can spare, so
the list opens folded. It is the same rule as for a long list of values, met
where a real configuration meets it: at three objects rather than at a dozen
numbers.
"""

OPEN_BY_ID = f'reports_by_id: {DICT_REPORTS} entries'
"""How the dict of this example is shown, which is open.

Two objects of three members each is eight rows, which is what a window can
spare, so the two containers of one configuration open differently.
"""

AUDIT_ROWS = 'max_rows = 5000'
"""The value of the one member that is described by a selector of its own."""

COLLIDING_FILE = 'participants.csv'
"""File name of a report of the list, given to a report of the dict."""


def _dump(capsys: pytest.CaptureFixture[str], *settings: str) -> str:
    """Run this example with `--ui dump` and return what it printed."""
    return dump(e10_config_containers.main, capsys, *settings)


def _refused(capsys: pytest.CaptureFixture[str], *arguments: str) -> str:
    """Run this example, expect it to refuse, and return its error text."""
    return refused(e10_config_containers.main, capsys, *arguments)


def _open_list(capsys: pytest.CaptureFixture[str], *settings: str) -> str:
    """Run it with the list opened, which is what it does not start as."""
    return _dump(capsys, '--fold', 'reports', *settings)


def test_descriptions_real() -> None:
    """Test every selector of this example addresses something it has."""
    declared = set(vars(CourseReportsConfig()))
    assert {path[0] for path in DESCRIPTIONS} <= declared


def test_two_containers(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the two containers say how much they hold and fold differently."""
    printed = _dump(capsys)
    assert printed.startswith(f'{HEAD}\ncourse_name = python-intro')
    assert f'{FOLDED_REPORTS}{INSIDE_VALID}\n' in printed
    assert f'{OPEN_BY_ID}{INSIDE_VALID}\n' in printed
    assert printed.endswith(f'validation: valid\n{DUMP_TAIL}')


def test_elements_are_nodes(capsys: pytest.CaptureFixture[str]) -> None:
    """Test opening the list shows each element as the object it is.

    The row of an element says its class and not how many entries the dict it
    writes has, and it carries the badge that says what that one object is on
    its own, exactly as a nested object held by a member does.
    """
    printed = _open_list(capsys)
    for index in range(LIST_REPORTS):
        assert f'    {index}: {REPORT_CLASS}{OWN_VALID}' in printed
    assert '        title = Registered participants' in printed


def test_values_are_nodes(capsys: pytest.CaptureFixture[str]) -> None:
    """Test every value of the dict is a node, keyed and in sorted order."""
    printed = _dump(capsys)
    audit = f'    audit: {REPORT_CLASS}{OWN_VALID}'
    summary = f'    summary: {REPORT_CLASS}{OWN_VALID}'
    assert audit in printed
    assert summary in printed
    assert printed.index(audit) < printed.index(summary)


def test_one_text_for_every(capsys: pytest.CaptureFixture[str]) -> None:
    """Test one `'['` selector describes the same member of every element.

    That is what keeps an application from writing one description per index,
    which would become untrue the moment a report was added.
    """
    printed = _open_list(capsys)
    assert printed.count(f'            {ABOUT_ONE_FILE}') == LIST_REPORTS
    assert printed.count(f'        {ABOUT_ONE_REPORT}') == LIST_REPORTS


def test_every_dict_value(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the same selector reaches every value of a dict of objects."""
    printed = _dump(capsys)
    assert f'        max_rows = 50\n            {ABOUT_ANY_ROWS}' in printed


def test_named_beats_every(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a selector that names every step wins over one that says `'['`.

    Both address that member, and the more specific of two selectors is the
    one that describes it, so one report of the dict is explained on its own
    while every other keeps the general text.
    """
    printed = _dump(capsys)
    assert f'        {AUDIT_ROWS}\n            {ABOUT_AUDIT_ROWS}' in printed
    assert f'{AUDIT_ROWS}\n            {ABOUT_ANY_ROWS}' not in printed


def test_undescribed_member(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a member of an object that nothing describes says its kind."""
    printed = _dump(capsys)
    assert f'        title = Course summary\n        {TEXT_LINE}' in printed


def test_edit_in_an_element(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a member of one list element is edited by the path to it."""
    printed = _open_list(capsys, '--set', 'reports.0.file_name=other.csv')
    assert f'reports: {LIST_REPORTS} elements (edited)' in printed
    assert f'    0: {REPORT_CLASS} (edited){OWN_VALID}' in printed
    assert '        file_name = other.csv (edited)' in printed
    assert 'validation: valid' in printed


def test_edit_in_a_value(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a member of one dict value is edited by the path to it."""
    printed = _dump(capsys, '--set', 'reports_by_id.summary.max_rows=75')
    assert f'    summary: {REPORT_CLASS} (edited){OWN_VALID}' in printed
    assert (f'        max_rows = 75 (edited)\n            {ABOUT_ANY_ROWS}\n'
            f'        {WHOLE_LINE}') in printed


def test_own_rule_per_object(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the rule of the element class runs for each object of it.

    It belongs to that class, so the class holding the containers says
    nothing about it, and the one object it refused is the one that says so.
    """
    printed = _dump(capsys, '--set',
                    f'reports_by_id.audit.max_rows={FEWEST_ROWS - 1}')
    assert f'    audit: {REPORT_CLASS} (edited){OWN_REFUSED}' in printed
    assert f'    summary: {REPORT_CLASS}{OWN_VALID}' in printed
    assert 'validation: invalid, see reports_by_id.audit.max_rows' in printed
    assert f'is less than minimum {FEWEST_ROWS}' in printed


def test_container_inside(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the container of a refused object says that much on its own row.

    That row is what a folded container leaves on the screen, and every object
    it is about is then hidden, so without it folding a member would hide the
    one thing the user has to act on and leave nothing in its place. The other
    container holds nothing that was refused and says so.
    """
    printed = _dump(capsys, '--set',
                    f'reports_by_id.audit.max_rows={FEWEST_ROWS - 1}')
    assert f'{OPEN_BY_ID} (edited){INSIDE_REFUSED}' in printed
    assert f'{FOLDED_REPORTS}{INSIDE_VALID}' in printed


def test_rule_over_all(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a rule about every report refuses while each one is valid.

    The two reports it is about are in different containers, which is what
    makes it a rule no object could check for itself, and both of them are
    perfectly good objects while the export cannot be written at all.
    """
    printed = _open_list(capsys, '--set',
                         f'reports_by_id.audit.file_name={COLLIDING_FILE}')
    assert printed.count(OWN_VALID) == LIST_REPORTS + DICT_REPORTS
    assert OWN_REFUSED not in printed
    assert 'validation: invalid' in printed
    assert REPEAT_REFUSAL.format(name=COLLIDING_FILE) in printed


def test_read_file(capsys: pytest.CaptureFixture[str]) -> None:
    """Test how many objects a container holds follows the file.

    The file holds one report fewer than the class declares and one named
    report more, so the container that opens folded is the other one: which
    member it is says nothing, and how many rows opening it would add says
    everything.
    """
    printed = _dump(capsys, '-i', data_file('e10_reports.json'))
    assert f'reports: {DICT_REPORTS} elements{INSIDE_VALID}\n' in printed
    assert f'reports_by_id: {LIST_REPORTS} entries (folded)' in printed
    assert '        title = What each participant is billed' not in printed
    assert printed.endswith(input_tail('e10_reports.json'))


def test_save_inside_element(tmp_path: Path,
                             capsys: pytest.CaptureFixture[str]) -> None:
    """Test a value edited inside one element reaches the file."""
    out_file = tmp_path / 'out.json'
    _dump(capsys, '-o', str(out_file), '--save', '--set',
          'reports.2.max_rows=250')
    written = json.loads(out_file.read_text(encoding='UTF-8'))
    assert written['reports'][2]['max_rows'] == 250
    assert written['reports'][0]['max_rows'] == 1000
    assert sorted(written['reports_by_id']) == ['audit', 'summary']


def test_element_not_edited(capsys: pytest.CaptureFixture[str]) -> None:
    """Test an element of the list is edited through its rows, not as one."""
    error = _refused(capsys, '--ui', 'dump', '--set', 'reports.0={}')
    assert 'reports.0 is not a value that can be edited' in error


def test_tk_ui_opens(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui tk builds the window and returns when it is closed."""
    open_tk_ui(e10_config_containers.main, monkeypatch)


def test_textual_ui_opens(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui textual starts the application named after the class."""
    assert textual_titles(e10_config_containers.main,
                          monkeypatch) == ['CourseReportsConfig']
