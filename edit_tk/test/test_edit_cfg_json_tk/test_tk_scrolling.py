#! /usr/bin/env python3
"""Tests for the scrolling part of the editor, asked without an edit model.

What the editor does with it is tested with the window, in `test_tk_looks` and
`test_tk_finding`. What is here is the part of it that a window cannot be asked
about: which way one reported turn of the wheel goes, since the size of the
delta means different things on different platforms and only its sign is used,
and what bringing a widget into view does with a body that has not been laid
out yet.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import cast
import tkinter
import pytest
from edit_cfg_json_tk.scrolling import bring_into_view, scrolling_body
from edit_cfg_json_tk.tk_scope import KeyScope
from .helpers import FakeWidget

WHEEL_UP = -1
"""How far the body scrolls for one turn of the wheel away from the user."""

WHEEL_DOWN = 1
"""How far it scrolls for one turn towards the user."""

OFF_THE_WINDOW = (0.5, 0.6)
"""A view showing a part of the body that the widget looked for is not in."""


def _wheel_event(delta: int) -> 'tkinter.Event[tkinter.Misc]':
    """Return the event that reports one turn of the wheel.

    Args:
        delta: What the platform reported, whose sign is the direction.

    Returns:
        The wheel event, as Tk hands one to a binding.
    """
    event: 'tkinter.Event[tkinter.Misc]' = tkinter.Event()
    event.delta = delta
    return event


def _stub_area() -> tuple[FakeWidget, KeyScope]:
    """Return a stub parent and the scope that its scrolling part binds in."""
    parent = FakeWidget()
    return parent, KeyScope(cast(tkinter.Misc, parent))


@pytest.mark.parametrize('delta, moved', [(120, WHEEL_UP), (-120, WHEEL_DOWN),
                                          (1, WHEEL_UP), (-1, WHEEL_DOWN)])
def test_wheel_delta_sign(stub_tk: None, delta: int, moved: int) -> None:
    """Test one turn of the wheel scrolls one line, whichever way it turned.

    The size of the delta means different things on different platforms, so
    only its sign is read and one line per turn is a scroll everyone can
    follow.

    Args:
        stub_tk: The fixture that replaces the Tkinter widget classes.
        delta: What the platform reported for one turn.
        moved: How far the body is then scrolled.
    """
    _ = stub_tk
    parent, scope = _stub_area()
    area = scrolling_body(cast(tkinter.Misc, parent), scope)
    scope.reach()
    FakeWidget.tag_bindings[scope.tag]['<MouseWheel>'](_wheel_event(delta))
    canvas = cast(FakeWidget, area.canvas)
    assert canvas.scrolled == moved


def test_body_not_laid_out(stub_tk: None,
                           monkeypatch: pytest.MonkeyPatch) -> None:
    """Test nothing is scrolled while the body has no height to divide by.

    Where a widget is is asked for as a fraction of the height of the body, so
    a body that has not been laid out at all has no fraction to answer with.
    The layout is asked for first, and this is what is left if it gave nothing.
    """
    _ = stub_tk
    parent, scope = _stub_area()
    area = scrolling_body(cast(tkinter.Misc, parent), scope)
    canvas = cast(FakeWidget, area.canvas)
    canvas.view = OFF_THE_WINDOW
    monkeypatch.setattr(area.body, 'winfo_reqheight', lambda: 0)
    bring_into_view(area, area.body)
    assert canvas.moved == []


def test_real_body_scrolls(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk answers with a height, so the fraction can be worked out.

    An empty frame asks for a height of one pixel and never for none, which is
    what makes the guard above a guard rather than an ordinary case.
    """
    scope = KeyScope(root_or_skip)
    area = scrolling_body(root_or_skip, scope)
    root_or_skip.update_idletasks()
    assert area.body.winfo_reqheight() > 0
    bring_into_view(area, area.body)
    assert area.canvas.yview() == (0.0, 1.0)
