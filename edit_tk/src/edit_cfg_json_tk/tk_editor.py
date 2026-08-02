#! /usr/bin/env python3
"""Read-only Tkinter view of an edit model."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from edit_cfg_json import EditModel, MemberRow, row_value_text

NAME_COLUMN_WIDTH = 24
"""Width in characters of the column that holds the member names."""

PADDING = 4
"""Padding in pixels around the widgets of the editor."""


def _add_row(parent: tkinter.Misc, row: MemberRow) -> None:
    """Create the name and the value widget for one configuration member."""
    line = tkinter.Frame(parent)
    line.pack(fill='x', padx=PADDING)
    tkinter.Label(line, text=row.name, width=NAME_COLUMN_WIDTH,
                  anchor='w').pack(side='left')
    tkinter.Label(line, text=row_value_text(row), anchor='w').pack(side='left')


def build_editor_widgets(parent: tkinter.Misc, model: EditModel) -> None:
    """Create the read-only rows and a close button under one parent.

    The parent is a widget and not a window, so that the same rows can later
    be mounted inside a window that an application owns itself.

    Args:
        parent: Widget that becomes the parent of the created widgets.
        model: Model to show.
    """
    tkinter.Label(parent, text=model.config_type_name).pack(pady=PADDING)
    for row in model.rows:
        _add_row(parent=parent, row=row)
    window = parent.winfo_toplevel()
    tkinter.Button(parent, text='Close',
                   command=window.destroy).pack(pady=PADDING)


class TkEditor:  # pylint: disable=too-few-public-methods
    """Tkinter user interface backend for an edit model.

    The class has the single method that `EditorBackend` asks for, and
    deliberately nothing else: everything worth testing without a display
    lives in the core.
    """

    def run_editor(self, model: EditModel) -> None:
        """Show the model in a Tk window until the user closes it.

        Args:
            model: Model to show.
        """
        window = tkinter.Tk()
        window.title(model.config_type_name)
        build_editor_widgets(parent=window, model=model)
        window.mainloop()
