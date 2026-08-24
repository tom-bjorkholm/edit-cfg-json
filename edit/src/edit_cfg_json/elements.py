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
a dict whose keys the application decides with validators of its own is a key
policy that this version does not serve. Each of those is a sentence below
that member, in the same place and under the same toggle as everything else
explanatory.

**A member whose values are of two kinds is asked twice.** A
`DICT_VALUE_BY_KEY` declaration names one key of a dict that holds a
configuration object, and every other key of that dict holds an ordinary
value. Nothing checks which keys such a member has, because a member named in
`nested_configs()` never reaches the check above, so both halves of it are
answerable: the named key is a place that holds an object or holds nothing,
and the rest of the dict is an ordinary container whose new entry is copied
from what its own entries look like.

**Where an object is added, an object is made.** `placing` is where that
happens, because the model's own configuration object gains and loses the real
objects as the buffer gains and loses their values.

**How a member is written is not what decides whether it can be cleared.** A
member the class leaves out of the file while it holds nothing has a row all
the same, which `tree.shown_values` gives it, and so has a named key the dict
has not got, which `tree.shown_entries` gives it; putting either of them back
to holding nothing is therefore not a way of losing it. What the class does
decide is what a value of it would be: a declared object for a place that
holds one, and the emptiest value of its kind for a member declared to allow
no value.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Container, Iterable, Mapping, Sequence
from copy import deepcopy
from io import StringIO
from typing import NamedTuple, Optional, TextIO
from config_as_json import ConfigNesting, ConfigNestingKind, ConfigPath, \
    JsonType
from edit_cfg_json.leaf_value import LeafType, empty_value
from edit_cfg_json.loader import ConfigSource
from edit_cfg_json.member_types import node_types
from edit_cfg_json.placing import new_object
from edit_cfg_json.tree import ConfigNode, by_key_nestings, member_nestings, \
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

ENTRY_KINDS = (ConfigNestingKind.DICT_VALUE,
               ConfigNestingKind.DICT_VALUE_BY_KEY)
"""The declarations of a dict member whose keys its own class does not check.

`Config.check_dict_parse` is what matches an ordinary dict member against the
keys its class declares, and a member named in `nested_configs()` never
reaches it: `config_as_json` reads such a member whole instead. So an entry of
one of these can be taken out of it and another one put in. A member of
`_unchecked_dicts` is the other dict whose keys nothing here checks, and it is
left out for a different reason: its keys are the application's own to decide.
"""

CLEARED_KINDS = (ConfigNestingKind.OPTIONAL_MEMBER,
                 ConfigNestingKind.DICT_VALUE_BY_KEY)
"""The declarations of a place that holds one object or holds nothing.

They are the two that have the pair of states of design section 4.9 of
`doc/design.md`: a member that may hold none, and a named key that the file
need not have. `MEMBER` holds one always, and `LIST_ELEMENT` and `DICT_VALUE`
are about everything inside a member rather than about one place in it.
"""

NO_PATTERN = ('Nothing says what an element of this member would be: this '
              'class declares no element for it, it holds none, and its '
              'declared type names nothing the editor can make one of.')
"""What a list nothing says anything about says instead of growing.

It is the one case that design section 11 of `doc/design.md` puts out of scope
for good rather than for now, because the missing thing cannot be supplied by
any amount of work here: only the application knows what an element of its own
list looks like, and a member it never gave one for and never declared a type
for has never said. A member with an ordinary annotation is answered by that
annotation and never reaches this.
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

NO_DICT_YET = ('A dict written for a member that holds none is refused by '
               'the configuration class itself, which matches it against the '
               'dict the member holds. So this member cannot be given one.')
"""What a member declared to allow no value says instead of taking a dict.

`Config.check_dict_parse` refuses a dict written for a member whose value is
not one — *Unexpected dictionary for X in JSON data* — whatever keys it has and
even where it has none, so the empty dict of design section 4.2 of
`doc/design.md` is the one kind of value that such a member cannot be given.
It is the first bullet of section 4.9 one step up: what refuses a dict here is
the same check that refuses a new key of one, and offering the control anyway
would be offering one that produces a refusal.
"""

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
    class says that every value in it is a configuration object, for a dict
    where one named key of it does and something can be copied for the rest,
    and for a declared place that holds no object yet, where adding is making
    the one object that place is for.
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
    check can be taken out of what holds them. A declared place that holds an
    object, and a member that its class declared to allow no value, are put
    back to holding nothing instead, which `cleared` is what says. How the
    class writes such a member is not asked: one it leaves out of the file
    altogether keeps its row, which says that it holds nothing and offers to
    give it something.
    """

    cleared: bool = False
    """Whether removing puts this node back to holding nothing.

    The two ways of removing something differ in what is left behind, and the
    difference is not visible in the row: a declared place keeps its row and
    holds nothing, and an element of a container is gone. A declared key of a
    dict is the case that needs both to be said, because it is a place that
    keeps its row while being one key of a container beside the ordinary keys
    that are taken out of it.
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

    unchecked: frozenset[ConfigPath]
    """Every dict member whose keys its own class does not check."""

    types: Mapping[ConfigPath, LeafType]
    """What the class owning each node says the value there is.

    It is what a member allowed to hold nothing is known by, and what says
    what an element of a list its class declares empty would be.
    """

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
                     by_key=by_key_nestings(nodes),
                     unchecked=unchecked_members(nodes),
                     types=node_types(nodes=nodes, flat=flat),
                     defaults=defaults, made={})


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
    cleared = _clearable(path=path, facts=facts)
    return offer._replace(
        remove=cleared or _element_of(path=path, facts=facts) is not None,
        cleared=cleared, earlier=_movable(path=path, facts=facts, later=False),
        later=_movable(path=path, facts=facts, later=True))


def _extending(path: ConfigPath, facts: TreeFacts) -> ElementOffer:
    """Return whether one node can be given an element, and why not.

    A node where a class declared an object and none is there is the one node
    that is grown without being a container: adding there is making the object
    that the place is for, which design section 4.1 of `doc/design.md` says
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
    return _new_value(path=path, facts=facts)


def _new_value(path: ConfigPath, facts: TreeFacts) -> ElementOffer:
    """Return whether a member that holds nothing can be given a value.

    A member whose class declares that it may hold nothing has two states, and
    moving between them is the same pair of actions as making and clearing the
    object of a member declared to hold one: adding is giving it a value of
    the kind its declaration names, and removing is putting it back to holding
    none. That is what settles the open question at the end of design section
    4.2 — the user chooses between the states the class allowed, and never
    what kind of value the member is for.

    A member declared to hold a dict is the one that cannot be given a value,
    for the reason `NO_DICT_YET` gives: the class refuses a dict written for a
    member that holds none, so the control would be one that produces a
    refusal.
    """
    declared = facts.types.get(path, LeafType())
    if facts.values[path] is not None or not declared.nothing:
        return ElementOffer()
    if declared.kind is dict:
        return ElementOffer(refusal=NO_DICT_YET)
    return ElementOffer(extend=True, template=empty_value(declared.kind))


def _new_object(path: ConfigPath, facts: TreeFacts) -> ElementOffer:
    """Return whether a declared place holding no object can be given one.

    Two declarations reach this. An `OPTIONAL_MEMBER` does, whether its class
    writes `null` for the member or leaves it out of the file, and so does a
    key that `DICT_VALUE_BY_KEY` names and the dict has not got. Every other
    kind says that the member holds an object or a container of them, and
    `config_as_json` refuses such a member holding nothing while it validates,
    so no configuration the editor is given has one.
    """
    nesting = _declared_place(path=path, facts=facts)
    if nesting is None:
        return ElementOffer()
    return _from_class(nesting=nesting, facts=facts, keyed=False)


def _declared_place(path: ConfigPath,
                    facts: TreeFacts) -> Optional[ConfigNesting]:
    """Return what declares one node to hold a configuration object.

    A member is declared by the class that owns it and a named key of a dict
    by the same class one step further in, and the two cannot be the same
    node: a member is one step below the object that declares it and a named
    key is two.
    """
    return facts.nestings.get(path) or facts.by_key.get(path)


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
    case design section 11 of `doc/design.md` had put out of scope while the
    kind of an element was unknowable.
    """
    inside = facts.types.get(path, LeafType()).inside
    return None if inside is None else empty_value(inside.kind)


def _growing_dict(path: ConfigPath, facts: TreeFacts) -> ElementOffer:
    """Return whether one dict can be given an entry, and why not."""
    nesting = facts.nestings.get(path)
    kind = None if nesting is None else nesting.kind
    if kind is ConfigNestingKind.DICT_VALUE:
        assert nesting is not None
        return _from_class(nesting=nesting, facts=facts, keyed=True)
    if kind is ConfigNestingKind.DICT_VALUE_BY_KEY:
        return _growing_by_key(path=path, facts=facts)
    if _member_path(path=path, facts=facts) in facts.unchecked:
        return ElementOffer(refusal=UNCHECKED_SCOPE)
    return ElementOffer(refusal=FIXED_KEYS)


def _growing_by_key(path: ConfigPath, facts: TreeFacts) -> ElementOffer:
    """Return whether a dict with named objects in it can gain a key.

    Nothing checks which keys it has: `config_as_json` reads such a member
    whole, parsing the keys its declarations name as the classes they name and
    keeping every other key as the ordinary value it is, so a key it never
    heard of is read back exactly as it was written. What a new one of those
    holds is therefore the same three questions a list element is answered by,
    asked of the entries that no declaration names: an object belongs at the
    keys that declare one and never beside them, and `_validate_dict_by_key`
    is what refuses it there.
    """
    pattern = _ordinary_entry(path=path, facts=facts)
    if pattern is None:
        return ElementOffer(refusal=BY_KEY_PATTERN)
    return ElementOffer(extend=True, keyed=True, template=pattern)


def _ordinary_entry(path: ConfigPath, facts: TreeFacts) -> Optional[JsonType]:
    """Return what an entry of one dict that no declaration names holds."""
    named = {entry[-1] for entry in facts.by_key if entry[:-1] == path}
    for held in (_at_path(path=path, facts=facts), facts.values[path]):
        found = _first_entry(value=held, named=named)
        if found is not None:
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


def _member_path(path: ConfigPath, facts: TreeFacts) -> ConfigPath:
    """Return the path of the member of a configuration one node is in.

    A node is inside exactly one member of exactly one configuration object,
    and that member is what a class says its key policy about: a dict inside a
    dict of an unchecked member is unchecked with it, because the check that
    `_unchecked_dicts` takes away stops at the member rather than recursing.
    """
    owner = owner_path(path=path, nodes=facts.nodes)
    return path[:len(owner) + 1]


def _clearable(path: ConfigPath, facts: TreeFacts) -> bool:
    """Return whether removing one node puts it back to holding nothing.

    A member declared to allow no value is cleared by the same rule as a place
    declared to hold a configuration object, and neither of them asks how its
    class writes what it clears. A member that `_omit_none_from_json()` names
    is left out of the file altogether, and a key that `DICT_VALUE_BY_KEY`
    names is simply not there; each of them keeps a row all the same, so
    clearing it is not a way of losing it: the row then says that it holds
    nothing, exactly as it does for the member its class writes `null` for.

    A node that a class declared is answered by that declaration alone, and
    never by the type its member is annotated with. A nesting kind that
    `CLEARED_KINDS` leaves out can never hold nothing — `config_as_json`
    requires the list or the dict while it validates — so an annotation
    allowing it says something no configuration the editor is given is in.
    """
    declared = _declared_place(path=path, facts=facts)
    if declared is not None:
        node = facts.nodes.get(path)
        return declared.kind in CLEARED_KINDS and node is not None \
            and node.config is not None
    return facts.types.get(path, LeafType()).nothing \
        and facts.values[path] is not None


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

    They are wherever the class of the configuration declared the member in
    `nested_configs()`, because such a member never reaches the check that
    matches an ordinary dict against the keys its class declares.
    """
    nesting = facts.nestings.get(path)
    return nesting is not None and nesting.kind in ENTRY_KINDS


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
