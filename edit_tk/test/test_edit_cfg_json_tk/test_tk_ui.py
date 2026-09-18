#! /usr/bin/env python3
"""Tests for what this package registers about itself.

**No Tk is built in this process by any test here**, which is the point of
asking in a process of its own: a Tk that a test built and destroyed would be
the first of two in the process that goes on to open a real editor, and that
is what has crashed Tk in this repository before. The one test that lets the
child process run really asks the machine, so it asserts only that an answer
came back; the rest replace the child with a recorded result and say what is
made of one.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
import subprocess
import pytest
from edit_cfg_json import DUMP_UI, UiBackend, discovered_uis
from edit_cfg_json_tk import TK_UI, TkEditor, tk_can_run
from edit_cfg_json_tk.tk_ui import HOME_SETTINGS, PROBE


def answered(monkeypatch: pytest.MonkeyPatch,
             code: Optional[int]) -> list[list[str]]:
    """Make the child process answer with one exit code, without running.

    The cached answer of a previous question is cleared as well, because the
    real one may already have been asked in this process.

    Args:
        monkeypatch: What the replacement is undone by.
        code: What the child is to exit with, or None for a child that cannot
            be started at all.

    Returns:
        The command lines that the probe asked to be run.
    """
    asked: list[list[str]] = []

    def fake_run(command: list[str], **named: object
                 ) -> subprocess.CompletedProcess[bytes]:
        """Record the command and answer with the wanted exit code."""
        _ = named
        asked.append(command)
        if code is None:
            raise OSError('no process here')
        return subprocess.CompletedProcess(args=command, returncode=code)
    tk_can_run.cache_clear()
    monkeypatch.setattr(subprocess, 'run', fake_run)
    return asked


def test_registration() -> None:
    """Test this package registers the window editor as the best one.

    The priority is the answer to which editor a machine that can run both of
    them is given, and a window is what a user of such a machine expects.
    """
    assert TK_UI.ui_name == 'tk'
    assert TK_UI.priority > DUMP_UI.priority
    assert isinstance(TK_UI.backend(), TkEditor)
    assert TK_UI.interactive
    assert TK_UI.home_settings == HOME_SETTINGS


def test_registration_found() -> None:
    """Test the registration is reached through the entry point group.

    Naming it in `pyproject.toml` is what makes this package discoverable at
    all, and a program that chooses an editor finds it that way and no other.
    """
    found = [one for one in discovered_uis() if one.ui_name == 'tk']
    assert found == [TK_UI]
    assert isinstance(TK_UI, UiBackend)


def test_home_settings_named() -> None:
    """Test the settings file is the one named after the program.

    It belongs to the user interface rather than to the program, so a session
    that the launcher opens in this editor reads the same file as the program
    of this package does.
    """
    assert HOME_SETTINGS == '.edit-cfg-json-tk.cfg'


def test_probe_builds_a_tk() -> None:
    """Test what the child process runs is a Tk that is thrown away.

    Building it is what asks the question, because that is what connects to
    the display. Destroying it is what keeps the child from drawing anything:
    a window is mapped when the event loop runs, and the child never gets
    there.
    """
    assert 'tkinter.Tk()' in PROBE
    assert '.destroy()' in PROBE
    assert 'mainloop' not in PROBE


def test_asks_a_child_process(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the question is put to a Python of its own and not to this one."""
    asked = answered(monkeypatch, code=0)
    assert tk_can_run()
    assert len(asked) == 1
    assert asked[0][1:] == ['-c', PROBE]


@pytest.mark.parametrize('code, expected', [(0, True), (1, False),
                                            (2, False)])
def test_answer_is_the_code(monkeypatch: pytest.MonkeyPatch, code: int,
                            expected: bool) -> None:
    """Test a child that failed means that there is no display here."""
    answered(monkeypatch, code=code)
    assert tk_can_run() is expected


def test_no_child_is_no(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a child that cannot be started at all is answered and not raised.

    A program that cannot start a process of its own has bigger problems than
    this one, and the answer it needs here is still an answer: this editor
    cannot be opened, so another one is tried.
    """
    answered(monkeypatch, code=None)
    assert not tk_can_run()


def test_answer_is_remembered(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the child is started once however often the question is put.

    Asking is starting a Python, and the display of a machine does not appear
    while one program runs, so a program that asks every installed user
    interface pays for this once.
    """
    asked = answered(monkeypatch, code=0)
    assert tk_can_run()
    assert tk_can_run()
    assert len(asked) == 1


def test_real_answer() -> None:
    """Test asking the machine itself answers with yes or no and not a crash.

    This is the one test that lets the child process run, so it is also the
    one that says the probe is a command a Python can really execute. What
    the answer is depends on the machine, so it is not asserted.
    """
    tk_can_run.cache_clear()
    assert tk_can_run() in (True, False)
    tk_can_run.cache_clear()
