#! /usr/bin/env python3
"""Tests for example e11_add_remove.

What this example adds is changing how many things a member holds. So what is
asserted here is where a new element comes from, the four members that cannot
be given one and the four different reasons why, and that what was added is
validated and written exactly like anything that was there from the start.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import json
import pytest
from example import e11_add_remove
from example.e11_add_remove import DESCRIPTIONS, PipelineConfig, \
    REPEAT_REFUSAL, StageConfig
from .helpers import DUMP_TAIL, data_file, dump, head, open_tk_ui, refused, \
    saved_tail, textual_titles

HEAD = head(PipelineConfig())
"""The lines that every dump of this example begins with."""

STAGE_CLASS = StageConfig.__name__
"""What the row of one stage says instead of a value."""

DATA_NAME = 'e11_pipeline.json'
"""Input file of this example, whose spare hosts are not empty."""


FIXED_KEYS = ('    This version adds an entry only to a dict whose class '
              'declares that every value in it is one configuration object.')
"""What it says below an ordinary dict member."""

UNCHECKED = ("    The keys of this dict are the application's own to decide, "
             'with validators of its own. This version does not add or '
             'remove them.')
"""What it says below a dict listed in `_unchecked_dicts`."""

BY_KEY = ('    One named key of this dict holds a configuration object and '
          'the others do not, so its keys follow a policy of their own. This '
          'version does not add or remove them.')
"""What it says below a dict declared `DICT_VALUE_BY_KEY`."""

NEW_STAGE_LINES = ['        name = build', '        command = make',
                   '        minutes = 10']
"""What a stage the editor has just added is shown as.

A new element of a member declared `LIST_ELEMENT` is one object of the
declared class holding the values that class declares, which is what makes
these the same three values the first stage of this pipeline has.
"""


def _dump(capsys: pytest.CaptureFixture[str], *settings: str) -> str:
    """Run this example with `--ui dump` and return what it printed."""
    return dump(e11_add_remove.main, capsys, '--toggle-explain', *settings)


def _explained(capsys: pytest.CaptureFixture[str], *settings: str) -> str:
    """Run it with the explanations left on, which is how it starts."""
    return dump(e11_add_remove.main, capsys, *settings)


def _refused(capsys: pytest.CaptureFixture[str], *arguments: str) -> str:
    """Run this example, expect it to refuse, and return its error text."""
    return refused(e11_add_remove.main, capsys, *arguments)


def test_descriptions_real() -> None:
    """Test every selector of this example addresses something it has."""
    declared = set(vars(PipelineConfig()))
    assert {path[0] for path in DESCRIPTIONS} <= declared


def test_added_stage(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a list of objects is given one of the declared class."""
    printed = _dump(capsys, '--add', 'stages')
    assert 'stages: 3 elements (edited)' in printed
    assert f'    2: {STAGE_CLASS}' in printed
    assert '\n'.join(NEW_STAGE_LINES) in printed


def test_empty_list_grows(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a declared list that holds nothing can still be given one.

    What an element of it is comes from the declaration and not from what the
    member happens to hold, which is the case a container of plain values
    cannot answer.
    """
    printed = _dump(capsys, '--add', 'extra_stages')
    assert 'extra_stages: 1 element (edited)' in printed
    assert '    0: StageConfig' in printed


def test_declared_copied(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a list of plain values is grown with a copy of the first."""
    printed = _dump(capsys, '--add', 'retry_delays')
    assert 'retry_delays: 4 elements (edited)' in printed
    assert '    3 = 1' in printed


def test_typed_element_added(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the list with nothing to copy grows by what its type says.

    Its class declares an empty list and no nesting, so no value anywhere
    says what one host looks like. `list[str]` does, and the empty text is
    the one value of that kind which says no more than which kind it is.
    """
    printed = _dump(capsys, '--add', 'extra_hosts')
    assert 'extra_hosts: 1 element (edited)' in printed
    assert '    0 = \n' in printed


def test_file_gives_a_pattern(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a file that holds an element makes that member extendable.

    The declared values are asked first and what the member holds after them,
    so a member the class declares nothing for can be extended as soon as a
    file has put something in it.
    """
    printed = _dump(capsys, '-i', data_file(DATA_NAME), '--add', 'extra_hosts')
    assert 'extra_hosts: 3 elements (edited)' in printed
    assert '    2 = spare-1.example.org' in printed


def test_added_entry(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a dict of objects is given an entry under the key that was named.

    It appears where the sorted order of the keys puts it, because that is
    the order a file holds a dict in and therefore the order the rows are in.
    """
    printed = _dump(capsys, '--add', 'runners=nightly')
    assert 'runners: 3 entries (edited)' in printed
    assert printed.index('nightly: RunnerConfig') < printed.index('slow:')


def test_removed_entry(capsys: pytest.CaptureFixture[str]) -> None:
    """Test one entry of a dict of objects can be taken out of it."""
    printed = _dump(capsys, '--remove', 'runners.fast')
    assert 'runners: 1 entry (edited)' in printed
    assert 'fast: RunnerConfig' not in printed


@pytest.mark.parametrize('said', [FIXED_KEYS, UNCHECKED, BY_KEY])
def test_dicts_say_why(capsys: pytest.CaptureFixture[str], said: str) -> None:
    """Test each dict that cannot grow says why, in its own words.

    The three of them cannot for three different reasons, and each reason is
    the class's own decision: the keys it declares, the key policy it defines
    with validators of its own, and the one named key that holds an object.
    """
    assert said in _explained(capsys)


@pytest.mark.parametrize('name', ['limits', 'labels', 'hooks'])
def test_dicts_refuse(capsys: pytest.CaptureFixture[str], name: str) -> None:
    """Test none of those three dicts can be given an entry after all."""
    refusal = _refused(capsys, '--ui', 'dump', '--add', f'{name}=new')
    assert 'Nothing can be added' in refusal


def test_optional_added(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the optional member is given the object it is declared for."""
    printed = _dump(capsys, '--add', 'audit', '--set', 'audit.name=cleanup')
    assert f'audit: {STAGE_CLASS} (edited)' in printed
    assert '    name = cleanup (edited)' in printed


def test_moved_stage(capsys: pytest.CaptureFixture[str]) -> None:
    """Test one element of a list changes places with the one after it."""
    printed = _dump(capsys, '--move', 'stages.0=down')
    assert '    0: StageConfig' in printed
    assert printed.index('name = test') < printed.index('name = build')


def test_application_rules(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a copied stage is refused by the rule of the class holding them.

    Adding an element is not a way round the application's own rules: the
    editor copies what the class declares, and what the class makes of the
    result is what a validation pass says.
    """
    printed = _dump(capsys, '--add', 'stages')
    assert REPEAT_REFUSAL.format(name='build') in printed
    named = _dump(capsys, '--add', 'stages', '--set', 'stages.2.name=deploy')
    assert 'validation: valid' in named


def test_added_is_saved(capsys: pytest.CaptureFixture[str],
                        tmp_path: Path) -> None:
    """Test what was added reaches the file like anything else."""
    out_file = tmp_path / 'pipeline.json'
    named = ['--add', 'stages', '--set', 'stages.2.name=deploy']
    printed = _dump(capsys, *named, '-o', str(out_file), '--save')
    assert printed.endswith(saved_tail(out_file, 'PipelineConfig'))
    written = json.loads(out_file.read_text(encoding='UTF-8'))
    assert [stage['name'] for stage in written['stages']] == ['build', 'test',
                                                              'deploy']


def test_starts_as_declared(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the example says what it holds before anything is changed."""
    printed = _explained(capsys)
    assert printed.startswith(f'{HEAD}\npipeline_name = nightly')
    assert printed.endswith(f'validation: valid\n{DUMP_TAIL}')


def test_tk_shows_it(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the Tk backend opens on this example without failing."""
    open_tk_ui(e11_add_remove.main, monkeypatch, '--add', 'stages')


def test_textual_shows_it(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the Textual backend opens on this example and can be left."""
    titles = textual_titles(e11_add_remove.main, monkeypatch, '--add',
                            'stages')
    assert titles == ['PipelineConfig *']
