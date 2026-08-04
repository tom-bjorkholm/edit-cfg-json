#! /usr/bin/env python3
"""Tests for saying what reading one input file did to the values in it.

Every load is driven through a real file, because the text of the file is one
of the two things that are compared and the comparison is what is being tested
here. The other is what the load would write back, which is read from the
configuration object the load produced.

Both classes that read a file of an older shape are used throughout: one whose
constructor takes the change hook and one whose constructor does not. What the
editor says about the same file has to be true either way, and the class that
cannot report anything is the one most applications have.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from copy import deepcopy
from pathlib import Path
from typing import Optional
import json
import pytest
from config_as_json import Config
from edit_cfg_json import EditModel, LoadPolicy, LoadedConfig, load_config, \
    model_as_text, row_marks
from edit_cfg_json.auto_change import ChangeReport, FileChanges
from edit_cfg_json.loading import AUTO_CHANGED, DEFAULT_POLICY, DROPPED_FORM, \
    FILLED_MESSAGE, OLD_FORMAT_FORM, SUPPLIED_FORM
from edit_cfg_json.model_text import FILLED_MARK, LOAD_MARK
from .sample_cfg import CountedCfg, FlatCfg, ListCfg, NoJsonCfg, OldKeyCfg, \
    OldKeyHookCfg, RewriteCfg, SUPPLIED_ANSWER, VALIDATOR_RUNS

OLD_FILE = {'title': 'from an old file', 'trace': False}
"""A file in the older shape that `MigrateRules` reads.

Its one value is held under a key that the current shape renamed, it holds a
key that the current shape no longer has, and it does not hold the number
member that the rules supply. So all three of the rules run for this one file.
"""

OLD_KEYS = 'title, trace'
"""The older keys of that file, in the order a message names them."""

MIGRATED = {'name', 'answer'}
"""The members of the current shape that reading that old file put there."""

OLD_CLASSES: list[Callable[[], Config]] = [OldKeyCfg, OldKeyHookCfg]
"""Both classes that read that file, for what is true of either of them.

They are used as the callables they are, because what a test does with one is
build an object of it. A class is not written as a type here for that reason
and for one more: the two of them derive from different base classes, so what
they have in common is exactly that either of them answers to being called.
"""


def _written(tmp_path: Path, data: object) -> Path:
    """Write one JSON file in the temporary folder and return its path."""
    path = tmp_path / 'config.json'
    path.write_text(json.dumps(data), encoding='UTF-8')
    return path


def _loaded(config: Config, tmp_path: Path, data: object,
            policy: LoadPolicy = DEFAULT_POLICY) -> LoadedConfig:
    """Load one configuration from a file holding the given values."""
    return load_config(config=config, policy=policy,
                       in_file=_written(tmp_path=tmp_path, data=data))


def _model(config: Config, tmp_path: Path, data: object,
           policy: LoadPolicy = DEFAULT_POLICY) -> EditModel:
    """Return the model of a session on a file holding the given values."""
    loaded = _loaded(config=config, tmp_path=tmp_path, data=data,
                     policy=policy)
    return EditModel(loaded.config, loaded.report)


def _marks(model: EditModel, name: str) -> str:
    """Return the marks that one member of one model carries."""
    return row_marks(next(row for row in model.rows if row.name == name))


def _value(model: EditModel, name: str) -> object:
    """Return the value that one member of one model holds."""
    return next(row.value for row in model.rows if row.name == name)


def test_hook_is_not_copied() -> None:
    """Test that copying the hook of a load gives that very hook back.

    `Config.__init__` deep copies the hook it is given and records into the
    copy, so this is what makes a report reach the editor at all. Without it
    every test below that reads a report would see an empty one.
    """
    hook = ChangeReport()
    assert deepcopy(hook) is hook


@pytest.mark.parametrize('changes, anything', [
    (FileChanges(), False),
    (FileChanges(dropped=frozenset({'trace'})), True),
    (FileChanges(changed=frozenset({'name'})), True),
    (FileChanges(old_keys=('title',)), True),
    (FileChanges(supplied=('answer',)), True)])
def test_anything_changed(changes: FileChanges, anything: bool) -> None:
    """Test that a load reports having changed the file if any part did.

    Args:
        changes: What one load did to the file it read.
        anything: Whether that is a load that changed the file.
    """
    assert changes.anything is anything


def test_old_keys_are_named(tmp_path: Path) -> None:
    """Test that a class that takes the hook names the older keys.

    Naming them is the whole of what the hook adds. A key that was renamed is
    gone from the file, so nothing but the class itself can say that `name`
    is what `title` became.
    """
    report = _loaded(OldKeyHookCfg(), tmp_path, OLD_FILE).report
    assert AUTO_CHANGED in report.message
    assert OLD_FORMAT_FORM.format(names=OLD_KEYS) in report.message
    assert SUPPLIED_FORM.format(names='answer') in report.message
    assert DROPPED_FORM.format(names=OLD_KEYS) not in report.message


def test_dropped_keys_named(tmp_path: Path) -> None:
    """Test that a class that takes no hook still says what it can see.

    The comparison sees that the file holds two keys this configuration does
    not write back, and says so. It cannot say that one of them was renamed
    and the other removed, and it does not pretend to.
    """
    report = _loaded(OldKeyCfg(), tmp_path, OLD_FILE).report
    assert AUTO_CHANGED in report.message
    assert DROPPED_FORM.format(names=OLD_KEYS) in report.message
    assert OLD_FORMAT_FORM.format(names=OLD_KEYS) not in report.message
    assert 'answer' not in report.message


@pytest.mark.parametrize('builder', OLD_CLASSES)
def test_migrated_members(builder: Callable[[], Config],
                          tmp_path: Path) -> None:
    """Test that both classes report the same members as changed.

    What the load did to the values is the same for the two of them, because
    the rules are the same. Only what can be said about why differs.

    Args:
        builder: Class that reads a file of the older shape.
        tmp_path: The pytest fixture holding the folder of the input file.
    """
    loaded = _loaded(builder(), tmp_path, OLD_FILE)
    assert set(loaded.report.changed) == MIGRATED
    assert not loaded.report.filled


@pytest.mark.parametrize('builder', OLD_CLASSES)
def test_migrated_rows(builder: Callable[[], Config], tmp_path: Path) -> None:
    """Test that the row of every migrated member is marked as one.

    The mark is what makes a migration visible in a configuration too tall for
    a window, where the message at the top of it has scrolled away.

    Args:
        builder: Class that reads a file of the older shape.
        tmp_path: The pytest fixture holding the folder of the input file.
    """
    model = _model(builder(), tmp_path, OLD_FILE)
    assert _marks(model, 'name') == LOAD_MARK
    assert _marks(model, 'answer') == LOAD_MARK
    assert _value(model, 'name') == OLD_FILE['title']
    assert _value(model, 'answer') == SUPPLIED_ANSWER


def test_normalized_value(tmp_path: Path) -> None:
    """Test that a value a validator rewrote while loading is reported.

    This is the second of the three ways a load changes a file, and it needs
    no rules for an older format at all: the value is under the key the file
    has it under, and it is not the value the file has.
    """
    model = _model(RewriteCfg(), tmp_path, {'name': 'lower case'})
    assert _value(model, 'name') == 'Lower case'
    assert _marks(model, 'name') == LOAD_MARK
    assert AUTO_CHANGED in model.load_message
    assert DROPPED_FORM.format(names='name') not in model.load_message
    assert f'name = Lower case{LOAD_MARK}' in model_as_text(model)


def test_unchanged_is_silent(tmp_path: Path) -> None:
    """Test that a load which changed nothing says nothing at all.

    This is the ordinary case, and it is the one that decides whether the
    message is worth anything: an editor that remarked on every file would be
    teaching the user to ignore the remark.
    """
    model = _model(FlatCfg(), tmp_path, {'name': 'a name', 'answer': 7})
    assert model.load_message == ''
    assert _marks(model, 'name') == ''
    assert _marks(model, 'answer') == ''


def test_filled_is_no_change(tmp_path: Path) -> None:
    """Test that a member the defaults filled in carries the older mark only.

    Both marks would be true, and the one that says the defaults filled this
    in says more, so it is the one that is shown. The message says the same
    thing once for the same reason.
    """
    model = _model(FlatCfg(), tmp_path, {'name': 'a name'},
                   LoadPolicy.DEFAULTS)
    assert _marks(model, 'answer') == FILLED_MARK
    assert model.load_message == FILLED_MESSAGE


def test_dict_order_kept(tmp_path: Path) -> None:
    """Test that a file whose dict keys are in another order is unchanged.

    `config_as_json` writes the keys of a dictionary sorted and a file is
    written by hand, so the two orders differ for no reason that concerns the
    user. The comparison sorts them, which is what keeps this file from being
    reported as one that reading changed.
    """
    values = {'tags': ['first', 'second'], 'limits': {'low': 1, 'high': 9},
              'answer': 3}
    model = _model(ListCfg(), tmp_path, values)
    assert model.load_message == ''
    assert _marks(model, 'limits') == ''


def test_unwritable_class(tmp_path: Path) -> None:
    """Test that a class that cannot write itself is refused as it was.

    The comparison reads what the load would write, so a class that cannot be
    written has nothing to compare. That is not a new way for a load to fail:
    such a class cannot be shown at all, and it is the model that says so,
    exactly as it did before there was anything to compare.
    """
    loaded = _loaded(NoJsonCfg(), tmp_path, {}, LoadPolicy.DEFAULTS)
    assert not loaded.report.changed
    with pytest.raises(ValueError):
        EditModel(loaded.config, loaded.report)


@pytest.mark.parametrize('policy', list(LoadPolicy))
def test_every_policy_reports(policy: LoadPolicy, tmp_path: Path) -> None:
    """Test that an older file is reported the same under every policy.

    The rules for an older format run while the file is parsed and before its
    keys are checked, so a file in the older shape is complete by the time the
    policy has anything to say about it. Nothing was filled in from the
    declared defaults under any of the three, and the permissive policy is the
    one that says so only because the parse is what answers it: the keys of the
    file would have said that two members were filled in, and neither was.

    Args:
        policy: Policy for declared keys the file does not hold.
        tmp_path: The pytest fixture holding the folder of the input file.
    """
    report = _loaded(OldKeyHookCfg(), tmp_path, OLD_FILE, policy).report
    assert set(report.changed) == MIGRATED
    assert not report.filled
    assert FILLED_MESSAGE not in report.message
    assert OLD_FORMAT_FORM.format(names=OLD_KEYS) in report.message


@pytest.mark.parametrize('builder', OLD_CLASSES)
def test_older_and_incomplete(builder: Callable[[], Config],
                              tmp_path: Path) -> None:
    """Test the file that needs both the rules and the declared defaults.

    This is the one file about which the two marks could be confused, and each
    of them is exact: the number member was supplied by the rules for an older
    format, and the text member was filled in from the declared defaults,
    because the older file has no key that becomes it.

    Args:
        builder: Class that reads a file of the older shape.
        tmp_path: The pytest fixture holding the folder of the input file.
    """
    model = _model(builder(), tmp_path, {'trace': False})
    assert _marks(model, 'name') == FILLED_MARK
    assert _marks(model, 'answer') == LOAD_MARK
    assert _value(model, 'answer') == SUPPLIED_ANSWER
    assert FILLED_MESSAGE in model.load_message
    assert AUTO_CHANGED in model.load_message


def test_filling_is_cheap(tmp_path: Path) -> None:
    """Test that asking what the defaults filled in validates nothing.

    Which members the declared defaults supplied is answered by a second parse
    of the same text, and that parse is stopped at the key check that answers
    it. Everything after that check is what the load has already done, so a
    file that needed the defaults costs the application's own validators
    exactly what a complete file costs them and nothing more.
    """
    VALIDATOR_RUNS.clear()
    _loaded(CountedCfg(), tmp_path, {'name': 'a name', 'answer': 1})
    complete = len(VALIDATOR_RUNS)
    VALIDATOR_RUNS.clear()
    _loaded(CountedCfg(), tmp_path, {'name': 'a name'}, LoadPolicy.DEFAULTS)
    assert len(VALIDATOR_RUNS) == complete


def test_hook_reaches_class(tmp_path: Path) -> None:
    """Test that the hook the editor passes is the one the class was given.

    The class records what it was constructed with, so this says that the
    editor really offers its own hook to a class that declares the parameter,
    and that what it offers is the hook it then reads.
    """
    loaded = _loaded(OldKeyHookCfg(), tmp_path, OLD_FILE)
    given: Optional[object] = None
    assert isinstance(loaded.config, OldKeyHookCfg)
    given = loaded.config.hook_given()
    assert isinstance(given, ChangeReport)
    assert 'title' in given.old_keys
