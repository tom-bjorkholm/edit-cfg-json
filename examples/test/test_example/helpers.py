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

from collections.abc import Callable
from pathlib import Path
import asyncio
import tkinter
from config_as_json import Config
import pytest
from textual.app import App
from edit_cfg_json import ActionSettings, EditModel

QUIT_KEY = ActionSettings().quit[0]
"""Key that ends the Textual editor for an application with no opinion.

It is read from the settings rather than written here, so that a default
that moves moves these tests with it.
"""

NO_DISPLAY = 'No display available for Tk.'
"""Why a test is skipped on a machine that cannot open a window."""

DATA_FOLDER = Path(__file__).resolve().parents[2] / 'data'
"""Folder holding the input files that the examples are run against.

The path is derived from this file rather than from the working folder, so
that the tests can be run from anywhere.
"""

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


def saved_tail(out_file: Path, class_name: str) -> str:
    """Return the two lines that a dump which wrote a file ends with.

    Args:
        out_file: File that the run was asked to write.
        class_name: Name of the configuration class of the example.

    Returns:
        What the run says about the save and about what `edit()` gave back.
    """
    return (f'Saved to {out_file}.\n'
            f'edit() returned the saved {class_name} object.')


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


def _close_window(window: tkinter.Tk) -> None:
    """Stand in for Tk.mainloop by closing the window immediately."""
    window.destroy()


def open_tk_ui(main: Callable[[list[str]], None],
               monkeypatch: pytest.MonkeyPatch, *settings: str) -> None:
    """Run one example with `--ui tk` and close its window at once.

    Args:
        main: The `main` function of the example to run.
        monkeypatch: The pytest fixture that replaces `Tk.mainloop`.
        settings: Further command line arguments, such as an input file.
    """
    monkeypatch.setattr(tkinter.Tk, 'mainloop', _close_window)
    try:
        main(['--ui', 'tk', *settings])
    except tkinter.TclError:
        pytest.skip(NO_DISPLAY)


async def _quit_at_once(app: App[None], quit_key: str) -> None:
    """Start one Textual application headlessly and press its quit key."""
    async with app.run_test() as pilot:
        await pilot.press(quit_key)


def _headless_run(titles: list[str],
                  quit_key: str) -> Callable[[App[None]], None]:
    """Return a replacement for App.run that runs it headlessly.

    Args:
        titles: List that receives the title of every started application.
        quit_key: Key that the stand-in user presses to end the editor.

    Returns:
        A function that can replace `App.run` for the duration of a test.
    """
    def run_headless(app: App[None]) -> None:
        """Record the title, start the application and quit it at once."""
        titles.append(app.title)
        asyncio.run(_quit_at_once(app, quit_key))
    return run_headless


def textual_titles(main: Callable[[list[str]], None],
                   monkeypatch: pytest.MonkeyPatch, *settings: str,
                   quit_key: str = QUIT_KEY) -> list[str]:
    """Run one example with `--ui textual` headlessly and report its title.

    The title is what the editor shows for the whole model, so it also says
    whether the buffer holds anything worth saving. That makes it enough to
    tell that the application started and that it started on the buffer the
    command line asked for.

    Args:
        main: The `main` function of the example to run.
        monkeypatch: The pytest fixture that replaces `App.run`.
        settings: Further command line arguments, usually `--set` pairs.
        quit_key: Key that ends the editor, for a run that moved it.

    Returns:
        The title of every application that was started.
    """
    titles: list[str] = []
    monkeypatch.setattr(App, 'run', _headless_run(titles, quit_key))
    main(['--ui', 'textual', *settings])
    return titles
