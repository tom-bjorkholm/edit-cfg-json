#! /usr/bin/env python3
"""What a container offers, and what adding or removing an element does.

A member that holds several of something is not finished when its values can
be edited. A list of report outputs is a list because the number of them is a
decision of whoever configures the application, so an editor that could change
every one of them and add none would be refusing the decision the shape of the
member exists to allow.

**A new element is copied and never invented**, from one of three places,
every one of them the application's. Where the class declares that every
element of a list or every value of a dict is a configuration object, the
declaration says which class to make one of, and one of that class holding its
own declared values is what a new element is. Where it declares nothing, the
values the class declares for the member itself are the pattern: the first
element of them, and failing that the first element the member holds now. And
where no value at all says, the declared type of the member does, which
`_typed_element` is: `list[str]` says that an element of that list is text,
and the empty text is the one value of that kind that says no more than which
kind it is. It is asked last because a value the application wrote says more
about what belongs in that list than its kind does. A member that has none of
the three is a member the editor has nothing to copy for, and it says so
rather than inventing a value that the application never mentioned.

**What cannot be done is said and not left to be discovered.** A dict whose
keys are the ones its class declares cannot gain or lose one at all —
`config_as_json` checks a dict against those keys while it parses — so that is
a sentence below that dict, in the same place and under the same toggle as
everything else explanatory.

**Which dicts those are is a question about where the dict sits.**
`Config.check_dict_parse` is applied once per member and recurses from there
into the dict values of that member, so it reaches a dict only where it was
applied to the member at all and where every step down was into a dict that
the object it checks against holds. What stops it is `dict_check`, which is
also what says which types a node may be given: a member named in
`nested_configs()`, which `config_as_json` reads whole instead; a place named
in `_unchecked_dicts`, whose key policy the class defines with validators of
its own; and a list between the member and the dict, which the recursion
cannot step into. A dict the check does not reach is an ordinary container
here, and what the application's own validators make of a new key is the
ordinary verdict.

**A member whose values are of two kinds is asked twice.** A
`DICT_VALUE_BY_KEY` declaration names one key of a dict that holds a
configuration object, and every other key of that dict holds an ordinary
value. Nothing checks which keys such a member has, nor which keys anything
inside it has, because the check above is never applied to it at all, so both
halves of it are answerable: the named key is a place that holds an object or
holds nothing, and the rest of the dict is an ordinary container whose new
entry is copied from what its own entries look like.

**Where an element is added, an object is made where one is declared.**
`placing` is where that happens, because the model's own configuration object
gains and loses the real objects as the buffer gains and loses their values.

**Holding nothing is not a matter of elements.** A member that may hold no
value, and a place that holds one configuration object or none, move between
those two states by the choice of a type (section 4.12 of
`doc/detailed_design.md`), so the controls offered here are about elements
and entries alone.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Container, Iterable, Mapping, Sequence
from copy import deepcopy
from io import StringIO
from typing import NamedTuple, Optional, TextIO
from config_as_json import ConfigNesting, ConfigNestingKind, ConfigPath, \
    JsonType, ParseConverter
from edit_cfg_json.converting import node_converters
from edit_cfg_json.dict_check import DictCheck, dict_check, dict_shape, \
    keys_checked
from edit_cfg_json.loader import ConfigSource
from edit_cfg_json.member_types import KeptTypes, node_types, nothing_allowed
from edit_cfg_json.placing import new_object
from edit_cfg_json.tree import ConfigNode, by_key_nestings, member_nestings, \
    member_values, omitted_paths
from edit_cfg_json.type_choice import NodeFacts, offered_types
from edit_cfg_json.type_options import TypeOption, choosable, \
    empty_option_value, fits, held_option, kept_choice, value_option

BUILD_ERRORS = (AttributeError, KeyError, TypeError, ValueError)
"""Every way in which constructing a configuration class can fail.

A class that needs a constructor argument this library knows nothing about
raises `TypeError`, one that declares no public member raises `AttributeError`,
and declared values that a validator refuses raise a `ValueError` subclass.
`NotImplementedError` is deliberately not one of them, for the same reason as
in the validation of a buffer: it says the configuration class is incomplete,
which is a defect of the application that no editing can put right.
"""

NO_PATTERN = ('Nothing says what an element of this member would be: this '
              'class declares no element for it, it holds none, and its '
              'declared type names nothing the editor can make one of.')
"""What a list nothing says anything about says instead of growing.

It is the one case that design section 11 of `doc/detailed_design.md` puts out
of scope for good rather than for now, because the missing thing cannot be
supplied by any amount of work here: only the application knows what an element
of its own list looks like, and a member it never gave one for and never
declared a type for has never said. A member with an ordinary annotation is
answered by that annotation and never reaches this.
"""

NO_CLASS_FORM = ('The editor cannot construct {name} on its own, so it has '
                 'nothing to add here.')
"""What a container of objects says when their class cannot be constructed.

`config_as_json` asks a nested class for the constructor that it builds one
with while it parses, so this is a class that could not be read from a file
either. It is said here rather than found out when the control is pressed,
because a control that refuses every press is worse than no control.
"""

FIXED_KEYS = ('The keys of this dict are the ones its class declares, and '
              'the configuration class checks them while it parses, so a '
              'dict that gained or lost one would be refused.')
"""What a dict the declared-keys check reaches says instead of growing.

`Config.check_dict_parse` matches such a dict against the keys the class
declares for it, so one that gained or lost a key would be refused by
`config_as_json` itself on the next validation pass. The editor says so rather
than offering a control that produces a refusal. Which dicts the check reaches
is `_holds_elements`, and a dict it does not reach is offered the entry
instead of this sentence.
"""

BY_KEY_PATTERN = ('Every key of this dict that no declaration names holds an '
                  'ordinary value, and nothing says what one would be: this '
                  'class declares no such entry for it, it holds none, and '
                  'its declared type names nothing the editor can make one '
                  'of.')
"""What a dict with named objects in it says instead of gaining a key.

It is `NO_PATTERN` for the half of such a member that is not declared: the
declared keys of it are answered by the class each of them names, and every
other key holds an ordinary value that only the application can have said
anything about. A member that says this can still be given the objects its
declarations name, at the row of each of those keys.
"""

NO_ENTRY_PATTERN = ('Nothing says what an entry of this dict would be: this '
                    'class declares none for it, it holds none, and its '
                    'declared type names nothing the editor can make one of.')
"""What a dict whose keys nothing checks says instead of gaining one.

It is `NO_PATTERN` for a dict, and it is reached by every dict the
declared-keys check does not reach and that has no declared key of its own:
the keys of such a dict are the application's own to decide, so the editor
offers an entry as soon as anything says what one would hold, and says this
where nothing does. `BY_KEY_PATTERN` is the same sentence for a member that
has declared keys beside the entries.
"""

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
    dict where one named key of it does and something can be copied for the
    rest.
    """

    keyed: bool = False
    """Whether adding here needs a key that only the user can give.

    A new entry of a dict has to be called something, and nothing but the
    person configuring the application knows what. The two backends ask, each
    in the way its own toolkit asks a question, and a list is never keyed
    because an element of a list is addressed by where it is.
    """

    remove: bool = False
    """Whether removing this node is something the user may ask for.

    An element of a list and an entry of a dict whose keys its class does not
    check can be taken out of what holds them. A member, and a key that a
    `DICT_VALUE_BY_KEY` declaration names, are not elements of anything: one
    that may hold nothing is put back to holding nothing by choosing `None` as
    its type, and keeps its row.
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

    by_key: Mapping[ConfigPath, ConfigNesting]
    """What each object declares about one key of a dict, by that path.

    It is the declaration that is about a key inside a member rather than
    about the member itself, so it is asked for by the path of that key and
    the mapping above answers for the member holding it.
    """

    check: DictCheck
    """What says where the check of the dicts of a file reaches."""

    converters: Mapping[ConfigPath, ParseConverter]
    """One parse converter per node of the tree that has one."""

    omitted: frozenset[ConfigPath]
    """Every node that the file holds no key for while it holds nothing.

    A member its own class may leave out is one, and a key that a class
    declared a configuration object at is the other. No converter is ever
    asked about either while it holds nothing.
    """

    declared: Mapping[ConfigPath, tuple[TypeOption, ...]]
    """The types the class owning each node declares it to hold."""

    types: Mapping[ConfigPath, tuple[TypeOption, ...]]
    """The types each node is offered, those its class would refuse left out.

    It is what says what an element of a list its class declares empty would
    be.
    """

    refusals: Mapping[ConfigPath, tuple[str, ...]]
    """Why each declared type that a node is not offered is left out."""

    nothing: frozenset[ConfigPath]
    """Every node for which holding nothing is a state rather than a value.

    `member_types.nothing_allowed` is what says which nodes those are.
    """

    held: Mapping[ConfigPath, TypeOption]
    """The type each node whose type the user chooses holds, by its path.

    It is what says what an element of a container of a chosen type is, where
    the value cannot: `[]` is a `list[str]` and a `list[list[str]]`.
    """

    defaults: Mapping[str, JsonType]
    """The values that the class of the configuration declares.

    They are one of the three places a new element of an ordinary list is
    copied from, and they are empty for a class the editor could not construct
    at all. That costs such a configuration this one place and nothing else: a
    list that already holds an element, or whose member the class annotated, is
    offered one all the same.
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
    4 of section 3 of `doc/detailed_design.md`: what the editor cannot find out
    it does without, and here that costs the offer to grow an ordinary list and
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
               defaults: Mapping[str, JsonType], kept: KeptTypes) -> TreeFacts:
    """Return everything that saying what one tree offers needs.

    Args:
        nodes: Every configuration object of the tree, by its path.
        flat: The path and the value of every node, in row order.
        defaults: The values that the class of the configuration declares.
        kept: The types the user chose before these rows were built, and
            whether a validation pass is what they are built from.

    Returns:
        The facts that one offer per node is made from.
    """
    values = dict(flat)
    converters = node_converters(nodes=nodes, flat=flat)
    omitted = omitted_paths(nodes)
    check = dict_check(nodes)
    made: dict[ConfigNesting, Optional[JsonType]] = {}
    declared = node_types(nodes=nodes, flat=flat, kept=kept)
    offered = {path: offered_types(options=options, facts=NodeFacts(
        value=values[path], converter=converters.get(path),
        omitted=path in omitted, holds_dict=dict_shape(path=path, check=check),
        placed=_placed(node=nodes.get(path), made=made)))
        for path, options in declared.items()}
    types = {path: offer.offered for path, offer in offered.items()}
    return TreeFacts(values=values, nodes=nodes,
                     nestings=member_nestings(nodes),
                     by_key=by_key_nestings(nodes), check=check,
                     converters=converters, omitted=omitted, declared=declared,
                     types=types,
                     refusals={path: offer.refusals
                               for path, offer in offered.items()},
                     nothing=frozenset(path for path, options in types.items()
                                       if nothing_allowed(options)),
                     held=_held_types(types=types, values=values, kept=kept),
                     defaults=defaults, made=made)


def _placed(node: Optional[ConfigNode],
            made: dict[ConfigNesting, Optional[JsonType]]) -> Optional[bool]:
    """Return whether one node can hold the object declared at it.

    It is None for a node where no object is declared, and otherwise whether
    one is there or the class the declaration names can be constructed, which
    is what choosing that class at the node would do.
    """
    if node is None:
        return None
    return node.config is not None or node.nesting is None or \
        _declared_object(nesting=node.nesting, made=made) is not None


def _held_types(types: Mapping[ConfigPath, tuple[TypeOption, ...]],
                values: Mapping[ConfigPath, JsonType],
                kept: KeptTypes) -> dict[ConfigPath, TypeOption]:
    """Return the type each node whose type the user chooses holds.

    A node that has just appeared holds the first type its value fits, one
    that was there keeps the type it held, and a validation pass that left a
    node a value its type does not fit makes the value say which type it
    holds, as `type_options.kept_choice` says.
    """
    found = ((path, kept_choice(options=options, value=values[path],
                                chosen=kept.chosen.get(path),
                                refreshing=kept.refreshing))
             for path, options in types.items() if choosable(options))
    return {path: held for path, held in found if held is not None}


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
    return _extending(path=path, facts=facts)._replace(
        remove=_element_of(path=path, facts=facts) is not None,
        earlier=_movable(path=path, facts=facts, later=False),
        later=_movable(path=path, facts=facts, later=True))


def _extending(path: ConfigPath, facts: TreeFacts) -> ElementOffer:
    """Return whether one node can be given an element, and why not.

    A node where a class declared an object is a configuration of its own or
    a place holding none, and neither holds elements: the members of a
    configuration are the ones its class declares, and a place is given its
    object by choosing its class as its type.
    """
    if path in facts.nodes:
        return ElementOffer()
    value = facts.values[path]
    if isinstance(value, list):
        return _growing_list(path=path, facts=facts, value=value)
    if isinstance(value, dict):
        return _growing_dict(path=path, facts=facts)
    return ElementOffer()


def _growing_list(path: ConfigPath, facts: TreeFacts,
                  value: list[JsonType]) -> ElementOffer:
    """Return whether one list can be given an element, and why not."""
    nesting = facts.nestings.get(path)
    if nesting is not None and nesting.kind is ConfigNestingKind.LIST_ELEMENT:
        return _from_class(nesting=nesting, facts=facts, keyed=False)
    held = (_declared_element(path=path, facts=facts),
            value[0] if value else None)
    pattern = next((one for one in held
                    if _fits_inside(path=path, facts=facts, pattern=one)),
                   None)
    if pattern is None:
        pattern = _typed_element(path=path, facts=facts)
    if pattern is None:
        return ElementOffer(refusal=NO_PATTERN)
    return ElementOffer(extend=True, template=pattern)


def _typed_element(path: ConfigPath, facts: TreeFacts) -> Optional[JsonType]:
    """Return the empty value that the type of one list says an element is.

    It is asked last, after the class has been asked for an element to copy
    and the member for one of its own, because a value the application wrote
    says more about what belongs in that list than its kind does. It is what
    makes a list that its class declares empty growable at all, which is the
    case design section 11 of `doc/detailed_design.md` had put out of scope
    while the kind of an element was unknowable.
    """
    first = value_option(_inside(path=path, facts=facts))
    return None if first is None else empty_option_value(first)


def _inside(path: ConfigPath, facts: TreeFacts) -> tuple[TypeOption, ...]:
    """Return the types one element of one container may hold.

    They are what is inside the type the container holds: the one the user
    chose where its type is chosen, because `[]` is a `list[str]` and a
    `list[list[str]]` alike, and the one its value is otherwise.
    """
    held = facts.held.get(path)
    if held is None:
        held = held_option(facts.types.get(path, ()), facts.values[path])
    return () if held is None else held.inside


def _fits_inside(path: ConfigPath, facts: TreeFacts,
                 pattern: JsonType) -> bool:
    """Return whether one value may be copied into one container as an element.

    A container whose type the user chose takes a value of what that type
    holds and nothing else: what the class declares for a `list[str]` is no
    element of the `list[list[str]]` the user chose instead. Every other
    container takes what the application wrote, which says more about what
    belongs in it than its declared kind does.
    """
    if pattern is None:
        return False
    inside = _inside(path=path, facts=facts)
    return path not in facts.held or not inside or \
        any(fits(option, pattern) for option in inside)


def _growing_dict(path: ConfigPath, facts: TreeFacts) -> ElementOffer:
    """Return whether one dict can be given an entry, and why not."""
    nesting = facts.nestings.get(path)
    if nesting is not None and nesting.kind is ConfigNestingKind.DICT_VALUE:
        return _from_class(nesting=nesting, facts=facts, keyed=True)
    if not _holds_elements(path=path, facts=facts):
        return ElementOffer(refusal=FIXED_KEYS)
    return _growing_entries(path=path, facts=facts)


def _growing_entries(path: ConfigPath, facts: TreeFacts) -> ElementOffer:
    """Return whether a dict whose keys nothing checks can gain one.

    Nothing checks which keys it has, for one of the three reasons that
    `_holds_elements` asks about, so a key it never heard of is read back
    exactly as it was written.

    What a new entry holds is therefore the same three questions a list
    element is answered by, asked of the entries that no declaration names: an
    object belongs at the keys that declare one and never beside them, and
    `_validate_dict_by_key` is what refuses it there. Which of the two
    sentences a member with nothing to copy says follows from the same thing:
    one that has declared keys is answered for those and for nothing else.
    """
    named = {entry[-1] for entry in facts.by_key if entry[:-1] == path}
    pattern = _ordinary_entry(path=path, facts=facts, named=named)
    if pattern is None:
        return ElementOffer(refusal=BY_KEY_PATTERN if named
                            else NO_ENTRY_PATTERN)
    return ElementOffer(extend=True, keyed=True, template=pattern)


def _ordinary_entry(path: ConfigPath, facts: TreeFacts,
                    named: Container[str]) -> Optional[JsonType]:
    """Return what an entry of one dict that no declaration names holds."""
    for held in (_at_path(path=path, facts=facts), facts.values[path]):
        found = _first_entry(value=held, named=named)
        if _fits_inside(path=path, facts=facts, pattern=found):
            return found
    return _typed_element(path=path, facts=facts)


def _first_entry(value: JsonType, named: Container[str]) -> Optional[JsonType]:
    """Return the first value of one dict under a key nothing declares."""
    if not isinstance(value, dict):
        return None
    return next((held for key, held in value.items() if key not in named),
                None)


def _from_class(nesting: ConfigNesting, facts: TreeFacts,
                keyed: bool) -> ElementOffer:
    """Return the offer of a node whose elements one class declares."""
    template = _declared_object(nesting=nesting, made=facts.made)
    if template is None:
        return ElementOffer(refusal=NO_CLASS_FORM.format(
            name=nesting.config_type.__name__))
    return ElementOffer(extend=True, keyed=keyed, template=template)


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
    found = _at_path(path=path, facts=facts)
    return found[0] if isinstance(found, list) and found else None


def _at_path(path: ConfigPath, facts: TreeFacts) -> JsonType:
    """Return what the class declares at one path, or None where nothing is."""
    found: JsonType = dict(facts.defaults)
    for step in path:
        found = _step_into(found, step)
    return found


def _step_into(value: JsonType, step: str) -> JsonType:
    """Return what is at one step of one path, or None where nothing is."""
    if isinstance(value, dict):
        return value.get(step)
    if isinstance(value, list) and step.isdigit() and int(step) < len(value):
        return value[int(step)]
    return None


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
    another one. Neither is a key that a class declared an object at: it is
    one key of a dict and it is a place of its own, which is put back to
    holding nothing rather than taken out.
    """
    parent = path[:-1]
    if not parent or parent in facts.nodes or path in facts.by_key:
        return None
    held = facts.values.get(parent)
    if isinstance(held, list):
        return held
    if isinstance(held, dict) and _holds_elements(parent, facts):
        return held
    return None


def _holds_elements(path: ConfigPath, facts: TreeFacts) -> bool:
    """Return whether the entries of one dict are elements of it.

    They are wherever the check that matches a dict against the keys its class
    declares does not reach that dict, or reaches it and returns there. That
    check is `Config.check_dict_parse`, and `dict_check.keys_checked` is where
    it is asked whether it reaches one dict: not inside a member named in
    `nested_configs()`, which `config_as_json` reads whole, not past a place
    named in `_unchecked_dicts`, and not below a list.

    It is one question rather than three, because adding an entry and taking
    one out are the same question about the same dict: a dict that can gain a
    key can lose one, and the sentence that says why neither is offered is
    about the check that refuses both.
    """
    return not keys_checked(path=path, check=facts.check)


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


def checked_key(offer: ElementOffer, value: JsonType, key: str,
                name: str) -> None:
    """Refuse a key that cannot name the new element of one container.

    Args:
        offer: What that container offers, which says whether it is keyed.
        value: Value of the container as it is now.
        key: Name that the new entry was asked to have.
        name: What the container is called, for the message.

    Raises:
        ValueError: A list was given a key, a dict was given none, or the key
            is one that dict already holds. The last of those is a refusal and
            not a replacement: a new entry that quietly overwrote an existing
            one would lose what the user had.
    """
    if not offer.keyed:
        if key:
            raise ValueError(KEY_UNWANTED.format(name=name))
        return
    if not key:
        raise ValueError(KEY_NEEDED.format(name=name))
    if isinstance(value, dict) and key in value:
        raise ValueError(KEY_TAKEN.format(name=name, key=key))


def refused(offered: bool, form: str, name: str) -> None:
    """Raise the refusal of one change that a node does not offer.

    Args:
        offered: Whether the node offers it after all.
        form: Form of the message that says it does not.
        name: What the node that was asked is called.

    Raises:
        ValueError: The node does not offer that change.
    """
    if not offered:
        raise ValueError(form.format(name=name))
