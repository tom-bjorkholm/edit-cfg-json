#! /usr/bin/env python3
"""Tests that each of the three packages ships the program it promises.

The three programs differ in one thing, which is the backend, so what they are
is one table and not three test modules. Written per package these tests were
near copies of each other, and pylint said so: three copies of one shape would
have been free to drift apart, and a table cannot.

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
from typing import NamedTuple
import importlib
import os
import subprocess
import sys
import pytest
from edit_cfg_json import ExitCode

MISSING_MODULE = 'no_such_module_here'
"""A module that is not installed, so a program refuses before it opens."""


class ProgramSpec(NamedTuple):
    """What one of the three programs of this repository is."""

    package: str
    """Import name of the package that ships it, and its `python -m` name."""

    program: str
    """Name it is installed under, which is what its own help text says."""

    backend: str
    """Class name of the backend it hands over."""

    interactive: bool
    """Whether its backend gives the user a session to press Save in."""


PROGRAMS = (ProgramSpec(package='edit_cfg_json', program='edit-cfg-json',
                        backend='DumpEditor', interactive=False),
            ProgramSpec(package='edit_cfg_json_tk', program='edit-cfg-json-tk',
                        backend='TkEditor', interactive=True),
            ProgramSpec(package='edit_cfg_json_textual',
                        program='edit-cfg-json-textual',
                        backend='TextualEditor', interactive=True))
"""Every program this repository installs, and what each of them is."""

PROGRAM_IDS = tuple(spec.package for spec in PROGRAMS)
"""Names of the parametrized cases, so a failure says which program it was."""


def _entry_point(spec: ProgramSpec) -> ModuleType:
    """Return the module that is the program of one package.

    Args:
        spec: The program to reach.

    Returns:
        The `__main__` module of that package, imported.
    """
    return importlib.import_module(f'{spec.package}.__main__')


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
    return subprocess.run([sys.executable, '-m', spec.package, *args],
                          check=False, capture_output=True, text=True,
                          env=environment)


@pytest.mark.parametrize('spec', PROGRAMS, ids=PROGRAM_IDS)
def test_supplies_own_backend(spec: ProgramSpec,
                              monkeypatch: pytest.MonkeyPatch) -> None:
    """Test each program hands over its own backend and says who it is.

    The backend is the one thing the shared command line cannot supply, so it
    is the one thing each program has to get right. A program whose backend
    gives the user no session says so as well, because that is what decides
    whether it offers `--save` and what its exit code answers.
    """
    entry_point = _entry_point(spec)
    given: dict[str, object] = {}

    def fake_run_cli(backend: object, prog: str, *, args: object,
                     interactive: bool = True) -> int:
        """Record what the program asked for instead of running it."""
        given.update(backend=backend, prog=prog, args=args,
                     interactive=interactive)
        return ExitCode.OK
    monkeypatch.setattr(entry_point, 'run_cli', fake_run_cli)
    command = ['--module', MISSING_MODULE, '--class', 'Cfg']
    assert entry_point.main(command) is ExitCode.OK
    assert type(given['backend']).__name__ == spec.backend
    assert given['prog'] == spec.program
    assert given['interactive'] is spec.interactive


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
