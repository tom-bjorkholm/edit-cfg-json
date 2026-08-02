#! /usr/bin/env python3
"""Plain text rendering of an edit model and of its individual values."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import json
from edit_cfg_json.edit_model import EditModel, MemberRow

NOT_EDITABLE_FORM = '<not editable yet: {kind}>'
"""Form of the value text of a member this version cannot edit."""


def row_value_text(row: MemberRow) -> str:
    """Return the value of one member as the text a field would show.

    A scalar is rendered as JSON, so that the user sees exactly what will
    land in the configuration file. A member that this version of the model
    cannot edit is named by its JSON kind instead of by its value, because
    a list or a dict needs more than one field.

    Args:
        row: Member to render.

    Returns:
        The value text of one member.
    """
    if not row.editable:
        return NOT_EDITABLE_FORM.format(kind=type(row.value).__name__)
    return json.dumps(row.value)


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
    return '\n'.join(f'{row.name} = {row_value_text(row)}'
                     for row in model.rows)
