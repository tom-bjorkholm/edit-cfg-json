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

from collections.abc import Callable, Sequence
from functools import partial
from typing import Optional
import tkinter
import tkinter.font
import edit_cfg_json as core
from edit_cfg_json_tk.scrolling import BODY_WIDTH

NAME_COLUMN_WIDTH = 24
"""Widest the column of the member names is ever given, in widths of `0`.

The column is as wide as the longest name of the editor, measured in
`ROW_FONT`, and never wider than this many widths of the character `0`, which
is what it always was before it was measured. A longer name is cut off.
"""

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
container is never cut off by the column that the names share. The pull-down
of the types is narrower by as much on every step, so that the column of the
types ends in one place and the values of every row begin in one column.
"""

ROW_FONT = 'TkDefaultFont'
"""Font of the name and the type of a row, which their widths are measured in.
"""

BLANK_WIDTH = 1
"""Width and height in pixels of the blank image of a name or a type.

A label or a menu button that shows an image is as wide as it is told in
pixels, where one with only a text is told its width in widths of the
character `0`, which is wider than most characters of a name or a type and
left much of their columns empty. The image is what makes the width one in
pixels, and it is blank and one pixel so that it takes nothing from the text
but that pixel. Such a widget has no padding beside its text: Tk leaves the
padding out of a width it is told but puts it between the image and the text,
which would cut that much off the end of the text.
"""

FOLD_WIDTH = 2
"""Width in characters of the control that folds one container.

Every row has one, and the rows that hold nothing to fold have an empty space
as wide as it is in pixels, so that the names of a container and of a value
beside it line up; see `fold_space`.
"""

ELEMENT_WIDTH = 4
"""Width in characters of one control that changes how many elements there are.

They sit at the end of the line of the node they belong to, so a row that
offers none of them needs no width held for it and gets none. That is what
makes four of them affordable where the one control that folds a container has
to keep a column clear on every row.
"""

FIND_WIDTH = 16
"""Width in characters that the field of the search asks for.

It is what that field gives way to when the window is too narrow for the row,
in the same way as the field of a member: what shares the row with it is four
controls whose labels are one or two characters and a button, and a control
that cannot be read is worse than a field with fewer characters in view.
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
backend; see section 9 of `doc/detailed_design.md`.
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


MEMBER_CHOICE_NAME = 'choice'
"""Tk name of the pull-down that offers the values of one member.

It says which kind of widget this is, for the reason the name below it does,
and it is what tells the pull-down of a member from the field of the same
member: the two share one variable and are on the same line, and exactly one
of them is in the layout.
"""

MEMBER_LABEL_NAME = 'name'
"""Tk name of the label that says the name of one member."""

MEMBER_TYPE_NAME = 'type'
"""Tk name of the pull-down that says which type one member holds.

It is on the line of its member between the name and the value, which is what
tells it from the pull-down of the values: that one is inside the area of the
value, where the two ways of editing the value take turns.
"""

TYPE_COLOUR = EMPHASIS_COLOURS[core.Emphasis.MUTED]
"""Colour of the type of a member, which nothing can be chosen in yet.

Tk greys a widget that is disabled to a colour too faint to read on the light
window this editor has, and a type is worth reading: it is the muted colour of
the explanations instead, which says that it is not something to edit and is
still read comfortably.
"""

MEMBER_FIELD_NAME = 'field'
"""Tk name of a field that holds the value of one member.

A Tk widget has no identifier of its own beyond its place in the window, so a
name is what says which kind of field this is — the same thing the Textual
backend says with a widget identifier. It is what lets an application, and a
test, tell the fields that are members of the configuration from the one that
is not, which is the field a search is typed into.

A name has to be unique among the children of one widget, and each of these is
the one field of the line of its own member, so one name serves them all.
"""


def edit_field(parent: tkinter.Misc, text: tkinter.StringVar, width: int,
               name: str = MEMBER_FIELD_NAME) -> tkinter.Entry:
    """Return a field of the editor, coloured so that it reads as one.

    The window is white, so a field that kept the background it is given could
    not be told from a label: the values were there to be edited and nothing
    said so. The tint, the border and the caret colour are what say that this
    one is edited and the labels are not.

    It is not packed here, because where a field goes is different for a member
    and for the search: one shares its row with the marks of that member and
    the other with the controls that say where a search looks.

    Args:
        parent: Widget that becomes the parent of the created field.
        text: Variable that holds what the field shows. It has to be created
            with the same parent, so that it lives in the same Tcl interpreter.
        width: Width in characters that the field asks for, which is how far it
            gives way when its row is too narrow for everything on it.
        name: Tk name of the field, which says what kind of field it is. The
            default is a field holding the value of one member.

    Returns:
        A field showing that variable.
    """
    return tkinter.Entry(parent, name=name, textvariable=text, relief='flat',
                         width=width, background=FIELD_BACKGROUND,
                         foreground=FIELD_FOREGROUND,
                         insertbackground=FIELD_FOREGROUND,
                         highlightbackground=FIELD_BORDER,
                         highlightthickness=1)


def choice_field(parent: tkinter.Misc, text: tkinter.StringVar,
                 choices: Sequence[str], width: int) -> tkinter.Menubutton:
    """Return the pull-down that offers the values one member takes.

    It is given the same variable as the field of that member, which is what
    makes the two ways of editing one member one edit: the pull-down writes
    the value the user picked into that variable, and the callback which
    writes the variable into the model is already there.

    It is a menu button with a menu on it, which is what `tkinter.OptionMenu`
    is, and it is built here rather than taken from there for one reason: that
    class passes only its own options on, so the Tk **name** of the widget
    cannot be given to it before Python 3.14 and this library supports 3.12.
    The name is what tells the pull-down of a member from its field, so it is
    worth the ten lines. What is gained beside it is that the width and the
    alignment are said where every other widget of this backend says them.

    It is coloured as the field is and left aligned as the field is, because
    the two stand in the same column of the same line and one of them is
    always the one showing the value. Tk centres the label of a menu button of
    its own accord, which would make the values of two members below each
    other begin in different columns.

    It is not packed here, for the reason the field is not: which of the two
    is in the layout is what the editor decides afresh whenever the user
    switches between typing and choosing.

    Args:
        parent: Widget that becomes the parent of the created pull-down.
        text: Variable that holds what the pull-down shows, which is the
            variable of the field of the same member.
        choices: The values that member takes, which are what it offers. It
            is never empty: a member with no such values has no pull-down.
        width: Width in characters that the pull-down asks for, which is the
            width its field asks for.

    Returns:
        A pull-down of those values, showing that variable.
    """
    pull_down = tkinter.Menubutton(parent, name=MEMBER_CHOICE_NAME,
                                   textvariable=text, indicatoron=True,
                                   anchor='w', width=width, relief='flat',
                                   borderwidth=2, highlightthickness=1,
                                   background=FIELD_BACKGROUND,
                                   foreground=FIELD_FOREGROUND,
                                   highlightbackground=FIELD_BORDER)
    menu_of(pull_down=pull_down,
            entries=[(choice, choice) for choice in choices], picked=text.set)
    return pull_down


def row_font(parent: tkinter.Misc) -> tkinter.font.Font:
    """Return `ROW_FONT`, in which the names and the types are measured.

    Args:
        parent: Widget of the editor, whose interpreter has the font.

    Returns:
        The font, as the interpreter of that widget has it.
    """
    return tkinter.font.Font(root=parent, name=ROW_FONT, exists=True)


def blank_image(parent: tkinter.Misc) -> tkinter.PhotoImage:
    """Return the blank image that makes a width one in pixels.

    Args:
        parent: Widget of the editor, whose interpreter gets the image.

    Returns:
        An image of `BLANK_WIDTH` pixels that shows nothing, which the caller
        keeps alive for as long as a widget showing it is.
    """
    return tkinter.PhotoImage(master=parent, width=BLANK_WIDTH,
                              height=BLANK_WIDTH)


def name_label(parent: tkinter.Misc, name: str, width: int,
               blank: tkinter.PhotoImage) -> tkinter.Label:
    """Return the label that says the name of one node, not yet packed.

    It shows the blank image beside its name for the reason the pull-down of
    the types does, and it is left aligned, so that a name longer than the
    column is cut off at its end.

    Args:
        parent: Line of the node that is being shown.
        name: The name of that node.
        width: Width in pixels of the column of the names, in `ROW_FONT`.
        blank: The image from `blank_image`.

    Returns:
        A label saying that name.
    """
    return tkinter.Label(parent, name=MEMBER_LABEL_NAME, text=name,
                         font=ROW_FONT, image=blank, compound='left',
                         anchor='w', padx=0, width=width + BLANK_WIDTH)


def fold_button(parent: tkinter.Misc) -> tkinter.Button:
    """Return the control that folds one container, without what it does.

    Args:
        parent: Line of the node that is being shown.

    Returns:
        A button `FOLD_WIDTH` characters wide, not yet packed.
    """
    return tkinter.Button(parent, width=FOLD_WIDTH, relief='flat',
                          borderwidth=0, highlightthickness=0, padx=0, pady=0)


def fold_space(parent: tkinter.Misc) -> tkinter.Frame:
    """Return the empty space that a row with nothing to fold begins with.

    It is exactly as wide as the control that folds a container, which a
    label of as many characters is not: a platform draws a button wider than
    its text by its own frame, and on macOS a button of two characters takes
    50 pixels where a label of two takes 24, which moved the name, the type
    and the value of such a row to the left of those of a container beside
    it. The width is asked of a button made for the purpose and destroyed
    again, because Tk says how wide a widget is and not how wide one would be.

    Args:
        parent: Line of the node that is being shown.

    Returns:
        An empty frame as wide as the control, not yet packed.
    """
    probe = fold_button(parent)
    width = probe.winfo_reqwidth()
    probe.destroy()
    return tkinter.Frame(parent, width=width, height=1)


def type_field(parent: tkinter.Misc, shown: str, width: int, active: bool,
               blank: tkinter.PhotoImage) -> tkinter.Menubutton:
    """Return the pull-down of the types one node may hold, without its menu.

    It is active only where the type of the node is the user's to choose, and
    is then written in the colour of a value, because what it shows can be
    changed as a value can. Everywhere else it is disabled and coloured as an
    explanation is, rather than greyed out as Tk would. It is left aligned for
    the reason the pull-down of the values is, and it is not packed here,
    because where it goes on its line is the editor's.

    It is out of the order the Tab key goes in, as Tk leaves every menu button
    and as the pull-down of the values is, so the key goes from one value to
    the next and the focus the editor opens with stays on the first value.

    It shows the blank image beside its text, which is what makes its width
    one in pixels, and it is told the width of its text and of that image.

    Args:
        parent: Line of the node that is being shown.
        shown: The type that node holds now.
        width: Width in pixels of the text of the pull-down, written in
            `ROW_FONT`.
        active: Whether another type can be chosen in it.
        blank: The image from `blank_image`.

    Returns:
        A pull-down showing that type.
    """
    return tkinter.Menubutton(parent, name=MEMBER_TYPE_NAME, text=shown,
                              font=ROW_FONT, image=blank, compound='left',
                              indicatoron=True, anchor='w',
                              width=width + BLANK_WIDTH, padx=0, relief='flat',
                              borderwidth=2, highlightthickness=0,
                              state='normal' if active else 'disabled',
                              foreground=FIELD_FOREGROUND,
                              disabledforeground=TYPE_COLOUR)


def menu_of(pull_down: tkinter.Menubutton, entries: Sequence[tuple[str, str]],
            picked: Callable[[str], None]) -> tkinter.Menu:
    """Give one pull-down the menu it opens, one entry per pair.

    Args:
        pull_down: The menu button the menu belongs to.
        entries: What each entry of the menu says and what picking it hands
            on, in their order.
        picked: What picking an entry does with what it hands on.

    Returns:
        The menu, so that its entries can be given again later.
    """
    menu = tkinter.Menu(pull_down, tearoff=0)
    fill_menu(menu=menu, entries=entries, picked=picked)
    pull_down.config(menu=menu)
    return menu


def fill_menu(menu: tkinter.Menu, entries: Sequence[tuple[str, str]],
              picked: Callable[[str], None]) -> None:
    """Add one entry per pair to one menu.

    What an entry says and what it hands on are two texts, because the
    pull-down of the types says a long type cut to its column and hands on the
    whole of it, while the pull-down of the values hands on what it says.

    Args:
        menu: The menu to add the entries to.
        entries: What each entry says and what picking it hands on.
        picked: What picking an entry does with what it hands on.
    """
    for label, value in entries:
        menu.add_command(label=label, command=partial(picked, value))


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

    **It is started at the width of the body**, which is what a paragraph of
    the editor is given give or take the indent it sits at. A paragraph that
    started unwrapped would be laid out on one line, ask for the width of its
    whole text, and become several lines high only once its own `<Configure>`
    had told it otherwise — and a frame around it grows a round of idle work
    after that, and the frame around that one a round later again. The last
    of those rounds lands after the window has been shown, which is a window
    that resizes itself under the user: `scrolling.BODY_WIDTH` says what that
    costs, and section 4.6 of the design says what it costs on macOS.

    Args:
        label: Label that holds text which may be longer than a line.
    """
    def wrapped(event: 'tkinter.Event[tkinter.Misc]') -> None:
        """Wrap the text of the label at the width it now has."""
        label.configure(wraplength=max(event.width, LEAST_WRAP_WIDTH))
    label.configure(wraplength=BODY_WIDTH)
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
