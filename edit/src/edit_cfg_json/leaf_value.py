#! /usr/bin/env python3
"""The JSON space meaning of one leaf value of the edit buffer."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from copy import deepcopy
from typing import NamedTuple, Optional
import json
from config_as_json import JsonType

TEXT_KIND = 'Text.'
"""What is said about a member that holds text."""

WHOLE_NUMBER_KIND = 'A whole number.'
"""What is said about a member that holds an integer."""

NUMBER_KIND = 'A number.'
"""What is said about a member that holds a floating point number."""

BOOL_KIND = 'True or false.'
"""What is said about a member that holds a boolean."""

LIST_KIND = 'A list.'
"""What is said about a member that holds a list and holds none now.

A member that really holds one says nothing here, because its row already says
how many elements there are. It is only worth saying where the row says that
the member holds nothing at all, which is where the kind of the value comes
from the declaration and not from a value.
"""

DICT_KIND = 'A dict.'
"""The same for a member that holds a dict and holds none now."""

VALUE_KINDS: tuple[tuple[type, str], ...] = ((bool, BOOL_KIND),
                                             (int, WHOLE_NUMBER_KIND),
                                             (float, NUMBER_KIND),
                                             (str, TEXT_KIND),
                                             (list, LIST_KIND),
                                             (dict, DICT_KIND))
"""What each kind of leaf value is called, in the order they are asked.

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

NO_KIND = 'No value, so what kind of value it holds is not known.'
"""What is said about a member whose kind nothing says.

The kind of a member is what the class declared for it, and failing that the
kind of the value it held when the file was last agreed with (section 4.2 of
`doc/design.md`). A member that has neither gave none.
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

BOOL_CHOICES = ', '.join(word for word, _ in BOOL_WORDS)
"""The two words as they are listed to the user, in the order asked."""


class LeafType(NamedTuple):
    """What the class of a configuration says one leaf of it holds.

    It is what the declaration of a member says, and it is empty where the
    declaration says nothing this editor can use: an annotation naming a class
    of the application's own, a member with no annotation at all, and a class
    whose source cannot be read all answer with this holding nothing.
    """

    kind: Optional[type] = None
    """Which kind of value belongs here, None where nothing says.

    It is one of the types of `VALUE_KINDS` and never a class of the
    application: what the editor does with a kind is say what it is and make
    an empty one of it, and it can do neither with a class it has never seen.
    """

    nothing: bool = False
    """Whether this member may hold no value at all.

    `Optional[str]` says it, and so does `str | None`. It is never true where
    `kind` says nothing, because the two states of such a member are *holds a
    value* and *holds nothing*, and a member the editor cannot make a value
    for has only one of them.

    It is set for a member that a class declares and never for a value inside
    a list or a dict. What may hold nothing is something a class says about a
    member of its own, and an element that could be taken out of what holds it
    already has a control that means that.
    """

    inside: Optional['LeafType'] = None
    """What one value inside this one is, None where nothing says.

    It is the element of a list and the value of a dict, which is what says
    what an element of a list that its class declares empty would be.
    """


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
    return next((kind for kind, _ in VALUE_KINDS if isinstance(value, kind)),
                None)


def leaf_kind(declared: LeafType, original: JsonType) -> Optional[type]:
    """Return the kind of value that one leaf takes.

    What the class declared wins over what the leaf held, because a member
    declared `float` whose default is written `0` is a number member whatever
    the value says, and a member declared `Optional[str]` says that it takes
    text while it holds nothing at all. The value answers where the class said
    nothing, which is a class whose source cannot be read and a member with no
    annotation.

    Args:
        declared: What the class says the value here is.
        original: Value that the leaf held when the file was last agreed with.

    Returns:
        The kind of value that leaf takes, None where nothing says.
    """
    return declared.kind if declared.kind is not None else kind_of(original)


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


def text_as_value(text: str, original: JsonType,
                  declared: LeafType = LeafType()) -> JsonType:
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
        original: Value that this member held when the file was last agreed
            with, which says how the text is read where the class said
            nothing. It never says what the text becomes.
        declared: What the class says the value here is, which says how the
            text is read wherever it says anything (section 4.2 of
            `doc/design.md`).

    Returns:
        The JSON space value that the text stands for.
    """
    kind = leaf_kind(declared=declared, original=original)
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
    return text if value is None and declared.nothing else value


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


def kind_text(declared: LeafType, value: JsonType) -> str:
    """Return what kind of value one node holds, as a line to read.

    It is what the editor knows about a member without being told anything by
    the application: which kind of value belongs there, which is what tells
    the digits of a number from a text that happens to be digits. What the
    class declared is asked first and the value answers where it said nothing,
    which is what `leaf_kind` decides.

    A node that really holds a list or a dict answers with nothing, because
    its row already says how many things are in it and the rows below it say
    what each of them is. One that holds nothing does say which of the two it
    would be, because its row then says only that it holds nothing.

    Args:
        declared: What the class says the value here is.
        value: Value that the node holds, in JSON space.

    Returns:
        What kind of value that is, and an empty text for a value whose kind
        is already said elsewhere.
    """
    if isinstance(value, (list, dict)):
        return ''
    kind = leaf_kind(declared=declared, original=value)
    if kind is None:
        return NO_KIND
    return next((text for known, text in VALUE_KINDS if known is kind), '')
