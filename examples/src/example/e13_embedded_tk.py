#! /usr/bin/env python3
"""Example 13: the editor in an area of a Tk window the application owns.

This example's window is split in two: a left panel that is the application's
own content -- a status line and two buttons -- and a right panel that is
nothing but an empty frame until the editor is built into it. Unlike example
15, the editor never gets a window of its own here.

It cannot be `edit_cfg_json_tk.edit`, which creates a `tkinter.Tk` of its own:
a second one in a process is a second Tcl interpreter, and no widget, variable,
font or image crosses between two of them.

area, not parent -- and modal is the application's call
------------------------------------------------------
Passing the frame as ``area`` tells ``TkEditorPanel`` to fill that frame rather
than to open a window of its own. modal defaults to True, but this example
passes modal=False on purpose: the button in the left panel keeps working while
the editor runs, which is the whole point of embedding instead of opening a
window. Passing modal=True here would still avoid a window, but would hold the
whole application until the editor closed.

Building the editor returns at once, because the application's own ``mainloop``
is already running. ``on_close`` says that the session has ended, and
``saved_config`` says what came of it -- a widget has no moment at which it
could return anything. The keys of the editor reach the editor and nothing
else, so ``ctrl+s`` in one of its fields saves and the application keeps its
own keys.

``panel.close()`` is how the application closes the editor itself, which is
what the second button of the left panel does. Because this editor is not
modal, that button can be pressed while the editor is running -- press it and
the area is empty again. It asks about anything unsaved, in the same words the
editor's own Close does; an application that is already putting a question of
its own to the user passes ``close(ask_about_unsaved=False)`` instead.

Running it
----------
::

    python3 e13_embedded_tk.py
    python3 e13_embedded_tk.py -i ../../data/e13_pipeline.json -o /tmp/p.json
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional
import sys
from tkinter import Button, Frame, Label, Tk
# Running this file directly puts only its own folder on sys.path, so the
# `example` package it belongs to would not be importable. Adding the folder
# above it makes both ways of using this file work: as a script, and imported
# by a test.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
# pylint: disable-next=wrong-import-position
from edit_cfg_json_tk import TkEditorPanel  # noqa: E402
# pylint: disable-next=wrong-import-position
from example._shared_pipeline import CLOSE_TEXT, DESCRIPTIONS, \
    EDIT_TEXT, PipelineConfig, editor_files, session_result  # noqa: E402


class SplitWindowApp:  # pylint: disable=too-few-public-methods
    """A window with its own left panel and a right area for the editor."""

    def __init__(self, root: Tk, in_file: Optional[str],
                 out_file: Optional[str]) -> None:
        """Build the two panels and the button that opens the editor.

        Args:
            root: Window of the application.
            in_file: Configuration file the editor reads, if any.
            out_file: Configuration file the editor writes, if any.
        """
        self._in_file = in_file
        self._out_file = out_file
        self._panel: Optional[TkEditorPanel] = None
        root.title('Pipeline console with an embedded editor')
        left = Frame(root, borderwidth=1, relief='groove')
        left.pack(side='left', fill='y', padx=8, pady=8)
        self._status = Label(left, text='No editing yet.', wraplength=160)
        self._status.pack(padx=8, pady=8)
        edit = Button(left, text=EDIT_TEXT, command=self._edit)
        edit.pack(padx=8, pady=8)
        close = Button(left, text=CLOSE_TEXT, command=self._close)
        close.pack(padx=8, pady=8)
        self._area = Frame(root, borderwidth=1, relief='sunken')
        self._area.pack(side='left', fill='both', expand=True, padx=8, pady=8)

    def _edit(self) -> None:
        """Build the editor inside the right area, non-modally."""
        # Every one of these four examples makes this one call, because that
        # call is what each of them is about. Keeping each example complete on
        # its own is worth more here than sharing the statement would be.
        # pylint: disable=duplicate-code
        if self._panel is None:
            self._panel = TkEditorPanel(PipelineConfig(), area=self._area,
                                        modal=False, in_file=self._in_file,
                                        out_file=self._out_file,
                                        descriptions=DESCRIPTIONS,
                                        on_close=self._editor_gone)

    def _close(self) -> None:
        """Close the editor from the application, asking about what is lost."""
        # See `_edit` about the deliberate repetition between the examples.
        # pylint: disable=duplicate-code
        if self._panel is not None:
            self._panel.close()

    def _editor_gone(self) -> None:
        """Say what the session wrote, and offer the button again."""
        # See `_edit` about the deliberate repetition between the examples.
        # pylint: disable=duplicate-code
        assert self._panel is not None
        self._status.configure(text=session_result(self._panel.saved_config))
        self._panel = None


def main(args: Optional[list[str]] = None) -> None:
    """Run the split-window application until its window is closed.

    Args:
        args: Optional replacement for `sys.argv[1:]`, mainly for tests.
    """
    # pylint: disable=duplicate-code
    files = editor_files('e13_embedded_tk', args)
    root = Tk()
    SplitWindowApp(root, in_file=files.in_file, out_file=files.out_file)
    root.mainloop()


# The usual guard, so that importing this module from a test runs nothing.
if __name__ == '__main__':
    main()
