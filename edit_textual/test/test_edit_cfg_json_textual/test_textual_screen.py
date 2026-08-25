#! /usr/bin/env python3
"""Tests for the editor as a screen, and for the palette entries it offers.

A widget cannot offer entries in the command palette at all, which is the whole
reason the screen exists beside the panel. So what is tested here is the
provider: what it offers before anything is typed, what it offers for what is
typed, and what it offers on a screen that holds no editor, which is a screen
somebody pushed this provider onto by mistake.

The provider is asked directly rather than through the palette, because that is
exactly what the palette does with it, and because a test that typed into the
palette would be testing Textual's own matching.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
import asyncio
from textual.app import App, ComposeResult
from textual.command import Provider
from textual.widgets import Label
from edit_cfg_json import EditModel
from edit_cfg_json_textual import EditorScreen
from edit_cfg_json_textual.textual_editor import EditorApp
from edit_cfg_json_textual.textual_screen import EditorCommands, ModelScreen
from edit_cfg_json_textual.textual_words import FOLD_COMMAND, VALIDATE_COMMAND
from example.e01_flat_config import FlatConfig
from example.e08_lists_and_dicts import ContainerConfig
from .helpers import ROOMY_SIZE

NO_MATCH = 'zzzz'
"""A query that no action of the editor is named anything like."""


class PlainApp(App[None]):
    """An application with no editor anywhere on its screen.

    It is what a palette provider of the editor must survive being put on: an
    application is free to name `EditorCommands` in the `COMMANDS` of a screen
    of its own, and such a screen holds no editor to ask.
    """

    def compose(self) -> ComposeResult:
        """Create the one label that is all this application shows."""
        yield Label('nothing to edit here')


class HostApp(App[None]):
    """An application that pushes the editor as a screen of its own.

    It has a screen of its own underneath, which is what makes the pop that
    ends the session visible: an editor that had gone without popping would
    leave an empty screen on top of this application's own.
    """

    def __init__(self) -> None:
        """Remember that nothing has been pushed and nothing has ended."""
        super().__init__()
        self.editor: Optional[EditorScreen] = None

    def compose(self) -> ComposeResult:
        """Create the one label of this application's own screen."""
        yield Label('the application')

    def on_mount(self) -> None:
        """Push the editor, telling it nothing about what closing does."""
        self.editor = EditorScreen(FlatConfig())
        self.push_screen(self.editor)


async def _offered(provider: Provider) -> list[str]:
    """Return the name of every action one provider offers unasked."""
    return [str(hit.text) async for hit in provider.discover()]


async def _matched(provider: Provider, query: str) -> list[str]:
    """Return the name of every action one provider offers for one query."""
    return [str(hit.text) async for hit in provider.search(query)]


def test_every_action_offered() -> None:
    """Test the palette is offered one entry per action of the editor.

    Every terminal can reach the palette, so it is what a terminal that cannot
    tell two key combinations apart is left with, and an entry per action is
    what that needs.
    """
    async def discovered() -> list[str]:
        """Run the editor and ask its provider what it offers unasked."""
        app = EditorApp(EditModel(FlatConfig()))
        async with app.run_test(size=ROOMY_SIZE):
            provider = EditorCommands(app.screen)
            return await _offered(provider)
    names = asyncio.run(discovered())
    assert VALIDATE_COMMAND in names
    assert len(names) == len(set(names))


def test_folding_is_offered() -> None:
    """Test the entry that folds is there for a configuration that can fold.

    A configuration with nothing to fold gets no entry for it, because an
    entry that could do nothing is one more thing to read past. So the two
    configurations differ by exactly that entry.
    """
    async def offered(config: object) -> list[str]:
        """Run the editor on one configuration and read what it offers."""
        assert isinstance(config, (FlatConfig, ContainerConfig))
        app = EditorApp(EditModel(config))
        async with app.run_test(size=ROOMY_SIZE):
            return await _offered(EditorCommands(app.screen))
    with_folding = asyncio.run(offered(ContainerConfig()))
    without = asyncio.run(offered(FlatConfig()))
    assert FOLD_COMMAND in with_folding
    assert FOLD_COMMAND not in without
    assert len(with_folding) == len(without) + 1


def test_typed_query_matches() -> None:
    """Test what is typed into the palette is what decides what it offers.

    An action whose name the matcher scores at nothing is left out, which is
    what makes the palette worth typing into at all.
    """
    async def searched(query: str) -> list[str]:
        """Run the editor and ask its provider about one query."""
        app = EditorApp(EditModel(FlatConfig()))
        async with app.run_test(size=ROOMY_SIZE):
            provider = EditorCommands(app.screen)
            return await _matched(provider, query)
    matched = asyncio.run(searched(VALIDATE_COMMAND))
    assert matched == [VALIDATE_COMMAND]
    assert asyncio.run(searched(NO_MATCH)) == []


def test_no_editor_offers() -> None:
    """Test a screen that holds no editor offers no entry of one.

    That is a screen this provider was put on by mistake, and saying nothing
    is the only honest answer: there is no editor there to run an action of.
    """
    async def asked() -> tuple[list[str], list[str]]:
        """Run an application with no editor and ask the provider twice."""
        app = PlainApp()
        async with app.run_test(size=ROOMY_SIZE):
            provider = EditorCommands(app.screen)
            return (await _offered(provider),
                    await _matched(provider, VALIDATE_COMMAND))
    assert asyncio.run(asked()) == ([], [])


def test_screen_holds_model() -> None:
    """Test the screen answers with the model of the session it is showing.

    An application that reads what the session did asks the screen, and the
    model is what says which rows there are and what has not been saved.
    """
    async def shown() -> str:
        """Run the editor and ask its screen for the model."""
        model = EditModel(FlatConfig())
        app = EditorApp(model)
        async with app.run_test(size=ROOMY_SIZE):
            screen = app.screen
            assert isinstance(screen, ModelScreen)
            assert screen.model is model
            return screen.model.config_type_name
    assert asyncio.run(shown()) == 'FlatConfig'


def test_closing_no_callback() -> None:
    """Test a screen told nothing about closing still takes itself off.

    Popping the screen is the screen's own to do, because it is what the
    editor was mounted as, and an application that reads `saved_config`
    afterwards has no callback to give. So the screen goes and nothing else
    happens.
    """
    async def closed() -> tuple[int, Optional[object]]:
        """Push the editor, close it, and see what the application is left."""
        app = HostApp()
        async with app.run_test(size=ROOMY_SIZE) as pilot:
            await pilot.pause()
            assert app.editor is not None
            editor = app.editor
            assert len(app.screen_stack) == 2
            editor.close(ask_about_unsaved=False)
            await pilot.pause()
            return len(app.screen_stack), editor.saved_config
    assert asyncio.run(closed()) == (1, None)
