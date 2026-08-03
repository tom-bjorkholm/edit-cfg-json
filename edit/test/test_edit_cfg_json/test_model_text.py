#! /usr/bin/env python3
"""Tests for the plain text rendering of an edit model."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import pytest
from config_as_json import JsonType
from edit_cfg_json import EditModel, LoadReport, MemberRow, load_text, \
    model_as_text, model_title, row_marks, row_value_text, save_text, \
    verdict_text
from .sample_cfg import FlatCfg, ListCfg, NoneCfg, RangeCfg, RewriteCfg

UNKNOWN_LINE = 'validation: not validated'
"""Line that a rendering of a model nobody has validated ends with."""

VALID_LINE = 'validation: valid'
"""Line that a rendering of an accepted buffer ends with."""

LOAD_LINE = 'the file left something out'
"""Message of the load in the tests that render one."""

FILLED_REPORT = LoadReport(message=LOAD_LINE, filled=frozenset({'answer'}))
"""Report of a load that filled the number member in from the default."""

NO_FILE_LINE = 'save to: no file chosen yet'
"""Line that a rendering of a model with no destination ends with."""


def test_flat_text() -> None:
    """Test the rendering has one line per member and then the verdict."""
    assert model_as_text(EditModel(FlatCfg())) == \
        f'name = flat text\nanswer = 42\n{UNKNOWN_LINE}\n{NO_FILE_LINE}'


def test_text_has_no_quotes() -> None:
    """Test a string member is shown as the string and not as JSON text."""
    assert '"' not in model_as_text(EditModel(FlatCfg()))


def test_none_text() -> None:
    """Test a member holding None is rendered as JSON null."""
    assert 'name = null' in model_as_text(EditModel(NoneCfg()))


def test_container_text() -> None:
    """Test a list member and a dict member are named as not editable."""
    text = model_as_text(EditModel(ListCfg()))
    assert 'tags = <not editable yet: list>' in text
    assert 'limits = <not editable yet: dict>' in text
    assert 'answer = 3' in text


def test_edited_text() -> None:
    """Test an edited member is marked, and only that member."""
    model = EditModel(FlatCfg())
    model.set_text(path=('answer',), text='7')
    assert model_as_text(model) == (
        f'name = flat text\nanswer = 7 (edited)\n{UNKNOWN_LINE}\n'
        f'{NO_FILE_LINE}')


def test_edit_undone_text() -> None:
    """Test a member typed back to what it was is not marked as edited."""
    model = EditModel(FlatCfg())
    model.set_text(path=('answer',), text='7')
    model.set_text(path=('answer',), text='42')
    assert model_as_text(model) == \
        f'name = flat text\nanswer = 42\n{UNKNOWN_LINE}\n{NO_FILE_LINE}'


def test_invalid_value_text() -> None:
    """Test text that is not a number yet is shown as it was typed."""
    model = EditModel(FlatCfg())
    model.set_text(path=('answer',), text='not-a-number')
    assert 'answer = not-a-number (edited)' in model_as_text(model)


def test_model_title() -> None:
    """Test the model label is the class name while there is no change."""
    assert model_title(EditModel(FlatCfg())) == 'FlatCfg'


def test_dirty_model_title() -> None:
    """Test the model label is marked while there is something to save."""
    model = EditModel(FlatCfg())
    model.set_text(path=('name',), text='other text')
    assert model_title(model) == 'FlatCfg *'


def test_unknown_verdict_text() -> None:
    """Test a model nobody validated says so rather than saying nothing."""
    assert verdict_text(EditModel(FlatCfg())) == UNKNOWN_LINE


def test_valid_verdict_text() -> None:
    """Test an accepted buffer is reported with nothing added to it."""
    model = EditModel(FlatCfg())
    model.validate()
    assert verdict_text(model) == VALID_LINE


def test_invalid_verdict_text() -> None:
    """Test a refused buffer is reported with the diagnostics below it."""
    model = EditModel(RangeCfg())
    model.set_text(path=('answer',), text='500')
    model.validate()
    assert verdict_text(model) == (
        'validation: invalid\nInvalid configuration: '
        'Value 500 for answer is greater than maximum 100.')


def test_edited_verdict_text() -> None:
    """Test an edit puts the rendering back to not having been validated."""
    model = EditModel(FlatCfg())
    model.validate()
    model.set_text(path=('answer',), text='7')
    assert verdict_text(model) == UNKNOWN_LINE


def test_rewritten_text() -> None:
    """Test a member a validator rewrote is shown as rewritten."""
    model = EditModel(RewriteCfg())
    model.set_text(path=('name',), text='typed text')
    model.validate()
    assert model_as_text(model) == (
        f'name = Typed text (edited) (changed by validator)\n'
        f'{VALID_LINE}\n{NO_FILE_LINE}')


def test_verdict_before_save() -> None:
    """Test the verdict and then the saving end a rendering, in that order.

    That is the order in which a session reaches them: what the application
    makes of the values decides whether they can be written at all.
    """
    model = EditModel(FlatCfg())
    model.validate()
    assert model_as_text(model).splitlines()[-2:] == [VALID_LINE, NO_FILE_LINE]


@pytest.mark.parametrize('value, expected',
                         [(42, '42'), (1.5, '1.5'), (True, 'true'),
                          (False, 'false'), (None, 'null'),
                          ('text', 'text'), ('', ''),
                          ('with "quotes"', 'with "quotes"'),
                          ('Björkholm', 'Björkholm'),
                          ('  spaced  ', '  spaced  '), ('42', '42')])
def test_row_value_text(value: JsonType, expected: str) -> None:
    """Test a string shows as itself and every other scalar as its JSON."""
    row = MemberRow(path=('member',), value=value, original=value)
    assert row_value_text(row) == expected


@pytest.mark.parametrize('value, expected',
                         [('typed', 'typed'), (7, '7'), ('', '')])
def test_edited_value_text(value: JsonType, expected: str) -> None:
    """Test an edited member shows what it holds now, not what it held."""
    row = MemberRow(path=('member',), value=value, original=42)
    assert row_value_text(row) == expected


@pytest.mark.parametrize('value, rewritten, filled, expected',
                         [(42, False, False, ''),
                          (7, False, False, ' (edited)'),
                          (42, True, False, ' (changed by validator)'),
                          (7, True, False,
                           ' (edited) (changed by validator)'),
                          (42, False, True, ' (filled from default)'),
                          (7, False, True,
                           ' (filled from default) (edited)'),
                          (7, True, True,
                           ' (filled from default) (edited) '
                           '(changed by validator)')])
def test_row_marks(value: JsonType, rewritten: bool, filled: bool,
                   expected: str) -> None:
    """Test the marks of a member are shown together when several apply."""
    row = MemberRow(path=('member',), value=value, original=42,
                    changed_by_validator=rewritten, filled_from_default=filled)
    assert row_marks(row) == expected


def test_no_load_text() -> None:
    """Test a model built without a load has nothing to say about one."""
    assert load_text(EditModel(FlatCfg())) == ''


def test_load_text() -> None:
    """Test the message of the load is what the rendering reports."""
    assert load_text(EditModel(FlatCfg(), FILLED_REPORT)) == LOAD_LINE


def test_load_text_is_first() -> None:
    """Test the load comes first, because it explains the marks below it."""
    model = EditModel(FlatCfg(), FILLED_REPORT)
    assert model_as_text(model) == (
        f'{LOAD_LINE}\nname = flat text\n'
        f'answer = 42 (filled from default)\n{UNKNOWN_LINE}\n'
        f'{NO_FILE_LINE}')


def test_no_load_no_line() -> None:
    """Test a rendering with nothing to say about a load has no empty line."""
    assert model_as_text(EditModel(FlatCfg())).splitlines()[0] == \
        'name = flat text'


def test_no_destination_text() -> None:
    """Test a model with nowhere to write says so rather than saying nothing.

    "No file chosen yet" and "this file is waiting to be written" are two
    different states, and a user who cannot tell them apart cannot tell
    whether pressing Save will ask them something.
    """
    assert save_text(EditModel(FlatCfg())) == NO_FILE_LINE


def test_destination_text(tmp_path: Path) -> None:
    """Test a model that has a destination says where it would write."""
    out_file = tmp_path / 'out.json'
    assert save_text(EditModel(FlatCfg(), out_file=out_file)) == \
        f'save to: {out_file}'


def test_saved_text(tmp_path: Path) -> None:
    """Test the rendering says what saving did once it has been asked for."""
    out_file = tmp_path / 'out.json'
    model = EditModel(FlatCfg(), out_file=out_file)
    model.save()
    assert save_text(model) == f'Saved to {out_file}.'
    assert model_as_text(model).splitlines()[-1] == f'Saved to {out_file}.'


def test_refused_save_text(tmp_path: Path) -> None:
    """Test a refused save is reported where a successful one would be."""
    model = EditModel(RangeCfg(), out_file=tmp_path / 'out.json')
    model.set_text(path=('answer',), text='500')
    model.save()
    assert save_text(model) == \
        'These values are not valid, so they cannot be saved.'


def test_edit_after_save_text(tmp_path: Path) -> None:
    """Test an edit puts the rendering back to naming the destination."""
    out_file = tmp_path / 'out.json'
    model = EditModel(FlatCfg(), out_file=out_file)
    model.save()
    model.set_text(path=('answer',), text='7')
    assert save_text(model) == f'save to: {out_file}'


def test_saved_title(tmp_path: Path) -> None:
    """Test the model label loses its mark once there is nothing to save."""
    model = EditModel(FlatCfg(), out_file=tmp_path / 'out.json')
    model.set_text(path=('name',), text='other text')
    assert model_title(model) == 'FlatCfg *'
    model.save()
    assert model_title(model) == 'FlatCfg'
