#! /usr/bin/env python3
"""How much each part of the editor stands out, and in which direction.

An editor that shows what the values are for shows a great deal of text, and
not all of it is the same kind of thing: a value is what the user came to
change, a description is text about that value, and a refused validation is
something to act on. Telling them apart by colour is what keeps the screen
readable once the explanations are on it.

What each kind of text is stays here, in the core, and what colour a kind is
belongs to each backend: Textual has theme variables that follow the terminal
into its light or dark mode, and Tk has colour names, and neither of them can
be expressed in the other. What the core owns is therefore the vocabulary and
the two decisions that depend on the state of the model, which are the ones
the two backends could otherwise answer differently.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from enum import Enum, auto
from edit_cfg_json.edit_model import EditModel
from edit_cfg_json.rows import MemberRow


class Emphasis(Enum):
    """One reason for a part of the editor to stand out from the rest.

    There is no member for ordinary text, which is the values and their names:
    they are what the user is editing, and they are the most legible thing on
    the screen precisely because nothing is done to them. Every member here is
    a reason to be shown differently from them.
    """

    MUTED = auto()
    """Text about the values rather than the values, and a state not reached.

    The explanatory text is this, and so is a validation that has not been run
    yet and a file that has not been written yet: what has not happened is
    worth saying and is not worth reading first.
    """

    ATTENTION = auto()
    """Something has happened to this member and the user should see it."""

    WARNING = auto()
    """The input file was not quite what was asked for."""

    GOOD = auto()
    """The application accepted this."""

    BAD = auto()
    """The application refused this."""


EXPLANATION = Emphasis.MUTED
"""How the docstring of the class and the description of a member are shown.

They are text about the values, so they are shown as the secondary text they
are — but readably, because an explanation nobody can read explains nothing.
"""

MEMBER_MARK = Emphasis.ATTENTION
"""How the marks of one member are shown.

Every mark says that something has happened to that member: the file did not
hold it, the user changed it, or a validator changed what the user wrote.
"""

MEMBER_DIAGNOSTIC = Emphasis.BAD
"""How what is wrong with one member is shown.

It is what the application refused, so it is shown as a refusal and not as
text about the member: it is the one thing on the row that has to be acted on,
and it is deliberately not the muted colour that the description beside it
has.
"""

LOAD_REMARK = Emphasis.WARNING
"""How what reading the input file did is shown.

A load that had nothing to say says nothing at all, so a message that is there
is always a remark about a file that was not quite what was asked for.
"""


def verdict_emphasis(model: EditModel) -> Emphasis:
    """Return how the validation state of one buffer is shown.

    A buffer that has not been validated since it last changed is the third
    state and not a kind of failure, so it is shown as what has not happened
    yet rather than as something wrong.

    Args:
        model: Model whose validation state is shown.

    Returns:
        The emphasis of the validation state of that model.
    """
    verdict = model.verdict
    if verdict is None:
        return Emphasis.MUTED
    return Emphasis.GOOD if verdict.valid else Emphasis.BAD


def subtree_emphasis(row: MemberRow) -> Emphasis:
    """Return how what the objects at or inside one node amount to is shown.

    The same three states as the validation of the whole configuration, and
    the same three ways of showing them, because they are the same kind of
    answer about a smaller thing: a node that has not been asked since
    something inside it changed is what has not happened yet rather than
    something wrong.

    A list or a dict of configuration objects is shown the same way, and says
    the same three things about the objects it holds rather than about itself.

    Args:
        row: Node whose own state is shown.

    Returns:
        The emphasis of what that node is on its own, or of what it holds.
    """
    if row.subtree_valid is None:
        return Emphasis.MUTED
    return Emphasis.GOOD if row.subtree_valid else Emphasis.BAD


def save_emphasis(model: EditModel) -> Emphasis:
    """Return how what saving did, or would do, is shown.

    Where a save would write is not a state that has been reached, so it is
    shown as one that has not, exactly like a validation nobody has asked for.

    Args:
        model: Model whose saving is shown.

    Returns:
        The emphasis of the last attempt to save, or of the destination that
        is waiting when there has been no attempt.
    """
    outcome = model.save_outcome
    if outcome is None:
        return Emphasis.MUTED
    return Emphasis.GOOD if outcome.saved else Emphasis.BAD
