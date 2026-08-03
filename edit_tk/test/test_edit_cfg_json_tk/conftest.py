#! /usr/bin/env python3
"""Fixtures for the tests of the Tkinter backend."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Iterator
import tkinter
import pytest
from .helpers import FakeVar, FakeWidget


@pytest.fixture(name='stub_tk')
def fixture_stub_tk(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Replace the Tkinter widget and variable classes with stubs.

    It lives here rather than in `helpers`, because a fixture is found by the
    tests of a package through its `conftest`, and the four test modules of
    this backend all want this one.
    """
    FakeWidget.created.clear()
    FakeVar.created.clear()
    for widget_name in ('Frame', 'Label', 'Button', 'Entry'):
        monkeypatch.setattr(tkinter, widget_name, FakeWidget)
    monkeypatch.setattr(tkinter, 'StringVar', FakeVar)
    yield
    FakeWidget.created.clear()
    FakeVar.created.clear()


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
