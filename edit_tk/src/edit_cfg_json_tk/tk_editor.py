#! /usr/bin/env python3
"""Tkinter view of an edit model, with one editable field per member.

Everything this backend takes from the core is reached through `core`, which is
`edit_cfg_json` itself. A backend may use the public API of the core and
nothing else, and naming it at every call site is what makes that visible; it
also keeps the two backends from each holding the same block of twenty
imported names, which is a duplication with nothing to factor out, since
neither backend may import the other.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from typing import NamedTuple, Optional, TextIO
import sys
import tkinter
from tkinter import filedialog
from config_as_json import Config, ConfigPath, PathOrStr
import edit_cfg_json as core
from edit_cfg_json_tk.key_names import bind_key
from edit_cfg_json_tk.scrolling import scrolling_body
from edit_cfg_json_tk.tk_look import FIELD_BACKGROUND, FIELD_BORDER, \
    FIELD_FOREGROUND, FOLD_WIDTH, LEAST_FIELD_WIDTH, NAME_COLUMN_WIDTH, \
    PADDING, TREE_INDENT, label_text, place_text, shown_text, told

VALIDATE_TEXT = 'Validate'
"""Text of the button that runs the validation of the application."""

SAVE_TEXT = 'Save'
"""Text of the button that writes the output file."""

SAVE_AS_TEXT = 'Save as...'
"""Text of the button that chooses an output file and then writes it."""

EXPLAIN_TEXT = 'Explain'
"""Text of the tick-box that shows or hides the explanatory text.

A tick-box and not a button, because the action is a toggle and a button
called Explain that hides the explanations reads as the wrong thing entirely.
The tick says which of the two states the editor is in, so one text is true in
both. The Textual backend has no button row to put one in and renames its own
action instead.
"""

FOLD_ALL_TEXT = 'Fold all'
"""Text of the button while at least one list or dict is open.

A button and not a tick-box, unlike the explanations beside it, because its
two states are not the two states of one thing: a configuration can be partly
folded, and what the button says is what the next press will do to all of it.
That is the same answer the Textual backend gives, which renames its action.
"""

OPEN_ALL_TEXT = 'Unfold all'
"""Text of the same button once every list and dict is folded."""

FOLD_SHUT_TEXT = '+'
"""Text of the control of a container that is folded away."""

FOLD_OPEN_TEXT = '-'
"""Text of the control of a container that is open.

The two are what a tree has always used for this, and they are one character
wide in every font, which the arrows that a modern tree draws are not.
"""

CLOSE_TEXT = 'Close'
"""Text of the button that ends the editor.

Closing writes nothing of its own. It is the "cancel" of the design, and it
is called Close because saving leaves the editor open: a button called Cancel
beside values that have already been written would read as an offer to undo
the writing, which it is not.
"""

SAVE_AS_TITLE = 'Save the configuration as'
"""Title of the dialog that asks which file to write."""

CONFIG_FILES = 'Configuration files ({extension})'
"""What the dialog calls the files of the extension the application uses."""

ALL_FILES = 'All files'
"""What the dialog calls every other file."""


def _file_types(settings: core.Settings) -> list[tuple[str, str]]:
    """Return what the dialog that asks for a file offers to filter by.

    An application that enforces its extension has that one filter and no
    other, because a name with another extension cannot be saved and a
    dialog that offered to look for one would be inviting a refusal. An
    application whose extension is a default offers it first and everything
    else after it, because a name with another extension can be saved. An
    application with no opinion offers nothing, which is what this dialog
    did before there were settings at all.

    Args:
        settings: What the application has decided about file names.

    Returns:
        The file types of the dialog, empty when it has no opinion.
    """
    extension = settings.file_extension
    if extension is None:
        return []
    named = (CONFIG_FILES.format(extension=extension), f'*{extension}')
    if settings.extension_enforced:
        return [named]
    return [named, (ALL_FILES, '*')]


class StateWidgets(NamedTuple):
    """The widgets that say what is true of the whole model.

    They are one object rather than one attribute each, so that the class
    below has a handful of things to hold rather than a dozen.
    """

    title: tkinter.Label
    """The label that names the configuration and marks unsaved changes."""

    docstring: Optional[tkinter.Label]
    """The label that says what the configuration class says about itself.

    It is None for a class with no docstring of its own, because there is then
    nothing that could ever appear in it.
    """

    verdict: tkinter.Label
    """The label that says what the application makes of these values."""

    saving: tkinter.Label
    """The label that says what saving did, or where it would write."""

    explained: tkinter.BooleanVar
    """Whether the tick-box of the explanations is ticked.

    The variable is what a `Checkbutton` shows its state through, and it has
    to be kept for as long as the tick-box lives: a `tkinter.Variable` unsets
    its Tcl variable when it is collected.
    """

    folding: Optional[tkinter.Button]
    """The button that folds every container away, or opens every one.

    It is None for a configuration with no list and no dict in it, because a
    button that could never do anything would be offering something that is
    not there.
    """


class RowWidgets(NamedTuple):
    """The widgets that one node of the configuration owns."""

    frame: tkinter.Frame
    """The widget that holds the whole node, which is what folding hides.

    It is packed and unpacked rather than created and destroyed, so that a
    field the user is typing into survives its container being folded and
    opened again.
    """

    fold: Optional[tkinter.Button]
    """The control that folds this container, None for a node with none."""

    field: Optional[tkinter.StringVar]
    """The field of an editable node, and None for every other node."""

    mark: tkinter.Label
    """The widget that says what has happened to this member."""

    description: Optional[tkinter.Label]
    """The widget that says what this member is for.

    It is None for a member that nothing is said about, because there is then
    nothing that could ever appear in it.
    """

    diagnostic: tkinter.Label
    """The widget that says what is wrong with this member.

    Every member has one, unlike the description above it: any member can be
    refused, so there is no member for which this could never say anything.
    """


def _show_below(widgets: RowWidgets, description: str,
                diagnostic: str) -> None:
    """Show what belongs below one member, in the order it belongs in.

    Both texts are taken out of the layout and put back rather than only the
    one that changed, because Tk packs a widget after the ones that are
    already there: a description that came back while a diagnostic was
    showing would otherwise land below it. Nothing is touched while both
    texts are already what they should be, so the ordinary case of typing
    into a field does not lay the window out again on every key.

    Args:
        widgets: Widgets of the member.
        description: What the member is for, empty while that is hidden.
        diagnostic: What is wrong with the member, empty when nothing is.
    """
    if label_text(widgets.description) == description and \
            label_text(widgets.diagnostic) == diagnostic:
        return
    for label in (widgets.description, widgets.diagnostic):
        place_text(label, '')
    place_text(widgets.description, description)
    place_text(widgets.diagnostic, diagnostic)


class EditorWidgets:  # pylint: disable=too-few-public-methods
    """The widgets that show one edit model below one parent widget.

    This is a class rather than a function because the fields have to be
    kept: a `tkinter.StringVar` unsets its Tcl variable when it is collected,
    and the field it belongs to would then lose both its text and the
    callback that writes it into the model. Keeping them together also gives
    an application that mounts these widgets in a window of its own a single
    object to hold on to.

    The widgets of the nodes are kept in the order the model reports its rows
    in, which is the order they were created in. A validation pass can change
    how many rows there are, because a validator that normalizes a list
    changes how many values it holds, so the paths that were built are kept
    and the widgets are made again when they no longer match. Every other
    refresh leaves them alone, which is what keeps the focus in the field the
    user is typing into.
    """

    def __init__(self, parent: tkinter.Misc, model: core.EditModel, *,
                 on_close: Optional[Callable[[], None]] = None) -> None:
        """Create the labels, one row per member, the verdict and the buttons.

        The parent is a widget and not a window, so that the same rows can
        later be mounted inside a window that an application owns itself.

        Args:
            parent: Widget that becomes the parent of the created widgets.
            model: Model to show and to edit.
            on_close: What closing the editor does, or None to destroy the
                window these widgets are in. None is for a caller that owns
                that window, which is what `TkEditor` does. A caller that
                mounts these widgets in a window of an application says what
                closing does, because the editor must never destroy a window
                it did not create.
        """
        self._model = model
        self._close = on_close or parent.winfo_toplevel().destroy
        scrolling = scrolling_body(parent)
        # The part that does not scroll is packed first, because Tk gives each
        # child the space it asks for in the order they were packed: a window
        # too short for everything would otherwise leave nothing at all for
        # the verdict, the saving and the buttons, and they are what a user
        # reaches for after editing. It is created second, so that the widgets
        # of the editor are still created in the order they are read in.
        fixed = tkinter.Frame(parent)
        fixed.pack(side='bottom', fill='x')
        scrolling.area.pack(side='top', fill='both', expand=True)
        body = scrolling.body
        title = tkinter.Label(body, text=core.model_title(model))
        title.pack(pady=PADDING)
        docstring = self._add_docstring(body)
        self._add_load_message(body)
        self._members = tkinter.Frame(body)
        self._members.pack(fill='x')
        self._rows: list[RowWidgets] = []
        self._paths: tuple[ConfigPath, ...] = ()
        self._create_rows()
        verdict = self._add_verdict(fixed)
        saving = self._add_saving(fixed)
        explained = tkinter.BooleanVar(master=parent,
                                       value=model.explanations_shown)
        self._state = StateWidgets(title=title, docstring=docstring,
                                   verdict=verdict, saving=saving,
                                   explained=explained,
                                   folding=self._add_buttons(fixed, explained))
        self._show_rows()
        self._bind_keys(parent.winfo_toplevel())

    @property
    def label_text(self) -> str:
        """Return the text that the label of the whole model shows."""
        return str(self._state.title.cget('text'))

    @property
    def verdict_text_shown(self) -> str:
        """Return the text that the validation part of the editor shows."""
        return str(self._state.verdict.cget('text'))

    @property
    def save_text_shown(self) -> str:
        """Return the text that the saving part of the editor shows."""
        return str(self._state.saving.cget('text'))

    @property
    def wrong_shown(self) -> list[str]:
        """Return what the editor says about each member, in row order.

        A member that nothing is known to be wrong with says nothing, so most
        of these are empty most of the time.
        """
        return [label_text(row.diagnostic) for row in self._rows]

    @property
    def docstring_shown(self) -> str:
        """Return the text that the label of the configuration class shows."""
        if self._state.docstring is None:
            return ''
        return str(self._state.docstring.cget('text'))

    def _add_docstring(self, parent: tkinter.Misc) -> Optional[tkinter.Label]:
        """Show what the configuration class says about itself, if anything.

        The widget is created only when that class has a docstring of its
        own. What the explain action changes is how much of a docstring is
        shown and not whether there is one, so a class without one would
        leave an empty widget taking a line of the window for good.

        Args:
            parent: Widget that becomes the parent of the created widget.

        Returns:
            The widget that shows the docstring, or None when the
            configuration class has none.
        """
        if not self._model.docstring:
            return None
        label = shown_text(parent, core.docstring_text(self._model),
                           core.EXPLANATION)
        label.pack(fill='x', padx=PADDING)
        return label

    def _add_load_message(self, parent: tkinter.Misc) -> None:
        """Show what reading the input file did, when it did anything.

        The widget is created only when there is something to say. The file
        was read before the model was built, so the message cannot arrive
        later, and an empty widget would take a line of the window for a
        message that will never come.
        """
        message = core.load_text(self._model)
        if message:
            shown_text(parent, message,
                       core.LOAD_REMARK).pack(fill='x', padx=PADDING)

    def _add_verdict(self, parent: tkinter.Misc) -> tkinter.Label:
        """Create the label that says what the application makes of these.

        It is packed below the scrolling part rather than at the end of it, so
        that it cannot scroll away: a user who has just asked what the
        application makes of these values is looking at it.
        """
        label = shown_text(parent, core.verdict_text(self._model),
                           core.verdict_emphasis(self._model))
        label.pack(side='top', fill='x', padx=PADDING, pady=PADDING)
        return label

    def _add_saving(self, parent: tkinter.Misc) -> tkinter.Label:
        """Create the label that says what saving did, or where it would."""
        label = shown_text(parent, core.save_text(self._model),
                           core.save_emphasis(self._model))
        label.pack(side='top', fill='x', padx=PADDING)
        return label

    def _add_buttons(self, parent: tkinter.Misc, explained: tkinter.BooleanVar
                     ) -> Optional[tkinter.Button]:
        """Create the buttons, the tick-box and the one that ends the run.

        They share one row, because six of them stacked above each other
        would push the values of a real configuration off the window.

        The explanations get a tick-box rather than a button, because the
        action is a toggle: a button saying Explain beside explanations that
        are already there would be offering something that has been done. The
        folding gets a button that is renamed instead, because a partly
        folded configuration is neither of the two states a tick could show.

        Args:
            parent: Widget that becomes the parent of the button row.
            explained: Whether the tick-box of the explanations is ticked.

        Returns:
            The button that folds everything, or None for a configuration
            that has nothing to fold.
        """
        line = tkinter.Frame(parent)
        line.pack(side='top', pady=PADDING)
        for text, command in ((VALIDATE_TEXT, self._validate),
                              (SAVE_TEXT, self._save),
                              (SAVE_AS_TEXT, self._save_as)):
            tkinter.Button(line, text=text, command=command).pack(side='left',
                                                                  padx=PADDING)
        tkinter.Checkbutton(line, text=EXPLAIN_TEXT, command=self._explain,
                            variable=explained).pack(side='left', padx=PADDING)
        folding = self._add_fold_all(line)
        tkinter.Button(line, text=CLOSE_TEXT,
                       command=self._close).pack(side='left', padx=PADDING)
        return folding

    def _add_fold_all(self, parent: tkinter.Misc) -> Optional[tkinter.Button]:
        """Create the button that folds or opens every container, if any.

        Args:
            parent: Widget that becomes the parent of the created button.

        Returns:
            That button, or None for a configuration with no list and no
            dict in it, which has nothing for the action to do.
        """
        if not core.can_fold(self._model):
            return None
        button = tkinter.Button(parent, text=FOLD_ALL_TEXT,
                                command=self._fold_all)
        button.pack(side='left', padx=PADDING)
        return button

    def _bind_keys(self, window: tkinter.Misc) -> None:
        """Bind the key combinations that the application chose.

        The bindings are made on the window and not on each field, because
        a key that a field does not use for itself reaches the window that
        the field is in. Nothing is bound for the cancel action: the only
        question this backend asks is the toolkit's own file dialog, which
        answers that key itself. Nothing is bound for the folding either
        where there is nothing to fold, for the same reason as the button.

        The keys are read once, here, which is the whole of what a later
        answer from a settings callable cannot change.

        Args:
            window: Window that the bindings are made on.
        """
        actions = self._model.settings.actions
        folding = actions.fold if core.can_fold(self._model) else ()
        for keys, command in ((actions.quit, self._close),
                              (actions.validate, self._validate),
                              (actions.save, self._save),
                              (actions.save_as, self._save_as),
                              (actions.explain, self._explain),
                              (folding, self._fold_all)):
            for key in keys:
                bind_key(window=window, key=key, command=command)

    def _create_rows(self) -> None:
        """Create the widgets of every node, replacing the ones there are.

        Nothing is put into the layout here, because which of the rows are
        shown is what `_show_rows` decides, and because the widgets that do
        not scroll have to be packed before these whatever order they are
        created in.
        """
        for child in self._members.winfo_children():
            child.destroy()
        self._rows = [self._add_row(parent=self._members, row=row)
                      for row in self._model.rows]
        self._paths = tuple(row.path for row in self._model.rows)

    def _build_rows(self) -> None:
        """Make the widgets of every node again and put them on the window.

        A validation pass can change how many rows the model has, because a
        validator that normalizes a list changes how many values it holds. So
        the widgets are made again whenever the paths no longer match, and
        left exactly as they are whenever they do, which is every ordinary
        refresh and is what keeps the focus where the user put it.
        """
        self._create_rows()
        self._show_rows()

    def _add_row(self, parent: tkinter.Misc,
                 row: core.MemberRow) -> RowWidgets:
        """Create the widgets of one node, and its description below them.

        The node gets a frame of its own, holding the line that is edited
        and the texts under it, so that hiding one of those and showing it
        again cannot move it away from the node it belongs to. That frame is
        also what folding takes out of the layout, which is why it is not
        packed here but by `_show_rows`.
        """
        frame = tkinter.Frame(parent)
        line = tkinter.Frame(frame)
        line.pack(fill='x')
        fold = self._add_fold(parent=line, row=row)
        tkinter.Label(line, text=row.name, width=NAME_COLUMN_WIDTH,
                      anchor='w').pack(side='left')
        field = self._add_value(parent=line, row=row)
        mark = shown_text(line, core.row_marks(row), core.MEMBER_MARK,
                          wrapping=False)
        mark.pack(side='left')
        widgets = RowWidgets(
            frame=frame, fold=fold, field=field, mark=mark,
            description=self._add_description(parent=frame, row=row),
            diagnostic=shown_text(frame, '', core.MEMBER_DIAGNOSTIC))
        self._show_row_texts(row=row, widgets=widgets)
        return widgets

    def _add_fold(self, parent: tkinter.Misc,
                  row: core.MemberRow) -> Optional[tkinter.Button]:
        """Create the control that folds one container, if it is one.

        A node that holds nothing gets a label of the same width instead of
        no widget at all, so that the names of a container and of a value
        beside it begin in the same column. A configuration with nothing to
        fold anywhere gets no column at all, because a column that could
        never hold anything is width taken from the values for nothing.

        Args:
            parent: Line of the node that is being shown.
            row: Node to create the control for.

        Returns:
            The control that folds that container, or None for a node that
            is not one.
        """
        if not core.can_fold(self._model):
            return None
        if not row.foldable:
            tkinter.Label(parent, text='', width=FOLD_WIDTH).pack(side='left')
            return None
        button = tkinter.Button(parent, width=FOLD_WIDTH, relief='flat',
                                borderwidth=0, highlightthickness=0, padx=0,
                                pady=0, command=self._folder(row.path))
        button.pack(side='left')
        return button

    def _folder(self, path: ConfigPath) -> Callable[[], None]:
        """Return the command that folds one container or opens it again."""
        def fold_row() -> None:
            """Fold that container, and show what the model says now."""
            self._model.toggle_fold(path)
            self._show_rows()
        return fold_row

    def _fold_all(self) -> None:
        """Fold every container away, or open every one of them."""
        self._model.toggle_fold_all()
        self._show_rows()

    def _show_rows(self) -> None:
        """Put every node that is shown into the layout, in its order.

        Every one of them is taken out first and put back afterwards, because
        Tk packs a widget after the ones that are already there: a node that
        came back would otherwise land below the ones below it. Nothing here
        is created or destroyed, so a field the user was typing into keeps
        what is in it while its container is folded and opened again.
        """
        for widgets in self._rows:
            widgets.frame.pack_forget()
        for row, widgets in zip(self._model.rows, self._rows, strict=True):
            if widgets.fold is not None:
                widgets.fold.config(text=FOLD_SHUT_TEXT if row.folded
                                    else FOLD_OPEN_TEXT)
            if row.shown:
                widgets.frame.pack(fill='x', padx=(self._indent(row), PADDING))
        self._show_fold_all()

    @staticmethod
    def _indent(row: core.MemberRow) -> int:
        """Return how far from the left edge one node begins, in pixels."""
        return PADDING + row.depth * TREE_INDENT

    def _show_fold_all(self) -> None:
        """Say what the next press of the fold button will do."""
        if self._state.folding is not None:
            self._state.folding.config(
                text=FOLD_ALL_TEXT if core.fold_hides(self._model)
                else OPEN_ALL_TEXT)

    def _show_row_texts(self, row: core.MemberRow,
                        widgets: RowWidgets) -> None:
        """Show what the model says belongs below one node."""
        _show_below(widgets,
                    description=core.row_description(model=self._model,
                                                     row=row),
                    diagnostic=core.row_diagnostic(model=self._model, row=row))

    def _add_description(self, parent: tkinter.Misc,
                         row: core.MemberRow) -> Optional[tkinter.Label]:
        """Create the widget that says what one member is for, if anything.

        A member that nothing is said about gets no widget, because there is
        nothing that could ever appear in it.

        Args:
            parent: Frame of the member that is being described.
            row: Member to describe.

        Returns:
            The widget that shows the description, or None when nothing is
            said about this member.
        """
        if not row.description:
            return None
        return shown_text(parent, '', core.EXPLANATION)

    def _add_value(self, parent: tkinter.Misc,
                   row: core.MemberRow) -> Optional[tkinter.StringVar]:
        """Create the value widget of one member and wire it to the model.

        A member that the model cannot edit yet gets a widget that only
        shows text, because there is nothing the user could do to it.

        The variable is given the parent as its master, so that it is
        created in the same Tcl interpreter as the field that reads it. A
        variable constructed without one is created in the first interpreter
        of the process instead, which is the wrong one as soon as the editor
        is not the only Tk in the application: the field would then show
        nothing and the callback below would never run.
        """
        if not row.editable:
            tkinter.Label(parent, text=core.row_value_text(row),
                          anchor='w').pack(side='left')
            return None
        field = tkinter.StringVar(master=parent,
                                  value=core.row_value_text(row))
        # The window is white, so a field that kept the background it is given
        # could not be told from a label. The tint, the border and the caret
        # colour are what say that this one is edited and the labels are not.
        entry = tkinter.Entry(parent, textvariable=field, relief='flat',
                              width=LEAST_FIELD_WIDTH,
                              background=FIELD_BACKGROUND,
                              foreground=FIELD_FOREGROUND,
                              insertbackground=FIELD_FOREGROUND,
                              highlightbackground=FIELD_BORDER,
                              highlightthickness=1)
        entry.pack(side='left', fill='x', expand=True)
        entry.bind('<FocusOut>', self._leaver(row))
        field.trace_add('write', self._writer(row=row, field=field))
        return field

    def _writer(self, row: core.MemberRow,
                field: tkinter.StringVar) -> Callable[..., None]:
        """Return the callback that writes one field into the model.

        Tk reports a change of the variable and not of the widget, so the
        callback reads the field itself. Every change is written through,
        including the ones that no key press caused, such as a paste.
        """
        def write_field(*trace_arguments: str) -> None:
            """Write the text of the field and show what the model says."""
            _ = trace_arguments
            self._model.set_text(path=row.path, text=field.get())
            self._show_state()
        return write_field

    def _leaver(self, row: core.MemberRow) -> Callable[..., None]:
        """Return the callback that one field runs when it loses the focus.

        Leaving a field is when the user has moved on from it, and it is
        therefore when the editor says whether what they typed means a value
        of that member at all. Nothing is validated here: the whole
        configuration is what a validation pass is about, and this is one
        field answering for itself.
        """
        def left_field(*event: 'tkinter.Event[tkinter.Misc]') -> None:
            """Check the member that was left and show what the model says."""
            _ = event
            self._model.check_field(row.path)
            self._show_state()
        return left_field

    def _validate(self) -> None:
        """Validate the buffer and show what the application would say."""
        self._model.validate()
        self._refresh()

    def _save(self) -> None:
        """Write the output file, and say what came of trying.

        Saving validates, so it can rewrite a value exactly as validating
        can, and the fields are refreshed for the same reason.

        A session that has no file to write yet is asked where to write,
        which is what every editor does and what the design asks a backend
        for. There is no way round to loop back here, because the question
        is what gives the session a file.
        """
        if self._model.out_file is None:
            self._save_as()
            return
        self._model.save()
        self._refresh()

    def _save_as(self) -> None:
        """Ask which file to write, and write it when one was named.

        What the dialog offers is what the application decided: the
        extension it uses for its configuration is the one the dialog adds
        to a name that has none, and the one it offers to filter by. An
        application with no opinion gets a dialog with none, which is what
        this dialog had before there were settings at all.

        The name that comes back is handed to the model, which is what
        completes it and what refuses it, so that a user of this backend and
        a user of the other one are told the same thing about one name.
        """
        settings = self._model.settings
        chosen = filedialog.asksaveasfilename(
            title=SAVE_AS_TITLE, filetypes=_file_types(settings),
            defaultextension=settings.file_extension or '')
        if chosen:
            self._model.set_out_file(chosen)
            self._save()

    def _explain(self) -> None:
        """Show or hide what the application says about these values."""
        self._model.toggle_explanations()
        self._show_explanations()

    def _show_explanations(self) -> None:
        """Show as much of the explanatory text as the model says to show.

        The tick-box is set from the model rather than left to Tk, because Tk
        only flips it when it is the tick-box that was pressed. The key of the
        explain action reaches this method without touching it, and a tick
        that disagreed with the window would be worse than no tick at all.

        It is not part of `_show_state`, which runs on every key the user
        types: nothing the user types into a field can change what this
        configuration is for or what one of its members means.
        """
        self._state.explained.set(self._model.explanations_shown)
        if self._state.docstring is not None:
            self._state.docstring.config(text=core.docstring_text(self._model))
        self._show_member_texts()

    def _show_member_texts(self) -> None:
        """Show what belongs below every node, as the model says it now."""
        for row, widgets in zip(self._model.rows, self._rows, strict=True):
            self._show_row_texts(row=row, widgets=widgets)

    def _refresh(self) -> None:
        """Write the buffer back into the fields and show the new state.

        A pass over the buffer is not read only: a member validator returns
        the value that is stored back into the member, so a value can end up
        different from the one the user typed. Writing the text the model
        already holds into a field is not an edit, so this refresh does not
        undo the marks that the pass has just set.

        A pass can also leave the model with other rows than it had, which a
        validator that normalizes a list does, and the widgets are then made
        again rather than written into.
        """
        if self._paths != tuple(row.path for row in self._model.rows):
            self._build_rows()
        for row, widgets in zip(self._model.rows, self._rows, strict=True):
            if widgets.field is not None:
                widgets.field.set(core.row_value_text(row))
        self._show_state()

    def _show_state(self) -> None:
        """Show the label, the verdict, the saving and every member.

        The verdict and the saving change colour as well as text, because what
        they say is either what the application accepted, what it refused, or
        what has not been asked of it yet, and a user who has to read three
        lines to tell those apart is reading too much.

        What is wrong with a member is shown here too, and not with the
        explanations: a description says what a member is for and stays until
        the user asks for it to go, while a refusal is answered afresh by
        every pass and by every field that is left.
        """
        self._state.title.config(text=core.model_title(self._model))
        told(self._state.verdict, text=core.verdict_text(self._model),
             emphasis=core.verdict_emphasis(self._model))
        told(self._state.saving, text=core.save_text(self._model),
             emphasis=core.save_emphasis(self._model))
        for row, widgets in zip(self._model.rows, self._rows, strict=True):
            widgets.mark.config(text=core.row_marks(row))
        self._show_member_texts()


class TkEditor:  # pylint: disable=too-few-public-methods
    """Tkinter user interface backend for an edit model.

    The class has the single method that `EditorBackend` asks for, and
    deliberately nothing else: everything worth testing without a display
    lives in the core.
    """

    def __init__(self) -> None:
        """Create a backend that has not shown a model yet."""
        self._widgets: Optional[EditorWidgets] = None

    def run_editor(self, model: core.EditModel) -> None:
        """Show the model in a Tk window until the user closes it.

        The widgets are held for as long as the window lives, because they
        own the fields that the Tcl variables belong to. The window is this
        backend's own, which is why closing the editor destroys it.

        This is for an application that has no Tk of its own yet, because a
        second `tkinter.Tk` is a second Tcl interpreter and nothing can be
        shared between the two. An application that already runs Tk gets the
        entry point of section 8.2 of `doc/design.md` instead, which mounts
        the editor in a widget that application owns.

        Args:
            model: Model to show and to edit.
        """
        window = tkinter.Tk()
        window.title(model.config_type_name)
        self._widgets = EditorWidgets(parent=window, model=model)
        window.mainloop()


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
    """Edit one configuration in a Tk window, and return what was saved.

    This is `edit_cfg_json.edit` with this package's backend filled in, for
    an application that has already chosen Tkinter. Everything it does is
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
    return core.edit(config=config, backend=TkEditor(),
                     descriptions=descriptions, in_file=in_file, loader=loader,
                     out_file=out_file, policy=policy, settings=settings,
                     stderr_file=stderr_file)
