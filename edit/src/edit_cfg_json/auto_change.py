#! /usr/bin/env python3
"""What reading one input file did to the values that it holds.

Reading a file can change what the values are, and from three directions: the
rules a configuration class declares for reading a file of an older format,
the normalization that parsing and validating do, and the declared defaults
filling in what the file left out. The user has to be told, because the values
on the screen are then not the values in the file, and an editor that said
nothing about that would look broken.

**What changed is found by comparing, and not by asking.** The values the load
produced are written back to JSON and compared with the text of the file, key
by key. That is exact, it needs nothing of the configuration class, and it
covers all three directions at once, which is why it is the mechanism rather
than the fallback: the report below is one that a class has to opt into, and
most classes do not.

**Why it changed is asked of the class, where the class answers.**
`ConfigAutoChangeHook` is what `config_as_json` reports its own automatic
changes through, and it reaches a class only where that class declares
`auto_ch_hook` and hands it on. What it adds is what the comparison cannot
know: the older keys the file was read with. A key that was renamed is simply
gone from the file, and nothing in the file says which member it became.

**What the declared defaults filled in is asked of the parse.** It is the one
of the three that has a mark of its own, so it has to be exact, and the keys
of the file do not answer it: a key the rules for an older format renamed into
a member was in the file under another name, and a value those rules supplied
was in the file under no name at all. What the defaults filled in is exactly
what the key check of the parse was not given, so the parse is what is asked,
by a throwaway subclass whose key check records and stops.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Mapping, Sequence
from copy import deepcopy
from io import StringIO
from typing import NamedTuple, Optional, TextIO
import json
from config_as_json import Config, ConfigAutoChangeHook, JsonType
from edit_cfg_json.constructing import built_config

WRITE_ERRORS = (TypeError, ValueError)
"""Every way in which writing the values of one load back to JSON can fail.

A class may leave part of its own writing to code outside itself, and there is
then nothing to compare the file with. Such a class cannot be shown at all,
because the editor reads the values it shows the very same way, so saying
nothing about the changes here is what leaves that refusal where it belongs.
"""

PARSE_ERRORS = (KeyError, TypeError, ValueError)
"""Every way the parse that records the keys can fail before it records them.

It cannot fail for a text that a load has already read, since the throwaway
subclass differs from the class that read it in the one method that is not
reached until the keys have been recorded. It is caught because a mark is not
worth an exception: what the defaults filled in is then simply not claimed,
and every member of it is reported as one the load changed instead, which is
true of it as well and says less.
"""

KEY_PROBE_NAME = 'RecordedKeys'
"""Name of the throwaway class that records the keys of one parse."""

RECORDED = 'The keys of one parse were recorded.'
"""What the exception that carries those keys says for itself."""


# Every method that a hook has is inherited, and the one method below is the
# whole reason this class exists.
# pylint: disable-next=too-few-public-methods
class ChangeReport(ConfigAutoChangeHook):
    """The automatic changes of one load, as the load itself reports them.

    `Config.__init__` deep copies the hook it is given and records into the
    copy, so a hook that is read afterwards would answer with nothing at all.
    This one is read afterwards, and `__deepcopy__` is how it says so: the
    object is a channel back to the editor, and a copy of a channel is the
    channel.
    """

    def __deepcopy__(self, memo: dict[int, object]) -> 'ChangeReport':
        """Return this very hook, so that the load reports to the editor.

        Args:
            memo: What `copy.deepcopy` has copied already, which a copy that
                copies nothing has no use for.

        Returns:
            This object, which is then the one the load records into.
        """
        _ = memo
        return self


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
    """Keys of the file that this configuration does not write back.

    A key the rules for an older format renamed or removed is one of these,
    and so is one whose member the class leaves out of JSON while it is None.
    None of them has a row, because none of them is a member of this
    configuration, so the message is the only place they can be reported.
    """

    changed: frozenset[str] = frozenset()
    """Members whose value the load itself put there or altered.

    A member the declared defaults filled in is deliberately not one of them.
    It is marked already, by a mark that says more than this one would, and
    one member carrying two marks about the same thing would be worse than
    either of them alone.
    """

    old_keys: tuple[str, ...] = ()
    """Older keys the load accepted, as the configuration class reported them.

    Empty for a class that does not declare the hook, and empty for a file
    that is in the current format. A key that was moved rather than renamed is
    reported as `old.path -> new.path`, which is what `config_as_json` puts
    there.
    """

    supplied: tuple[str, ...] = ()
    """Paths the rules for an older format supplied values for.

    These are the values that neither the file nor the declared defaults gave:
    the configuration class supplied them, because the file is too old to hold
    them at all.
    """

    @property
    def anything(self) -> bool:
        """Return whether reading the file changed what the file said.

        What the declared defaults filled in is deliberately not one of the
        things that answer this. A file that did not hold every value is
        reported as the incomplete file it is, which is a different thing from
        a file that was read as something other than what it says.
        """
        return bool(self.dropped or self.changed or self.old_keys
                    or self.supplied)


def _canonical(value: JsonType) -> str:
    """Return one value as the text that decides whether it is unchanged.

    The keys of a dictionary are sorted, because `config_as_json` writes them
    sorted while a file is written by hand, and a file that holds the same
    values in another order holds the same values. Everything else is compared
    as it is written, which is what tells `1` from `1.0` and from `true`: all
    three of them reach the file differently.

    Args:
        value: One value in JSON space.

    Returns:
        The text that stands for that value.
    """
    return json.dumps(value, sort_keys=True)


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
                     or _canonical(value) != _canonical(held[name]))


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

    This stands in for `Config.check_key_match` in the throwaway class below,
    so the parameters are that method's and in its order, because that is how
    `Config.parse_json` calls it.

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


def _filled(config_type: type[Config], text: str) -> frozenset[str]:
    """Return the members whose value the declared defaults supplied.

    A load that was allowed to fill in what the file left out cannot afterwards
    be asked which of its values came from the file, and the keys of the file
    do not answer it either: the rules for an older format may have renamed a
    key of the file into a member, or supplied a value for a member the file
    never had. What the defaults filled in is exactly what the key check of
    the parse was not given, so the parse is what is asked.

    The class is therefore parsed a second time, by a throwaway subclass whose
    key check records what it was given and stops the parse there. Stopping is
    what keeps this from repeating anything: everything after the key check is
    what the real load has already done, so the application's own validators
    still run once, on the object that is really being edited.

    Args:
        config_type: Class of the configuration that was loaded.
        text: The whole text of the input file.

    Returns:
        The names of the members that the declared defaults supplied, and
        nothing at all when the parse did not reach the key check.
    """
    probe = type(KEY_PROBE_NAME, (config_type,),
                 {'check_key_match': staticmethod(_record_keys)})
    assert issubclass(probe, Config)
    try:
        built_config(probe, stream=StringIO(), text=text)
    except _ParsedKeys as keys:
        return frozenset(keys.declared) - frozenset(keys.held)
    except PARSE_ERRORS:
        return frozenset()
    return frozenset()


def file_changes(config: Config, text: str, hook: ChangeReport,
                 permissive: bool) -> FileChanges:
    """Return what one successful load did to the file that it read.

    Args:
        config: Configuration object that the load produced.
        text: The whole text of the input file.
        hook: Hook the load was given, which a configuration class that
            declares it has reported its own automatic changes through.
        permissive: Whether the load was allowed to fill in what the file left
            out. A load that was not fills nothing in, so there is nothing to
            ask the parse about.

    Returns:
        What the load did, with every field empty for a file that the load
        took exactly as it stood.
    """
    try:
        written = _written(config)
    except WRITE_ERRORS:
        return FileChanges()
    held = _held(text)
    filled = _filled(config_type=type(config), text=text) if permissive \
        else frozenset()
    return FileChanges(filled=filled,
                       dropped=frozenset(held) - frozenset(written),
                       changed=_altered(written=written, held=held) - filled,
                       old_keys=tuple(hook.old_keys),
                       supplied=tuple(hook.rocf_val_keys))
