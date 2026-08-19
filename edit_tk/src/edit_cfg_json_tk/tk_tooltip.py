#! /usr/bin/env python3
"""The tooltip that Tk does not have, for a control too small to label.

Every control of this editor says what it does in the word on it, with two
exceptions: the four that say where a search looks are ticked and unticked
often enough to be worth a line of their own, and a line of their own is width
that the values would lose, and the one that goes to the next member found
carries the arrow that every editor draws for that. Those five carry a label of
one or two characters and say the rest here.

Tk has no tooltip. There is no widget for one and no option on a widget that
asks for one, so this is what it amounts to: a label with a line round it, put
beside the pointer while the pointer rests on the control and taken away again
when it leaves. It is a module of its own for the same reason as the scrolling
beside it — none of it is about an edit model, and it is what Tk needs in order
to have a tooltip at all.

The label goes *inside the window the control is in*, and not in a borderless
window of its own. A window of its own is what a toolkit with a tooltip does,
and it is what this had first: macOS then gives it rounded corners and a
shadow, and a corner whose radius is about half the height of a line of text
eats the first character and the last. A label inside the window is drawn by Tk
and by nothing else, so it is a rectangle with sharp corners on every platform
and every version of Tk, and it cannot outlive the window it is in. What that
costs is that a tooltip cannot reach outside the window, which is why it is
kept inside it and why its text is wrapped.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from typing import Optional
import textwrap
import tkinter

TOOLTIP_BACKGROUND = '#ffffe0'
"""Background of a tooltip, which is the pale yellow every toolkit uses."""

TOOLTIP_BORDER = '#9aa5b1'
"""Colour of the line around a tooltip, as around an edit field."""

TOOLTIP_OFFSET = (12, 20)
"""How far from the pointer, in pixels across and down, a tooltip is put.

Down rather than up, and to the right rather than the left, so that the
tooltip does not land under the pointer itself: a label that appeared where
the pointer is would take the leave event that closes it again.
"""

TOOLTIP_PADDING = 4
"""Padding in pixels between the text of a tooltip and its border."""

TOOLTIP_WIDTH = 60
"""How many characters of a tooltip go on one line.

Characters and not pixels, because that is what the standard library measures
in and a width in pixels would have to be measured in whatever font the label
ended up with. Sixty of them is narrow enough that a whole tooltip fits beside
a control anywhere in a window that a configuration is edited in, which is what
a tooltip drawn inside that window has to do.
"""


def _inside(place: int, need: int, room: int) -> int:
    """Return where the tooltip goes so that the whole of it is in the window.

    Args:
        place: Where it would go, which is beside the pointer.
        need: How much room it needs, across or down.
        room: How much there is.

    Returns:
        Where it goes, which is where it would have gone unless that would put
        an edge of it outside the window, and the near edge where the window is
        smaller than the tooltip.
    """
    return max(0, min(place, room - need))


class Tooltip:  # pylint: disable=too-few-public-methods
    """One text that appears while the pointer rests on one widget.

    The label is made when the pointer arrives and destroyed when it leaves,
    rather than made once and hidden, because a tooltip is seen for a second or
    two in a session and a label that is never shown is a label that is in the
    way of everything the window lays out.
    """

    def __init__(self, widget: tkinter.Misc, text: str) -> None:
        """Say what one widget tells the pointer that rests on it.

        Args:
            widget: Widget that the pointer rests on.
            text: What that widget says about itself.
        """
        self._widget = widget
        self._text = text
        self._label: Optional[tkinter.Label] = None
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
        if self._label is not None or event is None:
            return
        window = self._widget.winfo_toplevel()
        label = self._made(window)
        self._put(label=label, window=window, event=event)
        self._label = label

    def _made(self, window: tkinter.Misc) -> tkinter.Label:
        """Return the label of this tooltip, its text laid out in lines.

        Args:
            window: Window the control is in, which the label goes in too.

        Returns:
            The label, which is not yet anywhere in that window.
        """
        return tkinter.Label(window, justify='left',
                             text=textwrap.fill(self._text, TOOLTIP_WIDTH),
                             background=TOOLTIP_BACKGROUND,
                             highlightbackground=TOOLTIP_BORDER,
                             highlightthickness=1, padx=TOOLTIP_PADDING,
                             pady=0)

    @staticmethod
    def _put(label: tkinter.Label, window: tkinter.Misc,
             event: 'tkinter.Event[tkinter.Misc]') -> None:
        """Put one tooltip beside the pointer and over everything else.

        The place is asked for in the coordinates of the window, and the
        pointer says where it is in the coordinates of the screen, so the two
        differ by wherever the window is.

        Args:
            label: The label of the tooltip.
            window: Window the control is in.
            event: The event that says where the pointer is.
        """
        across, down = TOOLTIP_OFFSET
        x_place = event.x_root - window.winfo_rootx() + across
        y_place = event.y_root - window.winfo_rooty() + down
        label.place(x=_inside(x_place, label.winfo_reqwidth(),
                              window.winfo_width()),
                    y=_inside(y_place, label.winfo_reqheight(),
                              window.winfo_height()))
        label.lift()

    def _hide(self) -> None:
        """Take the tooltip away, if there is one there."""
        if self._label is not None:
            self._label.destroy()
            self._label = None
