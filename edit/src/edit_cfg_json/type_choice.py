#! /usr/bin/env python3
"""Which types the user may choose between, and what choosing one does.

A node whose declaration allows more than one plain type, list or dict, or one
of them and `None`, holds the one of them that the user chose (section 4.12 of
`doc/detailed_design.md`). This module answers two of the three questions
choosing raises: which of the declared types are offered at all, and what a
node holds once another is chosen. The third, which of them a node holds as
the buffer changes, is `type_options.kept_choice`, because the types of the
nodes inside a container are read through it before anything is offered.

**A type the class would refuse is not offered.** `Config.check_dict_parse`
matches what a file holds against the object the class parses it into, member
by member and down through the dicts the object holds, and refuses a dict
where the object holds something else and anything else where it holds a dict.
Where that check reaches a node is `dict_shape`, and a type of the wrong side
of it is left out of every node, because it also decides what the control that
gives a member a value would give it. `config_as_json` also hands the
value of a member with a parse converter to that converter whenever the value
is not already of the type the converter makes, and the converter it ships for
an enum refuses everything that is not text: `3` beside `Colors`, and the
`null` of an `Optional[Colors]` that its class writes as `null`. So the
converter is run on the value that choosing a type would give, as it is run on
a field losing the focus, and a type whose value it refuses is left out with a
sentence saying why. An application whose own converter takes more is offered
more, which is principle 1 of section 3 of the design. That one is asked only
of a node whose type is chosen, because only there is the value of another
type something the user could give it.

**The choice outlives the value**, because a value can fit more than one type:
`5` is an `int` and a `float`, `''` is a `str` and may be a `Literal` of
text, and `[]` is a `list[str]` and a `list[list[str]]`. So the type a node
holds is first read from its value, then kept, and
read from the value again only where a validation pass left a value that the
kept type does not fit. Typing never changes it: a text that is no number,
typed while `int` is chosen, is a value of the wrong type and not a choice.

**Switching keeps what still fits.** A plain value keeps its text where that
text means a value of the new type, so the text `5` becomes the number `5`
when `str` is changed to `int`, and everything else is given the empty value
of the new type: `''`, `0`, the first name of an enum, the first value of a
`Literal`, or nothing at all. A list or a dict on either side of the switch
is given that empty value as well, `[]` and `{}` among them, because what a
container held is no value of a container of another type.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Sequence
from typing import NamedTuple, Optional
import json
from config_as_json import JsonType, ParseConverter
from edit_cfg_json.converting import CONVERSION_ERRORS
from edit_cfg_json.leaf_value import text_as_value, value_as_text
from edit_cfg_json.type_options import SCALAR_KINDS, TypeOption, choosable, \
    empty_option_value, fits

NOT_CONVERTED_FORM = ('{type} is not offered, because the parse converter of '
                      'this member refuses {value}.')
"""What is said below a node about a declared type the class would refuse.

The value is written in JSON, so that the empty text is `""` and no value at
all is `null`, which is what the converter would be given.
"""

NO_DICT_YET = ('{type} is not offered, because the configuration class '
               'matches a dict written here against the dict it holds here, '
               'and it holds none.')
"""What is said below a node about a dict type the class would refuse.

`Config.check_dict_parse` refuses a dict written for a place where the object
it parses into holds no dict — *Unexpected dictionary for X in JSON data* —
whatever keys it has and even where it has none, so the empty dict that
choosing the type would give is refused as surely as any other. It is the
check that refuses a new key of a dict the class declares the keys of, one
step up.
"""

DICT_ONLY = ('{type} is not offered, because the configuration class holds a '
             'dict here and refuses anything else written for it.')
"""What is said below a node about a type the class refuses beside a dict.

It is the other half of the same check: where the object holds a dict, the
file has to hold one too — *Not dictionary for X in JSON data* — and `None` is
no dict, which is what makes the `remove` of a member that its class writes as
`null` and that holds a dict a control that produced a refusal.
"""

NOT_CHOOSABLE = 'The type of {name} is not one to choose.'
"""Message of the error raised when the type of a node cannot be chosen."""

NOT_OFFERED = '{name} may hold {types}, and not {type}.'
"""Message of the error raised when a node is given a type it is not offered.
"""


class TypeOffer(NamedTuple):
    """The types one node is offered, and why any declared one is not."""

    offered: tuple[TypeOption, ...]
    """The declared types the class would accept, in declared order."""

    refusals: tuple[str, ...] = ()
    """One sentence per declared type that is left out, saying why."""


def offered_types(options: Sequence[TypeOption],
                  converter: Optional[ParseConverter], omitted: bool,
                  holds_dict: Optional[bool]) -> TypeOffer:
    """Return which of the types one node may hold its class would accept.

    The dict-shape check is asked of every node, and the parse converter only
    of a node whose type is the user's to choose: every other node holds what
    its value is, and only the control that gives it a value makes a value of
    one of its types, which is never one the converter is asked about.

    Args:
        options: The types the declaration of that node allows.
        converter: How the text of that node becomes the value it holds, or
            None for a node that holds what the file holds.
        omitted: Whether its class leaves it out of the file while it holds
            nothing, which is when `config_as_json` converts nothing at all.
        holds_dict: Whether the dict-shape check demands a dict at that node,
            None where the check does not reach it, as `dict_shape` says.

    Returns:
        The types offered, and why each of the others is not.
    """
    asking = converter if choosable(options) else None
    reasons = [_refusal(option=option, converter=asking, omitted=omitted,
                        holds_dict=holds_dict) for option in options]
    return TypeOffer(offered=tuple(option for option, reason
                                   in zip(options, reasons) if not reason),
                     refusals=tuple(reason for reason in reasons if reason))


def _refusal(option: TypeOption, converter: Optional[ParseConverter],
             omitted: bool, holds_dict: Optional[bool]) -> str:
    """Return why one type is not offered, empty where it is.

    A class of the application's own whose kind only the value can say is
    never refused by the dict-shape check, because nothing says it is or is
    not written as a dict.
    """
    if holds_dict is not None and option.kind is not None and \
            (option.kind is dict) != holds_dict:
        return (DICT_ONLY if holds_dict else NO_DICT_YET).format(
            type=option.text)
    if converter is not None and \
            not _converts(option=option, converter=converter, omitted=omitted):
        return NOT_CONVERTED_FORM.format(
            type=option.text, value=json.dumps(empty_option_value(option)))
    return ''


def _converts(option: TypeOption, converter: ParseConverter,
              omitted: bool) -> bool:
    """Return whether one converter takes the empty value of one type."""
    value = empty_option_value(option)
    if (value is None and omitted) or \
            isinstance(value, converter.result_type):
        return True
    try:
        converter.func(value, **converter.args)
    except CONVERSION_ERRORS:
        return False
    return True


def chosen_option(options: Sequence[TypeOption], text: str,
                  name: str) -> TypeOption:
    """Return the type one text names among those one node is offered.

    Args:
        options: The types that node is offered.
        text: The type as a Python type hint spells it.
        name: What the node is called, for the message.

    Returns:
        The type that text names.

    Raises:
        ValueError: The type of that node is not the user's to choose, or the
            text names none of its types.
    """
    if not choosable(options):
        raise ValueError(NOT_CHOOSABLE.format(name=name))
    found = next((option for option in options if option.text == text), None)
    if found is None:
        raise ValueError(NOT_OFFERED.format(
            name=name, type=text,
            types=', '.join(option.text for option in options)))
    return found


def switched_value(option: TypeOption, value: JsonType) -> JsonType:
    """Return what one node holds once the user has chosen one of its types.

    Args:
        option: The type chosen.
        value: The value the node held before.

    Returns:
        That value read again as a value of the new type, where both are
        plain values and its text means one, and the empty value of the new
        type otherwise.
    """
    if option.kind not in SCALAR_KINDS or value is None or \
            isinstance(value, (list, dict)):
        return empty_option_value(option)
    kept = text_as_value(text=value_as_text(value), kind=option.kind)
    return kept if fits(option, kept) else empty_option_value(option)
