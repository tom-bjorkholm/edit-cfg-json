#! /usr/bin/env python3
"""Tests for the editor mounted in an application that already runs Textual.

What these are about is what makes an embedded editor different from one that
owns the terminal: it is a widget, so its keys are offered from the widget
that has the focus upwards and reach the editor and nothing else; it takes
only itself off the screen; and the application is told when the session has
ended. Everything else about the editor is the same editor and is tested
where it always was.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import ClassVar, Optional
import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Input, Label, Static
from config_as_json import Config
from edit_cfg_json import ActionSettings, Settings
from edit_cfg_json_textual import EditorPanel, EditorScreen
from edit_cfg_json_textual.textual_look import DOCSTRING_ID, TITLE_ID, \
    value_id
from example.e01_flat_config import FlatConfig

OWN_FIELD_ID = 'own_field'
"""Identifier of the field that the host application has of its own."""

OWN_KEY = 'ctrl+e'
"""A key that Textual's own field reads for itself.

It is what tells the two answers of `edit_cfg_json.Settings.priority_keys`
apart: with a priority binding the editor is offered the key before the field
that has the focus, and without one the field takes it.
"""

FIELD_KEYS = Settings(actions=ActionSettings(explain=(OWN_KEY,)))
"""Settings giving the editor a key that its own field claims."""

ORDINARY_KEYS = Settings(actions=ActionSettings(explain=(OWN_KEY,)),
                         priority_keys=False)
"""The same keys, offered to the field that has the focus first."""

APP_SIZE = (100, 40)
"""Terminal size with room for the host application and the editor."""


class HostApp(App[None]):
    """An application of its own that mounts the editor in one area.

    It has a field of its own above the editor, which is what gives these
    tests somewhere to put the focus that is not inside the editor.
    """

    def __init__(self, config: Config, as_screen: bool = False,
                 settings: Settings = Settings()) -> None:
        """Remember the configuration and how the editor is to be mounted.

        Args:
            config: Configuration for the editor to read and show.
            as_screen: Whether the editor is pushed as a screen of its own
                rather than mounted in an area of this application's screen.
            settings: What this application decided about the editor.
        """
        super().__init__()
        self.ended: list[str] = []
        self._config = config
        self._settings = settings
        self._as_screen = as_screen
        self.panel: Optional[EditorPanel] = None
        self.editor: Optional[EditorScreen] = None

    def compose(self) -> ComposeResult:
        """Create this application's own widgets, and maybe the editor."""
        yield Label('the application')
        yield Input(id=OWN_FIELD_ID)
        if not self._as_screen:
            self.panel = EditorPanel(self._config, settings=self._settings,
                                     on_close=self._gone)
            yield self.panel

    def on_mount(self) -> None:
        """Push the editor as a screen, for the run that asked for one."""
        if self._as_screen:
            self.editor = EditorScreen(self._config, settings=self._settings,
                                       on_close=self._gone)
            self.push_screen(self.editor)

    def _gone(self) -> None:
        """Record that the editor said the session had ended."""
        self.ended.append('gone')


async def _started(config: Config,
                   as_screen: bool = False) -> tuple[HostApp, str]:
    """Run one host application and read the label of the editor in it.

    Args:
        config: Configuration for the editor to read and show.
        as_screen: Whether the editor is pushed as a screen of its own.

    Returns:
        The application, and the label the editor shows for the model.
    """
    app = HostApp(config, as_screen=as_screen)
    async with app.run_test(size=APP_SIZE) as pilot:
        await pilot.pause()
        return app, str(app.screen.query_one(f'#{TITLE_ID}', Static).content)


def test_panel_shows_model() -> None:
    """Test an application that mounts the editor gets the whole editor."""
    _, label = asyncio.run(_started(FlatConfig()))
    assert label == 'FlatConfig'


def test_screen_shows_model() -> None:
    """Test the same editor pushed as a screen shows the same thing."""
    _, label = asyncio.run(_started(FlatConfig(), as_screen=True))
    assert label == 'FlatConfig'


def test_screen_palette() -> None:
    """Test a pushed editor offers its actions in the command palette.

    A widget cannot offer palette entries at all, which is why the screen
    exists beside the panel, and an application that pushed the screen has a
    palette of its own that it never had to be told about these.
    """
    async def offered() -> list[str]:
        """Run a host application and read what the editor screen offers."""
        app, _ = await _started(FlatConfig(), as_screen=True)
        assert app.editor is not None
        return [entry.name for entry in app.editor.panel.command_entries()]
    assert 'Validate' in asyncio.run(offered())


async def _explained_after(settings: Settings) -> bool:
    """Run a host application and press a key inside a field of the editor.

    Args:
        settings: What the application decided about the keys of the editor.

    Returns:
        Whether pressing that key changed what the editor says about the
        configuration class, which is what its explain action does.
    """
    app = HostApp(FlatConfig(), settings=settings)
    async with app.run_test(size=APP_SIZE) as pilot:
        app.screen.query_one(f'#{value_id(0)}', Input).focus()
        await pilot.pause()
        docstring = app.screen.query_one(f'#{DOCSTRING_ID}', Static)
        before = str(docstring.content)
        await pilot.press(OWN_KEY)
        await pilot.pause()
        return str(docstring.content) != before


def test_priority_key_wins() -> None:
    """Test the editor is offered its key before the field that has focus."""
    assert asyncio.run(_explained_after(FIELD_KEYS))


def test_ordinary_key_lost() -> None:
    """Test an application can give the focused widget the key first.

    That is the whole of what `priority_keys` says, and the field of Textual
    reading this combination for itself is what makes it visible.
    """
    assert not asyncio.run(_explained_after(ORDINARY_KEYS))


async def _key_outside(settings: Settings) -> bool:
    """Press a key of the editor with the focus in the application's field.

    Args:
        settings: What the application decided about the keys of the editor.

    Returns:
        Whether the editor acted on the key, which it must not.
    """
    app = HostApp(FlatConfig(), settings=settings)
    async with app.run_test(size=APP_SIZE) as pilot:
        app.query_one(f'#{OWN_FIELD_ID}', Input).focus()
        await pilot.pause()
        docstring = app.screen.query_one(f'#{DOCSTRING_ID}', Static)
        before = str(docstring.content)
        await pilot.press(OWN_KEY)
        await pilot.pause()
        return str(docstring.content) != before


def test_keys_scoped() -> None:
    """Test a key pressed outside the editor never reaches the editor.

    Textual offers a key from the widget that has the focus upwards, so the
    editor being a widget is the whole of what keeps it out of the rest of an
    application's window. A priority binding is what would be most likely to
    escape, so that is the one this presses.
    """
    assert not asyncio.run(_key_outside(FIELD_KEYS))


async def _closed(as_screen: bool, asking: bool,
                  typed: str = '') -> tuple[HostApp, int]:
    """Run a host application, maybe edit something, and close the editor.

    Args:
        as_screen: Whether the editor is pushed as a screen of its own.
        asking: Whether closing asks about what has not been saved.
        typed: Text to put into a field of the editor first, empty for a
            buffer that holds nothing worth saving.

    Returns:
        The application, and how many editors are left on the screen.
    """
    app = HostApp(FlatConfig(), as_screen=as_screen)
    async with app.run_test(size=APP_SIZE) as pilot:
        await pilot.pause()
        if typed:
            app.screen.query_one(f'#{value_id(0)}', Input).value = typed
            await pilot.pause()
        editor = app.editor or app.panel
        assert editor is not None
        editor.close(ask_about_unsaved=asking)
        await pilot.pause()
        return app, len(app.query(EditorPanel))


def test_panel_closes() -> None:
    """Test closing takes the editor off the screen and says so."""
    app, left = asyncio.run(_closed(as_screen=False, asking=True))
    assert app.ended == ['gone']
    assert not left


def test_screen_closes() -> None:
    """Test the same is true of an editor that was pushed as a screen."""
    app, _ = asyncio.run(_closed(as_screen=True, asking=True))
    assert app.ended == ['gone']


def test_close_asks_first() -> None:
    """Test a buffer holding something unsaved is asked about first.

    The editor is still there while the question is open, which is what the
    question is for: the answer that keeps the changes has to be able to keep
    them.
    """
    app, left = asyncio.run(_closed(as_screen=False, asking=True, typed='7'))
    assert not app.ended
    assert left == 1


def test_close_without_asking() -> None:
    """Test the application can close the editor without a question.

    An application that is shutting down for reasons of its own already has a
    question to put to the user, and a library that put a second one there
    would be deciding something that is the application's.
    """
    app, left = asyncio.run(_closed(as_screen=False, asking=False, typed='7'))
    assert app.ended == ['gone']
    assert not left


def test_close_twice_is_once() -> None:
    """Test closing an editor whose session has ended does nothing at all."""
    async def twice() -> list[str]:
        """Run a host application and close its editor twice."""
        app = HostApp(FlatConfig())
        async with app.run_test(size=APP_SIZE) as pilot:
            assert app.panel is not None
            app.panel.close()
            await pilot.pause()
            app.panel.close()
            await pilot.pause()
            return app.ended
    assert asyncio.run(twice()) == ['gone']


class SilentHost(App[None]):
    """A host application that says nothing about the session ending.

    `on_close` is optional, because an application may read the outcome from
    the model whenever it likes, and an editor that needed the callback would
    be making it required.
    """

    CSS: ClassVar[str] = ''
    """Nothing at all, which is what this test is about: the editor brings
    its own."""

    def __init__(self, config: Config) -> None:
        """Remember the configuration this application shows."""
        super().__init__()
        self._config = config

    def compose(self) -> ComposeResult:
        """Create the editor and nothing else."""
        yield EditorPanel(self._config)


def test_panel_no_callback() -> None:
    """Test an editor mounted without an `on_close` closes just the same."""
    async def closed() -> int:
        """Run the silent application and close the editor in it."""
        app = SilentHost(FlatConfig())
        async with app.run_test(size=APP_SIZE) as pilot:
            app.query_one(EditorPanel).close()
            await pilot.pause()
            return len(app.query(EditorPanel))
    assert not asyncio.run(closed())


def test_panel_styles_itself() -> None:
    """Test the editor brings its own style sheet wherever it is mounted.

    A widget declares the sheet of itself and of what is inside it, so an
    application that never heard of this editor still gets rows one cell high
    and a body that scrolls.
    """
    async def heights() -> tuple[object, object]:
        """Run the silent application and read two heights of the editor."""
        app = SilentHost(FlatConfig())
        async with app.run_test(size=APP_SIZE):
            panel = app.query_one(EditorPanel)
            return panel.styles.height, panel.query_one('#body').styles.height
    panel_height, body_height = asyncio.run(heights())
    assert str(panel_height) == '1fr'
    assert str(body_height) == '1fr'
