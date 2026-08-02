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
import pytest
from textual.app import App

QUIT_KEY = 'ctrl+q'
"""Key that ends the Textual editor. A letter belongs to a field."""

NO_DISPLAY = 'No display available for Tk.'
"""Why a test is skipped on a machine that cannot open a window."""

DATA_FOLDER = Path(__file__).resolve().parents[2] / 'data'
"""Folder holding the input files that the examples are run against.

The path is derived from this file rather than from the working folder, so
that the tests can be run from anywhere.
"""


def data_file(name: str) -> str:
    """Return the path of one input file of the examples.

    Args:
        name: File name inside the data folder of the examples.

    Returns:
        The path of that file, as the command line takes it.
    """
    return str(DATA_FOLDER / name)


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


async def _quit_at_once(app: App[None]) -> None:
    """Start one Textual application headlessly and press its quit key."""
    async with app.run_test() as pilot:
        await pilot.press(QUIT_KEY)


def _headless_run(titles: list[str]) -> Callable[[App[None]], None]:
    """Return a replacement for App.run that runs it headlessly.

    Args:
        titles: List that receives the title of every started application.

    Returns:
        A function that can replace `App.run` for the duration of a test.
    """
    def run_headless(app: App[None]) -> None:
        """Record the title, start the application and quit it at once."""
        titles.append(app.title)
        asyncio.run(_quit_at_once(app))
    return run_headless


def textual_titles(main: Callable[[list[str]], None],
                   monkeypatch: pytest.MonkeyPatch,
                   *settings: str) -> list[str]:
    """Run one example with `--ui textual` headlessly and report its title.

    The title is what the editor shows for the whole model, so it also says
    whether the buffer holds anything worth saving. That makes it enough to
    tell that the application started and that it started on the buffer the
    command line asked for.

    Args:
        main: The `main` function of the example to run.
        monkeypatch: The pytest fixture that replaces `App.run`.
        settings: Further command line arguments, usually `--set` pairs.

    Returns:
        The title of every application that was started.
    """
    titles: list[str] = []
    monkeypatch.setattr(App, 'run', _headless_run(titles))
    main(['--ui', 'textual', *settings])
    return titles
