#! /usr/bin/env python3
"""What reading one input file did to the values that it holds.

Reading a file can change what the values are, and from three directions: the
rules a configuration class declares for reading a file of an older format,
the normalization that parsing and validating do, and the declared defaults
filling in what the file left out. The user has to be told, because the values
on the screen are then not the values in the file, and an editor that said
nothing about that would look broken.

**What changed is found by comparing.** The values the load produced are
written back to JSON and compared with the text of the file, key by key. That
is exact, it needs nothing of the configuration class, and it covers all three
directions at once. It is the only one of the two mechanisms here that sees a
value which parsing or a validator normalized, so it stays the mechanism.

**Why it changed is asked of the load, which records it.**
`Config.auto_change_hook()` is the hook that `config_as_json` recorded the
automatic changes of the most recent parse into, and every configuration object
has one whether the application asked for it or not. Each record says what kind
of change it was, which path of the file it consumed and which path of the
configuration it produced, so the editor can say at the member itself what the
load did to it — which the comparison cannot: a key that was renamed is simply
gone from the file, and nothing in the file says which member it became.

**A record reaches a member or it reaches the message.** That one rule places
all of them. A record that produced a member of this configuration explains
that member and is shown there. A record that produced no member consumed a key
of the file that nothing here holds, so it joins the keys that saving leaves
out. A record that did neither supplied a value this configuration does not
write, and the message is the only place it can be named.

**The records are versioned, and the fallback is text.** `config_as_json` steps
`DATA_STRUCTURE_VERSION` whenever what it records changes, so a future version
records something this module was not written for. That is not worth a refusal:
the comparison still finds every changed member, and what the records would
have added is taken from `print_changes`, which is the library's own report and
is version independent. That text is shown as it stands and is never read.

**What the declared defaults filled in is asked of the parse.** It is the one
of the three that has a mark of its own, so it has to be exact, and the keys
of the file do not answer it: a key the rules for an older format renamed into
a member was in the file under another name, and a value those rules supplied
was in the file under no name at all. What the defaults filled in is exactly
what the key check of the parse was not given, so the parse is what is asked,
into a copy of the loaded object whose key check records and stops.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Iterable, Mapping, Sequence
from copy import deepcopy
from io import StringIO
from typing import NamedTuple, Optional, TextIO
import json
from config_as_json import Config, ConfigAutoChangeHook, \
    HookDataVersionError, JsonType, RocfChange, RocfChangeKind
from edit_cfg_json.constructing import parsed_config
from edit_cfg_json.leaf_value import canonical_text

HOOK_DATA_VERSION = 1
"""Version of the recorded automatic changes that this module reads.

`ConfigAutoChangeHook.DATA_STRUCTURE_VERSION` is stepped whenever the records
change, including purely additively, so that a reader of them is made to look
at what is new. This is the version that was looked at.
"""

WRITE_ERRORS = (TypeError, ValueError)
"""Every way in which writing the values of one load back to JSON can fail.

A class may leave part of its own writing to code outside itself, and there is
then nothing to compare the file with. Such a class cannot be shown at all,
because the editor reads the values it shows the very same way, so saying
nothing about the changes here is what leaves that refusal where it belongs.
"""

PARSE_ERRORS = (KeyError, TypeError, ValueError)
"""Every way the parse that records the keys can fail before it records them.

It cannot fail for a text that a load has already read, since the probe differs
from the object that read it in the one method that is not reached until the
keys have been recorded. It is caught because a mark is not worth an exception:
what the defaults filled in is then simply not claimed, and every member of it
is reported as one the load changed instead, which is true of it as well and
says less.
"""

KEY_METHOD = 'check_key_match'
"""Name of the method that the probe below has replaced with a recording."""

RECORDED = 'The keys of one parse were recorded.'
"""What the exception that carries those keys says for itself."""

NO_MEMBER = ''
"""What the records that reached no member of this configuration are under.

No member has it for a name, so it cannot collide with one, and grouping the
records that reached a member and the records that did not in one mapping is
what makes the rule of the module docstring one pass over them.
"""

REMOVING_KINDS = frozenset({RocfChangeKind.KEY_PRUNED,
                            RocfChangeKind.PATH_REMOVED,
                            RocfChangeKind.OLD_VALUE_DISCARDED,
                            RocfChangeKind.OLD_KEY_HANDLED})
"""The kinds of record that leave the value of an old path nowhere at all.

Only these are keys that saving leaves out. The kinds that are not here move a
value somewhere, and one of those that reached no member moved it to a path
this configuration does not write directly — a step on the way to a member of
it, which the rules for an older format take when a whole object moves. Such a
step is reported at the member the object became and nowhere else, because
naming it among the keys that are left out would be untrue of it.
"""


class FileChanges(NamedTuple):
    """What one load did to the file it read, beyond reading it.

    Every field is empty for a file whose values the load took exactly as they
    were, which is the ordinary case and the one in which the editor says
    nothing at all about the load.
    """

    filled: frozenset[str] = frozenset()
    """Members whose value the declared defaults of the class supplied.

    Empty for a load that was not allowed to use the defaults at all, and
    empty for a file that held every declared key.
    """

    dropped: frozenset[str] = frozenset()
    """Paths of the file that this configuration does not write back.

    A key the rules for an older format removed is one of these, and so is one
    whose member the class leaves out of JSON while it is None. None of them
    has a row, because none of them is a member of this configuration, so the
    message is the only place they can be reported.
    """

    changed: frozenset[str] = frozenset()
    """Members whose value the load itself put there or altered.

    This is what the comparison found, so a member that a validator or the
    parsing normalized is here and nowhere else. A member the declared defaults
    filled in is deliberately not one of them: it is marked already, by a mark
    that says more than this one would, and one member carrying two marks about
    the same thing would be worse than either of them alone.
    """

    reasons: Mapping[str, tuple[RocfChange, ...]] = {}
    """What the load recorded about each member that it recorded anything for.

    These are the records that produced a member of this configuration, which
    is what lets the editor say at the member what was done to it rather than
    only that something was. A member can have more than one when the record is
    about a value inside it, so the records of one member are kept in the order
    the rules applied them.
    """

    unplaced: tuple[RocfChange, ...] = ()
    """Records that neither a member nor a key of the file accounts for.

    A value that the rules for an older format supplied for something this
    configuration does not write is what that means in practice. It consumed no
    key of the file and produced no member, so the message is the only place it
    can be named, and the record carries the value it supplied.
    """

    detail: str = ''
    """What the library says about its records, for a version not read here.

    It is empty whenever the records were read, and it is the report of
    `ConfigAutoChangeHook.print_changes` when they were not. It is shown as it
    stands and never read: which version records what is the library's to say,
    and a text that was parsed would be a second way of depending on it.
    """

    @property
    def anything(self) -> bool:
        """Return whether reading the file changed what the file said.

        What the declared defaults filled in is deliberately not one of the
        things that answer this. A file that did not hold every value is
        reported as the incomplete file it is, which is a different thing from
        a file that was read as something other than what it says.
        """
        return bool(self.dropped or self.changed or self.reasons
                    or self.unplaced or self.detail)


def _written(config: Config) -> Mapping[str, JsonType]:
    """Return the values that one loaded configuration would write to a file.

    The object is copied first, because writing it validates it and a member
    validator returns the value that is stored back into the member. What is
    said while it is written is dropped, because the load has already reported
    whatever there was to say about this file.

    Args:
        config: Configuration object that the load produced.

    Returns:
        One JSON space value per member that this object writes.

    Raises:
        TypeError: A value of this class is no JSON value.
        ValueError: This class refuses to write the values it holds.
    """
    own = deepcopy(config)
    written = json.loads(own.as_json_string(stderr_file=StringIO()))
    assert isinstance(written, dict)
    return written


def _held(text: str) -> Mapping[str, JsonType]:
    """Return the values that the text of one input file holds.

    The text has already been read as configuration by the time this is asked,
    so it is JSON and it is an object.

    Args:
        text: The whole text of the input file.

    Returns:
        One value per key of that file.
    """
    held = json.loads(text)
    assert isinstance(held, dict)
    return held


def _altered(written: Mapping[str, JsonType],
             held: Mapping[str, JsonType]) -> frozenset[str]:
    """Return the members whose value is not the one the file holds.

    A member whose key the file does not hold at all is one of them, because
    the value shown for it came from somewhere other than the file: the
    declared defaults, the rules for an older format, or a key that was
    renamed into it.

    Args:
        written: What the load would write back to a file.
        held: What the file holds.

    Returns:
        The names of the members that are not as the file has them.
    """
    return frozenset(name for name, value in written.items()
                     if name not in held
                     or canonical_text(value) != canonical_text(held[name]))


def _member(path: Optional[str], written: Mapping[str, JsonType]) -> str:
    """Return the member of this configuration that one path belongs to.

    A recorded path names a value and not always a member: it is written as
    `outputs[0][encoding]` for a value inside a nested configuration object,
    and the member of this configuration is the first step of it. A path inside
    a member is therefore about that member, which is as near as anything can
    get to it while the member is one row.

    Args:
        path: Path that one record produced, or None when it produced none.
        written: The members that this configuration writes.

    Returns:
        The member that path belongs to, and `NO_MEMBER` for a path that
        belongs to none of them.
    """
    name = '' if path is None else path.partition('[')[0]
    return name if name in written else NO_MEMBER


def _by_member(changes: Sequence[RocfChange],
               written: Mapping[str, JsonType]) \
        -> dict[str, list[RocfChange]]:
    """Return the records of one load, grouped by the member each produced.

    Args:
        changes: What the load recorded about the file it read.
        written: The members that this configuration writes.

    Returns:
        The records of each member by its name, with the records that produced
        no member of this configuration under `NO_MEMBER`.
    """
    grouped: dict[str, list[RocfChange]] = {}
    for change in changes:
        member = _member(change.new_path, written)
        grouped.setdefault(member, []).append(change)
    return grouped


def _version_read(hook: ConfigAutoChangeHook) -> bool:
    """Return whether the records of one hook are of the version read here.

    Args:
        hook: Hook that the load recorded its automatic changes into.

    Returns:
        Whether what it recorded means what this module reads it as.
    """
    try:
        hook.check_data_version(written_for=HOOK_DATA_VERSION)
    except HookDataVersionError:
        return False
    return True


def _printed(hook: ConfigAutoChangeHook) -> str:
    """Return the report that the library writes about its own records.

    Args:
        hook: Hook that the load recorded its automatic changes into.

    Returns:
        That report, and nothing at all when there was nothing to report.
    """
    said = StringIO()
    hook.print_changes(stderr_file=said)
    return said.getvalue().strip()


class _ParsedKeys(Exception):
    """The keys of one parse, carried out of the parse that recorded them.

    It is internal because it exists only to carry two lists of names out of
    one method of one throwaway object, and it is an exception because the
    parse it comes from is not wanted beyond that point.
    """

    def __init__(self, declared: Sequence[str], held: Sequence[str]) -> None:
        """Say which keys were declared and which the parsed data held.

        Args:
            declared: The members that the configuration class declares.
            held: The keys the data held once the rules for an older format
                had finished with it.
        """
        self.declared = tuple(declared)
        self.held = tuple(held)
        super().__init__(RECORDED)


def _record_keys(expected_keys: list[str], j_keys: list[str],
                 ok_to_use_defaults: bool, stderr_file: TextIO,
                 allowed_missing_keys: Optional[list[str]] = None) -> None:
    """Record the keys of one parse, and stop that parse there.

    This stands in for `Config.check_key_match` on the probe below, so the
    parameters are that method's and in its order, because that is how
    `Config.parse_json` calls it. There is no object among them for the same
    reason as in `validation`: an attribute of an object is not a bound method,
    and the real method is a static one in any case.

    Args:
        expected_keys: The members that the configuration class declares.
        j_keys: The keys of the data that the parse is about to apply.
        ok_to_use_defaults: Whether missing keys may keep their default, which
            is the caller's own answer and is not what is being asked here.
        stderr_file: Stream for diagnostics, which a check that refuses
            nothing writes nothing to.
        allowed_missing_keys: Keys that may be missing whatever the policy is,
            which a check that refuses nothing has no use for either.

    Raises:
        _ParsedKeys: Always, carrying the two sets of keys.
    """
    _ = (ok_to_use_defaults, stderr_file, allowed_missing_keys)
    raise _ParsedKeys(declared=expected_keys, held=j_keys)


def _filled(config: Config, text: str) -> frozenset[str]:
    """Return the members whose value the declared defaults supplied.

    A load that was allowed to fill in what the file left out cannot afterwards
    be asked which of its values came from the file, and the keys of the file
    do not answer it either: the rules for an older format may have renamed a
    key of the file into a member, or supplied a value for a member the file
    never had. What the defaults filled in is exactly what the key check of
    the parse was not given, so the parse is what is asked.

    The file is therefore parsed a second time, into a copy of the loaded
    object whose key check records what it was given and stops the parse there.
    Stopping is what keeps this from repeating anything: everything after the
    key check is what the real load has already done, so the application's own
    validators still run once, on the object that is really being edited. The
    copy records into a copy of the hook as well, so what the load recorded is
    left exactly as the load left it.

    Args:
        config: Configuration object that the load produced.
        text: The whole text of the input file.

    Returns:
        The names of the members that the declared defaults supplied, and
        nothing at all when the parse did not reach the key check.
    """
    try:
        parsed_config(config, text, stream=StringIO(), replace=KEY_METHOD,
                      method=_record_keys)
    except _ParsedKeys as keys:
        return frozenset(keys.declared) - frozenset(keys.held)
    except PARSE_ERRORS:
        return frozenset()
    return frozenset()


def _compared(config: Config, text: str,
              permissive: bool) -> tuple[FileChanges,
                                         Mapping[str, JsonType]]:
    """Return what comparing one load with its file found, and the members.

    Args:
        config: Configuration object that the load produced.
        text: The whole text of the input file.
        permissive: Whether the load was allowed to fill in what the file left
            out. A load that was not fills nothing in, so there is nothing to
            ask the parse about.

    Returns:
        What the comparison alone found, and the members that this
        configuration writes.

    Raises:
        TypeError: This class cannot write the values it holds.
        ValueError: This class refuses to write the values it holds.
    """
    written = _written(config)
    held = _held(text)
    filled = _filled(config=config, text=text) if permissive else frozenset()
    return FileChanges(filled=filled,
                       dropped=frozenset(held) - frozenset(written),
                       changed=_altered(written=written,
                                        held=held) - filled), written


def _consumed(records: Iterable[RocfChange]) -> frozenset[str]:
    """Return the paths of the file that one set of records took a value from.

    Args:
        records: Records of what the load did.

    Returns:
        The old path of each of them that has one.
    """
    return frozenset(change.old_path for change in records
                     if change.old_path is not None)


def _recorded(changes: FileChanges, hook: ConfigAutoChangeHook,
              written: Mapping[str, JsonType]) -> FileChanges:
    """Return what the comparison found, with what the load recorded added.

    A key of the file that a member received is taken out of the keys that
    saving leaves out. The comparison puts it there, because the member holds
    it under another name and the comparison cannot know that; the record can,
    and a key that is reported at its member is not also reported as one that
    nothing here holds.

    Args:
        changes: What comparing the load with its file found.
        hook: Hook that the load recorded its automatic changes into.
        written: The members that this configuration writes.

    Returns:
        The same, with every record placed at the member it produced, among
        the keys of the file that nothing here holds, or in the message.
    """
    if not _version_read(hook):
        return changes._replace(detail=_printed(hook))
    grouped = _by_member(hook.changes, written)
    loose = grouped.pop(NO_MEMBER, [])
    gone = [change for change in loose if change.kind in REMOVING_KINDS]
    placed = [change for records in grouped.values() for change in records]
    return changes._replace(
        dropped=(changes.dropped | _consumed(gone)) - _consumed(placed),
        reasons={name: tuple(records) for name, records in grouped.items()},
        unplaced=tuple(change for change in loose if change.old_path is None))


def file_changes(config: Config, text: str, permissive: bool) -> FileChanges:
    """Return what one successful load did to the file that it read.

    Args:
        config: Configuration object that the load produced. What the load
            recorded is read from this object, because every configuration
            object holds the hook of its own most recent parse whether the
            application asked for one or not.
        text: The whole text of the input file.
        permissive: Whether the load was allowed to fill in what the file left
            out.

    Returns:
        What the load did, with every field empty for a file that the load
        took exactly as it stood.
    """
    try:
        changes, written = _compared(config=config, text=text,
                                     permissive=permissive)
    except WRITE_ERRORS:
        return FileChanges()
    return _recorded(changes=changes, hook=config.auto_change_hook(),
                     written=written)
