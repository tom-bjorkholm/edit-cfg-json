#! /usr/bin/env python3
"""Textual view of an edit model, with one editable field per member."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import ClassVar
from textual.app import App, ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Footer, Header, Input, Label, Static
from edit_cfg_json import EditModel, MemberRow, model_title, row_value_text

VALUE_ID_PREFIX = 'value_'
"""Prefix of the identifier of the widget that shows one member value."""

NAME_CLASS = 'member_name'
"""Style class of the widget that shows one member name."""

ROW_CLASS = 'member_row'
"""Style class of the container that holds the widgets of one member."""

NAME_WIDTH = 24
"""Width in cells of the column that holds the member names."""

QUIT_KEY = 'ctrl+q'
"""Key that ends the editor.

A single letter cannot be used for this any more, now that the value of a
member is edited in a field: an unmodified letter belongs to whichever field
has the focus, and a user who typed it would expect to see it appear.
"""


class EditorApp(App[None]):  # pylint: disable=too-few-public-methods
    """Textual application that edits one edit model."""

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding(QUIT_KEY, 'quit', 'Quit', priority=True)]
    """The quit key, which the footer shows so that it can be found.

    It is a priority binding, so that it is acted on before the field that
    has the focus is offered the key.
    """

    CSS: ClassVar[str] = (f'.{ROW_CLASS} {{ height: 1; }}\n'
                          f'.{NAME_CLASS} {{ width: {NAME_WIDTH}; }}\n'
                          f'.{ROW_CLASS} Input {{ height: 1; border: none; '
                          'padding: 0; }')
    """One cell high rows, so that the footer stays visible below them.

    A field is one cell high as well, which needs its border and its padding
    taken away, because both of them are part of how tall a field is.
    """

    def __init__(self, model: EditModel) -> None:
        """Remember the model and name the application after it.

        Args:
            model: Model to show and to edit.
        """
        super().__init__()
        self._model = model
        self._member_rows: dict[str, MemberRow] = {}
        self.title = model_title(model)

    def compose(self) -> ComposeResult:
        """Create one row per configuration member, with header and footer."""
        yield Header()
        for row in self._model.rows:
            with Horizontal(classes=ROW_CLASS):
                yield Label(row.name, classes=NAME_CLASS)
                yield self._value_widget(row)
        yield Footer()

    def _value_widget(self, row: MemberRow) -> Widget:
        """Return the widget that shows the value of one member.

        A member that the model cannot edit yet gets a widget that only
        shows text, because there is nothing the user could do to it.
        """
        widget_id = f'{VALUE_ID_PREFIX}{row.name}'
        if not row.editable:
            return Static(row_value_text(row), id=widget_id)
        self._member_rows[widget_id] = row
        # A field of its own accord selects all of its text when it is given
        # the focus, so that the first key typed replaces the whole value.
        # That is turned off here, because the two backends would otherwise
        # behave differently: a Tk field puts the cursor in the text and
        # keeps what is there, which is what an editor of existing values
        # should do.
        return Input(value=row_value_text(row), id=widget_id,
                     select_on_focus=False)

    def on_input_changed(self, event: Input.Changed) -> None:
        """Write one field into the model and show whether it changed.

        A field posts this message when it is given its initial value as
        well, which the model handles by treating a set that changes no text
        as no edit at all.
        """
        widget_id = event.input.id
        assert widget_id is not None
        self._model.set_text(path=self._member_rows[widget_id].path,
                             text=event.value)
        self.title = model_title(self._model)


class TextualEditor:  # pylint: disable=too-few-public-methods
    """Textual user interface backend for an edit model.

    The class has the single method that `EditorBackend` asks for, and
    deliberately nothing else: everything worth testing without a terminal
    lives in the core.
    """

    def run_editor(self, model: EditModel) -> None:
        """Show the model in a Textual screen until the user quits.

        Args:
            model: Model to show and to edit.
        """
        EditorApp(model).run()
