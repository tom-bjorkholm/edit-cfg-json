#! /usr/bin/env python3
"""The JSON space meaning of one leaf value of the edit buffer."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from copy import deepcopy
from typing import Optional
import json
from config_as_json import JsonType

VALUE_KINDS: tuple[type, ...] = (bool, int, float, str, list, dict)
"""Every kind of leaf value, in the order they are asked.

The order is what makes `True` say what it is: `bool` is a subclass of `int` in
Python, so a value that is asked in the other order would be a whole number.
Nothing else here depends on the order.
"""

EMPTY_VALUES: tuple[tuple[type, JsonType], ...] = ((bool, False), (int, 0),
                                                   (float, 0.0), (str, ''),
                                                   (list, []), (dict, {}))
"""What a value of each kind is before anything has been put into it.

It is what a member that holds nothing is given when the user asks for it to
hold something, and what an element of a list that the class declares empty
is. Nothing here is invented about the *application*: the kind is what the
class declared, and the value is the one value of that kind that says nothing
more than which kind it is.
"""

NO_VALUE_TEXT = 'no value'
"""What the row of a member holding nothing says where a value would be.

It is worded as the `no {name}` of a declared member holding no configuration
object, because it is the same state one step down: the member is one the
class allows to hold nothing, and it holds nothing. Showing the `null` that
the file holds would be showing the notation of the file as if it were a value
the user had typed, and it is exactly the confusion between that `null` and an
empty text that this state exists to end.
"""


BOOL_WORDS: tuple[tuple[str, bool], ...] = (('true', True), ('false', False))
"""The two words a member holding true or false is written with.

They are the JSON notation of the two values, which is what the file holds and
what the user therefore types. Nothing else means one of them: `yes` and `1`
are values of other kinds, and a member that holds one of those is a member of
another kind.
"""

BOOL_NAMES: tuple[str, ...] = tuple(word for word, _ in BOOL_WORDS)
"""The two words on their own, in the order they are asked in.

It is what a member holding true or false is offered as the values it takes,
where a member holding an enum is offered the names of that enum. The order
is the one above, so that the first value such a member can be given is
`true`.
"""

BOOL_CHOICES = ', '.join(BOOL_NAMES)
"""The two words as they are listed to the user, in the order asked."""


def empty_value(kind: Optional[type]) -> JsonType:
    """Return the value of one kind that says no more than its kind.

    Args:
        kind: Kind of value to make one of, None for a kind nothing says.

    Returns:
        That value, and None where nothing says which kind it would be. A
        fresh one every time, because a list and a dict are values that the
        next edit would otherwise reach through.
    """
    return deepcopy(next((empty for known, empty in EMPTY_VALUES
                          if known is kind), None))


def kind_of(value: JsonType) -> Optional[type]:
    """Return the kind of one value, None for a value that has no kind.

    Args:
        value: One leaf value of the edit buffer, in JSON space.

    Returns:
        The kind of that value, which is None only for `null`.
    """
    return next((kind for kind in VALUE_KINDS if isinstance(value, kind)),
                None)


def bool_word(text: str) -> Optional[bool]:
    """Return the value that the beginning of one of those words means.

    The case is ignored and a beginning is enough, which is what
    `config_as_json` already does for the name of an enum member: its
    `string_to_enum_best_match` tries the case variants of what was typed and
    then accepts a beginning that only one member has. A member holding true
    or false has no such converter, because there is nothing to convert it
    into, so it is answered here and by the same rules.

    A beginning that both words have is no answer, exactly as an ambiguous
    beginning of two enum member names is none. The empty text is the only one
    there is, and it is what a cleared field holds.

    Args:
        text: Text that the edit field holds.

    Returns:
        The value that text means, and None when it means neither of them.
    """
    typed = text.strip().lower()
    matched = [value for word, value in BOOL_WORDS if word.startswith(typed)]
    return matched[0] if len(matched) == 1 else None


def value_as_text(value: JsonType) -> str:
    """Return the text that an edit field shows for one value.

    A string is shown as the string itself. The quotation marks that JSON
    puts around a string belong to the file format and not to the value, so
    showing them would make the user believe that the text really begins and
    ends with a quotation mark. Every other value is shown as its JSON
    notation, which is also how the user would type it.

    Args:
        value: One leaf value of the edit buffer, in JSON space.

    Returns:
        The text of that value.
    """
    return value if isinstance(value, str) else json.dumps(value)


def text_as_value(text: str, kind: Optional[type],
                  nothing: bool = False) -> JsonType:
    """Return the value that the text of one edit field stands for.

    A member that takes text keeps exactly what the user typed, so that a
    text member can hold the digits of a number without becoming a number. A
    member that takes true or false takes any beginning of either word, as
    `bool_word` says. Every other member has its text read as JSON, which is
    the inverse of how `value_as_text` writes it.

    Text that is not JSON at all is kept as a string rather than refused. A
    value being typed passes through states that are not valid, and a field
    that refused them could not be typed in at all. The string that a number
    member then holds is not hidden: it is the wrong type, and validation
    reports it as the wrong type.

    **A field cannot put a member into the state that holds nothing.** Where a
    member has that state it has a control that means it, and `null` typed
    into the field is text that means no value of the member, exactly as any
    other text of the wrong type is. Without that, the four characters of
    `null` would take the field away from under the cursor that typed them. A
    member with no such state reads `null` as the JSON it is, as before.

    Args:
        text: Text that the edit field holds.
        kind: Which kind of value the text is read as, None where nothing
            says: what the class declared, and failing that what the member
            held when the file was last agreed with (section 4.2 of
            `doc/detailed_design.md`).
        nothing: Whether this member has the state of holding nothing.

    Returns:
        The JSON space value that the text stands for.
    """
    if kind is str:
        return text
    if kind is bool:
        word = bool_word(text)
        if word is not None:
            return word
    try:
        value: JsonType = json.loads(text)
    except json.JSONDecodeError:
        return text
    return text if value is None and nothing else value


def canonical_text(value: JsonType) -> str:
    """Return one value as the text that decides whether it is unchanged.

    The keys of a dictionary are sorted, because `config_as_json` writes them
    sorted and a file that holds the same values in another order holds the
    same values. The editor does hold them in another order: the members of a
    nested configuration object are kept in the order its class declares them,
    which is the order they are read in and not the order they are written in.

    Everything else is compared as it is written, which is what tells `1` from
    `1.0` and from `true`: all three of them reach the file differently.

    Args:
        value: One value in JSON space.

    Returns:
        The text that stands for that value.
    """
    return json.dumps(value, sort_keys=True)


def values_differ(value: JsonType, other: JsonType) -> bool:
    """Return whether two values would be written to the file differently.

    The comparison is made on the JSON notation and not with `==`, because
    Python considers `True` equal to `1` and `1` equal to `1.0`, while a
    JSON file shows all three of them differently. Changing a member from
    `1` to `1.0` changes the file, so it is a change that the user made and
    the editor has to say so.

    Args:
        value: One value in JSON space.
        other: The value to compare it with.

    Returns:
        Whether the two values are different values.
    """
    return canonical_text(value) != canonical_text(other)
