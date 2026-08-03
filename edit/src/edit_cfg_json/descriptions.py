#! /usr/bin/env python3
"""The explanatory text that the editor shows about a configuration.

There are two sources of it, they are independent, and both of them are
optional. The docstring of the configuration class labels the configuration
object, and a mapping supplied by the application labels the individual
members.

It takes two sources because only one of them exists. A class has a
docstring and every reader of the code can see it, while a member has
nothing of the kind at runtime: a string literal written after an assignment
is discarded by the compiler, and a PEP 526 annotation on an instance
attribute is recorded nowhere at all. So the members are described by the
application in a mapping, and the editor invents nothing.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Mapping
import inspect
from config_as_json import Config, ConfigPath

EVERY_ELEMENT = '['
"""The path step that means every list element or dictionary value here.

It is the step that `config_as_json` gives this meaning to, and it keeps it
here, which is what stops an application from having to repeat one
description once per list index or once per dictionary key.
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


def class_docstring(config_type: type[Config]) -> str:
    """Return the whole docstring of one configuration class, or nothing.

    `config_type.__doc__` and deliberately not `inspect.getdoc()`, which
    inherits from the base classes: a configuration class without a docstring
    of its own would then be labelled with the docstring of `Config`, and a
    label that describes the library rather than the configuration is worse
    than no label at all.

    Args:
        config_type: Class of the configuration that is being described.

    Returns:
        The docstring of that class as `inspect.cleandoc` leaves it, and an
        empty text when the class has none of its own.
    """
    docstring = config_type.__doc__
    return inspect.cleandoc(docstring) if docstring else ''


def class_summary(config_type: type[Config]) -> str:
    """Return the first paragraph of the docstring, as a single line.

    The first paragraph is the summary a docstring is written to begin with,
    and one line is what a label of one row can show. The line breaks inside
    that paragraph belong to the width of a source file and not to the text,
    so they are not kept.

    Args:
        config_type: Class of the configuration that is being described.

    Returns:
        The summary of that class, and an empty text when it has no docstring.
    """
    first = class_docstring(config_type).split('\n\n', maxsplit=1)[0]
    return ' '.join(first.split())
