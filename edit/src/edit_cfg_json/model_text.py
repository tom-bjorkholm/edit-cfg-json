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

SAVE_TO_FORM = 'save to: {name}'
"""Form of the line that says where saving would write."""

NO_DESTINATION_TEXT = 'save to: no file chosen yet'
"""Line shown while no output file has been chosen."""

SUMMARY_SEPARATOR = ' - '
"""What separates the label of the configuration from its summary.

They share one line while the explanations are hidden, because the summary is
one line for the whole configuration and hiding it would save nothing.
"""

DESCRIPTION_INDENT = '    '
"""What the description of a member is indented by, below that member.

The indentation is what says that the line belongs to the member above it
rather than being a member of its own.
"""


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


def docstring_text(model: EditModel) -> str:
    """Return what the configuration class says about itself, as it is shown.

    The summary while the explanations are hidden and the whole docstring
    while they are shown, which is what the toggle of the model is for: the
    summary is one line for the whole configuration and is worth keeping,
    and the rest of the docstring is what a user who knows this
    configuration wants out of the way.

    Both backends show this, so that neither of them decides on its own how
    much of a docstring the user is offered.

    Args:
        model: Model whose configuration class is reported.

    Returns:
        The text to show for the configuration object, and nothing at all
        when its class has no docstring of its own.
    """
    return model.docstring if model.explanations_shown else model.summary


def row_description(model: EditModel, row: MemberRow) -> str:
    """Return what the application says about one member, as it is shown.

    It is the description of the member while the explanations are shown, and
    nothing while they are hidden. Which of the two it is belongs to the
    model, so that the two backends cannot hide different things.

    Args:
        model: Model that the member belongs to.
        row: Member to describe.

    Returns:
        The description of one member, empty while it is not being shown or
        when the application said nothing about that member.
    """
    return row.description if model.explanations_shown else ''


def _row_as_text(model: EditModel, row: MemberRow) -> str:
    """Return the line that shows one member, and its description below it."""
    line = f'{row.name} = {row_value_text(row)}{row_marks(row)}'
    description = row_description(model=model, row=row)
    if not description:
        return line
    return f'{line}\n{DESCRIPTION_INDENT}{description}'


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


def save_text(model: EditModel) -> str:
    """Return what saving did, or where it would write if it were asked.

    Before anything has been saved there is still something to say, because
    where a save would go is the one thing a user cannot see from the values
    themselves, and there is a real difference between a destination that is
    waiting and no destination at all.

    Both backends show this, so that neither of them decides on its own what
    the user is told about the output file.

    Args:
        model: Model whose saving is reported.

    Returns:
        What the last attempt to save did, or where saving would write.
    """
    if model.save_message:
        return model.save_message
    if model.out_file is None:
        return NO_DESTINATION_TEXT
    return SAVE_TO_FORM.format(name=model.out_file)


def _head_text(model: EditModel) -> str:
    """Return the label of the configuration and what its class says.

    The two share a line while the explanations are hidden and take a line
    each while they are shown, because the whole docstring is more than one
    line whenever it is more than the summary.

    Args:
        model: Model whose configuration object is labelled.

    Returns:
        The label of the configuration, with as much of its docstring as is
        being shown.
    """
    title = model_title(model)
    explanation = docstring_text(model)
    if not explanation:
        return title
    if model.explanations_shown:
        return f'{title}\n{explanation}'
    return f'{title}{SUMMARY_SEPARATOR}{explanation}'


def model_as_text(model: EditModel) -> str:
    """Return the whole model as text, one line per configuration member.

    The configuration object labels itself first, because what the whole
    configuration is for is what the members below it are read in the light
    of. What reading the input file did comes next, because it is what
    explains the marks on those members. The validation state of the buffer
    follows them, and the saving after that, in the order in which a session
    reaches them, so that a rendering never leaves it unsaid what the
    application would make of what is shown or where it would be written.
    This is the rendering used by the examples and by the tests, so that
    every step of the editor can be observed without a display. It belongs
    to the core rather than to a backend because it is user interface
    agnostic.

    Args:
        model: Model to render.

    Returns:
        The label of the configuration and what its class says about itself,
        what the load did, one line per member with its description below it,
        and then the validation state and the saving, without a trailing line
        break.
    """
    rows = [_row_as_text(model=model, row=row) for row in model.rows]
    lines = [_head_text(model), load_text(model)] + rows + \
        [verdict_text(model), save_text(model)]
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
