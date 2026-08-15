#! /usr/bin/env python3
"""The whole editor of this backend, as one widget.

It is a widget and not an application, so that the same editor serves both
ways of running it: `EditorApp` composes a screen that holds one of these and
owns the terminal, and an application that already runs Textual mounts one of
these in an area of its own and goes on running its own event loop. One body,
so that the two cannot drift apart, and everything that only an application
may do — the title of the terminal, ending the process, the entries of the
command palette — is deliberately not here.

Everything this backend takes from the core is reached through `core`, which is
`edit_cfg_json` itself. A backend may use the public API of the core and
nothing else, and naming it at every call site is what makes that visible; it
also keeps the two backends from each holding the same block of twenty
imported names, which is a duplication with nothing to factor out, since
neither backend may import the other.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable, Sequence
from typing import ClassVar, NamedTuple, Optional
from config_as_json import Config, ConfigPath
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widget import Widget
from textual.widgets import Button, Input, Label, Static
import edit_cfg_json as core
from edit_cfg_json_textual.textual_ask import AskScreen, ConfirmScreen, \
    DISCARD_LABEL, KEEP_LABEL, NO_SAVE_LABEL, OVERWRITE_LABEL, \
    QUESTION_SCREENS
from edit_cfg_json_textual.textual_elements import ADD_ACTION, ASK_KEY_ID, \
    ASK_KEY_LEAVE, ASK_KEY_PROMPT, EARLIER_ACTION, REMOVE_ACTION, \
    element_button, element_id, offered_actions
from edit_cfg_json_textual.textual_look import BODY_ID, DESCRIPTION_CLASS, \
    DIAGNOSTIC_CLASS, DOCSTRING_ID, FOLD_CLASS, LOAD_ID, MARK_CLASS, \
    MEMBERS_ID, MEMBER_CLASS, NAME_CLASS, PANEL_CSS, ROW_CLASS, SAVE_AS_ID, \
    SAVE_ID, SUBTREE_CLASS, TITLE_ID, TREE_INDENT, TYPE_MARK, VALUE_CLASS, \
    VERDICT_ID, bind_action, description_id, diagnostic_id, fold_glyph, \
    fold_id, mark_id, member_id, plain_widget, show_emphasis, subtree_id, \
    value_id

CLOSE_COMMAND = 'Close'
"""Name of the action that ends the editing session.

It is Close and not Quit because this editor may be one panel of an
application that goes on running, and because closing writes nothing of its
own: it is the "cancel" of the design, exactly as the button of the Tk
backend that carries the same word.
"""

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

FOLD_COMMAND = 'Fold all'
"""What the fold action is called while at least one container is open."""

OPEN_COMMAND = 'Unfold all'
"""What it is called once every container is folded.

The name says what the next press does, exactly as the explain action above
is named. The Tk backend answers the same question by renaming its button.
"""

FOLD_HELP = 'Fold every list and dict away, or open every one of them'
"""What the command palette says the fold entry does."""

SAVE_AS_PROMPT = 'Save as (Enter writes the file):'
"""What the screen that asks for the output file says."""

SAVE_AS_LEAVE = 'Save as (Enter writes the file, {key} leaves it):'
"""What that screen says while there is a key that leaves it.

The key is named from the settings and not written into the sentence,
because an application that took `escape` for itself would otherwise be
telling its users to press a key that does nothing.
"""

EDITOR_ACTIONS = ('close', 'validate', 'save', 'save_as', 'explain', 'fold')
"""The actions of the editor, which a question of its own turns off.

Textual offers a priority binding the key before the widget that has the focus
gets it, and it goes on doing that while a modal screen is up: the dispatch of
a priority binding walks the whole chain and not the part of it above the last
modal screen. So a modal screen is only really modal if the editor says that
its own actions do not apply while it is there.
"""


class EditorCommand(NamedTuple):
    """One action of the editor, as a command palette offers it."""

    name: str
    """What the palette calls it, which says what the next press will do."""

    help_text: str
    """What the palette says it does."""

    run: Callable[[], None]
    """What choosing it in the palette runs."""


# The panel is where every widget of the editor and every message about one
# arrives, which is what having one body for both ways of running the editor
# means. See the same disable on the model in the core.
# pylint: disable-next=too-many-public-methods
class ModelPanel(Widget):
    """The whole editor of one edit model, as one widget.

    It holds the label of the configuration, what the class says about itself,
    what reading the input file did, one row per node, and below those the
    validation verdict and the saving line. What does not scroll with the rest
    is what a user reaches for after editing, exactly as in the Tk backend.

    The keys of the editor are bound on this widget, so they are acted on
    while the focus is inside the editor and not while it is elsewhere in a
    window that an application owns.

    It takes a model, which is what this package has of its own and what
    `EditorApp` shows. An application reads a configuration instead, with
    `edit_cfg_json_textual.EditorPanel`.
    """

    DEFAULT_CSS: ClassVar[str] = PANEL_CSS.replace(TYPE_MARK, 'ModelPanel')
    """The widths and the heights that make one member fit on one line.

    See `PANEL_CSS`, which is where each of them is explained. It is
    `DEFAULT_CSS` and not `CSS` because Textual ignores a `CSS` class variable
    on a widget and says so, and the name of the class is written into it
    because a widget styles itself by its type name.
    """

    def __init__(self, model: core.EditModel, *,
                 on_close: Optional[Callable[[], None]] = None) -> None:
        """Remember the model and bind the keys the application chose.

        Args:
            model: Model to show and to edit.
            on_close: What the application does once the session has ended,
                or None for an application that reads the outcome some other
                way. It is called after the editor has taken itself off the
                screen, so that `saved_config` can be read from it.
        """
        super().__init__()
        self._model = model
        self._on_close = on_close
        self._ended = False
        self._member_rows: dict[str, core.MemberRow] = {}
        self._fold_rows: dict[str, core.MemberRow] = {}
        self._element_rows: dict[str, tuple[core.MemberRow, str]] = {}
        self._built: tuple[ConfigPath, ...] = ()
        self._bind_editor_keys()

    @property
    def model(self) -> core.EditModel:
        """Return the model of this session."""
        return self._model

    @property
    def saved_config(self) -> Optional[Config]:
        """Return the configuration this session wrote, None until it does."""
        return self._model.saved_config

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
                (actions.quit, 'close', CLOSE_COMMAND),
                (actions.validate, 'validate', VALIDATE_COMMAND),
                (actions.save, 'save', SAVE_COMMAND),
                (actions.save_as, 'save_as', SAVE_AS_COMMAND)):
            self._bind(keys=keys, action=action, name=name)
        self._bind_explain()
        self._bind_fold()

    def _bind(self, keys: Sequence[str], action: str, name: str) -> None:
        """Bind one action of the editor, as hard as the application asked.

        Args:
            keys: Key combinations that run the action.
            action: Name of the action, without its `action_` prefix.
            name: What the footer and the palette call it.
        """
        bind_action(self._bindings, keys=keys, action=action, description=name,
                    priority=self._model.settings.priority_keys)

    def _bind_explain(self) -> None:
        """Bind the explain keys, named for what the next press will do.

        The name of this one action depends on the state of the model, so its
        bindings are made again whenever that state changes. A `Binding` cannot
        be renamed, so the bindings of these keys are dropped and made afresh;
        `refresh_bindings` is then what tells the footer to read them again.
        """
        self._rebind(keys=self._model.settings.actions.explain,
                     action='explain', name=self._explain_name())

    def _bind_fold(self) -> None:
        """Bind the fold keys, named for what the next press will do.

        Nothing at all is bound for a configuration with no list and no dict
        in it, because there would be nothing for the action to do and a
        footer that offered it would be offering something that is not there.
        """
        keys = self._model.settings.actions.fold \
            if core.can_fold(self._model) else ()
        self._rebind(keys=keys, action='fold', name=self._fold_name())

    def _rebind(self, keys: Sequence[str], action: str, name: str) -> None:
        """Bind one action that is named for what the next press will do.

        A `Binding` cannot be renamed, so the bindings of these keys are
        dropped and made afresh; `refresh_bindings` is then what tells the
        footer to read them again.

        Args:
            keys: Key combinations that run the action.
            action: Name of the action, without its `action_` prefix.
            name: What the footer and the palette call it as things stand.
        """
        for key in keys:
            self._bindings.key_to_bindings.pop(key, None)
        self._bind(keys=keys, action=action, name=name)
        self.refresh_bindings()

    def _explain_name(self) -> str:
        """Return what the explain action is called as things stand now."""
        if self._model.explanations_shown:
            return HIDE_COMMAND
        return EXPLAIN_COMMAND

    def _fold_name(self) -> str:
        """Return what the fold action is called as things stand now."""
        return FOLD_COMMAND if core.fold_hides(self._model) else OPEN_COMMAND

    def compose(self) -> ComposeResult:
        """Create the label, one row per member, the verdict and the saving.

        The label of the configuration comes first and is a widget of this
        editor rather than the title of an application, because an editor
        mounted in a window an application owns has no business writing there.
        What the configuration class says about itself comes next, because
        what the whole configuration is for is what the members below it are
        read in the light of, and what reading the input file did comes after
        that, because it is what explains the marks on them. Both are created
        only when there is something to say: the file was read before the
        model was built, and a class either has a docstring or has not, so
        neither of the two can arrive later and an empty widget would take a
        line of the screen for good.

        Those and the members are the part that scrolls, because they are the
        part that a configuration of any size makes as tall as it likes. What
        the application makes of the values and where they would be written
        stay below it, where a user who has just edited something looks for
        them.
        """
        with VerticalScroll(id=BODY_ID):
            yield plain_widget(core.model_title(self._model), TITLE_ID)
            yield from self._docstring_widgets()
            yield from self._load_widgets()
            yield Vertical(*self._row_widgets(), id=MEMBERS_ID)
        yield plain_widget(core.verdict_text(self._model), VERDICT_ID,
                           emphasis=core.verdict_emphasis(self._model))
        yield plain_widget(core.save_text(self._model), SAVE_ID,
                           emphasis=core.save_emphasis(self._model))

    def _row_widgets(self) -> list[Widget]:
        """Return the widgets of every node, and forget the ones before.

        Returns:
            One widget per node of the model, in the order it reports them.
        """
        self._member_rows = {}
        self._fold_rows = {}
        self._element_rows = {}
        self._built = tuple(row.path for row in self._model.rows)
        return [self._member_widget(index=index, row=row)
                for index, row in enumerate(self._model.rows)]

    def _member_widget(self, index: int, row: core.MemberRow) -> Widget:
        """Return everything one node owns, as one widget.

        The node is indented once for every container it is inside, which is
        what makes the rows a tree, and it is hidden while any of those
        containers is folded away.

        Args:
            index: Place of the node among the rows, which its widgets are
                identified by.
            row: Node to show.

        Returns:
            A widget holding the line of that node and what is said below it.
        """
        marks = plain_widget(core.row_marks(row), mark_id(index), MARK_CLASS,
                             core.MEMBER_MARK)
        beside = [Label(row.name, classes=NAME_CLASS),
                  self._value_widget(index=index, row=row), marks,
                  *self._subtree_widgets(index=index, row=row),
                  *self._element_widgets(index=index, row=row)]
        folding = self._fold_widget(index=index, row=row)
        line = Horizontal(*([folding] if folding is not None else []), *beside,
                          classes=ROW_CLASS)
        below = list(self._description_widgets(index=index, row=row))
        below.append(self._diagnostic_widget(index=index, row=row))
        member = Vertical(line, *below, id=member_id(index),
                          classes=MEMBER_CLASS)
        member.styles.padding = (0, 0, 0, row.depth * TREE_INDENT)
        member.display = row.shown
        return member

    def _element_widgets(self, index: int,
                         row: core.MemberRow) -> ComposeResult:
        """Create the controls that change how many elements one node holds.

        They are at the end of the line, after the value and the marks, so a
        node that offers none of them costs the values no width at all. That
        is what makes four of them affordable where the one control that folds
        a container has to keep a column clear on every row.

        Args:
            index: Place of the node among the rows.
            row: Node to create the controls for.

        Returns:
            The controls that node offers, and none at all for one that
            offers none, which is most nodes of most configurations.
        """
        for action in offered_actions(row):
            widget_id = element_id(index=index, action=action)
            self._element_rows[widget_id] = (row, action)
            yield element_button(widget_id=widget_id, action=action)

    @staticmethod
    def _subtree_widgets(index: int, row: core.MemberRow) -> ComposeResult:
        """Create the widget that says what one object is on its own.

        A node that is no configuration object gets none, by the same rule as
        the description below the row: a widget that could never hold anything
        is a piece of the screen spent on nothing.

        Args:
            index: Place of the node among the rows.
            row: Node to create the widget for.

        Returns:
            One widget for a nested configuration object, and none at all for
            every other node.
        """
        if core.row_validates(row):
            yield plain_widget(core.row_subtree_text(row), subtree_id(index),
                               SUBTREE_CLASS, core.subtree_emphasis(row))

    def _fold_widget(self, index: int,
                     row: core.MemberRow) -> Optional[Widget]:
        """Return the control that folds one container, or an empty space.

        A node that holds nothing gets a widget of the same width rather than
        no widget at all, so that the names of a container and of a value
        beside it begin in the same column. A configuration with nothing to
        fold anywhere gets no column at all, because a column that could never
        hold anything is width taken from the values for nothing.

        Args:
            index: Place of the node among the rows.
            row: Node to create the control for.

        Returns:
            A button for a container, a label for every other node of a
            configuration that has one, and None for one that has none.
        """
        if not core.can_fold(self._model):
            return None
        if not row.foldable:
            return Label('', classes=FOLD_CLASS)
        widget_id = fold_id(index)
        self._fold_rows[widget_id] = row
        return Button(fold_glyph(row), id=widget_id, classes=FOLD_CLASS)

    def command_entries(self) -> tuple[EditorCommand, ...]:
        """Return the actions of the editor, for a command palette.

        Every terminal can reach the palette, because it is opened with one
        key and then typed into. That is what makes it the answer for the key
        of Save as, which a terminal without the Kitty keyboard protocol
        cannot tell apart from the key of Save. The other actions are here for
        the same reason a menu lists what has a shortcut: a user who has not
        learnt the keys should still be able to work.

        The names of two of them say what the next press will do, so this is
        asked afresh whenever the palette is opened rather than being a table
        that was written once.

        Returns:
            One entry per action this editor offers as things stand.
        """
        offered = [EditorCommand(VALIDATE_COMMAND, VALIDATE_HELP,
                                 self.action_validate),
                   EditorCommand(SAVE_COMMAND, SAVE_HELP, self.action_save),
                   EditorCommand(SAVE_AS_COMMAND, SAVE_AS_HELP,
                                 self.action_save_as),
                   EditorCommand(self._explain_name(), EXPLAIN_HELP,
                                 self.action_explain)]
        if core.can_fold(self._model):
            offered.append(EditorCommand(self._fold_name(), FOLD_HELP,
                                         self.action_fold))
        return tuple(offered)

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

    def _description_widgets(self, index: int,
                             row: core.MemberRow) -> ComposeResult:
        """Create the widget that says what one node is for, if anything.

        A node that nothing can ever be said about gets no widget, because
        there is nothing that could ever appear in it. Whether anything can be
        is asked of the core, because the description the row carries is not
        the whole of what is said below a nested configuration object.

        A widget that is created starts out shown or hidden as the model says,
        which is not the same as shown: a model can have been told to hide the
        explanations before the editor was started.
        """
        if core.row_describes(row):
            shown = core.row_description(model=self._model, row=row)
            widget = plain_widget(shown, description_id(index),
                                  DESCRIPTION_CLASS, core.EXPLANATION)
            widget.display = bool(shown)
            yield widget

    def _diagnostic_widget(self, index: int, row: core.MemberRow) -> Static:
        """Create the widget that says what is wrong with one node.

        Every node gets one, unlike the description above it: any node
        can be refused, so there is no node for which this could never say
        anything. It starts out hidden unless the model already has something
        to say about that node, which it has when a model that has been
        validated already reaches this backend.
        """
        wrong = core.row_diagnostic(model=self._model, row=row)
        widget = plain_widget(wrong, diagnostic_id(index), DIAGNOSTIC_CLASS,
                              core.MEMBER_DIAGNOSTIC)
        widget.display = bool(wrong)
        return widget

    def _value_widget(self, index: int, row: core.MemberRow) -> Widget:
        """Return the widget that shows the value of one node.

        A node that the model cannot edit gets a widget that only shows text,
        because there is nothing the user could do to it: a list, a dict and a
        nested configuration object are each edited through the rows below
        them, and a declared member that holds no object holds no text either.
        """
        if not row.editable:
            return plain_widget(core.row_value_text(row), value_id(index),
                                VALUE_CLASS)
        self._member_rows[value_id(index)] = row
        # A field of its own accord selects all of its text when it is given
        # the focus, so that the first key typed replaces the whole value.
        # That is turned off here, because the two backends would otherwise
        # behave differently: a Tk field puts the cursor in the text and
        # keeps what is there, which is what an editor of existing values
        # should do.
        return Input(value=core.row_value_text(row), id=value_id(index),
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

    def action_close(self) -> None:
        """End the session, asking first where there is something to lose."""
        self.close()

    def close(self, ask_about_unsaved: bool = True) -> None:
        """End the session and take the editor off the screen.

        Closing writes nothing, so a buffer holding something that has not
        reached the file loses it. Whether that is so and what is asked about
        it are the core's, so that this backend and the Tk one cannot ask one
        user something and another user nothing; how the question is put is
        this backend's, and a modal screen is how a Textual application asks
        anything.

        Whether the user is asked at all is the application's to decide,
        because only the application knows what it is closing the editor for.
        The Close button and the quit key of the editor are this method with
        the default, so the question is put in the same words whichever of the
        three ended the session.

        Calling this again once the session has ended does nothing, so an
        application need not keep track of whether the user has closed the
        editor already.

        Args:
            ask_about_unsaved: Whether the user is asked before a buffer that
                holds something unsaved is dropped. The default asks, which is
                the way a default about something that cannot be undone should
                lean.
        """
        question = core.close_question(self._model) \
            if ask_about_unsaved else ''
        if not question:
            self._end_session()
            return
        self._ask(question=question, yes_text=DISCARD_LABEL,
                  no_text=KEEP_LABEL, answered=self._end_if_dropped)

    def _ask(self, question: str, yes_text: str, no_text: str,
             answered: Callable[[Optional[bool]], None]) -> None:
        """Put one question of the editor on a screen of its own.

        Args:
            question: What the core says is to be asked.
            yes_text: What the control that agrees to it does.
            no_text: What the control that leaves everything as it is does.
            answered: What is called with the answer, and with None where the
                question was left unanswered.
        """
        self.app.push_screen(
            ConfirmScreen(question=question,
                          cancel_keys=self._model.settings.actions.cancel,
                          yes_text=yes_text, no_text=no_text), answered)

    def _end_if_dropped(self, discard: Optional[bool]) -> None:
        """End the session where the changes were given up, and not else.

        Args:
            discard: What the user answered, and None where the question was
                left unanswered, which is the same as keeping them.
        """
        if discard:
            self._end_session()

    def _end_session(self) -> None:
        """Take the editor off the screen, and say that it has gone.

        Only what the editor created is removed, which is this widget and
        everything it built inside it. What the application had on the screen
        beside it is left exactly as it was.
        """
        if self._ended:
            return
        self._ended = True
        self.remove()
        if self._on_close is not None:
            self._on_close()

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

        A destination that holds a file this session did not write is asked
        about as well, because that file is about to stop existing. Nothing is
        shown when the user says no: they have just been asked and answered,
        and a line saying that nothing was written would be telling them what
        they decided.
        """
        if self._model.out_file is None:
            self.action_save_as()
            return
        question = core.overwrite_question(self._model)
        if not question:
            self._write_file()
            return
        self._ask(question=question, yes_text=OVERWRITE_LABEL,
                  no_text=NO_SAVE_LABEL, answered=self._write_if_allowed)

    def _write_if_allowed(self, overwrite: Optional[bool]) -> None:
        """Write the file where that was agreed to, and not else.

        Args:
            overwrite: What the user answered, and None where the question was
                left unanswered, which is the same as leaving the file alone.
        """
        if overwrite:
            self._write_file()

    def _write_file(self) -> None:
        """Write the output file and show what came of trying."""
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

    def action_fold(self) -> None:
        """Fold every container away, or open every one of them."""
        self._model.toggle_fold_all()
        self._show_folding()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Do what the control the user pressed is for.

        There are two kinds of them and the identifier says which: the control
        that folds one container, and the ones that change how many elements
        a node holds. The message is stopped here because nothing above them
        has any use for it.
        """
        widget_id = event.button.id
        assert widget_id is not None
        event.stop()
        if widget_id in self._fold_rows:
            self._model.toggle_fold(self._fold_rows[widget_id].path)
            self._show_folding()
            return
        row, action = self._element_rows[widget_id]
        self._change_elements(row=row, action=action)

    def _change_elements(self, row: core.MemberRow, action: str) -> None:
        """Add, remove or move one element, asking for a key where needed.

        Args:
            row: Node whose control was pressed.
            action: What that control is for.
        """
        if action == REMOVE_ACTION:
            self._model.remove_element(row.path)
            self._rebuilt_elements()
            return
        if action != ADD_ACTION:
            self._model.move_element(path=row.path,
                                     later=action != EARLIER_ACTION)
            self._rebuilt_elements()
            return
        if not row.offer.keyed:
            self._model.add_element(row.path)
            self._rebuilt_elements()
            return
        self._ask_key(row)

    def _ask_key(self, row: core.MemberRow) -> None:
        """Ask what a new entry of one dict is to be called.

        A new entry of a dict has to be called something, and nothing but the
        person configuring the application knows what.

        Args:
            row: Node that is about to be given an entry.
        """
        cancel = self._model.settings.actions.cancel
        name = core.path_text(row.path)
        prompt = ASK_KEY_PROMPT.format(name=name) if not cancel \
            else ASK_KEY_LEAVE.format(name=name, key=cancel[0])

        def add_named(key: Optional[str]) -> None:
            """Add the entry that was named, and nothing when none was.

            A key the dict already holds is asked about again rather than
            allowed to take the place of what is there: the model refuses such
            a key, and an editor that let the question be answered with one
            would be offering to lose an entry.
            """
            if not key:
                return
            if key in (row.value if isinstance(row.value, dict) else {}):
                self._ask_key(row)
                return
            self._model.add_element(path=row.path, key=key)
            self._rebuilt_elements()
        self.app.push_screen(AskScreen(prompt=prompt, field_id=ASK_KEY_ID,
                                       cancel_keys=cancel), add_named)

    def _rebuilt_elements(self) -> None:
        """Show the rows the model has now, after an element changed.

        The widgets are always mounted afresh, and not only where the paths
        differ as a validation pass leaves them: which controls a row offers
        changes with the elements, so a row that is still at the same path is
        not necessarily still offering the same things.
        """
        self.call_next(self._rebuild_rows)

    def _show_folding(self) -> None:
        """Show which containers are folded and what each control now does.

        What is said below the nodes is shown again as well, because folding a
        nested configuration object changes it: an object that is showing less
        of itself says less about itself. What is wrong with a node is shown
        again for a second reason: folding asks every object at or inside the
        node that was folded, and what one of them refuses is said at the node
        it is about.

        This is not part of `_show_state`, which runs on every key the user
        types: nothing typed into a field folds anything.
        """
        for index, row in enumerate(self._model.rows):
            self.query_one(f'#{member_id(index)}',
                           Vertical).display = row.shown
            if row.foldable:
                self.query_one(f'#{fold_id(index)}',
                               Button).label = fold_glyph(row)
        self._show_descriptions()
        self._show_diagnostics()
        self._show_subtrees()
        self._bind_fold()

    def _show_subtrees(self) -> None:
        """Say what each nested object is on its own, as the model says now.

        It is shown after folding as well as after a validation pass, because
        folding a nested object is one of the moments the model asks that
        object about itself.
        """
        for index, row in enumerate(self._model.rows):
            if not core.row_validates(row):
                continue
            widget = self.query_one(f'#{subtree_id(index)}', Static)
            widget.update(core.row_subtree_text(row))
            show_emphasis(widget, core.subtree_emphasis(row))

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
        self._show_descriptions()

    def _show_descriptions(self) -> None:
        """Show what belongs below every node, as the model says it now."""
        for index, row in enumerate(self._model.rows):
            if not core.row_describes(row):
                continue
            description = core.row_description(model=self._model, row=row)
            widget = self.query_one(f'#{description_id(index)}', Static)
            widget.update(description)
            widget.display = bool(description)

    def action_save_as(self) -> None:
        """Ask which file to write, and write it when one was named."""
        cancel = self._model.settings.actions.cancel
        prompt = SAVE_AS_PROMPT if not cancel \
            else SAVE_AS_LEAVE.format(key=cancel[0])
        self.app.push_screen(AskScreen(prompt=prompt, field_id=SAVE_AS_ID,
                                       cancel_keys=cancel,
                                       answer=self._out_file_text()),
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
        if action in EDITOR_ACTIONS and isinstance(self.app.screen,
                                                   QUESTION_SCREENS):
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

        A pass can also leave the model with other rows than it had, which a
        validator that normalizes a list does, and the widgets are then
        mounted afresh rather than written into. That is done after this
        message rather than inside it, because taking a widget out of the
        screen and putting another one in its place is awaited and this is
        not.
        """
        if self._built != tuple(row.path for row in self._model.rows):
            self.call_next(self._rebuild_rows)
            return
        for index, row in enumerate(self._model.rows):
            if value_id(index) in self._member_rows:
                self._field(index).value = core.row_value_text(row)
        self._show_state()

    async def _rebuild_rows(self) -> None:
        """Show the rows the model has now instead of the ones it had."""
        members = self.query_one(f'#{MEMBERS_ID}', Vertical)
        await members.remove_children()
        await members.mount_all(self._row_widgets())
        self._bind_fold()
        self._show_state()

    def _field(self, index: int) -> Input:
        """Return the field that this editor shows for one node."""
        return self.query_one(f'#{value_id(index)}', Input)

    def _show_state(self) -> None:
        """Show the label, the verdict, the saving and every node.

        The verdict and the saving change colour as well as text, because what
        they say is either what the application accepted, what it refused, or
        what has not been asked of it yet, and a user who has to read three
        lines to tell those apart is reading too much.

        What is wrong with a node is shown here too, and not with the
        explanations: a description says what a node is for and stays until
        the user asks for it to go, while a refusal is answered afresh by
        every pass and by every field that is left.
        """
        self.query_one(f'#{TITLE_ID}',
                       Static).update(core.model_title(self._model))
        self._told(VERDICT_ID, text=core.verdict_text(self._model),
                   emphasis=core.verdict_emphasis(self._model))
        self._told(SAVE_ID, text=core.save_text(self._model),
                   emphasis=core.save_emphasis(self._model))
        for index, row in enumerate(self._model.rows):
            self.query_one(f'#{mark_id(index)}',
                           Static).update(core.row_marks(row))
        self._show_diagnostics()
        self._show_subtrees()

    def _show_diagnostics(self) -> None:
        """Show what is wrong with every node, as the model says it now."""
        for index, row in enumerate(self._model.rows):
            wrong = core.row_diagnostic(model=self._model, row=row)
            widget = self.query_one(f'#{diagnostic_id(index)}', Static)
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
