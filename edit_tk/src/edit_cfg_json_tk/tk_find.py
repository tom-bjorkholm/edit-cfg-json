#! /usr/bin/env python3
"""The search of a Tkinter editor: a field, four controls and a line.

A configuration of any interesting size does not fit a window, so the member a
user wants is often one they cannot see. This is what they look for it with,
and it is a part of the window rather than a dialog that is asked and gone: a
search is a text that is changed a character at a time, with the answer moving
under it as it is typed, and four controls beside it that change what it
reaches.

What is being looked for, how it is compared and which node the search has got
to are all state of the model, so nothing here decides any of it. What is here
is the widgets, the words on them and the wiring: this backend's half of a
question the core answers.

Everything this backend takes from the core is reached through `core`, which is
`edit_cfg_json` itself. A backend may use the public API of the core and
nothing else, and naming it at every call site is what makes that visible.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from typing import NamedTuple
import tkinter
import edit_cfg_json as core
from edit_cfg_json_tk.tk_look import FIND_WIDTH, PADDING, edit_field, \
    shown_text, told
from edit_cfg_json_tk.tk_tooltip import Tooltip

FIND_FIELD_NAME = 'find_field'
"""Tk name of the field that a search is typed into.

It is what tells this one field from the fields that hold the values of the
members: it is no member of the configuration, and an application that reaches
into the widgets of the editor has to be able to say which of them it means.
See `edit_cfg_json_tk.tk_look.MEMBER_FIELD_NAME`.
"""

FIND_LABEL_TEXT = 'Find:'
"""Text of the label beside the field that a search is typed into."""

FIND_NEXT_TEXT = '►'
"""Label of the button that goes to the next member the search reaches.

A button as well as a key, because a function key is the one thing a keyboard
is most likely not to deliver and because a user who has just typed into the
field is looking at this row.

The arrow that every editor draws for this rather than the two words it stands
for, because the row it shares is the row the field needs the width of. It is
U+25BA and not the U+25B6 that reads the same, because that one is an emoji
code point and a font fallback is then free to answer it with a coloured
picture instead of a character. What it means in words is `FIND_NEXT_TIP`, said
in a tooltip for the same reason the four controls beside it say theirs there.
"""

FIND_NEXT_TIP = 'Go to the next member that the search reaches.'
"""What the button that goes to the next member says about itself.

It is a word of this backend and not one of the core, unlike the four
explanations of `edit_cfg_json.FIND_OPTION_HELP`: the terminal editor has the
room to write `next` on its own control, so nothing but this window needs this
sentence.
"""

FIND_TICK_LABELS = ('path', 'value', 'Aa', '==')
"""The label of each control that says where a search looks.

They are in the order of the members of `edit_cfg_json.FindOptions`, which is
what pairs each control with the answer it shows, and a member added there
without a label here is refused where the controls are created rather than
being silently left out.

Two of them are one or two characters, which is what keeps the whole row one
line: the width of that row is what the field is for. What each of them means
is `edit_cfg_json.FIND_OPTION_HELP`, said in a tooltip, because Tk has nowhere
else to put it and because what a control of the model means is the core's.
"""


class FindWidgets(NamedTuple):
    """The widgets of one search, once they have been created."""

    text: tkinter.StringVar
    """The variable that holds what is being looked for.

    It has to be kept for as long as the field lives: a `tkinter.Variable`
    unsets its Tcl variable when it is collected, and the field would then lose
    both its text and the callback that searches with it.
    """

    entry: tkinter.Entry
    """The field that a search is typed into, which one key focuses."""

    ticks: tuple[tkinter.BooleanVar, ...]
    """Whether each control that says where a search looks is ticked.

    One per member of `edit_cfg_json.FindOptions`, in that order, and each of
    them kept for the same reason as the variable above.
    """

    line: tkinter.Label
    """The label that says what the search has reached."""


class FindPanel:
    """The search of one Tk editor, as the widgets and what they do.

    It holds the model and asks it, rather than reporting keystrokes to the
    editor, because what a search is belongs to the model and this is the one
    place in this backend that is about a search at all. What it hands back to
    the editor is the two things only the editor can do: lay the rows out again
    when a container was opened, and bring what was found into view.
    """

    def __init__(self, parent: tkinter.Misc, model: core.EditModel, *,
                 searched: Callable[[bool], None],
                 reached: Callable[[], None]) -> None:
        """Create the field, the four controls and the line below them.

        They go in a frame of their own, holding the row and the line under it,
        so that taking the line out of the layout and putting it back cannot
        move it away from the row it belongs to. That is the same arrangement
        as a member and what is said below it.

        Args:
            parent: Widget that becomes the parent of the created widgets.
            model: Model that the search is of.
            searched: What the editor does once a search has run, told whether
                a container was opened to reach what was found.
            reached: What the editor does to go into what was found, which is
                bringing it into view and typing in it.
        """
        self._model = model
        self._searched = searched
        self._reached = reached
        frame = tkinter.Frame(parent)
        frame.pack(side='top', fill='x')
        row = tkinter.Frame(frame)
        row.pack(side='top', fill='x')
        tkinter.Label(row, text=FIND_LABEL_TEXT).pack(side='left',
                                                      padx=PADDING)
        report = model.search
        text = tkinter.StringVar(master=row, value=report.text)
        entry = self._add_entry(parent=row, text=text)
        ticks = self._add_ticks(parent=row, options=report.options)
        self._add_next(parent=row)
        # The line is created last, so that the widgets are created in the
        # order they are read in: the row above it is finished first.
        self._widgets = FindWidgets(text=text, entry=entry, ticks=ticks,
                                    line=shown_text(frame, ''))
        self.show()

    def focus(self) -> None:
        """Put the cursor in the field that a search is typed into.

        What is in the field is left exactly as it is, because a user who has
        found one member and wants another comes back to text that is worth
        changing rather than text that is worth typing again.
        """
        self._widgets.entry.focus_set()

    def find_next(self) -> None:
        """Go to the next node the search reaches, and type in it."""
        self._searched(self._model.find_next())
        self._reached()

    def show(self) -> None:
        """Say what the search has reached, and nothing when nothing is.

        The line is taken out of the layout while there is nothing to say,
        because a blank line under the search row would otherwise be there in
        every session that nobody searched in.
        """
        line = self._widgets.line
        shown = core.find_text(self._model)
        told(line, text=shown, emphasis=core.find_emphasis(self._model))
        if shown:
            line.pack(side='top', fill='x', padx=PADDING)
            return
        line.pack_forget()

    def _add_entry(self, parent: tkinter.Misc,
                   text: tkinter.StringVar) -> tkinter.Entry:
        """Create the field that a search is typed into.

        It is the field of a member all over again, because it is the same
        kind of thing: the one place on its row where the user types.

        Args:
            parent: Row of the search.
            text: Variable that holds what is being looked for.

        Returns:
            The field that a search is typed into.
        """
        entry = edit_field(parent=parent, text=text, width=FIND_WIDTH,
                           name=FIND_FIELD_NAME)
        entry.pack(side='left', fill='x', expand=True)
        entry.bind('<Return>', self._entered)
        text.trace_add('write', self._typed(text))
        return entry

    def _add_ticks(self, parent: tkinter.Misc, options: core.FindOptions
                   ) -> tuple[tkinter.BooleanVar, ...]:
        """Create the four controls that say where a search looks.

        Args:
            parent: Row of the search.
            options: How the text being looked for is compared now.

        Returns:
            The variable of each control, in the order of the members of
            `edit_cfg_json.FindOptions`.
        """
        return tuple(self._add_tick(parent=parent, label=label, tip=tip,
                                    value=value)
                     for label, tip, value in zip(FIND_TICK_LABELS,
                                                  core.FIND_OPTION_HELP,
                                                  options, strict=True))

    def _add_tick(self, parent: tkinter.Misc, label: str, tip: str,
                  value: bool) -> tkinter.BooleanVar:
        """Create one control that says where a search looks.

        Args:
            parent: Row of the search.
            label: The one or two words on the control.
            tip: What it says when the pointer rests on it, which is where the
                whole of what it means is: the label is too short to say.
            value: Whether it starts out ticked.

        Returns:
            The variable that holds whether it is ticked.
        """
        flag = tkinter.BooleanVar(master=parent, value=value)
        box = tkinter.Checkbutton(parent, text=label, variable=flag,
                                  command=self._toggled)
        box.pack(side='left')
        Tooltip(box, tip)
        return flag

    def _add_next(self, parent: tkinter.Misc) -> None:
        """Create the button that goes to the next member the search reaches.

        Args:
            parent: Row of the search.
        """
        button = tkinter.Button(parent, text=FIND_NEXT_TEXT,
                                command=self.find_next)
        button.pack(side='left', padx=PADDING)
        Tooltip(button, FIND_NEXT_TIP)

    def _typed(self, text: tkinter.StringVar) -> Callable[..., None]:
        """Return the callback that writes the field into the model.

        Every change of the text is a search, because that is what a field
        which stays on the window is for: the answer moves under it as it is
        typed, and nothing has to be pressed to ask.

        The cursor stays in this field, unlike the one that a press of Find
        next leaves: the user is typing here.
        """
        def find_typed(*trace_arguments: str) -> None:
            """Look for what the field holds, and show what that reached."""
            _ = trace_arguments
            self._searched(self._model.find(text.get()))
        return find_typed

    def _entered(self, *event: 'tkinter.Event[tkinter.Misc]') -> None:
        """Go into the node that the search has already reached.

        This is the press that says the user has found what they were looking
        for and wants to edit it, which is why it moves the cursor and typing
        does not.
        """
        _ = event
        self._reached()

    def _toggled(self) -> None:
        """Look again with the places and the comparison as they are now."""
        self._searched(self._model.set_find_options(self._options()))

    def _options(self) -> core.FindOptions:
        """Return what the four controls of the search say now."""
        ticked = tuple(flag.get() for flag in self._widgets.ticks)
        return core.FindOptions(in_path=ticked[0], in_value=ticked[1],
                                cased=ticked[2], whole=ticked[3])
