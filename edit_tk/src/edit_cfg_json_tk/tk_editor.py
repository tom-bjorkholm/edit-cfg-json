#! /usr/bin/env python3
"""Tkinter view of an edit model, with one editable field per member."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from typing import NamedTuple, Optional
import tkinter
from edit_cfg_json import EditModel, MemberRow, model_title, row_marks, \
    row_value_text, verdict_text

NAME_COLUMN_WIDTH = 24
"""Width in characters of the column that holds the member names."""

PADDING = 4
"""Padding in pixels around the widgets of the editor."""

VALIDATE_TEXT = 'Validate'
"""Text of the button that runs the validation of the application."""

CLOSE_TEXT = 'Close'
"""Text of the button that ends the editor."""


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
        self._rows = [self._add_row(parent=parent, row=row)
                      for row in model.rows]
        self._verdict = tkinter.Label(parent, text=verdict_text(model),
                                      anchor='w', justify='left')
        self._verdict.pack(fill='x', padx=PADDING, pady=PADDING)
        self._add_buttons(parent)

    @property
    def label_text(self) -> str:
        """Return the text that the label of the whole model shows."""
        return str(self._label.cget('text'))

    @property
    def verdict_text_shown(self) -> str:
        """Return the text that the validation part of the editor shows."""
        return str(self._verdict.cget('text'))

    def _add_buttons(self, parent: tkinter.Misc) -> None:
        """Create the button that validates and the one that ends the run."""
        window = parent.winfo_toplevel()
        tkinter.Button(parent, text=VALIDATE_TEXT,
                       command=self._validate).pack(pady=PADDING)
        tkinter.Button(parent, text=CLOSE_TEXT,
                       command=window.destroy).pack(pady=PADDING)

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
        """Validate the buffer and show what the application would say.

        The fields are written back from the model afterwards, because a
        validation pass is not read only: a member validator returns the
        value that is stored back into the member, so a value can end up
        different from the one the user typed. Writing the text the model
        already holds into a field is not an edit, so this refresh does not
        undo the marks that the pass has just set.
        """
        self._model.validate()
        for row, widgets in zip(self._model.rows, self._rows, strict=True):
            if widgets.field is not None:
                widgets.field.set(row_value_text(row))
        self._show_state()

    def _show_state(self) -> None:
        """Show the label, the verdict and the mark of every member."""
        self._label.config(text=model_title(self._model))
        self._verdict.config(text=verdict_text(self._model))
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
