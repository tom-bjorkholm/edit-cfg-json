#! /usr/bin/env python3
"""Configuration classes used by the tests of edit_cfg_json."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from enum import Enum
from typing import Optional, TextIO
import sys
from config_as_json import Config, IntFloatValidator, MemberValidationStep, \
    MemberValidator, ParseConverter, PathOrStr, StrCaseChangeValidator, \
    StrCaseSpec, StrPositionSpec, StrValidator, ValidationPlan, \
    ValueTypeValidator

REFUSAL_MESSAGE = 'The application refuses {name}.'
"""Message of the validator that refuses without saying anything else."""

LOWEST = 0
"""Smallest number that `RangeCfg` accepts."""

HIGHEST = 100
"""Largest number that `RangeCfg` accepts."""


class SampleCfg(Config):
    """Base class of the sample configurations used in these tests.

    A subclass only implements `declare_members`, because the constructor
    keywords and the empty validation plan are the same for all of them.
    """

    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Declare the members of the subclass and then apply the JSON."""
        self.declare_members()
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file)

    def declare_members(self) -> None:
        """Assign the configuration members and their default values."""
        raise NotImplementedError

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return no extra validation steps."""
        _ = stderr_file
        return []


class FlatCfg(SampleCfg):
    """A configuration with one text member and one number member."""

    def declare_members(self) -> None:
        """Assign one string member and one integer member."""
        self.name: str = 'flat text'
        self.answer: int = 42


class NoneCfg(SampleCfg):
    """A configuration whose text member defaults to None."""

    def declare_members(self) -> None:
        """Assign one optional string member and one integer member."""
        self.name: Optional[str] = None
        self.answer: int = 7


class ListCfg(SampleCfg):
    """A configuration with a list member and a dict member."""

    def declare_members(self) -> None:
        """Assign one list member, one dict member and one scalar member."""
        self.tags: list[str] = ['first', 'second']
        self.limits: dict[str, int] = {'low': 1, 'high': 9}
        self.answer: int = 3


class OmitCfg(SampleCfg):
    """A configuration whose optional member is left out of JSON when None."""

    def declare_members(self) -> None:
        """Assign one optional member between two ordinary members."""
        self.first: int = 1
        self.optional: Optional[str] = None
        self.last: int = 2

    def _omit_none_from_json(self) -> list[str]:
        """Return the member that is left out of JSON while it is None."""
        return ['optional']


class RewriteCfg(SampleCfg):
    """A configuration whose validator rewrites its text member.

    Serializing a configuration object validates it, and a member validator
    returns the value that is stored back into the member. This class exists
    so that the tests can show that building a model from a configuration
    object leaves that object alone, and that a validation pass that rewrote
    a value says so.
    """

    def declare_members(self) -> None:
        """Assign the one string member that the validator rewrites."""
        self.name: str = 'lower case text'

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return a step that upper cases the first character of `name`."""
        _ = stderr_file
        change_case = StrCaseChangeValidator(
            special_position=StrPositionSpec.FIRST_IN_STRING,
            special_position_case=StrCaseSpec.UPPER,
            other_position_case=StrCaseSpec.ORIGINAL)
        return [MemberValidationStep(member_names=['name'],
                                     validator=change_case)]


class RangeCfg(SampleCfg):
    """A configuration whose number member has to be within a range."""

    def declare_members(self) -> None:
        """Assign the one number member that the range applies to."""
        self.answer: int = 42

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return a step that refuses a number outside the range."""
        _ = stderr_file
        in_range = IntFloatValidator[int](min_value=LOWEST, max_value=HIGHEST,
                                          allowed_values=None)
        return [MemberValidationStep(member_names=['answer'],
                                     validator=in_range)]


class AllowedCfg(SampleCfg):
    """A configuration whose text member has a set of allowed values."""

    def declare_members(self) -> None:
        """Assign the one text member that the allowed values apply to."""
        self.colour: str = 'red'

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return a step that refuses a value outside the allowed set."""
        _ = stderr_file
        allowed = StrValidator(allowed_values=['red', 'green'],
                               ignore_case=False)
        return [MemberValidationStep(member_names=['colour'],
                                     validator=allowed)]


class TypedCfg(SampleCfg):
    """A configuration whose member is checked for its runtime type."""

    def declare_members(self) -> None:
        """Assign the one member whose runtime type is checked."""
        self.count: int = 1

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return a step that refuses a value that is not a whole number."""
        _ = stderr_file
        return [MemberValidationStep(member_names=['count'],
                                     validator=ValueTypeValidator(int))]


class Colour(Enum):
    """The values that the enum member of `EnumCfg` can hold."""

    RED = 1
    """The colour a new configuration starts with."""

    GREEN = 2
    """The other colour."""


class EnumCfg(SampleCfg):
    """A configuration with an enum member, written as its member name.

    An enum is what makes a conversion fail rather than a validator: a name
    that is no member of the enum cannot be turned into a value at all, and
    the configuration class reports that as JSON it cannot use.
    """

    def declare_members(self) -> None:
        """Assign the one enum member."""
        self.colour: Colour = Colour.RED

    def parse_converters(self) -> Optional[dict[str, ParseConverter]]:
        """Return the converter that turns a member name into a member."""
        return {'colour': Config.get_converter_dict(Colour)}


class SilentRefusal(MemberValidator):  # pylint: disable=too-few-public-methods
    """A member validator of the kind an application writes for itself.

    It refuses every value with a plain `ValueError` and writes nothing to
    the diagnostics stream, which an application's own validator is free to
    do. It is what shows that a verdict still has something to report when
    the configuration class itself reported nothing.
    """

    def validate_member(self, config: Config, member_name: str,
                        member_value: object,
                        stderr_file: TextIO = sys.stderr) -> Optional[object]:
        """Refuse the value without writing to the diagnostics stream."""
        _ = (config, member_value, stderr_file)
        raise ValueError(REFUSAL_MESSAGE.format(name=member_name))


class RefuseCfg(SampleCfg):
    """A configuration whose own validator refuses every value."""

    def declare_members(self) -> None:
        """Assign the one member that the validator refuses."""
        self.name: str = 'text'

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the step that refuses whatever the member holds."""
        _ = stderr_file
        return [MemberValidationStep(member_names=['name'],
                                     validator=SilentRefusal())]


class ExtraArgCfg(Config):
    """A configuration whose constructor needs an argument of its own.

    The editor cannot construct this class, because it knows nothing about
    the extra argument. An explicit loader is what the design gives the
    application for exactly that, and it arrives in a later step. Until
    then such a class is refused, with the diagnostics Python itself
    produces, rather than being half handled.
    """

    def __init__(self, home: str, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Take the extra argument and then apply the JSON."""
        self.home: str = home
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file)

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return no extra validation steps."""
        _ = stderr_file
        return []
