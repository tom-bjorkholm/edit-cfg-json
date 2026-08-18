#! /usr/bin/env python3
"""The JSON space meaning of one leaf value of the edit buffer."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import json
from typing import Optional
from config_as_json import JsonType

TEXT_KIND = 'Text.'
"""What is said about a member that holds text."""

WHOLE_NUMBER_KIND = 'A whole number.'
"""What is said about a member that holds an integer."""

NUMBER_KIND = 'A number.'
"""What is said about a member that holds a floating point number."""

BOOL_KIND = 'True or false.'
"""What is said about a member that holds a boolean."""

VALUE_KINDS: tuple[tuple[type, str], ...] = ((bool, BOOL_KIND),
                                             (int, WHOLE_NUMBER_KIND),
                                             (float, NUMBER_KIND),
                                             (str, TEXT_KIND))
"""What each kind of leaf value is called, in the order they are asked.

The order is what makes `True` say what it is: `bool` is a subclass of `int` in
Python, so a value that is asked in the other order would be a whole number.
Nothing else here depends on the order.
"""

NO_KIND = 'No value, so what kind of value it holds is not known.'
"""What is said about a member that holds nothing at all.

The kind of a member is the kind of the value it held when the file was last
agreed with, which is the only type information there is (section 4.2 of
`doc/design.md`), and a member that held nothing gave none.
"""

BOOL_WORDS: tuple[tuple[str, bool], ...] = (('true', True), ('false', False))
"""The two words a member holding true or false is written with.

They are the JSON notation of the two values, which is what the file holds and
what the user therefore types. Nothing else means one of them: `yes` and `1`
are values of other kinds, and a member that holds one of those is a member of
another kind.
"""

BOOL_CHOICES = ', '.join(word for word, _ in BOOL_WORDS)
"""The two words as they are listed to the user, in the order asked."""


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


def text_as_value(text: str, original: JsonType) -> JsonType:
    """Return the value that the text of one edit field stands for.

    A member that holds text keeps exactly what the user typed, so that a
    text member can hold the digits of a number without becoming a number. A
    member that holds true or false takes any beginning of either word, as
    `bool_word` says. Every other member has its text read as JSON, which is
    the inverse of how `value_as_text` writes it.

    Text that is not JSON at all is kept as a string rather than refused. A
    value being typed passes through states that are not valid, and a field
    that refused them could not be typed in at all. The string that a number
    member then holds is not hidden: it is the wrong type, and validation
    reports it as the wrong type.

    Args:
        text: Text that the edit field holds.
        original: Value that this member held when the file was last agreed
            with, which is the whole of the type information there is
            (section 4.2 of `doc/design.md`). It says how the text is read
            and never what it becomes.

    Returns:
        The JSON space value that the text stands for.
    """
    if isinstance(original, str):
        return text
    if isinstance(original, bool):
        word = bool_word(text)
        if word is not None:
            return word
    try:
        value: JsonType = json.loads(text)
    except json.JSONDecodeError:
        return text
    return value


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


def value_kind(value: JsonType) -> str:
    """Return what kind of value one member holds, as a line to read.

    It is what the editor knows about a member without being told anything by
    the application: what the value is, which is what tells the digits of a
    number from a text that happens to be digits. A list and a dict answer with
    nothing, because a member the editor cannot edit yet already says which of
    the two it is where its value would be.

    Args:
        value: One leaf value of the edit buffer, in JSON space.

    Returns:
        What kind of value that is, and an empty text for a value whose kind
        is already said elsewhere.
    """
    if value is None:
        return NO_KIND
    return next((text for kind, text in VALUE_KINDS
                 if isinstance(value, kind)), '')
