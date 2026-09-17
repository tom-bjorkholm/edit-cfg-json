#! /usr/bin/env python3
"""Tests for what waits until the editor is really on the screen.

Tk drops a request for the keyboard focus while the widget or an ancestor of
it is not mapped, and refuses a grab for a window that is not viewable, so the
editor asks for both when its window has been shown. What that costs is one
binding and one rule, and the rule is that it happens once however often a
window is hidden and shown again.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import cast
import tkinter
from edit_cfg_json_tk.showing import when_shown
from .stubs import FakeWidget


def test_stub_waits_for_map(stub_tk: None) -> None:
    """Test nothing is done until Tk says the widget is on the screen.

    Args:
        stub_tk: The fixture that replaces the Tkinter widget classes.
    """
    _ = stub_tk
    widget = FakeWidget()
    done: list[str] = []
    when_shown(cast(tkinter.Misc, widget), lambda: done.append('shown'))
    assert not done
    widget.bindings['<Map>']()
    assert done == ['shown']


def test_stub_shown_once(stub_tk: None) -> None:
    """Test a window shown a second time does not do it a second time.

    What waits here gives the keyboard focus to the first value of the
    editor, and an editor that took the focus back every time its window came
    up would take it from wherever the user had put it since.

    It has no companion in real Tk, because a window that can be mapped twice
    in a test is a window on the screen, and the map of one that is withdrawn
    cannot be generated.

    Args:
        stub_tk: The fixture that replaces the Tkinter widget classes.
    """
    _ = stub_tk
    widget = FakeWidget()
    done: list[str] = []
    when_shown(cast(tkinter.Misc, widget), lambda: done.append('shown'))
    widget.bindings['<Map>']()
    widget.bindings['<Map>']()
    assert done == ['shown']


def test_real_binding_added(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk takes the binding, and takes a second one beside it.

    A withdrawn window is never mapped, and Tk delivers no map event to a
    window that is not viewable however one is generated, so what a test
    without a display can ask is that Tk accepts the sequence — it answers
    with the script it bound, and with nothing at all for a sequence nobody
    bound — and that waiting for the same widget twice leaves both of them
    bound, which makes that script longer. The editor waits for
    its window twice: the grab of a modal session waits for it and so does the
    focus of its first value, and a second binding that replaced the first
    would cost it one of the two. That either of them then runs is the
    `focus_sensitive` test in `test_tk_looks`.

    Args:
        root_or_skip: The fixture that yields a real withdrawn Tk window.
    """
    frame = tkinter.Frame(root_or_skip)
    frame.pack()
    when_shown(frame, lambda: None)
    alone = frame.bind('<Map>')
    when_shown(frame, lambda: None)
    assert alone
    assert len(frame.bind('<Map>')) > len(alone)
