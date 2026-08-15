#! /usr/bin/env python3
"""Example 14: the editor in an area of a Textual screen the application owns.

This is example 13 in the other toolkit. The application's screen holds a
status line and a button of its own, and an area that stays empty until the
editor is mounted into it. Unlike example 16, the editor never gets a screen of
its own here.

It cannot be `edit_cfg_json_textual.edit`, because `App.run` calls
`asyncio.run`, and calling that from inside a running application raises or
deadlocks.

A widget the application mounts
-------------------------------
``EditorPanel`` is a widget, so it goes wherever the application puts a widget,
and the application keeps its own header, its own footer and its own command
palette. Mounting returns at once, because the application's event loop is
already running. ``on_close`` says that the session has ended, and
``saved_config`` says what came of it -- a widget has no moment at which it
could return anything.

Textual offers a key from the focused widget upwards, so the keys of the editor
act while the focus is inside the editor and the application keeps its own. The
footer names the editor's actions while the focus is in there, and this
application's own footer is the one that shows them.

``panel.close()`` is how the application closes the editor itself, which is
what its second button does. It is worth having: ``ctrl+q`` is the editor's own
key for closing *and* Textual's key for quitting an application, and Textual
gives an application's own binding the key first, so an application that wants
the editor's close key to work gives the editor another one with
``Settings(actions=ActionSettings(quit=...))``.

Who is offered a key first
--------------------------
This application builds a ``Settings`` of its own in Python, the way a real
application does -- it knows its own answers and does not parse them from a
command line. What it says is ``priority_keys=False``, which is the one setting
that only an embedded editor has a reason to change, and it is shown here on a
combination where the difference can be seen: the editor is asked to explain on
``ctrl+e`` beside its ``f1``, and Textual's own ``Input`` reads ``ctrl+e`` as
"go to the end of the line".

So press ``ctrl+e`` in a field of the editor and the caret moves; press ``f1``
and the editor explains, because no field claims ``f1``. Change the one line
below to ``priority_keys=True``, which is the default, and ``ctrl+e`` explains
instead of moving the caret. The price of saying False is on the screen too:
``ctrl+q`` is then Textual's quit rather than the editor's close, which is why
the application has a button for closing.

Running it
----------
::

    python3 e14_embedded_textual.py
    python3 e14_embedded_textual.py -i ../../data/e13_pipeline.json -o /tmp/p
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import ClassVar, Optional
import sys
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Footer, Label
# See e13_embedded_tk.py: this is what makes the `example` package importable
# when this file is run as a script.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
# pylint: disable-next=wrong-import-position
from edit_cfg_json import ActionSettings, Settings  # noqa: E402
# pylint: disable-next=wrong-import-position
from edit_cfg_json_textual import EditorPanel  # noqa: E402
# pylint: disable-next=wrong-import-position
from example._shared_pipeline import CLOSE_TEXT, DESCRIPTIONS, \
    EDIT_TEXT, PipelineConfig, editor_files, \
    session_result  # noqa: E402

AREA_ID = 'area'
"""Identifier of the part of the screen the editor is mounted in."""

ORDINARY_KEYS = Settings(priority_keys=False,
                         actions=ActionSettings(explain=('f1', 'ctrl+e')))
"""What this application has already decided about the editor's keys.

`priority_keys=False` offers a key to the widget that has the focus before the
editor, which is the other way round from the default. `ctrl+e` beside `f1` is
what makes the difference visible, because Textual's own `Input` reads that
combination for itself. See the module docstring.
"""


class SplitScreenApp(App[None]):
    """An application screen with an area that the editor is mounted in."""

    CSS: ClassVar[str] = f'#{AREA_ID} {{ height: 1fr; }}'
    """The one thing this application says about its own widgets.

    The editor brings its own style sheet, because a Textual widget declares
    how what is inside it looks.
    """

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
        self._panel: Optional[EditorPanel] = None
        self._status = Label('No editing yet.')

    def compose(self) -> ComposeResult:
        """Create this application's own widgets and the empty area."""
        yield self._status
        yield Button(EDIT_TEXT)
        yield Button(CLOSE_TEXT)
        yield Vertical(id=AREA_ID)
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Mount the editor, or close it, as the pressed button says."""
        if str(event.button.label) == CLOSE_TEXT:
            if self._panel is not None:
                self._panel.close()
            return
        self._mount_editor()

    def _mount_editor(self) -> None:
        """Mount the editor in the area of the application's own screen."""
        # See e13_embedded_tk.py about the deliberate repetition of this call
        # between the four examples.
        # pylint: disable=duplicate-code
        if self._panel is None:
            self._panel = EditorPanel(PipelineConfig(),
                                      descriptions=DESCRIPTIONS,
                                      in_file=self._in_file,
                                      out_file=self._out_file,
                                      settings=ORDINARY_KEYS,
                                      on_close=self._editor_gone)
            self.query_one(f'#{AREA_ID}', Vertical).mount(self._panel)

    def _editor_gone(self) -> None:
        """Say what the session wrote, once the area is empty again."""
        # See `on_button_pressed` about the repetition between the examples.
        # pylint: disable=duplicate-code
        assert self._panel is not None
        self._status.update(session_result(self._panel.saved_config))
        self._panel = None


def main(args: Optional[list[str]] = None) -> None:
    """Run the application until the user quits it.

    Args:
        args: Optional replacement for `sys.argv[1:]`, mainly for tests.
    """
    # pylint: disable=duplicate-code
    files = editor_files('e14_embedded_textual', args)
    SplitScreenApp(in_file=files.in_file, out_file=files.out_file).run()


# The usual guard, so that importing this module from a test runs nothing.
if __name__ == '__main__':
    main()
