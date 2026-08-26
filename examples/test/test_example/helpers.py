#! /usr/bin/env python3
"""Ways of running an example program that its tests share.

Every example has the same command line, because they all hand their
configuration object to the same `run_example`. So every example is tested
the same four ways: dump it, refuse it, open it in Tk, open it in Textual.
Those four live here rather than in each test module, so that one example
more does not mean one more copy of them.

An example is passed in as its `main` function rather than as a module, so
that these helpers need to know nothing at all about which example they are
running.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Optional
import asyncio
import json
import tkinter
from config_as_json import Config
import pytest
from textual.app import App
from textual.pilot import Pilot
from textual.widgets import Button, Input, Label, Static
from edit_cfg_json import ActionSettings, EditModel
# The identifier of the label is taken from the backend rather than written
# out here, in the same way as every widget identifier a test of that backend
# reaches for. What the label says is the core's `model_title`, which is what
# these tests are really about.
from edit_cfg_json_textual.textual_look import DOCSTRING_ID, TITLE_ID, \
    value_id

SAVE_KEY = ActionSettings().save[0]
"""Key that saves in the editor for an application with no opinion."""

QUIT_KEY = ActionSettings().quit[0]
"""Key that ends the Textual editor for an application with no opinion.

It is read from the settings rather than written here, so that a default
that moves moves these tests with it.
"""

NO_DISPLAY = 'No display available for Tk.'
"""Why a test is skipped on a machine that cannot open a window."""

EDITOR_SIZE = (100, 40)
"""Terminal size with room for an application and the editor together."""

PIPELINE_FILE = 'e13_pipeline.json'
"""Input file that the six examples of opening the editor share."""

SAVED_PIPELINE = {'name': 'release-candidate', 'workers': 8}
"""What a save of that file unchanged writes, as JSON reads it back.

Every example that opens the editor on `PIPELINE_FILE` and saves it writes
these two members, so the expectation is here rather than in each test module.
"""

DATA_FOLDER = Path(__file__).resolve().parents[2] / 'data'
"""Folder holding the input files that the examples are run against.

The path is derived from this file rather than from the working folder, so
that the tests can be run from anywhere.
"""

TEXT_LINE = '    Text.'
"""What a dump says under a member that holds text.

The editor says what kind of value every member holds, because that is the one
thing it knows about every member of every configuration without being told
anything at all. It is written out here rather than read from the core, in the
same way that the names of an enum are written out where a test expects them.
"""

WHOLE_LINE = '    A whole number.'
"""What a dump says under a member that holds a whole number."""

NUMBER_LINE = '    A number.'
"""What a dump says under a member that holds a number with a fraction."""

NO_DESTINATION = 'save to: no file chosen yet'
"""What a dump says when no output file was named on the command line."""

NOTHING_SAVED = 'edit() returned None, so nothing was saved.'
"""What a run says when the session ended without writing anything."""

DUMP_TAIL = f'{NO_DESTINATION}\n{NOTHING_SAVED}'
"""The two lines that every dump without an output file ends with.

Every example run ends by saying where it would save and what `edit()` gave
back, because both are part of the contract of the library and a contract is
better seen than read. The two lines are here rather than in each test
module, so that one example more does not mean one more copy of them.
"""


def head(config: Config, edited: bool = False) -> str:
    """Return the lines that a dump of one configuration begins with.

    A dump begins by labelling the configuration object: the name of its
    class, marked while there is something worth saving, and then the
    docstring of that class. The docstring is read from the model rather than
    written out in each test module, because what a docstring becomes is
    decided in the core and tested there. What these tests are about is that
    the examples are shown with the one they have.

    Args:
        config: Configuration object of the example, which is what says both
            what the class is called and what it says about itself.
        edited: Whether the buffer holds something worth saving, which the
            label of the configuration is marked while it does.

    Returns:
        The first lines of a dump of that configuration.
    """
    model = EditModel(config)
    mark = ' *' if edited else ''
    lines = [f'{type(config).__name__}{mark}', model.docstring]
    return '\n'.join(line for line in lines if line)


def saved_tail(out_file: Path, class_name: str,
               kept: Optional[Path] = None) -> str:
    """Return the lines that a dump which wrote a file ends with.

    Args:
        out_file: File that the run was asked to write.
        class_name: Name of the configuration class of the example.
        kept: File that what the destination held was kept as, or None where
            the destination held nothing to keep. A save says so, because a
            user whose file has been moved has to be told where it went.

    Returns:
        What the run says about the save and about what `edit()` gave back.
    """
    lines = [f'Saved to {out_file}.']
    if kept is not None:
        lines.append(f'The previous content is in {kept}.')
    lines.append(f'edit() returned the saved {class_name} object.')
    return '\n'.join(lines)


def data_file(name: str) -> str:
    """Return the path of one input file of the examples.

    Args:
        name: File name inside the data folder of the examples.

    Returns:
        The path of that file, as the command line takes it.
    """
    return str(DATA_FOLDER / name)


def input_tail(name: str) -> str:
    """Return the two lines a dump ends with when only `-i` was given.

    The input file is what a save writes when no output file was named, which
    is what an editor is normally asked to do.

    Args:
        name: File name inside the data folder of the examples.

    Returns:
        What the run says about the save and about what `edit()` gave back.
    """
    return f'save to: {data_file(name)}\n{NOTHING_SAVED}'


def dump(main: Callable[[list[str]], None], capsys: pytest.CaptureFixture[str],
         *settings: str) -> str:
    """Run one example with `--ui dump` and return what it printed.

    Args:
        main: The `main` function of the example to run.
        capsys: The pytest fixture that captured the output.
        settings: Further command line arguments, usually `--set` pairs.

    Returns:
        What the example printed, without surrounding blank space.
    """
    main(['--ui', 'dump', *settings])
    return capsys.readouterr().out.strip()


def refused(main: Callable[[list[str]], None],
            capsys: pytest.CaptureFixture[str], *arguments: str) -> str:
    """Run one example, expect it to refuse, and return its error text.

    Args:
        main: The `main` function of the example to run.
        capsys: The pytest fixture that captured the output.
        arguments: The whole command line the example is given.

    Returns:
        What the example wrote to its error stream.
    """
    with pytest.raises(SystemExit) as exit_info:
        main(list(arguments))
    assert exit_info.value.code == 2
    return capsys.readouterr().err


def _acting_loop(acting: Optional[Callable[[tkinter.Tk], None]]
                 ) -> Callable[[tkinter.Tk], None]:
    """Return a replacement for Tk.mainloop that acts once and closes.

    The window is withdrawn first, so that a test suite does not put windows
    on the screen of whoever runs it, and realized with `update_idletasks`, so
    that the widgets in it can be found and pressed.

    Args:
        acting: What is done to the window, standing in for the user, or None
            for a run that only opens it.

    Returns:
        A function that can replace `Tk.mainloop` for the duration of a test.
    """
    def instead(window: tkinter.Tk) -> None:
        """Act on the window once instead of waiting for the user."""
        window.withdraw()
        window.update_idletasks()
        try:
            if acting is not None:
                acting(window)
        finally:
            window.destroy()
    return instead


def open_tk_editor(main: Callable[[list[str]], None],
                   monkeypatch: pytest.MonkeyPatch, *settings: str,
                   acting: Optional[Callable[[tkinter.Tk], None]] = None
                   ) -> None:
    """Run one example whose editor owns the window, and act on it once.

    Such an example runs no `Tk.mainloop` of its own: the editor creates the
    window and runs the loop, so replacing that loop is what stands in for the
    user of the editor itself.

    Args:
        main: The `main` function of the example to run.
        monkeypatch: The pytest fixture that replaces `Tk.mainloop`.
        settings: The whole command line the example is given.
        acting: What is done to the editor's window before it is closed, or
            None for a run that only opens it.
    """
    monkeypatch.setattr(tkinter.Tk, 'mainloop', _acting_loop(acting))
    try:
        main(list(settings))
    except tkinter.TclError:
        pytest.skip(NO_DISPLAY)


def open_tk_ui(main: Callable[[list[str]], None],
               monkeypatch: pytest.MonkeyPatch, *settings: str) -> None:
    """Run one example with `--ui tk` and close its window at once.

    Args:
        main: The `main` function of the example to run.
        monkeypatch: The pytest fixture that replaces `Tk.mainloop`.
        settings: Further command line arguments, such as an input file.
    """
    open_tk_editor(main, monkeypatch, '--ui', 'tk', *settings)


async def _pressed(app: App[None], titles: list[str],
                   keys: tuple[str, ...]) -> None:
    """Start one Textual application headlessly and press keys in it.

    The label is read while the application is running, because it is a widget
    of the editor and not the title of the application: an editor that an
    application mounts in a window of its own has no business writing there.
    """
    async with app.run_test() as pilot:
        titles.append(str(app.query_one(f'#{TITLE_ID}', Static).content))
        for key in keys:
            await pilot.press(key)


def _headless_run(titles: list[str],
                  keys: tuple[str, ...]) -> Callable[[App[None]], None]:
    """Return a replacement for App.run that runs it headlessly.

    Args:
        titles: List that receives the label of every started editor.
        keys: Keys that the stand-in user presses, ending with one that ends
            the editor.

    Returns:
        A function that can replace `App.run` for the duration of a test.
    """
    def run_headless(app: App[None]) -> None:
        """Start the application, read its label and press those keys."""
        asyncio.run(_pressed(app, titles=titles, keys=keys))
    return run_headless


def tk_buttons(parent: tkinter.Misc) -> list[tkinter.Button]:
    """Return every Tk button below one widget, in creation order.

    Args:
        parent: Widget whose descendants are looked through.

    Returns:
        Every button below that widget.
    """
    found: list[tkinter.Button] = []
    for child in parent.winfo_children():
        if isinstance(child, tkinter.Button):
            found.append(child)
        found.extend(tk_buttons(child))
    return found


def tk_fields(parent: tkinter.Misc) -> list[tkinter.Entry]:
    """Return every Tk edit field below one widget, in creation order.

    Args:
        parent: Widget whose descendants are looked through.

    Returns:
        Every edit field below that widget.
    """
    found: list[tkinter.Entry] = []
    for child in parent.winfo_children():
        if isinstance(child, tkinter.Entry):
            found.append(child)
        found.extend(tk_fields(child))
    return found


def tk_press(parent: tkinter.Misc, text: str) -> None:
    """Press the one button below one widget that shows the given text.

    Args:
        parent: Widget whose descendants are looked through.
        text: What the button to press says.
    """
    buttons = [button for button in tk_buttons(parent)
               if str(button.cget('text')) == text]
    assert len(buttons) == 1
    buttons[0].invoke()


def _no_grab(widget: tkinter.Misc) -> None:
    """Stand in for taking or giving back the events of the application.

    Args:
        widget: Widget that asked for the grab, which is left alone.
    """
    _ = widget


def run_tk_example(main: Callable[[list[str]], None],
                   monkeypatch: pytest.MonkeyPatch,
                   acting: Callable[[tkinter.Tk], None],
                   *settings: str) -> None:
    """Run one embedding example and act on its window instead of looping.

    The examples that mount the editor have no `--ui dump`, and cannot have
    one: what they teach is where the editor is in a window, and a printout
    has no window to be one part of. So this runs the real application, with
    `Tk.mainloop` replaced by what a user would do next, which is category 2
    of design section 10.2 and skips where there is no display.

    A modal editor is asked for by two of these examples, and a real grab is
    taken away from it here: a test that grabbed the pointer and the keyboard
    would hold the machine it runs on, and a grab left behind by a window the
    test then destroys hangs whatever runs next. That the editor asks for the
    grab is tested with a stub, where it costs nothing.

    Args:
        main: The `main` function of the example to run.
        monkeypatch: The pytest fixture that replaces `Tk.mainloop`.
        acting: What is done to the window of the application, standing in
            for the user of it.
        settings: Command line arguments of the run.
    """
    monkeypatch.setattr(tkinter.Misc, 'grab_set', _no_grab)
    monkeypatch.setattr(tkinter.Misc, 'grab_release', _no_grab)
    monkeypatch.setattr(tkinter.Tk, 'mainloop', _acting_loop(acting))
    try:
        main(list(settings))
    except tkinter.TclError:
        pytest.skip(NO_DISPLAY)


def run_textual_app(main: Callable[[list[str]], None],
                    monkeypatch: pytest.MonkeyPatch,
                    driving: Callable[[App[None], Pilot[None]],
                                      Awaitable[None]],
                    *settings: str) -> None:
    """Run one embedding example headlessly and drive the application.

    `App.run` is replaced rather than the application being built here, so
    that what is driven is what the example's own `main` puts together.

    Args:
        main: The `main` function of the example to run.
        monkeypatch: The pytest fixture that replaces `App.run`.
        driving: What to do with the application once it is running.
        settings: Command line arguments of the run.
    """
    async def started(app: App[None]) -> None:
        """Run one application headlessly and drive it."""
        async with app.run_test(size=EDITOR_SIZE) as pilot:
            await pilot.pause()
            await driving(app, pilot)

    def run_headless(app: App[None]) -> None:
        """Stand in for App.run by running the application headlessly."""
        asyncio.run(started(app))
    monkeypatch.setattr(App, 'run', run_headless)
    main(list(settings))


async def press_own_button(app: App[None], pilot: Pilot[None],
                           text: str) -> None:
    """Press the one button of the application's own screen with that text.

    The application's own screen is looked at rather than the whole
    application, because an editor pushed as a screen has buttons of its own
    on top of it.

    Args:
        app: Application that is running.
        pilot: Driver of that application.
        text: What the button to press says.
    """
    buttons = [button for button in app.screen_stack[0].query(Button)
               if str(button.label) == text]
    assert len(buttons) == 1
    buttons[0].press()
    await pilot.pause()


def own_status(app: App[None]) -> str:
    """Return what the application says on its own status line.

    Args:
        app: Application that is running.

    Returns:
        The text of the first label of the application's own screen.
    """
    return str(app.screen_stack[0].query(Label).first().content)


def editor_title(app: App[None]) -> str:
    """Return the label that the editor shows for the whole model.

    Args:
        app: Application that is running, with an editor showing.

    Returns:
        What the editor calls the configuration it is editing.
    """
    return str(app.screen.query_one(f'#{TITLE_ID}', Static).content)


def editor_docstring(app: App[None]) -> str:
    """Return what the editor is showing of the class docstring.

    How much of it is shown is what the explain action changes, so this is
    what says whether a key explained anything.

    Args:
        app: Application that is running, with an editor showing.

    Returns:
        The whole docstring while the explanations are shown, and its first
        paragraph while they are hidden.
    """
    return str(app.screen.query_one(f'#{DOCSTRING_ID}', Static).content)


async def focus_editor(app: App[None], pilot: Pilot[None]) -> None:
    """Put the focus in the first field of the editor.

    The keys of the editor are offered from the focused widget upwards, so a
    test about one of them starts by getting the focus in there.

    Args:
        app: Application that is running, with an editor showing.
        pilot: Driver of that application.
    """
    app.screen.query_one(f'#{value_id(0)}', Input).focus()
    await pilot.pause()


async def edit_and_save(app: App[None], pilot: Pilot[None], text: str) -> None:
    """Type one value into the first field of the editor and save it.

    The focus is moved into the editor first, because the keys of the editor
    are offered from the focused widget upwards.

    Args:
        app: Application that is running, with an editor showing.
        pilot: Driver of that application.
        text: What to type into the first field of the editor.
    """
    await focus_editor(app, pilot)
    app.screen.query_one(f'#{value_id(0)}', Input).value = text
    await pilot.pause()
    await pilot.press(SAVE_KEY)
    await pilot.pause()


def saved_members(main: Callable[[list[str]], None],
                  capsys: pytest.CaptureFixture[str], out_file: Path,
                  class_name: str, *settings: str) -> dict[str, object]:
    """Run one example with `--ui dump`, save it, and return what it wrote.

    Two things are checked on the way, because both of them have to hold for
    the values to mean anything: the run said that it saved, and what it saved
    is a JSON object. What the test then asserts is the members themselves.

    Args:
        main: The `main` function of the example to run.
        capsys: The pytest fixture that captured the output.
        out_file: File to write, which the run is given with `-o`.
        class_name: Name of the configuration class of the example.
        settings: Further command line arguments, usually `--set` pairs.

    Returns:
        One JSON space value per member that reached the file.
    """
    printed = dump(main, capsys, *settings, '-o', str(out_file), '--save')
    assert printed.endswith(saved_tail(out_file, class_name))
    written = written_json(out_file)
    assert isinstance(written, dict)
    return written


def refusal_of(running: Callable[[], object]) -> str:
    """Run one example that must refuse, and return what it ended with.

    An example whose input file cannot be read ends the process rather than
    opening an editor on values the user did not ask for. What it ended with
    is the message, because that is what `sys.exit` is given.

    Args:
        running: The run that is expected to refuse. What it would have
            answered with is not looked at, and differs between the ways of
            running an example, which is what `object` says here.

    Returns:
        What the run ended with, as text.
    """
    with pytest.raises(SystemExit) as ended:
        running()
    return str(ended.value.code)


def written_json(out_file: Path) -> object:
    """Return what one output file holds, as JSON space values.

    Args:
        out_file: File that a run of an example wrote.

    Returns:
        The values in it, as JSON reads them.
    """
    return json.loads(out_file.read_text(encoding='UTF-8'))


def editor_titles(main: Callable[[list[str]], None],
                  monkeypatch: pytest.MonkeyPatch, *settings: str,
                  keys: tuple[str, ...] = (QUIT_KEY,)) -> list[str]:
    """Run one example whose editor owns the terminal, and read its label.

    Such an example runs no Textual application of its own: the editor runs
    one, so replacing `App.run` is what stands in for the user of the editor
    itself.

    Args:
        main: The `main` function of the example to run.
        monkeypatch: The pytest fixture that replaces `App.run`.
        settings: The whole command line the example is given.
        keys: Keys the stand-in user presses, ending with one that ends the
            editor.

    Returns:
        The label of every editor that was started.
    """
    titles: list[str] = []
    monkeypatch.setattr(App, 'run', _headless_run(titles, keys))
    main(list(settings))
    return titles


def textual_titles(main: Callable[[list[str]], None],
                   monkeypatch: pytest.MonkeyPatch, *settings: str,
                   quit_key: str = QUIT_KEY) -> list[str]:
    """Run one example with `--ui textual` headlessly and read its label.

    The label is what the editor shows for the whole model, so it also says
    whether the buffer holds anything worth saving. That makes it enough to
    tell that the editor started and that it started on the buffer the
    command line asked for.

    Args:
        main: The `main` function of the example to run.
        monkeypatch: The pytest fixture that replaces `App.run`.
        settings: Further command line arguments, usually `--set` pairs.
        quit_key: Key that ends the editor, for a run that moved it.

    Returns:
        The label of every editor that was started.
    """
    return editor_titles(main, monkeypatch, '--ui', 'textual', *settings,
                         keys=(quit_key,))
