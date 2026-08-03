#! /usr/bin/env python3
"""Textual view of an edit model, with one editable field per member."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Iterable
from typing import ClassVar, Optional, TextIO
import sys
from config_as_json import Config, PathOrStr
from textual.app import App, ComposeResult, SystemCommand
from textual.binding import Binding, BindingType
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen, Screen
from textual.widget import Widget
from textual.widgets import Footer, Header, Input, Label, Static
from edit_cfg_json import EditModel, LoadPolicy, MemberRow, load_text, \
    model_title, row_marks, row_value_text, save_text, verdict_text
from edit_cfg_json import edit as core_edit

VALUE_ID_PREFIX = 'value_'
"""Prefix of the identifier of the widget that shows one member value."""

MARK_ID_PREFIX = 'mark_'
"""Prefix of the identifier of the widget that marks one member."""

VERDICT_ID = 'verdict'
"""Identifier of the widget that shows what validation found."""

SAVE_ID = 'saving'
"""Identifier of the widget that shows what saving did or would do."""

LOAD_ID = 'load'
"""Identifier of the widget that shows what reading the file did."""

SAVE_AS_BOX_ID = 'save_as_box'
"""Identifier of the box that asks which file to write."""

SAVE_AS_ID = 'save_as'
"""Identifier of the field that the file to write is typed into."""

NAME_CLASS = 'member_name'
"""Style class of the widget that shows one member name."""

VALUE_CLASS = 'member_value'
"""Style class of the widget that shows or edits one member value."""

MARK_CLASS = 'member_mark'
"""Style class of the widget that marks one member."""

ROW_CLASS = 'member_row'
"""Style class of the container that holds the widgets of one member."""

NAME_WIDTH = 24
"""Width in cells of the column that holds the member names."""

LEAST_VALUE_WIDTH = 8
"""Smallest width in cells that the value of a member is given.

A row that does not fit the terminal has to give way somewhere, and it is
the marks that are cut rather than the field: the field is what the user
edits, and `model_as_text` shows every mark in full whatever the terminal.
"""

QUIT_KEY = 'ctrl+q'
"""Key that ends the editor.

A single letter cannot be used for this any more, now that the value of a
member is edited in a field: an unmodified letter belongs to whichever field
has the focus, and a user who typed it would expect to see it appear.

Quitting writes nothing of its own. It is the "cancel" of the design; saving
leaves the editor open, and what has been saved has been saved.
"""

VALIDATE_KEY = 'ctrl+r'
"""Key that validates the buffer, and the one the footer names.

Not a plain letter, for the same reason as the quit key. This letter in
particular because a field claims most of the others: `Input` already reads
`ctrl+a`, `ctrl+c`, `ctrl+d`, `ctrl+e`, `ctrl+k`, `ctrl+u`, `ctrl+v`,
`ctrl+w` and `ctrl+x`, and the terminal itself claims `ctrl+c` and the four
that are Backspace, Tab, Return and Escape. Of what is left, `r` is the one
that means something: re-check.
"""

VALIDATE_ALT_KEY = 'f5'
"""The other key that validates the buffer.

Function keys are what other editors use to ask a tool to check what has
been written, so the key is kept. It is not shown in the footer, because a
footer that named the same action twice would suggest they were two
actions, and because a function key is the one of the two that a keyboard
or a terminal is most likely not to deliver.
"""

SAVE_KEY = 'ctrl+s'
"""Key that writes the output file.

The key every application uses for this, and it does reach the application:
Textual's driver clears `IXON` and `IXOFF` when it puts the terminal into raw
mode, so neither `ctrl+s` nor `ctrl+q` is taken for flow control any more.
"""

SAVE_AS_KEY = 'ctrl+shift+s'
"""Key that chooses an output file and then writes it.

The key every application uses for this as well, but unlike the one above it
is not delivered everywhere. A legacy terminal encodes a control letter as a
single byte with nowhere to put the shift, so this key arrives as `SAVE_KEY`
and the wrong action runs. Textual asks the terminal for the Kitty keyboard
protocol at startup, and a terminal that speaks it reports the two keys
apart; one that does not cannot.

That is why the command palette also offers this action. A palette entry is
delivered by every terminal, because it is a letter typed into a field and
not a key combination at all.
"""

VALIDATE_COMMAND = 'Validate'
"""Name of the command palette entry that validates the buffer."""

SAVE_COMMAND = 'Save'
"""Name of the command palette entry that writes the output file."""

SAVE_AS_COMMAND = 'Save as'
"""Name of the command palette entry that chooses a file and writes it."""

VALIDATE_HELP = 'Ask the application what it makes of these values'
"""What the command palette says the validate entry does."""

SAVE_HELP = 'Write these values to the output file'
"""What the command palette says the save entry does."""

SAVE_AS_HELP = 'Choose the file to write, and write it'
"""What the command palette says the save as entry does."""

SAVE_AS_PROMPT = 'Save as (Enter writes the file, Escape leaves it):'
"""What the screen that asks for the output file says."""

CANCEL_KEY = 'escape'
"""Key that leaves the question about the output file unanswered."""

EDITOR_ACTIONS = ('quit', 'validate', 'save', 'save_as')
"""The actions of the editor, which a question of its own turns off.

Textual offers a priority binding of an application the key before the screen
that has the focus, and it goes on doing that while a modal screen is up: the
dispatch of a priority binding walks the whole chain and not the part of it
above the last modal screen. So a modal screen is only really modal if the
application says that its own actions do not apply while it is there.
"""


CSS_RULES = (
    f'.{ROW_CLASS} {{ height: 1; }}',
    f'.{NAME_CLASS} {{ width: {NAME_WIDTH}; }}',
    f'.{VALUE_CLASS} {{ width: 1fr; min-width: {LEAST_VALUE_WIDTH}; }}',
    f'.{MARK_CLASS} {{ width: auto; }}',
    f'.{ROW_CLASS} Input {{ height: 1; border: none; padding: 0; }}',
    'SaveAsScreen { align: center middle; }',
    f'#{SAVE_AS_BOX_ID} {{ width: 80%; height: auto; padding: 1 2;'
    ' border: round $primary; background: $surface; }')
"""The width and the height of every part of one member row.

Rows are one cell high, so that the footer stays visible below them. A field
is one cell high as well, which needs its border and its padding taken away,
because both of them are part of how tall a field is.

The widths are the part that has to be said rather than left to Textual. A
`Input` is a full width widget of its own accord, so it would take the whole
line and lay the marks of the member out beyond the right edge of the screen,
where they are there and cannot be seen. The value therefore takes what is
left over and the marks take what they need, which is the opposite way round
from the default and the only way round that shows both.

The question about the output file sits in the middle of the screen and takes
most of its width, so that a long path is still readable in a narrow
terminal. Its own field is untouched by the rule above, which reaches only
the fields inside a member row.
"""


def _value_id(row: MemberRow) -> str:
    """Return the identifier of the widget that shows one member value."""
    return f'{VALUE_ID_PREFIX}{row.name}'


def _mark_id(row: MemberRow) -> str:
    """Return the identifier of the widget that marks one member."""
    return f'{MARK_ID_PREFIX}{row.name}'


def plain_widget(text: str, widget_id: str,
                 classes: Optional[str] = None) -> Static:
    """Return a widget that shows text of the configuration as it is.

    Textual reads console markup in the text of a widget, so a square
    bracket in a configuration value or in a diagnostic would be taken for
    the beginning of a style and the text between brackets would silently
    disappear. Nothing here is written by this editor, so nothing here is
    markup.

    Args:
        text: Text to show exactly as it is.
        widget_id: Identifier the application finds this widget by.
        classes: Style classes of the widget, or None for a widget that the
            style sheet does not have to reach.

    Returns:
        A widget showing that text.
    """
    return Static(text, id=widget_id, markup=False, classes=classes)


class SaveAsScreen(ModalScreen[Optional[str]]):
    """Ask which file to write, and give back None when none was named.

    The question is a screen of its own rather than a field in the editor,
    because it is asked, answered and gone: a field that was always there
    would be a fifth thing to read on every row of every session, for a
    question that is asked once or never.
    """

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding(CANCEL_KEY, 'leave', 'Cancel', priority=True)]
    """The key that leaves the question unanswered.

    A priority binding, so that the field the question is typed into does not
    get the key first.
    """

    def __init__(self, out_file: str) -> None:
        """Start the field at the file that would be written now.

        Args:
            out_file: File that saving would write, empty when there is none
                yet. Starting from it is what makes saving a copy beside the
                original a matter of changing a few characters.
        """
        super().__init__()
        self._out_file = out_file

    def compose(self) -> ComposeResult:
        """Create the question and the field that answers it."""
        with Vertical(id=SAVE_AS_BOX_ID):
            yield Label(SAVE_AS_PROMPT)
            yield Input(value=self._out_file, id=SAVE_AS_ID,
                        select_on_focus=False)

    def on_input_changed(self, event: Input.Changed) -> None:
        """Keep what happens in this field to this screen.

        The editor underneath writes every field change into the model, and
        this field is not a member of the configuration: it is the name of a
        file. A message that reached the editor would be looked for among the
        members and found nowhere.
        """
        event.stop()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Give back the file that was named, and leave the screen."""
        event.stop()
        self.dismiss(event.value)

    def action_leave(self) -> None:
        """Leave the screen without naming a file."""
        self.dismiss(None)


class EditorApp(App[None]):
    """Textual application that edits one edit model."""

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding(QUIT_KEY, 'quit', 'Quit', priority=True),
        Binding(VALIDATE_KEY, 'validate', VALIDATE_COMMAND, priority=True),
        Binding(VALIDATE_ALT_KEY, 'validate', VALIDATE_COMMAND, priority=True,
                show=False),
        Binding(SAVE_KEY, 'save', SAVE_COMMAND, priority=True),
        Binding(SAVE_AS_KEY, 'save_as', SAVE_AS_COMMAND, priority=True)]
    """What the keys of the editor do, and which of them the footer names.

    They are priority bindings, so that they are acted on before the field
    that has the focus is offered the key. The two keys that validate are
    two bindings rather than one binding of two keys, because that is what
    lets the footer name one of them and still leave the other working.

    A footer too narrow for all of them shows what fits, which costs nothing:
    the key panel of the command palette lists every binding, including the
    ones the footer never shows.
    """

    CSS: ClassVar[str] = '\n'.join(CSS_RULES)
    """The widths and heights that make one member fit on one line.

    See `CSS_RULES`, which is where each of them is explained.
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
                yield plain_widget(row_marks(row), _mark_id(row), MARK_CLASS)
        yield plain_widget(verdict_text(self._model), VERDICT_ID)
        yield plain_widget(save_text(self._model), SAVE_ID)
        yield Footer()

    def get_system_commands(self, screen: Screen[object]
                            ) -> Iterable[SystemCommand]:
        """Offer the actions of the editor in the command palette as well.

        Every terminal can reach the palette, because it is opened with one
        key and then typed into. That is what makes it the answer for
        `SAVE_AS_KEY`, which a terminal without the Kitty keyboard protocol
        cannot tell apart from `SAVE_KEY`. The other two actions are here for
        the same reason a menu lists what has a shortcut: a user who has not
        learnt the keys should still be able to work.

        Args:
            screen: Screen the palette was opened from.

        Returns:
            The commands of Textual itself, and then the ones of the editor.
        """
        yield from super().get_system_commands(screen)
        yield SystemCommand(VALIDATE_COMMAND, VALIDATE_HELP,
                            self.action_validate)
        yield SystemCommand(SAVE_COMMAND, SAVE_HELP, self.action_save)
        yield SystemCommand(SAVE_AS_COMMAND, SAVE_AS_HELP, self.action_save_as)

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
            return plain_widget(row_value_text(row), _value_id(row),
                                VALUE_CLASS)
        self._member_rows[_value_id(row)] = row
        # A field of its own accord selects all of its text when it is given
        # the focus, so that the first key typed replaces the whole value.
        # That is turned off here, because the two backends would otherwise
        # behave differently: a Tk field puts the cursor in the text and
        # keeps what is there, which is what an editor of existing values
        # should do.
        return Input(value=row_value_text(row), id=_value_id(row),
                     select_on_focus=False, classes=VALUE_CLASS)

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
        """Validate the buffer and show what the application would say."""
        self._model.validate()
        self._refresh()

    def action_save(self) -> None:
        """Write the output file, and say what came of trying.

        Saving validates, so it can rewrite a value exactly as validating
        can, and the fields are refreshed for the same reason.

        A session that has no file to write yet is asked where to write,
        which is what every editor does and what the design asks a backend
        for. There is no way round to loop back here, because the question
        is what gives the session a file.
        """
        if self._model.out_file is None:
            self.action_save_as()
            return
        self._model.save()
        self._refresh()

    def action_save_as(self) -> None:
        """Ask which file to write, and write it when one was named."""
        self.push_screen(SaveAsScreen(self._out_file_text()), self._save_to)

    def check_action(self, action: str,
                     parameters: tuple[object, ...]) -> Optional[bool]:
        """Turn the actions of the editor off while it is asking a question.

        See `EDITOR_ACTIONS` for why this is needed at all. The answer is
        None rather than False, so that the footer shows the actions greyed
        out instead of losing them: a user who is answering a question should
        be able to see that the rest of the editor is waiting for them.

        Args:
            action: Name of the action that is about to run.
            parameters: Arguments of that action, of which these have none.

        Returns:
            None while the question is open and the action is the editor's
            own, and True for every other action at every other time.
        """
        _ = parameters
        if action in EDITOR_ACTIONS and isinstance(self.screen, SaveAsScreen):
            return None
        return True

    def _out_file_text(self) -> str:
        """Return the file saving would write now, as text to be edited."""
        out_file = self._model.out_file
        return '' if out_file is None else str(out_file)

    def _save_to(self, chosen: Optional[str]) -> None:
        """Write the file that was named, and nothing when none was.

        Args:
            chosen: File the user named, or None when the question was left
                unanswered. An empty answer is the same as no answer: there
                is no file whose name is nothing.
        """
        if chosen:
            self._model.set_out_file(chosen)
            self.action_save()

    def _refresh(self) -> None:
        """Write the buffer back into the fields and show the new state.

        A pass over the buffer is not read only: a member validator returns
        the value that is stored back into the member, so a value can end up
        different from the one the user typed. Writing the text the model
        already holds into a field is not an edit, so this refresh does not
        undo the marks that the pass has just set.
        """
        for row in self._model.rows:
            if _value_id(row) in self._member_rows:
                self._field(row).value = row_value_text(row)
        self._show_state()

    def _field(self, row: MemberRow) -> Input:
        """Return the field that this application shows for one member."""
        return self.query_one(f'#{_value_id(row)}', Input)

    def _show_state(self) -> None:
        """Show the title, the verdict, the saving and every member mark."""
        self.title = model_title(self._model)
        verdict = self.query_one(f'#{VERDICT_ID}', Static)
        verdict.update(verdict_text(self._model))
        self.query_one(f'#{SAVE_ID}', Static).update(save_text(self._model))
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


# See the same disable in the core: every argument after the first is an
# optional keyword saying one independent thing about the session.
# pylint: disable-next=too-many-arguments
def edit(config: Config, *, in_file: Optional[PathOrStr] = None,
         out_file: Optional[PathOrStr] = None,
         policy: LoadPolicy = LoadPolicy.STRICT_THEN_DEFAULTS,
         stderr_file: TextIO = sys.stderr) -> Optional[Config]:
    """Edit one configuration in the terminal, and return what was saved.

    This is `edit_cfg_json.edit` with this package's backend filled in, for
    an application that has already chosen Textual. Everything it does is
    documented there.

    Args:
        config: Configuration object to edit. It is never modified.
        in_file: File to read, or None to start from the declared defaults.
        out_file: File to write, or None to write the input file.
        policy: What to do about declared keys the input file does not hold.
        stderr_file: Stream used for user-facing diagnostics.

    Returns:
        The configuration object that was written, or None when nothing was.

    Raises:
        ConfigLoadError: The input file cannot be opened for editing.
    """
    return core_edit(config=config, backend=TextualEditor(), in_file=in_file,
                     out_file=out_file, policy=policy, stderr_file=stderr_file)
