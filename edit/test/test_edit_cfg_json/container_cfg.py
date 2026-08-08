#! /usr/bin/env python3
"""Configuration classes whose members hold lists and dicts.

They are in a module of their own rather than beside the flat ones, because
what they are for is one step of the delivery plan and because one module of
every sample configuration would be too long to read.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional, TextIO
from config_as_json import Config, ConfigNesting, ConfigNestingKind, \
    ListOrderingValidator, ListValueValidator, MemberValidationStep, \
    NestedConfigs, ParseConverter, ValidationPlan
from .sample_cfg import Colour, SampleCfg

MANY_LABELS = 12
"""How many labels the long list of `BigListCfg` holds.

It is more than a container may add before the editor opens it folded, which
is what that class is for.
"""

SMALL_LIMIT = 9
"""Largest value that the list of `RangedListCfg` accepts."""


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
