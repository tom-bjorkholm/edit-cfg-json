#! /usr/bin/env python3
"""The JSON space meaning of one leaf value of the edit buffer."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import json
from config_as_json import JsonType


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


def text_as_value(text: str, is_text_member: bool) -> JsonType:
    """Return the value that the text of one edit field stands for.

    A member that holds text keeps exactly what the user typed, so that a
    text member can hold the digits of a number without becoming a number.
    Every other member has its text read as JSON, which is the inverse of
    how `value_as_text` writes it.

    Text that is not JSON at all is kept as a string rather than refused. A
    value being typed passes through states that are not valid, and a field
    that refused them could not be typed in at all. The string that a number
    member then holds is not hidden: it is the wrong type, and validation
    reports it as the wrong type.

    Args:
        text: Text that the edit field holds.
        is_text_member: Whether this member holds text.

    Returns:
        The JSON space value that the text stands for.
    """
    if is_text_member:
        return text
    try:
        value: JsonType = json.loads(text)
    except json.JSONDecodeError:
        return text
    return value


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
    return json.dumps(value) != json.dumps(other)
