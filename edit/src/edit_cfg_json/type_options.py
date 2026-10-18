#! /usr/bin/env python3
"""The types a declaration allows one node to hold, spelled as Python does.

A declaration is read into a tuple of alternatives, one per type a union names:
a plain type is a union of one, and `Optional[X]` is the union of `X` and
`None` rather than a state of its own. Each alternative is spelled in the
vocabulary of Python type hints, because that is the vocabulary the users of
this editor already know, and it is spelled from the resolved hint rather than
copied from the source, so that a declaration read from source and one read
with `typing.get_type_hints` are spelled alike.

**What is made of a type is still deliberately little** (section 4.1 of
`doc/detailed_design.md`). An alternative says which kind of JSON value
belongs there, what is inside it where it is a list or a dict, which class it
names and which values a `Literal` allows. A class of the application's own
says no kind at all, because what kind of JSON value it is written as is said
by its converters and therefore read from the value; an enum is written as the
name of a member and a configuration class as a dict, which this module knows
without being told.

**A declaration names nothing usable** where any part of it is a type the
editor can make nothing of: `tuple`, `set`, `Any`, a `Literal` whose values are
of more than one kind, and every other generic. Such a declaration answers with
no alternatives at all, and the type of the node is then the one its value
has, exactly as for a member with no annotation.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Sequence
from enum import Enum
from types import NoneType, UnionType
from typing import Any, Literal, NamedTuple, Optional, TypeAliasType, Union, \
    get_args, get_origin
from config_as_json import Config, JsonType
from edit_cfg_json.leaf_value import VALUE_KINDS, empty_value, kind_of


class TypeOption(NamedTuple):
    """One type that the declaration of a node allows it to hold."""

    text: str
    """The type as a Python type hint spells it, such as `list[str]`."""

    kind: Optional[type] = None
    """Which kind of JSON value this type is written as.

    It is one of the types of `leaf_value.VALUE_KINDS`, `NoneType` for the
    `None` alternative, and None for a class of the application's own whose
    kind only the value can say.
    """

    inside: tuple['TypeOption', ...] = ()
    """The types one value inside this one may hold, where it is a container.

    It is the element of a list and the value of a dict, and it is empty where
    nothing usable says what that is.
    """

    of_class: Optional[type] = None
    """The class this type names, None for a type that names no class.

    An enum, a configuration class and every other class of the application
    are one; the built in types of JSON are not.
    """

    literals: tuple[str | int | bool, ...] = ()
    """The values a `Literal` allows, empty for every other type."""


NONE_TYPE = TypeOption(text='None', kind=NoneType)
"""The alternative that allows a node to hold no value at all."""

TYPE_COLUMN_LIMIT = 40
"""The most characters the column of the types gives one type.

A longer type is cut to this with `CUT_MARK` at its end, and the explanation
line below its row then says the whole of it, so nothing of a declaration is
lost to the width of a column.
"""

CUT_MARK = '…'
"""What ends a type that is cut to fit its column."""

UNION_ORIGINS = (Union, UnionType)
"""What `typing.get_origin` answers for a union, in every way it is spelled.

`typing.Union` and `types.UnionType` are two types before Python 3.14 and one
type from then on, so both are named and nothing depends on which it is.
"""


UNUSABLE_CLASSES: tuple[object, ...] = (tuple, set, frozenset, object, Any)
"""Plain classes that say nothing the editor can use.

`typing.Any` is among them because it is a class from Python 3.11 on, and
would otherwise be read as a class of the application's own.
"""

SCALAR_KINDS: tuple[type, ...] = (bool, int, float, str)
"""The kinds of JSON value that a field holds, rather than rows below it.

An enum and a `Literal` are written as one of them, so a type of either is a
plain value too. A list, a dict, a configuration object and a class whose kind
only its value can say are not.
"""


class _Unusable(Exception):
    """Raised where one part of a declaration names nothing usable."""


def type_options(hint: object) -> tuple[TypeOption, ...]:
    """Return the types one resolved annotation allows, in declared order.

    Args:
        hint: What one annotation means.

    Returns:
        One alternative per type the annotation allows, and none at all for an
        annotation of which any part names nothing usable.
    """
    try:
        return _alternatives(hint)
    except _Unusable:
        return ()


def _alternatives(hint: object) -> tuple[TypeOption, ...]:
    """Return the alternatives of one hint, raising for an unusable one."""
    if isinstance(hint, TypeAliasType):
        return _alternatives(hint.__value__)
    if get_origin(hint) in UNION_ORIGINS:
        return tuple(option for arg in get_args(hint)
                     for option in _alternatives(arg))
    return (_one_option(hint),)


def _one_option(hint: object) -> TypeOption:
    """Return the one type a hint that is not a union names."""
    if hint is None or hint is NoneType:
        return NONE_TYPE
    origin = get_origin(hint)
    if origin is Literal:
        return _literal_option(hint)
    if origin in (list, dict):
        return _container_option(hint)
    if origin is not None or not isinstance(hint, type):
        raise _Unusable()
    return _class_option(hint)


def _class_option(hint: type) -> TypeOption:
    """Return the type one plain class names, raising for an unusable one."""
    kind = next((kind for kind in VALUE_KINDS if hint is kind), None)
    if kind is not None:
        return TypeOption(text=spelled(hint), kind=kind)
    if hint in UNUSABLE_CLASSES:
        raise _Unusable()
    return TypeOption(text=spelled(hint), kind=_class_kind(hint),
                      of_class=hint)


def _class_kind(hint: type) -> Optional[type]:
    """Return the kind of JSON value a class of the application is written as.

    An enum is written as the name of one of its members and a configuration
    class as a dict, which is what `config_as_json` does with both. Every other
    class is written as whatever its converters make of it, which only the
    value can say.
    """
    if issubclass(hint, Enum):
        return str
    return dict if issubclass(hint, Config) else None


def _literal_option(hint: object) -> TypeOption:
    """Return the type a `Literal` names, raising where its kinds are mixed."""
    values = get_args(hint)
    kinds = {type(value) for value in values}
    if len(kinds) != 1 or kinds - {str, int, bool}:
        raise _Unusable()
    allowed = tuple(value for value in values
                    if isinstance(value, (str, int, bool)))
    return TypeOption(text=spelled(hint), kind=kinds.pop(), literals=allowed)


def _container_option(hint: object) -> TypeOption:
    """Return the type a list or a dict names.

    A container is usable whatever is inside it, because what a list or a dict
    is does not depend on what it holds. What is inside is spelled all the
    same, and where it names nothing usable the values inside answer for
    themselves as every node with no usable declaration does.
    """
    args = get_args(hint)
    inside = type_options(args[-1]) if args else ()
    return TypeOption(text=spelled(hint), kind=get_origin(hint), inside=inside)


def spelled(hint: object) -> str:
    """Return one hint as a Python type hint spells it, usable or not.

    It is what spells every type this module reads, and the inside of a
    container whatever that is, so that a member declared
    `list[tuple[int, int]]` says so even though the editor can make nothing of
    a tuple. A PEP 695 alias is spelled as what it stands for.

    Args:
        hint: What one annotation, or one part of it, means.

    Returns:
        That hint as text.
    """
    if isinstance(hint, TypeAliasType):
        return spelled(hint.__value__)
    origin = get_origin(hint)
    if origin is None:
        return _plain_text(hint)
    args = get_args(hint)
    if origin in UNION_ORIGINS:
        return ' | '.join(spelled(arg) for arg in args)
    if origin is Literal:
        return f"Literal[{', '.join(repr(arg) for arg in args)}]"
    inner = ', '.join(spelled(arg) for arg in args)
    return f'{spelled(origin)}[{inner}]' if args else spelled(origin)


def _plain_text(hint: object) -> str:
    """Return one hint that has no arguments as Python spells it."""
    if hint is None or hint is NoneType:
        return NONE_TYPE.text
    if hint is Ellipsis:
        return '...'
    name = getattr(hint, '__name__', None)
    return name if isinstance(name, str) else repr(hint)


def cut_type_text(text: str) -> str:
    """Return one type as the column of the types shows it.

    Args:
        text: The type as a Python type hint spells it.

    Returns:
        That text, cut to `TYPE_COLUMN_LIMIT` characters with `CUT_MARK` at
        its end where it is longer.
    """
    if len(text) <= TYPE_COLUMN_LIMIT:
        return text
    return text[:TYPE_COLUMN_LIMIT - len(CUT_MARK)] + CUT_MARK


def fits(option: TypeOption, value: JsonType) -> bool:
    """Return whether one value is a value of one type.

    A whole number is a number as well, because JSON has one kind of number
    and `config_as_json` reads `0` into a member declared `float`; true and
    false are not whole numbers, although Python says they are. A type whose
    values are a known set, an enum and a `Literal`, is fitted by those values
    alone: the name of a member of that enum, and one of those literals. A
    container fits where everything inside it fits one of the types inside it,
    which is
    what tells `[['x']]` from `['x']` where both `list[str]` and
    `list[list[str]]` are allowed.

    Args:
        option: The type asked about.
        value: The value asked about, in JSON space.

    Returns:
        Whether that value is one of that type.
    """
    if option.kind is None:
        return value is not None
    if not _kind_fits(kind=option.kind, value=value):
        return False
    allowed = allowed_values(option)
    if allowed:
        return value in allowed
    held = list(value.values()) if isinstance(value, dict) else \
        value if isinstance(value, list) else []
    return not option.inside or all(
        any(fits(inner, one) for inner in option.inside) for one in held)


def _kind_fits(kind: type, value: JsonType) -> bool:
    """Return whether one value is of one kind of JSON value."""
    found = kind_of(value)
    return found is kind or (kind is NoneType and found is None) or \
        (kind is float and found is int)


def held_option(options: Sequence[TypeOption],
                value: JsonType) -> Optional[TypeOption]:
    """Return the one of some types that a value holds.

    It is the first one the value fits, in the order the declaration writes
    them, so `5` holds `int` where the declaration is `int | float` and
    `float` where it is `float | int`. A value that fits none of them — a text
    half typed into a number member, or what a file held that its class never
    checked — holds the first alternative that is not `None`, which is what
    its text is read by.

    Args:
        options: The types allowed.
        value: The value held, in JSON space.

    Returns:
        The type that value holds, and None where no type is allowed at all.
    """
    found = next((option for option in options if fits(option, value)), None)
    if found is not None:
        return found
    return value_option(options) or next(iter(options), None)


def kept_choice(options: Sequence[TypeOption], value: JsonType,
                chosen: Optional[TypeOption],
                refreshing: bool) -> Optional[TypeOption]:
    """Return the type one node holds once its rows have been built again.

    Args:
        options: The types the user may choose between for that node.
        value: The value it holds now.
        chosen: The type it held before, None for a node that had none.
        refreshing: Whether the rows are what a validation pass left behind,
            which is the one change that gives the value a say again.

    Returns:
        The type it held, where it still may and the value has no say, the
        first type its value fits otherwise, and None where no type is
        allowed at all.
    """
    if chosen is not None and chosen in options and \
            (not refreshing or fits(chosen, value)):
        return chosen
    return held_option(options, value)


def node_options(options: Sequence[TypeOption],
                 is_object: bool) -> tuple[TypeOption, ...]:
    """Return the types one node can be holding, as the tree has it.

    Whether a configuration object is at a node is said by the tree and not
    by the value, because an object is written as a dict and so is a dict:
    `{"cpu": 2}` fits `StageConfig` as well as `dict[str, int]`. So a node
    where an object is holds one of the configuration classes it allows, and
    every other node holds one of the other types. `None` is either.

    Args:
        options: The types the declaration of that node allows.
        is_object: Whether the tree has a configuration object declared
            there, holding one or not.

    Returns:
        Those of the types that node can be holding.
    """
    return tuple(option for option in options if option == NONE_TYPE
                 or names_config(option) == is_object)


def names_config(option: TypeOption) -> bool:
    """Return whether one type is a configuration class.

    Args:
        option: The type asked about.

    Returns:
        Whether it names a subclass of `Config`.
    """
    return option.of_class is not None and issubclass(option.of_class, Config)


def value_option(options: Sequence[TypeOption]) -> Optional[TypeOption]:
    """Return the first of some types that is a value rather than `None`.

    Args:
        options: The types allowed, in the order the declaration writes them.

    Returns:
        The first of them that is not `None`, and None where there is none.
    """
    return next((option for option in options if option != NONE_TYPE), None)


def inferred_option(value: JsonType) -> TypeOption:
    """Return the type that a value says it is, where nothing else says.

    Args:
        value: The value a node held when the file was last agreed with.

    Returns:
        The kind of that value as a type, and `None` for no value at all.
    """
    kind = kind_of(value)
    return NONE_TYPE if kind is None else TypeOption(text=kind.__name__,
                                                     kind=kind)


def reading_kind(options: Sequence[TypeOption],
                 original: JsonType) -> Optional[type]:
    """Return the kind of value that the text of one node is read as.

    It is asked of the value the node held when the file was last agreed with
    and never of the value it holds now, because a number member whose text
    is half typed holds text, and reading the next key by that would make it a
    text member for good (section 4.2 of `doc/detailed_design.md`). `None` is
    never the answer while another type is allowed, because a node holding
    nothing is not typed into, and the text of one that has just been given a
    value is a text of that value. A class whose kind only the value can say
    is read by what the value says.

    Args:
        options: The types the declaration of that node allows.
        original: Value that the node held when the file was last agreed with.

    Returns:
        The kind of value that text is read as, None where nothing says.
    """
    held = held_option([option for option in options
                        if option != NONE_TYPE], original)
    if held is None or held.kind is None:
        return kind_of(original)
    return held.kind


def allowed_values(option: TypeOption) -> tuple[str | int | bool, ...]:
    """Return the values one type allows, where they are a known set.

    Args:
        option: The type asked about.

    Returns:
        The values a `Literal` allows, the names of the members of an enum in
        the order the enum declares them, which is how `config_as_json` writes
        one, and nothing for every other type.
    """
    if option.literals:
        return option.literals
    if option.of_class is not None and issubclass(option.of_class, Enum):
        return tuple(option.of_class.__members__)
    return ()


def empty_option_value(option: TypeOption) -> Optional[JsonType]:
    """Return the value of one type that says no more than its type.

    Args:
        option: Type to make a value of.

    Returns:
        That value for a type of JSON the editor can make one of, the first of
        the values of a type whose values are a known set, and None for every
        other type: a class of the application's own is a type the editor
        cannot make a value of on its own, and so is an enum with no members.
    """
    allowed = allowed_values(option)
    if allowed:
        return allowed[0]
    if option.of_class is not None:
        return None
    return empty_value(option.kind)


def makes_value(option: TypeOption) -> bool:
    """Return whether the editor can make a value of one type on its own.

    It can of a plain value, a list, a dict, an enum with members and a
    `Literal`, whose empty value `empty_option_value` gives, and of a
    configuration class, whose object is constructed where a declaration
    names that class (`type_choice.offered_types` leaves the class out where
    it cannot be). It cannot of a class of the application's own whose kind
    only its value can say, nor of `None`, which is no value at all.

    Args:
        option: The type asked about.

    Returns:
        Whether choosing that type can give a node a value of it.
    """
    return names_config(option) or empty_option_value(option) is not None


def choosable(options: Sequence[TypeOption]) -> bool:
    """Return whether the user may choose which of some types a node holds.

    They may where there is more than one type to choose from and the editor
    can make a value of at least one of them besides `None`, which is what
    `int | str`, `float | None`, `Colors | None`, `list[str] | None`,
    `list[str] | list[list[str]]` and `StageConfig | None` are. A choice of
    the user's between them is a value of the other type in the same field, a
    container of the other type with rows of its own below it, an object with
    the members of its class below it, or no value at all.

    A type the editor cannot make a value of is offered only where the node
    holds it or where nothing else could be chosen instead, as
    `type_choice.offered_types` says. So choosing never gives a node a type
    it cannot be given a value of, and `Path | None`, where nothing else
    could, is not a choice at all: such a member is a field, as it always was.

    Args:
        options: The types a node may hold.

    Returns:
        Whether the type that node holds is the user's to choose.
    """
    return len(options) > 1 and any(makes_value(option) for option in options)
