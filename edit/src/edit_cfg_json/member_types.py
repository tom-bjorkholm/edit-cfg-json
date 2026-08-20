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

**What is made of the answer is deliberately little.** An annotation says one
of the kinds of `leaf_value`, or it says nothing this editor can use. A class
of the application's own is nothing it can use: what the editor does with a
kind is say what it is and make an empty one of it, and it can do neither with
a class it has never seen. Where the member holds a nested configuration
object, the object itself is what answers (section 4.1 of `doc/design.md`),
and where it holds an enum, the parse converter of the class answers.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Mapping, Sequence
from textwrap import dedent
from types import NoneType
from typing import Optional, get_args, get_origin, get_type_hints
import ast
import inspect
import sys
from config_as_json import ConfigPath, JsonType
from edit_cfg_json.leaf_value import LeafType, VALUE_KINDS
from edit_cfg_json.tree import ConfigNode, owner_path

SELF_NAME = 'self'
"""What the first argument of a method is called, by every convention."""

SOURCE_ERRORS = (OSError, SyntaxError, TypeError, ValueError)
"""Every way in which the source of one method can fail to be read.

`inspect.getsource` raises `OSError` for a class defined where there is no
source to read — an interactive session, `exec`, and a frozen program are the
three — and `TypeError` for an object it cannot take source from at all.
Parsing what it did read is what raises the other two.
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


def _optional_type(rest: Sequence[object]) -> LeafType:
    """Return what an annotation that also allows nothing says.

    A union of more than one type beside `None` says nothing this editor can
    use, and it therefore does not say that the member may hold nothing
    either: the two states of such a member are *holds a value* and *holds
    nothing*, and a member the editor cannot make a value for has only one of
    them.

    Args:
        rest: What the union allows beside nothing.

    Returns:
        What the annotation says, which says that it may hold nothing only
        where it also says what a value there would be.
    """
    found = leaf_type(rest[0]) if len(rest) == 1 else LeafType()
    return found._replace(nothing=found.kind is not None)


def leaf_type(hint: object) -> LeafType:
    """Return what one annotation says about the value it is about.

    Args:
        hint: What one annotation means.

    Returns:
        What that says about the value, which is empty for an annotation
        naming anything the editor cannot make a value of.
    """
    args = get_args(hint)
    if NoneType in args:
        return _optional_type([arg for arg in args if arg is not NoneType])
    origin: object = get_origin(hint) or hint
    if origin is list and args:
        return LeafType(kind=list, inside=leaf_type(args[0]))
    if origin is dict and len(args) > 1:
        return LeafType(kind=dict, inside=leaf_type(args[1]))
    return LeafType(kind=_known_kind(origin))


def _known_kind(origin: object) -> Optional[type]:
    """Return the kind one annotation names, None for anything else."""
    return next((kind for kind, _ in VALUE_KINDS if origin is kind), None)


def member_types(described: type[object]) -> dict[str, LeafType]:
    """Return what one class says about the type of each member it declares.

    Args:
        described: Class of the configuration object being asked.

    Returns:
        One answer per member whose declaration says anything, by the name of
        that member. A private attribute is never one, because a member of a
        configuration is a public attribute of it.
    """
    return {name: leaf_type(hint)
            for name, hint in declared_hints(described).items()
            if not name.startswith('_')}


def _type_at(path: ConfigPath, nodes: Mapping[ConfigPath, ConfigNode],
             owned: Mapping[ConfigPath, Mapping[str, LeafType]]
             ) -> Optional[LeafType]:
    """Return what the class owning one node says the value there is.

    The class that answers is the one that owns the subtree, exactly as it is
    for a parse converter and for an optional member: a nested configuration
    object declares its own members. What it declares is about the member, and
    a node inside that member is reached by stepping into what the member says
    is inside it, once per step.

    Args:
        path: Path of the node to answer for.
        nodes: Every configuration object of the tree, by its path.
        owned: What each of those objects declares, by the path of the object.

    Returns:
        What the value at that node is, and None where nothing says. A node
        that is not the member itself never says that it may hold nothing.
    """
    owner = owner_path(path=path, nodes=nodes)
    member = path[:len(owner) + 1]
    held = owned.get(owner, {}).get(member[-1])
    for _ in path[len(member):]:
        if held is None:
            return None
        held = held.inside
    if held is None or len(path) == len(member):
        return held
    return held._replace(nothing=False)


def node_types(nodes: Mapping[ConfigPath, ConfigNode],
               flat: Sequence[tuple[ConfigPath, JsonType]]
               ) -> dict[ConfigPath, LeafType]:
    """Return what the classes of one tree say about each node of it.

    Args:
        nodes: Every configuration object of the tree, by its path.
        flat: The path and the value of every node, in row order.

    Returns:
        One answer per node whose declaration says anything, by the path of
        that node.
    """
    owned = {path: member_types(type(node.config))
             for path, node in nodes.items() if node.config is not None}
    found = ((path, _type_at(path=path, nodes=nodes, owned=owned))
             for path, _ in flat)
    return {path: held for path, held in found if held is not None}
