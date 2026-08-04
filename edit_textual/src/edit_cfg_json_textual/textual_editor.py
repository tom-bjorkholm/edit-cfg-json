#! /usr/bin/env python3
"""Textual view of an edit model, with one editable field per member.

Everything this backend takes from the core is reached through `core`, which is
`edit_cfg_json` itself. A backend may use the public API of the core and
nothing else, and naming it at every call site is what makes that visible; it
also keeps the two backends from each holding the same block of twenty
imported names, which is a duplication with nothing to factor out, since
neither backend may import the other.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Iterable, Sequence
from typing import ClassVar, Optional, TextIO
import sys
from config_as_json import Config, PathOrStr
from textual.app import App, ComposeResult, SystemCommand
from textual.binding import BindingsMap
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen, Screen
from textual.widget import Widget
from textual.widgets import Footer, Header, Input, Label, Static
import edit_cfg_json as core

VALUE_ID_PREFIX = 'value_'
"""Prefix of the identifier of the widget that shows one member value."""

MARK_ID_PREFIX = 'mark_'
"""Prefix of the identifier of the widget that marks one member."""

DESCRIPTION_ID_PREFIX = 'about_'
"""Prefix of the identifier of the widget that describes one member."""

DIAGNOSTIC_ID_PREFIX = 'wrong_'
"""Prefix of the identifier of the widget that refuses one member."""

DOCSTRING_ID = 'docstring'
"""Identifier of the widget that shows what the configuration class says."""

VERDICT_ID = 'verdict'
"""Identifier of the widget that shows what validation found."""

SAVE_ID = 'saving'
"""Identifier of the widget that shows what saving did or would do."""

LOAD_ID = 'load'
"""Identifier of the widget that shows what reading the file did."""

BODY_ID = 'body'
"""Identifier of the part of the screen that scrolls."""

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

MEMBER_CLASS = 'member'
"""Style class of the container that holds one member and its description."""

DESCRIPTION_CLASS = 'member_about'
"""Style class of the widget that says what one member is for."""

DIAGNOSTIC_CLASS = 'member_wrong'
"""Style class of the widget that says what is wrong with one member."""

NAME_WIDTH = 24
"""Width in cells of the column that holds the member names."""

DESCRIPTION_INDENT = 4
"""Indentation in cells of the description of one member.

The indentation is what says that the line belongs to the member above it
rather than being a member of its own.
"""

LEAST_VALUE_WIDTH = 8
"""Smallest width in cells that the value of a member is given.

A row that does not fit the terminal has to give way somewhere, and it is
the marks that are cut rather than the field: the field is what the user
edits, and `model_as_text` shows every mark in full whatever the terminal.
"""

QUIT_COMMAND = 'Quit'
"""Name of the action that ends the editor."""

CANCEL_COMMAND = 'Cancel'
"""Name of the action that leaves the question about the output file."""

VALIDATE_COMMAND = 'Validate'
"""Name of the command palette entry that validates the buffer."""

SAVE_COMMAND = 'Save'
"""Name of the command palette entry that writes the output file."""

SAVE_AS_COMMAND = 'Save as'
"""Name of the command palette entry that chooses a file and writes it."""

EXPLAIN_COMMAND = 'Explain'
"""What the explain action is called while the explanations are hidden."""

HIDE_COMMAND = 'Hide explanation'
"""What it is called while they are shown.

The name says what the next press does rather than what the action is about,
because "Explain" beside explanations that are already there reads as an offer
to do something that has been done. The Tk backend answers the same question
with a tick-box, which is what a button row can do and a footer cannot.
"""

VALIDATE_HELP = 'Ask the application what it makes of these values'
"""What the command palette says the validate entry does."""

SAVE_HELP = 'Write these values to the output file'
"""What the command palette says the save entry does."""

SAVE_AS_HELP = 'Choose the file to write, and write it'
"""What the command palette says the save as entry does."""

EXPLAIN_HELP = 'Show or hide what the application says about these values'
"""What the command palette says the explain entry does."""

EMPHASIS_CLASSES = {core.Emphasis.MUTED: 'muted',
                    core.Emphasis.ATTENTION: 'attention',
                    core.Emphasis.WARNING: 'warning',
                    core.Emphasis.GOOD: 'good',
                    core.Emphasis.BAD: 'bad'}
"""The style class of every reason the core has to show something differently.

One class per member of `edit_cfg_json.Emphasis`, and the style sheet gives
each of them a theme colour, so that the editor follows the terminal into its
light or dark
mode instead of naming colours of its own. What each kind of text is comes
from the core, so the two backends cannot colour one thing two ways.
"""

SAVE_AS_PROMPT = 'Save as (Enter writes the file):'
"""What the screen that asks for the output file says."""

SAVE_AS_LEAVE = 'Save as (Enter writes the file, {key} leaves it):'
"""What that screen says while there is a key that leaves it.

The key is named from the settings and not written into the sentence,
because an application that took `escape` for itself would otherwise be
telling its users to press a key that does nothing.
"""

EDITOR_ACTIONS = ('quit', 'validate', 'save', 'save_as', 'explain')
"""The actions of the editor, which a question of its own turns off.

Textual offers a priority binding of an application the key before the screen
that has the focus, and it goes on doing that while a modal screen is up: the
dispatch of a priority binding walks the whole chain and not the part of it
above the last modal screen. So a modal screen is only really modal if the
application says that its own actions do not apply while it is there.
"""


COLOUR_RULES = ('.muted { color: $text-muted; }',
                '.attention { color: $text-accent; }',
                '.warning { color: $text-warning; }',
                '.good { color: $text-success; }',
                '.bad { color: $text-error; }')
"""What each reason to stand out looks like, as a colour of the theme.

Theme colours and not colours of this backend's own: they are what follows the
terminal into its light or dark mode, and an editor that named colours itself
would be legible in one of the two and a guess in the other.

The values and their names are left alone, so the thing the user came to edit
is the most legible thing on the screen. Everything else is either secondary
text or a state to act on, which is what `edit_cfg_json.Emphasis` names.
"""


CSS_RULES = COLOUR_RULES + (
    f'#{BODY_ID} {{ height: 1fr; }}',
    f'.{MEMBER_CLASS} {{ height: auto; }}',
    f'.{ROW_CLASS} {{ height: 1; }}',
    f'.{NAME_CLASS} {{ width: {NAME_WIDTH}; }}',
    f'.{VALUE_CLASS} {{ width: 1fr; min-width: {LEAST_VALUE_WIDTH}; }}',
    f'.{MARK_CLASS} {{ width: auto; }}',
    f'.{DESCRIPTION_CLASS}, .{DIAGNOSTIC_CLASS} {{ width: 1fr; height: auto;'
    f' padding-left: {DESCRIPTION_INDENT}; }}',
    f'#{DOCSTRING_ID} {{ width: 1fr; height: auto; }}',
    f'.{ROW_CLASS} Input {{ height: 1; border: none; padding: 0; }}',
    'SaveAsScreen { align: center middle; }',
    f'#{SAVE_AS_BOX_ID} {{ width: 80%; height: auto; padding: 1 2;'
    ' border: round $primary; background: $surface; }')
"""The width and the height of every part of one member row.

Rows are one cell high, so that the footer stays visible below them. A field
is one cell high as well, which needs its border and its padding taken away,
because both of them are part of how tall a field is.

A member is as high as it needs to be rather than one cell, because it is the
row and the description below it, and the explanatory text is as high as the
lines it takes: a container of Textual's own accord takes an equal share of
the height it is given, which would leave two members holding half a screen
each.

The body takes whatever height is left over, which is what makes it the part
that scrolls: a configuration of any size fits a terminal of any size, and the
verdict, the saving and the footer stay where the user left them, because they
are what a user reaches for after editing rather than something to scroll to.

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


def _value_id(row: core.MemberRow) -> str:
    """Return the identifier of the widget that shows one member value."""
    return f'{VALUE_ID_PREFIX}{row.name}'


def _mark_id(row: core.MemberRow) -> str:
    """Return the identifier of the widget that marks one member."""
    return f'{MARK_ID_PREFIX}{row.name}'


def _description_id(row: core.MemberRow) -> str:
    """Return the identifier of the widget that describes one member."""
    return f'{DESCRIPTION_ID_PREFIX}{row.name}'


def _diagnostic_id(row: core.MemberRow) -> str:
    """Return the identifier of the widget that refuses one member."""
    return f'{DIAGNOSTIC_ID_PREFIX}{row.name}'


def plain_widget(text: str, widget_id: str, classes: Optional[str] = None,
                 emphasis: Optional[core.Emphasis] = None) -> Static:
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
        emphasis: Why this text stands out from the values, or None for a
            widget that is shown in the ordinary text colour.

    Returns:
        A widget showing that text.
    """
    widget = Static(text, id=widget_id, markup=False, classes=classes)
    show_emphasis(widget, emphasis)
    return widget


def show_emphasis(widget: Widget, emphasis: Optional[core.Emphasis]) -> None:
    """Show one widget in the way that one reason to stand out asks for.

    Every class of `EMPHASIS_CLASSES` is set or unset, so that a widget whose
    emphasis changes as the model changes cannot end up carrying two of them
    at once.

    Args:
        widget: Widget to show.
        emphasis: Why the text of that widget stands out from the values, or
            None for the ordinary text colour.
    """
    for kind, name in EMPHASIS_CLASSES.items():
        widget.set_class(kind is emphasis, name)


def bind_action(bindings: BindingsMap, keys: Sequence[str], action: str,
                description: str) -> None:
    """Bind every key combination that the application gave one action.

    The first combination is the one the footer names and the rest work
    without being named, because a footer that named one action twice would
    suggest that they were two actions. An action the application gave no
    combination at all is bound to nothing and stays reachable through the
    command palette.

    Every binding is a priority binding, so that it is acted on before the
    field that has the focus is offered the key. That is also why the
    bindings cannot be made with `App.bind`, which cannot make one and which
    says of itself that it may be removed.

    Args:
        bindings: The bindings of the application or of the screen that the
            action belongs to.
        keys: Key combinations that run the action, in the order that
            decides which of them is named.
        action: Name of the action, without its `action_` prefix.
        description: What the footer and the key panel call the action.
    """
    for index, key in enumerate(keys):
        shown = index == 0
        bindings.bind(key, action, description, show=shown, priority=True)


class SaveAsScreen(ModalScreen[Optional[str]]):
    """Ask which file to write, and give back None when none was named.

    The question is a screen of its own rather than a field in the editor,
    because it is asked, answered and gone: a field that was always there
    would be a fifth thing to read on every row of every session, for a
    question that is asked once or never.
    """

    def __init__(self, out_file: str, cancel_keys: Sequence[str]) -> None:
        """Start the field at the file that would be written now.

        The keys that leave the question are bound here rather than declared
        as a class variable, because which keys they are is the
        application's decision and not this screen's.

        Args:
            out_file: File that saving would write, empty when there is none
                yet. Starting from it is what makes saving a copy beside the
                original a matter of changing a few characters.
            cancel_keys: Key combinations that leave the question
                unanswered, empty when the application gave it none.
        """
        super().__init__()
        self._out_file = out_file
        self._cancel_keys = tuple(cancel_keys)
        bind_action(self._bindings, keys=self._cancel_keys, action='leave',
                    description=CANCEL_COMMAND)

    def compose(self) -> ComposeResult:
        """Create the question and the field that answers it."""
        with Vertical(id=SAVE_AS_BOX_ID):
            yield Label(self._prompt())
            yield Input(value=self._out_file, id=SAVE_AS_ID,
                        select_on_focus=False)

    def _prompt(self) -> str:
        """Return what this screen says, naming the key that leaves it."""
        if not self._cancel_keys:
            return SAVE_AS_PROMPT
        return SAVE_AS_LEAVE.format(key=self._cancel_keys[0])

    def on_input_changed(self, event: Input.Changed) -> None:
        """Keep what happens in this field to this screen.

        The editor underneath writes every field change into the model, and
        this field is not a member of the configuration: it is the name of a
        file. A message that reached the editor would be looked for among the
        members and found nowhere.
        """
        event.stop()

    def on_input_blurred(self, event: Input.Blurred) -> None:
        """Keep leaving this field to this screen, for the same reason.

        The editor underneath asks the model about the member whose field was
        left, and the name of a file is no member of the configuration.
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

    CSS: ClassVar[str] = '\n'.join(CSS_RULES)
    """The widths and heights that make one member fit on one line.

    See `CSS_RULES`, which is where each of them is explained.
    """

    def __init__(self, model: core.EditModel) -> None:
        """Remember the model and name the application after it.

        Args:
            model: Model to show and to edit.
        """
        super().__init__()
        self._model = model
        self._member_rows: dict[str, core.MemberRow] = {}
        self.title = core.model_title(model)
        self._bind_editor_keys()

    def _bind_editor_keys(self) -> None:
        """Bind the key combinations that the application chose.

        The bindings are made on this instance rather than declared as a
        class variable, because which keys the editor takes is not the
        editor's decision any more: the application it runs inside has
        already given some of them to itself. They are read once, here,
        which is the whole of what a later answer from a settings callable
        cannot change.

        A footer too narrow for all of them shows what fits, which costs
        nothing: the key panel of the command palette lists every binding,
        including the ones the footer never shows.
        """
        actions = self._model.settings.actions
        for keys, action, name in (
                (actions.quit, 'quit', QUIT_COMMAND),
                (actions.validate, 'validate', VALIDATE_COMMAND),
                (actions.save, 'save', SAVE_COMMAND),
                (actions.save_as, 'save_as', SAVE_AS_COMMAND)):
            bind_action(self._bindings, keys=keys, action=action,
                        description=name)
        self._bind_explain()

    def _bind_explain(self) -> None:
        """Bind the explain keys, named for what the next press will do.

        The name of this one action depends on the state of the model, so its
        bindings are made again whenever that state changes. A `Binding` cannot
        be renamed, so the bindings of these keys are dropped and made afresh;
        `refresh_bindings` is then what tells the footer to read them again.
        """
        keys = self._model.settings.actions.explain
        for key in keys:
            self._bindings.key_to_bindings.pop(key, None)
        bind_action(self._bindings, keys=keys, action='explain',
                    description=self._explain_name())
        self.refresh_bindings()

    def _explain_name(self) -> str:
        """Return what the explain action is called as things stand now."""
        if self._model.explanations_shown:
            return HIDE_COMMAND
        return EXPLAIN_COMMAND

    def compose(self) -> ComposeResult:
        """Create one row per member, the verdict, a header and a footer.

        What the configuration class says about itself comes above everything
        else, because what the whole configuration is for is what the members
        below it are read in the light of. What reading the input file did
        comes next, because it is what explains the marks on them. Both are
        created only when there is something to say: the file was read before
        the model was built, and a class either has a docstring or has not, so
        neither of the two can arrive later and an empty widget would take a
        line of the screen for good.

        Those and the members are the part that scrolls, because they are the
        part that a configuration of any size makes as tall as it likes. What
        the application makes of the values and where they would be written
        stay below it, where a user who has just edited something looks for
        them.
        """
        yield Header()
        with VerticalScroll(id=BODY_ID):
            yield from self._docstring_widgets()
            yield from self._load_widgets()
            for row in self._model.rows:
                with Vertical(classes=MEMBER_CLASS):
                    with Horizontal(classes=ROW_CLASS):
                        yield Label(row.name, classes=NAME_CLASS)
                        yield self._value_widget(row)
                        yield plain_widget(core.row_marks(row), _mark_id(row),
                                           MARK_CLASS, core.MEMBER_MARK)
                    yield from self._description_widgets(row)
                    yield self._diagnostic_widget(row)
        yield plain_widget(core.verdict_text(self._model), VERDICT_ID,
                           emphasis=core.verdict_emphasis(self._model))
        yield plain_widget(core.save_text(self._model), SAVE_ID,
                           emphasis=core.save_emphasis(self._model))
        yield Footer()

    def get_system_commands(self, screen: Screen[object]
                            ) -> Iterable[SystemCommand]:
        """Offer the actions of the editor in the command palette as well.

        Every terminal can reach the palette, because it is opened with one
        key and then typed into. That is what makes it the answer for
        `SAVE_AS_KEY`, which a terminal without the Kitty keyboard protocol
        cannot tell apart from `SAVE_KEY`. The other actions are here for the
        same reason a menu lists what has a shortcut: a user who has not
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
        yield SystemCommand(self._explain_name(), EXPLAIN_HELP,
                            self.action_explain)

    def _load_widgets(self) -> ComposeResult:
        """Create the widget that says what reading the input file did."""
        message = core.load_text(self._model)
        if message:
            yield plain_widget(message, LOAD_ID, emphasis=core.LOAD_REMARK)

    def _docstring_widgets(self) -> ComposeResult:
        """Create the widget that says what the configuration class says."""
        if self._model.docstring:
            yield plain_widget(core.docstring_text(self._model), DOCSTRING_ID,
                               emphasis=core.EXPLANATION)

    def _description_widgets(self, row: core.MemberRow) -> ComposeResult:
        """Create the widget that says what one member is for, if anything.

        A member the application said nothing about gets no widget, because
        there is nothing that could ever appear in it. A widget that is
        created starts out shown or hidden as the model says, which is not the
        same as shown: a model can have been told to hide the explanations
        before the editor was started.
        """
        if row.description:
            widget = plain_widget(row.description, _description_id(row),
                                  DESCRIPTION_CLASS, core.EXPLANATION)
            shown = core.row_description(model=self._model, row=row)
            widget.display = bool(shown)
            yield widget

    def _diagnostic_widget(self, row: core.MemberRow) -> Static:
        """Create the widget that says what is wrong with one member.

        Every member gets one, unlike the description above it: any member
        can be refused, so there is no member for which this could never say
        anything. It starts out hidden unless the model already has something
        to say about that member, which it has when a model that has been
        validated already reaches this backend.
        """
        wrong = core.row_diagnostic(model=self._model, row=row)
        widget = plain_widget(wrong, _diagnostic_id(row), DIAGNOSTIC_CLASS,
                              core.MEMBER_DIAGNOSTIC)
        widget.display = bool(wrong)
        return widget

    def _value_widget(self, row: core.MemberRow) -> Widget:
        """Return the widget that shows the value of one member.

        A member that the model cannot edit yet gets a widget that only
        shows text, because there is nothing the user could do to it.
        """
        if not row.editable:
            return plain_widget(core.row_value_text(row), _value_id(row),
                                VALUE_CLASS)
        self._member_rows[_value_id(row)] = row
        # A field of its own accord selects all of its text when it is given
        # the focus, so that the first key typed replaces the whole value.
        # That is turned off here, because the two backends would otherwise
        # behave differently: a Tk field puts the cursor in the text and
        # keeps what is there, which is what an editor of existing values
        # should do.
        return Input(value=core.row_value_text(row), id=_value_id(row),
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

    def on_input_blurred(self, event: Input.Blurred) -> None:
        """Ask the model about the member whose field the user has just left.

        Leaving a field is when the user has moved on from it, and it is
        therefore when the editor says whether what they typed means a value
        of that member at all. Nothing is validated here: the whole
        configuration is what a validation pass is about, and this is one
        field answering for itself.
        """
        widget_id = event.input.id
        assert widget_id is not None
        self._model.check_field(self._member_rows[widget_id].path)
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

    def action_explain(self) -> None:
        """Show or hide what the application says about these values.

        The action is renamed as well, because what it is called says what the
        next press will do: "Explain" beside explanations that are already
        there would read as an offer to do something that has been done.
        """
        self._model.toggle_explanations()
        self._show_explanations()
        self._bind_explain()

    def _show_explanations(self) -> None:
        """Show as much of the explanatory text as the model says to show.

        Whether a description is shown is asked of the core rather than
        decided here, so that this backend and the Tk one cannot end up
        disagreeing about what hiding the explanations means.

        This is not part of `_show_state`, which runs on every key the user
        types: nothing typed into a field can change what this configuration
        is for or what one of its members means.
        """
        if self._model.docstring:
            self.query_one(f'#{DOCSTRING_ID}',
                           Static).update(core.docstring_text(self._model))
        for row in self._model.rows:
            if row.description:
                description = core.row_description(model=self._model, row=row)
                self.query_one(f'#{_description_id(row)}',
                               Static).display = bool(description)

    def action_save_as(self) -> None:
        """Ask which file to write, and write it when one was named."""
        self.push_screen(
            SaveAsScreen(out_file=self._out_file_text(),
                         cancel_keys=self._model.settings.actions.cancel),
            self._save_to)

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
                self._field(row).value = core.row_value_text(row)
        self._show_state()

    def _field(self, row: core.MemberRow) -> Input:
        """Return the field that this application shows for one member."""
        return self.query_one(f'#{_value_id(row)}', Input)

    def _show_state(self) -> None:
        """Show the title, the verdict, the saving and every member.

        The verdict and the saving change colour as well as text, because what
        they say is either what the application accepted, what it refused, or
        what has not been asked of it yet, and a user who has to read three
        lines to tell those apart is reading too much.

        What is wrong with a member is shown here too, and not with the
        explanations: a description says what a member is for and stays until
        the user asks for it to go, while a refusal is answered afresh by
        every pass and by every field that is left.
        """
        self.title = core.model_title(self._model)
        self._told(VERDICT_ID, text=core.verdict_text(self._model),
                   emphasis=core.verdict_emphasis(self._model))
        self._told(SAVE_ID, text=core.save_text(self._model),
                   emphasis=core.save_emphasis(self._model))
        for row in self._model.rows:
            self.query_one(f'#{_mark_id(row)}',
                           Static).update(core.row_marks(row))
            self._show_diagnostic(row)

    def _show_diagnostic(self, row: core.MemberRow) -> None:
        """Show what is wrong with one member, or nothing when nothing is."""
        wrong = core.row_diagnostic(model=self._model, row=row)
        widget = self.query_one(f'#{_diagnostic_id(row)}', Static)
        widget.update(wrong)
        widget.display = bool(wrong)

    def _told(self, widget_id: str, text: str,
              emphasis: core.Emphasis) -> None:
        """Show one text of the editor, in the way its state asks for.

        Args:
            widget_id: Identifier of the widget that shows it.
            text: Text to show.
            emphasis: Why that text stands out from the values.
        """
        widget = self.query_one(f'#{widget_id}', Static)
        widget.update(text)
        show_emphasis(widget, emphasis)


class TextualEditor:  # pylint: disable=too-few-public-methods
    """Textual user interface backend for an edit model.

    The class has the single method that `EditorBackend` asks for, and
    deliberately nothing else: everything worth testing without a terminal
    lives in the core.
    """

    def run_editor(self, model: core.EditModel) -> None:
        """Show the model in a Textual screen until the user quits.

        Args:
            model: Model to show and to edit.
        """
        EditorApp(model).run()


# See the same disable in the core: every argument after the first is an
# optional keyword saying one independent thing about the session.
# pylint: disable-next=too-many-arguments
def edit(config: Config, *, descriptions: Optional[core.Descriptions] = None,
         in_file: Optional[PathOrStr] = None,
         loader: Optional[core.ConfigLoader] = None,
         out_file: Optional[PathOrStr] = None,
         policy: core.LoadPolicy = core.LoadPolicy.STRICT_THEN_DEFAULTS,
         settings: core.SettingsSource = core.Settings(),
         stderr_file: TextIO = sys.stderr) -> Optional[Config]:
    """Edit one configuration in the terminal, and return what was saved.

    This is `edit_cfg_json.edit` with this package's backend filled in, for
    an application that has already chosen Textual. Everything it does is
    documented there.

    Args:
        config: Configuration object to edit. It is never modified.
        descriptions: What the application says about the members it
            declares, or None when it says nothing.
        in_file: File to read, or None to start from the declared defaults.
        loader: How this application constructs its configuration, or None for
            a class the editor can construct on its own.
        out_file: File to write, or None to write the input file.
        policy: What to do about declared keys the input file does not hold.
        settings: What this application has already decided about key
            combinations and file names, or a callable that answers with it.
        stderr_file: Stream used for user-facing diagnostics.

    Returns:
        The configuration object that was written, or None when nothing was.

    Raises:
        ConfigLoadError: The input file cannot be opened for editing.
    """
    return core.edit(config=config, backend=TextualEditor(),
                     descriptions=descriptions, in_file=in_file, loader=loader,
                     out_file=out_file, policy=policy, settings=settings,
                     stderr_file=stderr_file)
