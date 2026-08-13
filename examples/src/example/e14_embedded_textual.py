#! /usr/bin/env python3
"""Example 14: the editor inside a Textual application that already runs.

This is example 13 in the other toolkit, and the reason is the same one:
`edit()` runs a Textual application of its own, `App.run()` calls
`asyncio.run`, and calling it from inside a running application raises or
deadlocks. An application that already runs Textual therefore mounts the
editor instead of being replaced by it.

Textual gives it two shapes, and this example runs both:

````python
from edit_cfg_json_textual import EditorPanel, EditorScreen

yield EditorPanel(model, on_close=self.editor_gone)   # one area of a screen
self.push_screen(EditorScreen(model, on_close=self.editor_gone))  # a screen
````

`EditorPanel` is a widget, so it goes wherever the application puts a widget
and the application keeps its own header, its own footer and its own command
palette. `EditorScreen` is that same panel with a header, a footer and the
palette entries of the editor around it, for an application that wants the
editor to have the terminal for a while. Neither of them blocks: the
application's event loop is already running, and `on_close` is how it learns
that the session has ended.

## What the terminal shows

````sh
cd examples/src/example
python3 e14_embedded_textual.py
python3 e14_embedded_textual.py --mount screen
python3 e14_embedded_textual.py -i ../../data/e13_pipeline.json
````

With `--mount panel`, which is the default, the application's own screen holds
a heading of its own, a field of its own, and the editor below them. With
`--mount screen`, that same screen holds the heading and the field, and the
editor is pushed on top of it as a screen with a footer and a palette of its
own; `f7` pushes it again once it has been closed.

- **The keys of the editor reach the editor.** Put the focus in the
  application's own field and press `ctrl+s`: the application says that it
  read the key itself. Put it in a field of the editor and press the same
  combination, and the editor saves. Textual offers a key from the focused
  widget upwards, and the application's field is not inside the editor, which
  is what mounting the editor as a widget buys.
- **`--ordinary-keys` gives the key to the focused widget first**, which is
  `edit_cfg_json.Settings.priority_keys` and is the one setting that only an
  embedded editor has a reason to change. This application gives the explain
  action `ctrl+e` beside its `f1`, because Textual's own field reads `ctrl+e`
  as "go to the end of the line": with the flag, `ctrl+e` in a field of the
  editor moves the caret and explains nothing, and without it the editor is
  offered the key first and explains. `f1` explains either way, because no
  field claims it.
- **Closing is asked for and answered.** The editor's own Close asks before it
  drops something unsaved, and so does the application's `f8`. `f9` is
  `close(ask_about_unsaved=False)`, for an application that already has a
  question of its own to put.
- **The application is told, and reads the outcome itself.** `on_close` says
  that the session ended and `model.saved_config` says what came of it, which
  is what a non-blocking editor can offer instead of a return value.

## What is not in this file

The configuration class is example 13's, imported rather than written again:
this example is about where the editor is and not about what it is editing.
Examples 8 to 11 are where the shapes a real configuration has are taught, and
all of it works here unchanged, because it is the same editor.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import ClassVar, Optional
import argparse
import sys
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header, Input, Label
from edit_cfg_json import ActionSettings, EditModel, Settings, load_config, \
    named_policy
from edit_cfg_json_textual import EditorPanel, EditorScreen

MOUNT_PANEL = 'panel'
"""Value of `--mount` that puts the editor in an area of the screen."""

MOUNT_SCREEN = 'screen'
"""Value of `--mount` that pushes the editor as a screen of its own."""

APP_HEADING = 'Pipeline console — the application owns this screen'
"""What the application says above the editor it mounted."""

APP_FIELD_LABEL = 'Search (a field of the application):'
"""Label of the field that the application has beside the editor.

It is here so that there is somewhere to put the focus that is not the
editor, which is what shows that the keys of the editor reach the editor.
"""

TOLD_ID = 'told'
"""Identifier of the line the application says its own things on."""

FIELD_ID = 'search'
"""Identifier of the application's own field."""

APP_KEY_TEXT = 'The application read ctrl+s itself.'
"""What the application says when its own key was pressed."""

GONE_TEXT = 'The editor has closed. Saved: {saved}'
"""What the application says once the session has ended."""

OPEN_TEXT = 'Press f7 to open the editor again.'
"""What it says while there is no editor on the screen."""

FIELD_KEY = 'ctrl+e'
"""A key of the editor that its own field claims for itself.

Textual's `Input` reads it as "go to the end of the line", so it is the one
combination in this example where `edit_cfg_json.Settings.priority_keys`
decides which of the two acts on a key press.
"""

EDITOR_ACTIONS = ActionSettings(explain=('f1', FIELD_KEY))
"""The keys this application gives the editor.

It is the editor's own defaults with one combination added, and that one is
there to be fought over. Every other key of the editor is left alone.
"""

APP_CSS = """
#told { height: 1; color: $text-accent; }
#search { height: 3; }
"""
"""The little the application says about how its own widgets look."""


class PipelineApp(App[None]):
    """A Textual application with widgets of its own and an editor in it.

    A real application has more in it than this, and it has exactly this much
    to do with the editor: it builds the model, it mounts the editor where it
    wants it, and it is told when the session has ended.
    """

    CSS: ClassVar[str] = APP_CSS
    """How the application's own widgets look.

    The editor brings its own, because a widget declares the style sheet of
    what is inside it, so nothing here says anything about the editor at all.
    """

    BINDINGS: ClassVar[list[Binding | tuple[str, str] |
                            tuple[str, str, str]]] = [
        Binding('f7', 'open_editor', 'Open editor'),
        Binding('f8', 'close_editor', 'Close editor'),
        Binding('f9', 'drop_editor', 'Drop editor')]
    """The keys of the application itself, which are not the editor's.

    They are function keys that no field claims, because an application key
    that a field read for itself would be showing something this example is
    not about.
    """

    def __init__(self, model: EditModel, as_screen: bool) -> None:
        """Remember the model and how the editor is to be mounted.

        Args:
            model: Model to edit, which the application built itself.
            as_screen: Whether the editor is pushed as a screen of its own
                rather than mounted in an area of the application's screen.
        """
        super().__init__()
        self._model = model
        self._as_screen = as_screen
        self._panel: Optional[EditorPanel] = None
        self._told = Label('', id=TOLD_ID)

    def compose(self) -> ComposeResult:
        """Create the application's own widgets, and maybe the editor.

        The editor is one more widget of this screen, put where the
        application wants it. What is above it is the application's and the
        editor can neither reach it nor style it.
        """
        yield Header()
        yield Label(APP_HEADING)
        yield Label(APP_FIELD_LABEL)
        yield Input(id=FIELD_ID)
        yield self._told
        if not self._as_screen:
            self._panel = EditorPanel(self._model, on_close=self._editor_gone)
            yield self._panel
        yield Footer()

    def on_mount(self) -> None:
        """Push the editor as a screen, for the run that asked for one."""
        if self._as_screen:
            self.action_open_editor()

    def action_open_editor(self) -> None:
        """Open the editor again once a session has ended.

        Only the run that mounts it as a screen can do this, because a screen
        is pushed and popped while a widget of a screen is composed with it.
        """
        if self._as_screen and self._panel is None:
            screen = EditorScreen(self._model, on_close=self._editor_gone)
            self._panel = screen.panel
            self.push_screen(screen)

    def action_close_editor(self) -> None:
        """Close the editor, asking about what has not been saved."""
        if self._panel is not None:
            self._panel.close()

    def action_drop_editor(self) -> None:
        """Close it without asking, which is what the application decides.

        An application that is shutting down for reasons of its own already
        has a question to put to the user and does not want two.
        """
        if self._panel is not None:
            self._panel.close(ask_about_unsaved=False)

    def on_key(self, event: object) -> None:
        """Say that the application read the save combination itself.

        The editor uses the same combination, which is the point: pressing it
        with the focus in the field above and with the focus in a field of the
        editor is what shows which of the two a key reaches.
        """
        key = getattr(event, 'key', '')
        if key == 'ctrl+s':
            self._told.update(APP_KEY_TEXT)

    def _editor_gone(self) -> None:
        """Say that the session has ended, and what came of it.

        This is what an application learns from an embedded editor, because
        an editor that does not block cannot return anything. What was written
        is on the model, which the application built and still holds.
        """
        saved = self._model.saved_config
        name = 'nothing' if saved is None else type(saved).__name__
        if self._as_screen:
            self.pop_screen()
        self._panel = None
        # The label is held rather than looked up, because in the run that
        # pushes the editor as a screen this happens while the screen that
        # holds the label is not the one on top.
        self._told.update(f'{GONE_TEXT.format(saved=name)} {OPEN_TEXT}'
                          if self._as_screen
                          else GONE_TEXT.format(saved=name))


def _parsed(args: Optional[list[str]]) -> argparse.Namespace:
    """Return the command line of this example.

    It is the one that example 13 has, with the choice this toolkit offers
    and the other one does not added to it.

    Args:
        args: Optional replacement for `sys.argv[1:]`.

    Returns:
        The parsed command line.
    """
    # The import is inside the function so that running this file directly
    # works. The block at the end of the file puts the examples source folder
    # on sys.path first, and only after that is `example.cmd_line` importable.
    # pylint: disable-next=import-outside-toplevel
    from example.cmd_line import embedded_parser
    parser = embedded_parser('e14_embedded_textual')
    parser.add_argument('--mount', default=MOUNT_PANEL,
                        choices=(MOUNT_PANEL, MOUNT_SCREEN),
                        help='Where the editor goes in the application.')
    return parser.parse_args(args)


def _model_of(parsed: argparse.Namespace) -> EditModel:
    """Return the model that this application edits.

    An application that mounts the editor builds the model itself, which is
    the two statements `edit()` saves a program that does not.

    Args:
        parsed: Parsed command line of one run.

    Returns:
        The model to hand to the editor.
    """
    # The class is example 13's, because what these two examples teach is
    # where the editor goes and not what it is editing.
    # pylint: disable-next=import-outside-toplevel
    from example.e13_embedded_tk import DESCRIPTIONS, PipelineConfig
    settings = Settings(actions=EDITOR_ACTIONS,
                        priority_keys=not parsed.ordinary_keys)
    loaded = load_config(config=PipelineConfig(), settings=settings,
                         in_file=parsed.input,
                         policy=named_policy(parsed.policy))
    return EditModel(config=loaded.config, report=loaded.report,
                     descriptions=DESCRIPTIONS, settings=settings,
                     out_file=parsed.output or parsed.input)


def main(args: Optional[list[str]] = None) -> None:
    """Run this example from the command line.

    Args:
        args: Optional replacement for `sys.argv[1:]`, mainly for tests.
    """
    # See `_parsed` for why this import is inside the function.
    # pylint: disable-next=import-outside-toplevel
    from example.cmd_line import session_result
    parsed = _parsed(args)
    model = _model_of(parsed)
    PipelineApp(model, as_screen=parsed.mount == MOUNT_SCREEN).run()
    print(session_result(model.saved_config))


# The usual guard, so that importing this module from a test runs nothing.
if __name__ == '__main__':
    # Running a file directly puts only that file's own folder on sys.path,
    # so the `example` package this file belongs to would not be importable.
    # Adding the folder above it makes both ways of using this file work:
    # `python3 examples/src/example/e14_embedded_textual.py` and
    # `from example import e14_embedded_textual` from a test.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    main()
