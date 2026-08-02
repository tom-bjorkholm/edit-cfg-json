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

VALIDATOR_MARK = ' (changed by validator)'
"""Mark that follows the value of a member a validation pass rewrote."""

FILLED_MARK = ' (filled from default)'
"""Mark that follows the value of a member the input file did not hold."""

DIRTY_MARK = ' *'
"""Mark that follows the model label while the buffer has changes."""

VERDICT_FORM = 'validation: {state}'
"""Form of the line that reports what the last validation pass found."""

VALID_STATE = 'valid'
"""State of a buffer that the application itself would accept."""

INVALID_STATE = 'invalid'
"""State of a buffer that the application itself would refuse."""

UNKNOWN_STATE = 'not validated'
"""State of a buffer that has not been validated since it last changed."""


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


def row_marks(row: MemberRow) -> str:
    """Return the marks that follow the value of one member.

    Every mark can be shown at once, because they say three different things
    that can all be true: the input file did not hold this member, the user
    changed it, and a validator then changed what the user had written. They
    are in the order in which they can happen. Both backends read the marks
    from here, so that neither of them decides on its own what a member the
    load, the user or a validator touched looks like.

    Args:
        row: Member to mark.

    Returns:
        The marks of one member, empty when nothing has happened to it.
    """
    filled = FILLED_MARK if row.filled_from_default else ''
    edited = EDITED_MARK if row.edited else ''
    rewritten = VALIDATOR_MARK if row.changed_by_validator else ''
    return filled + edited + rewritten


def _row_as_text(row: MemberRow) -> str:
    """Return the one line of text that shows the state of one member."""
    return f'{row.name} = {row_value_text(row)}{row_marks(row)}'


def verdict_text(model: EditModel) -> str:
    """Return what the last validation pass found, as text.

    A buffer that has not been validated since it last changed says so,
    because that is a third state and not a kind of success. The
    diagnostics follow on the lines below, and they can be present for an
    accepted buffer too, since a validator may remark on a value without
    refusing it.

    Args:
        model: Model whose validation state is reported.

    Returns:
        The state of the buffer, followed by any diagnostics.
    """
    verdict = model.verdict
    if verdict is None:
        return VERDICT_FORM.format(state=UNKNOWN_STATE)
    state = VALID_STATE if verdict.valid else INVALID_STATE
    lines = [VERDICT_FORM.format(state=state), verdict.diagnostics.strip()]
    return '\n'.join(line for line in lines if line)


def load_text(model: EditModel) -> str:
    """Return what reading the input file did, or an empty text.

    Both backends show this, so that the two of them cannot tell the user
    two different things about one file.

    Args:
        model: Model whose load is reported.

    Returns:
        What the load did, and nothing at all when it did nothing worth
        saying.
    """
    return model.load_message


def model_as_text(model: EditModel) -> str:
    """Return the whole model as text, one line per configuration member.

    What reading the input file did comes before the members, because it is
    what explains the marks on them. The validation state of the buffer
    follows them, so that a rendering never leaves it unsaid what the
    application would make of what is shown. This is the rendering used by
    the examples and by the tests, so that every step of the editor can be
    observed without a display. It belongs to the core rather than to a
    backend because it is user interface agnostic.

    Args:
        model: Model to render.

    Returns:
        What the load did, one line per member and then the validation
        state, without a trailing line break.
    """
    rows = [_row_as_text(row) for row in model.rows]
    lines = [load_text(model)] + rows + [verdict_text(model)]
    return '\n'.join(line for line in lines if line)


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
