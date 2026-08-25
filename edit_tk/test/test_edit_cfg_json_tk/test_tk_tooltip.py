#! /usr/bin/env python3
"""Tests for the tooltip that Tk does not have.

Where the editor puts one and what it says there is tested with the controls
that carry one, in `test_tk_finding`. What is here is the tooltip on its own:
what it says about itself, and the three states it has to answer for besides
the one it is made for — a pointer that arrives twice, a callback that Tk ran
without an event, and a pointer that leaves a control it never rested on.

They are asked of the stubs, because a tooltip is put up by a pointer arriving
and Tk reports that only to a window that is on the screen. What real Tk can be
asked without one is that the bindings are really made, and that is the last
test here.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import cast
import tkinter
from edit_cfg_json_tk.tk_tooltip import Tooltip
from .helpers import FakeWidget

TIP_TEXT = 'What this control is for, in a sentence.'
"""What the tooltip of these tests says."""

POINTER_PLACE = (40, 30)
"""Where the pointer is when it arrives, in screen pixels."""


def _pointer() -> 'tkinter.Event[tkinter.Misc]':
    """Return the event that says where the pointer has just arrived."""
    event: 'tkinter.Event[tkinter.Misc]' = tkinter.Event()
    event.x_root, event.y_root = POINTER_PLACE
    return event


def _stub_tips(widget: FakeWidget) -> list[FakeWidget]:
    """Return the stub labels that one stub widget has been given."""
    return [made for made in FakeWidget.created
            if made is not widget and made.options.get('text')]


def _stubbed() -> tuple[FakeWidget, Tooltip]:
    """Return a stub control and the tooltip that was put on it."""
    widget = FakeWidget()
    tooltip = Tooltip(cast(tkinter.Misc, widget), TIP_TEXT)
    return widget, tooltip


def test_says_what_it_holds(stub_tk: None) -> None:
    """Test a tooltip answers with the text it was given.

    The editor reads it back when it puts the same explanation on the control
    and on the tooltip of that control, so the tooltip is the one place the
    text is kept.
    """
    _ = stub_tk
    assert _stubbed()[1].text == TIP_TEXT


def test_stub_arrives_twice(stub_tk: None) -> None:
    """Test a pointer reported as arriving twice puts up one tooltip.

    Tk reports an arrival for a widget and again for what is inside it, so a
    control with anything in it would otherwise end up with a stack of labels
    that only the topmost of them is ever taken away from.
    """
    _ = stub_tk
    widget, _ = _stubbed()
    for _ in range(2):
        widget.bindings['<Enter>'](_pointer())
    assert len(_stub_tips(widget)) == 1


def test_stub_without_event(stub_tk: None) -> None:
    """Test a callback run without an event puts nothing up.

    There is then nothing that says where the pointer is, and a tooltip in the
    corner of a window says nothing about which control it belongs to.
    """
    _ = stub_tk
    widget, _ = _stubbed()
    widget.bindings['<Enter>']()
    assert not _stub_tips(widget)


def test_stub_leaving_first(stub_tk: None) -> None:
    """Test leaving a control the pointer never rested on takes nothing away.

    Tk reports a departure for a widget the pointer only crossed, and there is
    then no label to destroy.
    """
    _ = stub_tk
    widget, _ = _stubbed()
    widget.bindings['<Leave>']()
    assert not _stub_tips(widget)
    widget.bindings['<Enter>'](_pointer())
    assert len(_stub_tips(widget)) == 1


def test_real_bindings_made(root_or_skip: tkinter.Tk) -> None:
    """Test a real Tk control is given the two bindings a tooltip needs.

    That is as far as real Tk can be asked here: a pointer arriving is
    reported only to a window that is on the screen, and these tests run on a
    withdrawn one so that they neither disturb the user nor depend on which
    window has the keyboard focus. What the tooltip then does is the stubbed
    tests above.
    """
    widget = tkinter.Label(root_or_skip, text='c')
    tooltip = Tooltip(widget, TIP_TEXT)
    assert tooltip.text == TIP_TEXT
    assert widget.bind('<Enter>')
    assert widget.bind('<Leave>')
