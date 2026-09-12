#! /usr/bin/env python3
"""What the configuration makes of the text of one leaf of the buffer.

The buffer holds JSON space values, and some members do not hold a JSON space
value at all once the configuration class has them: `parse_converters()` says
which of them become a richer Python type and how. An enum is the case that
arises in practice, and it is what makes this worth having. A name that is no
member of an enum cannot be turned into one, and `config_as_json` reports that
inside the message it prints for JSON it could not load — which is right for a
program reading a file and wrong for a person editing a field, who was not
asking about JSON at all.

The converter that the class declared is *run* rather than looked at, exactly
as `config_as_json` runs it while it parses. That is the same rule that
validation follows and for the same reason: an application may declare any
converter it likes, and running the real one is right for every converter that
exists or ever will.

Which class declared it is a question of its own once there are nested
configuration objects, and `node_converters` is where it is answered: a nested
object parses its own JSON, so what is inside it is answered by its own class
and not by the class above it.

Running the converter is also what answers *which of the values a member takes
one value means*, which is what a pull-down of those values has to know. That
is `matched_choice`, and it is here rather than beside the values themselves
for the reason above: the reading of a name is the conversion the class
declared and never a rule of this editor.

What a text the class itself refuses most likely meant is a different question
and `nearest_choice` is a different answer, which runs no converter and asks
the class nothing. It is the editor allowing for one mistyped character in a
text it has to make a value of anyway, so it is the one reading here that is a
rule of this editor, and it is kept apart from the reading above for exactly
that reason.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Mapping, Sequence
from enum import Enum
from typing import NamedTuple, Optional
from config_as_json import Config, ConfigPath, JsonType, ParseConverter
from edit_cfg_json.leaf_value import BOOL_CHOICES, value_as_text
from edit_cfg_json.tree import ConfigNode, owner_path, under_dict

CONVERSION_ERRORS = (AssertionError, AttributeError, KeyError, TypeError,
                     ValueError)
"""Every way in which a parse converter can refuse one value.

`config_as_json` catches every exception around the parsing it does, so a
converter is not promised to fail in any particular way, and these are the
ways in which the converters it ships do fail: a name that is no member of an
enum raises `KeyError`, and a value that is not text at all trips the
assertion that the enum converter begins with.

`NotImplementedError` is deliberately not one of them, exactly as it is not
one of the failures a validation pass catches: it says that the configuration
class is incomplete, which is a defect of the application that no edit of the
buffer can put right.
"""

REPLACED_FORM = ('{name}: {text} is no value this member takes, so it has '
                 'been given {value}.')
"""What is said about a text that had to make way for a value.

A pull-down offers the values its member takes and nothing else, and holds one
of them at every moment, so a text that means none of them has to become one
of them. The member is given the value `nearest_choice` says it most likely
meant, and this is the sentence that says what became of what was there —
which the editor owes the user, because it is the one change of the buffer
that the user did not make, and because the value it was given is the editor
reading a mistyped text rather than the class reading a name.
"""

CLEARED_FORM = ('{name}: an empty field is no value this member takes, so '
                'it has been given {value}.')
"""The same for a member whose field held nothing at all.

It is a form of its own because the sentence above it would name the text and
there is none, leaving a gap where the reader is looking for what was there.
"""

NOT_A_BOOL_FORM = '{text} is not one of: {words}'
"""Why the text of a member holding true or false means neither of them.

It is worded as `config_as_json` words the same refusal about the name of an
enum member, because it is the same refusal: the member holds one of a known
set of values and the text names none of them. Such a member has no parse
converter to answer it — there is nothing to convert true into — so this is
the one refusal of a leaf that the editor makes itself, and it makes it about
the type of the member and never about a rule of the application.
"""


class Converted(NamedTuple):
    """One leaf value as the configuration class would hold it."""

    value: object
    """What the converter of that member made of the value, or the value.

    It is the value itself for a member that has no converter, and also for
    one whose converter refused it, so that there is always something to go
    on. The type is genuinely unknown here: a converter may return anything.
    """

    message: str
    """Why the converter refused the value, empty when nothing refused it."""


def member_converters(config: Config) -> dict[str, ParseConverter]:
    """Return the parse converters of the members that one class declares.

    A class that declares none inherits a placeholder converter under a key of
    the base class's own, so the answer is restricted to the members the
    object really has. A converter named after something that is no member of
    the configuration could never be applied to anything in any case.

    Args:
        config: Configuration object to ask. It is not modified.

    Returns:
        One converter per member that has one.
    """
    declared = vars(config)
    return {name: converter
            for name, converter in (config.parse_converters() or {}).items()
            if name in declared}


def node_converters(nodes: Mapping[ConfigPath, ConfigNode],
                    flat: Sequence[tuple[ConfigPath, JsonType]]) \
        -> dict[ConfigPath, ParseConverter]:
    """Return the parse converter of every node of one tree that has one.

    Two things decide it, and each of them is a rule of `config_as_json`
    rather than of this editor. A converter is applied while an object is
    decoded, so it reaches the value of a dictionary key at any depth and
    never an element of a list. And a converter belongs to the class that owns
    the subtree, exactly as a write-side converter does: a nested
    configuration object parses its own JSON and applies its own converters,
    so the converters of the class above it are not the ones that answer for
    what is inside it.

    Args:
        nodes: Every configuration object of the tree, by its path.
        flat: The path and the value of every node, in row order.

    Returns:
        One converter per node that has one, by the path of that node.
    """
    owned = {path: member_converters(node.config)
             for path, node in nodes.items() if node.config is not None}
    values = dict(flat)
    found = ((path, owned.get(owner_path(path=path, nodes=nodes), {})
              .get(path[-1]))
             for path, _ in flat if under_dict(path=path, values=values))
    return {path: converter for path, converter in found
            if converter is not None}


def convert_member(converter: Optional[ParseConverter], value: JsonType,
                   is_bool_member: bool = False) -> Converted:
    """Return one leaf value as its member holds it, or why it cannot.

    A value that already has the type the converter produces is left alone,
    and so is a value that is `None`: a member that its class leaves out of
    JSON while it is None has nothing to convert, and a `None` that is wrong
    is refused by the validation of the whole configuration, which has a
    message of its own for it.

    A member holding true or false is answered without a converter, because
    it has none and needs none: `text_as_value` has already made the value of
    every text that means one of the two words, so a value that is neither
    means neither and is refused here as an enum member name that names no
    member is.

    Args:
        converter: How the text of this member becomes a value, or None for a
            member that holds what the file holds.
        value: JSON space value that the buffer holds for that member.
        is_bool_member: Whether this member held true or false when the file
            was last agreed with, which is what makes those the two values it
            takes.

    Returns:
        The value the configuration would hold, or the reason it would not.
    """
    if value is None:
        return Converted(value=value, message='')
    if converter is None:
        return _converted_bool(value=value, is_bool_member=is_bool_member)
    if isinstance(value, converter.result_type):
        return Converted(value=value, message='')
    try:
        return Converted(value=converter.func(value, **converter.args),
                         message='')
    except CONVERSION_ERRORS as error:
        return Converted(value=value, message=refusal_text(error))


def _converted_bool(value: JsonType, is_bool_member: bool) -> Converted:
    """Return one value of a member that no converter answers for.

    Args:
        value: JSON space value that the buffer holds for that member.
        is_bool_member: Whether that member holds true or false.

    Returns:
        The value, and why it is neither of the two words where it is neither.
    """
    if not is_bool_member or isinstance(value, bool):
        return Converted(value=value, message='')
    said = NOT_A_BOOL_FORM.format(text=value_as_text(value),
                                  words=BOOL_CHOICES)
    return Converted(value=value, message=said)


def matched_choice(converter: Optional[ParseConverter], value: JsonType,
                   choices: Sequence[str],
                   is_bool_member: bool = False) -> str:
    """Return which of the values one member takes its value means.

    A value that is already one of them means itself. Anything else is handed
    to the conversion that the class declared, which is the same reading that
    a field losing the focus is answered by: `config_as_json` accepts the name
    of a member of that enum in any case, and accepts a beginning that only
    one member of that enum has. Which beginnings those are is a fact about
    the enum the application declared and about nothing else: a beginning that
    names one member of one enum names two of another. A member holding true
    or false needs no conversion, because `text_as_value` has already made the
    value of every text that means one of the two words.

    Args:
        converter: How the text of this member becomes a value, or None for a
            member that holds what the file holds.
        value: JSON space value that the buffer holds for that member.
        choices: The values that member takes, as the text of each of them.
        is_bool_member: Whether this member holds true or false.

    Returns:
        The value it means, as text, and an empty text where it means none of
        them or more than one of them.
    """
    text = value_as_text(value)
    if text in choices:
        return text
    converted = convert_member(converter=converter, value=value,
                               is_bool_member=is_bool_member)
    if converted.message or not isinstance(converted.value, Enum):
        return ''
    name = converted.value.name
    return name if name in choices else ''


def nearest_choice(text: str, choices: Sequence[str]) -> str:
    """Return which value one text that means none of them most likely meant.

    It is asked where `matched_choice` answered with nothing, which is a text
    the class itself refuses, and what it does is assume the user typed what
    they meant and then allow for one mistyped character. Four questions in
    this order, and the first of them that answers decides:

    - Is there exactly one value that **one character change** turns the text
      into? Changing a character is changing what it is, adding one or
      dropping one, which are the three ways one is mistyped.
    - Do the values the text is **the beginning of** narrow it down? The first
      of them is taken, which is why `MEC` means `MECHANIC` where the values
      are `ELECTRIC`, `MECHANIC` and `MECHATRONIC`: it begins two of them and
      the first of those two is taken.
    - Do they narrow it down **once one character is changed**? That is why
      `MEK` means `MECHANIC` among those same three values.
    - Nothing of the above, so the **first value the member takes**, which is
      the answer this had before it had any of the others.

    The case is ignored throughout, as it is ignored by the reading that was
    asked first, and the space around the text is not part of what was typed.

    Args:
        text: What the field of that member held.
        choices: The values that member takes, as the text of each of them,
            which is never empty for a member that has a set of values.

    Returns:
        The value it most likely meant, and an empty text only where that
        member takes no values at all.
    """
    typed = text.strip().lower()
    corrected = [name for name in choices
                 if _one_edit_apart(typed, name.lower())]
    ranked = (corrected if len(corrected) == 1 else [],
              [name for name in choices if name.lower().startswith(typed)],
              [name for name in choices if _starts_near(typed, name.lower())],
              list(choices))
    return next((names[0] for names in ranked if names), '')


def _one_edit_apart(typed: str, name: str) -> bool:
    """Return whether one character change turns one text into another.

    What the two texts do not share is then one character of each of them at
    most, so what they begin with in common and what the rest of them ends
    with in common is the whole of what decides it. The longer of the two
    says how much is left over, which is one character for a change of any of
    the three kinds and none at all for two texts that are the same text.

    Args:
        typed: What was typed, in the case the comparison is made in.
        name: The value to compare it with, in that same case.

    Returns:
        Whether one change of one character is all that separates them.
    """
    same = _shared_start(typed, name)
    tail = _shared_start(typed[same:][::-1], name[same:][::-1])
    return max(len(typed), len(name)) - same - tail <= 1


def _starts_near(typed: str, name: str) -> bool:
    """Return whether one character change makes one text begin another.

    How long a beginning is worth trying is decided by the text itself: one
    character change makes a text as long as itself, one shorter or one
    longer, so those are the three beginnings of the name there is any point
    in comparing it with.

    Args:
        typed: What was typed, in the case the comparison is made in.
        name: The value whose beginnings to compare it with, in that case.

    Returns:
        Whether one change of one character makes it a beginning of that
        value.
    """
    cuts = range(max(0, len(typed) - 1), len(typed) + 2)
    return any(_one_edit_apart(typed, name[:cut]) for cut in cuts)


def _shared_start(text: str, other: str) -> int:
    """Return how many characters two texts begin with in common.

    Args:
        text: One of the two texts.
        other: The other of them.

    Returns:
        How many characters they have in common from the beginning, which is
        none for two texts that begin differently and for an empty text.
    """
    same = 0
    for one, another in zip(text, other):
        if one != another:
            break
        same += 1
    return same


def replaced_text(name: str, text: str, value: str) -> str:
    """Return what is said about one text that a value was put in place of.

    Args:
        name: What the member is called on its own, which is the whole path
            for reaching it.
        text: What the field of that member held.
        value: The value it has been given instead.

    Returns:
        The sentence the user is shown about that member.
    """
    form = REPLACED_FORM if text else CLEARED_FORM
    return form.format(name=name, text=text, value=value)


def refusal_text(error: Exception) -> str:
    """Return what one refusal says, as the user should read it.

    A `KeyError` writes the representation of its argument rather than the
    argument itself, so the message about a name that is no member of an enum
    would otherwise arrive wrapped in quotation marks that nobody wrote.

    Args:
        error: The failure that was reported.

    Returns:
        What that failure says.
    """
    if isinstance(error, KeyError) and error.args:
        return str(error.args[0])
    return str(error)
