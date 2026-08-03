#! /usr/bin/env python3
"""Configuration classes used by the tests of edit_cfg_json."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from enum import Enum, IntEnum
from typing import Optional, TextIO
import sys
from config_as_json import Config, ConfigAutoChangeHook, \
    InvalidConfiguration, IntFloatValidator, MemberValidationStep, \
    MemberValidator, ParseConverter, PathOrStr, StrCaseChangeValidator, \
    StrCaseSpec, StrPositionSpec, StrValidator, ValidationPlan, \
    ValueTypeValidator, WholeConfigValidationStep, WholeConfigValidator

REFUSAL_MESSAGE = 'The application refuses {name}.'
"""Message of the validator that refuses without saying anything else."""

TOO_LARGE_MESSAGE = 'The two numbers add up to {total}, which is too much.'
"""Message of the rule that is about two members and therefore neither."""

LOWEST = 0
"""Smallest number that `RangeCfg` accepts."""

HIGHEST = 100
"""Largest number that `RangeCfg` accepts."""

SUM_LIMIT = 120
"""Largest sum of the two numbers of `RulesCfg`.

It is above the largest that either of them may be on its own, so that the
rule about both of them can only be reached by a configuration whose members
are each of them allowed.
"""


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


class DocumentedCfg(SampleCfg):
    """One line that says what this configuration is for.

    A second paragraph that is the detail of this class.
    """

    def declare_members(self) -> None:
        """Assign one member, because the docstring is the point of this."""
        self.name: str = 'documented'


class NoDocCfg(DocumentedCfg):
    """This docstring is taken away below, so that this class has none."""


# A configuration class written without a docstring is one the editor has to
# handle, and it cannot be written here, because every class in this
# repository has to have one. Taking it away afterwards is the same thing: a
# class defined without a docstring holds None under `__doc__` in its own
# namespace, which is exactly what this assignment puts there.
NoDocCfg.__doc__ = None


class WrappedDocCfg(DocumentedCfg):
    """This docstring is replaced below, by one that spans two lines."""


# An application may write a summary that runs over two lines, which no
# docstring convention allows and which the checks of this repository refuse.
# Putting one here is how the editor is given one to read.
WrappedDocCfg.__doc__ = ('A summary that is long enough to have been written\n'
                         '    on two lines of the source file.\n\n'
                         '    A second paragraph that is the detail.\n    ')


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


class Level(IntEnum):
    """The values that the int enum member of `IntEnumCfg` can hold.

    Two of the three names begin with the same two characters, so that the
    tests can tell an exact name, a prefix that names one member and a
    prefix that names two of them apart.
    """

    LOWEST = 1
    """The name that `LO` is not enough to pick out."""

    LOW = 2
    """The name that is also the beginning of another name."""

    HIGH = 3
    """The name that `HI` is enough to pick out."""


class IntEnumCfg(SampleCfg):
    """A configuration with an int enum member, written as its name.

    An `IntEnum` member is an `int`, so Python's own JSON encoder would
    write its number. `config_as_json` converts it to its member name
    before that happens, which is what this class is here to show.
    """

    def declare_members(self) -> None:
        """Assign the one int enum member."""
        self.level: Level = Level.LOWEST

    def parse_converters(self) -> Optional[dict[str, ParseConverter]]:
        """Return the converter that turns a member name into a member."""
        return {'level': Config.get_converter_dict(Level)}


def _from_hex(value: object) -> int:
    """Return the number that one piece of hexadecimal text stands for."""
    return int(str(value), 16)


class HexCfg(SampleCfg):
    """A configuration whose number is written as hexadecimal text.

    Its converter is not an enum converter and `config_as_json` does not
    ship it, which is what this class is for: the editor runs whatever
    converter a member declares and knows nothing about enums in particular.
    """

    def declare_members(self) -> None:
        """Assign the one number member that the converter is about."""
        self.mask: int = 255

    def parse_converters(self) -> Optional[dict[str, ParseConverter]]:
        """Return the converter that reads that number from hexadecimal."""
        return {'mask': ParseConverter(result_type=int, func=_from_hex,
                                       args={})}


class PlainLevel(Enum):
    """This docstring is taken away below, so that this enum has none."""

    QUIET = 1
    LOUD = 2


# An enum class written without a docstring is one the editor has to handle,
# and it cannot be written here, because every class in this repository has to
# have one. Taking it away afterwards is the same thing.
PlainLevel.__doc__ = None


class PlainEnumCfg(SampleCfg):
    """A configuration whose enum member has no docstring of its own."""

    def declare_members(self) -> None:
        """Assign the one enum member."""
        self.level: PlainLevel = PlainLevel.QUIET

    def parse_converters(self) -> Optional[dict[str, ParseConverter]]:
        """Return the converter that turns a member name into a member."""
        return {'level': Config.get_converter_dict(PlainLevel)}


class TooLarge(WholeConfigValidator):  # pylint: disable=too-few-public-methods
    """A rule about two members together and therefore about neither.

    It is what shows the difference the editor has to make: a member
    validator says which member it is about, and this does not, because the
    sum of two members is not one of them.
    """

    def validate(self, config: Config,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Refuse a configuration whose two numbers add up to too much."""
        total = getattr(config, 'first', 0) + getattr(config, 'second', 0)
        if total > SUM_LIMIT:
            message = TOO_LARGE_MESSAGE.format(total=total)
            print(message, file=stderr_file)
            raise InvalidConfiguration(message)


class RulesCfg(SampleCfg):
    """A configuration with a rule per member and one about both of them.

    Every case the attribution of a refusal has to tell apart is reachable
    from this one class: one member refused, both of them refused, and a rule
    that is about neither of them.
    """

    def declare_members(self) -> None:
        """Assign the two numbers that the rules are about."""
        self.first: int = 1
        self.second: int = 2

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return one step per member and then the step about both."""
        _ = stderr_file
        in_range = IntFloatValidator[int](min_value=LOWEST, max_value=HIGHEST,
                                          allowed_values=None)
        return [MemberValidationStep(member_names=['first', 'second'],
                                     validator=in_range),
                WholeConfigValidationStep(validator=TooLarge())]


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
    """A configuration whose own validator refuses every value.

    No application could use this class, because its own declared defaults
    are refused and every way into the editor constructs it first. It is here
    to make one thing reachable that is otherwise hard to reach: a validator
    that refuses without writing a word, which an application's own validator
    is free to do and which the editor still has to explain.
    """

    def declare_members(self) -> None:
        """Assign the one member that the validator refuses."""
        self.name: str = 'text'

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the step that refuses whatever the member holds."""
        _ = stderr_file
        return [MemberValidationStep(member_names=['name'],
                                     validator=SilentRefusal())]


class HookCfg(Config):
    """A configuration whose constructor declares the change hook.

    `Config.__init__` takes the hook, but a class has to declare it and hand
    it on for the hook to reach it, and the constructor that
    `config_as_json` documents does not. This class is the one that does, so
    that the tests can show the editor forwarding the hook to a class that
    takes it and dropping it for a class that does not.
    """

    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 auto_ch_hook: Optional[ConfigAutoChangeHook] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Record the hook that was given and then apply the JSON.

        The hook is recorded under a private name, so that it does not
        become a member of the configuration: `config_as_json` reads the
        public attributes of the object as its schema.
        """
        self._hook_given = auto_ch_hook
        self.name: str = 'hook text'
        self.answer: int = 42
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         auto_ch_hook=auto_ch_hook, stderr_file=stderr_file)

    def hook_given(self) -> Optional[ConfigAutoChangeHook]:
        """Return the hook this object was constructed with, if any."""
        return self._hook_given

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return no extra validation steps."""
        _ = stderr_file
        return []


class ExtraArgCfg(SampleCfg):
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

    def declare_members(self) -> None:
        """Declare nothing, because the constructor did it already.

        The one member of this class is the extra constructor argument, so
        it cannot be assigned anywhere else.
        """
