#! /usr/bin/env python3
"""The user interface agnostic model of one editable configuration."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Sequence
from copy import deepcopy
from typing import NamedTuple, TextIO
import json
import sys
from config_as_json import Config, ConfigPath, JsonType
from edit_cfg_json.leaf_value import text_as_value, value_as_text, \
    values_differ

NOT_EDITABLE_ERROR = 'Member {name} cannot be edited by this version.'
"""Message of the error raised when a member cannot be edited."""


class MemberRow(NamedTuple):
    """One configuration member as it appears in the JSON file."""

    path: ConfigPath
    """Path that addresses this member in the model.

    Every path of a flat configuration has one step. The further steps that
    lists, dicts and nested configuration objects need arrive together with
    those, and no call site has to change when they do.
    """

    value: JsonType
    """Current value of the member in JSON space, as the user edits it."""

    original: JsonType
    """Value that this member had when the model was built.

    It is what the current value is compared against, and it is also the only
    type information that the model has. A PEP 526 annotation on an instance
    attribute is recorded nowhere at runtime, so the value that the
    configuration object holds is the only source of the type. Reading the
    type from the current value instead would not work: a number member that
    the user has half typed holds text for as long as the text is not a
    number yet, and the member would then stop being a number member.
    """

    changed_by_validator: bool = False
    """Whether a validation pass rewrote this value.

    This is storage for a flag that validation sets, which arrives in a later
    step. It belongs to the model rather than to a backend, so that two
    backends cannot end up showing it differently.
    """

    filled_from_default: bool = False
    """Whether a permissive load supplied this value.

    This is storage for a flag that loading sets, which arrives in a later
    step, and it belongs to the model for the same reason as the flag above.
    """

    @property
    def name(self) -> str:
        """Return the name of the member, the last step of its path."""
        return self.path[-1]

    @property
    def editable(self) -> bool:
        """Return whether this member is a scalar that can be edited.

        A list or a dict value is ordinary JSON structure that needs a tree
        of fields rather than a single field, which this version of the
        model does not have. Such a member is still reported as a row, so
        that no configuration member can silently go missing.
        """
        return not isinstance(self.original, (dict, list))

    @property
    def is_text(self) -> bool:
        """Return whether this member holds text.

        This is the difference between a value that is text and a value
        whose text is a rendering of it. The text of a text member is the
        value itself, while the text of a number is how the number is
        written.
        """
        return isinstance(self.original, str)

    @property
    def edited(self) -> bool:
        """Return whether the user changed this member.

        A member is changed when it would now be written to the file
        differently, and not when it merely was typed in. Typing a value
        back to what it was leaves nothing to save, and an editor that still
        claimed to have changes would be telling the user something untrue.
        """
        return values_differ(self.value, self.original)


def _ordered_names(config: Config, members: dict[str, JsonType]) -> list[str]:
    """Return the serialized member names in the order they are declared.

    The declaration order is the order in which the configuration class
    assigns its members, which `vars()` preserves. That is the order the
    application thinks about its configuration in, so it is the order the
    editor shows. The JSON document cannot supply it, because
    `config_as_json` writes its keys sorted.

    A member that the class omits from JSON while its value is `None` is
    not serialized and so gets no row. A serialized name that is not an
    attribute of the object is appended instead of dropped, so that no
    member can go missing whatever a validator or a converter did.
    """
    declared = [name for name in vars(config) if name in members]
    return declared + [name for name in members if name not in declared]


def _rows_from_config(config: Config, stderr_file: TextIO) -> list[MemberRow]:
    """Return one row per serialized member, in declaration order."""
    members = json.loads(config.as_json_string(stderr_file=stderr_file))
    assert isinstance(members, dict)
    return [MemberRow(path=(name,), value=members[name],
                      original=members[name])
            for name in _ordered_names(config=config, members=members)]


class EditModel:
    """The editable state of one `config_as_json.Config` object.

    The model does no input or output of its own and owns no event loop, so
    a backend can either be run by a convenience wrapper or be mounted as a
    widget by an application that already runs its own event loop.

    Leaf values are held in JSON space, so that an enum member is held as its
    name and a value being typed does not have to be a valid Python value
    yet. JSON space is about the kind of the value, not about its notation:
    a string member holds the string, and the quotes that the file format
    puts around it are added when the file is written and nowhere else.

    This version of the model handles scalar members only. A member whose
    value is a list or a dict is reported as a row that is not editable.
    """

    def __init__(self, config: Config,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Read the JSON space values of one configuration object.

        The object is deep copied before it is serialized, because
        `Config.as_json_string()` validates, and a member validator returns
        the value that is stored back into the member. Serializing the
        caller's object directly could therefore change it, and the editor
        never mutates the caller's configuration object.

        Args:
            config: Configuration object to edit. It is the source of both
                the member names and their values, and is not modified.
            stderr_file: Stream used for user-facing diagnostics.

        Raises:
            InvalidConfiguration: The configuration object is not valid.
            InvalidConfigurationValue: A member of the configuration object
                does not hold a valid value.
        """
        self._type_name = type(config).__name__
        self._rows = _rows_from_config(config=deepcopy(config),
                                       stderr_file=stderr_file)
        self._number = {row.path: number
                        for number, row in enumerate(self._rows)}

    @property
    def config_type_name(self) -> str:
        """Return the class name of the edited configuration object."""
        return self._type_name

    @property
    def rows(self) -> Sequence[MemberRow]:
        """Return one row per configuration member, in declaration order.

        Declaration order is the order the configuration class assigns its
        members in, and not the sorted order that the JSON file has. How
        the file is written is an implementation detail of saving; what the
        application declared is what the user thinks about.

        The rows are a snapshot. Editing a member replaces its row, so a row
        that a caller kept is the state at the time it was read.
        """
        return tuple(self._rows)

    @property
    def dirty(self) -> bool:
        """Return whether the buffer holds anything that is worth saving."""
        return any(row.edited for row in self._rows)

    def set_text(self, path: ConfigPath, text: str) -> None:
        """Set one member of the buffer from the text of an edit field.

        Text that the field already shows changes nothing, because it is not
        an edit. That is not only tidiness: a field posts a change when it is
        given its initial text, and a model that counted that as an edit
        would report unsaved changes before the user had touched anything.

        Args:
            path: Path of the member to set.
            text: Text that the edit field holds.

        Raises:
            KeyError: The path is not a member of this configuration.
            ValueError: The member is not one that this version can edit.
        """
        number = self._number[path]
        row = self._rows[number]
        if not row.editable:
            raise ValueError(NOT_EDITABLE_ERROR.format(name=row.name))
        if value_as_text(row.value) == text:
            return
        value = text_as_value(text=text, is_text_member=row.is_text)
        self._rows[number] = row._replace(value=value)
