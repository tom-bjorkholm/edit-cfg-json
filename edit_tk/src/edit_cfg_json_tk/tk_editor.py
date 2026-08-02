#! /usr/bin/env python3
"""Tkinter view of an edit model, with one editable field per member."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from typing import Optional
import tkinter
from edit_cfg_json import EditModel, MemberRow, model_title, row_value_text

NAME_COLUMN_WIDTH = 24
"""Width in characters of the column that holds the member names."""

PADDING = 4
"""Padding in pixels around the widgets of the editor."""


class EditorWidgets:  # pylint: disable=too-few-public-methods
    """The widgets that show one edit model below one parent widget.

    This is a class rather than a function because the fields have to be
    kept: a `tkinter.StringVar` unsets its Tcl variable when it is collected,
    and the field it belongs to would then lose both its text and the
    callback that writes it into the model. Keeping them together also gives
    an application that mounts these widgets in a window of its own a single
    object to hold on to.
    """

    def __init__(self, parent: tkinter.Misc, model: EditModel) -> None:
        """Create the label, one row per member and a close button.

        The parent is a widget and not a window, so that the same rows can
        later be mounted inside a window that an application owns itself.

        Args:
            parent: Widget that becomes the parent of the created widgets.
            model: Model to show and to edit.
        """
        self._model = model
        self._fields: list[tkinter.StringVar] = []
        self._label = tkinter.Label(parent, text=model_title(model))
        self._label.pack(pady=PADDING)
        for row in model.rows:
            self._add_row(parent=parent, row=row)
        window = parent.winfo_toplevel()
        tkinter.Button(parent, text='Close',
                       command=window.destroy).pack(pady=PADDING)

    @property
    def label_text(self) -> str:
        """Return the text that the label of the whole model shows."""
        return str(self._label.cget('text'))

    def _add_row(self, parent: tkinter.Misc, row: MemberRow) -> None:
        """Create the name widget and the value widget of one member."""
        line = tkinter.Frame(parent)
        line.pack(fill='x', padx=PADDING)
        tkinter.Label(line, text=row.name, width=NAME_COLUMN_WIDTH,
                      anchor='w').pack(side='left')
        if row.editable:
            self._add_field(parent=line, row=row)
            return
        tkinter.Label(line, text=row_value_text(row),
                      anchor='w').pack(side='left')

    def _add_field(self, parent: tkinter.Misc, row: MemberRow) -> None:
        """Create the field of one member and wire it to the model."""
        field = tkinter.StringVar(value=row_value_text(row))
        self._fields.append(field)
        tkinter.Entry(parent, textvariable=field).pack(side='left', fill='x',
                                                       expand=True)
        field.trace_add('write', self._writer(row=row, field=field))

    def _writer(self, row: MemberRow,
                field: tkinter.StringVar) -> Callable[..., None]:
        """Return the callback that writes one field into the model.

        Tk reports a change of the variable and not of the widget, so the
        callback reads the field itself. Every change is written through,
        including the ones that no key press caused, such as a paste.
        """
        def write_field(*trace_arguments: str) -> None:
            """Write the text of the field and show whether it changed."""
            _ = trace_arguments
            self._model.set_text(path=row.path, text=field.get())
            self._label.config(text=model_title(self._model))
        return write_field


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
