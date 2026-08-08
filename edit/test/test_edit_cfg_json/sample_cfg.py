#! /usr/bin/env python3
"""Configuration classes used by the tests of edit_cfg_json."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from enum import Enum, IntEnum
from functools import partial
from typing import Optional, TextIO
import sys
from config_as_json import Config, ConfigAutoChangeHook, ConfigPath, \
    InvalidConfiguration, IntFloatValidator, MemberValidationStep, \
    MemberValidator, ParseConverter, PathOrStr, ReadOldConfiguration, \
    RocfKeyMove, RocfKeyRename, RocfValueMigration, RocfValueWrite, \
    SerializeConverter, SerializeConverters, \
    StrCaseChangeValidator, StrCaseSpec, StrPositionSpec, \
    StrValidator, ValidationPlan, ValueTypeValidator, \
    WholeConfigValidationStep, WholeConfigValidator
from edit_cfg_json import Descriptions, derived_loader

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


ABOUT_FLAT_NAME = 'What this name is for, as an application would say it.'
"""What `FLAT_DESCRIPTIONS` says about the text member of `FlatCfg`."""

FLAT_DESCRIPTIONS: Descriptions = {('name',): ABOUT_FLAT_NAME}
"""What an application says about the members of `FlatCfg`.

It describes one of the two members and says nothing about the other, which is
what an application is free to do. It is a module level name so that the
programs of this library can be told it with `--descriptions`.
"""


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


ACCEPTED_VALUE = 'text'
"""The one value that `SilentRefusal` accepts, and the declared default."""


class SilentRefusal(MemberValidator):  # pylint: disable=too-few-public-methods
    """A member validator of the kind an application writes for itself.

    It refuses with a plain `ValueError` and writes nothing to the diagnostics
    stream, which an application's own validator is free to do. It is what
    shows that a verdict still has something to report when the configuration
    class itself reported nothing.

    The declared default is the one value it accepts, so the class below is one
    an application could really have. A validator that refused that value too
    would make the class impossible to construct, and therefore impossible to
    reach the editor with at all.
    """

    def validate_member(self, config: Config, member_name: str,
                        member_value: object,
                        stderr_file: TextIO = sys.stderr) -> Optional[object]:
        """Refuse anything but the declared value, and say nothing about it."""
        _ = (config, stderr_file)
        if member_value == ACCEPTED_VALUE:
            return member_value
        raise ValueError(REFUSAL_MESSAGE.format(name=member_name))


class RefuseCfg(SampleCfg):
    """A configuration whose own validator refuses without a word.

    It is here to make one thing reachable that is otherwise hard to reach: a
    validator that refuses without writing anything, which an application's own
    validator is free to do and which the editor still has to explain.
    """

    def declare_members(self) -> None:
        """Assign the one member, holding the one value that is accepted."""
        self.name: str = ACCEPTED_VALUE

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the step that refuses any other value of that member."""
        _ = stderr_file
        return [MemberValidationStep(member_names=['name'],
                                     validator=SilentRefusal())]


class HookCfg(Config):
    """A configuration whose constructor declares the change hook.

    An application declares `auto_ch_hook` and hands it on when it wants to
    read the records of a parse from an object of its own. The editor needs
    none of that and passes none, and this class is what says so: it records
    what it was constructed with, so a test can see that the editor offered it
    nothing and that the object still reports its own automatic changes.
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


VALIDATOR_RUNS: list[str] = []
"""Members that the validator of `CountedCfg` has been run on.

It is module level because a validation plan is asked for anew at every pass,
so a counter that belonged to a validator would be a different counter every
time. A test clears it before it reads it.
"""


# pylint: disable-next=too-few-public-methods
class CountingValidator(MemberValidator):
    """A member validator that records every run and refuses nothing.

    It is what shows how often reading one file runs the validators of the
    application, which matters because a load asks the configuration class
    more than one question and each of them costs a parse.
    """

    def validate_member(self, config: Config, member_name: str,
                        member_value: object,
                        stderr_file: TextIO = sys.stderr) -> Optional[object]:
        """Record this run and keep the value exactly as it is."""
        _ = (config, stderr_file)
        VALIDATOR_RUNS.append(member_name)
        return member_value


class CountedCfg(SampleCfg):
    """A configuration whose validator records every run of itself."""

    def declare_members(self) -> None:
        """Assign one member that the file may hold and one it may not."""
        self.name: str = 'counted'
        self.answer: int = 11

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the step that records a run for each of the members."""
        _ = stderr_file
        return [MemberValidationStep(member_names=['name', 'answer'],
                                     validator=CountingValidator())]


SUPPLIED_ANSWER = 3
"""Value that the rules for an older file supply for the number member.

It is deliberately neither declared default, so that a test can tell a value
the migration rules supplied from one the declared defaults filled in.
"""


class MigrateRules(ReadOldConfiguration):
    """How a file of the older shape of these tests becomes a current one.

    All three kinds of rule are here, because each of them is something the
    editor has to report differently: a key that changed its name, a key that
    is gone, and a value that only the current shape has.
    """

    def get_json_key_renames(self) -> list[RocfKeyRename]:
        """Return the one key of the older shape that has a new name."""
        return [RocfKeyRename(old='title', new='name')]

    def get_keys_to_prune(self) -> list[str]:
        """Return the one key of the older shape that no longer exists."""
        return ['trace']

    def get_missing_path_values(self) -> dict[ConfigPath, object]:
        """Return the value that only the current shape of a file holds."""
        return {('answer',): SUPPLIED_ANSWER}


class OldKeyCfg(SampleCfg):
    """A configuration that reads a file of its own older shape.

    Its constructor takes no hook, which is what most configuration classes
    look like and which costs it nothing: `Config` gives every object one of
    its own, and the editor reads the records from the object.
    """

    def declare_members(self) -> None:
        """Assign the members of the current shape of this configuration."""
        self.name: str = 'current name'
        self.answer: int = 7

    def _get_read_old_config(self) -> ReadOldConfiguration:
        """Return the rules that turn a file of the older shape into this."""
        return MigrateRules()


OLDER_DICT_KEY = 'bounds'
"""Name that the dict member of `DictKeyCfg` had in older files."""

OLDER_COUNT_KEY = 'count'
"""Name of the older value that the number member of today is derived from."""


def doubled(value: object) -> object:
    """Return twice one older number, as a migration of its meaning.

    An older file counted pairs where the current one counts items, which is
    the kind of change that needs a value migration rather than a move: the
    path and the value both change.

    Args:
        value: The number that the older file held.

    Returns:
        The number that the current shape holds instead.
    """
    assert isinstance(value, int)
    return 2 * value


class DictKeyRules(ReadOldConfiguration):
    """How an older file of `DictKeyCfg` becomes a file of today.

    Two keys inside one dict member were renamed, and the dict member itself
    was called something else. Renames are recursive and run before moves, so
    an older file records the two renames under the older name of the member,
    which is a path that no member of the current shape has.
    """

    def get_json_key_renames(self) -> list[RocfKeyRename]:
        """Return the two keys inside the dict member that were renamed."""
        return [RocfKeyRename(old='lo', new='low'),
                RocfKeyRename(old='hi', new='high')]

    def get_json_key_moves(self) -> list[RocfKeyMove]:
        """Return the older name that the dict member itself had."""
        return [RocfKeyMove(old_path=(OLDER_DICT_KEY,), new_path=('limits',))]

    def get_value_migrations(self) -> list[RocfValueMigration]:
        """Return the older value that the number member is derived from."""
        return [RocfValueMigration(
            old_path=(OLDER_COUNT_KEY,),
            writes=[RocfValueWrite(new_path=('answer',),
                                   transform_value=doubled)])]


class DictKeyCfg(ListCfg):
    """A configuration whose older files differ from it in three ways.

    It is the one class of these tests about which the load records more than
    one thing for one member, because two keys inside one dict member were
    renamed. It is the one whose records can name a path that is neither a
    member nor a key of the file, which is what a rule that runs before another
    rule moves the member leaves behind. And it is the one whose number member
    is produced by a value migration rather than moved, which the load records
    as its own kind of change.
    """

    def _get_read_old_config(self) -> ReadOldConfiguration:
        """Return the rules that turn an older file into this shape."""
        return DictKeyRules()


SUPPLIED_NOTE = 'a note that the current version does not keep'
"""Value that the rules below supply for a member nothing writes back."""


class NoteRules(ReadOldConfiguration):
    """Rules that supply a value which the configuration does not write."""

    def get_missing_path_values(self) -> dict[ConfigPath, object]:
        """Return the value supplied for the member that is not written."""
        return {('note',): SUPPLIED_NOTE}


# The one method is the whole of what a member validator is.
# pylint: disable-next=too-few-public-methods
class EmptyingValidator(MemberValidator):
    """A member validator that empties the member it is given."""

    # A member validator returns the value that is stored back into the
    # member, so returning None is the whole of what this one does and the
    # return is anything but useless.
    # pylint: disable-next=useless-return
    def validate_member(self, config: Config, member_name: str,
                        member_value: object,
                        stderr_file: TextIO = sys.stderr) -> Optional[object]:
        """Return None, which is what that member holds from now on."""
        _ = (config, member_name, member_value, stderr_file)
        return None


class SuppliedNoteCfg(SampleCfg):
    """A configuration whose supplied value reaches no key of its own file.

    The rules for an older file supply `note`, the validation plan then empties
    it, and the class leaves it out of JSON while it is None. So the load
    recorded a value that nothing the configuration writes holds, and there is
    no row it could be shown at. That is the one thing the editor can report
    only from the record, and only in the message.
    """

    def declare_members(self) -> None:
        """Assign one ordinary member and the one that is not written."""
        self.name: str = 'noted'
        self.note: Optional[str] = None

    def _omit_none_from_json(self) -> list[str]:
        """Return the member that is left out of JSON while it is None."""
        return ['note']

    def _get_read_old_config(self) -> ReadOldConfiguration:
        """Return the rules that supply the member that is not written."""
        return NoteRules()

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the step that empties what the rules supplied."""
        _ = stderr_file
        return [MemberValidationStep(member_names=['note'],
                                     validator=EmptyingValidator())]


class OldKeyHookCfg(HookCfg):
    """The same older shape, by a class whose constructor takes the hook.

    `HookCfg` declares `auto_ch_hook` and hands it on, and `OldKeyCfg` above
    does not. Everything else about the two of them is the same, so what one
    of them reports about a file and what the other reports about the same
    file have to be the same word for word.
    """

    def _get_read_old_config(self) -> ReadOldConfiguration:
        """Return the rules that turn a file of the older shape into this."""
        return MigrateRules()


class AltNameCfg(Config):
    """A configuration class that names its JSON text parameter its own way.

    `Config.__init__` calls the parameter `from_json_data_text`, and the
    example configuration classes that `config_as_json` ships call it
    `from_json_text` in the constructors they declare. Both names are in use,
    so the editor reads the signature rather than assuming one of them, and
    this class is the other one.
    """

    def __init__(self, from_json_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Declare the members and then apply the JSON under the other name."""
        self.name: str = 'other name'
        self.answer: int = 5
        super().__init__(from_json_data_text=from_json_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file)

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return no extra validation steps."""
        _ = stderr_file
        return []


class NoTextCfg(Config):
    """A configuration class whose constructor takes no JSON text at all.

    The editor never passes a JSON text to a constructor, so this class is
    constructed, edited, validated and saved exactly as any other: a buffer
    reaches it through `Config.parse_json`, which every configuration class
    has. It was refused until step 9, when the construction of a candidate
    became a copy of the object instead.
    """

    def __init__(self, stderr_file: TextIO = sys.stderr) -> None:
        """Declare the one member, and take no JSON source of any kind."""
        self.name: str = 'no text'
        super().__init__(from_json_data_text=None, from_json_filename=None,
                         stderr_file=stderr_file)

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return no extra validation steps."""
        _ = stderr_file
        return []


SHOUTED = 'TEXT'
"""The value that `RoundTripCfg` declares, and the only one it accepts."""


def _shouted(value: object) -> str:
    """Return one piece of text, refusing it unless it is upper case."""
    text = str(value)
    if text != text.upper():
        raise ValueError(f'{text} is not upper case.')
    return text


def _muttered(value: object, path_text: str, stderr_file: TextIO) -> str:
    """Return one piece of text in lower case, for the file to hold."""
    _ = (path_text, stderr_file)
    return str(value).lower()


class RoundTripCfg(SampleCfg):
    """A configuration that cannot read back what it writes.

    Its parse converter refuses text that is not upper case and its serialize
    converter writes the text in lower case, so the file it writes is one it
    would refuse to read. That is a defect of such a class and not of the
    editor, and the editor has to report it rather than fall over it: the
    buffer it reads from this class is not a configuration of it.
    """

    def declare_members(self) -> None:
        """Assign the one member that the two converters disagree about."""
        self.label: str = SHOUTED

    def parse_converters(self) -> Optional[dict[str, ParseConverter]]:
        """Return the converter that refuses anything but upper case."""
        return {'label': ParseConverter(result_type=type(None), args={},
                                        func=_shouted)}

    def serialize_converters(self) -> SerializeConverters:
        """Return the converter that writes the text in lower case."""
        return {('label',): SerializeConverter(value_type=str, args={},
                                               func=_muttered)}


PICKED_NAME = 'picked'
"""Value of the text member that makes `picking_loader` choose `PickedCfg`."""


class PickedCfg(SampleCfg):
    """The class that a loader chooses when the values of a file say so.

    It holds exactly the members `FlatCfg` holds, so a file of either of them
    can be read as the other. That is what makes it possible to tell that one
    of them was chosen rather than the other, and it is what a save has to
    notice before it writes such a file.
    """

    def declare_members(self) -> None:
        """Assign the same two members that `FlatCfg` declares."""
        self.name: str = PICKED_NAME
        self.answer: int = 42


def picking_loader(*, from_json_data_text: Optional[str] = None,
                   from_json_filename: Optional[PathOrStr] = None,
                   ok_to_use_defaults: bool = False,
                   stderr_file: TextIO = sys.stderr) -> Config:
    """Return the class that the values of one JSON text select.

    This is a loader written by hand, which is what a class chosen by looking
    at the JSON needs: `derived_loader` constructs one class, and choosing
    which class is the whole of what this adds, so the rest is handed over to
    it. A call with no JSON source is answered with `FlatCfg`, because the
    protocol says a loader answers one and a configuration that does not exist
    yet has to be of some class.
    """
    picked = PICKED_NAME in (from_json_data_text or '')
    chosen = derived_loader(PickedCfg if picked else FlatCfg)
    return chosen(from_json_data_text=from_json_data_text,
                  from_json_filename=from_json_filename,
                  ok_to_use_defaults=ok_to_use_defaults,
                  stderr_file=stderr_file)


def exiting_loader(*, from_json_data_text: Optional[str] = None,
                   from_json_filename: Optional[PathOrStr] = None,
                   ok_to_use_defaults: bool = False,
                   stderr_file: TextIO = sys.stderr) -> Config:
    """End the program instead of refusing, as `config_as_json` itself does.

    `config_factory_from_json` ends the process when no matcher accepts the
    JSON it was given, so a loader written around it does that too. Inside an
    editor it would cost the user the whole session, so the editor turns it
    into a refusal like any other.
    """
    _ = (from_json_data_text, from_json_filename, ok_to_use_defaults,
         stderr_file)
    sys.exit(1)


def text_only_loader(*, from_json_data_text: Optional[str] = None,
                     from_json_filename: Optional[PathOrStr] = None,
                     ok_to_use_defaults: bool = False,
                     stderr_file: TextIO = sys.stderr) -> Config:
    """Return a configuration, refusing to answer without a JSON text.

    That is what `edit_cfg_json.ConfigLoader` says a loader does not do, so
    this is here to be refused: the editor asks a loader for the values of a
    configuration that does not exist yet, and a loader that answers with
    nothing leaves it with nothing to edit.
    """
    _ = (from_json_filename, ok_to_use_defaults)
    if from_json_data_text is None:
        raise ValueError('This loader needs a file.')
    return FlatCfg(from_json_data_text=from_json_data_text,
                   stderr_file=stderr_file)


class Marker:  # pylint: disable=too-few-public-methods
    """A value that is not a JSON value and has no converter of its own."""


class NoJsonCfg(SampleCfg):
    """A configuration whose value cannot be written as JSON.

    A class may leave part of its own writing to code outside itself, and
    `config_as_json` then refuses to serialize it. The editor reads the values
    it shows by serializing the configuration object, so such a class has
    nothing for the editor to show at all.
    """

    def declare_members(self) -> None:
        """Assign the one member whose value is no JSON value."""
        self.marker: object = Marker()


class ExtraArgCfg(SampleCfg):
    """A configuration whose constructor needs an argument of its own.

    The editor cannot construct this class, because it knows nothing about the
    extra argument. It can still be edited, validated and saved, because a
    buffer is applied to a copy of an object the application built; reading a
    file is the one thing that needs a `ConfigLoader`, and `extra_arg_loader`
    below is that loader for this class.
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


HOME_VALUE = 'bound home'
"""The extra constructor argument that `extra_arg_loader` binds."""

extra_arg_loader = derived_loader(partial(ExtraArgCfg, home=HOME_VALUE))
"""How an application would let the editor read a file of `ExtraArgCfg`.

`functools.partial` binds the argument that the editor knows nothing about, and
`derived_loader` makes the five keyword arguments of a loader out of the rest.
It is a module level name so that the programs of this library can be told it.
"""
