#! /usr/bin/env python3
"""What the class of a configuration says the type of each member is.

The value a member held when the file was last agreed with says a great deal
about it, and there are two things it cannot say. A member that holds nothing
says nothing at all about what it would hold, and a member declared `float`
whose default is written `0` says the wrong thing. Both are answered by the
declaration, which is what this module reads.

**Three sources, in order of authority.** A class built on the dataclass
pattern, and any class with class level annotations, records real types that
`typing.get_type_hints` answers with. The ordinary `Config` pattern records
nothing at all: `self.answer: int = 42` inside `__init__` is a PEP 526
annotation on an instance attribute, and Python keeps it nowhere, so the
source of the class is read and its annotations are taken from there.
Where neither answers, the value is still what says the kind, exactly as
before, and that is what makes every one of these optional: a class whose
source cannot be read costs the editor what a declaration would have added
and nothing else.

**Nothing here is evaluated by this module.** An annotation read from source
is a text, and the text is given to `inspect.get_annotations`, which is the
standard library's own resolver for one — the same resolution
`typing.get_type_hints` does, in the namespace of the module that class was
written in. One annotation that will not resolve costs that member its
declaration and leaves every other member of the class alone.

**What is made of the answer is the types it allows**, as `type_options`
reads them: one alternative per type a union names, each spelled as Python
spells it. A member whose declaration names nothing usable answers with none,
and the value it holds is then what says its type. Where the member holds a
nested configuration object the object itself is what answers for its members
(section 4.1 of `doc/detailed_design.md`), and where it holds an enum the parse
converter of the class answers for its names.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Mapping, Sequence
from textwrap import dedent
from types import MappingProxyType
from typing import NamedTuple, Optional, get_type_hints
import ast
import inspect
import sys
from config_as_json import ConfigNesting, ConfigNestingKind, ConfigPath, \
    JsonType
from edit_cfg_json.tree import ConfigNode, owner_path
from edit_cfg_json.type_options import NONE_TYPE, TypeOption, choosable, \
    kept_choice, node_options, type_options

SELF_NAME = 'self'
"""What the first argument of a method is called, by every convention."""

SOURCE_ERRORS = (OSError, SyntaxError, TypeError, ValueError)
"""Every way in which the source of one method can fail to be read.

`inspect.getsource` raises `OSError` for a class defined where there is no
source to read — an interactive session, `exec`, and a frozen program are the
three — and `TypeError` for an object it cannot take source from at all.
Parsing what it did read is what raises the other two.
"""

NOTHING_KINDS = (ConfigNestingKind.OPTIONAL_MEMBER,
                 ConfigNestingKind.DICT_VALUE_BY_KEY)
"""The declarations of a place that holds one object or holds nothing.

A member that may hold none, and a named key that the file need not have.
`MEMBER` holds one always, and so does every element of a `LIST_ELEMENT` and
every value of a `DICT_VALUE` member: `config_as_json` refuses `null` there.
"""

HINT_ERRORS = (AttributeError, NameError, SyntaxError, TypeError, ValueError,
               RecursionError)
"""Every way in which one annotation can fail to say what it means.

A name that is not in the namespace of its own module is the ordinary one, and
it arises for real: a name imported under `if TYPE_CHECKING` exists while the
type checker reads the file and never at runtime. An annotation that fails
costs that member its declaration and nothing else.
"""


def _self_attribute(target: ast.expr) -> Optional[str]:
    """Return the attribute one `self.x` target names, or None for anything.

    Args:
        target: What one annotated assignment assigns to.

    Returns:
        The name of the attribute, and None for an assignment to anything
        other than an attribute of `self`.
    """
    if isinstance(target, ast.Attribute) and \
            isinstance(target.value, ast.Name) and \
            target.value.id == SELF_NAME:
        return target.attr
    return None


def attribute_texts(described: type[object]) -> dict[str, str]:
    """Return the annotation of every attribute one class sets on `self`.

    The whole of the class is read and not only its `__init__`, because a
    class is free to declare its members in a method of its own that
    `__init__` calls, and the annotations are just as real there. Only the
    source this class writes itself: a class further up is asked in its own
    right, and its own module is where the names of its annotations mean
    something.

    Args:
        described: Class to read the source of.

    Returns:
        One annotation per annotated attribute of `self`, as the text it is
        written as, and nothing at all for a class whose source cannot be
        read.
    """
    try:
        body = ast.parse(dedent(inspect.getsource(described)))
    except SOURCE_ERRORS:
        return {}
    found = ((_self_attribute(node.target), node.annotation)
             for node in ast.walk(body) if isinstance(node, ast.AnnAssign))
    return {name: _annotation_text(annotation) for name, annotation in found
            if name is not None}


def _annotation_text(annotation: ast.expr) -> str:
    """Return one annotation as the text that says what it means.

    An annotation written in quotation marks is a text in the source, so
    writing that source out again would give a text of a text, and resolving
    *that* would answer with the name rather than with what the name means. A
    forward reference means the same thing as the annotation written without
    the quotation marks, so it is unwrapped here.

    Args:
        annotation: What one annotated assignment is annotated with.

    Returns:
        The annotation as the text to resolve.
    """
    if isinstance(annotation, ast.Constant) and \
            isinstance(annotation.value, str):
        return annotation.value
    return ast.unparse(annotation)


def _one_hint(name: str, text: str,
              namespace: Mapping[str, object]) -> dict[str, object]:
    """Return what one annotation text means, or nothing where it will not.

    Args:
        name: Name of the member the annotation is about.
        text: The annotation as it is written in the source.
        namespace: The module the class was written in, which is where the
            names of its annotations mean something.

    Returns:
        That one member and what its annotation means, and an empty mapping
        for an annotation that does not resolve.
    """
    def holder() -> None:
        """Carry the annotation so that the standard library resolves it."""
    holder.__annotations__ = {name: text}
    try:
        return dict(inspect.get_annotations(holder, globals=dict(namespace),
                                            eval_str=True))
    except HINT_ERRORS:
        return {}


def _written_hints(described: type[object]) -> dict[str, object]:
    """Return what the annotations in one class's own source mean."""
    module = sys.modules.get(described.__module__)
    namespace = {} if module is None else vars(module)
    found: dict[str, object] = {}
    for name, text in attribute_texts(described).items():
        found.update(_one_hint(name=name, text=text, namespace=namespace))
    return found


def _class_hints(described: type[object]) -> dict[str, object]:
    """Return the class level annotations of one class and its bases."""
    try:
        return dict(get_type_hints(described))
    except HINT_ERRORS:
        return {}


def declared_hints(described: type[object]) -> dict[str, object]:
    """Return what every declaration of one class says its members are.

    The bases are walked from the top down, so a class that annotates a member
    its base also annotates is the one that answers for it, which is what
    Python itself does with the value.

    Args:
        described: Class of the configuration object being asked.

    Returns:
        One annotation per member that has one, as what it means.
    """
    found = _class_hints(described)
    for base in reversed(described.__mro__):
        found.update(_written_hints(base))
    return found


def member_types(described: type[object]) -> dict[str,
                                                  tuple[TypeOption, ...]]:
    """Return the types one class allows each member it declares to hold.

    Args:
        described: Class of the configuration object being asked.

    Returns:
        The alternatives of every member whose declaration names any usable
        type, by the name of that member. A private attribute is never one,
        because a member of a configuration is a public attribute of it.
    """
    found = ((name, type_options(hint))
             for name, hint in declared_hints(described).items()
             if not name.startswith('_'))
    return {name: options for name, options in found if options}


class KeptTypes(NamedTuple):
    """The types the user chose, as the rows are about to be built again."""

    chosen: Mapping[ConfigPath, TypeOption] = MappingProxyType({})
    """The type each node whose type is chosen held before, by its path."""

    refreshing: bool = False
    """Whether the rows are what a validation pass left behind.

    That is the one build in which the value has a say again over the type
    the user chose, as `type_options.kept_choice` says.
    """


def _type_at(path: ConfigPath, nodes: Mapping[ConfigPath, ConfigNode],
             owned: Mapping[ConfigPath, Mapping[str, tuple[TypeOption, ...]]],
             values: Mapping[ConfigPath, JsonType],
             kept: KeptTypes) -> tuple[TypeOption, ...]:
    """Return the types the class owning one node allows that node to hold.

    The class that answers is the one that owns the subtree, exactly as it is
    for a parse converter and for an optional member: a nested configuration
    object declares its own members. A node where a declaration puts an object
    is answered by that declaration instead, as `object_types` says. What it
    declares is about the member, and a node inside that member is reached by
    stepping into what the member allows inside it, once per step. Where a
    container is allowed to be more than one type, the step goes through the
    one it holds, which is what makes the inside of `list[str] |
    list[list[str]]` either of the two, and through a configuration class only
    where the tree has an object. The type it holds is the one the user chose
    where there is one, because `[]` is both of those lists and only the choice
    says which, and the one its value is otherwise.

    Args:
        path: Path of the node to answer for.
        nodes: Every configuration object of the tree, by its path.
        owned: What each of those objects declares, by the path of the object.
        values: The value of every node of the tree, by its path.
        kept: The types the user chose, and whether a pass is being taken in.

    Returns:
        The types that node may hold, and none where nothing usable says.
    """
    node = nodes.get(path)
    if node is not None and node.nesting is not None:
        return object_types(node.nesting)
    owner = owner_path(path=path, nodes=nodes)
    member = path[:len(owner) + 1]
    options = owned.get(owner, {}).get(member[-1], ())
    for depth in range(len(member), len(path)):
        step = path[:depth]
        held = kept_choice(options=node_options(options, step in nodes),
                           value=values.get(step),
                           chosen=kept.chosen.get(step),
                           refreshing=kept.refreshing)
        options = () if held is None else held.inside
    return options


def node_types(nodes: Mapping[ConfigPath, ConfigNode],
               flat: Sequence[tuple[ConfigPath, JsonType]],
               kept: KeptTypes = KeptTypes()
               ) -> dict[ConfigPath, tuple[TypeOption, ...]]:
    """Return the types the classes of one tree allow each node of it.

    Args:
        nodes: Every configuration object of the tree, by its path.
        flat: The path and the value of every node, in row order.
        kept: The types the user chose, and whether a pass is being taken in,
            which is what says which type a container whose value fits more
            than one of its types holds.

    Returns:
        The alternatives of every node whose declaration names any usable
        type, by the path of that node.
    """
    owned = {path: member_types(type(node.config))
             for path, node in nodes.items() if node.config is not None}
    values = dict(flat)
    found = ((path, _type_at(path=path, nodes=nodes, owned=owned,
                             values=values, kept=kept)) for path, _ in flat)
    return {path: options for path, options in found if options}


def object_types(nesting: ConfigNesting) -> tuple[TypeOption, ...]:
    """Return the types a place that one declaration puts an object at allows.

    It is the class the declaration names, and `None` beside it where the
    declaration lets the place hold nothing. The declaration answers rather
    than the annotation of the member, because it is what `config_as_json`
    constructs the object by and what it refuses `null` by: an
    `Optional[StageConfig]` declared `MEMBER` may not hold nothing, and an
    unannotated member declared `OPTIONAL_MEMBER` may.

    Args:
        nesting: What the class declared about the place.

    Returns:
        The class, and `None` where the place may hold none.
    """
    nothing = (NONE_TYPE,) if nesting.kind in NOTHING_KINDS else ()
    return type_options(nesting.config_type) + nothing


def nothing_allowed(options: Sequence[TypeOption]) -> bool:
    """Return whether holding nothing is a state of one node, not a value.

    A node has the two states of a value and of nothing where `None` is one of
    the types it is offered and the type it holds is the user's to choose: the
    pull-down of its types then moves it between the two, a value inside a
    list or a dict as much as a member, and a configuration object as much as
    a value (section 4.2 of `doc/detailed_design.md`).

    A node offered `None` and nothing else holds nothing as the one state its
    class would accept, wherever it is: `Optional[dict[str, int]]` where the
    class holds no dict to match one against is that. It is a state for the
    same reason, so that no field is given it to type a refused value into.

    Every other node has one state, whatever its declaration allows: that is
    `Path | None`, where the editor could make no value of anything but
    `None`, and its field takes the text of `null` as the JSON it is.

    Args:
        options: The types the node is offered, the ones its class would
            refuse left out.

    Returns:
        Whether that node holding nothing is a state of it.
    """
    return NONE_TYPE in options and (len(options) == 1 or choosable(options))
