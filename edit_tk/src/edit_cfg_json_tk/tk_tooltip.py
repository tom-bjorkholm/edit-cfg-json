#! /usr/bin/env python3
"""The tooltip that Tk does not have, for a control too small to label.

Every control of this editor says what it does in the word on it, with one
exception: the four that say where a search looks are ticked and unticked
often enough to be worth a line of their own, and a line of their own is width
that the values would lose. So they carry a label of one or two characters and
say the rest here.

Tk has no tooltip. There is no widget for one and no option on a widget that
asks for one, so this is what it amounts to: a borderless window with a label
on it, put beside the pointer while the pointer rests on the control and taken
away again when it leaves. It is a module of its own for the same reason as the
scrolling beside it — none of it is about an edit model, and it is what Tk
needs in order to have a tooltip at all.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from typing import Optional
import tkinter

TOOLTIP_BACKGROUND = '#ffffe0'
"""Background of a tooltip, which is the pale yellow every toolkit uses."""

TOOLTIP_BORDER = '#9aa5b1'
"""Colour of the line around a tooltip, as around an edit field."""

TOOLTIP_OFFSET = (12, 20)
"""How far from the pointer, in pixels across and down, a tooltip is put.

Down rather than up, and to the right rather than the left, so that the
tooltip does not land under the pointer itself: a window that appeared where
the pointer is would take the leave event that closes it again.
"""

TOOLTIP_PADDING = 4
"""Padding in pixels between the text of a tooltip and its border."""


class Tooltip:  # pylint: disable=too-few-public-methods
    """One text that appears while the pointer rests on one widget.

    The window is made when the pointer arrives and destroyed when it leaves,
    rather than made once and hidden, because a tooltip is seen for a second or
    two in a session and a window that is never shown is a window that can
    still be left behind by an editor that was closed.
    """

    def __init__(self, widget: tkinter.Misc, text: str) -> None:
        """Say what one widget tells the pointer that rests on it.

        Args:
            widget: Widget that the pointer rests on.
            text: What that widget says about itself.
        """
        self._widget = widget
        self._text = text
        self._window: Optional[tkinter.Toplevel] = None
        widget.bind('<Enter>', self._shower())
        widget.bind('<Leave>', self._hider())

    @property
    def text(self) -> str:
        """Return what this widget says about itself."""
        return self._text

    def _shower(self) -> Callable[..., None]:
        """Return the callback that the pointer arriving runs."""
        def show(*event: 'tkinter.Event[tkinter.Misc]') -> None:
            """Put the tooltip beside the pointer that has just arrived."""
            self._show(event[0] if event else None)
        return show

    def _hider(self) -> Callable[..., None]:
        """Return the callback that the pointer leaving runs."""
        def hide(*event: 'tkinter.Event[tkinter.Misc]') -> None:
            """Take the tooltip away again."""
            _ = event
            self._hide()
        return hide

    def _show(self, event: Optional['tkinter.Event[tkinter.Misc]']) -> None:
        """Put the tooltip beside the pointer, unless one is there already.

        Args:
            event: The event that says where the pointer is, or None where the
                callback was run without one.
        """
        if self._window is not None or event is None:
            return
        across, down = TOOLTIP_OFFSET
        window = tkinter.Toplevel(self._widget)
        window.overrideredirect(True)
        window.geometry(f'+{event.x_root + across}+{event.y_root + down}')
        label = tkinter.Label(window, text=self._text, justify='left',
                              background=TOOLTIP_BACKGROUND,
                              highlightbackground=TOOLTIP_BORDER,
                              highlightthickness=1, padx=TOOLTIP_PADDING,
                              pady=0)
        label.pack()
        self._window = window

    def _hide(self) -> None:
        """Take the tooltip away, if there is one there."""
        if self._window is not None:
            self._window.destroy()
            self._window = None
