#! /usr/bin/env python3
"""Fixtures for the tests of the Tkinter backend."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Iterator
import tkinter
import pytest


@pytest.fixture(name='root_or_skip')
def fixture_root_or_skip() -> Iterator[tkinter.Tk]:
    """Yield a withdrawn Tk root, or skip when there is no display.

    This is real Tk, so it catches the places where a stub has drifted from
    what Tk actually does. The window is withdrawn and therefore never
    visible, which keeps the test automatable: it neither disturbs the user
    nor depends on which window has the keyboard focus.

    On a machine without a display the test is skipped rather than failed.
    """
    try:
        window = tkinter.Tk()
    except tkinter.TclError:
        pytest.skip('No display available for Tk.')
    window.withdraw()
    yield window
    window.destroy()
