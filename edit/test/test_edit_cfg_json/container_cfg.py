#! /usr/bin/env python3
"""Configuration classes whose members hold lists and dicts.

They are in a module of their own rather than beside the flat ones, because
what they are for is one step of the delivery plan and because one module of
every sample configuration would be too long to read.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional, TextIO
import sys
from config_as_json import Config, ConfigNesting, ConfigNestingKind, \
    IntFloatValidator, InvalidConfiguration, ListOrderingValidator, \
    ListValueValidator, MemberValidationStep, MemberValidator, NestedConfigs, \
    ParseConverter, ValidationPlan, WholeConfigValidationStep, \
    WholeConfigValidator
from .sample_cfg import Colour, SampleCfg

MANY_LABELS = 12
"""How many labels the long list of `BigListCfg` holds.

It is more than a container may add before the editor opens it folded, which
is what that class is for.
"""

SMALL_LIMIT = 9
"""Largest value that the list of `RangedListCfg` accepts."""

INNER_LIMIT = 10
"""Largest width that the nested class of `SubtreeCfg` accepts."""

ORDER_REFUSAL = 'The low value {low} is above the high value {high}.'
"""What the rule of a nested class that is about no member of it says."""

CROSS_REFUSAL = 'The width {width} is the low value of the other object.'
"""What the rule that reaches across two nested objects says.

It is about both of them and therefore about neither, which is what makes each
of them a perfectly good configuration on its own while the one holding them
is refused.
"""


def _refuse(message: str, stderr_file: TextIO) -> None:
    """Write one refusal to the diagnostics stream and then raise it.

    Args:
        message: What is wrong with the configuration.
        stderr_file: Stream that a validator writes its refusal to before it
            raises, which is the contract `config_as_json` states.

    Raises:
        InvalidConfiguration: Always, which is what this is for.
    """
    print(message, file=stderr_file)
    raise InvalidConfiguration(message)


class TreeCfg(SampleCfg):
    """A configuration whose containers hold containers of their own."""

    def declare_members(self) -> None:
        """Assign a list of dicts, a dict of lists and one plain member."""
        self.rules: list[dict[str, int]] = [{'low': 1}, {'high': 9}]
        self.groups: dict[str, list[str]] = {'red': ['a', 'b'],
                                             'blue': ['c']}
        self.answer: int = 3


class EmptyCfg(SampleCfg):
    """A configuration whose containers hold nothing at all."""

    def declare_members(self) -> None:
        """Assign one empty list and one empty dict."""
        self.tags: list[str] = []
        self.limits: dict[str, int] = {}


class BigListCfg(SampleCfg):
    """A configuration with a list too long for the editor to open."""

    def declare_members(self) -> None:
        """Assign one long list and one short one."""
        self.many: list[str] = [f'label-{index}' for index in
                                range(MANY_LABELS)]
        self.few: list[str] = ['one', 'two']


class NormalizeCfg(SampleCfg):
    """A configuration whose validator sorts and de-duplicates a list.

    It is what shows that a validation pass can leave the model with other
    rows than it had: removing a duplicate removes a row.
    """

    def declare_members(self) -> None:
        """Assign the list that the validator normalizes."""
        self.words: list[str] = ['beta', 'alpha']

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the one step that sorts the list and de-duplicates it."""
        _ = stderr_file
        ordering = ListOrderingValidator(str, order=True,
                                         keep_only_unique=True)
        return [MemberValidationStep(member_names=['words'],
                                     validator=ordering)]


GROUP_FORM = 'group-{stage}'
"""Form of the key that the validator of `GrowingCfg` fills in.

Which key it is follows the value of another member, so a stage the
configuration has not been at yet is a node that the rows had nothing for at
all. That is what a container appearing means, and a validator that wrote the
same key every time could not show it: the class validates itself as it is
constructed, so a key that does not follow a value is already there before the
editor has run a pass of its own.
"""


def _stage_labels() -> list[str]:
    """Return the labels of one stage, too many for the editor to open.

    Returns:
        More labels than a container may add before it starts folded.
    """
    return [f'label-{index}' for index in range(MANY_LABELS)]


# A validator has one method, which is what a validator is.
# pylint: disable-next=too-few-public-methods
class FillsInAStage(MemberValidator):
    """A validator that fills in the labels of the stage it is told.

    An application that works out a part of its own configuration from another
    member of it is what this stands for. A member validator returns the value
    that is stored back into the member, so it is also how a validation pass
    creates a container that the rows before it had no node for.
    """

    def validate_member(self, config: Config, member_name: str,
                        member_value: object,
                        stderr_file: TextIO = sys.stderr) -> Optional[object]:
        """Return the dict with the labels of the stage added to it."""
        _ = (member_name, stderr_file)
        assert isinstance(member_value, dict)
        key = GROUP_FORM.format(stage=getattr(config, 'stage'))
        return dict(member_value) | {key: _stage_labels()}


class GrowingCfg(SampleCfg):
    """A configuration whose validator creates a container of its own.

    The container it creates is long enough to open folded, which is what a
    program that shows the buffer once has to be able to say it does not want:
    such a program validates before it prints, so a container the pass created
    would be folded away in the one printout there is.
    """

    def declare_members(self) -> None:
        """Assign the stage and the dict that the validator fills in."""
        self.stage: int = 1
        self.groups: dict[str, list[str]] = {}

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the one step that fills in the labels of the stage."""
        _ = stderr_file
        return [MemberValidationStep(member_names=['groups'],
                                     validator=FillsInAStage())]


class RangedListCfg(SampleCfg):
    """A configuration whose list elements each have to be in a range.

    What the validator refuses is the whole member, because that is what a
    `MemberValidator` is given, so it is what shows where such a refusal is
    reported.
    """

    def declare_members(self) -> None:
        """Assign the list that the validator is about."""
        self.sizes: list[int] = [1, 2]

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the one step that checks every element of the list."""
        _ = stderr_file
        in_range = ListValueValidator[int](0, SMALL_LIMIT, None)
        return [MemberValidationStep(member_names=['sizes'],
                                     validator=in_range)]


class KeyedEnumCfg(SampleCfg):
    """A configuration whose dict holds a key named after a member.

    `config_as_json` applies a parse converter while it decodes an object, so
    the converter of `colour` reaches the value of every dictionary key of
    that name and not only the member. This class is what says whether the
    editor answers the same way.
    """

    def declare_members(self) -> None:
        """Assign one enum member and one dict holding a key of that name."""
        self.colour: Colour = Colour.RED
        self.shades: dict[str, str] = {'colour': 'GREEN', 'other': 'x'}

    def parse_converters(self) -> Optional[dict[str, ParseConverter]]:
        """Return the converter that turns a name into a member of `Colour`."""
        return {'colour': Config.get_converter_dict(Colour)}


class InnerCfg(SampleCfg):
    """A nested configuration object with two members of its own.

    It derives from the base class of these samples like every other one of
    them, which is also the constructor shape that a nested configuration
    object has to have: `config_as_json` builds one with the three keyword
    arguments that base class already takes.
    """

    def declare_members(self) -> None:
        """Assign the two members of this nested object."""
        self.width: int = 4
        self.height: int = 6


class NestedCfg(SampleCfg):
    """A configuration that declares one nested configuration object.

    That member serializes as a dict and is not one, so it is a node with a
    class and members of its own rather than the dictionary it writes.
    """

    def declare_members(self) -> None:
        """Assign the nested object and one ordinary dict beside it."""
        self.inner: InnerCfg = InnerCfg()
        self.limits: dict[str, int] = {'low': 1}

    def nested_configs(self) -> NestedConfigs:
        """Return the declaration of the one nested configuration object."""
        return {'inner': ConfigNesting(kind=ConfigNestingKind.MEMBER,
                                       config_type=InnerCfg)}


class OmitNestedCfg(SampleCfg):
    """A configuration whose optional nested object is left out of JSON.

    Nothing is written for a member that is not there, so it has no row at
    all, which is what any member the class omits already does.
    """

    def declare_members(self) -> None:
        """Assign the optional nested object and one ordinary member."""
        self.inner: Optional[InnerCfg] = None
        self.answer: int = 3

    def nested_configs(self) -> NestedConfigs:
        """Return the declaration of the optional nested object."""
        optional = ConfigNestingKind.OPTIONAL_MEMBER
        return {'inner': ConfigNesting(kind=optional, config_type=InnerCfg)}

    def _omit_none_from_json(self) -> list[str]:
        """Return the member that is left out of JSON while it is None."""
        return ['inner']


class NullNestedCfg(SampleCfg):
    """A configuration whose optional nested object is written as null.

    This is the one shape in which a declared nested member has a row and no
    object: the class does not omit it, so `null` reaches the file. The row
    says which class is missing and cannot be edited, because no text typed
    into a field becomes a configuration object.
    """

    def declare_members(self) -> None:
        """Assign the optional nested object that is written as null."""
        self.inner: Optional[InnerCfg] = None
        self.answer: int = 3

    def nested_configs(self) -> NestedConfigs:
        """Return the declaration of the optional nested object."""
        optional = ConfigNestingKind.OPTIONAL_MEMBER
        return {'inner': ConfigNesting(kind=optional, config_type=InnerCfg)}


class EnumInnerCfg(SampleCfg):
    """A nested object whose own class declares the converter it needs."""

    def declare_members(self) -> None:
        """Assign the enum member that this class converts for itself."""
        self.colour: Colour = Colour.RED

    def parse_converters(self) -> Optional[dict[str, ParseConverter]]:
        """Return the converter that turns a name into a member of `Colour`."""
        return {'colour': Config.get_converter_dict(Colour)}


class OwnedEnumCfg(SampleCfg):
    """A configuration whose nested object converts a name that it does not.

    Both classes have a member called `colour` and only the nested one
    declares a converter for it, so the two members answer differently. That
    is what a parse converter belonging to the class that owns the subtree
    means, and it is the one thing about nesting that the rows could not have
    read from the configuration alone.
    """

    def declare_members(self) -> None:
        """Assign the nested object and a plain member of the same name."""
        self.inner: EnumInnerCfg = EnumInnerCfg()
        self.colour: str = 'plain text'

    def nested_configs(self) -> NestedConfigs:
        """Return the declaration of the one nested configuration object."""
        return {'inner': ConfigNesting(kind=ConfigNestingKind.MEMBER,
                                       config_type=EnumInnerCfg)}


class OmitInnerCfg(SampleCfg):
    """A nested object that leaves one of its own members out of JSON.

    Which members may be left out is the class's own to say, so a member of
    this one is optional inside it while the member of that name in the class
    holding it is not.
    """

    def declare_members(self) -> None:
        """Assign one optional member and one ordinary member.

        The optional one holds a value, so that it is written and has a row:
        a member that is left out has no row to say anything about it on.
        """
        self.note: Optional[str] = 'inner note'
        self.width: int = 4

    def _omit_none_from_json(self) -> list[str]:
        """Return the member that is left out of JSON while it is None."""
        return ['note']


class OwnedOptionCfg(SampleCfg):
    """A configuration whose nested object decides its own optional member.

    The member called `note` is optional inside the nested object and
    mandatory here, which is what says that `_omit_none_from_json()` belongs
    to the class that owns the subtree.
    """

    def declare_members(self) -> None:
        """Assign the nested object and a member of the same name beside it."""
        self.inner: OmitInnerCfg = OmitInnerCfg()
        self.note: str = 'kept'

    def nested_configs(self) -> NestedConfigs:
        """Return the declaration of the one nested configuration object."""
        return {'inner': ConfigNesting(kind=ConfigNestingKind.MEMBER,
                                       config_type=OmitInnerCfg)}


class DeepInnerCfg(SampleCfg):
    """A nested object that holds a dict of nested objects of its own."""

    def declare_members(self) -> None:
        """Assign the dict of nested objects and one plain member."""
        self.parts: dict[str, InnerCfg] = {'one': InnerCfg()}
        self.label: str = 'deep'

    def nested_configs(self) -> NestedConfigs:
        """Return the declaration that every value of the dict is one."""
        return {'parts': ConfigNesting(kind=ConfigNestingKind.DICT_VALUE,
                                       config_type=InnerCfg)}


class DeepConfigCfg(SampleCfg):
    """A list of nested objects, each holding a dict of more of them.

    This is what a real configuration looks like rather than a special case,
    which is why it is one of the samples: the ownership has to hold at every
    depth and not only at the first.
    """

    def declare_members(self) -> None:
        """Assign the list of nested objects."""
        self.outputs: list[DeepInnerCfg] = [DeepInnerCfg()]

    def nested_configs(self) -> NestedConfigs:
        """Return the declaration that every element of the list is one."""
        return {'outputs': ConfigNesting(kind=ConfigNestingKind.LIST_ELEMENT,
                                         config_type=DeepInnerCfg)}


class NoDocInnerCfg(InnerCfg):
    """This docstring is taken away below, so that this class has none."""


# A nested configuration class without a docstring is one the editor has to
# handle, and it cannot be written here, because every class in this
# repository has to have one. Taking it away afterwards is the same thing, and
# it is what makes the class hold None under `__doc__` of its own.
NoDocInnerCfg.__doc__ = None


class NoDocNestedCfg(SampleCfg):
    """A configuration whose nested object has no docstring of its own.

    The docstring of a base class is deliberately not used in its place, so
    such a node is shown with its class and nothing else.
    """

    def declare_members(self) -> None:
        """Assign the nested object whose class says nothing about itself."""
        self.inner: NoDocInnerCfg = NoDocInnerCfg()

    def nested_configs(self) -> NestedConfigs:
        """Return the declaration of the one nested configuration object."""
        return {'inner': ConfigNesting(kind=ConfigNestingKind.MEMBER,
                                       config_type=NoDocInnerCfg)}


class RangedInnerCfg(SampleCfg):
    """A nested object whose own class refuses a width above a limit.

    The rule belongs to this class, so it runs while `parse_json` builds one
    of these. That is exactly why the walk over the class holding it cannot
    say which member was refused: the object that would be asked is one that
    was never built.
    """

    def declare_members(self) -> None:
        """Assign the one member that the rule of this class is about."""
        self.width: int = 4

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the one rule that the width has to obey."""
        _ = stderr_file
        in_range = IntFloatValidator[int](min_value=0, max_value=INNER_LIMIT,
                                          allowed_values=None)
        return [MemberValidationStep(member_names=['width'],
                                     validator=in_range)]


# A validator has one method, which is what a validator is.
# pylint: disable-next=too-few-public-methods
class LowNotHigh(WholeConfigValidator):
    """A rule of a nested class that is about no single member of it.

    It is about two members together, so there is no member to attribute it
    to, and it is what shows that such a refusal is reported at the object
    rather than at one of the rows below it.
    """

    def validate(self, config: Config,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Refuse an object whose low value is above its high value."""
        low = getattr(config, 'low', 0)
        high = getattr(config, 'high', 0)
        if low > high:
            _refuse(ORDER_REFUSAL.format(low=low, high=high), stderr_file)


class OrderedInnerCfg(SampleCfg):
    """A nested object with a rule about two of its members at once."""

    def declare_members(self) -> None:
        """Assign the two members that the rule of this class is about."""
        self.low: int = 1
        self.high: int = 9

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the one rule that is about both members together."""
        _ = stderr_file
        return [WholeConfigValidationStep(validator=LowNotHigh())]


# A validator has one method, which is what a validator is.
# pylint: disable-next=too-few-public-methods
class WidthNotLow(WholeConfigValidator):
    """A rule that reaches across the boundary between two nested objects.

    Neither object can check it, because each of them knows its own members
    and nothing about the other, so it belongs to the class holding them
    both. It is what makes a configuration refused while every object inside
    it is a perfectly good configuration on its own.
    """

    def validate(self, config: Config,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Refuse a configuration whose two objects agree on one number."""
        width = getattr(config, 'ranged').width
        if width == getattr(config, 'ordered').low:
            _refuse(CROSS_REFUSAL.format(width=width), stderr_file)


class SubtreeCfg(SampleCfg):
    """A configuration whose two nested objects each have rules of their own.

    Every case that asking an object about itself has to tell apart is
    reachable from this one class: a member of an object refused by the class
    that owns it, an object refused for a reason that is about no member of
    it, and a configuration refused while both objects are valid on their own.
    """

    def declare_members(self) -> None:
        """Assign the two nested objects that the rules are about."""
        self.ranged: RangedInnerCfg = RangedInnerCfg()
        self.ordered: OrderedInnerCfg = OrderedInnerCfg()

    def nested_configs(self) -> NestedConfigs:
        """Return the declaration of the two nested configuration objects."""
        member = ConfigNestingKind.MEMBER
        return {'ranged': ConfigNesting(kind=member,
                                        config_type=RangedInnerCfg),
                'ordered': ConfigNesting(kind=member,
                                         config_type=OrderedInnerCfg)}

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the one rule that is about both objects together."""
        _ = stderr_file
        return [WholeConfigValidationStep(validator=WidthNotLow())]


class HoldingInnerCfg(SampleCfg):
    """A nested object that holds a nested object with a rule of its own."""

    def declare_members(self) -> None:
        """Assign the nested object that this one holds."""
        self.ranged: RangedInnerCfg = RangedInnerCfg()

    def nested_configs(self) -> NestedConfigs:
        """Return the declaration of the object inside this one."""
        return {'ranged': ConfigNesting(kind=ConfigNestingKind.MEMBER,
                                        config_type=RangedInnerCfg)}


class DeepSubtreeCfg(SampleCfg):
    """A configuration two objects deep, the innermost holding the rule.

    It is what shows that one mistake is reported once: an object holding a
    refused object is refused as well, and it is not asked again, so what is
    wrong appears at the innermost object it is really about.
    """

    def declare_members(self) -> None:
        """Assign the outer of the two nested objects."""
        self.outer: HoldingInnerCfg = HoldingInnerCfg()

    def nested_configs(self) -> NestedConfigs:
        """Return the declaration of the outer nested object."""
        return {'outer': ConfigNesting(kind=ConfigNestingKind.MEMBER,
                                       config_type=HoldingInnerCfg)}


class RangedObjectsCfg(SampleCfg):
    """A configuration whose list holds objects that have a rule of their own.

    It is what folding a member has to reach. The member is a list and is no
    configuration, so it has nothing to say about itself and asking the node
    that was folded would ask nothing at all, while folding it hides every
    object that does have something to say.
    """

    def declare_members(self) -> None:
        """Assign the list of objects that each obey a rule of their class."""
        self.outputs: list[RangedInnerCfg] = [RangedInnerCfg(),
                                              RangedInnerCfg()]

    def nested_configs(self) -> NestedConfigs:
        """Return the declaration that every element of the list is one."""
        return {'outputs': ConfigNesting(kind=ConfigNestingKind.LIST_ELEMENT,
                                         config_type=RangedInnerCfg)}


class ConfigListCfg(SampleCfg):
    """A configuration whose member holds a list of nested objects.

    This is the ordinary shape of a real configuration rather than a special
    case, so the member stays a container of the tree that can be folded and
    says how much it holds, and each object inside it is one node.
    """

    def declare_members(self) -> None:
        """Assign the list of nested objects and one plain member."""
        self.outputs: list[InnerCfg] = [InnerCfg(), InnerCfg()]
        self.answer: int = 3

    def nested_configs(self) -> NestedConfigs:
        """Return the declaration that every element of the list is one."""
        return {'outputs': ConfigNesting(kind=ConfigNestingKind.LIST_ELEMENT,
                                         config_type=InnerCfg)}


class ConfigDictCfg(SampleCfg):
    """A configuration whose member holds a dict of nested objects."""

    def declare_members(self) -> None:
        """Assign the dict of nested objects."""
        self.outputs: dict[str, InnerCfg] = {'first': InnerCfg()}

    def nested_configs(self) -> NestedConfigs:
        """Return the declaration that every value of the dict is one."""
        return {'outputs': ConfigNesting(kind=ConfigNestingKind.DICT_VALUE,
                                         config_type=InnerCfg)}


class ElementCfg(SampleCfg):
    """A configuration holding every kind of container that cannot grow.

    The four members are the four different answers the editor gives about
    adding an element, and they are together in one class so that a test can
    read all four of one model.
    """

    def declare_members(self) -> None:
        """Assign one list of each kind and one dict of each kind."""
        self.tags: list[str] = ['first', 'second']
        self.spare: list[str] = []
        self.limits: dict[str, int] = {'low': 1}
        self.labels: dict[str, str] = {'team': 'platform'}
        self._unchecked_dicts = ['labels']


class EmptyObjectsCfg(SampleCfg):
    """A configuration whose declared list of objects holds none of them.

    What an element of it is comes from the declaration and not from what the
    member happens to hold, so it can be given one while it is empty. That is
    the case that a container of plain values cannot answer.
    """

    def declare_members(self) -> None:
        """Assign the empty list of nested objects."""
        self.outputs: list[InnerCfg] = []

    def nested_configs(self) -> NestedConfigs:
        """Return the declaration that every element of the list is one."""
        return {'outputs': ConfigNesting(kind=ConfigNestingKind.LIST_ELEMENT,
                                         config_type=InnerCfg)}


class ByKeyCfg(SampleCfg):
    """A configuration whose dict holds an object under one named key.

    `DICT_VALUE_BY_KEY` is what declares that shape, and it is the one that
    makes the keys of a dict a policy of their own: one of them holds a
    configuration object and the others hold ordinary values.
    """

    def declare_members(self) -> None:
        """Assign the dict whose one named key holds a nested object."""
        self.hooks: dict[str, InnerCfg | str] = {'main': InnerCfg(),
                                                 'note': 'nothing'}

    def nested_configs(self) -> NestedConfigs:
        """Return the declaration of the one key that holds an object."""
        by_key = ConfigNestingKind.DICT_VALUE_BY_KEY
        return {'hooks': ConfigNesting(kind=by_key, config_type=InnerCfg,
                                       discriminator_key='main')}
