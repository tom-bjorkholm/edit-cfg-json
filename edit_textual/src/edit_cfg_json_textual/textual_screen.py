#! /usr/bin/env python3
"""One editor as a screen of a Textual application.

A screen is what a widget cannot be: it has a header and a footer of its own,
and it can offer entries in the command palette, which `Screen.COMMANDS` is
for and which a widget has no equivalent of at all. So this is what an
application pushes when it wants the editor to take the whole terminal for a
while, and it is what `EditorApp` shows when the editor is the whole program.

An application that wants the editor in an area of its own screen mounts
`edit_cfg_json_textual.EditorPanel` instead and keeps its own header, its own
footer and its own palette. That is the difference between the two, and it is
the whole of it.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from typing import ClassVar, Optional
from config_as_json import Config
from textual.app import ComposeResult
from textual.command import DiscoveryHit, Hit, Hits, Provider
from textual.screen import Screen
from textual.widgets import Footer, Header
import edit_cfg_json as core
from edit_cfg_json_textual.textual_panel import ModelPanel
from edit_cfg_json_textual.textual_words import EditorCommand


class EditorCommands(Provider):
    """The actions of the editor, as the command palette offers them.

    It asks the panel of its screen rather than holding a table of its own,
    because the name of two of those actions says what the next press will do
    and is therefore only true at the moment it is read.
    """

    def _offered(self) -> tuple[EditorCommand, ...]:
        """Return what the editor of this screen offers as things stand.

        Returns:
            One entry per action, and none at all for a screen that holds no
            editor, which is what a palette provider of a screen this was
            put on by mistake should say.
        """
        screen = self.screen
        if not isinstance(screen, ModelScreen):
            return ()
        return screen.panel.command_entries()

    async def discover(self) -> Hits:
        """Offer every action of the editor before anything is typed.

        Yields:
            One hit per action the editor offers.
        """
        for entry in self._offered():
            yield DiscoveryHit(entry.name, entry.run, help=entry.help_text)

    async def search(self, query: str) -> Hits:
        """Offer the actions whose names match what the user is typing.

        Args:
            query: What the user has typed into the palette.

        Yields:
            One hit per action whose name matches, as the matcher of the
            palette scores it.
        """
        matcher = self.matcher(query)
        for entry in self._offered():
            score = matcher.match(entry.name)
            if score > 0:
                yield Hit(score, matcher.highlight(entry.name), entry.run,
                          help=entry.help_text)


class ModelScreen(Screen[None]):
    """A screen holding one editor, with a header and a footer of its own.

    It takes a model, which is what this package has of its own and what
    `EditorApp` shows. An application reads a configuration instead, with
    `edit_cfg_json_textual.EditorScreen`.
    """

    COMMANDS: ClassVar[set[type[Provider] | Callable[[], type[Provider]]]] = \
        {EditorCommands}
    """The actions of the editor, offered in the command palette.

    They are declared here and not on an application, because an application
    that pushed this screen has a palette of its own and would otherwise be
    made to name the actions of a screen it did not write.
    """

    def __init__(self, model: core.EditModel, *,
                 on_close: Optional[Callable[[], None]] = None) -> None:
        """Show one model on a screen of its own.

        Args:
            model: Model to show and to edit.
            on_close: What the application does once the session has ended,
                or None for an application that reads the outcome some other
                way. This screen has taken itself off the application by then.
        """
        super().__init__()
        self._on_close = on_close
        self._panel = ModelPanel(model, on_close=self._session_ended)

    @property
    def panel(self) -> ModelPanel:
        """Return the editor that this screen is showing."""
        return self._panel

    @property
    def model(self) -> core.EditModel:
        """Return the model of this session."""
        return self._panel.model

    @property
    def saved_config(self) -> Optional[Config]:
        """Return the configuration this session wrote, None until it does."""
        return self._panel.saved_config

    def close(self, ask_about_unsaved: bool = True) -> None:
        """End the session, which takes this screen off the application.

        Args:
            ask_about_unsaved: Whether the user is asked before a buffer that
                holds something unsaved is dropped.
        """
        self._panel.close(ask_about_unsaved)

    def compose(self) -> ComposeResult:
        """Create the header, the editor and the footer, in that order."""
        yield Header()
        yield self._panel
        yield Footer()

    def _session_ended(self) -> None:
        """Take this screen off the application, and say that it has gone.

        An application that pushed this screen would otherwise be left with
        an empty screen on top of its own, and popping it is this screen's to
        do: it is what the editor was mounted as. The screen of an application
        that shows nothing but the editor is its only one and is not popped,
        because there is nothing underneath it.
        """
        if self.app.screen is self and len(self.app.screen_stack) > 1:
            self.app.pop_screen()
        if self._on_close is not None:
            self._on_close()
