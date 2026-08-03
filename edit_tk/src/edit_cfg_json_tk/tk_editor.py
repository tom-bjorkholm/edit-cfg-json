#! /usr/bin/env python3
"""Tkinter view of an edit model, with one editable field per member."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from typing import NamedTuple, Optional, TextIO
import sys
import tkinter
from tkinter import filedialog
from config_as_json import Config, PathOrStr
from edit_cfg_json import EditModel, LoadPolicy, MemberRow, Settings, \
    SettingsSource, load_text, model_title, row_marks, row_value_text, \
    save_text, verdict_text
from edit_cfg_json import edit as core_edit
from edit_cfg_json_tk.key_names import tk_sequence

NAME_COLUMN_WIDTH = 24
"""Width in characters of the column that holds the member names."""

PADDING = 4
"""Padding in pixels around the widgets of the editor."""

VALIDATE_TEXT = 'Validate'
"""Text of the button that runs the validation of the application."""

SAVE_TEXT = 'Save'
"""Text of the button that writes the output file."""

SAVE_AS_TEXT = 'Save as...'
"""Text of the button that chooses an output file and then writes it."""

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


def _file_types(settings: Settings) -> list[tuple[str, str]]:
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


def _key_handler(command: Callable[[], None]) -> Callable[..., str]:
    """Return the callback that runs one command for one key event.

    Args:
        command: What that key does.

    Returns:
        A callback that Tk can bind, which stops the event from being
        handled a second time by whatever else the window is bound to.
    """
    def run_command(*event: object) -> str:
        """Run the command, and keep the event from being handled again."""
        _ = event
        command()
        return 'break'
    return run_command


def _bind_key(window: tkinter.Misc, key: str,
              command: Callable[[], None]) -> None:
    """Bind one key combination of one action, if Tk can bind it.

    A combination that the translation does not know, or that Tk refuses,
    leaves that action without that key rather than without an editor: every
    action of this backend has a button as well.

    Args:
        window: Window that the binding is made on.
        key: One key combination, as `ActionSettings` writes them.
        command: What that key does.
    """
    sequence = tk_sequence(key)
    if sequence is None:
        return
    try:
        window.bind(sequence, _key_handler(command))
    except tkinter.TclError:
        # Tk refuses an event sequence it cannot parse, and a key the
        # application named is not worth an editor that does not open.
        pass


class RowWidgets(NamedTuple):
    """The widgets that one configuration member owns."""

    field: Optional[tkinter.StringVar]
    """The field of an editable member, and None for every other member."""

    mark: tkinter.Label
    """The widget that says what has happened to this member."""


class EditorWidgets:  # pylint: disable=too-few-public-methods
    """The widgets that show one edit model below one parent widget.

    This is a class rather than a function because the fields have to be
    kept: a `tkinter.StringVar` unsets its Tcl variable when it is collected,
    and the field it belongs to would then lose both its text and the
    callback that writes it into the model. Keeping them together also gives
    an application that mounts these widgets in a window of its own a single
    object to hold on to.

    The widgets of the members are kept in the order the model reports its
    rows in, which is the order they were created in. This version of the
    model neither adds nor removes a row, so the two orders stay the same
    one and the pairing is checked rather than assumed.
    """

    def __init__(self, parent: tkinter.Misc, model: EditModel) -> None:
        """Create the label, one row per member, the verdict and the buttons.

        The parent is a widget and not a window, so that the same rows can
        later be mounted inside a window that an application owns itself.

        Args:
            parent: Widget that becomes the parent of the created widgets.
            model: Model to show and to edit.
        """
        self._model = model
        self._label = tkinter.Label(parent, text=model_title(model))
        self._label.pack(pady=PADDING)
        self._add_load_message(parent)
        self._rows = [self._add_row(parent=parent, row=row)
                      for row in model.rows]
        self._verdict = tkinter.Label(parent, text=verdict_text(model),
                                      anchor='w', justify='left')
        self._verdict.pack(fill='x', padx=PADDING, pady=PADDING)
        self._saving = tkinter.Label(parent, text=save_text(model), anchor='w',
                                     justify='left')
        self._saving.pack(fill='x', padx=PADDING)
        self._add_buttons(parent)
        self._bind_keys(parent.winfo_toplevel())

    @property
    def label_text(self) -> str:
        """Return the text that the label of the whole model shows."""
        return str(self._label.cget('text'))

    @property
    def verdict_text_shown(self) -> str:
        """Return the text that the validation part of the editor shows."""
        return str(self._verdict.cget('text'))

    @property
    def save_text_shown(self) -> str:
        """Return the text that the saving part of the editor shows."""
        return str(self._saving.cget('text'))

    def _add_load_message(self, parent: tkinter.Misc) -> None:
        """Show what reading the input file did, when it did anything.

        The widget is created only when there is something to say. The file
        was read before the model was built, so the message cannot arrive
        later, and an empty widget would take a line of the window for a
        message that will never come.
        """
        message = load_text(self._model)
        if message:
            tkinter.Label(parent, text=message, anchor='w',
                          justify='left').pack(fill='x', padx=PADDING)

    def _add_buttons(self, parent: tkinter.Misc) -> None:
        """Create the buttons that validate, save and end the run.

        They share one row, because four buttons stacked above each other
        would push the values of a real configuration off the window.
        """
        window = parent.winfo_toplevel()
        line = tkinter.Frame(parent)
        line.pack(pady=PADDING)
        for text, command in ((VALIDATE_TEXT, self._validate),
                              (SAVE_TEXT, self._save),
                              (SAVE_AS_TEXT, self._save_as),
                              (CLOSE_TEXT, window.destroy)):
            tkinter.Button(line, text=text, command=command).pack(side='left',
                                                                  padx=PADDING)

    def _bind_keys(self, window: tkinter.Misc) -> None:
        """Bind the key combinations that the application chose.

        The bindings are made on the window and not on each field, because
        a key that a field does not use for itself reaches the window that
        the field is in. Nothing is bound for the cancel action: the only
        question this backend asks is the toolkit's own file dialog, which
        answers that key itself.

        The keys are read once, here, which is the whole of what a later
        answer from a settings callable cannot change.

        Args:
            window: Window that the bindings are made on.
        """
        actions = self._model.settings.actions
        for keys, command in ((actions.quit, window.destroy),
                              (actions.validate, self._validate),
                              (actions.save, self._save),
                              (actions.save_as, self._save_as)):
            for key in keys:
                _bind_key(window=window, key=key, command=command)

    def _add_row(self, parent: tkinter.Misc, row: MemberRow) -> RowWidgets:
        """Create the name widget, the value widget and the mark widget."""
        line = tkinter.Frame(parent)
        line.pack(fill='x', padx=PADDING)
        tkinter.Label(line, text=row.name, width=NAME_COLUMN_WIDTH,
                      anchor='w').pack(side='left')
        field = self._add_value(parent=line, row=row)
        mark = tkinter.Label(line, text=row_marks(row), anchor='w')
        mark.pack(side='left')
        return RowWidgets(field=field, mark=mark)

    def _add_value(self, parent: tkinter.Misc,
                   row: MemberRow) -> Optional[tkinter.StringVar]:
        """Create the value widget of one member and wire it to the model.

        A member that the model cannot edit yet gets a widget that only
        shows text, because there is nothing the user could do to it.
        """
        if not row.editable:
            tkinter.Label(parent, text=row_value_text(row),
                          anchor='w').pack(side='left')
            return None
        field = tkinter.StringVar(value=row_value_text(row))
        tkinter.Entry(parent, textvariable=field).pack(side='left', fill='x',
                                                       expand=True)
        field.trace_add('write', self._writer(row=row, field=field))
        return field

    def _writer(self, row: MemberRow,
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

    def _refresh(self) -> None:
        """Write the buffer back into the fields and show the new state.

        A pass over the buffer is not read only: a member validator returns
        the value that is stored back into the member, so a value can end up
        different from the one the user typed. Writing the text the model
        already holds into a field is not an edit, so this refresh does not
        undo the marks that the pass has just set.
        """
        for row, widgets in zip(self._model.rows, self._rows, strict=True):
            if widgets.field is not None:
                widgets.field.set(row_value_text(row))
        self._show_state()

    def _show_state(self) -> None:
        """Show the label, the verdict, the saving and every member mark."""
        self._label.config(text=model_title(self._model))
        self._verdict.config(text=verdict_text(self._model))
        self._saving.config(text=save_text(self._model))
        for row, widgets in zip(self._model.rows, self._rows, strict=True):
            widgets.mark.config(text=row_marks(row))


class TkEditor:  # pylint: disable=too-few-public-methods
    """Tkinter user interface backend for an edit model.

    The class has the single method that `EditorBackend` asks for, and
    deliberately nothing else: everything worth testing without a display
    lives in the core.
    """

    def __init__(self) -> None:
        """Create a backend that has not shown a model yet."""
        self._widgets: Optional[EditorWidgets] = None

    def run_editor(self, model: EditModel) -> None:
        """Show the model in a Tk window until the user closes it.

        The widgets are held for as long as the window lives, because they
        own the fields that the Tcl variables belong to.

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
def edit(config: Config, *, in_file: Optional[PathOrStr] = None,
         out_file: Optional[PathOrStr] = None,
         policy: LoadPolicy = LoadPolicy.STRICT_THEN_DEFAULTS,
         settings: SettingsSource = Settings(),
         stderr_file: TextIO = sys.stderr) -> Optional[Config]:
    """Edit one configuration in a Tk window, and return what was saved.

    This is `edit_cfg_json.edit` with this package's backend filled in, for
    an application that has already chosen Tkinter. Everything it does is
    documented there.

    Args:
        config: Configuration object to edit. It is never modified.
        in_file: File to read, or None to start from the declared defaults.
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
    return core_edit(config=config, backend=TkEditor(), in_file=in_file,
                     out_file=out_file, policy=policy, settings=settings,
                     stderr_file=stderr_file)
