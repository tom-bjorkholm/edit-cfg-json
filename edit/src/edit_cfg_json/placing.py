#! /usr/bin/env python3
"""Where a configuration object that a class declared is held, and putting one.

Adding an element, removing one and choosing the type of a place are changes of
the edit buffer, and each of them is more where the class of a configuration
declares that something is a configuration object: the object of the session
gains one or loses one with the values. The tree finds those objects by walking
the real objects rather than by matching a declaration, so an element that
existed only in the buffer would be shown as the dictionary it serializes to,
with the member order of nobody, the parse converters of nobody and no badge of
its own.

The object that changes is the model's own copy, which the caller never sees,
so principle 5 of section 3 of `doc/detailed_design.md` is untouched.

**A declaration names a place and not always a member.** `LIST_ELEMENT` and
`DICT_VALUE` say that everything inside one member is an object, `MEMBER` and
`OPTIONAL_MEMBER` say that the member itself is one, and `DICT_VALUE_BY_KEY`
names one key of a dict, leaving every other key of it an ordinary value. So
where an object goes is asked as a path, and `ObjectPlace` is what the answer
is: the object that declared it, what was declared, the member holding it and
the key inside that member where there is one.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import NamedTuple, Optional, TextIO
from config_as_json import Config, ConfigNesting, ConfigNestingKind, \
    ConfigPath, JsonType
from edit_cfg_json.constructing import built_config
from edit_cfg_json.tree import by_key_nestings, config_nodes, \
    member_nestings, member_values, owner_path

OBJECT_KINDS = (ConfigNestingKind.LIST_ELEMENT, ConfigNestingKind.DICT_VALUE)
"""The declarations that say every value inside one member is an object.

They are what makes a member of that shape extendable at all, and they are the
two that a new element is made from the declared class for. The other three
declarations are about the member itself, or about one key of it, rather than
about everything inside it.
"""


class ObjectPlace(NamedTuple):
    """Where one configuration object that a class declared is held."""

    holder: Config
    """The object whose class declared it."""

    nesting: ConfigNesting
    """What that class declared about the place."""

    member: str
    """Name of the member of that object which holds it."""

    key: str
    """Key of the dict that holds it, empty for the member itself.

    It is what tells the two things a `DICT_VALUE_BY_KEY` declaration is about
    apart: the member, which is a dict of ordinary values with named objects
    in it, and one of those named keys.
    """


def new_object(nesting: ConfigNesting, stream: TextIO) -> Config:
    """Return one new configuration object of a declared class.

    The factory the declaration names is asked where it named one, exactly as
    `config_as_json` asks it while it reads a file, so an application that
    answers with a subclass answers with it here too.

    Args:
        nesting: What the class declared about the member that holds these.
        stream: Stream that collects what the construction says.

    Returns:
        One object of that class, holding the values it declares.

    Raises:
        TypeError: The class cannot be constructed this way.
        ValueError: The declared values are ones the class refuses.
        AttributeError: The class declares no public member at all.
    """
    factory = nesting.factory_function or nesting.config_type
    return built_config(factory, stream=stream)


def object_added(config: Config, path: ConfigPath, key: str,
                 stream: TextIO) -> None:
    """Put a new configuration object where one has just been added.

    Nothing happens where the member holds no configuration objects, because
    there is then nothing about it that the object of the session says: what a
    list of numbers holds is what the buffer holds, and the tree asks the
    object only about the objects inside it.

    Args:
        config: Configuration object of the session, which this modifies. It
            is the editor's own copy and never the caller's.
        path: Path of the member that has gained an element.
        key: Name of the new entry of a dict, empty for a list.
        stream: Stream that collects what the construction says.

    Raises:
        TypeError: The declared class cannot be constructed this way.
        ValueError: Its declared values are ones it refuses.
        AttributeError: It declares no public member at all.
    """
    place = _declared_at(config=config, path=path)
    if place is None or _no_object_at(place):
        return
    _put_object(place=place, key=key,
                made=new_object(nesting=place.nesting, stream=stream))


def _no_object_at(place: ObjectPlace) -> bool:
    """Return whether a new entry of one declared place holds no object.

    A key that a `DICT_VALUE_BY_KEY` member does not declare holds an ordinary
    value, and `_validate_dict_by_key` is what refuses an object at one, so a
    new entry of such a member is the buffer's alone. A declared key is given
    its object by `object_switched` instead.
    """
    return not place.key and \
        place.nesting.kind is ConfigNestingKind.DICT_VALUE_BY_KEY


def _put_object(place: ObjectPlace, key: str, made: Config) -> None:
    """Put one new configuration object where its declaration holds it."""
    if place.key:
        getattr(place.holder, place.member)[place.key] = made
    elif place.nesting.kind is ConfigNestingKind.LIST_ELEMENT:
        getattr(place.holder, place.member).append(made)
    elif place.nesting.kind is ConfigNestingKind.DICT_VALUE:
        getattr(place.holder, place.member)[key] = made
    else:
        setattr(place.holder, place.member, made)


def object_switched(config: Config, path: ConfigPath, made: bool,
                    stream: TextIO) -> JsonType:
    """Give one declared place an object of its class, or take it away.

    It is what choosing the type of a place does: an `OPTIONAL_MEMBER` and a
    key that `DICT_VALUE_BY_KEY` names hold one object of the class declared
    for them or hold nothing, and choosing between the two is choosing between
    that class and `None` (section 4.12 of `doc/detailed_design.md`).

    Args:
        config: Configuration object of the session, which this modifies. It
            is the editor's own copy and never the caller's.
        path: Path of the declared place.
        made: Whether the place is to hold a new object rather than none.
        stream: Stream that collects what the construction says.

    Returns:
        What the place holds now, in JSON space: the values of the new object,
        or None where it holds none.

    Raises:
        TypeError: The declared class cannot be constructed this way.
        ValueError: Its declared values are ones it refuses.
        AttributeError: It declares no public member at all.
    """
    place = _declared_at(config=config, path=path)
    assert place is not None
    if not made:
        _take_object(place)
        return None
    built = new_object(nesting=place.nesting, stream=stream)
    _put_object(place=place, key='', made=built)
    return member_values(config=built, stderr_file=stream)


def object_removed(config: Config, path: ConfigPath) -> None:
    """Take the configuration object of a removed element out of the tree.

    Args:
        config: Configuration object of the session, which this modifies. It
            is the editor's own copy and never the caller's.
        path: Path of the element that has been removed.
    """
    place = _declared_at(config=config, path=path[:-1])
    if place is None or place.key or place.nesting.kind not in OBJECT_KINDS:
        return
    held = getattr(place.holder, place.member)
    del held[int(path[-1]) if isinstance(held, list) else path[-1]]


def _take_object(place: ObjectPlace) -> None:
    """Put one declared place back to holding no configuration object.

    A member holds nothing by being `None` and a declared key of a dict by not
    being there, which is the difference between the two ways a class writes a
    place that need not hold an object.
    """
    if place.key:
        del getattr(place.holder, place.member)[place.key]
        return
    setattr(place.holder, place.member, None)


def object_moved(config: Config, path: ConfigPath, later: bool) -> None:
    """Move the configuration object of a moved element with its values.

    Args:
        config: Configuration object of the session, which this modifies. It
            is the editor's own copy and never the caller's.
        path: Path of the element that has been moved.
        later: Whether it changed places with the one after it.
    """
    place = _declared_at(config=config, path=path[:-1])
    if place is None or \
            place.nesting.kind is not ConfigNestingKind.LIST_ELEMENT:
        return
    held = getattr(place.holder, place.member)
    index = int(path[-1])
    other = index + 1 if later else index - 1
    held[index], held[other] = held[other], held[index]


def _declared_at(config: Config, path: ConfigPath) -> Optional[ObjectPlace]:
    """Return where one declared place is held, and what declares it.

    A member that a class declared an object for and a key of a dict that a
    class declared one at are asked for the same way, and they cannot be the
    same node: a member is one step below the object that declares it and a
    named key is two.

    Args:
        config: Configuration object of the session. It is not modified here.
        path: Path to ask about, which is a declared place of one of the
            objects of the tree or something else entirely.

    Returns:
        Where that place is and what declared it, and None for a path that is
        no declared place of this configuration.
    """
    nodes = config_nodes(config)
    named = by_key_nestings(nodes)
    nesting = member_nestings(nodes).get(path) or named.get(path)
    if nesting is None:
        return None
    holder = nodes[owner_path(path=path, nodes=nodes)].config
    assert holder is not None
    return ObjectPlace(holder=holder, nesting=nesting,
                       member=path[-2] if path in named else path[-1],
                       key=path[-1] if path in named else '')
