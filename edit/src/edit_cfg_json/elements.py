#! /usr/bin/env python3
"""What a container offers, and what adding or removing an element does.

A member that holds several of something is not finished when its values can
be edited. A list of report outputs is a list because the number of them is a
decision of whoever configures the application, so an editor that could change
every one of them and add none would be refusing the decision the shape of the
member exists to allow.

**A new element is copied and never invented.** Where the class declares that
every element of a list or every value of a dict is a configuration object,
the declaration says which class to make one of, and one of that class holding
its own declared values is what a new element is. Where it declares nothing,
the values the class declares for the member itself are the pattern: the first
element of them, and failing that the first element the member holds now. A
member that has neither is a member the editor has nothing to copy for, and it
says so rather than inventing a value that the application never mentioned.

**What cannot be done is said and not left to be discovered.** A dict whose
keys are the ones its class declares cannot gain or lose one at all —
`config_as_json` checks a dict member against those keys while it parses — and
a dict whose keys the application decides with validators of its own, or one
where a single named key holds an object, is a key policy that this version
does not serve. Each of those is a sentence below that member, in the same
place and under the same toggle as everything else explanatory.

**Where an object is added, an object is made.** The tree finds the nested
configuration objects by walking the real objects rather than by matching a
declaration, so an element that existed only in the edit buffer would be shown
as the dictionary it serializes to, with the member order of nobody, the parse
converters of nobody and no badge of its own. So the model's own configuration
object — the copy the caller never sees — gains the object as the buffer gains
its values, and everything that walks the tree finds it there.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Iterable, Mapping, Sequence
from copy import deepcopy
from io import StringIO
from typing import NamedTuple, Optional, TextIO
from config_as_json import Config, ConfigNesting, ConfigNestingKind, \
    ConfigPath, JsonType
from edit_cfg_json.constructing import built_config
from edit_cfg_json.descriptions import optional_paths
from edit_cfg_json.loader import ConfigSource
from edit_cfg_json.tree import ConfigNode, config_nodes, member_nestings, \
    member_values, owner_path, path_text, unchecked_members

BUILD_ERRORS = (AttributeError, KeyError, TypeError, ValueError)
"""Every way in which constructing a configuration class can fail.

A class that needs a constructor argument this library knows nothing about
raises `TypeError`, one that declares no public member raises `AttributeError`,
and declared values that a validator refuses raise a `ValueError` subclass.
`NotImplementedError` is deliberately not one of them, for the same reason as
in the validation of a buffer: it says the configuration class is incomplete,
which is a defect of the application that no editing can put right.
"""

OBJECT_KINDS = (ConfigNestingKind.LIST_ELEMENT, ConfigNestingKind.DICT_VALUE)
"""The declarations that say every value inside one member is an object.

They are what makes a member of that shape extendable at all, and they are the
two that a new element is made from the declared class for. The other three
declarations are about the member itself rather than about what is inside it.
"""

NO_PATTERN = ('There is nothing here to copy a new element from: this class '
              'declares no element for this member and it holds none.')
"""What a list with nothing to copy says instead of offering to grow.

It is the one case that design section 11 of `doc/design.md` puts out of scope
for good rather than for now, because the missing thing cannot be supplied by
any amount of work here: only the application knows what an element of its own
list looks like, and a member it never gave one for has never said.
"""

NO_CLASS_FORM = ('The editor cannot construct {name} on its own, so it has '
                 'nothing to add here.')
"""What a container of objects says when their class cannot be constructed.

`config_as_json` asks a nested class for the constructor that it builds one
with while it parses, so this is a class that could not be read from a file
either. It is said here rather than found out when the control is pressed,
because a control that refuses every press is worse than no control.
"""

FIXED_KEYS = ('This version adds an entry only to a dict whose class '
              'declares that every value in it is one configuration object.')
"""What an ordinary dict member says instead of offering to grow.

`Config.check_dict_parse` matches such a member against the keys the class
declares for it, so a dict that gained or lost one would be refused by
`config_as_json` itself on the next validation pass. The editor says so rather
than offering a control that produces a refusal.
"""

BY_KEY_SCOPE = ('One named key of this dict holds a configuration object and '
                'the others do not, so its keys follow a policy of their own. '
                'This version does not add or remove them.')
"""What a `DICT_VALUE_BY_KEY` member says, which is out of scope for v1."""

UNCHECKED_SCOPE = ('The keys of this dict are the application\'s own to '
                   'decide, with validators of its own. This version does not '
                   'add or remove them.')
"""What a member of `_unchecked_dicts` says, which is out of scope for v1."""

NOT_EXTENDABLE = 'Nothing can be added to {name}.'
"""Message of the error raised when a node that offers no element is grown."""

NOT_REMOVABLE = '{name} is not something that can be removed.'
"""Message of the error raised when a node that is no element is removed."""

NOT_MOVABLE = '{name} cannot be moved that way.'
"""Message of the error raised when a node that is no element is moved."""

KEY_NEEDED = 'A new entry of {name} needs a key of its own.'
"""Message of the error raised when a dict is grown without a key."""

KEY_UNWANTED = '{name} holds a list, and an element of a list has no key.'
"""Message of the error raised when a list is grown with a key."""

KEY_TAKEN = '{name} already holds an entry called {key}.'
"""Message of the error raised when a new key is one the dict has."""


class ElementOffer(NamedTuple):
    """What one node of the tree offers to do with the elements it holds.

    It is one object rather than one attribute each on the row, because the
    five of them are read together and answer one question between them: what
    can be done here about how many things there are.

    A backend reads it to decide which controls one row gets, and creates none
    where nothing is offered: there is no column to keep clear, because these
    controls sit at the end of the line where a row without them needs no
    space held for it.
    """

    extend: bool = False
    """Whether an element can be added here.

    It is true for a list that something can be copied for, for a dict whose
    class says that every value in it is a configuration object, and for a
    declared member that holds no object yet, where adding is making the one
    object that member is for.
    """

    keyed: bool = False
    """Whether adding here needs a key that only the user can give.

    A new entry of a dict has to be called something, and nothing but the
    person configuring the application knows what. The two backends ask, each
    in the way its own toolkit asks a question, and a list is never keyed
    because an element of a list is addressed by where it is.
    """

    remove: bool = False
    """Whether this node can be taken out of the thing that holds it.

    An element of a list and a value of a dict of configuration objects can
    be. So can a declared optional member that holds an object, where removing
    is putting it back to holding none — but only where its class writes
    `null` for it. A class that leaves such a member out of the file
    altogether would leave it with no row at all, and a member the editor had
    taken off the screen for good could never be given an object again.
    """

    earlier: bool = False
    """Whether this element can change places with the one before it."""

    later: bool = False
    """Whether this element can change places with the one after it.

    The order of a list is part of what the file says, so it is part of what
    an editor of that file has to be able to change. A dict has no such
    question: it is written in the sorted order of its keys, so where an entry
    is shown follows from what it is called.
    """

    refusal: str = ''
    """Why nothing can be added here, empty where something can.

    It is empty for every node that is no container as well, because a value
    that holds nothing is not a member somebody expected to be able to grow.
    It is explanatory text and is shown with the explanations, below the
    member it is about, rather than as something to act on: it says what this
    member is, in the same way as the line saying what kind of value a member
    holds.
    """

    template: JsonType = None
    """What a new element here would hold, None where none can be added.

    It is kept with the offer because it is the same answer: what can be added
    is exactly what there is something to copy. A backend never reads it, and
    the buffer copies it rather than using it, since a list and a dict are
    values that the next edit would otherwise reach through both of them.
    """


class TreeFacts(NamedTuple):
    """Everything that saying what one tree offers needs.

    It is one object rather than one argument each, because every one of them
    is read once per node and none of them changes while the offers are made.
    """

    values: Mapping[ConfigPath, JsonType]
    """The value of every node of the tree, by its path."""

    nodes: Mapping[ConfigPath, ConfigNode]
    """Every configuration object of the tree, by its path."""

    nestings: Mapping[ConfigPath, ConfigNesting]
    """What each object declares about a member of its own, by that path."""

    unchecked: frozenset[ConfigPath]
    """Every dict member whose keys its own class does not check."""

    omitted: frozenset[ConfigPath]
    """Every member that the object holding it may leave out of the file."""

    defaults: Mapping[str, JsonType]
    """The values that the class of the configuration declares.

    They are what a new element of an ordinary list is copied from, and they
    are empty for a class the editor could not construct at all, which costs
    that configuration the offer and nothing else.
    """

    made: dict[ConfigNesting, Optional[JsonType]]
    """What one of each declared class holds, once it has been made.

    The offers are worked out again whenever the rows are, so a class that is
    declared in three places would otherwise be constructed three times per
    rebuild. None is a class that could not be constructed at all.
    """


def declared_values(source: ConfigSource, stream: TextIO) -> dict[str,
                                                                  JsonType]:
    """Return the values that the class of one session declares.

    They are asked for through the loader of the application where there is
    one, because that is what the loader protocol promises to answer with when
    it is given no JSON source, and a class that needs a constructor argument
    this library knows nothing about is reached no other way.

    A class that cannot be constructed answers with nothing, which is principle
    4 of section 3 of `doc/design.md`: what the editor cannot find out it does
    without, and here that costs the offer to grow an ordinary list and
    nothing else.

    Args:
        source: The configuration of this session and how it is constructed.
        stream: Stream that collects what the construction says.

    Returns:
        One JSON space value per declared member, and nothing at all for a
        class the editor could not construct.
    """
    try:
        return member_values(config=source.made(stream=stream),
                             stderr_file=stream)
    except BUILD_ERRORS:
        return {}


def tree_facts(nodes: Mapping[ConfigPath, ConfigNode],
               flat: Sequence[tuple[ConfigPath, JsonType]],
               defaults: Mapping[str, JsonType]) -> TreeFacts:
    """Return everything that saying what one tree offers needs.

    Args:
        nodes: Every configuration object of the tree, by its path.
        flat: The path and the value of every node, in row order.
        defaults: The values that the class of the configuration declares.

    Returns:
        The facts that one offer per node is made from.
    """
    return TreeFacts(values=dict(flat), nodes=nodes,
                     nestings=member_nestings(nodes),
                     unchecked=unchecked_members(nodes),
                     omitted=optional_paths(nodes), defaults=defaults, made={})


def element_offers(facts: TreeFacts) -> dict[ConfigPath, ElementOffer]:
    """Return what every node of one tree offers, by the path of that node.

    Args:
        facts: What the tree is, and what its class declares.

    Returns:
        One offer per node, most of them offering nothing at all: a value is
        not something that holds elements, and neither is a node of a
        configuration object, whose members are the ones its class declares.
    """
    return {path: _offer_of(path=path, facts=facts) for path in facts.values}


def _offer_of(path: ConfigPath, facts: TreeFacts) -> ElementOffer:
    """Return what one node offers about the elements it holds."""
    offer = _extending(path=path, facts=facts)
    return offer._replace(
        remove=_removable(path=path, facts=facts),
        earlier=_movable(path=path, facts=facts, later=False),
        later=_movable(path=path, facts=facts, later=True))


def _extending(path: ConfigPath, facts: TreeFacts) -> ElementOffer:
    """Return whether one node can be given an element, and why not.

    A node where a class declared an object and none is there is the one node
    that is grown without being a container: adding there is making the object
    that the member is for, which design section 4.1 of `doc/design.md` says
    belongs with adding an element of a list. A node that holds the object is
    a configuration of its own, and the members of a configuration are the
    ones its class declares.
    """
    node = facts.nodes.get(path)
    if node is not None:
        return ElementOffer() if node.config is not None \
            else _new_object(path=path, facts=facts)
    value = facts.values[path]
    if isinstance(value, list):
        return _growing_list(path=path, facts=facts, value=value)
    if isinstance(value, dict):
        return _growing_dict(path=path, facts=facts)
    return ElementOffer()


def _new_object(path: ConfigPath, facts: TreeFacts) -> ElementOffer:
    """Return whether a declared member holding no object can be given one."""
    nesting = facts.nestings.get(path)
    if nesting is None:
        return ElementOffer()
    if nesting.kind is ConfigNestingKind.DICT_VALUE_BY_KEY:
        return ElementOffer(refusal=BY_KEY_SCOPE)
    return _from_class(nesting=nesting, facts=facts, keyed=False)


def _growing_list(path: ConfigPath, facts: TreeFacts,
                  value: list[JsonType]) -> ElementOffer:
    """Return whether one list can be given an element, and why not."""
    nesting = facts.nestings.get(path)
    if nesting is not None and nesting.kind is ConfigNestingKind.LIST_ELEMENT:
        return _from_class(nesting=nesting, facts=facts, keyed=False)
    pattern = _declared_element(path=path, facts=facts)
    if pattern is None and value:
        pattern = value[0]
    if pattern is None:
        return ElementOffer(refusal=NO_PATTERN)
    return ElementOffer(extend=True, template=pattern)


def _growing_dict(path: ConfigPath, facts: TreeFacts) -> ElementOffer:
    """Return whether one dict can be given an entry, and why not."""
    nesting = facts.nestings.get(path)
    kind = None if nesting is None else nesting.kind
    if kind is ConfigNestingKind.DICT_VALUE:
        assert nesting is not None
        return _from_class(nesting=nesting, facts=facts, keyed=True)
    if kind is ConfigNestingKind.DICT_VALUE_BY_KEY:
        return ElementOffer(refusal=BY_KEY_SCOPE)
    if _member_path(path=path, facts=facts) in facts.unchecked:
        return ElementOffer(refusal=UNCHECKED_SCOPE)
    return ElementOffer(refusal=FIXED_KEYS)


def _from_class(nesting: ConfigNesting, facts: TreeFacts,
                keyed: bool) -> ElementOffer:
    """Return the offer of a node whose elements one class declares."""
    template = _declared_object(nesting=nesting, made=facts.made)
    if template is None:
        return ElementOffer(refusal=NO_CLASS_FORM.format(
            name=nesting.config_type.__name__))
    return ElementOffer(extend=True, keyed=keyed, template=template)


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


def _declared_object(nesting: ConfigNesting,
                     made: dict[ConfigNesting, Optional[JsonType]]
                     ) -> Optional[JsonType]:
    """Return what one new object of a declared class holds, or None."""
    if nesting not in made:
        made[nesting] = _built_values(nesting)
    return made[nesting]


def _built_values(nesting: ConfigNesting) -> Optional[JsonType]:
    """Return the values of one new object of a declared class, or None."""
    said = StringIO()
    try:
        return member_values(config=new_object(nesting=nesting, stream=said),
                             stderr_file=said)
    except BUILD_ERRORS:
        return None


def _declared_element(path: ConfigPath,
                      facts: TreeFacts) -> Optional[JsonType]:
    """Return the first element the class declares for one node, or None.

    The path is followed through the declared values of the configuration,
    which is what makes a list inside a nested object answerable as well as a
    list that is a member: it is the same path in both trees wherever the
    declared values reach that far. A step that they do not reach — an index
    of a list the class declares fewer elements for, or a key of a dict it
    does not hold — is a node the class said nothing about.

    Args:
        path: Path of the list to find a pattern for.
        facts: What the tree is, and what its class declares.

    Returns:
        The first element the class declares there, or None where it declares
        no list at that path or declares an empty one.
    """
    found: JsonType = dict(facts.defaults)
    for step in path:
        found = _step_into(found, step)
    return found[0] if isinstance(found, list) and found else None


def _step_into(value: JsonType, step: str) -> JsonType:
    """Return what is at one step of one path, or None where nothing is."""
    if isinstance(value, dict):
        return value.get(step)
    if isinstance(value, list) and step.isdigit() and int(step) < len(value):
        return value[int(step)]
    return None


def _member_path(path: ConfigPath, facts: TreeFacts) -> ConfigPath:
    """Return the path of the member of a configuration one node is in.

    A node is inside exactly one member of exactly one configuration object,
    and that member is what a class says its key policy about: a dict inside a
    dict of an unchecked member is unchecked with it, because the check that
    `_unchecked_dicts` takes away stops at the member rather than recursing.
    """
    owner = owner_path(path=path, nodes=facts.nodes)
    return path[:len(owner) + 1]


def _removable(path: ConfigPath, facts: TreeFacts) -> bool:
    """Return whether one node can be taken out of what holds it."""
    nesting = facts.nestings.get(path)
    if nesting is not None and \
            nesting.kind is ConfigNestingKind.OPTIONAL_MEMBER:
        node = facts.nodes.get(path)
        return node is not None and node.config is not None and \
            path not in facts.omitted
    return _element_of(path=path, facts=facts) is not None


def _movable(path: ConfigPath, facts: TreeFacts, later: bool) -> bool:
    """Return whether one element can change places with a neighbour."""
    held = _element_of(path=path, facts=facts)
    if not isinstance(held, list) or not path[-1].isdigit():
        return False
    index = int(path[-1])
    return index + 1 < len(held) if later else index > 0


def _element_of(path: ConfigPath, facts: TreeFacts) -> Optional[JsonType]:
    """Return the container one node is an element of, or None.

    A member of a configuration object is not an element of anything, however
    much the object writes itself as a dictionary: its members are the ones its
    class declares, and its class is what would have to be changed to have
    another one.
    """
    parent = path[:-1]
    if not parent or parent in facts.nodes:
        return None
    held = facts.values.get(parent)
    if isinstance(held, list):
        return held
    if isinstance(held, dict) and _holds_objects(parent, facts):
        return held
    return None


def _holds_objects(path: ConfigPath, facts: TreeFacts) -> bool:
    """Return whether a class declared every value of one dict an object."""
    nesting = facts.nestings.get(path)
    return nesting is not None and nesting.kind is ConfigNestingKind.DICT_VALUE


def grown(value: JsonType, key: str, template: JsonType) -> JsonType:
    """Return one container with one more element in it.

    A list grows at the end, because that is where a new element is put when
    nothing says otherwise, and it can be moved from there. A dict is written
    again in the sorted order of its keys, which is the order a file holds it
    in and therefore the order the rows are shown in.

    Args:
        value: Value of the container as it is now.
        key: Name of the new entry of a dict, empty for a list.
        template: What the new element holds, which is copied rather than
            used, so that editing it cannot reach whatever it came from.

    Returns:
        That container with the new element in it.
    """
    made = deepcopy(template)
    if isinstance(value, list):
        return [*value, made]
    assert isinstance(value, dict)
    return dict(sorted({**value, key: made}.items()))


def shrunk(value: JsonType, step: str) -> JsonType:
    """Return one container with one element taken out of it.

    Args:
        value: Value of the container as it is now.
        step: Last step of the path of the element, which is the index of a
            list element written out or the key of a dictionary entry.

    Returns:
        That container without that element.
    """
    if isinstance(value, list):
        index = int(step)
        return [*value[:index], *value[index + 1:]]
    assert isinstance(value, dict)
    return {key: held for key, held in value.items() if key != step}


def swapped(value: JsonType, index: int, later: bool) -> JsonType:
    """Return one list with one element in the place of a neighbour.

    Args:
        value: Value of the list as it is now.
        index: Where the element to move is now.
        later: Whether it changes places with the one after it rather than
            with the one before it.

    Returns:
        That list in its new order.
    """
    assert isinstance(value, list)
    other = index + 1 if later else index - 1
    order = list(range(len(value)))
    order[index], order[other] = order[other], order[index]
    return [value[old] for old in order]


def moved_paths(paths: Iterable[ConfigPath], container: ConfigPath,
                order: Sequence[int]) -> dict[ConfigPath, ConfigPath]:
    """Return where each node under one list goes when its order changes.

    Everything the editor holds about a node is held under the path of that
    node — what it is compared against, whether its container is folded, what
    the object at it said about itself — and an element of a list is addressed
    by where it is. So a change to how many elements there are, or to the order
    of them, moves all of that along with the values.

    Without it a removal would leave every element after it comparing itself
    with the element that used to be there, and would report every one of them
    as edited by a user who touched none of them.

    Args:
        paths: Path of every node there is.
        container: Path of the list whose elements have moved.
        order: The index each element of the new list had in the old one, one
            entry per element the list holds now.

    Returns:
        The new path of every node whose path has changed, by its old path.
        An element that stayed where it was is not in it, and neither is one
        that has gone.
    """
    places = {str(old): str(new) for new, old in enumerate(order)
              if old != new}
    depth = len(container)
    return {path: container + (places[path[depth]],) + path[depth + 1:]
            for path in paths
            if len(path) > depth and path[:depth] == container
            and path[depth] in places}


def kept_order(count: int, without: int) -> list[int]:
    """Return the order of one list with one element taken out of it."""
    return [index for index in range(count) if index != without]


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
    found = _declared_at(config=config, path=path)
    if found is None:
        return
    holder, nesting = found
    made = new_object(nesting=nesting, stream=stream)
    if nesting.kind is ConfigNestingKind.LIST_ELEMENT:
        getattr(holder, path[-1]).append(made)
    elif nesting.kind is ConfigNestingKind.DICT_VALUE:
        getattr(holder, path[-1])[key] = made
    else:
        setattr(holder, path[-1], made)


def object_removed(config: Config, path: ConfigPath) -> None:
    """Take the configuration object of a removed element out of the tree.

    Args:
        config: Configuration object of the session, which this modifies. It
            is the editor's own copy and never the caller's.
        path: Path of the element that has been removed, or of the declared
            member that has been put back to holding no object.
    """
    cleared = _declared_at(config=config, path=path)
    if cleared is not None:
        setattr(cleared[0], path[-1], None)
        return
    found = _declared_at(config=config, path=path[:-1])
    if found is None:
        return
    holder, nesting = found
    if nesting.kind in OBJECT_KINDS:
        held = getattr(holder, path[-2])
        del held[int(path[-1]) if isinstance(held, list) else path[-1]]


def object_moved(config: Config, path: ConfigPath, later: bool) -> None:
    """Move the configuration object of a moved element with its values.

    Args:
        config: Configuration object of the session, which this modifies. It
            is the editor's own copy and never the caller's.
        path: Path of the element that has been moved.
        later: Whether it changed places with the one after it.
    """
    found = _declared_at(config=config, path=path[:-1])
    if found is None or found[1].kind is not ConfigNestingKind.LIST_ELEMENT:
        return
    held = getattr(found[0], path[-2])
    index = int(path[-1])
    other = index + 1 if later else index - 1
    held[index], held[other] = held[other], held[index]


def _declared_at(config: Config,
                 path: ConfigPath) -> Optional[tuple[Config, ConfigNesting]]:
    """Return the object holding one declared member, and its declaration.

    Args:
        config: Configuration object of the session. It is not modified here.
        path: Path to ask about, which is a declared member of one of the
            objects of the tree or something else entirely.

    Returns:
        The object that declares that member and what it declared, and None
        for a path that is no declared member of this configuration.
    """
    nodes = config_nodes(config)
    nesting = member_nestings(nodes).get(path)
    if nesting is None:
        return None
    holder = nodes[owner_path(path=path, nodes=nodes)].config
    assert holder is not None
    return holder, nesting


def checked_key(offer: ElementOffer, value: JsonType, key: str,
                path: ConfigPath) -> None:
    """Refuse a key that cannot name the new element of one container.

    Args:
        offer: What that container offers, which says whether it is keyed.
        value: Value of the container as it is now.
        key: Name that the new entry was asked to have.
        path: Path of the container, for the message.

    Raises:
        ValueError: A list was given a key, a dict was given none, or the key
            is one that dict already holds. The last of those is a refusal and
            not a replacement: a new entry that quietly overwrote an existing
            one would lose what the user had.
    """
    if not offer.keyed:
        if key:
            raise ValueError(KEY_UNWANTED.format(name=path_text(path)))
        return
    if not key:
        raise ValueError(KEY_NEEDED.format(name=path_text(path)))
    if isinstance(value, dict) and key in value:
        raise ValueError(KEY_TAKEN.format(name=path_text(path), key=key))


def refused(offered: bool, form: str, path: ConfigPath) -> None:
    """Raise the refusal of one change that a node does not offer.

    Args:
        offered: Whether the node offers it after all.
        form: Form of the message that says it does not.
        path: Path of the node that was asked.

    Raises:
        ValueError: The node does not offer that change.
    """
    if not offered:
        raise ValueError(form.format(name=path_text(path)))
