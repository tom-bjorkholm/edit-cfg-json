#! /usr/bin/env python3
"""Tests for a node declared as a `Literal`, a set of values the editor knows.

A `Literal` whose values are of one kind is offered as those values, exactly
as a member holding true or false is offered the two words: the same
pull-down, the same reading of a text, and the same refusal of a text that
names none of them, which is the editor's own because no converter the class
declares says anything about it. A `Literal` of more than one kind is nothing
the editor can use.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from config_as_json import ConfigPath, JsonType
import pytest
from edit_cfg_json import EditModel, row_chooses
from edit_cfg_json.descriptions import INFERRED_TEXT
from .choice_cfg import LiteralCfg
from .container_cfg import FlagTreeCfg
from .model_helpers import row_at

LAYOUT = ('layout',)
"""The member declared `Optional[Literal['compact', 'wide']]`."""

PORT = ('port',)
"""The member declared `Literal[8080, 8443]`."""

LITERAL_CHOICES: list[tuple[ConfigPath, tuple[str, ...]]] = [
    (LAYOUT, ('compact', 'wide')), (PORT, ('8080', '8443')),
    (('strict',), ('true',)), (('shapes', '0'), ('round', 'square'))]
"""Every node declared as a `Literal` of one kind, with what it offers.

A `Literal` of true alone offers true alone, and not the two words of a node
holding true or false; the element of a list is offered its values as a
member is.
"""


TALL_FILE = ('{"layout": "tall", "port": 8080, "strict": true, '
             '"shapes": ["round"], "style": "bo", "mixed": "a"}')
"""A file of that configuration whose layout is none of its values."""


def _model() -> EditModel:
    """Return a model of the configuration with one of each `Literal`."""
    return EditModel(LiteralCfg())


@pytest.mark.parametrize('path, expected', LITERAL_CHOICES)
def test_literal_choices(path: ConfigPath, expected: tuple[str, ...]) -> None:
    """Test a `Literal` of one kind is offered its values to choose from."""
    row = row_at(_model(), path)
    assert row.choices == expected
    assert row_chooses(row)


def test_mixed_not_chosen() -> None:
    """Test a `Literal` of two kinds is nothing usable, and is typed.

    Its type is the one its value has, and the line below it says why, as it
    does for every declaration the editor can make nothing of.
    """
    row = row_at(_model(), ('mixed',))
    assert row.choices == ()
    assert not row.types
    assert row.chosen_type.text == 'str'
    assert INFERRED_TEXT in row.description


@pytest.mark.parametrize('path, text, expected',
                         [(LAYOUT, 'wi', 'wide'),
                          (LAYOUT, 'COMPACT', 'compact'),
                          (PORT, '8443', 8443), (('strict',), 'T', True),
                          (('shapes', '0'), 'sq', 'square')])
def test_text_completed(path: ConfigPath, text: str,
                        expected: JsonType) -> None:
    """Test a text that names one value is that value, and is accepted."""
    model = _model()
    model.set_text(path, text)
    assert row_at(model, path).value == expected
    assert model.validate().valid


@pytest.mark.parametrize('path, text, expected',
                         [(LAYOUT, 'tall',
                           'tall is not one of: compact, wide'),
                          (PORT, '80', '80 is not one of: 8080, 8443'),
                          (PORT, 'http', 'http is not one of: 8080, 8443'),
                          (('strict',), 'false', 'false is not one of: true'),
                          (('shapes', '0'), 'oval',
                           'oval is not one of: round, square')])
def test_text_refused(path: ConfigPath, text: str, expected: str) -> None:
    """Test a text that names none of the values is refused at its node.

    It is refused when the field loses the focus and by a validation pass,
    in the words an enum member name that names no member is refused in. A
    number is matched as the number it is written as, so `80` is no
    beginning of `8080`.
    """
    model = _model()
    model.set_text(path, text)
    model.check_field(path)
    assert row_at(model, path).conversion == expected
    verdict = model.validate()
    assert not verdict.valid
    assert verdict.refused == {path: expected}


def test_refused_inside() -> None:
    """Test a node inside a nested object is refused by that object as well.

    Folding the object asks it about its own part of the buffer, where the
    path of the node does not begin with the object's, so what the editor
    knows about the node has to be handed on under the shorter path.
    """
    model = EditModel(FlagTreeCfg())
    path = ('inner', 'enabled')
    model.set_text(path, 'maybe')
    model.toggle_fold(('inner',))
    expected = 'maybe is not one of: true, false'
    assert row_at(model, path).subtree_refusal == expected
    assert row_at(model, ('inner',)).subtree_valid is False


def test_settled_to_value() -> None:
    """Test a text naming no value is given the one it most likely meant."""
    model = _model()
    model.set_text(LAYOUT, 'wode')
    told = model.settle_choices()
    assert row_at(model, LAYOUT).value == 'wide'
    assert told == ('layout: wode is no value this member takes, so it has '
                    'been given wide.')


def test_none_chosen() -> None:
    """Test choosing `None` takes the value away, and the `Literal` gives one.

    The value it is given back is the first the `Literal` allows, because
    nothing is remembered per type.
    """
    model = _model()
    model.set_text(LAYOUT, 'wide')
    model.set_type(LAYOUT, 'None')
    assert row_at(model, LAYOUT).value is None
    assert not row_chooses(row_at(model, LAYOUT))
    model.set_type(LAYOUT, "Literal['compact', 'wide']")
    assert row_at(model, LAYOUT).value == 'compact'
    assert row_chooses(row_at(model, LAYOUT))


def test_switched_named() -> None:
    """Test switching a text to a `Literal` keeps the value it names."""
    model = _model()
    model.set_type(('style',), "Literal['plain', 'bold']")
    row = row_at(model, ('style',))
    assert row.value == 'bold'
    assert row.choices == ('plain', 'bold')


def test_text_type_typed() -> None:
    """Test the text beside a `Literal` takes any text, and offers nothing."""
    model = _model()
    row = row_at(model, ('style',))
    assert row.chosen_type.text == 'str'
    assert row.choices == ()
    model.set_text(('style',), 'tall')
    assert model.validate().valid


def test_loaded_settled() -> None:
    """Test a value no `Literal` allows, read by the class, is refused.

    `config_as_json` checks no value against an annotation, so a class can
    hold such a value where an enum or a boolean never could. The editor
    refuses it at the member, and where the values are chosen gives it the
    value it most likely meant and says so.
    """
    model = EditModel(LiteralCfg(from_json_data_text=TALL_FILE))
    assert model.validate().refused == {
        LAYOUT: 'tall is not one of: compact, wide'}
    told = model.settle_choices()
    assert row_at(model, LAYOUT).value == 'compact'
    assert told == ('layout: tall is no value this member takes, so it has '
                    'been given compact.')
