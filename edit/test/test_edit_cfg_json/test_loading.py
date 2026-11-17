#! /usr/bin/env python3
"""Tests for reading the configuration to edit from one input file.

Every load is driven through a file in a temporary folder rather than through
text, because reading the file is part of what is being tested: a file that
is missing, or that is not text at all, has to be refused with a message and
not with the `sys.exit` that `config_as_json` does on its own.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from io import StringIO
from pathlib import Path
from typing import Optional
import json
import pytest
from config_as_json import Config, ConfigAutoChangeHook
from edit_cfg_json import ConfigLoadError, ConfigLoader, EditModel, \
    LoadPolicy, LoadReport, Settings, load_config
from edit_cfg_json.loader import LOADER_EXITED
from edit_cfg_json.loading import BAD_VALUES, DEFAULT_POLICY, FILLED_MESSAGE, \
    INCOMPLETE, NOT_CONFIG, NOT_FILLABLE, NOT_TEXT, NO_DEFAULTS, NO_FILE, \
    UNKNOWN_KEY, WRONG_SHAPE
from .container_cfg import DeepConfigCfg, NestedCfg
from .defaults_cfg import UNKNOWN_NAME, BadDefaultCfg, LegacyFactoryCfg, \
    LegacyNestedCfg, LookupCfg
from .sample_cfg import NOT_A_NUMBER, PICKED_NAME, EnumCfg, ExtraArgCfg, \
    FlatCfg, HookCfg, OmitCfg, PickedCfg, RangeCfg, WholeOnlyCfg, \
    exiting_loader, extra_arg_loader, no_member_loader, picking_loader

COMPLETE = {'name': 'From a file', 'answer': 7}
"""Values of a file that holds every member of `FlatCfg`."""

INCOMPLETE_DATA = {'name': 'Only a name'}
"""Values of a file that leaves out the number member of `FlatCfg`."""

UNKNOWN_DATA = {'name': 'From a file', 'answer': 7, 'colour': 'red'}
"""Values of a file with a key that `FlatCfg` does not declare."""

BAD_VALUE_DATA = {'answer': 500}
"""Values of a file that `RangeCfg` reads and then refuses.

`FlatCfg` cannot show this, because it declares no validator at all. A value
outside a range is the plainest case of a file that is read and then refused.
"""

EVERY_POLICY = list(LoadPolicy)
"""Every load policy, for the cases that all of them treat alike."""

FILLING_POLICIES = [LoadPolicy.DEFAULTS, LoadPolicy.STRICT_THEN_DEFAULTS]
"""The load policies that open a file whose missing values can be filled."""

FULL_INNER = {'width': 9, 'height': 8}
"""Values of a nested `InnerCfg` that holds every member of it."""

NESTED_GAP = {'inner': {'width': 9}, 'limits': {'low': 1}}
"""Values of a file that leaves one value out of the nested object."""

FILLED_CASES = [
    (NestedCfg, NESTED_GAP, {('inner', 'height')}),
    (NestedCfg, {'inner': FULL_INNER, 'limits': {}}, {('limits', 'low')}),
    (NestedCfg, {'limits': {'low': 1}}, {('inner',)}),
    (DeepConfigCfg, {'outputs': [{'parts': {'one': {'width': 1}}}]},
     {('outputs', '0', 'label'), ('outputs', '0', 'parts', 'one', 'height')})]
"""Class, file values and the paths the declared defaults fill in for them.

The paths are those of the rows of the editor, which index a list with the
text of the index. Each names the outermost value the file lacks, so a member
the file leaves out altogether is one path.
"""

LEGACY_FULL: dict[str, object] = {
    'inner': FULL_INNER, 'items': [FULL_INNER], 'parts': {'a': FULL_INNER},
    'limits': {'low': 1}}
"""Values of a file that holds every member of `LegacyNestedCfg`."""

LEGACY_GAPS: list[tuple[dict[str, object], tuple[str, ...], str]] = [
    ({'inner': {'width': 9}}, ('inner', 'height'), 'inner.height'),
    ({'items': [{'height': 8}]}, ('items', '0', 'width'), 'items[0].width'),
    ({'parts': {'a': {'width': 9}}}, ('parts', 'a', 'height'),
     'parts[a].height'),
    ({'limits': {}}, ('limits', 'low'), 'limits[low]')]
"""What replaces part of `LEGACY_FULL`, the row path and the reported path.

Each leaves out one value at a depth below the members: in a nested object,
in one inside a list, in one inside a dict, and in a checked dict.
"""

WRONG_SHAPES = [{'inner': 5, 'limits': {'low': 1}},
                {'inner': FULL_INNER, 'limits': [1]}]
"""Values of files for `NestedCfg` with a value of the wrong JSON shape."""


def _written(tmp_path: Path, data: object) -> Path:
    """Write one JSON file in the temporary folder and return its path."""
    path = tmp_path / 'config.json'
    path.write_text(json.dumps(data), encoding='UTF-8')
    return path


def _text_file(tmp_path: Path, text: str) -> Path:
    """Write one file holding exactly the given text and return its path."""
    path = tmp_path / 'config.json'
    path.write_text(text, encoding='UTF-8')
    return path


def _refusal(config: Config, in_file: Path,
             policy: LoadPolicy = DEFAULT_POLICY,
             loader: Optional[ConfigLoader] = None) -> ConfigLoadError:
    """Load one file, expect a refusal, and return it."""
    with pytest.raises(ConfigLoadError) as refused:
        load_config(config=config, in_file=in_file, policy=policy,
                    loader=loader)
    return refused.value


def _values(config: Config) -> dict[str, object]:
    """Return the members of one configuration object as the file has them."""
    loaded = json.loads(config.as_json_string(stderr_file=StringIO()))
    assert isinstance(loaded, dict)
    return loaded


def _hook_of(config: Config) -> Optional[ConfigAutoChangeHook]:
    """Return the hook that one `HookCfg` object was constructed with."""
    assert isinstance(config, HookCfg)
    return config.hook_given()


def _flat(config: Config) -> FlatCfg:
    """Return one configuration object as the `FlatCfg` it has to be."""
    assert isinstance(config, FlatCfg)
    return config


def test_no_file_no_load() -> None:
    """Test the caller's own object is what is edited without a file.

    A caller then has one code path for both cases, and the object it handed
    over is the one it gets back rather than a copy of it.
    """
    config = FlatCfg()
    loaded = load_config(config=config)
    assert loaded.config is config
    assert loaded.report == LoadReport()


def test_empty_report() -> None:
    """Test a report that says nothing happened says nothing at all."""
    assert LoadReport().message == ''
    assert not LoadReport().filled


@pytest.mark.parametrize('policy', EVERY_POLICY)
def test_complete_file(tmp_path: Path, policy: LoadPolicy) -> None:
    """Test a file holding every value is read by every policy alike."""
    loaded = load_config(config=FlatCfg(), policy=policy,
                         in_file=_written(tmp_path, COMPLETE))
    assert _flat(loaded.config).name == 'From a file'
    assert _flat(loaded.config).answer == 7
    assert loaded.report == LoadReport()


@pytest.mark.parametrize('policy', [LoadPolicy.DEFAULTS,
                                    LoadPolicy.STRICT_THEN_DEFAULTS])
def test_incomplete_filled(tmp_path: Path, policy: LoadPolicy) -> None:
    """Test the declared default fills in a value the file does not hold."""
    loaded = load_config(config=FlatCfg(), policy=policy,
                         in_file=_written(tmp_path, INCOMPLETE_DATA))
    assert _flat(loaded.config).name == 'Only a name'
    assert _flat(loaded.config).answer == 42
    assert loaded.report.filled == frozenset({'answer'})
    assert FILLED_MESSAGE in loaded.report.message


def test_incomplete_strict(tmp_path: Path) -> None:
    """Test a strict policy refuses a file that leaves a value out.

    The retry that looks for an unknown key behind the missing one happens
    under this policy too, because `config_as_json` reports a missing key
    first. The retry only decides which message; it never opens the file.
    """
    error = _refusal(config=FlatCfg(), policy=LoadPolicy.STRICT,
                     in_file=_written(tmp_path, INCOMPLETE_DATA))
    assert error.message == INCOMPLETE
    assert 'No value for answer' in error.diagnostics


@pytest.mark.parametrize('policy', EVERY_POLICY)
def test_unknown_key(tmp_path: Path, policy: LoadPolicy) -> None:
    """Test a key the configuration does not declare is never rescued.

    Filling in from the defaults governs the keys that are missing and
    nothing else, so this file is refused by every policy.
    """
    error = _refusal(config=FlatCfg(), policy=policy,
                     in_file=_written(tmp_path, UNKNOWN_DATA))
    assert error.message == UNKNOWN_KEY
    assert 'Unexpected parameter colour' in error.diagnostics


@pytest.mark.parametrize('policy', EVERY_POLICY)
def test_not_json(tmp_path: Path, policy: LoadPolicy) -> None:
    """Test a file that is not JSON at all is refused by every policy."""
    error = _refusal(config=FlatCfg(), policy=policy,
                     in_file=_text_file(tmp_path, 'answer = 7\n'))
    assert error.message == NOT_CONFIG
    assert 'failed to load JSON' in error.diagnostics


@pytest.mark.parametrize('policy', EVERY_POLICY)
def test_json_not_object(tmp_path: Path, policy: LoadPolicy) -> None:
    """Test JSON that is not an object is refused rather than half read."""
    error = _refusal(config=FlatCfg(), policy=policy,
                     in_file=_written(tmp_path, [1, 2]))
    assert error.message == NOT_CONFIG


@pytest.mark.parametrize('policy', EVERY_POLICY)
def test_bad_enum_name(tmp_path: Path, policy: LoadPolicy) -> None:
    """Test a name that is no enum member makes the file unreadable.

    An enum name is turned into a member while the JSON is being read, so
    text that names no member means the file cannot be read as configuration
    at all. The same text typed into a field is kept, because a name is not a
    name for most of the time it takes to type it.
    """
    error = _refusal(config=EnumCfg(), policy=policy,
                     in_file=_written(tmp_path, {'colour': 'PURPLE'}))
    assert error.message == NOT_CONFIG
    assert 'is not one of: RED, GREEN' in error.diagnostics


@pytest.mark.parametrize('policy', EVERY_POLICY)
def test_bad_value(tmp_path: Path, policy: LoadPolicy) -> None:
    """Test a file whose values are refused cannot be opened.

    A member validator returns the value that is stored back into the
    member, so a load that stopped part way through leaves it unknown which
    values were already rewritten. There is nothing honest to show.
    """
    error = _refusal(config=RangeCfg(), policy=policy,
                     in_file=_written(tmp_path, BAD_VALUE_DATA))
    assert error.message == BAD_VALUES
    assert 'greater than maximum 100' in error.diagnostics


def test_missing_file(tmp_path: Path) -> None:
    """Test a file that is not there is a message and not an exit.

    `Config.read()` ends the process with `sys.exit` for this, which an
    editor cannot do, so the file is read by the editor itself.
    """
    missing = tmp_path / 'not_there.json'
    error = _refusal(config=FlatCfg(), in_file=missing)
    assert error.message == NO_FILE.format(name=missing)


def test_not_text(tmp_path: Path) -> None:
    """Test a file that is not UTF-8 text is refused as that, not as JSON."""
    path = tmp_path / 'config.json'
    path.write_bytes(b'{"name": "\xff\xfe"}')
    error = _refusal(config=FlatCfg(), in_file=path)
    assert error.message == NOT_TEXT.format(name=path)


def test_folder_not_file(tmp_path: Path) -> None:
    """Test a name that is a folder is refused as a file that cannot open."""
    error = _refusal(config=FlatCfg(), in_file=tmp_path)
    assert error.message == NO_FILE.format(name=tmp_path)


def test_cannot_construct(tmp_path: Path) -> None:
    """Test a class the editor cannot construct is refused, not crashed on.

    The editor knows nothing about a constructor argument of the application's
    own, so this is a refusal that names the class. An application whose class
    is like this hands over a loader, which is the test below.
    """
    error = _refusal(config=ExtraArgCfg(home='here'),
                     in_file=_written(tmp_path, {'home': 'there'}))
    assert error.message == NO_DEFAULTS.format(name='ExtraArgCfg')
    assert 'home' in error.diagnostics


def test_no_member_declared(tmp_path: Path) -> None:
    """Test a class with no public member is refused as one that cannot be.

    `config_as_json` has nothing to read a file into for such a class, and it
    says so with an `AttributeError` rather than with a refusal of its own.
    It is the same answer as for a constructor argument the editor knows
    nothing about, because it is the same thing from here: the editor cannot
    build an object of this class.
    """
    error = _refusal(config=FlatCfg(), loader=no_member_loader,
                     in_file=_written(tmp_path, COMPLETE))
    assert error.message == NO_DEFAULTS.format(name='FlatCfg')
    assert 'No object variables' in error.diagnostics


def test_wrong_type_refused(tmp_path: Path) -> None:
    """Test a value of a type the class refuses is the values being refused.

    A validator of an application is free to raise what a wrong type raises in
    Python, and the editor has to tell that apart from a class it cannot
    construct at all: this one it constructs perfectly well, so what is wrong
    is the file and not the class.
    """
    error = _refusal(config=WholeOnlyCfg(),
                     in_file=_written(tmp_path, {'answer': 'not a number'}))
    assert error.message == BAD_VALUES
    assert NOT_A_NUMBER.format(name='answer') in error.diagnostics


def test_loader_constructs_it(tmp_path: Path) -> None:
    """Test a loader is what opens a file of a class like that.

    The argument the editor knows nothing about is bound where the loader is
    written, so the load has everything it needs and the file opens.
    """
    loaded = load_config(config=ExtraArgCfg(home='here'),
                         in_file=_written(tmp_path, {'home': 'from a file'}),
                         loader=extra_arg_loader)
    assert getattr(loaded.config, 'home') == 'from a file'
    assert loaded.report.message == ''


def test_loader_may_choose(tmp_path: Path) -> None:
    """Test the class a loader chose for the file is the class that is edited.

    Which class a session is about is settled here and nowhere else, which is
    what the two `--class` cases of the programs and the check that a save
    makes are both about.
    """
    values = {'name': PICKED_NAME, 'answer': 3}
    loaded = load_config(config=FlatCfg(), loader=picking_loader,
                         in_file=_written(tmp_path, values))
    assert isinstance(loaded.config, PickedCfg)
    assert EditModel(loaded.config).config_type_name == 'PickedCfg'


def test_loader_that_exits(tmp_path: Path) -> None:
    """Test a loader that ends the program is a refusal and not the end.

    `config_as_json` ends the process for a file it cannot make sense of, so a
    loader written around it does that too, and an editor that let it would
    cost the user the session. It is reported as the values of the file being
    ones this application will not have, which is what happened.
    """
    error = _refusal(config=FlatCfg(), in_file=_written(tmp_path, COMPLETE),
                     loader=exiting_loader)
    assert error.message == BAD_VALUES
    assert LOADER_EXITED in error.diagnostics


def test_no_hook_forwarded(tmp_path: Path) -> None:
    """Test a load offers no hook to a class whose constructor declares one.

    What a load recorded is read from the object it produced, so a class that
    declares the parameter is constructed exactly like one that does not and
    the object holds the hook that `Config` gave it.
    """
    loaded = load_config(config=HookCfg(),
                         in_file=_written(tmp_path, COMPLETE))
    assert _hook_of(loaded.config) is None
    assert isinstance(loaded.config.auto_change_hook(), ConfigAutoChangeHook)


def test_class_without_hook(tmp_path: Path) -> None:
    """Test a class that does not declare the hook is loaded as any other.

    Every other test of this module already loads such a class, and this one
    says that it is loaded by the same construction: nothing is passed for the
    automatic changes, so there is no parameter a class can be refused over.
    """
    loaded = load_config(config=FlatCfg(),
                         in_file=_written(tmp_path, COMPLETE))
    assert _flat(loaded.config).answer == 7


def test_caller_not_changed(tmp_path: Path) -> None:
    """Test the caller's own object is not the one the file was read into."""
    config = FlatCfg()
    loaded = load_config(config=config, in_file=_written(tmp_path, COMPLETE))
    assert loaded.config is not config
    assert config.name == 'flat text'
    assert config.answer == 42


def test_nothing_printed(tmp_path: Path,
                         capsys: pytest.CaptureFixture[str]) -> None:
    """Test what the load says is reported and not printed.

    An application that runs the editor has a screen and not a terminal
    behind it, so what the load has to say belongs where the editor can show
    it and not in whatever was behind the window.
    """
    path = _written(tmp_path, UNKNOWN_DATA)
    error = _refusal(config=FlatCfg(), in_file=path)
    assert 'Unexpected parameter colour' in error.diagnostics
    assert capsys.readouterr().err == ''


def test_refusal_text(tmp_path: Path) -> None:
    """Test a refusal reads as the message with the diagnostics below it."""
    path = _written(tmp_path, UNKNOWN_DATA)
    error = _refusal(config=FlatCfg(), in_file=path)
    assert str(error) == f'{error.message}\n{error.diagnostics}'


def test_refusal_without_text() -> None:
    """Test a refusal that has no diagnostics is just its message."""
    assert str(ConfigLoadError('no room')) == 'no room'


def test_omitted_filled(tmp_path: Path) -> None:
    """Test an optional member the file leaves out is not one that is filled.

    It holds None, which a strict load gives it as well, so the declared
    defaults supplied nothing for it. Only the required member the file left
    out was filled in.
    """
    loaded = load_config(config=OmitCfg(),
                         in_file=_written(tmp_path, {'first': 5}))
    assert loaded.report.filled == frozenset({'last'})
    assert _values(loaded.config) == {'first': 5, 'last': 2}


def test_optional_member_read(tmp_path: Path) -> None:
    """Test an optional member the file does hold is read and not filled."""
    data = {'first': 5, 'optional': 'from file', 'last': 2}
    loaded = load_config(config=OmitCfg(), in_file=_written(tmp_path, data))
    assert not loaded.report.filled
    assert _values(loaded.config) == data


def test_report_reaches_model(tmp_path: Path) -> None:
    """Test the model marks the rows that the declared defaults supplied."""
    loaded = load_config(config=FlatCfg(),
                         in_file=_written(tmp_path, INCOMPLETE_DATA))
    model = EditModel(config=loaded.config, report=loaded.report)
    marked = {row.name: row.filled_from_default for row in model.rows}
    assert marked == {'name': False, 'answer': True}
    assert model.load_message == loaded.report.message


def test_model_without_report() -> None:
    """Test a model built without a report marks nothing and says nothing."""
    model = EditModel(FlatCfg())
    assert not any(row.filled_from_default for row in model.rows)
    assert model.load_message == ''


def test_filled_stays_marked(tmp_path: Path) -> None:
    """Test editing a filled in member does not unmark it.

    That the file did not hold this value stays true whatever the user then
    types into it, and the edited mark is what says the user has been there.
    """
    loaded = load_config(config=FlatCfg(),
                         in_file=_written(tmp_path, INCOMPLETE_DATA))
    model = EditModel(config=loaded.config, report=loaded.report)
    model.set_text(path=('answer',), text='9')
    row = {one.name: one for one in model.rows}['answer']
    assert row.filled_from_default
    assert row.edited


def test_buffer_is_the_file(tmp_path: Path) -> None:
    """Test the buffer holds the values of the file and not the defaults."""
    loaded = load_config(config=FlatCfg(),
                         in_file=_written(tmp_path, COMPLETE))
    model = EditModel(config=loaded.config, report=loaded.report)
    assert [row.value for row in model.rows] == ['From a file', 7]
    assert not model.dirty


def test_no_file_keeps_object() -> None:
    """Test the caller's object is used as it is when there is no file.

    Nothing is constructed then, so the object keeps whatever hook the
    application gave it, which is none here.
    """
    config = HookCfg()
    assert load_config(config=config).config is config
    assert _hook_of(config) is None


def _named(tmp_path: Path, name: str) -> Path:
    """Write one complete input file under one name and return its path."""
    path = tmp_path / name
    path.write_text(json.dumps(COMPLETE), encoding='UTF-8')
    return path


@pytest.mark.parametrize('name', ['config.cfg', 'config.CFG'])
def test_enforced_opens(tmp_path: Path, name: str) -> None:
    """Test a file with the enforced extension is opened as any other is."""
    settings = Settings(file_extension='.cfg', extension_enforced=True)
    loaded = load_config(config=FlatCfg(), in_file=_named(tmp_path, name),
                         settings=settings)
    assert isinstance(loaded.config, FlatCfg)
    assert loaded.config.answer == 7


@pytest.mark.parametrize('name', ['config.json', 'config'])
def test_enforced_refuses(tmp_path: Path, name: str) -> None:
    """Test a file without the enforced extension cannot be opened.

    A name to read is never completed with the extension either, because it
    names a file that already exists and completing it would open a
    different file from the one that was asked for.
    """
    settings = Settings(file_extension='.cfg', extension_enforced=True)
    with pytest.raises(ConfigLoadError, match='.cfg extension'):
        load_config(config=FlatCfg(), in_file=_named(tmp_path, name),
                    settings=settings)


@pytest.mark.parametrize('name', ['config.json', 'config'])
def test_default_ext_opens(tmp_path: Path, name: str) -> None:
    """Test an extension that is only a default says nothing about reading.

    It is about what the editor writes when the user did not say, and a file
    that is there to be read has already been named by somebody.
    """
    loaded = load_config(config=FlatCfg(), in_file=_named(tmp_path, name),
                         settings=Settings(file_extension='.cfg'))
    assert isinstance(loaded.config, FlatCfg)
    assert loaded.config.answer == 7


def test_load_asks_callable(tmp_path: Path) -> None:
    """Test a callable is asked for the settings of one load."""
    asked: list[int] = []

    def answer() -> Settings:
        """Answer with an application that enforces its extension."""
        asked.append(1)
        return Settings(file_extension='.cfg', extension_enforced=True)
    with pytest.raises(ConfigLoadError):
        load_config(config=FlatCfg(), settings=answer,
                    in_file=_named(tmp_path, 'config.json'))
    assert asked


@pytest.mark.parametrize('policy', FILLING_POLICIES)
@pytest.mark.parametrize(('builder', 'data', 'paths'), FILLED_CASES)
def test_nested_filled(tmp_path: Path, policy: LoadPolicy,
                       builder: Callable[[], Config], data: dict[str, object],
                       paths: set[tuple[str, ...]]) -> None:
    """Test the declared defaults fill in what a file lacks at every depth.

    A file that leaves a value out of a nested object is merely incomplete,
    exactly as one that leaves out a member, so it opens and says so.
    """
    loaded = load_config(config=builder(), policy=policy,
                         in_file=_written(tmp_path, data))
    assert loaded.report.filled_paths == frozenset(paths)
    assert loaded.report.filled == frozenset(path[0] for path in paths
                                             if len(path) == 1)
    assert FILLED_MESSAGE in loaded.report.message


def test_nested_value_kept(tmp_path: Path) -> None:
    """Test the value a nested object lacks is its declared default."""
    loaded = load_config(config=NestedCfg(),
                         in_file=_written(tmp_path, NESTED_GAP))
    assert _values(loaded.config)['inner'] == {'width': 9, 'height': 6}


def test_nested_strict(tmp_path: Path) -> None:
    """Test a strict policy refuses a file lacking a nested value as such.

    The file is incomplete and holds no key this configuration lacks, so it
    is refused for being incomplete, with the path of the missing value.
    """
    error = _refusal(config=NestedCfg(), policy=LoadPolicy.STRICT,
                     in_file=_written(tmp_path, NESTED_GAP))
    assert error.message == INCOMPLETE
    assert 'No value for inner.height' in error.diagnostics


@pytest.mark.parametrize('policy', EVERY_POLICY)
def test_nested_unknown(tmp_path: Path, policy: LoadPolicy) -> None:
    """Test a key that a nested object does not declare is never rescued."""
    data = {'inner': FULL_INNER | {'depth': 3}, 'limits': {'low': 1}}
    error = _refusal(config=NestedCfg(), policy=policy,
                     in_file=_written(tmp_path, data))
    assert error.message == UNKNOWN_KEY
    assert 'Unexpected parameter inner.depth' in error.diagnostics


@pytest.mark.parametrize('policy', EVERY_POLICY)
def test_missing_and_unknown(tmp_path: Path, policy: LoadPolicy) -> None:
    """Test a file both incomplete and with an unknown key is refused for it.

    `config_as_json` checks for a missing key first, so a strict load fails
    over that, and it is the retry that finds the key no policy rescues.
    """
    error = _refusal(config=FlatCfg(), policy=policy,
                     in_file=_written(tmp_path, {'name': 'n', 'colour': 1}))
    assert error.message == UNKNOWN_KEY
    assert 'Unexpected parameter colour' in error.diagnostics


@pytest.mark.parametrize('policy', EVERY_POLICY)
@pytest.mark.parametrize('data', WRONG_SHAPES)
def test_wrong_shape(tmp_path: Path, policy: LoadPolicy,
                     data: dict[str, object]) -> None:
    """Test a value of the wrong JSON shape is refused as that.

    It is neither a missing nor an unknown key, so neither of their messages
    would be true of it.
    """
    error = _refusal(config=NestedCfg(), policy=policy,
                     in_file=_written(tmp_path, data))
    assert error.message == WRONG_SHAPE


@pytest.mark.filterwarnings('ignore::DeprecationWarning')
@pytest.mark.parametrize(('policy', 'message'),
                         [(LoadPolicy.DEFAULTS, NOT_FILLABLE),
                          (LoadPolicy.STRICT_THEN_DEFAULTS, NOT_FILLABLE),
                          (LoadPolicy.STRICT, INCOMPLETE)])
def test_not_fillable(tmp_path: Path, policy: LoadPolicy,
                      message: str) -> None:
    """Test a file the defaults cannot complete is not called unknown.

    A factory that does not accept `ok_to_use_defaults` builds its nested
    object strictly, so the retry lacks the same value again. The file is
    incomplete, which a strict policy says, and the others say that the
    configuration cannot fill it in.
    """
    data = {'inner': {'width': 1}, 'answer': 3}
    error = _refusal(config=LegacyFactoryCfg(), policy=policy,
                     in_file=_written(tmp_path, data))
    assert error.message == message
    assert 'No value for inner.height' in error.diagnostics


@pytest.mark.parametrize('policy', FILLING_POLICIES)
@pytest.mark.parametrize(('gap', 'path'), [case[:2] for case in LEGACY_GAPS])
def test_legacy_filled(tmp_path: Path, policy: LoadPolicy,
                       gap: dict[str, object], path: tuple[str, ...]) -> None:
    """Test a class written for 1.8 has a value left out deep filled in.

    No constructor of it accepts `ok_to_use_defaults`, as in an application
    unchanged since 1.0.0, and the file is still merely incomplete.
    """
    loaded = load_config(config=LegacyNestedCfg(), policy=policy,
                         in_file=_written(tmp_path, LEGACY_FULL | gap))
    assert loaded.report.filled_paths == frozenset({path})
    assert FILLED_MESSAGE in loaded.report.message


@pytest.mark.parametrize(('gap', 'named'),
                         [(gap, named) for gap, _, named in LEGACY_GAPS])
def test_legacy_strict(tmp_path: Path, gap: dict[str, object],
                       named: str) -> None:
    """Test a strict policy refuses that file as incomplete, naming the path.

    It is never refused as holding a key this configuration does not have.
    """
    error = _refusal(config=LegacyNestedCfg(), policy=LoadPolicy.STRICT,
                     in_file=_written(tmp_path, LEGACY_FULL | gap))
    assert error.message == INCOMPLETE
    assert f'No value for {named} ' in error.diagnostics


@pytest.mark.parametrize('policy', EVERY_POLICY)
def test_legacy_unknown(tmp_path: Path, policy: LoadPolicy) -> None:
    """Test a key a nested object of a 1.8 class lacks is refused as that.

    The nested object of the file also lacks a value, which `config_as_json`
    reports first, and the key that no policy rescues is still what decides.
    """
    data = LEGACY_FULL | {'inner': {'width': 9, 'depth': 3}}
    error = _refusal(config=LegacyNestedCfg(), policy=policy,
                     in_file=_written(tmp_path, data))
    assert error.message == UNKNOWN_KEY
    assert 'Unexpected parameter inner.depth' in error.diagnostics


@pytest.mark.parametrize('policy', EVERY_POLICY)
def test_validator_key_error(tmp_path: Path, policy: LoadPolicy) -> None:
    """Test a `KeyError` of a validator is the values being refused.

    It says nothing about the keys of the file, which `config_as_json`
    reports with exceptions of their own types.
    """
    error = _refusal(config=LookupCfg(), policy=policy,
                     in_file=_written(tmp_path, {'name': 'gamma'}))
    assert error.message == BAD_VALUES
    assert UNKNOWN_NAME.format(name='gamma') in error.diagnostics


def test_nested_row_marked(tmp_path: Path) -> None:
    """Test the model marks the row of the nested value that was filled in.

    Only that row is marked: the member holding it and the value beside it
    are what the file held.
    """
    loaded = load_config(config=NestedCfg(),
                         in_file=_written(tmp_path, NESTED_GAP))
    model = EditModel(config=loaded.config, report=loaded.report)
    marked = {row.path for row in model.rows if row.filled_from_default}
    assert marked == {('inner', 'height')}


@pytest.mark.parametrize('policy', EVERY_POLICY)
def test_bad_defaults_load(tmp_path: Path, policy: LoadPolicy) -> None:
    """Test a class whose declared values are refused opens a valid file.

    Its constructor takes the load policy, so the editor gives it the text of
    the file together with the policy, and the declared values are never
    validated on their own. The object the editor is given has to be read from
    a file as well, which is what such an application does.
    """
    config = BadDefaultCfg(json.dumps({'answer': 5}))
    loaded = load_config(config=config, policy=policy,
                         in_file=_written(tmp_path, {'answer': 7}))
    assert _values(loaded.config) == {'answer': 7}
