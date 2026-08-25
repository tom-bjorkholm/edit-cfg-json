#! /usr/bin/env python3
"""Configuration classes that read a file of their own older format.

They are in a module of their own rather than beside the flat ones, because
what a load did to the file it read is one subject of its own and because one
module of every sample configuration would be too long to read.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional, TextIO
import sys
from config_as_json import Config, ConfigAutoChangeHook, ConfigPath, \
    MemberValidationStep, MemberValidator, ReadOldConfiguration, \
    RocfKeyMove, RocfKeyRename, RocfValueMigration, RocfValueWrite, \
    ValidationPlan
from .sample_cfg import HookCfg, ListCfg, SampleCfg


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

NOTE_NAME = 'note'
"""Name of the member that those rules supply and the class never writes."""


class NoteRules(ReadOldConfiguration):
    """Rules that supply a value which the configuration does not write."""

    def get_missing_path_values(self) -> dict[ConfigPath, object]:
        """Return the value supplied for the member that is not written."""
        return {(NOTE_NAME,): SUPPLIED_NOTE}


class OwnNoteRules(ReadOldConfiguration):
    """Rules that supply the same value and record it themselves.

    `ConfigAutoChangeHook.rocf_missing_value_provided` is the entry point that
    an application calls for old data it handled itself, and it is the one that
    is not given the value: the library records what it inserted, and an
    application that inserted the value itself records only the path. So the
    editor knows what a value was supplied for and not what it was.
    """

    def post_process_json(self, json_data: dict[str, object],
                          auto_ch_hook: ConfigAutoChangeHook,
                          stderr_file: TextIO) -> dict[str, object]:
        """Put in the value the current shape needs, and record its path."""
        _ = stderr_file
        json_data[NOTE_NAME] = SUPPLIED_NOTE
        auto_ch_hook.rocf_missing_value_provided(NOTE_NAME)
        return json_data


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


class OwnNoteCfg(SuppliedNoteCfg):
    """The same configuration, whose rules record the supply themselves.

    What reaches the user differs by exactly one thing: the line naming what
    the older format needed says the path alone, because that is all the record
    of an application that supplied the value itself holds.
    """

    def _get_read_old_config(self) -> ReadOldConfiguration:
        """Return the rules that supply the member and record it by hand."""
        return OwnNoteRules()


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
