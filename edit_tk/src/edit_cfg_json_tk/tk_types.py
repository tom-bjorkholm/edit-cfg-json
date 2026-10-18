#! /usr/bin/env python3
"""The pull-down that says which type one node holds.

Every row says the type it holds between its name and its value, which reads
as Python's `name: type = value`, and lists every type its declaration allows.
Nothing can be chosen in it yet: it is disabled on every row. It is a module
of its own because it is a piece of window with a life of its own — a button,
a menu, and what the two of them were last told — and because `tk_editor` is
the module of this backend that is nearest to being too long to read.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
import edit_cfg_json as core
from edit_cfg_json_tk.tk_look import fill_menu, menu_of, type_field


class TypeWidget:  # pylint: disable=too-few-public-methods
    """The pull-down of the types of one node, and what it offers.

    This is a class rather than a function because what it offers can change
    while the editor is open, and the menu then has to be given its entries
    again: a node whose declaration names nothing usable offers the one type
    its value has, and a value typed into it can be of another type.
    """

    def __init__(self, parent: tkinter.Misc, row: core.MemberRow,
                 width: int) -> None:
        """Create the pull-down of the types of one node.

        Args:
            parent: Line of the node that is being shown.
            row: Node to create the pull-down for.
            width: Width in characters of the column of the types, which every
                one of these is as wide as so that the values beside them
                begin in one column.
        """
        self._offered = core.row_type_texts(row)
        self.button = type_field(parent=parent, shown=core.row_type_text(row),
                                 width=width)
        self._menu = menu_of(pull_down=self.button, labels=self._offered)

    def show(self, row: core.MemberRow) -> None:
        """Show the type the node holds now, among what it may hold now.

        Args:
            row: Node whose type is being shown, as the model holds it now.
        """
        offered = core.row_type_texts(row)
        if offered != self._offered:
            self._offered = offered
            self._menu.delete(0, 'end')
            fill_menu(menu=self._menu, labels=offered)
        self.button.config(text=core.row_type_text(row))
