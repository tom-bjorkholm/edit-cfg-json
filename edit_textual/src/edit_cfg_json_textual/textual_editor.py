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
from edit_cfg_json import EditModel, MemberRow, load_text, model_title, \
    row_marks, row_value_text, verdict_text

VALUE_ID_PREFIX = 'value_'
"""Prefix of the identifier of the widget that shows one member value."""

MARK_ID_PREFIX = 'mark_'
"""Prefix of the identifier of the widget that marks one member."""

VERDICT_ID = 'verdict'
"""Identifier of the widget that shows what validation found."""

LOAD_ID = 'load'
"""Identifier of the widget that shows what reading the file did."""

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

VALIDATE_KEY = 'ctrl+r'
"""Key that validates the buffer, and the one the footer names.

Not a plain letter, for the same reason as the quit key. This letter in
particular because a field claims most of the others: `Input` already reads
`ctrl+a`, `ctrl+c`, `ctrl+d`, `ctrl+e`, `ctrl+k`, `ctrl+u`, `ctrl+v`,
`ctrl+w` and `ctrl+x`, and the terminal itself claims `ctrl+c`, `ctrl+d`,
`ctrl+s`, `ctrl+z` and the four that are Backspace, Tab, Return and Escape.
Of what is left, `r` is the one that means something: re-check.
"""

VALIDATE_ALT_KEY = 'f5'
"""The other key that validates the buffer.

Function keys are what other editors use to ask a tool to check what has
been written, so the key is kept. It is not shown in the footer, because a
footer that named the same action twice would suggest they were two
actions, and because a function key is the one of the two that a keyboard
or a terminal is most likely not to deliver.
"""


def _value_id(row: MemberRow) -> str:
    """Return the identifier of the widget that shows one member value."""
    return f'{VALUE_ID_PREFIX}{row.name}'


def _mark_id(row: MemberRow) -> str:
    """Return the identifier of the widget that marks one member."""
    return f'{MARK_ID_PREFIX}{row.name}'


def plain_widget(text: str, widget_id: str) -> Static:
    """Return a widget that shows text of the configuration as it is.

    Textual reads console markup in the text of a widget, so a square
    bracket in a configuration value or in a diagnostic would be taken for
    the beginning of a style and the text between brackets would silently
    disappear. Nothing here is written by this editor, so nothing here is
    markup.

    Args:
        text: Text to show exactly as it is.
        widget_id: Identifier the application finds this widget by.

    Returns:
        A widget showing that text.
    """
    return Static(text, id=widget_id, markup=False)


class EditorApp(App[None]):
    """Textual application that edits one edit model."""

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding(QUIT_KEY, 'quit', 'Quit', priority=True),
        Binding(VALIDATE_KEY, 'validate', 'Validate', priority=True),
        Binding(VALIDATE_ALT_KEY, 'validate', 'Validate', priority=True,
                show=False)]
    """What the keys of the editor do, and which of them the footer names.

    They are priority bindings, so that they are acted on before the field
    that has the focus is offered the key. The two keys that validate are
    two bindings rather than one binding of two keys, because that is what
    lets the footer name one of them and still leave the other working.
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
        """Create one row per member, the verdict, a header and a footer.

        What reading the input file did comes above the members, because it
        is what explains the marks on them. It is created only when there is
        something to say: the file was read before the model was built, so
        the message cannot arrive later, and an empty widget would take a
        line of the screen for a message that will never come.
        """
        yield Header()
        yield from self._load_widgets()
        for row in self._model.rows:
            with Horizontal(classes=ROW_CLASS):
                yield Label(row.name, classes=NAME_CLASS)
                yield self._value_widget(row)
                yield plain_widget(row_marks(row), _mark_id(row))
        yield plain_widget(verdict_text(self._model), VERDICT_ID)
        yield Footer()

    def _load_widgets(self) -> ComposeResult:
        """Create the widget that says what reading the input file did."""
        message = load_text(self._model)
        if message:
            yield plain_widget(message, LOAD_ID)

    def _value_widget(self, row: MemberRow) -> Widget:
        """Return the widget that shows the value of one member.

        A member that the model cannot edit yet gets a widget that only
        shows text, because there is nothing the user could do to it.
        """
        if not row.editable:
            return plain_widget(row_value_text(row), _value_id(row))
        self._member_rows[_value_id(row)] = row
        # A field of its own accord selects all of its text when it is given
        # the focus, so that the first key typed replaces the whole value.
        # That is turned off here, because the two backends would otherwise
        # behave differently: a Tk field puts the cursor in the text and
        # keeps what is there, which is what an editor of existing values
        # should do.
        return Input(value=row_value_text(row), id=_value_id(row),
                     select_on_focus=False)

    def on_input_changed(self, event: Input.Changed) -> None:
        """Write one field into the model and show what the model says.

        A field posts this message when it is given its initial value as
        well, which the model handles by treating a set that changes no text
        as no edit at all.
        """
        widget_id = event.input.id
        assert widget_id is not None
        self._model.set_text(path=self._member_rows[widget_id].path,
                             text=event.value)
        self._show_state()

    def action_validate(self) -> None:
        """Validate the buffer and show what the application would say.

        The fields are written back from the model afterwards, because a
        validation pass is not read only: a member validator returns the
        value that is stored back into the member, so a value can end up
        different from the one the user typed. Writing the text the model
        already holds into a field is not an edit, so this refresh does not
        undo the marks that the pass has just set.
        """
        self._model.validate()
        for row in self._model.rows:
            if _value_id(row) in self._member_rows:
                self._field(row).value = row_value_text(row)
        self._show_state()

    def _field(self, row: MemberRow) -> Input:
        """Return the field that this application shows for one member."""
        return self.query_one(f'#{_value_id(row)}', Input)

    def _show_state(self) -> None:
        """Show the title, the verdict and the mark of every member."""
        self.title = model_title(self._model)
        verdict = self.query_one(f'#{VERDICT_ID}', Static)
        verdict.update(verdict_text(self._model))
        for row in self._model.rows:
            self.query_one(f'#{_mark_id(row)}', Static).update(row_marks(row))


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
