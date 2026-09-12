#! /usr/bin/env python3
"""Tests for the scrolling part of the editor, asked without an edit model.

What the editor does with it is tested with the window, in `test_tk_looks` and
`test_tk_finding`. What is here is the part of it that a window cannot be asked
about: which way one reported turn of the wheel goes, since the size of the
delta means different things on different platforms and only its sign is used,
how far one reported movement of a touchpad goes, since that one reports both
directions packed into a single number, and what bringing a widget into view
does with a body that has not been laid out yet.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import cast
import tkinter
import pytest
from edit_cfg_json_tk.scrolling import bring_into_view, scrolling_body
from edit_cfg_json_tk.tk_scope import KeyScope
from .helpers import touchpad_known
from .stubs import FakeWidget, STUB_BODY_HEIGHT, TOUCHPAD

WHEEL_UP = -1
"""How far the body scrolls for one turn of the wheel away from the user."""

WHEEL_DOWN = 1
"""How far it scrolls for one turn towards the user."""

OFF_THE_WINDOW = (0.5, 0.6)
"""A view showing a part of the body that the widget looked for is not in."""

HALF_SCROLLED = (0.4, 0.5)
"""A view of the middle of the body, which one gesture moves away from."""

TOUCH_PIXELS = 30
"""How far one reported movement of a touchpad went, in pixels."""

TALL_LINES = 60
"""Height in lines of a label that is taller than a window of the body."""


def _scroll_event(delta: int) -> 'tkinter.Event[tkinter.Misc]':
    """Return the event that reports one movement of a wheel or a touchpad.

    Args:
        delta: What the platform reported. A wheel says only which way it
            turned by the sign of this, and a touchpad packs how far it went
            in both directions into it.

    Returns:
        The scrolling event, as Tk hands one to a binding.
    """
    event: 'tkinter.Event[tkinter.Misc]' = tkinter.Event()
    event.delta = delta
    return event


def _packed(sideways: int, upright: int) -> int:
    """Return the two directions of a touchpad as Tk packs them into one.

    Args:
        sideways: Pixels the gesture went sideways, which is the high half of
            the number that the event carries.
        upright: Pixels it went up or down, which is the low half of it as a
            signed 16 bit number.

    Returns:
        What the delta of a touchpad event holds.
    """
    return (sideways << 16) | (upright & 0xffff)


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
    FakeWidget.tag_bindings[scope.tag]['<MouseWheel>'](_scroll_event(delta))
    canvas = cast(FakeWidget, area.canvas)
    assert canvas.scrolled == moved


@pytest.mark.parametrize('sideways', [0, 99, -99])
@pytest.mark.parametrize('upright, moved', [(TOUCH_PIXELS, -TOUCH_PIXELS),
                                            (-TOUCH_PIXELS, TOUCH_PIXELS)])
def test_touchpad_pixels(stub_tk: None, sideways: int, upright: int,
                         moved: int) -> None:
    """Test a gesture scrolls the pixels it reported, and only up and down.

    A touchpad reports how far it went in both directions at once, and the
    body does not scroll sideways, so whatever the sideways half of the
    report holds must make no difference to where the view ends up. A canvas
    scrolls in nothing smaller than a tenth of its height, so the pixels are
    the fraction of the body that they are and the view is moved by that.

    Args:
        stub_tk: The fixture that replaces the Tkinter widget classes.
        sideways: What the sideways half of the report holds.
        upright: What its up and down half holds.
        moved: How far the body is then scrolled, in pixels.
    """
    _ = stub_tk
    parent, scope = _stub_area()
    area = scrolling_body(cast(tkinter.Misc, parent), scope)
    scope.reach()
    canvas = cast(FakeWidget, area.canvas)
    canvas.view = HALF_SCROLLED
    binding = FakeWidget.tag_bindings[scope.tag][TOUCHPAD]
    binding(_scroll_event(_packed(sideways, upright)))
    expected = HALF_SCROLLED[0] + moved / STUB_BODY_HEIGHT
    assert canvas.moved == [pytest.approx(expected)]


def test_touchpad_no_body(stub_tk: None,
                          monkeypatch: pytest.MonkeyPatch) -> None:
    """Test nothing is scrolled while the canvas has nothing to measure.

    Real Tk answers with no area at all for a canvas that nothing has been
    put on yet, and no height is no fraction of a gesture to scroll by.

    Args:
        stub_tk: The fixture that replaces the Tkinter widget classes.
        monkeypatch: The fixture that makes the canvas answer with no area.
    """
    _ = stub_tk
    parent, scope = _stub_area()
    area = scrolling_body(cast(tkinter.Misc, parent), scope)
    scope.reach()
    canvas = cast(FakeWidget, area.canvas)
    monkeypatch.setattr(canvas, 'bbox', lambda *what: None)
    binding = FakeWidget.tag_bindings[scope.tag][TOUCHPAD]
    binding(_scroll_event(_packed(0, TOUCH_PIXELS)))
    assert canvas.moved == []


def test_real_touchpad(root_or_skip: tkinter.Tk) -> None:
    """Test a gesture over the content of the body scrolls it in real Tk.

    This is the whole point of binding the event, and a stub cannot show it:
    what a touchpad reports goes to the widget under the pointer, which is a
    label inside the body rather than the canvas under it, and the binding
    has to reach that label to scroll anything.

    Tk 8 has no such event, and is asked about before anything is built:
    there is nothing to bind and nothing to generate there, and a window laid
    out for a test that cannot run is a window that can go wrong for nothing.

    Only the layout is waited for, and never the whole event loop. Tk lays a
    widget out when it next has nothing else to do, which is what makes the
    label a size and the body a height, and an event that is generated is
    handled as it is generated rather than queued.

    Args:
        root_or_skip: The fixture that yields a real withdrawn Tk window.
    """
    if not touchpad_known(root_or_skip):
        pytest.skip('This Tk does not report a touchpad.')
    scope = KeyScope(root_or_skip)
    area = scrolling_body(root_or_skip, scope)
    label = tkinter.Label(area.body, text='content', height=TALL_LINES)
    label.pack()
    scope.reach()
    root_or_skip.update_idletasks()
    label.event_generate(TOUCHPAD, delta=_packed(0, -TOUCH_PIXELS))
    assert area.canvas.yview()[0] > 0.0


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
