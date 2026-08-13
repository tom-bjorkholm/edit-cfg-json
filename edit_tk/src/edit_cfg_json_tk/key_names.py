#! /usr/bin/env python3
"""Binding one key combination, in the notation that Tk binds by.

The application writes its key combinations once, in the notation that
`edit_cfg_json.ActionSettings` documents, and each backend translates them
into whatever its own toolkit binds by. Tk needs a translation whatever
notation is chosen, because `<Control-Shift-S>` is a form that no other
toolkit shares.

A combination this module does not know leaves that action without that key
rather than without an editor: every action of this backend has a button as
well.

It is text going in and text coming out, and it binds nothing itself: which
part of a window a binding reaches is `tk_scope`, and needs Tk where this
needs nothing at all.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional

MODIFIERS = {'ctrl': 'Control', 'shift': 'Shift', 'alt': 'Alt',
             'meta': 'Meta'}
"""What Tk calls each modifier that a combination can name."""

KEY_NAMES = {'escape': 'Escape', 'enter': 'Return', 'tab': 'Tab',
             'space': 'space', 'backspace': 'BackSpace', 'delete': 'Delete',
             'insert': 'Insert', 'home': 'Home', 'end': 'End',
             'pageup': 'Prior', 'pagedown': 'Next', 'up': 'Up',
             'down': 'Down', 'left': 'Left', 'right': 'Right'}
"""What Tk calls each named key, where the two notations differ.

The keys of this mapping are the names that `ActionSettings` documents, and
the values are the keysyms of Tk. The two of them agree about nothing but
`Tab`, which is in here anyway so that the mapping answers for every name
the notation has rather than for the ones that happen to differ.
"""


def _tk_key(key: str, shifted: bool) -> Optional[str]:
    """Return the keysym that Tk knows one key by.

    A single character is that character, in upper case when the
    combination also names the shift, because Tk reads `<Control-S>` as the
    shifted key and `<Control-s>` as the unshifted one.

    Args:
        key: The part of a combination that is not a modifier.
        shifted: Whether the combination also names the shift.

    Returns:
        The keysym of that key, or None when this module does not know it.
    """
    if len(key) == 1:
        return key.upper() if shifted else key
    if key in KEY_NAMES:
        return KEY_NAMES[key]
    if key.startswith('f') and key[1:].isdigit():
        return key.upper()
    return None


def tk_sequence(combination: str) -> Optional[str]:
    """Return one key combination as the event sequence that Tk binds by.

    Args:
        combination: One key combination, as `ActionSettings` writes them.

    Returns:
        The Tk event sequence of that combination, or None when it names a
        modifier or a key that this module does not know. None is not an
        error: the action it belongs to keeps its button and loses only
        this way of reaching it.
    """
    parts = [part.strip().lower() for part in combination.split('+')]
    *modifiers, key = parts
    if any(modifier not in MODIFIERS for modifier in modifiers):
        return None
    keysym = _tk_key(key=key, shifted='shift' in modifiers)
    if keysym is None:
        return None
    named = [MODIFIERS[modifier] for modifier in modifiers] + [keysym]
    return f'<{"-".join(named)}>'
