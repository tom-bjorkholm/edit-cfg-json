#! /usr/bin/env python3
"""The settings of the editor, written as a configuration class of its own.

`Settings` is what an application decides in Python. This is the same thing
written as a `config_as_json.Config`, so that it can be read from a file, shown
in this editor like any other configuration, and declared as one member of an
application's own configuration class.

**It mirrors `Settings` and does not derive from it.** Deriving is what the
"third-party parameter class" pattern of `config_as_json` is for, and it is
impossible here for one reason: `ActionSettings` declares a member called
`validate`, which would shadow `Config.validate()` on every object of the
bridged class. `config_as_json` calls that method while it constructs and
while it parses, so such a class cannot be built at all. That is why `Settings`
and `ActionSettings` stay frozen, which is what section 9.1 of `doc/design.md`
asks of them for reasons of its own.

**The key combinations are a dict of lists and not a nested object.** A nested
`Config` object is read whole — `config_as_json` constructs one from its own
JSON without the permissive flag of the parse around it — so every settings
file would have had to name every action. A dict member is filled in per key
instead, its keys are checked against the ones this class declares, and a
member validator completes what a file left out. So a settings file may name
one action and the editor still shows all of them.

**Nothing here restates what a valid setting is.** Each member validator hands
the value to `Settings` or `ActionSettings` and reports what the dataclass
refused, which is principle 1 of section 3 of `doc/design.md` applied to the
editor's own settings: there is one place that says a key combination cannot
belong to two actions, and it is the place the editor itself is built on.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Mapping
from dataclasses import fields
from typing import Optional, TextIO
import sys
from config_as_json import Config, ConfigPath, DictKeyValueTypesValidator, \
    IntFloatValidator, InvalidConfiguration, ListValueTypeValidator, \
    MemberValidationStep, MemberValidator, MemberValidatorSequence, \
    OptionalMemberValidator, PathOrStr, ValidationPlan, ValueTypeValidator
from edit_cfg_json.descriptions import Descriptions
from edit_cfg_json.settings import ActionSettings, MIN_BACKUPS, \
    NOT_AN_EXTENSION, NOT_A_SUFFIX, Settings, names_a_file, with_dot

UNKNOWN_ACTION = 'This editor has no action called {name}.'
"""Message of the refusal of an action name that this editor does not have."""

REFUSED_KEYS = '{name}: {reason}'
"""The same for the combinations, whose value is every action there is.

Writing the value out would name every action of the editor to say something
about two of them, and the sentence that `ActionSettings` refuses them with
names those two itself.
"""


def declared_actions() -> dict[str, list[str]]:
    """Return the key combinations of every action, as a file holds them.

    They are read from `ActionSettings` rather than written out again, so that
    an action added there is an action this configuration class has without
    anything here being changed, and so that the two cannot disagree about a
    default.

    Returns:
        The combinations of each action, by the name of that action.
    """
    declared = ActionSettings()
    return {field.name: list(getattr(declared, field.name))
            for field in fields(declared)}


class _ActionKeys(MemberValidator):  # pylint: disable=too-few-public-methods
    """Complete the actions a file left out, and refuse what they refuse.

    A settings file is a file somebody writes by hand to change one or two
    things, so what it does not name keeps the default of the editor. The
    completed value is what is stored back into the member, which is what makes
    the editor show every action of a file that named one of them, and what
    lets the combinations of the others be edited there.
    """

    def validate_member(self, config: Config, member_name: str,
                        member_value: object,
                        stderr_file: TextIO = sys.stderr) -> Optional[object]:
        """Return every action of the editor, with what this member says.

        Args:
            config: The configuration object that owns the member.
            member_name: Name of the member, which is `actions`.
            member_value: What the file or the edit buffer holds for it, whose
                keys and values were checked by the validator before this one.
            stderr_file: Stream used for user-facing diagnostics.

        Returns:
            The combinations of every action, by the name of that action.

        Raises:
            InvalidConfiguration: An action name is not one this editor has,
                or one combination is set for two actions.
        """
        _ = config
        assert isinstance(member_value, dict)
        complete = declared_actions()
        for name, keys in member_value.items():
            if name not in complete:
                raise _refusal(UNKNOWN_ACTION.format(name=name), stderr_file)
            complete[name] = list(keys)
        _built_actions(complete, member_name, stderr_file)
        return complete


def _built_actions(actions: Mapping[str, list[str]], member_name: str,
                   stderr_file: TextIO) -> ActionSettings:
    """Return one `ActionSettings` of these combinations, or refuse them.

    Args:
        actions: The combinations of every action, by the name of that action.
        member_name: Name of the member, which a refusal names.
        stderr_file: Stream used for user-facing diagnostics.

    Returns:
        What the editor would bind for these actions.

    Raises:
        InvalidConfiguration: One combination is set for two actions.
    """
    try:
        return ActionSettings(**{name: tuple(keys)
                                 for name, keys in actions.items()})
    except ValueError as error:
        raise _refusal(REFUSED_KEYS.format(name=member_name, reason=error),
                       stderr_file) from error


def _refusal(message: str, stderr_file: TextIO) -> InvalidConfiguration:
    """Return the refusal of one setting, having said what is wrong with it.

    Args:
        message: What the user has to be told about this setting.
        stderr_file: Stream used for user-facing diagnostics, which a
            validator writes to before it raises.

    Returns:
        The failure to raise where the setting was refused.
    """
    print(message, file=stderr_file)
    return InvalidConfiguration(message)


class _NamesAFile(MemberValidator):  # pylint: disable=too-few-public-methods
    """Refuse text that adds nothing to a file name, as `Settings` does.

    An extension and a backup suffix are both text that a file name is made
    from, and text which strips to nothing makes the same name it was added to.
    Whether one piece of text does that is asked of `settings.names_a_file`,
    which is the one place that rule is written down and is what
    `Settings.__post_init__` asks as well.
    """

    def __init__(self, refusal: str) -> None:
        """Say how this member is refused when it names no file.

        Args:
            refusal: Form of the message, which names the value.
        """
        super().__init__()
        self._refusal = refusal

    def validate_member(self, config: Config, member_name: str,
                        member_value: object,
                        stderr_file: TextIO = sys.stderr) -> Optional[object]:
        """Return one piece of text that names a file, or refuse it.

        Args:
            config: The configuration object that owns the member.
            member_name: Name of the member being validated.
            member_value: What the file or the edit buffer holds for it, whose
                type was checked by the validator before this one.
            stderr_file: Stream used for user-facing diagnostics.

        Returns:
            That text, unchanged.

        Raises:
            InvalidConfiguration: The text adds nothing to a file name.
        """
        _ = config, member_name
        assert member_value is None or isinstance(member_value, str)
        if member_value is not None and not names_a_file(member_value):
            raise _refusal(self._refusal.format(value=repr(member_value)),
                           stderr_file)
        return member_value


class _WithDot(MemberValidator):  # pylint: disable=too-few-public-methods
    """Give the extension its dot, as `Settings` does.

    Normalizing here as well as in `Settings` is what makes the editor show
    the extension that the application will really use, rather than the text
    that was typed for it.
    """

    def validate_member(self, config: Config, member_name: str,
                        member_value: object,
                        stderr_file: TextIO = sys.stderr) -> Optional[object]:
        """Return one extension beginning with its dot.

        Args:
            config: The configuration object that owns the member.
            member_name: Name of the member being validated.
            member_value: The extension, which names a file by now.
            stderr_file: Stream used for user-facing diagnostics.

        Returns:
            That extension with its dot, and None for a member holding none.
        """
        _ = config, member_name, stderr_file
        assert member_value is None or isinstance(member_value, str)
        return None if member_value is None else with_dot(member_value)


_ACTION_KEYS = MemberValidatorSequence(
    [DictKeyValueTypesValidator(key_type=str, value_type=list,
                                value_validator=ListValueTypeValidator(str)),
     _ActionKeys()])
"""What the key combinations of every action are checked with."""

_EXTENSION = MemberValidatorSequence(
    [OptionalMemberValidator(ValueTypeValidator(str)),
     _NamesAFile(NOT_AN_EXTENSION), _WithDot()])
"""What the extension of a configuration file is checked with."""

_SUFFIX = MemberValidatorSequence(
    [OptionalMemberValidator(ValueTypeValidator(str)),
     _NamesAFile(NOT_A_SUFFIX)])
"""What the suffix of a kept file is checked with.

It is not normalized, unlike the extension: a suffix that begins with a dot
and one that does not are both shapes an application asks for.
"""

_COUNT = MemberValidatorSequence(
    [ValueTypeValidator(value_type=int, not_allowed_type=bool),
     IntFloatValidator(min_value=MIN_BACKUPS, max_value=None,
                       allowed_values=None)])
"""What the number of kept files is checked with.

Keeping none of them is what an empty `backup_suffix` says, so a count below
one would be a second way of saying it that could disagree with the first.
"""

_FLAG = ValueTypeValidator(bool)
"""What a member holding true or false is checked with.

Nothing else is asked of these three: every value of the type is one the
editor acts on, so there is nothing for `Settings` to refuse about them.
"""


class SettingsConfig(Config):
    """What has been decided about the editor itself.

    Which key combinations run the actions of the editor, what a configuration
    file of this application is called, and how the file that a save writes
    over is looked after. It is the same set of answers as `Settings`, in the
    form that can be read from a file and edited in this editor.

    A file of these need name only what it changes: what it leaves out keeps
    the answer the editor would have chosen anyway, and the editor shows every
    setting whatever the file held.
    """

    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Declare every setting of the editor, and read the file there is.

        The declared values are read from `Settings` and `ActionSettings`
        rather than written out again, so that the default of a setting is
        stated once and the two cannot come to disagree.

        Args:
            from_json_data_text: Optional JSON text to parse directly.
            from_json_filename: Optional path to a JSON file to read.
            stderr_file: Stream used for user-facing diagnostics.
        """
        declared = Settings()
        self.actions: dict[str, list[str]] = declared_actions()
        self.file_extension: Optional[str] = declared.file_extension
        self.extension_enforced: bool = declared.extension_enforced
        self.backup_suffix: Optional[str] = declared.backup_suffix
        self.backup_count: int = declared.backup_count
        self.priority_keys: bool = declared.priority_keys
        self.confirm_overwrite: bool = declared.confirm_overwrite
        Config.__init__(self, from_json_data_text=from_json_data_text,
                        from_json_filename=from_json_filename,
                        stderr_file=stderr_file)

    def as_settings(self) -> Settings:
        """Return these values as the editor is given them.

        Returns:
            What this configuration says, as the frozen object every entry
            point of this library takes.

        Raises:
            ValueError: One key combination is set for two actions, which
                cannot happen for a validated object and can for one whose
                members were assigned by hand.
        """
        return Settings(actions=ActionSettings(
                            **{name: tuple(keys)
                               for name, keys in self.actions.items()}),
                        file_extension=self.file_extension,
                        extension_enforced=self.extension_enforced,
                        backup_suffix=self.backup_suffix,
                        backup_count=self.backup_count,
                        priority_keys=self.priority_keys,
                        confirm_overwrite=self.confirm_overwrite)

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return what every setting of the editor is checked against.

        Args:
            stderr_file: Stream used for user-facing diagnostics, which the
                validators of this plan are given when they run.

        Returns:
            One step per kind of setting there is.
        """
        _ = stderr_file
        return [MemberValidationStep(member_names=['actions'],
                                     validator=_ACTION_KEYS),
                MemberValidationStep(member_names=['file_extension'],
                                     validator=_EXTENSION),
                MemberValidationStep(member_names=['backup_suffix'],
                                     validator=_SUFFIX),
                MemberValidationStep(member_names=['backup_count'],
                                     validator=_COUNT),
                MemberValidationStep(
                    member_names=['extension_enforced', 'priority_keys',
                                  'confirm_overwrite'], validator=_FLAG)]


ACTION_DESCRIPTIONS: Mapping[str, str] = {
    'quit': 'Ends the editor. It writes nothing of its own, so it asks '
            'first when something has not been saved.',
    'validate': 'Asks the application what it makes of these values, '
                'without writing anything.',
    'save': 'Writes the output file, and leaves the editor open.',
    'save_as': 'Chooses an output file and then writes it.',
    'cancel': 'Leaves a question of the editor unanswered.',
    'explain': 'Shows or hides what the application says about the values.',
    'fold': 'Folds every list and dict away, or opens every one of them.',
    'find': 'Puts the cursor in the field that a search is typed into.',
    'find_next': 'Goes to the next member that the search reaches.'}
"""What each action of the editor is, by the name it is set under.

Every action of `ActionSettings` has an entry, and one that is added later
without one is described by the line that reaches every action instead.
"""

EVERY_ACTION = 'Key combinations that run one action of the editor.'
"""What is said about an action that has nothing said about it.

It is what the `[` selector reaches, so it is the whole of what is said below
an action added to `ActionSettings` and not to `ACTION_DESCRIPTIONS`, and it is
never seen beside one of those: a selector naming the action is the more
specific of the two and wins.
"""

_MEMBER_DESCRIPTIONS: Descriptions = {
    ('actions',): 'Which key combinations run the actions of the editor. '
                  'Combinations are written the way Textual names keys, in '
                  'lower case, with the modifiers ctrl, shift, alt and meta '
                  'joined by + before a character, a function key such as f1, '
                  'or a name such as escape or pageup. The first combination '
                  'of an action is the one a button or a footer names and the '
                  'rest work without being named, and an empty list takes the '
                  'keys away and leaves the action, which is still reached by '
                  'its button or its command palette entry.',
    ('actions', '['): EVERY_ACTION,
    ('file_extension',): 'What a configuration file of this application is '
                         'called, or null for no opinion. A value that does '
                         'not begin with a dot is given one.',
    ('extension_enforced',): 'Whether a file name with another extension is '
                             'refused. It says nothing while there is no '
                             'extension to enforce.',
    ('backup_suffix',): 'What the file that a save writes over is kept as, or '
                        'null to keep nothing. It is added to the whole name, '
                        'so .bak keeps xx.cfg as xx.cfg.bak.',
    ('backup_count',): 'How many of those are kept. One is kept under the '
                       'plain name, and two or more are numbered from _1, '
                       'which is the file that was written over last.',
    ('priority_keys',): 'Whether a key of the editor is acted on before the '
                        'field that has the focus is offered it. False is for '
                        'an application that has taken one of these '
                        'combinations for a widget of its own.',
    ('confirm_overwrite',): 'Whether the user is asked before an existing '
                            'file is written over, once per file per session.'}
"""What this class says about each member that is not one action."""

SETTINGS_DESCRIPTIONS: Descriptions = dict(_MEMBER_DESCRIPTIONS) | {
    ('actions', name): text for name, text in ACTION_DESCRIPTIONS.items()}
"""What this configuration class says about each of its own members.

It is what an application hands to the editor beside `SettingsConfig`, and an
application that has this class as one member of its own configuration puts
its own path in front of every one of these paths.
"""


def described_below(prefix: ConfigPath) -> Descriptions:
    """Return what this class says about its members, below one member.

    An application that declares a `SettingsConfig` as one member of its own
    configuration describes that member's members with this, because a
    description addresses the whole path to what it is about.

    Args:
        prefix: Path of the member that holds the `SettingsConfig`, which is
            `('editor',)` for a member called `editor`.

    Returns:
        The same descriptions, each of them below that member.
    """
    return {prefix + path: text for path, text in
            SETTINGS_DESCRIPTIONS.items()}
