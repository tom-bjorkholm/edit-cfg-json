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


def _rows_from_json_text(json_text: str) -> tuple[MemberRow, ...]:
    """Return one row per member of a serialized configuration object.

    The rows keep the order of the JSON document. `config_as_json` writes
    its keys sorted, so that is the order in which the members appear in
    the configuration file, and not the order they are declared in.
    """
    members = json.loads(json_text)
    assert isinstance(members, dict)
    return tuple(MemberRow(name=name, value=value)
                 for name, value in members.items())


class EditModel:
    """The editable state of one `config_as_json.Config` object.

    The model does no input or output of its own and owns no event loop, so
    a backend can either be run by a convenience wrapper or be mounted as a
    widget by an application that already runs its own event loop.

    Values are held in JSON space, that is as they are written to the
    configuration file, so that an enum member is shown by its name and a
    value being typed does not have to be a valid Python value yet.

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
        self._rows = _rows_from_json_text(
            deepcopy(config).as_json_string(stderr_file=stderr_file))

    @property
    def config_type_name(self) -> str:
        """Return the class name of the edited configuration object."""
        return self._type_name

    @property
    def rows(self) -> Sequence[MemberRow]:
        """Return one row per configuration member, in file order.

        File order is sorted by member name, because that is how
        `config_as_json` writes the file the user edits.
        """
        return self._rows
