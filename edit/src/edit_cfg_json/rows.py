#! /usr/bin/env python3
"""One row of the editor, and the rows of one whole configuration.

A row is one node of the tree that `tree` takes a configuration apart into: a
member of the configuration, or a value inside a list or a dict that one of
its members holds. Every row is addressed by its path, and the rows of a
configuration are one mapping by path in the order they are shown.

The rows are built twice in the life of a model. They are built when the model
is built, from the values the load produced, and they are built again after a
validation pass, from the values the pass accepted: a member validator returns
the value that is stored back into the member, and one that normalizes a list
can change how many values it holds. What the earlier rows knew is carried
over, which is what makes the second build a refresh rather than a new session.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Container, Mapping, Sequence
from types import MappingProxyType
from typing import NamedTuple, Optional
from config_as_json import Config, ConfigPath, JsonType, ParseConverter
from edit_cfg_json.converting import node_converters
from edit_cfg_json.descriptions import Descriptions, MemberFacts, \
    member_description
from edit_cfg_json.elements import ElementOffer, element_offers, tree_facts
from edit_cfg_json.leaf_value import LeafType, NO_VALUE_TEXT, leaf_kind, \
    value_as_text, values_differ
from edit_cfg_json.loading import LoadReport
from edit_cfg_json.tree import ConfigNode, NO_OBJECT_FORM, child_values, \
    config_nodes, container_text, flat_values, is_container, omitted_paths, \
    ordered_names
from edit_cfg_json.validation import SubtreeAnswer

NOT_A_MEMBER = ''
"""What a node that is not a member of the configuration is named by.

The declared defaults and the records of a load are both about a member of the
configuration and never about one value inside one, so every node below a
member is looked up under this. No member has it for a name, so it cannot
collide with one, and the lookups are then one form rather than a condition
each.
"""


class MemberRow(NamedTuple):
    """One node of the configuration as it appears in the JSON file."""

    path: ConfigPath
    """Path that addresses this node in the model.

    A member of the configuration has one step. A value inside a list or a
    dict that a member holds has the steps of that member and then its own,
    which is the index of a list element written out or the key of a
    dictionary entry. It is the same path that the description mapping names
    a member by, so a description of every element of a list is written with
    the `'['` step and reaches each of them.
    """

    value: JsonType
    """Current value of the node in JSON space, as the user edits it.

    A container holds what its children hold, and it is kept that way as they
    are edited, so that the whole configuration is what the members of the
    model say it is and a folded container cannot hide a change.
    """

    original: JsonType
    """Value that this node had when the file was last agreed with.

    That is when the model was built, and again after every save: what has
    just been written is what there is no longer anything to save about, so a
    save makes the written value the one the buffer is compared against.

    It is what the current value is compared against, and it is the type
    information of every node whose declaration says nothing. Reading the type
    from the current value instead would not work: a number member that the
    user has half typed holds text for as long as the text is not a number
    yet, and the member would then stop being a number member. A save is safe
    to move it to, because only a validated value is ever written.
    """

    children: Optional[tuple[ConfigPath, ...]] = None
    """Paths of the nodes inside this one, or None for a node with none.

    An empty tuple is a list or a dict that holds nothing, which is a
    different thing from a value: it can be folded, it says how much it holds,
    and this version of the editor cannot put anything into it.

    A declared nested configuration object has the paths of its own members
    here, in the order its own class declares them, because it is a node with
    members and not the dictionary it happens to serialize as. It is None for
    such a member that holds no object at all, which an `OPTIONAL_MEMBER` does.
    """

    config_type: Optional[type[Config]] = None
    """Class of the nested object here, None for every other node.

    It is what makes a nested configuration object something other than the
    dict it serializes as: the row says the class instead of how many entries
    there are, and the docstring of that class is what is said below the row.

    It is set for a member that holds no object as well, because the class it
    would hold is worth saying and is the whole of what is known about it.
    """

    folded: bool = False
    """Whether this container is folded, so that its rows are not shown.

    It is always false for a node that holds nothing, because there would be
    nothing for folding it to hide. A container that the editor opened folded
    is one that would have added more rows than the window can spare, and
    every other container starts open: what an application put in its
    configuration was put there to be read.
    """

    shown: bool = True
    """Whether this node is on the screen as things stand.

    A node is hidden when any container it is inside has been folded away.
    Its own fold says how much of it is shown and not whether it is: a folded
    container is still a row, and it is the row the user presses to open it
    again.

    It is carried by the row rather than worked out by each backend, so that
    two backends cannot disagree about what folding a container hides.
    """

    changed_by_validator: bool = False
    """Whether a validation pass rewrote this value.

    A validation pass sets the flag and the next edit of this member clears
    it, so it always answers the same question: is the value shown here
    something a validator made of what was typed? It belongs to the model
    rather than to a backend, so that two backends cannot show it
    differently.
    """

    filled_from_default: bool = False
    """Whether the declared defaults supplied this value.

    It is set when a load that was allowed to use the defaults filled in a
    member the input file did not hold, and it stays set for the rest of the
    session: that the file did not hold this value remains true whatever the
    user then types into it. It belongs to the model for the same reason as
    the flag above, so that two backends cannot show it differently.

    Only a member of the configuration carries it, because the declared
    defaults supply a whole member and never one value inside one.
    """

    load_reason: str = ''
    """What reading the input file did to this member, empty when nothing.

    Reading a file is not always only reading it. A class that declares rules
    for reading an older format may have supplied this value or renamed a key
    of the file into this member, and parsing or validating may have
    normalized what the file held. The user has to be told, because the value
    shown is then not the value in the file.

    It says which of those things happened wherever the load recorded it, and
    says that the value is not the file's where it did not, which is the whole
    of what a comparison can know. It stays as it is for the rest of the
    session, exactly as the flag above does and for the same reason, and the
    two are never both there: what the declared defaults filled in is said by
    that flag, which says more than this would.

    Only a member of the configuration carries it, for the same reason as the
    flag above: what the load recorded is recorded for a member, and a record
    about a value inside one is a record about that member.
    """

    description: str = ''
    """What is said about this node, empty when nothing is.

    The application says most of it, in the description mapping, and the type
    of the node says the rest: the names an enum accepts, or what kind of
    value it holds, and whether the class that owns it may leave it out of the
    file. It is read whenever the rows are built, because it says what the node
    is for and that does not change while it is edited.

    A container is described by the application or not at all: the row of a
    container already says how much it holds, and the rows below it say what
    each of them is.

    The docstring of a nested configuration object is deliberately not here.
    How much of it is shown depends on whether that node is open, and what a
    row says about itself cannot depend on that: `row_description` is where
    the two are put together.
    """

    converter: Optional[ParseConverter] = None
    """How the text of this node becomes the value that is stored in it.

    It is None for a node that holds what the file holds, which is most of
    them. It is what says that a node holds an enum, and that answers two
    questions: which names the description of the node lists, and whether the
    text the field holds means a value of it at all.

    A value inside a list never has one, because `config_as_json` applies a
    parse converter to the values of a dictionary and to nothing else.
    """

    conversion: str = ''
    """Why the text of this node means no value of it, empty when it does.

    It is answered by this node alone, which is what makes it a different
    thing from what a validation pass says about it: it stays true until this
    node is edited again, whatever happens to the rest of the buffer. It is
    set when the user leaves the field and again by every validation pass, and
    the next edit of this node clears it.
    """

    subtree_valid: Optional[bool] = None
    """Whether the object here is a configuration on its own, None if unasked.

    It is set for a declared nested configuration object and for nothing else,
    because nothing else is a configuration that can be asked about itself. A
    list, a dict and an ordinary value have no class of their own to ask, and a
    declared member holding no object has no object to ask.

    None is a third state rather than a kind of failure, exactly as it is for
    the verdict of the whole configuration: this object has not been asked
    since something inside it last changed. It is answered by folding the node
    or opening it, and by every validation pass, and an edit anywhere inside it
    takes the answer away again.

    It says nothing about whether the configuration could be saved, and it is
    deliberately not the same question: a rule of the class above may relate
    two of these objects across the boundary between them, so both of them can
    be valid on their own while the configuration holding them is refused.

    A list or a dict of such objects carries it too, and there it is about the
    objects inside rather than about the container, which is no configuration
    and has nothing to say about itself. It is false as soon as one of them is
    refused, true once every one of them has been asked and accepted, and None
    while any of them is unasked and none is refused. Folding such a member
    hides every object in it, so folding it asks every object in it.
    """

    subtree_refusal: str = ''
    """Why the object owning this node refused it, empty when it did not.

    It is what asking one nested configuration object about itself found, kept
    at the node that answer was about: a member of that object where a member
    validator refused one, and the object itself where its class refused it
    for a reason that is about no member of it.

    It is a third thing beside the two that `conversion` and the verdict of the
    whole configuration answer, because it lives for a third length of time. A
    conversion is answered by one node alone and stays true until that node is
    edited; a verdict is dropped by any edit anywhere; and this is dropped by
    an edit inside the object it came from and by nothing else, which is the
    same lifetime as the state above it and for the same reason.
    """

    has_objects: bool = False
    """Whether a configuration object is at this node or inside it.

    A nested configuration object has it, and so does a list or a dict that
    holds them, at any depth. It is what a backend asks before it creates the
    widget that says what those objects are: a widget which could never hold
    anything is a piece of the window spent on nothing.

    A member declared to hold an object and holding none has it false, because
    there is no object there to ask about.
    """

    found: bool = False
    """Whether this is the node that the search has got to.

    A search is what a configuration too big for a window needs, and what it
    reaches is one node at a time: this is that node, and every other node of
    a search that reaches several of them says nothing. It is written onto the
    rows rather than carried by them, exactly as the fold state is, because a
    search outlives the rows that a validation pass replaces.
    """

    declared: LeafType = LeafType()
    """What the class that owns this node says the value here is.

    A member of a configuration is declared by the class that owns it, and
    what the declaration says is read from the attribute type rather than from
    the value: `self.ratio: float = 0` is a number member however its default
    is written, and `self.title: Optional[str] = None` is a text member that
    may hold nothing while it holds nothing at all. A value inside a list or a
    dict is answered by what the declaration of the member says is inside it.

    It is empty wherever nothing says anything, which is a member with no
    annotation, a class whose source cannot be read, and an annotation naming
    a class of the application's own. The value the node held is what answers
    then, exactly as it always did.
    """

    offer: ElementOffer = ElementOffer()
    """What can be done here about how many things this node holds.

    Whether an element can be added, whether this node is an element that can
    be taken out of what holds it, whether it can change places with a
    neighbour, and why none of that is offered where none of it is. Most nodes
    offer nothing: a value is not something that holds elements, and the
    members of a configuration object are the ones its class declares.

    It belongs to the model rather than to a backend for the same reason the
    fold state does: two user interfaces of one application that offered to
    change different things would be worse than either behaviour.
    """

    @property
    def name(self) -> str:
        """Return the name of the node, the last step of its path."""
        return self.path[-1]

    @property
    def depth(self) -> int:
        """Return how far inside a member of the configuration this is.

        A member of the configuration is at nothing, and a value inside one is
        one step further in for every container it is inside. It is what the
        backends indent a row by.
        """
        return len(self.path) - 1

    @property
    def foldable(self) -> bool:
        """Return whether this node holds rows that can be folded away.

        A list, a dict and a nested configuration object are all one. A
        declared member that holds no object is not: there is nothing below it
        for folding to hide.
        """
        return self.children is not None

    @property
    def is_object(self) -> bool:
        """Return whether a configuration object is really at this node.

        A member declared to hold one and holding none is not, because it has
        a class and no object, and everything the editor asks of such a node
        is asked of the object that is not there.
        """
        return self.config_type is not None and self.foldable

    @property
    def holds_nothing(self) -> bool:
        """Return whether this member is in the state of holding no value.

        A member whose class declares that it may hold nothing has two states
        rather than one, and this is the second of them. It is not a value
        being typed and it is not a value of the wrong kind: it is the member
        holding nothing, which is what the class allowed it to do, and it is
        told apart from an empty text by being a state and not a text.

        Which state it is in is changed by the two controls that change how
        many things a node holds and by nothing else, so a field can never
        take itself away from under the cursor that is typing in it.
        """
        return self.value is None and self.declared.nothing

    @property
    def editable(self) -> bool:
        """Return whether this node is a value that can be edited.

        A list, a dict and a nested configuration object are all structure
        rather than a value, so none of them is edited in a field: each of
        them is edited through the rows below it. A declared member that holds
        no object is not edited either, because no text typed into a field
        becomes a configuration object, and neither is a member that holds
        nothing, because the value it would hold is asked for and not typed.

        The rows below it are asked as well as the value it was compared
        against, because a member that may hold nothing held nothing then and
        holds a list of rows now. Neither of them is the value it holds this
        moment, which is what every keystroke changes: text that happens to be
        JSON for a list would otherwise take the field away while it was being
        typed.
        """
        return not self.foldable and not is_container(self.original) \
            and self.config_type is None and not self.holds_nothing

    @property
    def kind(self) -> Optional[type]:
        """Return which kind of value this node takes, None where unknown.

        What the class declared wins over what the node held, which is the
        whole of what more type information buys: a member declared `float`
        takes a number however its default was written, and a member that
        holds nothing still says what it would hold.
        """
        return leaf_kind(declared=self.declared, original=self.original)

    @property
    def is_text(self) -> bool:
        """Return whether this node takes text.

        This is the difference between a value that is text and a value
        whose text is a rendering of it. The text of a text value is the
        value itself, while the text of a number is how the number is
        written.
        """
        return self.kind is str

    @property
    def is_bool(self) -> bool:
        """Return whether this node takes true or false.

        It is what makes the two words the values this node takes, so that
        any beginning of either of them is one of them and anything else is
        neither. A node whose kind nothing says is not one of these: nothing
        is known, so nothing is refused.
        """
        return self.kind is bool

    @property
    def edited(self) -> bool:
        """Return whether this node holds something that is not saved yet.

        A node is changed when it would now be written to the file
        differently, and not when it merely was typed in. Typing a value
        back to what it was leaves nothing to save, and an editor that still
        claimed to have changes would be telling the user something untrue.
        Saving says the same thing about every node at once.

        A container answers for everything inside it, because what it holds is
        kept as its children hold it: a change the user cannot see, because
        the container it is in is folded, is still a change.
        """
        return values_differ(self.value, self.original)

    @property
    def value_text(self) -> str:
        """Return the value of this node as the text a field would show.

        A nested configuration object says its class, because that is what it
        is: showing how many entries it serializes to would be showing it as
        the dictionary it is not. A member that holds no object says which
        class is missing, and a member that holds no value says that it holds
        none. A list or a dict says how much it holds, because its value is on
        the rows below it. Every other node shows the text of the value it
        holds.
        """
        if self.config_type is not None:
            return self.config_type.__name__ if self.foldable else \
                NO_OBJECT_FORM.format(name=self.config_type.__name__)
        if self.holds_nothing:
            return NO_VALUE_TEXT
        if is_container(self.value):
            return container_text(self.value)
        return value_as_text(self.value)


class RowContext(NamedTuple):
    """Everything that building the rows of one configuration needs.

    It is one object rather than one argument each, because every one of them
    is read once per node and none of them changes while the rows are built.

    The last three are by path and not by name, because the class that answers
    for a node is the class that owns it: a nested configuration object parses
    its own JSON, applies its own parse converters and decides for itself which
    of its members it may leave out of a file.
    """

    report: LoadReport
    """What reading the input file did beyond reading the values."""

    descriptions: Descriptions
    """What the application says about the members it declares."""

    nodes: Mapping[ConfigPath, ConfigNode]
    """Every configuration object of the tree, by its path.

    The configuration itself is one of them, under the empty path, so a node
    is answered the same way whether it is a member of the configuration or a
    member of something nested inside it.
    """

    converters: Mapping[ConfigPath, ParseConverter]
    """One parse converter per node of the tree that has one."""

    optional: frozenset[ConfigPath]
    """Every node that the file holds no key for while it holds nothing.

    A member its own class may leave out is one, and a key that a class
    declared a configuration object at is the other.
    """

    offers: Mapping[ConfigPath, ElementOffer]
    """What each node offers about the elements it holds, by its path."""

    types: Mapping[ConfigPath, LeafType]
    """What the class owning each node says the value there is."""

    refreshing: bool
    """Whether these rows are what a validation pass left behind.

    A pass is not read only, so a node whose value it changed is marked, and a
    node it created is marked as well: a validator that normalizes a list can
    make one. Every other rebuild is a change the user asked for — an element
    added, removed or moved — and marking that as a validator's work would be
    telling the user that something happened to what they just did.
    """


def _children_of(path: ConfigPath, value: JsonType,
                 node: Optional[ConfigNode]) -> Optional[tuple[ConfigPath,
                                                               ...]]:
    """Return the paths inside one node, or None for a node with none.

    A nested configuration object holds its own members, in the order its own
    class declares them, and not the sorted keys of the dictionary it writes.
    A member that holds no object holds nothing.

    Args:
        path: Path that addresses the node.
        value: JSON space value that the node holds.
        node: What is at that path where a configuration object is declared,
            and None for every ordinary node.

    Returns:
        The path of every child of that node, and None for a value and for a
        declared member that holds no object.
    """
    if node is not None:
        if node.config is None or not isinstance(value, dict):
            return None
        return tuple((*path, name) for name in
                     ordered_names(config=node.config, members=value))
    if not is_container(value):
        return None
    return tuple(child for child, _ in child_values(path=path, value=value))


def _rewritten(was: Optional[MemberRow], value: JsonType,
               refreshing: bool) -> bool:
    """Return whether a validation pass has rewritten one node.

    A mark that an earlier pass set stays until the user edits that node, so
    a second pass over an unchanged buffer does not take it away. A node that
    had no row at all is one that a pass has just created, which a validator
    that normalizes a list does.

    A build that is not a validation pass marks nothing new. The first build
    of a session is one of those, and so is the rebuild after an element has
    been added, removed or moved: what the user asked for is what the rows
    say, and a validator had no part in it.

    Args:
        was: The row of that node before the pass, or None when it had none.
        value: The value the node holds now.
        refreshing: Whether these rows are what a validation pass left behind.

    Returns:
        Whether the row is marked as one a validator wrote.
    """
    if was is None:
        return refreshing
    if not refreshing:
        return was.changed_by_validator
    return was.changed_by_validator or values_differ(value, was.value)


def _row_of(path: ConfigPath, value: JsonType, context: RowContext,
            previous: Mapping[ConfigPath, MemberRow]) -> MemberRow:
    """Return the row of one node of one configuration.

    What the load did is looked up by the name of a member of the
    configuration, because that is what the load recorded it for: a record
    about a value inside a member is a record about that member, and a member
    of a nested configuration object is inside the member that holds it.

    Args:
        path: Path that addresses the node.
        value: JSON space value that the node holds.
        context: What the rows of this configuration are built from.
        previous: The rows as they were before, empty for the first build.

    Returns:
        The row of that node, with what an earlier row knew carried over.
    """
    member = path[0] if len(path) == 1 else NOT_A_MEMBER
    node = context.nodes.get(path)
    converter = context.converters.get(path)
    declared = context.types.get(path, LeafType())
    was = previous.get(path)
    return MemberRow(
        path=path, value=value,
        original=value if was is None else was.original,
        children=_children_of(path=path, value=value, node=node),
        config_type=None if node is None else node.config_type,
        changed_by_validator=_rewritten(was=was, value=value,
                                        refreshing=context.refreshing),
        offer=context.offers[path], declared=declared,
        filled_from_default=member in context.report.filled,
        load_reason=context.report.reasons.get(member, ''),
        description=member_description(
            descriptions=context.descriptions, path=path,
            facts=MemberFacts(value=value, declared=declared,
                              converter=converter,
                              optional=path in context.optional,
                              nested=node is not None)),
        converter=converter, conversion='' if was is None else was.conversion)


# One argument per independent thing that the rows of a configuration are
# built from, which is what keeps every one of them a fact of the session
# rather than something this module works out for itself.
# pylint: disable-next=too-many-arguments
def built_rows(config: Config, *, members: Mapping[str, JsonType],
               report: LoadReport, descriptions: Descriptions,
               previous: Mapping[ConfigPath, MemberRow],
               defaults: Mapping[str, JsonType] = MappingProxyType({}),
               refreshing: bool = False) -> dict[ConfigPath, MemberRow]:
    """Return one row per node of one configuration, in the order shown.

    A mapping by path is what the design asks for, because every node is
    addressed by its path and no other name for it is needed. A dictionary
    keeps the order it was built in, so the order the rows are shown in
    survives being a mapping.

    The configuration object is asked again at every build rather than once,
    because a validation pass hands back the object it accepted and the nested
    configuration objects of that one are the objects that own its values.

    Args:
        config: Configuration object whose values these are. It is not
            modified, and it is what says which nodes are configuration
            objects and in which order each of them declares its members.
        members: One JSON space value per serialized member.
        report: What reading the input file did beyond reading the values.
        descriptions: What the application says about its members.
        previous: The rows as they were before, empty for the first build.
            A node that had a row keeps what that row was compared against
            and is marked when a validation pass changed it; a node that had
            none is a node a validation pass created.
        defaults: The values that the class of the configuration declares,
            which is what a new element of an ordinary list is copied from.
        refreshing: Whether these rows are what a validation pass left behind,
            which is what decides whether a node it changed is marked.

    Returns:
        The rows of that configuration, by path.
    """
    nodes = config_nodes(config)
    flat = flat_values(members=members, nodes=nodes)
    facts = tree_facts(nodes=nodes, flat=flat, defaults=defaults)
    context = RowContext(report=report, descriptions=descriptions, nodes=nodes,
                         converters=node_converters(nodes=nodes, flat=flat),
                         optional=omitted_paths(nodes),
                         offers=element_offers(facts), types=facts.types,
                         refreshing=refreshing)
    return {path: _row_of(path=path, value=value, context=context,
                          previous=previous)
            for path, value in flat}


def _shown(path: ConfigPath, folded: Container[ConfigPath]) -> bool:
    """Return whether one node is shown while those containers are folded."""
    return not any(path[:depth] in folded for depth in range(1, len(path)))


def _objects_below(rows: Mapping[ConfigPath, MemberRow]
                   ) -> dict[ConfigPath, list[ConfigPath]]:
    """Return the configuration objects below each node, by that node's path.

    It is built from the objects outwards rather than asked of each node,
    because a node has few ancestors and a configuration has many nodes: the
    same answer costs one walk up per object instead of one walk over every
    object per row, and these are written again on every keystroke.

    Args:
        rows: The rows of the configuration, by path.

    Returns:
        The path of every object strictly inside one node, for each node that
        has any. A node with none is not a key of it.
    """
    below: dict[ConfigPath, list[ConfigPath]] = {}
    for path, row in rows.items():
        if not row.is_object:
            continue
        for depth in range(len(path)):
            below.setdefault(path[:depth], []).append(path)
    return below


def _state_of(row: MemberRow, held: Sequence[ConfigPath],
              answers: Mapping[ConfigPath, SubtreeAnswer]) -> Optional[bool]:
    """Return what the objects at or inside one node are on their own.

    An object answers for itself. A list or a dict answers for the objects it
    holds: it is refused as soon as one of them is, valid once every one of
    them has been asked and accepted, and unasked while any of them is unasked
    and none is refused. Nothing else has anything to answer.

    Args:
        row: The row of the node to answer for.
        held: The path of every configuration object inside that node.
        answers: What each object that has been asked said about itself.

    Returns:
        What that node says, and None for one that has not been asked and for
        one that can never say anything.
    """
    if row.is_object:
        answer = answers.get(row.path)
        return None if answer is None else answer.valid
    if any(not answers[other].valid for other in held if other in answers):
        return False
    if held and all(other in answers for other in held):
        return True
    return None


class BufferState(NamedTuple):
    """What the buffer knows about the rows rather than about one row.

    Each of these outlives the rows it is about, because the rows are built
    again after every validation pass and after every change of how many
    elements a container holds: what the user folded, what each object said
    about itself and what a search has got to are all older than the rows they
    are written onto.
    """

    folded: Container[ConfigPath]
    """Paths of the containers that are folded away."""

    answers: Mapping[ConfigPath, SubtreeAnswer]
    """What each object that has been asked said about itself, by path."""

    found: Optional[ConfigPath]
    """Path of the node the search has got to, None when it is at none."""


def stamped(rows: Mapping[ConfigPath, MemberRow],
            state: BufferState) -> dict[ConfigPath, MemberRow]:
    """Return the rows with the state of the buffer written onto them.

    A backend reads what is folded, what is shown, what the configuration
    objects amount to and what a search has got to from the row each of those
    is about, exactly as it reads the marks and the description from there, so
    that the two backends cannot fold, hide, judge or find different things.

    They are written here rather than carried by the rows they are about,
    because they belong to the buffer: the rows are built again after every
    validation pass, and a fold the user asked for, an answer an object gave
    and a node a search reached all outlive the rows that were there then.

    Args:
        rows: The rows of the configuration, by path.
        state: What the buffer knows that is written onto them.

    Returns:
        The same rows, each saying whether it is folded, whether it shows,
        what the configuration objects at or inside it are on their own, and
        whether it is the node the search has got to.
    """
    below = _objects_below(rows)
    refused = {path: message for answer in state.answers.values()
               for path, message in answer.refused.items()}
    return {path: _stamped_row(row=row, state=state, held=below.get(path, ()),
                               refusal=refused.get(path, ''))
            for path, row in rows.items()}


def _stamped_row(row: MemberRow, state: BufferState,
                 held: Sequence[ConfigPath], refusal: str) -> MemberRow:
    """Return one row with the state of the buffer written onto it."""
    return row._replace(
        folded=row.path in state.folded,
        shown=_shown(path=row.path, folded=state.folded),
        subtree_valid=_state_of(row=row, held=held, answers=state.answers),
        subtree_refusal=refusal, has_objects=row.is_object or bool(held),
        found=row.path == state.found)
