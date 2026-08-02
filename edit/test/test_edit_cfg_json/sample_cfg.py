#! /usr/bin/env python3
"""Configuration classes used by the tests of edit_cfg_json."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional, TextIO
import sys
from config_as_json import Config, MemberValidationStep, PathOrStr, \
    StrCaseChangeValidator, StrCaseSpec, StrPositionSpec, ValidationPlan


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
    object leaves that object alone.
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
