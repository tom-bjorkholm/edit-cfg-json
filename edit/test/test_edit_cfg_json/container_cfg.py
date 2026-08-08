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

    That member serializes as a dict and is not one, so this version of the
    editor leaves it as one row. Step 11 of the delivery plan is what makes
    it a node with a class and a validity state of its own.
    """

    def declare_members(self) -> None:
        """Assign the nested object and one ordinary dict beside it."""
        self.inner: InnerCfg = InnerCfg()
        self.limits: dict[str, int] = {'low': 1}

    def nested_configs(self) -> NestedConfigs:
        """Return the declaration of the one nested configuration object."""
        return {'inner': ConfigNesting(kind=ConfigNestingKind.MEMBER,
                                       config_type=InnerCfg)}


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
