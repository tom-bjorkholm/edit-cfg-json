#! /usr/bin/env python3
"""The explanatory text that the editor shows about a configuration.

There are three sources of it, they are independent, and all of them are
optional. The docstring of a configuration class labels the configuration
object — the one being edited, and every nested one inside it, because each of
those is an object with a class of its own. A mapping supplied by the
application labels the individual members, and the type of a member says the
rest.

What a type says is the names of an enum where the member holds one, and what
kind of value the member holds where it does not: text, a whole number, a
number, or true or false. That last one is the least the editor can say about
any member and it is never nothing, which is what a review of step 9 asked for:
a program that is told a class and no mapping showed the members with nothing
under them at all, and the editor does know something about each of them.

It takes a mapping for the members because a member has no docstring at
runtime. A class has one and every reader of the code can see it, while a
string literal written after an assignment is discarded by the compiler and a
PEP 526 annotation on an instance attribute is recorded nowhere at all. So the
members are described by the application in a mapping, and the editor invents
nothing: what it adds to that mapping is read from the enum class of the
member, which is a fact about the type and not a constraint read out of a
validator.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Mapping
from enum import Enum
from typing import NamedTuple, Optional
import inspect
from config_as_json import Config, ConfigPath, JsonType, ParseConverter
from edit_cfg_json.leaf_value import value_kind
from edit_cfg_json.tree import ConfigNode, EVERY_ELEMENT, selects

CHOICES_FORM = 'One of: {names}.'
"""What the editor says about the names one enum member accepts."""

OPTIONAL_TEXT = 'It may be left out of the file.'
"""What the editor says about a member that the class treats as optional.

`_omit_none_from_json()` is what says which members those are, and section 4.1
of `doc/design.md` names it as one of the sources of the structure. It is a
protected name of `config_as_json` and it is read anyway, because nothing else
answers the question and the answer is worth having: a member that may be left
out is a member a user may leave empty.
"""


type Descriptions = Mapping[ConfigPath, str]
"""What the application says about the individual members it declares.

A member is named by the absolute `config_as_json.ConfigPath` that addresses
it, so that a member inside a list, a dict or a nested configuration object
needs no second way of naming it. A path is a tuple of strings and is
hashable, which is what makes this a mapping rather than a list of pairs.

The `'['` step keeps its `config_as_json` meaning of every list element or
every dictionary value at that point, and two selectors that both address one
member are resolved in favour of the more specific one rather than refused.

Paths cross the boundary of a nested configuration object, which is the one
place where these paths differ from the paths of `serialize_converters()`.
Converters stop at a child owned subtree because each nested object
serializes itself; an application explaining its own members should not have
to know where its nesting boundaries fall.
"""


def _named_steps(selector: ConfigPath) -> tuple[bool, ...]:
    """Return which steps of one selector name a step rather than all of them.

    This is how two selectors that both address one member are compared, and
    the more specific of them is the greater: a step that names one key is
    more specific than the step that means every element, and an earlier step
    decides before a later one. Two different selectors can never compare
    equal here, because two selectors with the same pattern of named steps
    that both address one member are the same selector.

    Args:
        selector: One key of the description mapping.

    Returns:
        One value per step, saying whether that step names a single step.
    """
    return tuple(step != EVERY_ELEMENT for step in selector)


def path_description(descriptions: Descriptions, path: ConfigPath) -> str:
    """Return what the application says about one member, or nothing.

    A selector that addresses no member of this configuration is simply never
    used, and is not an error: a wrong description is a cosmetic mistake, and
    refusing to open the editor over one would be a much larger one.

    Args:
        descriptions: What the application says about its members.
        path: Path of the member that is being described.

    Returns:
        The description of that member, and an empty text when the
        application said nothing about it.
    """
    selectors = [selector for selector in descriptions
                 if selects(selector=selector, path=path)]
    if not selectors:
        return ''
    return descriptions[max(selectors, key=_named_steps)]


def class_docstring(described: type[object]) -> str:
    """Return the whole docstring of one class, or nothing.

    `described.__doc__` and deliberately not `inspect.getdoc()`, which
    inherits from the base classes: a configuration class without a docstring
    of its own would then be labelled with the docstring of `Config`, and a
    label that describes the library rather than the configuration is worse
    than no label at all. The same holds for the enum class of a member,
    which would otherwise be described as an enumeration.

    Args:
        described: Class that is being described, which is the class of the
            configuration or the enum class of one of its members.

    Returns:
        The docstring of that class as `inspect.cleandoc` leaves it, and an
        empty text when the class has none of its own.
    """
    docstring = described.__doc__
    return inspect.cleandoc(docstring) if docstring else ''


def class_summary(described: type[object]) -> str:
    """Return the first paragraph of the docstring, as a single line.

    The first paragraph is the summary a docstring is written to begin with,
    and one line is what a label of one row can show. The line breaks inside
    that paragraph belong to the width of a source file and not to the text,
    so they are not kept.

    Args:
        described: Class that is being described.

    Returns:
        The summary of that class, and an empty text when it has no docstring.
    """
    first = class_docstring(described).split('\n\n', maxsplit=1)[0]
    return ' '.join(first.split())


def _enum_type(converter: Optional[ParseConverter]) -> Optional[type[Enum]]:
    """Return the enum class one member holds, or None when it holds none.

    Args:
        converter: How the text of this member becomes a value, or None.

    Returns:
        The enum class of that member, or None for every other member.
    """
    if converter is None or not issubclass(converter.result_type, Enum):
        return None
    return converter.result_type


def enum_text(converter: Optional[ParseConverter]) -> str:
    """Return what the type of one member says about it, or nothing.

    `parse_converters()` is what says that a member holds an enum, because it
    is what turns the name in the file back into a member of that enum. The
    enum class then says the rest itself: the summary of its own docstring,
    when it has one, and the names it accepts.

    Reading the names an enum has is not the reading of a validator that this
    library has decided never to do. It is the type of the member, it is as
    true as the name of the member itself, and it is the same kind of reading
    as the docstring of the configuration class.

    The summary of that docstring and not the whole of it, which is the one
    place where a class here is treated differently from the class of the
    configuration. The reason is what the rest of an enum docstring usually
    is: notes for whoever writes the application, about how the members are
    numbered or how they reach the file, which is not what somebody choosing
    between them needs. What they need is the first line and the names.

    Args:
        converter: How the text of this member becomes a value, or None for a
            member that holds what the file holds.

    Returns:
        What that enum class says about itself and which names it accepts,
        and an empty text for a member that holds no enum.
    """
    enum_type = _enum_type(converter)
    if enum_type is None:
        return ''
    names = CHOICES_FORM.format(names=', '.join(enum_type.__members__))
    return '\n'.join(line for line in [class_summary(enum_type), names]
                     if line)


def optional_members(config: Config) -> frozenset[str]:
    """Return the members that this configuration may leave out of a file.

    The class is asked, because only the class knows: a member that holds
    nothing right now may be one that has to hold something, and one that holds
    something may still be allowed to hold nothing. What it is asked is a
    protected method, for the reason `OPTIONAL_TEXT` gives, and the answer
    needs no checking here, because constructing the object checked it.

    Args:
        config: Configuration object being edited. It is not modified.

    Returns:
        The names of the members that are genuinely optional.
    """
    # pylint: disable-next=protected-access
    return frozenset(config._omit_none_from_json())


def optional_paths(nodes: Mapping[ConfigPath, ConfigNode]) \
        -> frozenset[ConfigPath]:
    """Return every member of one tree that its own class may leave out.

    A nested configuration object writes its own JSON, so which of its members
    it may leave out of that JSON is its class's to say and not the class's
    above it. The paths are absolute, so a member is looked up here by the same
    path that addresses it everywhere else.

    Args:
        nodes: Every configuration object of the tree, by its path.

    Returns:
        The path of every member that the object holding it may omit.
    """
    return frozenset(path + (name,) for path, node in nodes.items()
                     if node.config is not None
                     for name in optional_members(node.config))


class MemberFacts(NamedTuple):
    """What the editor knows about the type of one node of the tree.

    It is one object rather than one argument each, because the four of them
    are read together and answer one question between them: what can be said
    about this node that the application did not say.
    """

    value: JsonType
    """Value the node held when the file was last agreed with.

    It is the only type information there is for an ordinary value, because a
    PEP 526 annotation on an instance attribute is recorded nowhere at runtime.
    """

    converter: Optional[ParseConverter] = None
    """How the text of this node becomes the value it holds, or None."""

    optional: bool = False
    """Whether the class that owns this node may leave it out of the file."""

    nested: bool = False
    """Whether this node is a declared nested configuration object.

    Such a node holds no value of its own, so what kind of value it is cannot
    be said about it. What is said about it instead is the docstring of its
    class, and where that is said depends on whether the node is open, which
    is why it is not said here.
    """


def type_text(facts: MemberFacts) -> str:
    """Return everything the type of one node says about it.

    An enum says the most, so where a node holds one that is what is said and
    the kind of the value would only repeat it: the name of an enum member is
    text, and knowing that is worth nothing beside knowing which names there
    are. Every other value says what kind of value it is, which is the one
    thing the editor knows about every member of every configuration.

    A declared nested configuration object says neither, because it holds no
    value: it says its class, which its row shows, and its docstring, which is
    shown below it. What it can still say here is that the class above it may
    leave it out of the file altogether.

    Args:
        facts: What the editor knows about the type of that node.

    Returns:
        What the type of that node says, and an empty text when it says
        nothing at all.
    """
    said = '' if facts.nested else \
        (enum_text(facts.converter) or value_kind(facts.value))
    if not facts.optional:
        return said
    return f'{said} {OPTIONAL_TEXT}'.strip()


def member_description(descriptions: Descriptions, path: ConfigPath,
                       facts: MemberFacts) -> str:
    """Return everything the editor has to say about one node.

    What the application says comes first, because it is what this node is
    for in this application, and what the type of the node says comes after
    it. The second is appended rather than used only where the first is
    missing: what a node holds is true whatever the application wrote, and an
    application that explains what its members mean should not have to list the
    names of an enum or say that a number is a number.

    Args:
        descriptions: What the application says about its members.
        path: Path of the node that is being described.
        facts: What the editor knows about the type of that node.

    Returns:
        The description of that node, which is never empty for a node the
        editor can edit, because the type of it always says something.
    """
    said = [path_description(descriptions=descriptions, path=path),
            type_text(facts)]
    return '\n'.join(line for line in said if line)
