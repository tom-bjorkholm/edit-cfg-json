#! /usr/bin/env python3
"""The two ways of editing one value, and the one that is on the window.

A value the editor can edit is typed into a field, and a value whose whole set
the editor knows is picked from a pull-down of that set instead. Which of the
two is on the window is one answer for the whole editor, which the user
switches and the model holds, so every node has both widgets and shows one of
them.

Both of them show one `tkinter.StringVar`, which is what makes them two ways of
making the same edit rather than two things to keep in step: the pull-down
writes the value that was picked into that variable, and the callback which
writes the variable into the model is the one the field already had.

It is a module of its own because it is a piece of window with a life of its
own — two widgets, a variable, and the rule about which of them is shown — and
because `tk_editor` is the module of this backend that is nearest to being too
long to read.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from typing import Optional
import tkinter
import edit_cfg_json as core
from edit_cfg_json_tk.tk_look import LEAST_FIELD_WIDTH, choice_field, \
    edit_field


class ValueWidgets:
    """The ways of editing the value of one node, below one line of it.

    This is a class rather than a function because the variable has to be
    kept: a `tkinter.StringVar` unsets its Tcl variable when it is collected,
    and the field it belongs to would then lose both its text and the callback
    that writes it into the model.

    The widgets are inside an area of their own on the line of the node, so
    that showing one of them and hiding the other cannot move the value out of
    the column it belongs in: Tk packs a widget after the ones that are already
    there, so a widget that came back at the end of the line would land after
    the marks of its own member.
    """

    def __init__(self, parent: tkinter.Misc, row: core.MemberRow,
                 model: core.EditModel, changed: Callable[[], None]) -> None:
        """Create the field of one node, and its pull-down where it has one.

        The variable is given the area as its master, so that it is created in
        the same Tcl interpreter as the widgets that show it. A variable
        constructed without one is created in the first interpreter of the
        process instead, which is the wrong one as soon as the editor is not
        the only Tk in the application: the widgets would then show nothing
        and the callback below would never run.

        Args:
            parent: Line of the node that is being shown.
            row: Node whose value these widgets edit.
            model: Model that the edits are written into.
            changed: What to do once an edit has reached the model, which is
                to show what the model says about it now.
        """
        self._model = model
        self._path = row.path
        self._changed = changed
        self._area = tkinter.Frame(parent)
        self._area.pack(side='left', fill='x', expand=True)
        self._text = tkinter.StringVar(master=self._area,
                                       value=core.row_value_text(row))
        self._entry = edit_field(parent=self._area, text=self._text,
                                 width=LEAST_FIELD_WIDTH)
        self._entry.bind('<FocusOut>', self._left_field)
        self._chooser = self._made_chooser(row)
        self._text.trace_add('write', self._write_field)
        self.show_way()

    def _made_chooser(self, row: core.MemberRow
                      ) -> Optional[tkinter.Menubutton]:
        """Return the pull-down of one node, for a node that has values.

        Args:
            row: Node whose value these widgets edit.

        Returns:
            The pull-down of the values that node takes, or None for a node
            whose values are not a set the editor knows the whole of.
        """
        if not core.row_chooses(row):
            return None
        return choice_field(parent=self._area, text=self._text,
                            choices=row.choices, width=LEAST_FIELD_WIDTH)

    @property
    def reached(self) -> tkinter.Misc:
        """Return the widget that a search gives the keyboard focus to.

        It is whichever of the two is on the window, because a widget that is
        out of the layout is one the user cannot see and cannot type in.
        """
        if self._chooser is not None and self._model.choices_shown:
            return self._chooser
        return self._entry

    def show_way(self) -> None:
        """Put the way of editing this value that the model asks for now.

        The one that is not being used is taken out of the layout rather than
        destroyed, so that a field the user was typing into still holds what
        they typed when they switch back to it. A node with no pull-down has
        nothing to do here: its field is the only way of editing it and stays
        where it was put.
        """
        if self._chooser is None:
            return
        chosen = self._model.choices_shown
        shown, hidden = (self._chooser, self._entry) if chosen \
            else (self._entry, self._chooser)
        hidden.pack_forget()
        shown.pack(fill='x', expand=True)

    def show_value(self, text: str) -> None:
        """Write the text that the model holds for this node.

        Writing the text that is already there is not an edit, which is what
        lets this be done after a validation pass without undoing the marks
        that the pass has just set.

        Args:
            text: Value of this node as the model holds it now.
        """
        self._text.set(text)

    def _write_field(self, *trace_arguments: str) -> None:
        """Write what these widgets show into the model, and show the state.

        Tk reports a change of the variable and not of the widget, so this
        reads the variable itself. Every change is written through, whichever
        of the two widgets made it and including the ones that no key press
        caused, such as a paste.
        """
        _ = trace_arguments
        self._model.set_text(path=self._path, text=self._text.get())
        self._changed()

    def _left_field(self, *event: 'tkinter.Event[tkinter.Misc]') -> None:
        """Ask the model about this node once its field has been left.

        Leaving a field is when the user has moved on from it, and it is
        therefore when the editor says whether what they typed means a value
        of that member at all. Nothing is validated here: the whole
        configuration is what a validation pass is about, and this is one
        field answering for itself.

        A pull-down needs no such moment. Every value it offers is a value
        that member takes, so there is nothing for leaving it to find out.
        """
        _ = event
        self._model.check_field(self._path)
        self._changed()
