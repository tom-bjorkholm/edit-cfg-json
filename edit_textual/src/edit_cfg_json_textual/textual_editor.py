#! /usr/bin/env python3
"""Read-only Textual view of an edit model."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import ClassVar
from textual.app import App, ComposeResult
from textual.binding import BindingType
from textual.containers import Horizontal
from textual.widgets import Footer, Header, Label, Static
from edit_cfg_json import EditModel, row_value_text

VALUE_ID_PREFIX = 'value_'
"""Prefix of the identifier of the widget that shows one member value."""

NAME_CLASS = 'member_name'
"""Style class of the widget that shows one member name."""

ROW_CLASS = 'member_row'
"""Style class of the container that holds the widgets of one member."""

NAME_WIDTH = 24
"""Width in cells of the column that holds the member names."""


class EditorApp(App[None]):  # pylint: disable=too-few-public-methods
    """Textual application that shows one edit model read-only."""

    BINDINGS: ClassVar[list[BindingType]] = [('q', 'quit', 'Quit')]
    """The quit key, which the footer shows so that it can be found."""

    CSS: ClassVar[str] = (f'.{ROW_CLASS} {{ height: 1; }}\n'
                          f'.{NAME_CLASS} {{ width: {NAME_WIDTH}; }}')
    """One cell high rows, so that the footer stays visible below them."""

    def __init__(self, model: EditModel) -> None:
        """Remember the model and name the application after it.

        Args:
            model: Model to show.
        """
        super().__init__()
        self._model = model
        self.title = model.config_type_name

    def compose(self) -> ComposeResult:
        """Create one row per configuration member, with header and footer."""
        yield Header()
        for row in self._model.rows:
            with Horizontal(classes=ROW_CLASS):
                yield Label(row.name, classes=NAME_CLASS)
                yield Static(row_value_text(row),
                             id=f'{VALUE_ID_PREFIX}{row.name}')
        yield Footer()


class TextualEditor:  # pylint: disable=too-few-public-methods
    """Textual user interface backend for an edit model.

    The class has the single method that `EditorBackend` asks for, and
    deliberately nothing else: everything worth testing without a terminal
    lives in the core.
    """

    def run_editor(self, model: EditModel) -> None:
        """Show the model in a Textual screen until the user quits.

        Args:
            model: Model to show.
        """
        EditorApp(model).run()
