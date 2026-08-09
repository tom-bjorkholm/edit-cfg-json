#! /usr/bin/env python3
"""How the Textual backend names, styles and identifies its widgets.

The identifiers, the style classes, the sizes, the style sheet and the colours
of this backend are here rather than in the modules that build the screen,
because they are what one has to look at to know how the editor will look.
Nothing here knows what an edit model is beyond the row it is given, and
nothing here imports another module of this backend, so everything that builds
a widget can read its own identifier and its own style class from here.

What each kind of text is stays in the core, as `edit_cfg_json.Emphasis`, and
what a kind looks like belongs here: a colour of the terminal's own theme, so
that the editor follows it into a light or a dark mode instead of naming
colours of its own.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Sequence
from typing import Optional
from textual.binding import BindingsMap
from textual.widget import Widget
from textual.widgets import Static
import edit_cfg_json as core

VALUE_ID_PREFIX = 'value_'
"""Prefix of the identifier of the widget that shows one node value.

Every identifier of a node is that prefix and the place of the node among the
rows, and not the name of the node: two values inside two different dicts can
have one name, and a path holds whatever a dictionary key holds, which is not
always something Textual accepts as an identifier.
"""

MARK_ID_PREFIX = 'mark_'
"""Prefix of the identifier of the widget that marks one node."""

SUBTREE_ID_PREFIX = 'own_'
"""Prefix of the identifier of the widget that says what one object is."""

DESCRIPTION_ID_PREFIX = 'about_'
"""Prefix of the identifier of the widget that describes one node."""

DIAGNOSTIC_ID_PREFIX = 'wrong_'
"""Prefix of the identifier of the widget that refuses one node."""

FOLD_ID_PREFIX = 'fold_'
"""Prefix of the identifier of the control that folds one container."""

MEMBER_ID_PREFIX = 'member_'
"""Prefix of the identifier of everything that one node owns."""

DOCSTRING_ID = 'docstring'
"""Identifier of the widget that shows what the configuration class says."""

VERDICT_ID = 'verdict'
"""Identifier of the widget that shows what validation found."""

SAVE_ID = 'saving'
"""Identifier of the widget that shows what saving did or would do."""

LOAD_ID = 'load'
"""Identifier of the widget that shows what reading the file did."""

BODY_ID = 'body'
"""Identifier of the part of the screen that scrolls."""

MEMBERS_ID = 'members'
"""Identifier of the part of the body that holds the nodes.

They have a container of their own inside the part that scrolls, because a
validation pass can leave the model with other rows than it had and they are
then mounted afresh. What is above them is not, so it is not in here.
"""

SAVE_AS_ID = 'save_as'
"""Identifier of the field that the file to write is typed into."""

ASK_BOX_ID = 'ask_box'
"""Identifier of the box that holds one question and its answer."""

NAME_CLASS = 'member_name'
"""Style class of the widget that shows one member name."""

VALUE_CLASS = 'member_value'
"""Style class of the widget that shows or edits one member value."""

MARK_CLASS = 'member_mark'
"""Style class of the widget that marks one member."""

SUBTREE_CLASS = 'member_own'
"""Style class of the widget that says what one object is on its own."""

ROW_CLASS = 'member_row'
"""Style class of the container that holds the widgets of one member."""

MEMBER_CLASS = 'member'
"""Style class of the container that holds one member and its description."""

DESCRIPTION_CLASS = 'member_about'
"""Style class of the widget that says what one member is for."""

DIAGNOSTIC_CLASS = 'member_wrong'
"""Style class of the widget that says what is wrong with one member."""

FOLD_CLASS = 'member_fold'
"""Style class of the control that folds one container."""

ELEMENT_CLASS = 'member_element'
"""Style class of a control that changes how many elements there are."""

QUESTION_CLASS = 'ask_screen'
"""Style class of a screen that asks the user a question."""

ANSWER_CLASS = 'ask_answer'
"""Style class of the row of controls that answers a question."""

NAME_WIDTH = 24
"""Width in cells of the column that holds the member names."""

FOLD_WIDTH = 3
"""Width in cells of the control that folds one container.

Every row has one that wide, and the rows that hold nothing to fold have an
empty one, so that the names of a container and of a value beside it line up.
"""

TREE_INDENT = 4
"""Indentation in cells of each step inside a list or a dict.

The whole node is indented and not only its name, so that a name inside a
container is never cut off by the column that the names share. What that costs
is a value column that steps to the right with the tree, which is what a tree
looks like. The Tk backend indents by the same amount and for the same reason.
"""

DESCRIPTION_INDENT = 4
"""Indentation in cells of the description of one member.

The indentation is what says that the line belongs to the member above it
rather than being a member of its own.
"""

LEAST_VALUE_WIDTH = 8
"""Smallest width in cells that the value of a member is given.

A row that does not fit the terminal has to give way somewhere, and it is
the marks that are cut rather than the field: the field is what the user
edits, and `model_as_text` shows every mark in full whatever the terminal.
"""

FOLD_SHUT_TEXT = '+'
"""Label of the control of a container that is folded away."""

FOLD_OPEN_TEXT = '-'
"""Label of the control of a container that is open.

The two are what a tree has always used for this, and they are one cell wide
in every terminal, which the arrows that a modern tree draws are not.
"""

EMPHASIS_CLASSES = {core.Emphasis.MUTED: 'muted',
                    core.Emphasis.ATTENTION: 'attention',
                    core.Emphasis.WARNING: 'warning',
                    core.Emphasis.GOOD: 'good',
                    core.Emphasis.BAD: 'bad'}
"""The style class of every reason the core has to show something differently.

One class per member of `edit_cfg_json.Emphasis`, and the style sheet gives
each of them a theme colour, so that the editor follows the terminal into its
light or dark mode instead of naming colours of its own. What each kind of
text is comes from the core, so the two backends cannot colour one thing two
ways.
"""

COLOUR_RULES = ('.muted { color: $text-muted; }',
                '.attention { color: $text-accent; }',
                '.warning { color: $text-warning; }',
                '.good { color: $text-success; }',
                '.bad { color: $text-error; }')
"""What each reason to stand out looks like, as a colour of the theme.

Theme colours and not colours of this backend's own: they are what follows the
terminal into its light or dark mode, and an editor that named colours itself
would be legible in one of the two and a guess in the other.

The values and their names are left alone, so the thing the user came to edit
is the most legible thing on the screen. Everything else is either secondary
text or a state to act on, which is what `edit_cfg_json.Emphasis` names.
"""

CSS_RULES = COLOUR_RULES + (
    f'#{BODY_ID} {{ height: 1fr; }}',
    f'#{MEMBERS_ID} {{ height: auto; }}',
    f'.{MEMBER_CLASS} {{ height: auto; }}',
    f'.{ROW_CLASS} {{ height: 1; }}',
    f'.{NAME_CLASS} {{ width: {NAME_WIDTH}; }}',
    f'.{VALUE_CLASS} {{ width: 1fr; min-width: {LEAST_VALUE_WIDTH}; }}',
    f'.{MARK_CLASS}, .{SUBTREE_CLASS} {{ width: auto; }}',
    f'.{ELEMENT_CLASS} {{ width: auto; min-width: 0; height: 1;'
    ' border: none; padding: 0 1; margin: 0; }',
    f'.{FOLD_CLASS} {{ width: {FOLD_WIDTH}; min-width: {FOLD_WIDTH};'
    ' height: 1; border: none; padding: 0; margin: 0;'
    ' text-align: center; }',
    f'.{DESCRIPTION_CLASS}, .{DIAGNOSTIC_CLASS} {{ width: 1fr; height: auto;'
    f' padding-left: {DESCRIPTION_INDENT}; }}',
    f'#{DOCSTRING_ID} {{ width: 1fr; height: auto; }}',
    f'.{ROW_CLASS} Input {{ height: 1; border: none; padding: 0; }}',
    f'.{QUESTION_CLASS} {{ align: center middle; }}',
    f'#{ASK_BOX_ID} {{ width: 80%; height: auto; padding: 1 2;'
    ' border: round $primary; background: $surface; }',
    f'.{ANSWER_CLASS} {{ width: auto; height: auto; }}')
"""The width and the height of every part of one member row.

Rows are one cell high, so that the footer stays visible below them. A field
is one cell high as well, which needs its border and its padding taken away,
because both of them are part of how tall a field is.

A member is as high as it needs to be rather than one cell, because it is the
row and the description below it, and the explanatory text is as high as the
lines it takes: a container of Textual's own accord takes an equal share of
the height it is given, which would leave two members holding half a screen
each.

The body takes whatever height is left over, which is what makes it the part
that scrolls: a configuration of any size fits a terminal of any size, and the
verdict, the saving and the footer stay where the user left them, because they
are what a user reaches for after editing rather than something to scroll to.

The widths are the part that has to be said rather than left to Textual. A
`Input` is a full width widget of its own accord, so it would take the whole
line and lay the marks of the member out beyond the right edge of the screen,
where they are there and cannot be seen. The value therefore takes what is
left over and the marks take what they need, which is the opposite way round
from the default and the only way round that shows both.

A screen that asks a question sits in the middle of the screen and takes most
of its width, so that a long path or a long file name is still readable in a
narrow terminal. Its own field is untouched by the rule above, which reaches
only the fields inside a member row, and the controls that answer it take the
width they need rather than a share of the box.
"""


def value_id(index: int) -> str:
    """Return the identifier of the widget that shows one node value."""
    return f'{VALUE_ID_PREFIX}{index}'


def mark_id(index: int) -> str:
    """Return the identifier of the widget that marks one node."""
    return f'{MARK_ID_PREFIX}{index}'


def subtree_id(index: int) -> str:
    """Return the identifier of the widget that says what one object is."""
    return f'{SUBTREE_ID_PREFIX}{index}'


def description_id(index: int) -> str:
    """Return the identifier of the widget that describes one node."""
    return f'{DESCRIPTION_ID_PREFIX}{index}'


def diagnostic_id(index: int) -> str:
    """Return the identifier of the widget that refuses one node."""
    return f'{DIAGNOSTIC_ID_PREFIX}{index}'


def fold_id(index: int) -> str:
    """Return the identifier of the control that folds one container."""
    return f'{FOLD_ID_PREFIX}{index}'


def member_id(index: int) -> str:
    """Return the identifier of everything that one node owns."""
    return f'{MEMBER_ID_PREFIX}{index}'


def fold_glyph(row: core.MemberRow) -> str:
    """Return what the control of one container shows as things stand."""
    return FOLD_SHUT_TEXT if row.folded else FOLD_OPEN_TEXT


def plain_widget(text: str, widget_id: str, classes: Optional[str] = None,
                 emphasis: Optional[core.Emphasis] = None) -> Static:
    """Return a widget that shows text of the configuration as it is.

    Textual reads console markup in the text of a widget, so a square
    bracket in a configuration value or in a diagnostic would be taken for
    the beginning of a style and the text between brackets would silently
    disappear. Nothing here is written by this editor, so nothing here is
    markup.

    Args:
        text: Text to show exactly as it is.
        widget_id: Identifier the application finds this widget by.
        classes: Style classes of the widget, or None for a widget that the
            style sheet does not have to reach.
        emphasis: Why this text stands out from the values, or None for a
            widget that is shown in the ordinary text colour.

    Returns:
        A widget showing that text.
    """
    widget = Static(text, id=widget_id, markup=False, classes=classes)
    show_emphasis(widget, emphasis)
    return widget


def show_emphasis(widget: Widget, emphasis: Optional[core.Emphasis]) -> None:
    """Show one widget in the way that one reason to stand out asks for.

    Every class of `EMPHASIS_CLASSES` is set or unset, so that a widget whose
    emphasis changes as the model changes cannot end up carrying two of them
    at once.

    Args:
        widget: Widget to show.
        emphasis: Why the text of that widget stands out from the values, or
            None for the ordinary text colour.
    """
    for kind, name in EMPHASIS_CLASSES.items():
        widget.set_class(kind is emphasis, name)


def bind_action(bindings: BindingsMap, keys: Sequence[str], action: str,
                description: str) -> None:
    """Bind every key combination that the application gave one action.

    The first combination is the one the footer names and the rest work
    without being named, because a footer that named one action twice would
    suggest that they were two actions. An action the application gave no
    combination at all is bound to nothing and stays reachable through the
    command palette.

    Every binding is a priority binding, so that it is acted on before the
    field that has the focus is offered the key. That is also why the
    bindings cannot be made with `App.bind`, which cannot make one and which
    says of itself that it may be removed.

    Args:
        bindings: The bindings of the application or of the screen that the
            action belongs to.
        keys: Key combinations that run the action, in the order that
            decides which of them is named.
        action: Name of the action, without its `action_` prefix.
        description: What the footer and the key panel call the action.
    """
    for index, key in enumerate(keys):
        shown = index == 0
        bindings.bind(key, action, description, show=shown, priority=True)
