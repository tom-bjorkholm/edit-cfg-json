#! /usr/bin/env python3
"""Tests for reading the configuration to edit from one input file.

Every load is driven through a file in a temporary folder rather than through
text, because reading the file is part of what is being tested: a file that
is missing, or that is not text at all, has to be refused with a message and
not with the `sys.exit` that `config_as_json` does on its own.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

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
    INCOMPLETE, NOT_CONFIG, NOT_TEXT, NO_DEFAULTS, NO_FILE, UNKNOWN_KEY
from .sample_cfg import PICKED_NAME, EnumCfg, ExtraArgCfg, FlatCfg, \
    HookCfg, OmitCfg, PickedCfg, RangeCfg, exiting_loader, extra_arg_loader, \
    picking_loader

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

    The retry that tells an incomplete file from one with an unknown key
    happens under this policy too, because the two need different messages.
    The retry only decides which message; it never opens the file.
    """
    error = _refusal(config=FlatCfg(), policy=LoadPolicy.STRICT,
                     in_file=_written(tmp_path, INCOMPLETE_DATA))
    assert error.message == INCOMPLETE
    assert 'No value for answer' in error.diagnostics


@pytest.mark.parametrize('policy', EVERY_POLICY)
def test_unknown_key(tmp_path: Path, policy: LoadPolicy) -> None:
    """Test a key the configuration does not declare is never rescued.

    Filling in from the defaults governs the keys that are missing and
    nothing else, so this file is refused by every policy. That is what makes
    the retry able to tell the two failures apart.
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


def test_hook_forwarded(tmp_path: Path) -> None:
    """Test the hook reaches a class whose constructor declares it."""
    loaded = load_config(config=HookCfg(),
                         in_file=_written(tmp_path, COMPLETE))
    assert isinstance(_hook_of(loaded.config), ConfigAutoChangeHook)


def test_hook_not_forced(tmp_path: Path) -> None:
    """Test a class that does not declare the hook is loaded without it.

    Every other test of this module already loads such a class, but this one
    says why it works: offering the hook to a class that does not take it
    would make the load fail with a `TypeError`.
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
    """Test an optional member the file leaves out is filled in and named.

    Such a member has no row while it is None, so the name is reported and
    the model has nothing to mark. Reporting it anyway is what keeps the
    report about the file rather than about what the editor can show.
    """
    loaded = load_config(config=OmitCfg(),
                         in_file=_written(tmp_path, {'first': 5}))
    assert loaded.report.filled == frozenset({'optional', 'last'})
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


def test_hook_without_file() -> None:
    """Test the caller's object is used as it is when there is no file.

    Nothing is constructed then, so the hook question does not arise, and
    the object keeps whatever hook the application gave it.
    """
    config = HookCfg()
    assert _hook_of(load_config(config=config).config) is None


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
