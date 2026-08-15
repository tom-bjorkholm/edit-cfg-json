#! /usr/bin/env python3
"""Example 16: the editor as a Textual screen of its own, over an application.

This is example 15 in the other toolkit: an application with a screen of its
own -- a status line and a button -- that also offers a configuration editor.
Textual has no second window to open, so the editor is pushed as a screen on
top of the application's own.

A screen the application pushes
-------------------------------
``EditorScreen`` is ``EditorPanel`` with a header, a footer and the command
palette entries of the editor around it, which is what a widget cannot have. It
takes itself off the application again when the session ends, so the
application's own screen is back on top by the time it is told. See
e14_embedded_textual.py for the alternative: mounted in an area of the
application's own screen, which keeps the application's header, footer and
palette.

Pushing it returns at once, because the application's event loop is already
running. ``on_close`` says that the session has ended, and ``saved_config``
says what came of it.

``screen.close()`` is how the application closes the editor itself, which is
what its second button does. It is worth having: ``ctrl+q`` is the editor's own
key for closing *and* Textual's key for quitting an application, and Textual
gives an application's own binding the key first, so an application that wants
the editor's close key to work gives the editor another one with
``Settings(actions=ActionSettings(quit=...))``.

Running it
----------
::

    python3 e16_screen_textual.py
    python3 e16_screen_textual.py -i ../../data/e13_pipeline.json -o /tmp/p
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional
import sys
from textual.app import App, ComposeResult
from textual.widgets import Button, Label
# See e13_embedded_tk.py: this is what makes the `example` package importable
# when this file is run as a script.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
# pylint: disable-next=wrong-import-position
from edit_cfg_json_textual import EditorScreen  # noqa: E402
# pylint: disable-next=wrong-import-position
from example._shared_pipeline import CLOSE_TEXT, DESCRIPTIONS, \
    EDIT_TEXT, PipelineConfig, editor_files, \
    session_result  # noqa: E402


class PipelineApp(App[None]):
    """An application that pushes the editor as a screen of its own."""

    def __init__(self, in_file: Optional[str],
                 out_file: Optional[str]) -> None:
        """Remember which files the editor is to read and write.

        Args:
            in_file: Configuration file the editor reads, if any.
            out_file: Configuration file the editor writes, if any.
        """
        super().__init__()
        self._in_file = in_file
        self._out_file = out_file
        self._editor: Optional[EditorScreen] = None
        self._status = Label('No editing yet.')

    def compose(self) -> ComposeResult:
        """Create this application's own widgets."""
        yield self._status
        yield Button(EDIT_TEXT)
        yield Button(CLOSE_TEXT)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Push the editor, or close it, as the pressed button says."""
        if str(event.button.label) == CLOSE_TEXT:
            if self._editor is not None:
                self._editor.close()
            return
        self._push_editor()

    def _push_editor(self) -> None:
        """Push the editor on top of the application's own screen."""
        # See e13_embedded_tk.py about the deliberate repetition of this call
        # between the four examples.
        # pylint: disable=duplicate-code
        if self._editor is None:
            self._editor = EditorScreen(PipelineConfig(),
                                        descriptions=DESCRIPTIONS,
                                        in_file=self._in_file,
                                        out_file=self._out_file,
                                        on_close=self._editor_gone)
            self.push_screen(self._editor)

    def _editor_gone(self) -> None:
        """Say what the session wrote, once its screen has been popped."""
        # See `on_button_pressed` about the repetition between the examples.
        # pylint: disable=duplicate-code
        assert self._editor is not None
        self._status.update(session_result(self._editor.saved_config))
        self._editor = None


def main(args: Optional[list[str]] = None) -> None:
    """Run the application until the user quits it.

    Args:
        args: Optional replacement for `sys.argv[1:]`, mainly for tests.
    """
    # pylint: disable=duplicate-code
    files = editor_files('e16_screen_textual', args)
    PipelineApp(in_file=files.in_file, out_file=files.out_file).run()


# The usual guard, so that importing this module from a test runs nothing.
if __name__ == '__main__':
    main()
