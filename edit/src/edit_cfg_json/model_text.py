#! /usr/bin/env python3
"""Plain text rendering of an edit model and of its individual values."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from edit_cfg_json.edit_model import EditModel, MemberRow
from edit_cfg_json.leaf_value import value_as_text

NOT_EDITABLE_FORM = '<not editable yet: {kind}>'
"""Form of the value text of a member this version cannot edit."""

EDITED_MARK = ' (edited)'
"""Mark that follows the value of a member the user has changed."""

DIRTY_MARK = ' *'
"""Mark that follows the model label while the buffer has changes."""


def row_value_text(row: MemberRow) -> str:
    """Return the value of one member as the text a field would show.

    A member that this version of the model cannot edit is named by its kind
    instead of by its value, because a list or a dict needs more than one
    field. Every other member shows the text of the value it holds.

    Args:
        row: Member to render.

    Returns:
        The value text of one member.
    """
    if not row.editable:
        return NOT_EDITABLE_FORM.format(kind=type(row.original).__name__)
    return value_as_text(row.value)


def _row_as_text(row: MemberRow) -> str:
    """Return the one line of text that shows the state of one member."""
    mark = EDITED_MARK if row.edited else ''
    return f'{row.name} = {row_value_text(row)}{mark}'


def model_as_text(model: EditModel) -> str:
    """Return the whole model as one text line per configuration member.

    This is the rendering used by the examples and by the tests, so that
    every step of the editor can be observed without a display. It belongs
    to the core rather than to a backend because it is user interface
    agnostic.

    Args:
        model: Model to render.

    Returns:
        One line per member, without a trailing line break.
    """
    return '\n'.join(_row_as_text(row) for row in model.rows)


def model_title(model: EditModel) -> str:
    """Return the label of the whole model, marked while it has changes.

    Both backends show this, so that neither of them decides on its own how
    an unsaved change looks.

    Args:
        model: Model to label.

    Returns:
        The class name of the configuration, with a mark while there are
        changes that are worth saving.
    """
    return model.config_type_name + (DIRTY_MARK if model.dirty else '')
