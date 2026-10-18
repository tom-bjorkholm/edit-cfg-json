#! /usr/bin/env python3
"""How the column of the types shows the type of every row of an edit model.

Every row says the type it holds between its name and its value, in a
pull-down that lists every type it may hold. What is here is what both
backends ask of that column: the text each type is shown as, which of them a
row offers, whether choosing is the user's to do, and how wide the pull-down
of each row is. It is a module of its own because it is one thing the backends
lay out, and `model_text` holds the rendering of everything else.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from edit_cfg_json.edit_model import EditModel
from edit_cfg_json.rows import MemberRow
from edit_cfg_json.type_options import cut_type_text


def row_type_text(row: MemberRow) -> str:
    """Return the type one node holds, as the column of the types shows it.

    It is the type the node holds now and not the whole of what its
    declaration allows, which the line below it says where it allows more
    than one. A type longer than the column is cut, and that line then says
    the whole of it.

    Args:
        row: Node to render.

    Returns:
        The type that node holds, as the column shows it.
    """
    return cut_type_text(row.chosen_type.text)


def row_type_choices(row: MemberRow) -> tuple[tuple[str, str], ...]:
    """Return every type one node may hold, as shown and as it is named.

    They are what the pull-down of the types offers, in the order the
    declaration writes them, and then the type the node holds where that is
    none of them: the one type its value has where nothing usable is
    declared, and `None` for a place declared to hold an object and holding
    none.

    Each is given twice, because the column cuts a long type and two types
    can be cut to the same text: what the pull-down shows, and the whole of
    the type, which is what `EditModel.set_type` is given when it is chosen.

    Args:
        row: Node to render.

    Returns:
        One pair of the shown text and the whole text per type that node may
        hold, the type it holds among them.
    """
    held = row.chosen_type
    options = row.types if held in row.types else (*row.types, held)
    return tuple((cut_type_text(option.text), option.text)
                 for option in options)


def row_type_texts(row: MemberRow) -> tuple[str, ...]:
    """Return every type one node may hold, as the column shows each of them.

    Args:
        row: Node to render.

    Returns:
        The shown text of every type `row_type_choices` lists, among them
        `row_type_text`.
    """
    return tuple(shown for shown, _ in row_type_choices(row))


def row_chooses_type(row: MemberRow) -> bool:
    """Return whether the type one node holds can be chosen in its pull-down.

    Every node has the pull-down, so that every row says its type in the same
    place, and this is what says whether it is active: a node whose
    declaration allows more than one plain type, or a plain type and `None`.
    A backend asks it whenever it makes the pull-down, because whether it is
    active depends on the types the node may hold and on nothing a user types.

    Args:
        row: Node to ask about.

    Returns:
        Whether choosing another of its types is something the user may do.
    """
    return row.type_choosable


def type_column_widths(model: EditModel, measure: Callable[[str], int],
                       indent: int) -> tuple[int, ...]:
    """Return how wide the pull-down of the types of each row is.

    The column of the types ends in one place for the whole editor, so that
    the values of every row begin in one column: where the longest type any
    row may hold ends, after the indentation of that row. A row is indented
    once for every container it is inside, so its pull-down is narrower by as
    much, and the types of a deep row are the short ones inside a container
    whose own type is long. The cut keeps each type to
    `edit_cfg_json.type_options.TYPE_COLUMN_LIMIT` characters. Every row is
    asked and not only the ones on the screen, so that folding a container
    never moves the values of the rows beside it.

    The widths are in the unit the backend measures in, which is a cell of a
    terminal for one and a pixel of a proportional font for another.

    Args:
        model: Model to ask about.
        measure: How wide one text is.
        indent: How far one step into a container indents a row.

    Returns:
        The width of the pull-down of each row, in the order of
        `EditModel.rows`, without whatever the pull-down draws beside its
        text.
    """
    end = max((row.depth * indent + max(map(measure, row_type_texts(row)))
               for row in model.rows), default=0)
    return tuple(end - row.depth * indent for row in model.rows)
