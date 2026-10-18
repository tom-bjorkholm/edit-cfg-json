#! /usr/bin/env python3
"""The pull-down that says which type one node holds, and lets it be chosen.

Every row says the type it holds between its name and its value, which reads
as Python's `name: type = value`, and lists every type its declaration allows.
Where the type is the user's to choose, picking one of them is what changes
it; everywhere else the pull-down is disabled. It is a module of its own
because it is a piece of window with a life of its own — a button, a menu, and
what the two of them were last told — and because `tk_editor` is the module of
this backend that is nearest to being too long to read.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
import tkinter
import edit_cfg_json as core
from edit_cfg_json_tk.tk_look import TREE_INDENT, fill_menu, menu_of, \
    row_font, type_field


def type_widths(parent: tkinter.Misc,
                model: core.EditModel) -> tuple[int, ...]:
    """Return how wide in pixels the pull-down of the types of each row is.

    They are measured in the font the pull-downs write their types in, because
    the characters of that font are not all as wide as each other, and a type
    is mostly narrow letters and brackets.

    Args:
        parent: Widget of the editor, whose interpreter has the font.
        model: Model whose rows are being shown.

    Returns:
        The width of the text of the pull-down of each row, in the order of
        `EditModel.rows`.
    """
    return core.type_column_widths(model, measure=row_font(parent).measure,
                                   indent=TREE_INDENT)


class TypeWidget:  # pylint: disable=too-few-public-methods
    """The pull-down of the types of one node, and what it offers.

    This is a class rather than a function because what it offers can change
    while the editor is open, and the menu then has to be given its entries
    again: a node whose declaration names nothing usable offers the one type
    its value has, and a value typed into it can be of another type.
    """

    def __init__(self, parent: tkinter.Misc, row: core.MemberRow, width: int,
                 blank: tkinter.PhotoImage,
                 picked: Callable[[str], None]) -> None:
        """Create the pull-down of the types of one node.

        Args:
            parent: Line of the node that is being shown.
            row: Node to create the pull-down for.
            width: Width in pixels of the text of this pull-down, which is
                what `type_widths` gives the row, so that the column of the
                types ends in one place and the values begin in one column.
            blank: The image from `edit_cfg_json_tk.tk_look.blank_image`.
            picked: What choosing a type does, given the whole of that type as
                a Python type hint spells it. A menu entry says the type as the
                column shows it, which is cut where it is long, so each entry
                carries the whole type it stands for.
        """
        self._picked = picked
        self._offered = core.row_type_choices(row)
        self.button = type_field(parent=parent, shown=core.row_type_text(row),
                                 width=width,
                                 active=core.row_chooses_type(row),
                                 blank=blank)
        self._menu = menu_of(pull_down=self.button, entries=self._offered,
                             picked=picked)

    def show(self, row: core.MemberRow) -> None:
        """Show the type the node holds now, among what it may hold now.

        Args:
            row: Node whose type is being shown, as the model holds it now.
        """
        offered = core.row_type_choices(row)
        if offered != self._offered:
            self._offered = offered
            self._menu.delete(0, 'end')
            fill_menu(menu=self._menu, entries=offered, picked=self._picked)
        self.button.config(text=core.row_type_text(row))
