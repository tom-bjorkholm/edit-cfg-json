#! /usr/bin/env python3
"""Tests for the values a member takes, and for choosing one of them.

Two kinds of member have a set of values the editor knows the whole of: one
holding true or false takes the two words, and one whose class declares a
parse converter into an enum takes the names of that enum. Everything here is
driven by a real configuration class and its real converter, for the reason
`test_converting` gives: a test that read an enum itself would be testing
nothing about the editor.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from config_as_json import ConfigPath
import pytest
from edit_cfg_json import EditModel, Settings, row_chooses
from edit_cfg_json.converting import matched_choice
from edit_cfg_json.settings_config import SettingsConfig
from .container_cfg import FlagTreeCfg, KeyedEnumCfg, TreeCfg
from .model_helpers import row_at
from .sample_cfg import EnumCfg, FlagCfg, FlatCfg, HexCfg, IntEnumCfg, \
    ListCfg, OmitCfg, SampleCfg


def _answered_settings() -> Settings:
    """Return the settings of an application that answers when it is asked.

    Returns:
        What the editor would have chosen anyway, which is what a callable
        answering nothing in particular says.
    """
    return Settings()


BOOL_CHOICES = ('true', 'false')
"""The values a member holding true or false takes.

They are written out here rather than read from the core, in the same way as
every other text these tests expect, and their order matters: the first of
them is what such a member is given when its text means neither.
"""

ENUM_CHOICES: list[tuple[type[SampleCfg], ConfigPath, tuple[str, ...]]] = [
    (EnumCfg, ('colour',), ('RED', 'GREEN')),
    (IntEnumCfg, ('level',), ('LOWEST', 'LOW', 'HIGH'))]
"""One case per kind of enum member, with the names that class declares."""

NO_CHOICES: list[tuple[type[SampleCfg], ConfigPath]] = [
    (FlatCfg, ('name',)), (FlatCfg, ('answer',)), (HexCfg, ('mask',)),
    (ListCfg, ('tags',)), (ListCfg, ('tags', '0')),
    (OmitCfg, ('optional',))]
"""One case per node whose values are not a set the editor knows.

Text and a number can hold anything of their kind; a list is edited through
the rows below it; a converter of the application's own says nothing about
which values there are; an element of a list of text has no converter at all,
because `config_as_json` applies one to the values of a dict and to nothing
else; and a member holding nothing is given a value by a control of its own
rather than by a pull-down.
"""


@pytest.mark.parametrize('config_type, path, expected', ENUM_CHOICES)
def test_enum_choices(config_type: type[SampleCfg], path: ConfigPath,
                      expected: tuple[str, ...]) -> None:
    """Test an enum member takes the names of its own enum class."""
    row = row_at(EditModel(config_type()), path)
    assert row.choices == expected
    assert row_chooses(row)


@pytest.mark.parametrize('path', [('checked',), ('plain',)])
def test_bool_choices(path: ConfigPath) -> None:
    """Test a member holding true or false takes the two words."""
    row = row_at(EditModel(FlagCfg()), path)
    assert row.choices == BOOL_CHOICES
    assert row_chooses(row)


@pytest.mark.parametrize('config_type, path', NO_CHOICES)
def test_no_choices(config_type: type[SampleCfg], path: ConfigPath) -> None:
    """Test every other node has no set of values and is typed into."""
    row = row_at(EditModel(config_type()), path)
    assert row.choices == ()
    assert not row_chooses(row)


def test_container_not_chosen() -> None:
    """Test a node the editor cannot edit is never chosen from a list.

    The containers here hold no such values in any case; what this is about is
    that being edited at all is asked first, so that a type which does say
    what its values are could not put a pull-down on a row that holds none.
    """
    model = EditModel(TreeCfg())
    for row in model.rows:
        if not row.editable:
            assert not row_chooses(row)


@pytest.mark.parametrize('path', [('flags', '0'), ('inner', 'enabled')])
def test_flags_inside_chosen(path: ConfigPath) -> None:
    """Test a value holding true or false is chosen wherever it sits.

    Neither of these is a member of the class that is being edited: one is an
    element of a list and the other a member of a nested object, and both take
    the two words because what a node holds is known at any depth.
    """
    assert row_chooses(row_at(EditModel(FlagTreeCfg()), path))


def test_dict_value_chosen() -> None:
    """Test the value of a dict key an enum converter reaches is chosen.

    `config_as_json` applies a parse converter while it decodes an object, so
    the converter of `colour` reaches the value of every dictionary key of
    that name. The pull-down follows the converter and reaches it too.
    """
    model = EditModel(KeyedEnumCfg())
    assert row_chooses(row_at(model, ('shades', 'colour')))
    assert not row_chooses(row_at(model, ('shades', 'other')))


def test_settings_chosen() -> None:
    """Test the settings of the editor are themselves chosen from a list.

    Four of its members hold true or false, so the editor showing its own
    settings is the shortest thing to run that shows this working.
    """
    model = EditModel(SettingsConfig())
    chosen = {row.name for row in model.rows if row_chooses(row)}
    assert chosen == {'extension_enforced', 'priority_keys',
                      'confirm_overwrite', 'choose_values'}


def test_opens_choosing() -> None:
    """Test the editor opens with the values chosen rather than typed."""
    assert EditModel(EnumCfg()).choices_shown


def test_settings_start() -> None:
    """Test the application says which of the two the editor opens in."""
    typed = EditModel(EnumCfg(), settings=Settings(choose_values=False))
    assert not typed.choices_shown


def test_toggle_choices() -> None:
    """Test the switch answers for the rest of the session.

    A settings callable is asked again at each point of use, and the point of
    use of this answer is over once somebody has switched: what the user
    decided is not overruled by an application answering again.
    """
    model = EditModel(EnumCfg(), settings=_answered_settings)
    model.toggle_choices()
    assert not model.choices_shown
    model.toggle_choices()
    assert model.choices_shown


MATCHED = [('RED', 'RED'), ('red', 'RED'), ('G', 'GREEN'), ('PURPLE', ''),
           ('', ''), ('R', 'RED')]
"""What each text of an enum member means, and nothing where it means none.

The case is ignored and a beginning that only one name has is that name,
which is what `config_as_json` already does for the name of an enum member.
"""


@pytest.mark.parametrize('text, expected', MATCHED)
def test_matched_choice(text: str, expected: str) -> None:
    """Test which of the values a member takes one text means."""
    row = row_at(EditModel(EnumCfg()), ('colour',))
    assert matched_choice(converter=row.converter, value=text,
                          choices=row.choices) == expected


def test_completed_silently() -> None:
    """Test a text that means one value is given that value and nothing said.

    Completing a beginning is what the pull-down is for, and it is the same
    completion a validation pass makes, so there is nothing to tell the user
    that the row does not already say by being marked as edited.
    """
    model = EditModel(EnumCfg())
    model.toggle_choices()
    model.set_text(('colour',), 'GRE')
    model.toggle_choices()
    assert model.settle_choices() == ''
    assert row_at(model, ('colour',)).value == 'GREEN'
    assert model.dirty


REPLACED = [('PURPLE', 'PURPLE is no value this member takes'),
            ('', 'an empty field is no value this member takes')]
"""What is said about a text that means none of the values there are."""


@pytest.mark.parametrize('text, expected', REPLACED)
def test_replaced_reported(text: str, expected: str) -> None:
    """Test a text meaning no value is replaced and the user is told."""
    model = EditModel(EnumCfg())
    model.toggle_choices()
    model.set_text(('colour',), text)
    model.toggle_choices()
    message = model.settle_choices()
    assert expected in message
    assert 'colour' in message
    assert 'RED' in message
    assert row_at(model, ('colour',)).value == 'RED'


def test_replaced_bool() -> None:
    """Test a member holding neither word is given the first of the two."""
    model = EditModel(FlagCfg())
    model.toggle_choices()
    model.set_text(('plain',), 'yes')
    model.toggle_choices()
    assert 'plain' in model.settle_choices()
    assert row_at(model, ('plain',)).value is True


def test_bool_word_kept() -> None:
    """Test a member already holding one of the words is left alone.

    `false` is written into the buffer as soon as `f` is typed, so there is
    nothing for the switch to complete and nothing to tell anybody.
    """
    model = EditModel(FlagCfg())
    model.toggle_choices()
    model.set_text(('checked',), 'f')
    model.toggle_choices()
    assert model.settle_choices() == ''
    assert row_at(model, ('checked',)).value is False


def test_nothing_while_typing() -> None:
    """Test the values are left exactly as they are while they are typed.

    A field can hold a value being typed, and a name is no name of an enum
    member for most of the time it takes to type it. Anything that replaced
    such a text would make the field impossible to type in.
    """
    model = EditModel(EnumCfg())
    model.toggle_choices()
    model.set_text(('colour',), 'PURPLE')
    assert model.settle_choices() == ''
    assert row_at(model, ('colour',)).value == 'PURPLE'


def test_settling_again() -> None:
    """Test asking twice replaces nothing a second time.

    That is what lets a backend ask wherever it is about to show a pull-down
    as well as when the user switches.
    """
    model = EditModel(EnumCfg())
    model.toggle_choices()
    model.set_text(('colour',), 'PURPLE')
    model.toggle_choices()
    assert model.settle_choices() != ''
    assert model.settle_choices() == ''


def test_drops_verdict() -> None:
    """Test a replaced value leaves the verdict saying nothing.

    A verdict is about the values that were there when it was reached, so one
    that stood while the buffer has changed since would be saying something
    untrue.
    """
    model = EditModel(EnumCfg())
    model.toggle_choices()
    model.set_text(('colour',), 'GREEN')
    assert model.validate().valid
    model.set_text(('colour',), 'PURPLE')
    model.toggle_choices()
    model.settle_choices()
    assert model.verdict is None


def test_verdict_kept() -> None:
    """Test a switch that changes no value leaves the verdict standing."""
    model = EditModel(EnumCfg())
    assert model.validate().valid
    model.toggle_choices()
    model.toggle_choices()
    assert model.settle_choices() == ''
    assert model.verdict is not None
