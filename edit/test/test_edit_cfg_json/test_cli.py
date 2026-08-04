#! /usr/bin/env python3
"""Tests for the command line that all three programs of this library share.

The program is what makes any configuration class in reach editable without a
line of user interface code, so most of what is tested here is the two doors to
a module, the two ways of saying what to edit in it, and every way of being
refused at any of them. Every refusal is checked for both its message and its
exit code: a program of this library is meant to be used from a script, so the
number it ends with is as much part of what it promises as the sentence it
prints.

The backend is a stub throughout, which is the point of `run_cli` taking one:
none of this needs a display or a toolkit.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from argparse import ArgumentParser
from pathlib import Path
from typing import Optional
import json
import sys
import pytest
from edit_cfg_json import DumpEditor, EditModel, EditorBackend, ExitCode, \
    LoadPolicy, add_file_options, named_policy, run_cli
from edit_cfg_json.cli import LOADER_ARGS_MESSAGE, NOT_CONFIG_MESSAGE, \
    NOT_DESCRIPTIONS, NOT_IMPORTABLE_MESSAGE, NOT_LOADER_MESSAGE, \
    NOT_PYTHON_MESSAGE, NOT_SHOWABLE_MESSAGE, NO_FILE_MESSAGE, \
    NO_LOADER_CONFIG, NO_MODULE_MESSAGE, NO_NAME_MESSAGE, NO_TARGET_MESSAGE, \
    WRONG_CLASS_MESSAGE
from .sample_cfg import ABOUT_FLAT_NAME, HOME_VALUE, PICKED_NAME

PROGRAM = 'edit-cfg-json-test'
"""Name the program is given in these tests, which is in every refusal."""

SAMPLE = 'test_edit_cfg_json.sample_cfg'
"""Module of the configuration classes that these tests reach through it.

It is this test package's own module, so the `--module` door is tested against
something that is really importable rather than against a stand-in for one.
"""

FILE_MODULE = '''"""A configuration class in a file of its own."""

from typing import Optional, TextIO
import sys
from config_as_json import Config, PathOrStr, ValidationPlan


class FileCfg(Config):
    """A configuration class that lives in a file and not in a package."""

    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Declare the one member and then apply the JSON."""
        self.name: str = 'from a file'
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file)

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return no extra validation steps."""
        _ = stderr_file
        return []
'''
"""A whole configuration module, written to a file by the tests that need it.

It imports nothing of its own, because that is the case the `--file` door is
for: a class that is not installed and does not belong to a package.
"""

RELATIVE_MODULE = 'from .neighbour import thing\n'
"""A module that only its own package could import."""

BROKEN_MODULE = 'class Cfg(:\n'
"""A file that ends in `.py` and that Python cannot compile."""


class Recorder:  # pylint: disable=too-few-public-methods
    """A backend that keeps the model it was given and does nothing to it."""

    def __init__(self) -> None:
        """Create a backend that has not been given a model yet."""
        self.model: Optional[EditModel] = None

    def run_editor(self, model: EditModel) -> None:
        """Keep the model, so that a test can read what the program built."""
        self.model = model


class Saver:  # pylint: disable=too-few-public-methods
    """A backend that saves, which is what a user pressing Save would do."""

    def run_editor(self, model: EditModel) -> None:
        """Write the output file of the model."""
        model.save()


def _run(backend: EditorBackend, *args: str, interactive: bool = True) -> int:
    """Run the program once with one backend and one command line.

    The stubs above are accepted here because `EditorBackend` is a protocol:
    anything with a `run_editor` method is one, which is the whole reason a
    program of this library can be tested with no display.

    Args:
        backend: Backend to run the session in.
        args: The whole command line, without the program name.
        interactive: Whether this program's backend gives the user a session.

    Returns:
        What that run ended with.
    """
    return run_cli(backend=backend, prog=PROGRAM, args=list(args),
                   interactive=interactive)


def _named(class_name: str, *args: str) -> list[str]:
    """Return the command line that names one class of the sample module.

    Args:
        class_name: Class of that module to edit.
        args: The rest of the command line.

    Returns:
        A whole command line, without the program name.
    """
    return ['--module', SAMPLE, '--class', class_name, *args]


def _loaded(loader_name: str, *args: str) -> list[str]:
    """Return the command line that names one loader of the sample module.

    Args:
        loader_name: Name in that module that `--loader` is given.
        args: The rest of the command line.

    Returns:
        A whole command line, without the program name.
    """
    return ['--module', SAMPLE, '--loader', loader_name, *args]


def _written(path: Path, text: str) -> Path:
    """Write one file for a test and return its path.

    Args:
        path: File to write.
        text: What to write into it.

    Returns:
        That path.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='UTF-8')
    return path


def _input_file(tmp_path: Path, **values: object) -> str:
    """Write one configuration file and return its name.

    Args:
        tmp_path: Folder of one test.
        values: The members that the file holds.

    Returns:
        The name of that file, as a command line takes it.
    """
    return str(_written(tmp_path / 'in.json', json.dumps(values)))


@pytest.mark.parametrize('args', [(), ('--module', SAMPLE, '--file', 'x.py')])
def test_one_location(args: tuple[str, ...],
                      capsys: pytest.CaptureFixture[str]) -> None:
    """Test the class is told through exactly one of the two doors.

    Neither door and both doors are the same mistake, and `argparse` is what
    reports both of them, which is the whole reason the two are separate
    options rather than one `module:Class` argument.
    """
    with pytest.raises(SystemExit) as exit_info:
        _run(Recorder(), *args, '--class', 'FlatCfg')
    assert exit_info.value.code == ExitCode.USAGE
    assert PROGRAM in capsys.readouterr().err


def test_class_name_needed(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a run that names no class at all is refused by argparse."""
    with pytest.raises(SystemExit) as exit_info:
        _run(Recorder(), '--module', SAMPLE)
    assert exit_info.value.code == ExitCode.USAGE
    assert PROGRAM in capsys.readouterr().err


def test_no_such_module(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a module that cannot be imported is refused by name."""
    assert _run(Recorder(), '--module', 'no_such_module_here', '--class',
                'FlatCfg') == ExitCode.NO_MODULE
    said = capsys.readouterr().err
    assert NO_MODULE_MESSAGE.format(name='no_such_module_here') in said
    assert 'ModuleNotFoundError' in said


def test_no_such_file(tmp_path: Path,
                      capsys: pytest.CaptureFixture[str]) -> None:
    """Test a file that is not there is refused by name."""
    missing = tmp_path / 'nowhere.py'
    assert _run(Recorder(), '--file', str(missing), '--class',
                'FileCfg') == ExitCode.NO_FILE
    assert NO_FILE_MESSAGE.format(name=missing) in capsys.readouterr().err


@pytest.mark.parametrize('name,text', [('notes.txt', FILE_MODULE),
                                       ('broken.py', BROKEN_MODULE)])
def test_not_python(name: str, text: str, tmp_path: Path,
                    capsys: pytest.CaptureFixture[str]) -> None:
    """Test a file Python cannot import as a module is refused.

    A name that is no `.py` file at all and a `.py` file that does not compile
    are the same thing to whoever ran the program, so they are the same
    refusal with the same number.
    """
    path = _written(tmp_path / name, text)
    assert _run(Recorder(), '--file', str(path), '--class',
                'FileCfg') == ExitCode.NOT_PYTHON
    assert NOT_PYTHON_MESSAGE.format(name=path) in capsys.readouterr().err


def test_needs_its_package(tmp_path: Path,
                           capsys: pytest.CaptureFixture[str]) -> None:
    """Test a module with a relative import says to use the other door.

    A path names no package, so there is nothing a bare file name can do about
    a relative import. The refusal has to say what will work instead.
    """
    path = _written(tmp_path / 'inside.py', RELATIVE_MODULE)
    assert _run(Recorder(), '--file', str(path), '--class',
                'FileCfg') == ExitCode.NOT_IMPORTABLE
    said = capsys.readouterr().err
    assert NOT_IMPORTABLE_MESSAGE.format(name=path) in said
    assert '--module' in said


def test_no_such_name(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a name the module does not hold is refused by name."""
    assert _run(Recorder(), *_named('NotThere')) == ExitCode.NO_NAME
    assert NO_NAME_MESSAGE.format(module=SAMPLE,
                                  name='NotThere') in capsys.readouterr().err


def test_not_a_config(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a name that is not a configuration class is refused.

    `REFUSAL_MESSAGE` is a piece of text in that module, so it is a name the
    module really holds and really is not a class of the right kind.
    """
    outcome = _run(Recorder(), *_named('REFUSAL_MESSAGE'))
    assert outcome == ExitCode.NOT_CONFIG
    expected = NOT_CONFIG_MESSAGE.format(module=SAMPLE, name='REFUSAL_MESSAGE')
    assert expected in capsys.readouterr().err


def test_cannot_construct(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a class needing an argument of its own is refused by name."""
    outcome = _run(Recorder(), *_named('ExtraArgCfg'))
    assert outcome == ExitCode.NO_DEFAULTS
    assert 'ExtraArgCfg' in capsys.readouterr().err


def test_cannot_be_shown(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a class whose values are no JSON values is refused by name.

    The editor reads what it shows by serializing the configuration object, so
    a class that cannot write itself has nothing at all for it to show.
    """
    outcome = _run(Recorder(), *_named('NoJsonCfg'))
    assert outcome == ExitCode.NOT_SHOWABLE
    said = capsys.readouterr().err
    assert NOT_SHOWABLE_MESSAGE.format(name='NoJsonCfg') in said
    assert 'JsonWriteHookError' in said


def test_module_door() -> None:
    """Test a class reached through an importable module is edited."""
    backend = Recorder()
    assert _run(backend, *_named('FlatCfg')) == ExitCode.OK
    assert backend.model is not None
    assert [row.name for row in backend.model.rows] == ['name', 'answer']
    assert backend.model.config_type_name == 'FlatCfg'


def test_file_door(tmp_path: Path) -> None:
    """Test a class reached through a file of its own is edited."""
    path = _written(tmp_path / 'own_file.py', FILE_MODULE)
    backend = Recorder()
    assert _run(backend, '--file', str(path), '--class',
                'FileCfg') == ExitCode.OK
    assert backend.model is not None
    assert backend.model.rows[0].value == 'from a file'


def test_file_leaves_no_trace(tmp_path: Path) -> None:
    """Test the file door puts the path and the modules back as it found them.

    Both matter for a program that is run more than once in one process, and
    the modules matter most: a second file with the same stem would otherwise
    be found among the modules of the first and never be read at all.
    """
    path = _written(tmp_path / 'traceless.py', FILE_MODULE)
    saved_path = list(sys.path)
    assert _run(Recorder(), '--file', str(path), '--class',
                'FileCfg') == ExitCode.OK
    assert sys.path == saved_path
    assert 'traceless' not in sys.modules


def test_second_file_is_read(tmp_path: Path) -> None:
    """Test two files of the same name in one run are both really read."""
    first = _written(tmp_path / 'first' / 'same.py', FILE_MODULE)
    second = _written(tmp_path / 'second' / 'same.py',
                      FILE_MODULE.replace('from a file', 'from the second'))
    for path, expected in ((first, 'from a file'),
                           (second, 'from the second')):
        backend = Recorder()
        assert _run(backend, '--file', str(path), '--class',
                    'FileCfg') == ExitCode.OK
        assert backend.model is not None
        assert backend.model.rows[0].value == expected


def test_input_file_is_read(tmp_path: Path) -> None:
    """Test the values of the input file are the ones that are edited."""
    in_file = _input_file(tmp_path, name='from the file', answer=11)
    backend = Recorder()
    assert _run(backend, *_named('FlatCfg', '-i', in_file)) == ExitCode.OK
    assert backend.model is not None
    assert [row.value for row in backend.model.rows] == ['from the file', 11]
    assert backend.model.out_file == in_file


def test_input_refused(tmp_path: Path,
                       capsys: pytest.CaptureFixture[str]) -> None:
    """Test a file with a key the class does not have cannot be opened."""
    in_file = _input_file(tmp_path, name='a', answer=1, colour='red')
    outcome = _run(Recorder(), *_named('FlatCfg', '-i', in_file))
    assert outcome == ExitCode.LOAD_REFUSED
    assert 'key' in capsys.readouterr().err


@pytest.mark.parametrize('policy,complete,code',
                         [('strict', True, ExitCode.OK),
                          ('strict', False, ExitCode.LOAD_REFUSED),
                          ('defaults', True, ExitCode.OK),
                          ('defaults', False, ExitCode.OK),
                          ('strict-then-defaults', True, ExitCode.OK),
                          ('strict-then-defaults', False, ExitCode.OK)])
def test_policy_option(policy: str, complete: bool, code: ExitCode,
                       tmp_path: Path) -> None:
    """Test what each policy makes of a complete and an incomplete file."""
    values: dict[str, object] = {'name': 'a'}
    if complete:
        values['answer'] = 3
    in_file = _input_file(tmp_path, **values)
    backend = Recorder()
    arguments = _named('FlatCfg', '-i', in_file, '--policy', policy)
    assert _run(backend, *arguments) == code
    if code is ExitCode.OK:
        assert backend.model is not None
        assert backend.model.rows[1].filled_from_default is not complete


def test_output_is_chosen(tmp_path: Path) -> None:
    """Test the output file of a run is the one the command line named."""
    out_file = tmp_path / 'out.json'
    backend = Recorder()
    arguments = _named('FlatCfg', '-o', str(out_file))
    assert _run(backend, *arguments) == ExitCode.OK
    assert backend.model is not None
    assert backend.model.out_file == str(out_file)


def test_round_trip(tmp_path: Path) -> None:
    """Test a backend that saves writes a file the class can read back."""
    out_file = tmp_path / 'round.json'
    arguments = _named('FlatCfg', '-o', str(out_file))
    assert _run(Saver(), *arguments) == ExitCode.OK
    assert json.loads(out_file.read_text(encoding='UTF-8')) == {
        'name': 'flat text', 'answer': 42}


def test_save_option_writes(tmp_path: Path) -> None:
    """Test `--save` writes the file for a program with no Save to press."""
    out_file = tmp_path / 'asked.json'
    arguments = _named('FlatCfg', '-o', str(out_file), '--save')
    assert _run(DumpEditor(), *arguments, interactive=False) == ExitCode.OK
    assert out_file.is_file()


def test_save_is_not_offered(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a program whose user can press Save has no `--save` option.

    It is `argparse` that refuses it, because the option is not added at all,
    which is better than an option that exists and says it means nothing here.
    """
    with pytest.raises(SystemExit) as exit_info:
        _run(Recorder(), *_named('FlatCfg', '--save'))
    assert exit_info.value.code == ExitCode.USAGE
    assert '--save' in capsys.readouterr().err


def test_nothing_to_write() -> None:
    """Test `--save` with no destination says the file was not written."""
    outcome = _run(DumpEditor(), *_named('FlatCfg', '--save'),
                   interactive=False)
    assert outcome == ExitCode.NOT_WRITTEN


def test_invalid_is_reported() -> None:
    """Test a program with no user ends on the verdict of the buffer.

    `RoundTripCfg` writes a file that it would itself refuse to read, so the
    values it shows are not a configuration of it. A program that printed
    `invalid` and ended with success could not be used as a check.
    """
    outcome = _run(DumpEditor(), *_named('RoundTripCfg'), interactive=False)
    assert outcome == ExitCode.INVALID


def test_session_end_is_ok() -> None:
    """Test closing an editor is not a failure, whatever is in the fields."""
    assert _run(Recorder(), *_named('NoTextCfg')) == ExitCode.OK


def test_target_needed(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a run that names neither a class nor a loader is refused.

    `argparse` can be asked for exactly one of two options and not for at
    least one of them, so this refusal is written by hand and still ends the
    way every wrong command line ends.
    """
    with pytest.raises(SystemExit) as exit_info:
        _run(Recorder(), '--module', SAMPLE)
    assert exit_info.value.code == ExitCode.USAGE
    assert NO_TARGET_MESSAGE in capsys.readouterr().err


def test_loader_door() -> None:
    """Test a loader is what opens a class the editor cannot construct."""
    backend = Recorder()
    assert _run(backend, *_loaded('extra_arg_loader')) == ExitCode.OK
    assert backend.model is not None
    assert backend.model.config_type_name == 'ExtraArgCfg'
    assert [row.value for row in backend.model.rows] == [HOME_VALUE]


def test_loader_reads_file(tmp_path: Path) -> None:
    """Test the loader is what the input file of such a class is read with."""
    in_file = _input_file(tmp_path, home='from a file')
    backend = Recorder()
    arguments = _loaded('extra_arg_loader', '-i', in_file)
    assert _run(backend, *arguments) == ExitCode.OK
    assert backend.model is not None
    assert [row.value for row in backend.model.rows] == ['from a file']


def test_class_beside_loader() -> None:
    """Test a class named beside a loader is the class that has to come out."""
    assert _run(Recorder(), *_loaded('extra_arg_loader', '--class',
                                     'ExtraArgCfg')) == ExitCode.OK


def test_wrong_class_refused(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a loader that answers with another class stops the program.

    A loader may choose its class by looking at the file, so `--class` beside
    it is how a script says which class it is prepared to go on with. The check
    is made on the object that is really going to be edited.
    """
    outcome = _run(Recorder(), *_loaded('picking_loader', '--class',
                                        'PickedCfg'))
    assert outcome == ExitCode.WRONG_CLASS
    expected = WRONG_CLASS_MESSAGE.format(name='picking_loader',
                                          other='FlatCfg', wanted='PickedCfg')
    assert expected in capsys.readouterr().err


def test_chosen_class_checked(tmp_path: Path) -> None:
    """Test the class the file selected is the one that `--class` is asked of.

    The loader answers with `FlatCfg` when there is no file, so a check made
    before the load would have refused this run and this file really is the
    other class.
    """
    in_file = _input_file(tmp_path, name=PICKED_NAME, answer=2)
    assert _run(Recorder(), *_loaded('picking_loader', '--class', 'PickedCfg',
                                     '-i', in_file)) == ExitCode.OK


def test_not_a_loader(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a name that cannot be called at all is refused as no loader."""
    outcome = _run(Recorder(), *_loaded('REFUSAL_MESSAGE'))
    assert outcome == ExitCode.NOT_LOADER
    name = 'REFUSAL_MESSAGE'
    expected = NOT_LOADER_MESSAGE.format(module=SAMPLE, name=name)
    assert expected in capsys.readouterr().err


def test_loader_needs_args(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a callable that is not a loader yet says what has to be done.

    A configuration class is exactly that case: it can be called, and it takes
    none of the five keyword arguments that a loader takes. What a command line
    cannot supply has to be bound where the loader is written, and saying so
    plainly is better than a half answer.
    """
    outcome = _run(Recorder(), *_loaded('ExtraArgCfg'))
    assert outcome == ExitCode.LOADER_ARGS
    said = capsys.readouterr().err
    assert LOADER_ARGS_MESSAGE.format(name='ExtraArgCfg') in said
    assert 'TypeError' in said


def test_loader_says_nothing(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a loader that will not answer without a file is refused.

    The program asks a loader for a configuration with no JSON source, which
    is what a loader answers. One that ends the program instead is turned into
    a refusal, because ending it is never this library's answer.
    """
    outcome = _run(Recorder(), *_loaded('exiting_loader'))
    assert outcome == ExitCode.NO_DEFAULTS
    expected = NO_LOADER_CONFIG.format(name='exiting_loader')
    assert expected in capsys.readouterr().err


def test_no_such_loader(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a loader name the module does not hold is refused by name."""
    outcome = _run(Recorder(), *_loaded('no_loader_here'))
    assert outcome == ExitCode.NO_NAME
    expected = NO_NAME_MESSAGE.format(module=SAMPLE, name='no_loader_here')
    assert expected in capsys.readouterr().err


def test_descriptions_door() -> None:
    """Test what an application says about its members reaches the editor.

    It is the one thing this program could not otherwise pass on, because a
    member has no docstring at runtime: what a member is for is in a mapping
    like this one or nowhere at all.
    """
    backend = Recorder()
    assert _run(backend, *_named('FlatCfg', '--descriptions',
                                 'FLAT_DESCRIPTIONS')) == ExitCode.OK
    assert backend.model is not None
    described = {row.name: row.description for row in backend.model.rows}
    assert described == {'name': ABOUT_FLAT_NAME, 'answer': ''}


def test_no_descriptions() -> None:
    """Test a run that names none shows the members without a description."""
    backend = Recorder()
    assert _run(backend, *_named('FlatCfg')) == ExitCode.OK
    assert backend.model is not None
    assert not any(row.description for row in backend.model.rows)


def test_no_such_described(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a name the module does not hold is refused by name."""
    named = _named('FlatCfg', '--descriptions', 'NotThere')
    outcome = _run(Recorder(), *named)
    assert outcome == ExitCode.NO_NAME
    expected = NO_NAME_MESSAGE.format(module=SAMPLE, name='NotThere')
    assert expected in capsys.readouterr().err


def test_not_a_mapping(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a name that is no mapping at all is refused as no mapping.

    What the keys and the values of a mapping are is deliberately not checked:
    a selector that addresses no member is never used, and a wrong description
    is not worth refusing to open an editor over.
    """
    outcome = _run(Recorder(), *_named('FlatCfg', '--descriptions',
                                       'REFUSAL_MESSAGE'))
    assert outcome == ExitCode.NOT_DESCRIPTIONS
    expected = NOT_DESCRIPTIONS.format(module=SAMPLE, name='REFUSAL_MESSAGE')
    assert expected in capsys.readouterr().err


def test_added_file_options() -> None:
    """Test the shared options are the ones every program is given."""
    parser = ArgumentParser(prog=PROGRAM)
    add_file_options(parser)
    parsed = parser.parse_args(['-i', 'in.json', '-o', 'out.json'])
    assert parsed.input == 'in.json'
    assert parsed.output == 'out.json'
    assert named_policy(parsed.policy) is LoadPolicy.STRICT_THEN_DEFAULTS


@pytest.mark.parametrize('name,policy',
                         [('strict', LoadPolicy.STRICT),
                          ('defaults', LoadPolicy.DEFAULTS),
                          ('strict-then-defaults',
                           LoadPolicy.STRICT_THEN_DEFAULTS)])
def test_named_policy(name: str, policy: LoadPolicy) -> None:
    """Test each accepted `--policy` value means what it says."""
    assert named_policy(name) is policy


def test_policy_is_checked() -> None:
    """Test a policy that is not one of them cannot reach the editor."""
    parser = ArgumentParser(prog=PROGRAM)
    add_file_options(parser)
    with pytest.raises(SystemExit):
        parser.parse_args(['--policy', 'whatever'])
