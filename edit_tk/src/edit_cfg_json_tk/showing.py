#! /usr/bin/env python3
"""What this editor has to wait for its own window to be on the screen for.

Two things it asks Tk for cannot be asked for while it is being built. The
keyboard focus for its first field is one: Tk drops a request for the focus
while the widget or any of its ancestors is unmapped, and says nothing about
having dropped it. The grab of a modal session is the other: Tk refuses one
for a window that is not viewable, and whether a window that has just been
created counts as viewable is a platform answer rather than a rule.

So both wait for the map, which is what this module is. Nothing here knows
what an edit model is: it is what Tk needs in order to do something once,
when what was built is really on the screen, in the same way as the scrolling
beside it.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
import tkinter


def when_shown(widget: tkinter.Misc, action: Callable[[], None]) -> None:
    """Run one action the first time a widget reaches the screen.

    **The layout is asked for before the action runs**, because the event
    says that this widget is mapped and not that what is inside it is: an
    editor mounted in a window that is already up is mapped a round of idle
    work before its own fields are, and a focus asked for in between is one
    that Tk drops.

    **The action runs once.** A window that is hidden and shown again is
    mapped again, and an editor that took the focus back each time would take
    it from wherever the user had put it since.

    Args:
        widget: Widget that the editor built, whose arrival on the screen is
            what the action waits for.
        action: What to do once it is there.
    """
    shown_once = False

    def shown(*event: 'tkinter.Event[tkinter.Misc]') -> None:
        """Do it, now that Tk says the widget is on the screen."""
        _ = event
        nonlocal shown_once
        if shown_once:
            return
        shown_once = True
        widget.update_idletasks()
        action()
    widget.bind('<Map>', shown, add='+')
