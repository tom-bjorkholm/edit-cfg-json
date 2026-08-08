#! /usr/bin/env python3
"""The shape of the JSON structure that one configuration owns.

A configuration member is not always a value. It may be a list or a dict, and
what is inside it may be a list or a dict again, so what the editor shows is a
tree and not a row per member. This module owns the two operations that make
that tree, and they are inverses of each other: taking the values of one
configuration apart into one entry per node, and putting the edit buffer back
together into the values of one configuration.

Every node is addressed by a `config_as_json.ConfigPath`, which is what
section 4.2 of `doc/design.md` asks for: a member inside a list or a dict needs
no second way of naming it, and the description mapping already names one that
way. A list element is addressed by its index written out, which is what makes
`('retry_delays', '0')` a path and lets `('retry_delays', '[')` describe every
element of it.

**A declared nested configuration object is not taken apart here.** It
serializes as a dict and it is not one: it has a class, a docstring and a
validity state of its own, and step 11 of the delivery plan is what gives it
those. Until then it is one node holding what it serializes to, which is the
honest thing to show and is what keeps step 11 an addition rather than a
correction.

**Which nodes those are is asked as a path and not as a member name**, because
a member holding one nested object is the least interesting case. A real
configuration has a list of nested objects, each of which holds a dict of more
of them, and `ConfigNestingKind` says so: `LIST_ELEMENT` and `DICT_VALUE`
declare that every value *inside* a member is one. So a nesting declaration
becomes a selector over paths, written the way `config_as_json` writes one,
with `'['` for every element or every value at that point. The member that
holds them stays an ordinary container that can be folded and says how much it
holds, and each of the objects inside it is one node. What the later steps add
is what such a node *is*; how it is found is settled here.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Collection, Iterable, Iterator, \
    Mapping, Sequence
from config_as_json import Config, ConfigNesting, ConfigNestingKind, \
    ConfigPath, JsonType

EVERY_ELEMENT = '['
"""The path step that means every list element or dictionary value here.

It is the step that `config_as_json` gives this meaning to, in the paths of its
write-side converters and of its child-owned subtrees, and it keeps it here: it
is what one description reaches every element of a list with, and what one
nesting declaration says every element of a list is a configuration object
with.
"""

PATH_SEPARATOR = '.'
"""What separates the steps of a path where a path is written as text.

A path is a tuple everywhere inside the editor. It becomes text where a person
has to read it or type it, which is the line that names the members a
validation pass refused and the command line of the example programs.
"""

ELEMENTS_FORM = '{count} elements'
"""What is said about a list, in place of the value a leaf shows."""

ELEMENT_FORM = '{count} element'
"""The same for the one list that holds a single element."""

ENTRIES_FORM = '{count} entries'
"""What is said about a dict, in place of the value a leaf shows."""

ENTRY_FORM = '{count} entry'
"""The same for the one dict that holds a single entry."""

OPEN_AT_MOST = 8
"""How many rows a container may add before it starts folded.

A configuration is shown with everything the application put in it, for the
same reason the explanations start shown: what was written was written to be
read. A list of two hundred elements is the case where that stops being true,
because it fills the window before the user has seen the members below it.

It counts every row the container would add and not only its direct children,
because that is what fills the window: a list of three dicts of five entries
each is eighteen rows and not three.
"""


def path_text(path: ConfigPath) -> str:
    """Return one path as the text that a person reads and types.

    Args:
        path: Path that addresses one node of the tree.

    Returns:
        The steps of that path, separated by dots.
    """
    return PATH_SEPARATOR.join(path)


def text_path(text: str) -> ConfigPath:
    """Return the path that one piece of text addresses.

    This is the inverse of `path_text`, and it is why a dictionary key that
    holds a dot cannot be addressed as text. Such a key is edited in the
    editor like any other; it is only the writing of its path that this
    cannot express.

    Args:
        text: Path written with a dot between its steps.

    Returns:
        The path that text stands for.
    """
    return tuple(text.split(PATH_SEPARATOR))


def is_container(value: JsonType) -> bool:
    """Return whether one value holds other values rather than being one.

    Args:
        value: One value in JSON space.

    Returns:
        Whether that value is a list or a dict.
    """
    return isinstance(value, (dict, list))


def container_text(value: JsonType) -> str:
    """Return what one container says in the place where a value is shown.

    How many values it holds and nothing else. What they are is on the rows
    below it, and a container that showed them again would be showing the
    same thing twice — once in a form that a narrow window cuts off.

    Args:
        value: Value of a list or a dict node.

    Returns:
        How much that container holds.
    """
    count = len(value) if isinstance(value, (dict, list)) else 0
    if isinstance(value, list):
        return (ELEMENT_FORM if count == 1 else ELEMENTS_FORM) \
            .format(count=count)
    return (ENTRY_FORM if count == 1 else ENTRIES_FORM).format(count=count)


def rows_below(path: ConfigPath, paths: Iterable[ConfigPath]) -> int:
    """Return how many rows one container would add if it were opened.

    Everything below it and not only its direct children, because that is
    what fills the window. It is counted from the rows there are and not from
    the value, because a declared configuration object inside it is one row
    however much it holds.

    Args:
        path: Path of the container.
        paths: The path of every node of the configuration.

    Returns:
        The number of rows below that node.
    """
    return sum(1 for other in paths
               if len(other) > len(path) and other[:len(path)] == path)


def starts_folded(path: ConfigPath, paths: Iterable[ConfigPath]) -> bool:
    """Return whether one container is folded when the editor opens.

    Args:
        path: Path of the container.
        paths: The path of every node of the configuration.

    Returns:
        Whether opening it would add more rows than `OPEN_AT_MOST`.
    """
    return rows_below(path=path, paths=paths) > OPEN_AT_MOST


def child_values(path: ConfigPath,
                 value: JsonType) -> list[tuple[ConfigPath, JsonType]]:
    """Return the nodes that are directly inside one container.

    Args:
        path: Path of the container.
        value: Value of the container.

    Returns:
        The path and the value of each of its children, in the order the
        container holds them, and nothing at all for a value that holds none.
    """
    if isinstance(value, dict):
        return [(path + (key,), held) for key, held in value.items()]
    if isinstance(value, list):
        return [(path + (str(index),), held)
                for index, held in enumerate(value)]
    return []


def _walked(path: ConfigPath, value: JsonType, nested: Collection[ConfigPath]
            ) -> Iterator[tuple[ConfigPath, JsonType]]:
    """Yield one container and everything below it, the container first.

    The container comes before what is inside it, which is the order the rows
    are read in and the order they are shown in. A declared configuration
    object is yielded and not walked into, whatever it holds.
    """
    yield path, value
    if is_nested(path=path, nested=nested):
        return
    for child, held in child_values(path=path, value=value):
        yield from _walked(path=child, value=held, nested=nested)


def selects(selector: ConfigPath, path: ConfigPath) -> bool:
    """Return whether one selector addresses one node.

    A selector is a path whose steps are either the name of one step or
    `EVERY_ELEMENT`, which stands for every element of a list and every value
    of a dict at that point. It is what a description of the application is
    written with and what a nesting declaration becomes.

    Args:
        selector: Selector to apply.
        path: Path of the node it is applied to.

    Returns:
        Whether that selector is about that node.
    """
    return len(selector) == len(path) and \
        all(step in (EVERY_ELEMENT, named)
            for step, named in zip(selector, path))


def _nesting_selector(name: str, nesting: ConfigNesting) -> ConfigPath:
    """Return the paths that one nesting declaration says are objects.

    Args:
        name: Name of the member the declaration is about.
        nesting: What the class declared about that member.

    Returns:
        The selector that addresses every configuration object it declares.
    """
    if nesting.kind is ConfigNestingKind.DICT_VALUE_BY_KEY:
        return (name, nesting.discriminator_key or EVERY_ELEMENT)
    if nesting.kind in (ConfigNestingKind.LIST_ELEMENT,
                        ConfigNestingKind.DICT_VALUE):
        return (name, EVERY_ELEMENT)
    return (name,)


def nested_selectors(config: Config) -> frozenset[ConfigPath]:
    """Return where this configuration declares nested objects to be.

    A member that holds one is addressed by its own path, and a member that
    holds a list or a dict of them is addressed by that path and
    `EVERY_ELEMENT`: what is declared is where the objects are, and the member
    that holds them is an ordinary container of the tree.

    Args:
        config: Configuration object being edited. It is not modified.

    Returns:
        One selector per nesting the class declares.
    """
    return frozenset(_nesting_selector(name=name, nesting=nesting)
                     for name, declared in config.nested_configs().items()
                     for nesting in (declared if isinstance(declared, list)
                                     else [declared]))


def is_nested(path: ConfigPath, nested: Collection[ConfigPath]) -> bool:
    """Return whether one node is a declared nested configuration object.

    Args:
        path: Path of the node to ask about.
        nested: The selectors that say where such an object is.

    Returns:
        Whether any of them addresses that node.
    """
    return any(selects(selector=selector, path=path) for selector in nested)


def flat_values(members: Mapping[str, JsonType], order: Sequence[str],
                nested: Collection[ConfigPath] = frozenset()) \
        -> list[tuple[ConfigPath, JsonType]]:
    """Return every node of one configuration, depth first, in row order.

    Args:
        members: One JSON space value per serialized member.
        order: The member names in the order they are shown, which is the
            order the configuration class declares them in.
        nested: Selectors saying which nodes are declared configuration
            objects, which are not taken apart whatever they hold.

    Returns:
        The path and the value of every node, each container before what is
        inside it.
    """
    found: list[tuple[ConfigPath, JsonType]] = []
    for name in order:
        found.extend(_walked((name,), members[name], nested))
    return found


def under_dict(path: ConfigPath,
               values: Mapping[ConfigPath, JsonType]) -> bool:
    """Return whether one node is a value of a dictionary.

    A member of the configuration is one, because the configuration itself is
    the outermost dictionary of the file. An element of a list is not. It is
    the question a parse converter is answered by, since `config_as_json`
    applies one while it decodes an object and to nothing else.

    Args:
        path: Path of the node to ask about.
        values: The value of every node, by path.

    Returns:
        Whether that node is the value of a dictionary key.
    """
    parent = path[:-1]
    return not parent or isinstance(values.get(parent), dict)


def dict_nodes(members: Mapping[str, JsonType],
               nested: Collection[ConfigPath] = frozenset()) \
        -> list[tuple[ConfigPath, JsonType]]:
    """Return every node that a parse converter of this class can reach.

    Args:
        members: One JSON space value per serialized member.
        nested: Selectors saying which nodes are declared configuration
            objects, whose own converters are their own class's to declare.

    Returns:
        The path and the value of every node that is the value of a
        dictionary key, the configuration itself counting as a dictionary.
    """
    flat = flat_values(members=members, order=list(members), nested=nested)
    values = dict(flat)
    return [(path, value) for path, value in flat
            if under_dict(path=path, values=values)]


def assembled(children: Sequence[tuple[str, JsonType]],
              as_list: bool) -> JsonType:
    """Return the value of one container, built from its children.

    Args:
        children: The last step and the current value of each child, in the
            order the container holds them.
        as_list: Whether the container is a list rather than a dict.

    Returns:
        The value that the container holds now.
    """
    if as_list:
        return [value for _, value in children]
    return dict(children)
