#! /usr/bin/env python3
"""The part of a Tkinter editor that scrolls.

A configuration of any interesting size does not fit a window, and with the
explanations shown it fits one even less. Tk has no scrolling frame, so this
is the one it has: a canvas with a scrollbar beside it and a frame on the
canvas. What goes in the frame scrolls, and everything the editor keeps in
view is packed outside it.

It is a module of its own because none of it is about an edit model: it is
what Tk needs in order to have a scrolling area at all, and the editor uses
it the way it uses the toolkit.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from typing import NamedTuple, Optional
import tkinter

BODY_HEIGHT = 480
"""Largest height in pixels that the scrolling part of the editor is given.

A configuration of any size therefore opens a window that fits a screen, and
what does not fit is scrolled to rather than lost. A configuration smaller
than this gets a window that is smaller than this, because the height is what
the body asks for up to this limit and not this limit.
"""

BODY_WIDTH = 720
"""Width in pixels that the scrolling part of the editor opens at.

A canvas asks for a width of its own that has nothing to do with what is on it,
so the width the editor opens at has to be said, and this is where it is said.

**It is said rather than measured, because the width of the body cannot be
measured.** Every paragraph wraps to the width it is given, so a body that has
been laid out asks for about the width it already has, whatever it would have
liked. Following that answer is what made showing the explanations flicker
between two window sizes for ever: the wrapped paragraph asked for a little
less than it was given, the canvas asked for that, the window narrowed, the
paragraph wrapped into one more line and asked for something else again.
Measured in a window: one toggle cost 19099 resizes of the window in two
seconds and never stopped.

So the width is this, the height is what the body asks for up to a window's
worth, and a user who wants another width resizes the window — after which
every paragraph wraps to what there is. A small configuration therefore opens
in a window no taller than it needs, and this wide whatever it holds.
"""


def _wheel_step(event: 'tkinter.Event[tkinter.Misc]') -> int:
    """Return which way one reported turn of the mouse wheel goes.

    The type of the event is written as text here and in the three callbacks
    around it, because `tkinter.Event` is a generic class to a type checker and
    a plain one at runtime: Python 3.12 and 3.13 evaluate an annotation where
    it is written, and subscripting it there is an error.

    Only the sign of the delta is used. Its size means different things on
    different platforms, and one line per turn is a scroll everyone can
    follow.

    Args:
        event: The wheel event that Tk reported.

    Returns:
        How far to scroll the body, in lines.
    """
    return -1 if event.delta > 0 else 1


def _scroll_by(canvas: tkinter.Canvas, step: Optional[int]
               ) -> Callable[..., str]:
    """Return the callback that one turn of the mouse wheel runs.

    Args:
        canvas: Canvas that holds the scrolling part of the editor.
        step: How far to scroll, or None to read it from the event. X11
            reports a wheel as two buttons and says nothing about how far,
            while every other platform reports a delta whose sign is the
            direction.

    Returns:
        A callback that Tk can bind, which stops the event from being handled
        a second time by whatever else the window is bound to.
    """
    def scroll(*event: 'tkinter.Event[tkinter.Misc]') -> str:
        """Scroll the body by one line, in the direction of the wheel."""
        moved = step if step is not None else _wheel_step(event[0])
        canvas.yview_scroll(moved, 'units')
        return 'break'
    return scroll


def _bind_wheel(window: tkinter.Misc, canvas: tkinter.Canvas) -> None:
    """Let the mouse wheel scroll the body, however it is reported.

    The bindings are made on the window rather than on the canvas, because a
    wheel event goes to the widget under the pointer and the pointer is
    usually over a field or a label inside the body. That is the same window
    the keys are bound on, and it is the same open question for the same
    reason: an editor mounted in a window it shares would be claiming the
    wheel of a whole application. See section 8.2.7 of `doc/design.md`.

    Args:
        window: Window that the bindings are made on.
        canvas: Canvas that holds the scrolling part of the editor.
    """
    for sequence, step in (('<MouseWheel>', None), ('<Button-4>', -1),
                           ('<Button-5>', 1)):
        try:
            window.bind(sequence, _scroll_by(canvas=canvas, step=step))
        except tkinter.TclError:
            # A platform whose Tk does not know one of these sequences leaves
            # the wheel out and keeps the scrollbar, which is not worth an
            # editor that does not open.
            pass


def _fit_body(canvas: tkinter.Canvas,
              body: tkinter.Frame) -> Callable[..., None]:
    """Return the callback that follows the height of the body.

    It is what makes the canvas scroll: a canvas shows the part of its
    contents that its scroll region says is there, and the contents of this
    one grow and shrink as the explanations are shown and hidden. The height
    follows too, up to the height of a window, so that showing the
    explanations makes the window taller while there is room for it.

    **The width is deliberately not followed**, and `BODY_WIDTH` says why it
    cannot be.

    Args:
        canvas: Canvas that holds the body.
        body: Frame that holds everything that scrolls.

    Returns:
        A callback for the event that says the body has been laid out.
    """
    def fitted(*event: 'tkinter.Event[tkinter.Misc]') -> None:
        """Follow the height of the body, up to the height of a window."""
        _ = event
        canvas.configure(scrollregion=canvas.bbox('all'),
                         height=min(body.winfo_reqheight(), BODY_HEIGHT))
    return fitted


def _fit_width(canvas: tkinter.Canvas, item: int) -> Callable[..., None]:
    """Return the callback that gives the body the width of the canvas.

    An item on a canvas is as wide as it asks to be, so without this the
    fields would keep the width they wanted rather than the width there is.

    Args:
        canvas: Canvas that holds the body.
        item: The canvas item that the body was put on.

    Returns:
        A callback for the event that says the canvas has been resized.
    """
    def fitted(event: 'tkinter.Event[tkinter.Misc]') -> None:
        """Make the body as wide as the canvas now is."""
        canvas.itemconfigure(item, width=event.width)
    return fitted


class ScrollingArea(NamedTuple):
    """The part of the editor that scrolls, before it has been placed."""

    area: tkinter.Frame
    """The frame to pack where the scrolling part of the editor belongs."""

    body: tkinter.Frame
    """The frame to build the scrolling part of the editor in."""


def scrolling_body(parent: tkinter.Misc) -> ScrollingArea:
    """Return the frame that the scrolling part of the editor is built in.

    The area is not packed here. Tk gives each child the space it asks for in
    the order they were packed, so the part that does not scroll has to be
    packed before this one to be sure of its space, while this one is created
    first so that the widgets of the editor are created in the order they are
    read in.

    Args:
        parent: Widget that becomes the parent of the created widgets.

    Returns:
        The frame to pack, and the frame to build in.
    """
    area = tkinter.Frame(parent)
    canvas = tkinter.Canvas(area, highlightthickness=0)
    slider = tkinter.Scrollbar(area, orient='vertical', command=canvas.yview)
    canvas.configure(yscrollcommand=slider.set, height=BODY_HEIGHT,
                     width=BODY_WIDTH)
    slider.pack(side='right', fill='y')
    canvas.pack(side='left', fill='both', expand=True)
    body = tkinter.Frame(canvas)
    item = canvas.create_window(0, 0, window=body, anchor='nw')
    body.bind('<Configure>', _fit_body(canvas=canvas, body=body))
    canvas.bind('<Configure>', _fit_width(canvas=canvas, item=item))
    _bind_wheel(window=parent.winfo_toplevel(), canvas=canvas)
    return ScrollingArea(area=area, body=body)
