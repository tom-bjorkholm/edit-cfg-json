#! /usr/bin/env python3
"""Tests for example e01_flat_config."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
import asyncio
import tkinter
import pytest
from textual.app import App
from example import e01_flat_config

EXPECTED_DUMP = 'name = flat example\nanswer = 42'
"""Text that `--ui dump` is expected to print for the default values."""


def test_dump(capsys: pytest.CaptureFixture[str]) -> None:
    """Test --ui dump prints both members with their default values."""
    e01_flat_config.main(['--ui', 'dump'])
    assert capsys.readouterr().out.strip() == EXPECTED_DUMP


def test_ui_is_required(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the example refuses to run without a selected user interface."""
    with pytest.raises(SystemExit) as exit_info:
        e01_flat_config.main([])
    assert exit_info.value.code == 2
    assert '--ui' in capsys.readouterr().err


def test_unknown_ui(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the example refuses a user interface it does not have."""
    with pytest.raises(SystemExit) as exit_info:
        e01_flat_config.main(['--ui', 'curses'])
    assert exit_info.value.code == 2
    assert 'curses' in capsys.readouterr().err


@pytest.mark.parametrize('option', ['-i', '--input', '-o', '--output'])
def test_files_refused(option: str,
                       capsys: pytest.CaptureFixture[str]) -> None:
    """Test the file options are refused until a later step implements them."""
    with pytest.raises(SystemExit) as exit_info:
        e01_flat_config.main(['--ui', 'dump', option, 'some.json'])
    assert exit_info.value.code == 2
    assert 'not supported yet' in capsys.readouterr().err


def _close_window(window: tkinter.Tk) -> None:
    """Stand in for Tk.mainloop by closing the window immediately."""
    window.destroy()


def test_tk_ui_opens(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui tk builds the window and returns when it is closed."""
    monkeypatch.setattr(tkinter.Tk, 'mainloop', _close_window)
    try:
        e01_flat_config.main(['--ui', 'tk'])
    except tkinter.TclError:
        pytest.skip('No display available for Tk.')


async def _quit_at_once(app: App[None]) -> None:
    """Start one Textual application headlessly and press its quit key."""
    async with app.run_test() as pilot:
        await pilot.press('q')


def _headless_run(titles: list[str]) -> Callable[[App[None]], None]:
    """Return a replacement for App.run that runs the application headlessly.

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


def test_textual_ui_opens(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui textual starts the application named after the class."""
    titles: list[str] = []
    monkeypatch.setattr(App, 'run', _headless_run(titles))
    e01_flat_config.main(['--ui', 'textual'])
    assert titles == ['FlatConfig']
