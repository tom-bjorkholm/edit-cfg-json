#! /usr/bin/env python3
"""The widgets that one node of the configuration owns, and the texts below it.

A node is one line — its name, the way of editing its value, the marks of what
has happened to it — and under that line the two texts that can appear about
it: what the member is for and what is wrong with it. Which of the two is
showing is a rule of its own, because Tk packs a widget after the ones that
are already there, and it belongs beside the widgets it is about.

It is a module of its own because `tk_editor` is the module of this backend
that is nearest to being too long to read, and because what a row of the
editor is made of is worth reading without the whole editor around it.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import NamedTuple, Optional
import tkinter
from edit_cfg_json_tk.tk_look import label_text, place_text
from edit_cfg_json_tk.tk_values import ValueWidgets


class RowWidgets(NamedTuple):
    """The widgets that one node of the configuration owns."""

    frame: tkinter.Frame
    """The widget that holds the whole node, which is what folding hides.

    It is packed and unpacked rather than created and destroyed, so that a
    field the user is typing into survives its container being folded and
    opened again.
    """

    fold: Optional[tkinter.Button]
    """The control that folds this container, None for a node with none."""

    field: Optional[ValueWidgets]
    """The ways of editing a node, and None for a node with none of them."""

    mark: tkinter.Label
    """The widget that says what has happened to this member."""

    subtree: Optional[tkinter.Label]
    """The widget that says what this object is on its own.

    It is None for every node that is not a nested configuration object,
    because nothing else is a configuration that can be asked about itself.
    """

    description: Optional[tkinter.Label]
    """The widget that says what this member is for.

    It is None for a member that nothing is said about, because there is then
    nothing that could ever appear in it.
    """

    diagnostic: tkinter.Label
    """The widget that says what is wrong with this member.

    Every member has one, unlike the description above it: any member can be
    refused, so there is no member for which this could never say anything.
    """

    elements: tuple[tkinter.Button, ...] = ()
    """The controls that change how many elements this node holds.

    A node is given exactly the ones it offers and nothing at all where it
    offers none, because they sit at the end of the line rather than in a
    column that every row has to keep clear. Which of them a node offers can
    change — the first element of a list cannot move up until something is put
    in front of it — and the rows are built again whenever it does.
    """


def show_below(widgets: RowWidgets, description: str, diagnostic: str) -> None:
    """Show what belongs below one member, in the order it belongs in.

    Both texts are taken out of the layout and put back rather than only the
    one that changed, because Tk packs a widget after the ones that are
    already there: a description that came back while a diagnostic was
    showing would otherwise land below it. Nothing is touched while both
    texts are already what they should be, so the ordinary case of typing
    into a field does not lay the window out again on every key.

    Args:
        widgets: Widgets of the member.
        description: What the member is for, empty while that is hidden.
        diagnostic: What is wrong with the member, empty when nothing is.
    """
    if label_text(widgets.description) == description and \
            label_text(widgets.diagnostic) == diagnostic:
        return
    for label in (widgets.description, widgets.diagnostic):
        place_text(label, '')
    place_text(widgets.description, description)
    place_text(widgets.diagnostic, diagnostic)
