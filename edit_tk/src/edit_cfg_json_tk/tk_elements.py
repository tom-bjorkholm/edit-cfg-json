#! /usr/bin/env python3
"""The Tk controls that change how many elements a node holds.

They are here rather than in the module that builds the window for the reason
every other split of this backend was made: one module of a thousand lines is
one nobody reads to the end. What is here is one row's worth of controls and
the one question this backend has to ask that the toolkit has no dialog of its
own for, which is what a new entry of a dict is to be called.

Nothing here decides *whether* a node offers anything. That is
`edit_cfg_json.MemberRow.offer`, which the core works out once so that the two
backends cannot offer different things.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from typing import Optional
import tkinter
from tkinter import simpledialog
import edit_cfg_json as core
from edit_cfg_json_tk.tk_look import ELEMENT_WIDTH

ADD_TEXT = 'Add'
"""Text of the control that puts one more element into a node.

It is a word and not the `+` of the fold control beside it, because the two do
different things and one row can have both: a list of configuration objects
folds away and grows, and two controls saying `+` on one line would be two
offers that could not be told apart.
"""

REMOVE_TEXT = 'Del'
"""Text of the control that takes one element out of what holds it."""

EARLIER_TEXT = 'Up'
"""Text of the control that moves one element towards the front."""

LATER_TEXT = 'Down'
"""Text of the control that moves one element towards the back."""

ADD_KEY_TITLE = 'Add an entry'
"""Title of the dialog that asks what a new entry of a dict is called."""

ADD_KEY_PROMPT = 'Key of the new entry of {name}:'
"""What that dialog asks, naming the member that is about to grow."""


def element_controls(parent: tkinter.Misc, row: core.MemberRow,
                     model: core.EditModel,
                     after: Callable[[], None]) -> tuple[tkinter.Button, ...]:
    """Create the controls that change how many elements one node holds.

    They are put at the end of the line of the node, after the value and the
    marks, so a node that offers none of them costs the values no width at
    all. That is what makes four of them affordable where the one control
    that folds a container has to keep a column clear on every row.

    Args:
        parent: Line of the node that is being shown.
        row: Node to create the controls for.
        model: Model that the change is made in.
        after: What to do once the model has changed, which is to make the
            widgets again: a change of the elements changes how many rows
            there are and which controls each of them offers.

    Returns:
        The controls that node offers, and nothing at all for one that offers
        none, which is most nodes of most configurations.
    """
    offer = row.offer
    wanted = ((offer.extend, ADD_TEXT, _adder(row, model, after)),
              (offer.remove, REMOVE_TEXT, _remover(row, model, after)),
              (offer.earlier, EARLIER_TEXT, _mover(row, model, after, False)),
              (offer.later, LATER_TEXT, _mover(row, model, after, True)))
    return tuple(_control(parent=parent, text=text, command=command)
                 for offered, text, command in wanted if offered)


def _control(parent: tkinter.Misc, text: str,
             command: Callable[[], None]) -> tkinter.Button:
    """Create one control that changes how many elements there are."""
    button = tkinter.Button(parent, text=text, width=ELEMENT_WIDTH,
                            command=command)
    button.pack(side='left')
    return button


def _adder(row: core.MemberRow, model: core.EditModel,
           after: Callable[[], None]) -> Callable[[], None]:
    """Return the command that puts one more element into one node."""
    def add_element() -> None:
        """Add the element, asking for a key where one is needed."""
        key = asked_key(row) if row.offer.keyed else ''
        if key is None:
            return
        model.add_element(path=row.path, key=key)
        after()
    return add_element


def _remover(row: core.MemberRow, model: core.EditModel,
             after: Callable[[], None]) -> Callable[[], None]:
    """Return the command that takes one element out of what holds it."""
    def remove_element() -> None:
        """Remove that element, and show what the model says now."""
        model.remove_element(row.path)
        after()
    return remove_element


def _mover(row: core.MemberRow, model: core.EditModel,
           after: Callable[[], None], later: bool) -> Callable[[], None]:
    """Return the command that moves one element by one place."""
    def move_element() -> None:
        """Move that element, and show what the model says now."""
        model.move_element(path=row.path, later=later)
        after()
    return move_element


def asked_key(row: core.MemberRow) -> Optional[str]:
    """Ask what a new entry of one dict is to be called.

    A new entry of a dict has to be called something, and nothing but the
    person configuring the application knows what. A key the dict already
    holds is asked about again rather than allowed to take the place of what
    is there: the model refuses such a key, and an editor that let the
    question be answered with one would be offering to lose an entry.

    Args:
        row: Node that is about to be given an entry.

    Returns:
        The key that was named, and None where the question was left
        unanswered or answered with nothing.
    """
    held = row.value if isinstance(row.value, dict) else {}
    while True:
        named = simpledialog.askstring(
            ADD_KEY_TITLE,
            ADD_KEY_PROMPT.format(name=core.path_text(row.path)))
        if not named:
            return None
        if named not in held:
            return named
