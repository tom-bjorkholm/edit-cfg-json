#! /usr/bin/env python3
"""How the Textual backend names, styles and identifies its widgets.

The identifiers, the style classes and the colours of this backend are here
rather than in the module that builds the screen, because they are what one
has to look at to know how the editor will look. Nothing here knows what an
edit model is beyond the row it is given.

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

DESCRIPTION_ID_PREFIX = 'about_'
"""Prefix of the identifier of the widget that describes one node."""

DIAGNOSTIC_ID_PREFIX = 'wrong_'
"""Prefix of the identifier of the widget that refuses one node."""

FOLD_ID_PREFIX = 'fold_'
"""Prefix of the identifier of the control that folds one container."""

MEMBER_ID_PREFIX = 'member_'
"""Prefix of the identifier of everything that one node owns."""

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


def value_id(index: int) -> str:
    """Return the identifier of the widget that shows one node value."""
    return f'{VALUE_ID_PREFIX}{index}'


def mark_id(index: int) -> str:
    """Return the identifier of the widget that marks one node."""
    return f'{MARK_ID_PREFIX}{index}'


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
