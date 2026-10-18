#! /usr/bin/env python3
"""Configuration classes whose members let the user choose their type.

A member whose declaration allows more than one plain type, or a plain type
and `None`, holds the one the user chooses. These classes hold one of each
such declaration, and the classes whose parse converter refuses some of the
declared types, which are not offered for that reason.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Literal, Optional, TextIO
import sys
from config_as_json import Config, MemberValidationStep, MemberValidator, \
    ParseConverter, ValidationPlan
from .sample_cfg import Colour, SampleCfg


# One member per shape of declaration is the whole point of this class, so it
# has more of them than pylint likes one class to have.
# pylint: disable-next=too-many-instance-attributes
class ChoiceCfg(SampleCfg):
    """A configuration holding one member of each type that can be chosen."""

    def declare_members(self) -> None:
        """Assign one member per shape of choosable declaration."""
        self.width: int | str = 80
        self.ratio: int | float = 5
        self.flag: bool | str = True
        self.maybe: Optional[float] = None
        self.mode: Literal['fast', 'slow'] | int = 'fast'
        self.colour: Optional[Colour] = None
        self.levels: list[int | str] = [1, 'two', 3]
        self.sizes: list[int | float] = [1, 2]
        self.notes: list[Optional[str]] = ['x', None]
        self.hosts: Optional[list[str]] = None


class DigitsAreNumbers(MemberValidator):  # pylint: disable=R0903
    """A validator that makes a text of digits the number it spells."""

    def validate_member(self, config: Config, member_name: str,
                        member_value: object,
                        stderr_file: TextIO = sys.stderr) -> Optional[object]:
        """Return the number a text of digits spells, and anything else as is.

        Args:
            config: The configuration object that owns the member.
            member_name: Name of the member being validated.
            member_value: What that member holds.
            stderr_file: Stream used for user-facing diagnostics.

        Returns:
            The value that is stored back into the member.
        """
        _ = (config, member_name, stderr_file)
        if isinstance(member_value, str) and member_value.isdigit():
            return int(member_value)
        return member_value


class NumberingCfg(SampleCfg):
    """A configuration whose validator changes the type of one member."""

    def declare_members(self) -> None:
        """Assign the one member, holding a whole number."""
        self.width: int | str = 80

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the one rule that makes a text of digits a number."""
        _ = stderr_file
        return [MemberValidationStep(member_names=['width'],
                                     validator=DigitsAreNumbers())]


class ConvertedCfg(SampleCfg):
    """A configuration whose enum converter refuses some declared types.

    The converter `config_as_json` ships for an enum refuses every value that
    is not text, so `None` beside an enum the class writes as `null` and a
    whole number beside an enum are both types it would refuse. A member the
    class leaves out of the file while it holds nothing is never converted at
    all, so `None` is offered there.
    """

    def declare_members(self) -> None:
        """Assign one enum member beside `None` twice, and one beside `int`."""
        self.written: Optional[Colour] = Colour.RED
        self.omitted: Optional[Colour] = None
        self.mixed: Colour | int = Colour.RED

    def parse_converters(self) -> Optional[dict[str, ParseConverter]]:
        """Return the converter that turns a name into a member of `Colour`."""
        return {name: Config.get_converter_dict(Colour)
                for name in ('written', 'omitted', 'mixed')}

    def _omit_none_from_json(self) -> list[str]:
        """Return the member that is left out of JSON while it is None."""
        return ['omitted']


def _lenient_colour(value: object) -> Colour | int:
    """Return the member of `Colour` a name means, and a number as it is."""
    if isinstance(value, int):
        return value
    assert isinstance(value, str)
    return Colour[value]


class LenientCfg(SampleCfg):
    """A configuration whose own converter takes a whole number as well."""

    def declare_members(self) -> None:
        """Assign one enum member beside `int`."""
        self.mixed: Colour | int = Colour.RED

    def parse_converters(self) -> Optional[dict[str, ParseConverter]]:
        """Return the converter that takes a name or a number."""
        return {'mixed': ParseConverter(result_type=Colour,
                                        func=_lenient_colour, args={})}
