#! /usr/bin/env python3
"""Tests for example e06_factory_config.

What this example adds is a configuration class the editor cannot construct,
and a loader that says how it is built. So what is asserted here is both sides
of that: the file opens with the loader, the rule that only the application
could have written is applied, and the very same class without a loader is
refused with the message that names it.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import json
import pytest
from edit_cfg_json import ConfigLoadError, EditModel, LoadPolicy, load_config
from example import e06_factory_config
from example.e06_factory_config import DESCRIPTIONS, KNOWN_TEAMS, TeamConfig, \
    team_loader
from .helpers import DUMP_TAIL, data_file, dump, head, input_tail, \
    open_tk_ui, saved_tail, textual_titles

VALID_LINE = 'validation: valid'
"""Line that `--ui dump` ends with for a buffer the example accepts."""

HEAD = head(TeamConfig(KNOWN_TEAMS))
"""The lines that every dump of this example begins with."""

ABOUT_TEAM = DESCRIPTIONS[('team',)]
"""What this example says about the member its own rule is about."""

FILE_VALUES = {'team': 'beta', 'head_count': 4}
"""What the input file of this example holds."""


def _dump(capsys: pytest.CaptureFixture[str], *settings: str) -> str:
    """Run this example with `--ui dump` and return what it printed."""
    return dump(e06_factory_config.main, capsys, *settings)


def test_defaults_accepted(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the declared values satisfy the rule the application wrote."""
    printed = _dump(capsys)
    assert printed.startswith(HEAD)
    assert f'team = {KNOWN_TEAMS[0]}' in printed
    assert printed.endswith(f'{VALID_LINE}\n{DUMP_TAIL}')


def test_file_is_read(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the loader is what opens the input file of this class."""
    printed = _dump(capsys, '-i', data_file('e06_teams.json'))
    assert 'team = beta' in printed
    assert 'head_count = 4' in printed
    assert printed.endswith(input_tail('e06_teams.json'))


def test_best_match_rewrites(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the rule of the application completes a name that begins one team.

    The list of teams reached the validator through the constructor argument
    that only the application knows, which is what the loader is for, and it is
    still there when a validation pass runs because the pass works on a copy of
    the object the loader made.
    """
    printed = _dump(capsys, '-i', data_file('e06_teams.json'), '--set',
                    'team=alp')
    assert 'team = alpha (edited) (changed by validator)' in printed
    assert VALID_LINE in printed


def test_no_such_team(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a name that begins no team is refused beside its own member."""
    printed = _dump(capsys, '--set', 'team=delta')
    assert f'team = delta (edited)\n    {ABOUT_TEAM}\n' in printed
    assert 'alpha, beta, gamma' in printed
    assert 'validation: invalid, see team' in printed


def test_round_trip(tmp_path: Path,
                    capsys: pytest.CaptureFixture[str]) -> None:
    """Test the whole way from the input file to an output file.

    Only the reading needed the loader, and the writing is what shows that
    everything after the reading works on the object it produced.
    """
    out_file = tmp_path / 'out.json'
    printed = _dump(capsys, '-i', data_file('e06_teams.json'), '-o',
                    str(out_file), '--set', 'head_count=6', '--save')
    assert printed.endswith(saved_tail(out_file, 'TeamConfig'))
    assert json.loads(out_file.read_text(encoding='UTF-8')) == \
        {'team': 'beta', 'head_count': 6}


def test_loader_is_needed() -> None:
    """Test the same file cannot be opened without the loader.

    This is what the example is about, said in the plainest way there is: the
    editor knows nothing about the list of teams, so it cannot construct the
    class that is told it, and the loader is the whole difference.
    """
    with pytest.raises(ConfigLoadError) as refused:
        load_config(config=TeamConfig(KNOWN_TEAMS),
                    in_file=data_file('e06_teams.json'))
    assert 'TeamConfig' in refused.value.message


def test_loader_opens_it() -> None:
    """Test the loader of the example opens that same file, strictly."""
    loaded = load_config(config=TeamConfig(KNOWN_TEAMS), loader=team_loader,
                         policy=LoadPolicy.STRICT,
                         in_file=data_file('e06_teams.json'))
    model = EditModel(loaded.config)
    assert model.config_type_name == 'TeamConfig'
    assert {row.name: row.value for row in model.rows} == FILE_VALUES


def test_tk_ui_opens(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui tk builds the window and returns when it is closed."""
    open_tk_ui(e06_factory_config.main, monkeypatch)


def test_textual_ui_opens(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui textual starts the application named after the class."""
    assert textual_titles(e06_factory_config.main,
                          monkeypatch) == ['TeamConfig']
