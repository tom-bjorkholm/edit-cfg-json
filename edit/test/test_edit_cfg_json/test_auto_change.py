#! /usr/bin/env python3
"""Tests for saying what reading one input file did to the values in it.

Every load is driven through a real file, because the text of the file is one
of the two things that are compared and the comparison is what is being tested
here. The other is what the load would write back, which is read from the
configuration object the load produced.

Both classes that read a file of an older shape are used throughout: one whose
constructor takes the change hook and one whose constructor does not. What the
editor says about the same file has to be the same either way, because what a
load recorded belongs to the object it loaded and not to the constructor of its
class, and the class that declares nothing is the one most applications have.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from pathlib import Path
from typing import Optional
import json
import pytest
from config_as_json import Config, ConfigAutoChangeHook, RocfChange, \
    RocfChangeKind
from edit_cfg_json import EditModel, LoadPolicy, LoadedConfig, load_config, \
    model_as_text, row_marks
from edit_cfg_json.auto_change import FileChanges, _filled
from edit_cfg_json.loading import AUTO_CHANGED, DEFAULT_POLICY, DROPPED_FORM, \
    FILLED_MESSAGE, MORE_REASONS_FORM, NORMALIZED_REASON, REASON_FORMS, \
    SUPPLIED_FORM
from edit_cfg_json.model_text import FILLED_MARK
from .old_format_cfg import DictKeyCfg, OLDER_COUNT_KEY, OLDER_DICT_KEY, \
    OldKeyCfg, OldKeyHookCfg, OwnNoteCfg, SUPPLIED_ANSWER, SUPPLIED_NOTE, \
    SuppliedNoteCfg
from .sample_cfg import CountedCfg, FlatCfg, ListCfg, NoJsonCfg, RewriteCfg, \
    VALIDATOR_RUNS

OLD_FILE = {'title': 'from an old file', 'trace': False}
"""A file in the older shape that `MigrateRules` reads.

Its one value is held under a key that the current shape renamed, it holds a
key that the current shape no longer has, and it does not hold the number
member that the rules supply. So all three of the rules run for this one file.
"""

DROPPED_KEY = 'trace'
"""The one key of that file that no member of the current shape receives."""

RENAMED_MARK = ' (' + REASON_FORMS[RocfChangeKind.KEY_RENAMED] \
    .format(old='title') + ')'
"""What the member that the older key `title` became is marked with."""

SUPPLIED_MARK = ' (' + REASON_FORMS[RocfChangeKind.MISSING_VALUE_ADDED] + ')'
"""What the member that the rules supplied a value for is marked with."""

NORMALIZED_MARK = f' ({NORMALIZED_REASON})'
"""What a member that only the comparison found is marked with.

Parsing and validating are recorded nowhere, so this is what is left to say
about a value that one of them changed.
"""

MIGRATED = {'name': RENAMED_MARK, 'answer': SUPPLIED_MARK}
"""The members of the current shape that reading that old file put there.

Each of them is marked with what the load recorded about it, which is what the
comparison alone could never have said: that `name` is what `title` became, and
that the value of `answer` was in no version of that file at all.
"""

OLD_CLASSES: list[Callable[[], Config]] = [OldKeyCfg, OldKeyHookCfg]
"""Both classes that read that file, for what is true of either of them.

They are used as the callables they are, because what a test does with one is
build an object of it. A class is not written as a type here for that reason
and for one more: the two of them derive from different base classes, so what
they have in common is exactly that either of them answers to being called.
"""

FUTURE_VERSION = ConfigAutoChangeHook.DATA_STRUCTURE_VERSION + 1
"""A version of the records that this editor was certainly not written for."""


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


def _dropped(names: str) -> str:
    """Return the line that names the keys of a file that are left out."""
    return DROPPED_FORM.format(names=names)


@pytest.mark.parametrize('changes, anything', [
    (FileChanges(), False),
    (FileChanges(dropped=frozenset({DROPPED_KEY})), True),
    (FileChanges(changed=frozenset({'name'})), True),
    (FileChanges(reasons={'name': ()}), True),
    (FileChanges(unplaced=(RocfChange(kind=RocfChangeKind.MISSING_VALUE_ADDED,
                                      old_path=None, new_path='a'),)), True),
    (FileChanges(detail='something was changed'), True)])
def test_anything_changed(changes: FileChanges, anything: bool) -> None:
    """Test that a load reports having changed the file if any part did.

    Args:
        changes: What one load did to the file it read.
        anything: Whether that is a load that changed the file.
    """
    assert changes.anything is anything


@pytest.mark.parametrize('builder', OLD_CLASSES)
def test_records_at_members(builder: Callable[[], Config],
                            tmp_path: Path) -> None:
    """Test what the load recorded is said at the member it is about.

    The class that declares the hook and the class that does not are both here
    because the whole point is that they answer alike: `Config` gives every
    object a hook of its own, so the records of a parse are the object's and
    not the constructor's.

    Args:
        builder: Class that reads a file of the older shape.
        tmp_path: The pytest fixture holding the folder of the input file.
    """
    report = _loaded(builder(), tmp_path, OLD_FILE).report
    assert report.reasons == {name: mark.strip(' ()')
                              for name, mark in MIGRATED.items()}


@pytest.mark.parametrize('builder', OLD_CLASSES)
def test_renamed_not_dropped(builder: Callable[[], Config],
                             tmp_path: Path) -> None:
    """Test a key of the file that a member received is not called unused.

    The comparison puts `title` among the keys that saving leaves out, because
    the member holds it under another name and the comparison cannot know that.
    The record can, so the key is reported at its member and not twice.

    Args:
        builder: Class that reads a file of the older shape.
        tmp_path: The pytest fixture holding the folder of the input file.
    """
    message = _loaded(builder(), tmp_path, OLD_FILE).report.message
    assert AUTO_CHANGED in message
    assert _dropped(DROPPED_KEY) in message
    assert 'title' not in message


@pytest.mark.parametrize('builder', OLD_CLASSES)
def test_migrated_rows(builder: Callable[[], Config], tmp_path: Path) -> None:
    """Test the row of every migrated member is marked with what happened.

    The mark is what makes a migration visible in a configuration too tall for
    a window, where the message at the top of it has scrolled away.

    Args:
        builder: Class that reads a file of the older shape.
        tmp_path: The pytest fixture holding the folder of the input file.
    """
    model = _model(builder(), tmp_path, OLD_FILE)
    assert _marks(model, 'name') == RENAMED_MARK
    assert _marks(model, 'answer') == SUPPLIED_MARK
    assert _value(model, 'name') == OLD_FILE['title']
    assert _value(model, 'answer') == SUPPLIED_ANSWER


def test_future_version_text(tmp_path: Path,
                             monkeypatch: pytest.MonkeyPatch) -> None:
    """Test records of a version this was not written for become a report.

    `config_as_json` steps the version whenever it records something else, and
    that is not worth refusing a file over: the comparison still finds every
    member the load changed, and what the records would have added is taken
    from the report that the library writes about them itself.
    """
    monkeypatch.setattr(ConfigAutoChangeHook, 'DATA_STRUCTURE_VERSION',
                        FUTURE_VERSION)
    model = _model(OldKeyHookCfg(), tmp_path, OLD_FILE)
    assert _marks(model, 'name') == NORMALIZED_MARK
    assert _marks(model, 'answer') == NORMALIZED_MARK
    assert 'title -> name' in model.load_message
    assert _dropped(f'title, {DROPPED_KEY}') in model.load_message


def test_unplaced_value_named(tmp_path: Path) -> None:
    """Test a supplied value that no member holds is named in the message.

    Such a record consumed no key of the file and produced nothing the
    configuration writes, so the message is the only place it can be reported.
    It is reported with the value the rules put there, which is the one thing
    the editor would otherwise have no way at all of knowing.

    The member does have a row, because a member the class leaves out of the
    file has one whether the file held it or not. What the row says is that
    the member holds nothing, which is not what the rules supplied: the
    validation plan emptied it again, so the value is still nowhere but in the
    message.
    """
    model = _model(SuppliedNoteCfg(), tmp_path, {'name': 'noted'})
    assert SUPPLIED_FORM.format(
        names=f'note = {SUPPLIED_NOTE!r}') in model.load_message
    assert AUTO_CHANGED in model.load_message
    assert [row.name for row in model.rows] == ['name', 'note']
    assert [row.holds_nothing for row in model.rows] == [False, True]


def test_unplaced_no_value(tmp_path: Path) -> None:
    """Test a supplied value the record has no value for is still named.

    `ConfigAutoChangeHook.rocf_missing_value_provided` is what an application
    calls for old data it supplied itself, and it is the one entry point that
    is not given the value. The path is then all there is to say, which is less
    than the line above says and is never wrong.
    """
    model = _model(OwnNoteCfg(), tmp_path, {'name': 'noted'})
    assert SUPPLIED_FORM.format(names='note') in model.load_message
    assert SUPPLIED_NOTE not in model.load_message
    assert AUTO_CHANGED in model.load_message


def test_filled_needs_keys() -> None:
    """Test a text the class cannot parse claims no filled-in member.

    A load has already read the text by the time this is asked, so a parse
    that fails before the key check is a state that no load reaches. The
    answer is a mark that is not claimed rather than an exception, because
    every member of such a load is reported as one the load changed instead,
    which is true of it as well and says less.
    """
    assert _filled(FlatCfg(), '[]') == frozenset()


def test_several_records(tmp_path: Path) -> None:
    """Test a member the load recorded twice about names the first and counts.

    Two keys inside one dict member were renamed, so both records are about
    that one member. The mark shares its line with the field, so the rest are
    counted rather than listed.
    """
    values = {'tags': ['first'], 'limits': {'lo': 1, 'hi': 9}, 'answer': 3}
    model = _model(DictKeyCfg(), tmp_path, values)
    first = REASON_FORMS[RocfChangeKind.KEY_RENAMED].format(old='limits[lo]')
    assert _marks(model, 'limits') == \
        f' ({MORE_REASONS_FORM.format(first=first, count=1)})'
    assert _value(model, 'limits') == {'low': 1, 'high': 9}


def test_step_is_not_dropped(tmp_path: Path) -> None:
    """Test a record on the way to a member is not called a key left out.

    Renaming the keys inside the dict member runs before the member itself is
    moved, so those two records name paths under the older name of the member.
    Nothing there was dropped: the member says where it came from, and the two
    steps on the way to it are said nowhere at all.
    """
    values = {'tags': ['first'], OLDER_DICT_KEY: {'lo': 1, 'hi': 9},
              'answer': 3}
    model = _model(DictKeyCfg(), tmp_path, values)
    moved = REASON_FORMS[RocfChangeKind.PATH_MOVED].format(old=OLDER_DICT_KEY)
    assert _marks(model, 'limits') == f' ({moved})'
    assert AUTO_CHANGED in model.load_message
    assert OLDER_DICT_KEY not in model.load_message


def test_migrated_value(tmp_path: Path) -> None:
    """Test a member a value migration produced says that it was converted.

    A migration is not a move: the value the member holds is one the rules made
    out of what the file held, so what is said about it names the older key and
    not the older value.
    """
    values = {'tags': ['first'], 'limits': {'low': 1, 'high': 9},
              OLDER_COUNT_KEY: 4}
    model = _model(DictKeyCfg(), tmp_path, values)
    migrated = REASON_FORMS[RocfChangeKind.VALUE_MIGRATED] \
        .format(old=OLDER_COUNT_KEY)
    assert _marks(model, 'answer') == f' ({migrated})'
    assert _value(model, 'answer') == 8
    assert OLDER_COUNT_KEY not in model.load_message


def test_normalized_value(tmp_path: Path) -> None:
    """Test that a value a validator rewrote while loading is reported.

    This is the second of the three ways a load changes a file, and it needs
    no rules for an older format at all: the value is under the key the file
    has it under, and it is not the value the file has. Nothing records it, so
    the comparison is what finds it and the mark says only that much.
    """
    model = _model(RewriteCfg(), tmp_path, {'name': 'lower case'})
    assert _value(model, 'name') == 'Lower case'
    assert _marks(model, 'name') == NORMALIZED_MARK
    assert AUTO_CHANGED in model.load_message
    assert _dropped('name') not in model.load_message
    assert f'name = Lower case{NORMALIZED_MARK}' in model_as_text(model)


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
    """Test a member the defaults filled in carries the more precise mark.

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
    assert not loaded.report.reasons
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
    assert set(report.reasons) == set(MIGRATED)
    assert not report.filled
    assert FILLED_MESSAGE not in report.message


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
    model = _model(builder(), tmp_path, {DROPPED_KEY: False})
    assert _marks(model, 'name') == FILLED_MARK
    assert _marks(model, 'answer') == SUPPLIED_MARK
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


def test_records_survive(tmp_path: Path) -> None:
    """Test the records of the load are the load's own and not a later parse.

    Asking what the declared defaults filled in parses the same text again, and
    a parse clears the hook it records into before it starts. It is a copy of
    the configuration object that parses, so it is a copy of the hook that is
    cleared, and what the load recorded is still there to be read afterwards.
    """
    loaded = _loaded(OldKeyHookCfg(), tmp_path, {DROPPED_KEY: False},
                     LoadPolicy.DEFAULTS)
    hook = loaded.config.auto_change_hook()
    kinds = [change.kind for change in hook.changes]
    assert RocfChangeKind.MISSING_VALUE_ADDED in kinds
    assert loaded.report.reasons == {'answer': SUPPLIED_MARK.strip(' ()')}


def test_hook_is_the_objects(tmp_path: Path) -> None:
    """Test the records are read from the object and need no hook passed in.

    The editor hands no hook to anything. `Config` gives every configuration
    object one of its own, `Config.auto_change_hook` is where it is, and that
    is what makes a class that declares nothing report as fully as one that
    declares the parameter.
    """
    loaded = _loaded(OldKeyCfg(), tmp_path, OLD_FILE)
    hook: Optional[ConfigAutoChangeHook] = loaded.config.auto_change_hook()
    assert isinstance(hook, ConfigAutoChangeHook)
    assert hook.has_changes()
