#! /usr/bin/env python3
"""The explanatory text that the editor shows about a configuration.

There are three sources of it, they are independent, and all of them are
optional. The docstring of the configuration class labels the configuration
object, a mapping supplied by the application labels the individual members,
and the type of a member says the rest where the member has a type that says
anything, which today means an enum.

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
from typing import Optional
import inspect
from config_as_json import ConfigPath, ParseConverter

EVERY_ELEMENT = '['
"""The path step that means every list element or dictionary value here.

It is the step that `config_as_json` gives this meaning to, and it keeps it
here, which is what stops an application from having to repeat one
description once per list index or once per dictionary key.
"""

CHOICES_FORM = 'One of: {names}.'
"""What the editor says about the names one enum member accepts."""


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


def _selects(selector: ConfigPath, path: ConfigPath) -> bool:
    """Return whether one selector of the mapping addresses one member.

    Args:
        selector: One key of the description mapping.
        path: Path of the member that is being described.

    Returns:
        Whether that selector is about that member.
    """
    return len(selector) == len(path) and \
        all(step in (EVERY_ELEMENT, named)
            for step, named in zip(selector, path))


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
                 if _selects(selector=selector, path=path)]
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


def member_description(descriptions: Descriptions, path: ConfigPath,
                       converter: Optional[ParseConverter]) -> str:
    """Return everything the editor has to say about one member.

    What the application says comes first, because it is what this member is
    for in this application, and what the type of the member says comes after
    it. The second is appended rather than used only where the first is
    missing: the names an enum accepts are true whatever the application
    wrote, and an application that explains what its members mean should not
    have to list the names as well.

    Args:
        descriptions: What the application says about its members.
        path: Path of the member that is being described.
        converter: How the text of this member becomes a value, or None.

    Returns:
        The description of that member, and an empty text when neither the
        application nor the type of the member says anything about it.
    """
    said = [path_description(descriptions=descriptions, path=path),
            enum_text(converter)]
    return '\n'.join(line for line in said if line)
