#! /usr/bin/env python3
"""The Textual controls that change how many elements a node holds.

They are here rather than in the module that builds the screen for the reason
every other split of this backend was made: one module of a thousand lines is
one nobody reads to the end. What is here is one row's worth of controls, the
identifiers that let a press be traced back to the node it was made on, and
the words of the one question this backend has to ask about them.

Nothing here decides *whether* a node offers anything. That is
`edit_cfg_json.MemberRow.offer`, which the core works out once so that the two
backends cannot offer different things.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from textual.widgets import Button
import edit_cfg_json as core
from edit_cfg_json_textual.textual_look import ELEMENT_CLASS

ADD_ACTION = 'add'
"""Name of the action that puts one more element into a node."""

REMOVE_ACTION = 'del'
"""Name of the action that takes one element out of what holds it."""

EARLIER_ACTION = 'up'
"""Name of the action that moves one element towards the front."""

LATER_ACTION = 'down'
"""Name of the action that moves one element towards the back."""

ADD_LABEL = 'Add'
"""Label of the control that puts one more element into a node.

It is a word and not the `+` of the fold control beside it, because the two do
different things and one row can have both: a list of configuration objects
folds away and grows, and two controls saying `+` on one line would be two
offers that could not be told apart.
"""

REMOVE_LABEL = 'Del'
"""Label of the control that takes one element out of what holds it."""

EARLIER_LABEL = 'Up'
"""Label of the control that moves one element towards the front."""

LATER_LABEL = 'Down'
"""Label of the control that moves one element towards the back."""

ELEMENT_LABELS = {ADD_ACTION: ADD_LABEL, REMOVE_ACTION: REMOVE_LABEL,
                  EARLIER_ACTION: EARLIER_LABEL, LATER_ACTION: LATER_LABEL}
"""What the control of each action says on it."""

ASK_KEY_ID = 'new_key'
"""Identifier of the field that a new entry of a dict is named in."""

ASK_KEY_PROMPT = 'Key of the new entry of {name} (Enter adds it):'
"""What the screen that asks for a new key says."""

ASK_KEY_LEAVE = 'Key of the new entry of {name} (Enter adds it, {key} leaves):'
"""What that screen says while there is a key that leaves it.

The key is named from the settings and not written into the sentence, for the
same reason the question about the output file names it: an application that
took `escape` for itself would otherwise be telling its users to press a key
that does nothing.
"""


def offered_actions(row: core.MemberRow) -> tuple[str, ...]:
    """Return the actions that one node offers about its elements.

    Args:
        row: Node to ask about.

    Returns:
        The name of each action that node offers, in the order the controls
        are shown, and nothing at all for a node that offers none, which is
        most nodes of most configurations.
    """
    offered = ((row.offer.extend, ADD_ACTION), (row.offer.remove,
                                                REMOVE_ACTION),
               (row.offer.earlier, EARLIER_ACTION), (row.offer.later,
                                                     LATER_ACTION))
    return tuple(action for offers, action in offered if offers)


def element_id(index: int, action: str) -> str:
    """Return the identifier of one control of one node.

    Args:
        index: Place of the node among the rows, which every widget of a node
            is identified by: two values inside two different dicts can have
            one name, and a dictionary key holds whatever a dictionary key
            holds, which Textual does not always accept as an identifier.
        action: Name of the action that control runs.

    Returns:
        The identifier that press is found by.
    """
    return f'{action}_{index}'


def element_button(widget_id: str, action: str) -> Button:
    """Return one control that changes how many elements there are.

    Args:
        widget_id: Identifier the application finds this control by.
        action: Name of the action it runs.

    Returns:
        A control that says what it does.
    """
    return Button(ELEMENT_LABELS[action], id=widget_id, classes=ELEMENT_CLASS,
                  compact=True)
