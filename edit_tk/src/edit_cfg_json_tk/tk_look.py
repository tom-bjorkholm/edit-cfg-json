#! /usr/bin/env python3
"""How the Tk backend measures and colours the parts of its window.

The sizes, the colours and the labels of this backend are here rather than in
the module that builds the window, because they are what one has to look at
to know how the editor will look and they are what a later theming decision
will change. Nothing here knows what an edit model is: it is given a text, a
reason for that text to stand out, and a widget to put it in.

What each kind of text is stays in the core, as `edit_cfg_json.Emphasis`, and
what colour a kind is belongs here. Tk has no theme to ask, unlike the Textual
backend, which names colours of its terminal's theme and follows it into a
dark mode.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
import tkinter
import edit_cfg_json as core

NAME_COLUMN_WIDTH = 24
"""Width in characters of the column that holds the member names."""

LEAST_FIELD_WIDTH = 8
"""Width in characters that a field asks for, and can be squeezed to.

A field takes every bit of the width that the name and the marks of its member
leave over, so this is not how wide a field is: it is how far a field gives way
when the window is too narrow for all three. The marks are what a narrow window
would otherwise cut off, and a mark that is there and cannot be read is worse
than a field with fewer characters in view. The Textual backend gives way in
the same direction and for the same reason.
"""

PADDING = 4
"""Padding in pixels around the widgets of the editor."""

DESCRIPTION_INDENT = 24
"""Indentation in pixels of what is written below one member.

The indentation is what says that the line belongs to the member above it
rather than being a member of its own.
"""

TREE_INDENT = 24
"""Indentation in pixels of each step inside a list or a dict.

The whole member is indented and not only its name, so that a name inside a
container is never cut off by the column that the names share. What that costs
is a value column that steps to the right with the tree, which is what a tree
looks like.
"""

FOLD_WIDTH = 2
"""Width in characters of the control that folds one container.

Every row has one that wide, and the rows that hold nothing to fold have an
empty one, so that the names of a container and of a value beside it line up.
"""

ELEMENT_WIDTH = 4
"""Width in characters of one control that changes how many elements there are.

They sit at the end of the line of the node they belong to, so a row that
offers none of them needs no width held for it and gets none. That is what
makes four of them affordable where the one control that folds a container has
to keep a column clear on every row.
"""

LEAST_WRAP_WIDTH = 200
"""Narrowest line in pixels that a paragraph of the editor is wrapped to.

A window can be made narrower than any text is readable in, and wrapping to
what is left of it would leave one word per line. Below this the text is cut
off by the window instead, which is the lesser of the two.
"""

EMPHASIS_COLOURS = {core.Emphasis.MUTED: '#4b5563',
                    core.Emphasis.ATTENTION: '#0969da',
                    core.Emphasis.WARNING: '#8a6100',
                    core.Emphasis.GOOD: '#1a7f37',
                    core.Emphasis.BAD: '#cf222e'}
"""The colour of every reason the core has to show something differently.

One colour per member of `edit_cfg_json.Emphasis`, chosen to be read on the
light window that Tk gives this editor: a grey that is dark enough for a
paragraph of explanation to be comfortable rather than faint, and a blue, an
amber, a green and a red that carry on a light background.

Tk has no theme to ask, unlike the Textual backend, which names colours of its
terminal's theme and follows it into a dark mode. A Tk that has been put into
a dark mode by its platform would want other values here, and that belongs
with the rest of what an application decides rather than in the middle of a
backend; see section 9 of `doc/design.md`.
"""

FIELD_BACKGROUND = '#eef1f5'
"""Background of a field the user can edit.

The window is white, so a field that kept the white background of its own
accord could not be told from a label: the values were there to be edited and
nothing said so. The tint plus the border below are what say it.
"""

FIELD_FOREGROUND = '#111827'
"""Colour of the text inside a field.

It is stated rather than inherited, because the background above is stated:
a platform that decided the text of a field should be white would otherwise
put white text on a light field.
"""

FIELD_BORDER = '#9aa5b1'
"""Colour of the line around a field the user can edit."""


def shown_text(parent: tkinter.Misc, text: str,
               emphasis: Optional[core.Emphasis] = None,
               wrapping: bool = True) -> tkinter.Label:
    """Return a label of the editor, in the colour its kind asks for.

    Args:
        parent: Widget that becomes the parent of the created label.
        text: Text to show, left aligned as every text of the editor is.
        emphasis: Why this text stands out from the values, or None for the
            ordinary text colour of the platform.
        wrapping: Whether the text is a paragraph, which wraps to the width
            of the window. The mark of a member is the one text of the editor
            that is not: it belongs beside its field on one line.

    Returns:
        A label showing that text.
    """
    label = tkinter.Label(parent, text=text, anchor='w', justify='left')
    show_emphasis(label, emphasis)
    if wrapping:
        wrap_to_width(label)
    return label


def told(label: tkinter.Label, text: str, emphasis: core.Emphasis) -> None:
    """Show one text of the editor, in the colour its state asks for.

    Args:
        label: Label that shows it.
        text: Text to show.
        emphasis: Why that text stands out from the values.
    """
    label.config(text=text)
    show_emphasis(label, emphasis)


def show_emphasis(label: tkinter.Label,
                  emphasis: Optional[core.Emphasis]) -> None:
    """Colour one label in the way one reason to stand out asks for.

    A label with no emphasis is left in the colour of the platform, which is
    what the values and their names are shown in: they are what the user came
    to change, and they are the most legible thing on the screen because
    nothing has been done to them.

    Args:
        label: Label to colour.
        emphasis: Why the text of that label stands out, or None for the
            ordinary text colour.
    """
    if emphasis is not None:
        label.config(foreground=EMPHASIS_COLOURS[emphasis])


def wrap_to_width(label: tkinter.Label) -> None:
    """Make one label wrap its text to the width it is given.

    A Tk label does not wrap at all unless it is told how wide a line may be,
    and it does not shrink its text either: a paragraph wider than the window
    is simply cut off, which is how a description lost its last words. The
    width to wrap at is not known until the window has been laid out, and it
    changes whenever the user resizes it, so it is followed rather than set.

    Args:
        label: Label that holds text which may be longer than a line.
    """
    def wrapped(event: 'tkinter.Event[tkinter.Misc]') -> None:
        """Wrap the text of the label at the width it now has."""
        label.configure(wraplength=max(event.width, LEAST_WRAP_WIDTH))
    label.bind('<Configure>', wrapped)


def label_text(label: Optional[tkinter.Label]) -> str:
    """Return the text one label is showing, empty when it is showing none.

    A label that is out of the layout holds no text, because that is how this
    backend hides one, so this answers what is on the window and not what a
    widget happens to remember.

    Args:
        label: Widget to read, or None for a widget that was never created.

    Returns:
        The text that widget shows.
    """
    return '' if label is None else str(label.cget('text'))


def place_text(label: Optional[tkinter.Label], text: str) -> None:
    """Put one text below a member into the layout, or take it out again.

    Hiding is taking the widget out of the layout and emptying it, because a
    label with text still takes the height of a line and a window with a
    blank line under every member would have hidden nothing.

    Args:
        label: Widget that shows one text below a member, or None for a text
            that this member can never have.
        text: Text to show, empty when there is nothing to show.
    """
    if label is None:
        return
    label.config(text=text)
    if not text:
        label.pack_forget()
        return
    label.pack(fill='x', padx=(DESCRIPTION_INDENT, PADDING))
