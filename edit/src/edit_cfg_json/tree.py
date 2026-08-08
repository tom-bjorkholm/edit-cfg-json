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

**A declared nested configuration object is a node of its own**, and it is
what segments the tree. It serializes as a dict and it is not one: it has a
class and a docstring of its own, its members are rows below it in the order
that class declares them, and everything below it belongs to that class rather
than to the one above. That last part is the whole of what ownership means
here: a parse converter and an optional member are the owning class's, exactly
as `serialize_converters()` is on the way out.

**Where those objects are is asked of the objects themselves.** A member
holding one nested object is the least interesting case. A real configuration
has a list of nested objects, each of which holds a dict of more of them, and
`ConfigNestingKind` says so: `LIST_ELEMENT` and `DICT_VALUE` declare that every
value *inside* a member is one. So the declarations are walked over the
configuration object, which answers with the absolute path of every nested
object there really is, and with the object at it. The member that holds them
stays an ordinary container that can be folded and says how much it holds.

Walking the objects rather than matching a selector is what makes ownership
answerable at all: `parse_converters()` and `_omit_none_from_json()` are
methods of an object, and the declaration says only which class was expected.
It also tells the truth about a factory that answered with a subclass, and an
`OPTIONAL_MEMBER` that holds nothing: such a member has a class and no object,
which is a different thing from a member that has both.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Iterable, Iterator, Mapping, Sequence
from typing import NamedTuple, Optional
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

NO_OBJECT_FORM = 'no {name}'
"""What a declared nested member that holds no object says instead.

An `OPTIONAL_MEMBER` is what holds none, and a class that writes it as `null`
rather than leaving it out gives it a row. The row says which class would be
there and that there is nothing there, because both of those are worth knowing
and neither is a value: no text typed into a field becomes a configuration
object, so the row cannot be edited. Making one is adding, and belongs with
adding an element of a list.
"""

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


class ConfigNode(NamedTuple):
    """One declared configuration object of the tree, wherever it is."""

    config_type: type[Config]
    """Class of the object, or the class the member would hold.

    It is the class of the object itself wherever there is one, which is not
    always the declared class: a `factory_function` may answer with a subclass,
    and what the object really is is what its docstring and its converters
    belong to. It is the declared class only where there is no object.
    """

    config: Optional[Config]
    """The object itself, None for a member that holds none.

    An `OPTIONAL_MEMBER` is what holds none. Everything the editor asks of a
    node below this one is asked of this object, so a node that has none has
    nothing below it either.
    """


def _member_objects(name: str, held: object,
                    nesting: ConfigNesting) -> list[tuple[ConfigPath,
                                                          ConfigNode]]:
    """Return the objects that one nesting declaration says one member holds.

    Args:
        name: Name of the member the declaration is about.
        held: What that member holds.
        nesting: What the class declared about that member.

    Returns:
        The path of every configuration object of that member, relative to the
        object that declares it, and what is at each of them.
    """
    kind = nesting.kind
    if kind is ConfigNestingKind.LIST_ELEMENT and isinstance(held, list):
        return [((name, str(index)), _config_node(element, nesting))
                for index, element in enumerate(held)]
    if kind is ConfigNestingKind.DICT_VALUE and isinstance(held, dict):
        return [((name, key), _config_node(value, nesting))
                for key, value in held.items()]
    if kind is ConfigNestingKind.DICT_VALUE_BY_KEY:
        key = nesting.discriminator_key
        if key is None or not isinstance(held, dict) or key not in held:
            return []
        return [((name, key), _config_node(held[key], nesting))]
    return [((name,), _config_node(held, nesting))]


def _config_node(held: object, nesting: ConfigNesting) -> ConfigNode:
    """Return what is at one declared place, whether or not it holds one."""
    if isinstance(held, Config):
        return ConfigNode(config_type=type(held), config=held)
    return ConfigNode(config_type=nesting.config_type, config=None)


def _declared_objects(config: Config) -> Iterator[tuple[ConfigPath,
                                                        ConfigNode]]:
    """Yield every configuration object that one object declares directly."""
    for name, declared in config.nested_configs().items():
        held = getattr(config, name, None)
        listed = declared if isinstance(declared, list) else [declared]
        for nesting in listed:
            yield from _member_objects(name=name, held=held, nesting=nesting)


def config_nodes(config: Config) -> dict[ConfigPath, ConfigNode]:
    """Return every configuration object of one tree, by its path.

    The configuration itself is one of them, under the empty path, so that the
    object owning any node is found the same way whether that node is a member
    of the configuration or a member of something nested inside it.

    Args:
        config: Configuration object being edited. It is not modified.

    Returns:
        One entry per declared nested configuration object, and one for the
        configuration itself.
    """
    found: dict[ConfigPath, ConfigNode] = {
        (): ConfigNode(config_type=type(config), config=config)}
    _add_nodes_below(config=config, prefix=(), found=found)
    return found


def _add_nodes_below(config: Config, prefix: ConfigPath,
                     found: dict[ConfigPath, ConfigNode]) -> None:
    """Add every configuration object below one object, and below those."""
    for path, node in _declared_objects(config):
        found[prefix + path] = node
        if node.config is not None:
            _add_nodes_below(config=node.config, prefix=prefix + path,
                             found=found)


def owner_path(path: ConfigPath,
               nodes: Mapping[ConfigPath, ConfigNode]) -> ConfigPath:
    """Return the path of the configuration object that owns one node.

    Args:
        path: Path of the node to ask about.
        nodes: Every configuration object of the tree, by its path.

    Returns:
        The path of the innermost object that this node is inside, which is
        the empty path for a node of the configuration itself.
    """
    return max((owner for owner in nodes if len(owner) < len(path)
                and path[:len(owner)] == owner), key=len)


def ordered_names(config: Config,
                  members: Mapping[str, JsonType]) -> list[str]:
    """Return the serialized member names in the order they are declared.

    The declaration order is the order in which the configuration class
    assigns its members, which `vars()` preserves. That is the order the
    application thinks about its configuration in, so it is the order the
    editor shows. The JSON document cannot supply it, because
    `config_as_json` writes its keys sorted.

    A member that the class omits from JSON while its value is `None` is
    not serialized and so gets no row. A serialized name that is not an
    attribute of the object is appended instead of dropped, so that no
    member can go missing whatever a validator or a converter did.

    Only the members are ordered this way, and a nested configuration object
    has members of its own that are ordered by its own class. What is inside a
    list is in the order that list holds it, and what is inside a dict is in
    the order the file has it, which is the sorted one: a dictionary key has no
    declaration to be read from, and the order a save writes is the order that
    is shown.

    Args:
        config: Configuration object whose members are ordered. It is not
            modified.
        members: One JSON space value per serialized member of that object.

    Returns:
        The names of those members, in the order they are shown.
    """
    declared = [name for name in vars(config) if name in members]
    return declared + [name for name in members if name not in declared]


def _walked(path: ConfigPath, value: JsonType,
            nodes: Mapping[ConfigPath, ConfigNode]
            ) -> Iterator[tuple[ConfigPath, JsonType]]:
    """Yield one node and everything below it, the node itself first.

    A node comes before what is inside it, which is the order the rows are
    read in and the order they are shown in. A declared configuration object
    is walked into by the order its own class declares, and every ordinary
    container by the order it holds its values in.
    """
    yield path, value
    node = nodes.get(path)
    if node is None:
        for child, held in child_values(path=path, value=value):
            yield from _walked(path=child, value=held, nodes=nodes)
        return
    if node.config is None or not isinstance(value, dict):
        return
    for name in ordered_names(config=node.config, members=value):
        yield from _walked(path=path + (name,), value=value[name], nodes=nodes)


def flat_values(members: Mapping[str, JsonType],
                nodes: Mapping[ConfigPath, ConfigNode]) \
        -> list[tuple[ConfigPath, JsonType]]:
    """Return every node of one configuration, depth first, in row order.

    Args:
        members: One JSON space value per serialized member.
        nodes: Every configuration object of the tree, by its path, including
            the configuration itself under the empty path.

    Returns:
        The path and the value of every node, each of them before what is
        inside it.
    """
    root = nodes[()].config
    assert root is not None
    found: list[tuple[ConfigPath, JsonType]] = []
    for name in ordered_names(config=root, members=members):
        found.extend(_walked((name,), members[name], nodes))
    return found


def under_dict(path: ConfigPath,
               values: Mapping[ConfigPath, JsonType]) -> bool:
    """Return whether one node is a value of a dictionary.

    A member of the configuration is one, because the configuration itself is
    the outermost dictionary of the file, and so is a member of a nested
    configuration object, which writes a dictionary of its own. An element of
    a list is not. It is the question a parse converter is answered by, since
    `config_as_json` applies one while it decodes an object and to nothing
    else.

    Args:
        path: Path of the node to ask about.
        values: The value of every node, by path.

    Returns:
        Whether that node is the value of a dictionary key.
    """
    parent = path[:-1]
    return not parent or isinstance(values.get(parent), dict)


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
