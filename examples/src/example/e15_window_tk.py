#! /usr/bin/env python3
"""Example 15: the editor in a Tk window of its own, over an application.

This example is a small Tkinter application: a window with content of its own
-- a status line and two buttons -- that also happens to offer a configuration
editor. Unlike example 13, the application already has a window it wants to
keep whole, so the editor gets a window of its own over it.

parent, not area
----------------
Passing the application's window as ``parent`` tells ``TkEditorPanel`` to build
its *own* new window for the editor over that one, and to destroy that window
again when the session ends. modal defaults to True, so the editor holds the
application until the user closes it -- which is what an application that wants
its configuration seen to usually means. See e13_embedded_tk.py for the
alternative: no window of its own, built into part of an existing window
instead.

Building the editor returns at once, because the application's own ``mainloop``
is already running. ``on_close`` says that the session has ended, and
``saved_config`` says what came of it.

``panel.close()`` is how the application closes the editor itself, which is
what the second button does, and this window is where what modal costs can be
seen: while the editor holds the application, that button cannot be pressed at
all, so the way out of a modal editor is the editor's own Close. Pass
``modal=False`` here and the button works exactly as it does in
e13_embedded_tk.py, at the price of an application whose own controls answer
beside a window that is asking to be finished.

Running it
----------
::

    python3 e15_window_tk.py
    python3 e15_window_tk.py -i ../../data/e13_pipeline.json -o /tmp/p.json
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional
import sys
from tkinter import Button, Label, Tk
# See e13_embedded_tk.py: this is what makes the `example` package importable
# when this file is run as a script.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
# pylint: disable-next=wrong-import-position
from edit_cfg_json_tk import TkEditorPanel  # noqa: E402
# pylint: disable-next=wrong-import-position
from example._shared_pipeline import CLOSE_TEXT, DESCRIPTIONS, \
    EDIT_TEXT, PipelineConfig, editor_files, session_result  # noqa: E402


class PipelineApp:  # pylint: disable=too-few-public-methods
    """An application window that opens the editor in a window of its own."""

    def __init__(self, root: Tk, in_file: Optional[str],
                 out_file: Optional[str]) -> None:
        """Build the window's own content and its editor button.

        Args:
            root: Window of the application.
            in_file: Configuration file the editor reads, if any.
            out_file: Configuration file the editor writes, if any.
        """
        self._root = root
        self._in_file = in_file
        self._out_file = out_file
        self._panel: Optional[TkEditorPanel] = None
        root.title('Pipeline console')
        self._status = Label(root, text='No editing yet.', width=44)
        self._status.pack(padx=12, pady=12)
        Button(root, text=EDIT_TEXT, command=self._edit).pack(pady=12)
        Button(root, text=CLOSE_TEXT, command=self._close).pack(pady=12)

    def _edit(self) -> None:
        """Open the editor in a modal window of its own over this one."""
        # See e13_embedded_tk.py about the deliberate repetition of this call
        # between the four examples: `parent` in place of `area` is the whole
        # difference this example is about.
        # pylint: disable=duplicate-code
        if self._panel is None:
            self._panel = TkEditorPanel(PipelineConfig(), parent=self._root,
                                        descriptions=DESCRIPTIONS,
                                        in_file=self._in_file,
                                        out_file=self._out_file,
                                        on_close=self._editor_gone)

    def _close(self) -> None:
        """Close the editor from the application, asking about what is lost.

        A modal editor holds the application, so this cannot be reached until
        the editor's window has gone. See the module docstring.
        """
        # See `_edit` about the deliberate repetition between the examples.
        # pylint: disable=duplicate-code
        if self._panel is not None:
            self._panel.close()

    def _editor_gone(self) -> None:
        """Say what the session wrote, once the editor's window has gone."""
        # See `_edit` about the deliberate repetition between the examples.
        # pylint: disable=duplicate-code
        assert self._panel is not None
        self._status.configure(text=session_result(self._panel.saved_config))
        self._panel = None


def main(args: Optional[list[str]] = None) -> None:
    """Run the application until its own window is closed.

    Args:
        args: Optional replacement for `sys.argv[1:]`, mainly for tests.
    """
    # pylint: disable=duplicate-code
    files = editor_files('e15_window_tk', args)
    root = Tk()
    PipelineApp(root, in_file=files.in_file, out_file=files.out_file)
    root.mainloop()


# The usual guard, so that importing this module from a test runs nothing.
if __name__ == '__main__':
    main()
