#! /usr/bin/env python3
"""Plain text rendering of an edit model and of its individual values."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from edit_cfg_json.descriptions import class_docstring, class_summary
from edit_cfg_json.edit_model import EditModel
from edit_cfg_json.rows import MemberRow
from edit_cfg_json.tree import path_text
from edit_cfg_json.validation import ValidationVerdict

FOLDED_MARK = ' (folded)'
"""What follows a container whose rows are hidden.

The two backends say this with a control that the user presses instead, which
is the wording each of them owns. This rendering has nowhere to put a control,
so it says it in words: a container that is folded is showing less than it
holds, and a reader who is not told that would read the values as all of them.
"""

EDITED_MARK = ' (edited)'
"""Mark that follows the value of a member the user has changed."""

VALIDATOR_MARK = ' (changed by validator)'
"""Mark that follows the value of a member a validation pass rewrote."""

FILLED_MARK = ' (filled from default)'
"""Mark that follows the value of a member the input file did not hold."""

LOAD_FORM = ' ({reason})'
"""Form of the mark that follows a value reading the input file put there.

A file in an older format is what puts one there in practice: a key of it was
renamed into this member, or the rules for that format supplied the value. A
value that parsing or validating normalized is marked with this too. What is
in it is what the model says the load did to that member, which is the words
of the record where the load recorded one.
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
"""Form of the line that names the nodes the application refused.

They are named here as well as marked below, because a configuration of any
size does not fit a window: a user who has just asked what the application
makes of these values should be told where to look rather than have to go
looking. A value inside a list or a dict is named by its whole path, because
its own name says nothing about where it is.
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
"""What is written below a node is indented by this much.

The indentation is what says that the line belongs to the node above it
rather than being a node of its own. Every line of it gets one, because
what the type of a node says about it runs to more than one line.
"""

TREE_INDENT = '    '
"""What each step further inside a list or a dict is indented by.

It is the same width as the indentation of the explanatory text, so that a
value inside a container and a sentence about the container line up. They are
told apart by their shape rather than by their place: a row has a name and a
value, and a sentence has neither.
"""

LEAF_FORM = '{indent}{name} = {value}{marks}'
"""Form of the line that shows one value of the configuration."""

CONTAINER_FORM = '{indent}{name}: {value}{folded}{marks}{subtree}'
"""Form of the line that shows one node that is not edited in a field.

A colon and not an equals sign, because what follows is not the value: for a
list, a dict or a nested configuration object the value is on the rows below,
and this says how many of them there are or which class they belong to.
"""

SUBTREE_VALID_MARK = ' [valid on its own]'
"""What a nested object that is a configuration on its own says.

*On its own* is the whole of what it claims, and the words are there because
of what it must not be read as. The configuration holding this object may be
refused for a reason that is about nothing inside it — a rule of the class
above relating this object to another one is exactly that — so this says
nothing at all about whether the file can be written. That is the line below
the members, and it is the only thing that answers it.
"""

SUBTREE_REFUSED_MARK = ' [refused on its own]'
"""What a nested object that its own class refuses says.

The other way round holds without qualification: an object its own class
refuses cannot be part of a configuration that is saved. What is wrong with it
is at the member it is about, or below the object where it is about no member
of it.
"""

INSIDE_VALID_MARK = ' [valid inside]'
"""What a list or a dict of configuration objects says when all of them pass.

A container is no configuration and can say nothing about itself, so what it
says is about the objects it holds. *Inside* is what keeps the two apart: a
rule of the class above may refuse the configuration while every object in this
container is a perfectly good one, exactly as it may for a single object.
"""

INSIDE_REFUSED_MARK = ' [refused inside]'
"""What such a container says when one of the objects it holds is refused.

It is on the row of the container because that row is what a folded container
leaves on the screen. Without it, folding a member would hide the one thing the
user has to act on and leave nothing at all in its place, and a user who folds
a member to get it out of the way is not asking to be told that everything in
it is fine.

What is wrong is still at the object it is about, and is read by opening the
container: this says that there is something to open it for.
"""


def row_value_text(row: MemberRow) -> str:
    """Return the value of one node as the text a field would show.

    A nested configuration object says its class, a list or a dict says how
    much it holds because its value is on the rows below it, and a declared
    member holding no object says which class is missing. Every other node
    shows the text of the value it holds.

    Both backends read it from here, so that neither of them decides on its
    own what a node that is not a value looks like.

    Args:
        row: Node to render.

    Returns:
        The value text of one node.
    """
    return row.value_text


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
    loaded = LOAD_FORM.format(reason=row.load_reason) \
        if row.load_reason else ''
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


def _class_text(row: MemberRow) -> str:
    """Return what the class of one nested configuration object says.

    The whole docstring while the object is open and the summary while it is
    folded, which is the same thing folding does to the values: a node that is
    showing less of itself says less about itself. A declared member that holds
    no object is never open, so it says the summary of the class it is missing.

    Args:
        row: Node to describe.

    Returns:
        What that class says about itself, and nothing for a node that is no
        configuration object and for a class with no docstring of its own.
    """
    if row.config_type is None:
        return ''
    if row.foldable and not row.folded:
        return class_docstring(row.config_type)
    return class_summary(row.config_type)


def row_describes(row: MemberRow) -> bool:
    """Return whether anything can ever be said below one node.

    A backend asks this before it creates the widget that says it, because a
    widget which could never hold anything is a line of the window spent on
    nothing. It is asked of the core rather than worked out by each backend,
    since what is said below a node is the core's to decide: the description
    the row carries is not the whole of it once a nested configuration object
    has a class docstring of its own.

    Args:
        row: Node to ask about.

    Returns:
        Whether the application, the type of the node or the class of the
        object at it has anything to say.
    """
    return bool(row.description) or bool(
        row.config_type is not None and class_docstring(row.config_type))


def row_description(model: EditModel, row: MemberRow) -> str:
    """Return what is said about one node, as it is shown.

    It is what the application said about the node and what the type of the
    node says, while the explanations are shown, and nothing while they are
    hidden. Which of the two it is belongs to the model, so that the two
    backends cannot hide different things.

    A nested configuration object says what its own class says as well, and
    how much of that is said depends on whether the node is open. That is why
    it is put together here rather than carried by the row: what a row says
    about itself cannot depend on the fold state that is stamped onto it
    afterwards.

    Args:
        model: Model that the node belongs to.
        row: Node to describe.

    Returns:
        What is said below that node, empty while it is not being shown or
        when there is nothing to say about it.
    """
    if not model.explanations_shown:
        return ''
    said = [row.description, _class_text(row)]
    return '\n'.join(line for line in said if line)


def row_validates(row: MemberRow) -> bool:
    """Return whether one node can ever say what its objects amount to.

    A backend asks this before it creates the widget that says it, by the same
    rule as `row_describes`: a widget that could never hold anything is a
    piece of the window spent on nothing.

    A declared nested configuration object that is really there can, and so
    can a list or a dict that holds such objects at any depth, which is the
    ordinary shape of a configuration worth editing. A value cannot, an empty
    container cannot, and a declared member that holds no object has no object
    to ask.

    Args:
        row: Node to ask about.

    Returns:
        Whether a configuration object is at that node or inside it.
    """
    return row.has_objects


def row_subtree_text(row: MemberRow) -> str:
    """Return what the objects at or inside one node amount to, as shown.

    A node that has not been asked since something inside it last changed says
    nothing, because that is a state and not an answer, and a line saying so
    under every object would be a line spent on nothing.

    A container of objects is worded differently from an object, because it is
    saying a different thing: an object answers for itself and a container
    answers for what it holds. Nothing else could tell them apart, since a
    folded container shows none of the objects the words are about.

    Both backends read it from here, so that neither of them decides on its
    own how a valid object and a refused one are told apart.

    Args:
        row: Node to render.

    Returns:
        What that node is on its own or what it holds, and nothing for a node
        that has no object at it or inside it and for one not asked yet.
    """
    if row.subtree_valid is None:
        return ''
    if row.is_object:
        return SUBTREE_VALID_MARK if row.subtree_valid \
            else SUBTREE_REFUSED_MARK
    return INSIDE_VALID_MARK if row.subtree_valid else INSIDE_REFUSED_MARK


def row_fold_text(row: MemberRow) -> str:
    """Return what says that one container is folded, empty when it is not.

    Args:
        row: Node to render.

    Returns:
        The mark of a folded container, and nothing for every other node.
    """
    return FOLDED_MARK if row.folded else ''


def can_fold(model: EditModel) -> bool:
    """Return whether anything in this configuration can be folded.

    A configuration of scalar members alone has nothing to fold, and a
    backend asks this before it offers the action at all: an editor that
    showed a control which could never do anything would be offering
    something that is not there.

    Args:
        model: Model to ask about.

    Returns:
        Whether the configuration holds a list or a dict.
    """
    return any(row.foldable for row in model.rows)


def fold_hides(model: EditModel) -> bool:
    """Return whether folding everything would hide anything.

    It is what the one action that folds everything does next, so a backend
    that names its actions after what the next press does reads the name
    from here. The action folds while anything is open and opens everything
    once nothing is, so a press always changes something.

    Args:
        model: Model to ask about.

    Returns:
        Whether at least one container is open.
    """
    return any(row.foldable and not row.folded for row in model.rows)


def row_diagnostic(model: EditModel, row: MemberRow) -> str:
    """Return what is wrong with one member, and nothing when nothing is.

    Three things can be wrong with a node and they are not the same thing.
    Its text may mean no value of that node at all, which is answered by
    the node alone and stays true until the node is edited again; the
    application may have refused the value it holds, which is answered by the
    whole configuration and is only known for as long as the rest of the
    buffer stands still; or the nested configuration object that owns the node
    may have refused it when it was asked about itself, which is known for as
    long as nothing inside that object changes. The first is preferred when
    more than one is there, because a value that does not exist yet is what
    has to be corrected first, and the verdict comes before the answer of one
    object because a pass over the whole buffer is the more recent of the two
    whenever both are there.

    What a member validator refused is about the whole member, because that
    is what the validator is given, so it is shown at the member and not at
    one of the values inside it. Both are addressed by their path, which is
    what keeps a value called `cpu` inside a dict from being told what the
    application said about a member of that name.

    Both backends read this from here, so that neither of them decides on its
    own what a refused node is told.

    Args:
        model: Model that the node belongs to.
        row: Node to report.

    Returns:
        What is wrong with that node, empty when nothing is known to be.
    """
    if row.conversion:
        return row.conversion
    verdict = model.verdict
    if verdict is not None and row.path in verdict.refused:
        return verdict.refused[row.path]
    return row.subtree_refusal


def _indented(text: str, indent: str) -> str:
    """Return one text that belongs to a node, with every line indented.

    A line with nothing on it is left alone, because indenting it would put
    blank space where there is nothing to line up.
    """
    return '\n'.join(indent + line if line else line
                     for line in text.split('\n'))


def _row_line(row: MemberRow, indent: str) -> str:
    """Return the one line that shows one node and what is true of it.

    A node that is not edited in a field has no value of its own, whether it
    is a list, a dict, a nested configuration object or a member that holds no
    object at all, so it is written with the colon that says as much.
    """
    shape = LEAF_FORM if row.editable else CONTAINER_FORM
    return shape.format(indent=indent, name=row.name,
                        value=row_value_text(row), marks=row_marks(row),
                        folded=row_fold_text(row),
                        subtree=row_subtree_text(row))


def _row_as_text(model: EditModel, row: MemberRow) -> str:
    """Return the line that shows one node, and what is said below it.

    The description comes before what is wrong with the node, because the
    description is part of the node and what is wrong comes and goes: a
    line that appears below everything moves nothing that is above it.

    A node inside a list or a dict is indented once for every container it is
    inside, which is what makes the rendering a tree.
    """
    indent = TREE_INDENT * row.depth
    below = [row_description(model=model, row=row),
             row_diagnostic(model=model, row=row)]
    lines = [_row_line(row=row, indent=indent)]
    lines += [_indented(text, indent + DESCRIPTION_INDENT)
              for text in below if text]
    return '\n'.join(lines)


def _state_line(verdict: ValidationVerdict) -> str:
    """Return the one line that says what the application made of a buffer.

    Args:
        verdict: What the last validation pass found.

    Returns:
        The state of the buffer, naming the nodes that were refused.
    """
    if verdict.refused:
        return REFUSED_FORM.format(
            names=', '.join(path_text(path) for path in verdict.refused))
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
    """Return the whole model as text, one line per node of it.

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

    A container that is folded away is one line saying so, and what is inside
    it is not shown at all, which is the same thing the two backends do with
    it. What is inside a list or a dict is indented below it.

    Returns:
        The label of the configuration and what its class says about itself,
        what the load did, one line per shown node with its description and
        anything wrong with it below it, and then the validation state and
        the saving, without a trailing line break.
    """
    rows = [_row_as_text(model=model, row=row) for row in model.rows
            if row.shown]
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
