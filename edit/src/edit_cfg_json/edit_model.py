#! /usr/bin/env python3
"""The user interface agnostic model of one editable configuration."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Sequence
from copy import deepcopy
from typing import NamedTuple, TextIO
import json
import sys
from config_as_json import Config, JsonType


class MemberRow(NamedTuple):
    """One configuration member as it appears in the JSON file."""

    name: str
    """Name of the configuration member."""

    value: JsonType
    """Value of the member in JSON space, as it is written to the file."""

    @property
    def editable(self) -> bool:
        """Return whether this member is a scalar that can be edited.

        A list or a dict value is ordinary JSON structure that needs a tree
        of fields rather than a single field, which this version of the
        model does not have. Such a member is still reported as a row, so
        that no configuration member can silently go missing.
        """
        return not isinstance(self.value, (dict, list))

    @property
    def is_text(self) -> bool:
        """Return whether this member holds a string.

        This is the difference between a value that is text and a value
        whose text is a rendering of it. A string member is shown and
        edited as the string itself, while a number is shown as the text
        it is written as.
        """
        return isinstance(self.value, str)


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


def _rows_from_config(config: Config,
                      stderr_file: TextIO) -> tuple[MemberRow, ...]:
    """Return one row per serialized member, in declaration order."""
    members = json.loads(config.as_json_string(stderr_file=stderr_file))
    assert isinstance(members, dict)
    return tuple(MemberRow(name=name, value=members[name])
                 for name in _ordered_names(config=config, members=members))


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
        """
        return self._rows
