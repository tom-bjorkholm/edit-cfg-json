#! /usr/bin/env python3
"""Configuration classes about the declared defaults and the load policy.

`config_as_json` fills in what a file leaves out at every depth when the
declared defaults may be used. Two of these classes are the ways a load still
fails over something that is not an unknown key: a nested object built by a
factory that is never told the defaults may be used, and a validator that
refuses a value with a plain `KeyError`.

The rest are about a constructor that takes the load policy, which the editor
gives the text of a file together with the policy: a class whose declared
values its own rule refuses, and a way of constructing any class that does not
take the text, which is what the editor does without that.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from typing import Optional, TextIO
import sys
from config_as_json import Config, ConfigNesting, ConfigNestingKind, \
    MemberValidationStep, MemberValidator, NestedConfigs, PathOrStr, \
    ValidationPlan
from .container_cfg import InnerCfg
from .sample_cfg import HIGHEST, RangeCfg, SampleCfg

KNOWN_NAMES = ('alpha', 'beta')
"""Names that the lookup of `LookupCfg` finds."""

UNKNOWN_NAME = 'No entry is named {name}.'
"""What the lookup of `LookupCfg` says about a name it does not find."""


def legacy_inner(*, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr,
                 member_name: Optional[str] = None) -> Config:
    """Construct the nested object the way a factory written for 1.8 does.

    It does not accept `ok_to_use_defaults`, so `config_as_json` calls it
    without it, and the object it builds is read strictly.
    """
    return InnerCfg(from_json_data_text=from_json_data_text,
                    from_json_filename=from_json_filename,
                    stderr_file=stderr_file, member_name=member_name)


class LegacyFactoryCfg(SampleCfg):
    """A configuration whose nested object comes from a legacy factory."""

    def declare_members(self) -> None:
        """Assign the nested object and one plain member."""
        self.inner: InnerCfg = InnerCfg()
        self.answer: int = 3

    def nested_configs(self) -> NestedConfigs:
        """Return the declaration naming the factory of the nested object."""
        # The factory deliberately lacks `ok_to_use_defaults`.
        return {'inner': ConfigNesting(
            kind=ConfigNestingKind.MEMBER, config_type=InnerCfg,
            factory_function=legacy_inner)}  # type: ignore[arg-type]


# pylint: disable-next=too-few-public-methods
class LookupRefuser(MemberValidator):
    """A validator that looks a name up and lets the `KeyError` through."""

    def validate_member(self, config: Config, member_name: str,
                        member_value: object,
                        stderr_file: TextIO = sys.stderr) -> Optional[object]:
        """Return the name when the lookup finds it, else raise `KeyError`."""
        _ = (config, member_name)
        assert isinstance(member_value, str)
        if member_value not in KNOWN_NAMES:
            message = UNKNOWN_NAME.format(name=member_value)
            print(message, file=stderr_file)
            raise KeyError(message)
        return member_value


class LookupCfg(SampleCfg):
    """A configuration whose one name has to be found by a lookup."""

    def declare_members(self) -> None:
        """Assign the name that is looked up."""
        self.name: str = 'alpha'

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the one step that looks the name up."""
        _ = stderr_file
        return [MemberValidationStep(member_names=['name'],
                                     validator=LookupRefuser())]


class BadDefaultCfg(RangeCfg):
    """A configuration whose declared number is one its own range refuses.

    It cannot be constructed holding its declared values, so it can read a
    file only when its constructor is given the text of the file and the load
    policy together, which never validates the declared values on their own.
    """

    def declare_members(self) -> None:
        """Assign a number above the highest that the range allows."""
        self.answer: int = HIGHEST + 1


def defaults_only(config_type: type[SampleCfg]) -> Callable[..., Config]:
    """Return a callable that constructs one class holding its declared values.

    It declares no JSON text parameter, so the editor never gives it the text
    of a file: it constructs the class first and applies the text afterwards,
    which is what it does for every class whose constructor does not take the
    load policy.

    Args:
        config_type: The class to construct.

    Returns:
        A callable that takes a diagnostics stream and nothing else.
    """
    def build(stderr_file: TextIO = sys.stderr) -> Config:
        """Construct the class holding its declared values."""
        return config_type(stderr_file=stderr_file)
    return build
