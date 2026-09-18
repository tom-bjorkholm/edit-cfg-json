#! /usr/bin/env python3
"""Tests for what this package registers about itself.

Nothing here starts a screen. What this package answers about being able to
run is a question about the two ends of the process, and the tests replace
those with something that says it is a terminal or says it is not.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
import pytest
from edit_cfg_json import DUMP_UI, UiBackend, discovered_uis
from edit_cfg_json_textual import TEXTUAL_UI, TextualEditor, textual_can_run
from edit_cfg_json_textual.textual_ui import HOME_SETTINGS


class _Stream:  # pylint: disable=too-few-public-methods
    """One end of a process that says whether it is a terminal."""

    def __init__(self, terminal: bool) -> None:
        """Say what this end is to answer.

        Args:
            terminal: What it answers about being a terminal.
        """
        self._terminal = terminal

    def isatty(self) -> bool:
        """Return whether this end of the process is a terminal."""
        return self._terminal


def ends(monkeypatch: pytest.MonkeyPatch, stdin: bool, stdout: bool) -> None:
    """Make the two ends of this process answer what a test wants.

    Args:
        monkeypatch: What the replacement is undone by.
        stdin: Whether the input end says it is a terminal.
        stdout: Whether the output end says it is one.
    """
    monkeypatch.setattr(sys, 'stdin', _Stream(stdin))
    monkeypatch.setattr(sys, 'stdout', _Stream(stdout))


def test_registration() -> None:
    """Test this package registers the terminal editor below the window one.

    A machine with a display and a terminal has both, and the window is what
    a user of such a machine expects to be given. This is above what is not
    an editor at all, because it is the editor of every machine with no
    display.
    """
    assert TEXTUAL_UI.ui_name == 'textual'
    assert TEXTUAL_UI.priority > DUMP_UI.priority
    assert isinstance(TEXTUAL_UI.backend(), TextualEditor)
    assert TEXTUAL_UI.interactive
    assert TEXTUAL_UI.home_settings == HOME_SETTINGS


def test_registration_found() -> None:
    """Test the registration is reached through the entry point group.

    Naming it in `pyproject.toml` is what makes this package discoverable at
    all, and a program that chooses an editor finds it that way and no other.
    """
    found = [one for one in discovered_uis() if one.ui_name == 'textual']
    assert found == [TEXTUAL_UI]
    assert isinstance(TEXTUAL_UI, UiBackend)


def test_home_settings_named() -> None:
    """Test the settings file is the one named after the program.

    It belongs to the user interface rather than to the program, so a session
    that the launcher opens in this editor reads the same file as the program
    of this package does.
    """
    assert HOME_SETTINGS == '.edit-cfg-json-textual.cfg'


def test_needs_a_terminal(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test this editor says it can run where both ends are a terminal."""
    ends(monkeypatch, stdin=True, stdout=True)
    assert textual_can_run()


@pytest.mark.parametrize('stdin, stdout', [(True, False), (False, True),
                                           (False, False)])
def test_redirected_is_no(monkeypatch: pytest.MonkeyPatch, stdin: bool,
                          stdout: bool) -> None:
    """Test a run whose input or output is not a terminal cannot show one.

    A screen that is drawn on one end and typed into at the other needs both,
    which is what a shell pipeline, a build job and a test suite with its
    output captured all lack.
    """
    ends(monkeypatch, stdin=stdin, stdout=stdout)
    assert not textual_can_run()


def test_not_remembered(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the answer is worked out again every time it is wanted.

    Asking costs nothing and touches nothing, unlike the display of a
    window, so a process whose output was redirected halfway through its own
    run gets the answer that is true now.
    """
    ends(monkeypatch, stdin=True, stdout=True)
    assert textual_can_run()
    ends(monkeypatch, stdin=True, stdout=False)
    assert not textual_can_run()
