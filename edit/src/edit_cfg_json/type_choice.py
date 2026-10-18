#! /usr/bin/env python3
"""Which types the user may choose between, and what choosing one does.

A node whose declaration allows more than one plain type, list, dict or
configuration class, or one of them and `None`, holds the one of them that the
user chose (section 4.12 of `doc/detailed_design.md`). This module answers two
of the three questions choosing raises: which of the declared types are offered
at all, and what a node holds once another is chosen. The third, which of them
a node holds as the buffer changes, is `type_options.kept_choice`, because the
types of the nodes inside a container are read through it before anything is
offered.

**A type the class would refuse is not offered.** `Config.check_dict_parse`
matches what a file holds against the object the class parses it into, member
by member and down through the dicts the object holds, and refuses a dict
where the object holds something else and anything else where it holds a dict.
Where that check reaches a node is `dict_shape`, and a type of the wrong side
of it is left out of every node. `config_as_json` also hands the value of a
member with a parse converter to that converter whenever the value is not
already of the type the converter makes, and the converter it ships for an
enum refuses everything that is not text: `3` beside `Colors`, and the `null`
of an `Optional[Colors]` that its class writes as `null`. So the converter is
run on the value that choosing a type would give, as it is run on a field
losing the focus, and a type whose value it refuses is left out with a
sentence saying why. An application whose own converter takes more is offered
more, which is principle 1 of section 3 of the design. That one is asked only
of a node whose type is chosen, because only there is the value of another
type something the user could give it.

**The choice outlives the value**, because a value can fit more than one type:
`5` is an `int` and a `float`, `''` is a `str` and may be a `Literal` of text,
and `[]` is a `list[str]` and a `list[list[str]]`. So the type a node holds is
first read from its value, then kept, and read from the value again only where
a validation pass left a value that the kept type does not fit. Typing never
changes it: a text that is no number, typed while `int` is chosen, is a value
of the wrong type and not a choice.

**A configuration class is offered where a declaration puts its object.**
`nested_configs()` is what says that an object is at a place, and nothing else
makes `config_as_json` read one: a dict written anywhere else is read as the
dict it is, and an object found anywhere else is refused. So the class is
offered only where the tree declares an object, and there only where one is
or the editor can construct one, because choosing it is what constructs it.

**A type the editor cannot make a value of is offered only where it must
be**, which is where the node holds it or where nothing besides `None` could
be chosen instead. `Optional[int | Path]` is offered `int | None` while it
holds a number, because choosing `Path` could give it no value of `Path`, and
`Path | None` stays the field it always was, because leaving `Path` out would
leave it nothing but `None` to hold.

**Switching keeps what still fits.** A plain value keeps its text where that
text means a value of the new type, so the text `5` becomes the number `5`
when `str` is changed to `int`, and everything else is given the empty value
of the new type: `''`, `0`, the first name of an enum, the first value of a
`Literal`, or nothing at all. A list or a dict on either side of the switch
is given that empty value as well, `[]` and `{}` among them, because what a
container held is no value of a container of another type. A configuration
class is given a new object of it, which `placing.object_switched` constructs,
because no value says more about one than its class does.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Sequence
from typing import NamedTuple, Optional
import json
from config_as_json import JsonType, ParseConverter
from edit_cfg_json.converting import CONVERSION_ERRORS
from edit_cfg_json.leaf_value import text_as_value, value_as_text
from edit_cfg_json.type_options import NONE_TYPE, SCALAR_KINDS, TypeOption, \
    choosable, empty_option_value, fits, held_option, makes_value, \
    names_config

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

NO_OBJECT_HERE = ('{type} is not offered, because the configuration class '
                  'reads one only where nested_configs() declares it, and it '
                  'declares none here.')
"""What is said below a node about a configuration class it cannot hold.

`config_as_json` makes an object of a class only where `nested_configs()`
declares one: a dict written anywhere else is read as a dict, and an object
held anywhere else is refused, which is what `_validate_dict_by_key` does with
an object beside the keys a `DICT_VALUE_BY_KEY` declaration names.
"""

NOT_MADE = ('{type} is not offered, because the editor cannot make one on its '
            'own.')
"""What is said below a node about a type the editor cannot give it.

It is a class of the application's own whose kind only its value can say, an
enum with no members, and a configuration class whose declaration names a
constructor the editor cannot call. The node is offered such a type wherever
it holds a value of it, so this is said only where choosing it would have had
to invent one.
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


class NodeFacts(NamedTuple):
    """What decides which of its declared types one node is offered."""

    value: JsonType = None
    """The value the node holds now, which says the one type it holds."""

    converter: Optional[ParseConverter] = None
    """How the text of the node becomes its value, None where it is as read."""

    omitted: bool = False
    """Whether its class leaves it out of the file while it holds nothing.

    That is when `config_as_json` converts nothing at all.
    """

    holds_dict: Optional[bool] = None
    """Whether the dict-shape check demands a dict at the node.

    It is None where the check does not reach it, as `dict_check.dict_shape`
    says.
    """

    placed: Optional[bool] = None
    """Whether the node can hold the object a declaration puts there.

    It is None where `nested_configs()` declares no object at the node, and
    otherwise whether one is there or the editor can construct one.
    """


def offered_types(options: Sequence[TypeOption],
                  facts: NodeFacts) -> TypeOffer:
    """Return which of the types one node may hold its class would accept.

    The dict-shape check and the declarations of objects are asked of every
    node, and the parse converter only of a node whose type is the user's to
    choose: every other node holds what its value is. A type the editor
    cannot make a value of is left out last, once it is known whether
    anything besides `None` is left to be chosen instead.

    Args:
        options: The types the declaration of that node allows.
        facts: What the class says about the node, and what it holds.

    Returns:
        The types offered, and why each of the others is not.
    """
    asked = facts if choosable(options) else facts._replace(converter=None)
    found = [_refusal(option=option, facts=asked) for option in options]
    making = any(makes_value(option)
                 for option, reason in zip(options, found) if not reason)
    held = held_option(options, facts.value)
    reasons = [reason or _unmade(option=option, held=held, making=making)
               for option, reason in zip(options, found)]
    return TypeOffer(offered=tuple(option for option, reason
                                   in zip(options, reasons) if not reason),
                     refusals=tuple(reason for reason in reasons if reason))


def _refusal(option: TypeOption, facts: NodeFacts) -> str:
    """Return why the class would refuse one type, empty where it would not.

    A class of the application's own whose kind only the value can say is
    never refused by the dict-shape check, because nothing says it is or is
    not written as a dict, and no converter is asked about a type the editor
    cannot make a value of, because there is no value to ask about.
    """
    if facts.holds_dict is not None and option.kind is not None and \
            (option.kind is dict) != facts.holds_dict:
        return (DICT_ONLY if facts.holds_dict else NO_DICT_YET).format(
            type=option.text)
    if names_config(option):
        return _object_refusal(option=option, placed=facts.placed)
    if facts.converter is not None and \
            (option == NONE_TYPE or makes_value(option)) and \
            not _converts(option=option, converter=facts.converter,
                          omitted=facts.omitted):
        return NOT_CONVERTED_FORM.format(
            type=option.text, value=json.dumps(empty_option_value(option)))
    return ''


def _object_refusal(option: TypeOption, placed: Optional[bool]) -> str:
    """Return why a configuration class is not offered, empty where it is."""
    if placed is None:
        return NO_OBJECT_HERE.format(type=option.text)
    return '' if placed else NOT_MADE.format(type=option.text)


def _unmade(option: TypeOption, held: Optional[TypeOption],
            making: bool) -> str:
    """Return why a type the editor cannot make is left out, or nothing.

    It is left out where the node does not hold it and where something
    besides `None` is offered instead, which `making` says. Where nothing is,
    leaving it out would leave the node nothing but `None` to hold.
    """
    if not making or option in (held, NONE_TYPE) or makes_value(option):
        return ''
    return NOT_MADE.format(type=option.text)


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
