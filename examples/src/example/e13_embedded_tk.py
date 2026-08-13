#! /usr/bin/env python3
"""Example 13: the editor inside a Tkinter window the application owns.

Every example before this one hands a configuration object to `edit()` and
gets a window with an editor in it. That is right for a program whose whole
job is editing a configuration, and it is wrong for an application that
already has a window of its own: `edit()` creates a `tkinter.Tk`, a second
`tkinter.Tk` in one process is a second Tcl interpreter, and no widget,
variable, font or image crosses between two of them.

So this example is the other door, and it is the whole of what an application
with its own window has to do:

````python
from edit_cfg_json import EditModel, load_config
from edit_cfg_json_tk import TkEditorPanel

loaded = load_config(config=PipelineConfig(), in_file='pipeline.json')
model = EditModel(config=loaded.config, report=loaded.report,
                  out_file='pipeline.json')
panel = TkEditorPanel(parent=area, model=model, on_close=editor_gone)
````

Three statements and a callback, and none of them starts an event loop: the
application's own `mainloop` is already running, and the editor is a widget
in it like any other. That is why this cannot be `TkEditor.run_editor`, which
promises to run until the user is done and would have to suspend the
application's call stack to keep that promise.

## What the window shows

````sh
cd examples/src/example
python3 e13_embedded_tk.py
python3 e13_embedded_tk.py -i ../../data/e13_pipeline.json
````

A window with a heading of the application's own, a row of the application's
own controls, and the editor filling the rest of it. The heading and the
controls are not the editor's and the editor cannot touch them, which is what
the four things below are about.

- **The application named the widget the editor goes in**, which is the frame
  that `PipelineWindow` builds last. The editor builds one frame of its own
  inside it and never anything outside it, so the title of the window, its
  size, its close button and the rest of what is in it stay the application's.
- **The keys of the editor reach the editor and nothing else.** Press `ctrl+s`
  while the focus is in a field of the editor and it saves; press it while the
  focus is in the application's own field above it and the application gets it
  and says so. That is what the editor being one part of a window means, and
  it is why the editor is not simply bound to the window.
- **Closing is asked for and answered.** Press the editor's own Close, or the
  application's *Close editor* button, and a session holding something unsaved
  asks before it drops it. What the application gets afterwards is `on_close`,
  and `model.saved_config` is what came of the session.
- **The application decides whether the question is asked at all.**
  `panel.close(ask_about_unsaved=False)` is what the *Drop editor* button does,
  because an application that is shutting down for reasons of its own knows
  that it has a question of its own to put and does not want two.

Run it with `--ordinary-keys` and the first of those changes: the editor is
then offered a key only after the widget with the focus has had it, which is
what an application whose own field already reads `ctrl+s` asks for. It is
`edit_cfg_json.Settings.priority_keys`, and it is the one setting that only an
embedded editor has a reason to change.

## What is not in this file

The configuration class is small on purpose: this example is about where the
editor is and not about what it is editing. Examples 8 to 11 are where the
shapes a real configuration has are taught, and everything they show works
here unchanged, because it is the same editor.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from pathlib import Path
from typing import Optional, TextIO
import sys
import tkinter
from config_as_json import Config, IntFloatValidator, \
    MemberValidationStep, PathOrStr, ValidationPlan
from edit_cfg_json import Descriptions, EditModel, Settings, load_config, \
    named_policy
from edit_cfg_json_tk import TkEditorPanel

APP_TITLE = 'Pipeline console'
"""Title of the window, which is the application's and not the editor's."""

APP_HEADING = 'Pipeline console — the application owns this window'
"""What the application says above the editor it mounted."""

APP_FIELD_LABEL = 'Search (a field of the application):'
"""Label of the field that the application has beside the editor.

It is here so that there is somewhere to put the focus that is not the
editor, which is what shows that the keys of the editor reach the editor.
"""

CLOSE_TEXT = 'Close editor'
"""Text of the application's own control that closes the editor."""

DROP_TEXT = 'Drop editor'
"""Text of the control that closes it without asking about the changes."""

GONE_TEXT = 'The editor has closed. Saved: {saved}'
"""What the application says once the session has ended."""

APP_KEY_TEXT = 'The application read {key} itself.'
"""What the application says when one of its own keys was pressed."""

DESCRIPTIONS: Descriptions = {
    ('name',): 'What this pipeline is called in the logs.',
    ('workers',): 'How many jobs run at the same time.'}
"""What this application says about the members it declares."""


MOST_WORKERS = 64
"""The largest number of jobs this application will run at the same time."""


def _sensible_count() -> IntFloatValidator[int]:
    """Return the validator that refuses an impossible number of workers."""
    return IntFloatValidator[int](min_value=1, max_value=MOST_WORKERS,
                                  allowed_values=None)


class PipelineConfig(Config):
    """How this application runs its pipeline.

    The members are two ordinary values and are not what this example is
    about. What it is about is that the editor for them is one widget of a
    window that the application built.
    """

    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Initialize the configuration with its default values.

        Args:
            from_json_data_text: Optional JSON text to parse directly.
            from_json_filename: Optional path to a JSON file to read.
            stderr_file: Stream used for user-facing diagnostics.
        """
        self.name: str = 'nightly'
        self.workers: int = 4
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file)

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the one rule this configuration has.

        An embedded editor validates and saves exactly as any other does, and
        one rule is what makes that visible: press Validate with a silly
        number of workers and the editor refuses it in the panel the
        application mounted. Example 4 is where the rules of an application
        are really taught.
        """
        _ = stderr_file
        return [MemberValidationStep(member_names=['workers'],
                                     validator=_sensible_count())]


class PipelineWindow:  # pylint: disable=too-few-public-methods
    """An application window with controls of its own and an editor in it.

    A real application has more in it than this, and it has exactly this much
    to do with the editor: it creates a widget for the editor to go in, it
    hands over a model, and it is told when the session has ended.
    """

    def __init__(self, model: EditModel) -> None:
        """Build the window of the application and mount the editor in it.

        Args:
            model: Model to edit, which the application built itself.
        """
        self._model = model
        self._window = tkinter.Tk()
        self._window.title(APP_TITLE)
        tkinter.Label(self._window, text=APP_HEADING).pack(pady=4)
        self._told = tkinter.Label(self._window, text='')
        self._add_own_field()
        self._add_own_buttons()
        self._told.pack()
        # The editor goes in a widget of the application's own, which is the
        # whole of what the application says about where it is. Everything
        # above stays the application's, and the editor cannot reach it.
        area = tkinter.Frame(self._window)
        area.pack(fill='both', expand=True)
        self._panel = TkEditorPanel(parent=area, model=model,
                                    on_close=self._editor_gone)

    def _add_own_field(self) -> None:
        """Create a field of the application's, beside the editor.

        It is here to be typed into: a key pressed while the focus is in this
        field is the application's and never the editor's, which is what an
        editor that is one part of a window has to be like.
        """
        line = tkinter.Frame(self._window)
        line.pack(fill='x', padx=4)
        tkinter.Label(line, text=APP_FIELD_LABEL).pack(side='left')
        field = tkinter.Entry(line)
        field.pack(side='left', fill='x', expand=True)
        # The application binds the same combination the editor uses for Save,
        # on the window, which is where an application binds its own keys.
        self._window.bind('<Control-s>', self._own_key)

    def _own_key(self, *event: 'tkinter.Event[tkinter.Misc]') -> str:
        """Say that the application itself read one key press.

        The combination is one the editor uses too, on purpose: pressing it in
        one place and in the other is what shows which of the two a key
        reaches. The answer is `break`, which is how a Tk binding says that
        the key has been dealt with, so an editor that is offered the key
        after this one is never offered it at all.
        """
        _ = event
        self._told.config(text=APP_KEY_TEXT.format(key='ctrl+s'))
        return 'break'

    def _add_own_buttons(self) -> None:
        """Create the controls that the application has for the editor."""
        line = tkinter.Frame(self._window)
        line.pack(pady=4)
        for text, asking in ((CLOSE_TEXT, True), (DROP_TEXT, False)):
            tkinter.Button(line, text=text,
                           command=self._closer(asking)).pack(side='left',
                                                              padx=4)

    def _closer(self, asking: bool) -> Callable[[], None]:
        """Return the command of one of the application's own controls.

        Args:
            asking: Whether the user is asked about what has not been saved.
                An application that is shutting down for reasons of its own
                already has a question to put and does not want two.

        Returns:
            What that control does when it is pressed.
        """
        def close_editor() -> None:
            """Close the editor, asking or not as this control decides."""
            self._panel.close(ask_about_unsaved=asking)
        return close_editor

    def _editor_gone(self) -> None:
        """Say that the session has ended, and what came of it.

        This is what an application learns from an embedded editor, because
        an editor that does not block cannot return anything. What was written
        is on the model, which the application built and still holds.
        """
        saved = self._model.saved_config
        name = 'nothing' if saved is None else type(saved).__name__
        self._told.config(text=GONE_TEXT.format(saved=name))

    def run(self) -> Optional[Config]:
        """Run the application until its window is closed.

        Returns:
            The configuration object the session wrote, or None when it wrote
            nothing. It is read from the model rather than returned by the
            editor, because a widget has no moment at which it could return.
        """
        self._window.mainloop()
        return self._model.saved_config


def main(args: Optional[list[str]] = None) -> None:
    """Run this example from the command line.

    An application that mounts the editor builds the model itself, which is
    the three statements `edit()` saves a program that does not.

    Args:
        args: Optional replacement for `sys.argv[1:]`, mainly for tests.
    """
    # The import is inside the function so that running this file directly
    # works. The block at the end of the file puts the examples source folder
    # on sys.path first, and only after that is `example.cmd_line` importable.
    # pylint: disable-next=import-outside-toplevel
    from example.cmd_line import embedded_parser, session_result
    parsed = embedded_parser('e13_embedded_tk').parse_args(args)
    settings = Settings(priority_keys=not parsed.ordinary_keys)
    loaded = load_config(config=PipelineConfig(), settings=settings,
                         in_file=parsed.input,
                         policy=named_policy(parsed.policy))
    model = EditModel(config=loaded.config, report=loaded.report,
                      descriptions=DESCRIPTIONS, settings=settings,
                      out_file=parsed.output or parsed.input)
    print(session_result(PipelineWindow(model).run()))


# The usual guard, so that importing this module from a test runs nothing.
if __name__ == '__main__':
    # Running a file directly puts only that file's own folder on sys.path,
    # so the `example` package this file belongs to would not be importable.
    # Adding the folder above it makes both ways of using this file work:
    # `python3 examples/src/example/e13_embedded_tk.py` and
    # `from example import e13_embedded_tk` from a test.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    main()
