#! /usr/bin/env python3
"""Plain text rendering of an edit model and of its individual values."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from edit_cfg_json.edit_model import EditModel, MemberRow
from edit_cfg_json.leaf_value import value_as_text
from edit_cfg_json.validation import ValidationVerdict

NOT_EDITABLE_FORM = '<not editable yet: {kind}>'
"""Form of the value text of a member this version cannot edit."""

EDITED_MARK = ' (edited)'
"""Mark that follows the value of a member the user has changed."""

VALIDATOR_MARK = ' (changed by validator)'
"""Mark that follows the value of a member a validation pass rewrote."""

FILLED_MARK = ' (filled from default)'
"""Mark that follows the value of a member the input file did not hold."""

LOAD_MARK = ' (changed by the load)'
"""Mark that follows a value that reading the input file put there.

A file in an older format is what puts one there in practice: a key of it was
renamed into this member, or the rules for that format supplied the value. A
value that parsing or validating normalized is marked with this too.
"""

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

REFUSED_FORM = 'validation: invalid, see {names}'
"""Form of the line that names the members the application refused.

They are named here as well as marked below, because a configuration of any
size does not fit a window: a user who has just asked what the application
makes of these values should be told where to look rather than have to go
looking.
"""

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
"""What is written below a member is indented by this much.

The indentation is what says that the line belongs to the member above it
rather than being a member of its own. Every line of it gets one, because
what the type of a member says about it runs to more than one line.
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

    They say different things that can all be true at once: the input file did
    not hold this member, reading the file changed what it holds, the user
    changed it, and a validator then changed what the user had written. They
    are in the order in which they can happen. The two that a load sets are
    never both there, because the more precise of the two is the one it sets.

    Both backends read the marks from here, so that neither of them decides on
    its own what a member the load, the user or a validator touched looks like.

    Args:
        row: Member to mark.

    Returns:
        The marks of one member, empty when nothing has happened to it.
    """
    filled = FILLED_MARK if row.filled_from_default else ''
    loaded = LOAD_MARK if row.changed_by_load else ''
    edited = EDITED_MARK if row.edited else ''
    rewritten = VALIDATOR_MARK if row.changed_by_validator else ''
    return filled + loaded + edited + rewritten


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


def row_diagnostic(model: EditModel, row: MemberRow) -> str:
    """Return what is wrong with one member, and nothing when nothing is.

    Two things can be wrong with a member and they are not the same thing.
    Its text may mean no value of that member at all, which is answered by
    the member alone and stays true until the member is edited again; or the
    application may have refused the value it holds, which is answered by the
    whole configuration and is only known for as long as the rest of the
    buffer stands still. The first is preferred when both are there, because
    a value that does not exist yet is what has to be corrected first.

    Both backends read this from here, so that neither of them decides on its
    own what a refused member is told.

    Args:
        model: Model that the member belongs to.
        row: Member to report.

    Returns:
        What is wrong with that member, empty when nothing is known to be.
    """
    if row.conversion:
        return row.conversion
    verdict = model.verdict
    return '' if verdict is None else verdict.refused.get(row.name, '')


def _indented(text: str) -> str:
    """Return one text that belongs to a member, with every line indented.

    A line with nothing on it is left alone, because indenting it would put
    blank space where there is nothing to line up.
    """
    return '\n'.join(DESCRIPTION_INDENT + line if line else line
                     for line in text.split('\n'))


def _row_as_text(model: EditModel, row: MemberRow) -> str:
    """Return the line that shows one member, and what is said below it.

    The description comes before what is wrong with the member, because the
    description is part of the member and what is wrong comes and goes: a
    line that appears below everything moves nothing that is above it.
    """
    below = [row_description(model=model, row=row),
             row_diagnostic(model=model, row=row)]
    lines = [f'{row.name} = {row_value_text(row)}{row_marks(row)}']
    lines += [_indented(text) for text in below if text]
    return '\n'.join(lines)


def _state_line(verdict: ValidationVerdict) -> str:
    """Return the one line that says what the application made of a buffer.

    Args:
        verdict: What the last validation pass found.

    Returns:
        The state of the buffer, naming the members that were refused.
    """
    if verdict.refused:
        return REFUSED_FORM.format(names=', '.join(verdict.refused))
    state = VALID_STATE if verdict.valid else INVALID_STATE
    return VERDICT_FORM.format(state=state)


def verdict_text(model: EditModel) -> str:
    """Return what the last validation pass found, as text.

    A buffer that has not been validated since it last changed says so,
    because that is a third state and not a kind of success. What was refused
    about one member is shown beside that member instead of here, and this
    line names those members so that they can be found. What follows on the
    lines below is what the application said that is about no single member,
    and it can be there for an accepted buffer too, since a validator may
    remark on a value without refusing it.

    Args:
        model: Model whose validation state is reported.

    Returns:
        The state of the buffer, followed by any diagnostics.
    """
    verdict = model.verdict
    if verdict is None:
        return VERDICT_FORM.format(state=UNKNOWN_STATE)
    lines = [_state_line(verdict), verdict.diagnostics.strip()]
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
        what the load did, one line per member with its description and
        anything wrong with it below it, and then the validation state and
        the saving, without a trailing line break.
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
