#! /usr/bin/env python3
"""Tests that each of the three packages ships the program it promises.

The three programs differ in the backend and in how they are reached, and
everything else about them is one command line, so what they are is one table
and not three test modules. Written per package these tests were near copies
of each other, and pylint said so: three copies of one shape would have been
free to drift apart, and a table cannot.

They live in the core's test folder for the same reason the layering tests do.
The backends may not import each other, so a shape they share cannot live in
either of them, and the core is where anything about all three belongs.

Nothing here opens a window or a screen. The in-process test replaces the call
that would run the backend, and the subprocess tests are refusals and help
text, both of which happen before there is anything to show.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from types import ModuleType
from typing import NamedTuple, Optional
import importlib.util
import os
import subprocess
import sys
import pytest
from edit_cfg_json import ExitCode

MISSING_MODULE = 'no_such_module_here'
"""A module that is not installed, so a program refuses before it opens."""

NO_HOME = 'no_such_home_folder_here'
"""Folder the subprocess tests use as a home folder with nothing in it.

A program reads its own settings from the home folder before it does anything
the command line asked for, so a test that ran with the home folder of whoever
is running it would pass or fail according to what that person had configured.
"""


class ProgramSpec(NamedTuple):
    """What one of the three programs of this repository is."""

    run_module: str
    """What `python -m` is given to run it."""

    main_module: str
    """Module that holds its `main`, which is `__main__` where there is one."""

    program: str
    """How it is run, which is what its own help text says."""

    backend: str
    """Class name of the backend it hands over."""

    interactive: bool
    """Whether its backend gives the user a session to press Save in."""

    home_settings: Optional[str]
    """Name of its own settings file in the home folder, or None for none."""


PROGRAMS = (ProgramSpec(run_module='edit_cfg_json.dump',
                        main_module='edit_cfg_json.dump',
                        program='python3 -m edit_cfg_json.dump',
                        backend='DumpEditor', interactive=False,
                        home_settings=None),
            ProgramSpec(run_module='edit_cfg_json_tk',
                        main_module='edit_cfg_json_tk.__main__',
                        program='edit-cfg-json-tk', backend='TkEditor',
                        interactive=True,
                        home_settings='.edit-cfg-json-tk.cfg'),
            ProgramSpec(run_module='edit_cfg_json_textual',
                        main_module='edit_cfg_json_textual.__main__',
                        program='edit-cfg-json-textual',
                        backend='TextualEditor', interactive=True,
                        home_settings='.edit-cfg-json-textual.cfg'))
"""Every program this repository ships, and what each of them is.

The two editors are installed under the names their help text says and are
reachable with `python -m` as well. The checker is reachable only that way: it
is no editor, so the name `edit-cfg-json` would promise what it cannot give.

Only the two editors have a settings file of their own in the home folder. What
the two of them differ about is their keys and their questions, and a backend
that prints once and returns has neither, so it reads the shared file or
nothing.
"""

PROGRAM_IDS = tuple(spec.run_module for spec in PROGRAMS)
"""Names of the parametrized cases, so a failure says which program it was."""


def _entry_point(spec: ProgramSpec) -> ModuleType:
    """Return the module that is the program of one package.

    Args:
        spec: The program to reach.

    Returns:
        The module that holds its `main`, imported.
    """
    return importlib.import_module(spec.main_module)


def _module_run(spec: ProgramSpec, *args: str) -> subprocess.CompletedProcess[
        str]:
    """Run one program with `python -m` in a process of its own.

    The test package is put on the path of that process, because a
    configuration class that a program is asked for lives in it.

    Args:
        spec: The program to run.
        args: The command line, without the program name.

    Returns:
        What that process did.
    """
    environment = dict(os.environ)
    environment['PYTHONPATH'] = str(Path(__file__).resolve().parents[1])
    environment.pop('CFG_EDIT_CFG_JSON', None)
    for name in ('HOME', 'USERPROFILE'):
        environment[name] = str(Path(sys.executable).parent / NO_HOME)
    return subprocess.run([sys.executable, '-m', spec.run_module, *args],
                          check=False, capture_output=True, text=True,
                          env=environment)


@pytest.mark.parametrize('spec', PROGRAMS, ids=PROGRAM_IDS)
def test_supplies_own_backend(spec: ProgramSpec,
                              monkeypatch: pytest.MonkeyPatch) -> None:
    """Test each program hands over its own backend and says who it is.

    The backend is the one thing the shared command line cannot supply, so it
    is the one thing each program has to get right. A program whose backend
    gives the user no session says so as well, because that is what decides
    whether it offers `--save` and what its exit code answers, and so is the
    name of its own settings file, which is the other thing the shared command
    line cannot know.
    """
    entry_point = _entry_point(spec)
    given: dict[str, object] = {}

    def fake_run_cli(backend: object, prog: str, *, args: object,
                     interactive: bool = True,
                     home_settings: Optional[str] = None) -> int:
        """Record what the program asked for instead of running it."""
        given.update(backend=backend, prog=prog, args=args,
                     interactive=interactive, home_settings=home_settings)
        return ExitCode.OK
    monkeypatch.setattr(entry_point, 'run_cli', fake_run_cli)
    command = ['--module', MISSING_MODULE, '--class', 'Cfg']
    assert entry_point.main(command) is ExitCode.OK
    assert type(given['backend']).__name__ == spec.backend
    assert given['prog'] == spec.program
    assert given['interactive'] is spec.interactive
    assert given['home_settings'] == spec.home_settings


@pytest.mark.parametrize('spec', PROGRAMS, ids=PROGRAM_IDS)
def test_home_settings_name(spec: ProgramSpec) -> None:
    """Test each program's own settings file is named after the program.

    The readme of each package writes that name from its distribution name,
    which is what `{{home_settings}}` expands to, so a program whose file was
    called something else would be documented as reading a file it does not.
    """
    expected = f'.{spec.program}.cfg' if spec.interactive else None
    assert spec.home_settings == expected


def test_no_misleading_name() -> None:
    """Test the core package runs nothing under the name of an editor.

    `python3 -m edit_cfg_json` printed the configuration and returned, which
    is the one thing a name must not do: it promises the editor this library
    is for, and what it gave was a printout. There is no `__main__` in the
    core at all now, so the utility is reached by naming it.
    """
    assert importlib.util.find_spec('edit_cfg_json.__main__') is None


@pytest.mark.parametrize('spec', PROGRAMS, ids=PROGRAM_IDS)
def test_module_run_refuses(spec: ProgramSpec) -> None:
    """Test `python -m` on each package really runs that program.

    A module that is not installed is refused before anything is shown, so
    this needs no display, and the exit code says the refusal survived being a
    real process rather than a returned number.
    """
    done = _module_run(spec, '--module', MISSING_MODULE, '--class', 'Cfg')
    assert done.returncode == ExitCode.NO_MODULE
    assert MISSING_MODULE in done.stderr


@pytest.mark.parametrize('spec', PROGRAMS, ids=PROGRAM_IDS)
def test_help_names_program(spec: ProgramSpec) -> None:
    """Test each program's help text names the program it is installed as."""
    done = _module_run(spec, '--help')
    assert done.returncode == ExitCode.OK
    assert f'usage: {spec.program}' in done.stdout


@pytest.mark.parametrize('spec', PROGRAMS, ids=PROGRAM_IDS)
def test_save_only_no_user(spec: ProgramSpec) -> None:
    """Test `--save` exists exactly where the user has no Save to press.

    It is `argparse` that refuses it where it does not belong, because the
    option is not added at all, which is better than an option that exists and
    then says it means nothing here.
    """
    done = _module_run(spec, '--save', '--module', MISSING_MODULE, '--class',
                       'Cfg')
    expected = ExitCode.USAGE if spec.interactive else ExitCode.NO_MODULE
    assert done.returncode == expected
    if spec.interactive:
        assert '--save' in done.stderr


@pytest.mark.parametrize('spec', PROGRAMS, ids=PROGRAM_IDS)
def test_settings_named_file(spec: ProgramSpec, tmp_path: Path) -> None:
    """Test every program refuses a settings file that was named and is not.

    It is refused before the class is looked for, because the settings are what
    the whole run behaves according to, and running with other settings than
    the ones that were asked for is the one thing a lookup must not do quietly.
    All three programs read one, which is why this is in the table.
    """
    missing = tmp_path / 'no_settings_here.cfg'
    done = _module_run(spec, '-c', str(missing), '--module', MISSING_MODULE,
                       '--class', 'Cfg')
    assert done.returncode == ExitCode.NO_SETTINGS
    assert str(missing) in done.stderr
