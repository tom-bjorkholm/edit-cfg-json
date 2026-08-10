#! /usr/bin/env python3
"""Tests for editing a configuration whose members hold lists and dicts.

What is tested here is what a container is to the model: the tree of rows,
editing a value inside a container, folding one away, and what a validator that
changes how many values a list holds does to the rows.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import pytest
from edit_cfg_json import EditModel, can_fold, fold_hides, model_as_text
from edit_cfg_json.tree import OPEN_AT_MOST
from .model_helpers import row_at, row_paths, shown_paths, written
from .container_cfg import BigListCfg, EmptyCfg, GROUP_FORM, GrowingCfg, \
    KeyedEnumCfg, NormalizeCfg, RangedListCfg, SMALL_LIMIT, TreeCfg
from .sample_cfg import FlatCfg, ListCfg

GROWN_STAGE = 2
"""Stage that the tests of `GrowingCfg` ask a validation pass to fill in.

It is not the stage the class declares, so the entry the pass fills in is one
that the rows of the model had no node for at all.
"""

GROWN_PATH = ('groups', GROUP_FORM.format(stage=GROWN_STAGE))
"""Path of the container that a pass over `GrowingCfg` creates."""


def test_tree_of_rows() -> None:
    """Test a container inside a container is a tree of rows."""
    assert row_paths(EditModel(TreeCfg())) == [
        ('rules',), ('rules', '0'), ('rules', '0', 'low'), ('rules', '1'),
        ('rules', '1', 'high'), ('groups',), ('groups', 'blue'),
        ('groups', 'blue', '0'), ('groups', 'red'), ('groups', 'red', '0'),
        ('groups', 'red', '1'), ('answer',)]


def test_depth_of_a_row() -> None:
    """Test a node says how far inside a member of the configuration it is."""
    model = EditModel(TreeCfg())
    assert row_at(model, ('rules',)).depth == 0
    assert row_at(model, ('rules', '0')).depth == 1
    assert row_at(model, ('rules', '0', 'low')).depth == 2


def test_empty_container_rows() -> None:
    """Test a container that holds nothing is one row that can be folded."""
    model = EditModel(EmptyCfg())
    assert row_paths(model) == [('tags',), ('limits',)]
    assert row_at(model, ('tags',)).foldable
    assert row_at(model, ('tags',)).value_text == '0 elements'
    assert row_at(model, ('limits',)).value_text == '0 entries'


def test_leaf_is_editable() -> None:
    """Test a value inside a container is edited like any other value."""
    model = EditModel(ListCfg())
    assert row_at(model, ('tags', '0')).editable
    assert row_at(model, ('limits', 'low')).editable
    assert not row_at(model, ('tags',)).editable


def test_edit_reaches_member() -> None:
    """Test editing a value writes it up into the container that holds it."""
    model = EditModel(ListCfg())
    model.set_text(path=('tags', '1'), text='changed')
    assert row_at(model, ('tags',)).value == ['first', 'changed']
    assert row_at(model, ('tags',)).edited
    assert model.dirty


def test_deep_edit_reaches_up() -> None:
    """Test an edit deep inside reaches every container it is inside."""
    model = EditModel(TreeCfg())
    model.set_text(path=('rules', '0', 'low'), text='5')
    assert row_at(model, ('rules', '0')).value == {'low': 5}
    assert row_at(model, ('rules',)).value == [{'low': 5}, {'high': 9}]


def test_container_not_edited() -> None:
    """Test a container cannot be typed into, because it holds no value."""
    model = EditModel(ListCfg())
    with pytest.raises(ValueError, match='not a value'):
        model.set_text(path=('tags',), text='[]')


def test_leaf_back_unmarked() -> None:
    """Test a value typed back to what it was leaves nothing to save."""
    model = EditModel(ListCfg())
    model.set_text(path=('tags', '0'), text='changed')
    model.set_text(path=('tags', '0'), text='first')
    assert not row_at(model, ('tags',)).edited
    assert not model.dirty


def test_saves_the_whole_tree(tmp_path: Path) -> None:
    """Test what is written is what every row of the tree now holds."""
    out_file = tmp_path / 'out.json'
    model = EditModel(TreeCfg(), out_file=out_file)
    model.set_text(path=('groups', 'red', '1'), text='z')
    assert model.save().saved
    assert written(out_file) == {'answer': 3,
                                 'groups': {'blue': ['c'], 'red': ['a', 'z']},
                                 'rules': [{'low': 1}, {'high': 9}]}


def test_refusal_at_member() -> None:
    """Test what a validator of a container refused is shown at the member.

    A member validator is given the whole member, so what it refuses is about
    the whole member and never about one value inside it.
    """
    model = EditModel(RangedListCfg())
    model.set_text(path=('sizes', '1'), text=str(SMALL_LIMIT + 1))
    verdict = model.validate()
    assert not verdict.valid
    assert set(verdict.refused) == {('sizes',)}
    assert 'validation: invalid, see sizes' in model_as_text(model)


def test_nested_key_converted() -> None:
    """Test a dictionary key named after a converted member is converted.

    `config_as_json` applies a parse converter while it decodes an object, so
    it reaches that key too, and the editor says so where the user typed it
    rather than in a message about JSON.
    """
    model = EditModel(KeyedEnumCfg())
    model.set_text(path=('shades', 'colour'), text='PURPLE')
    model.check_field(('shades', 'colour'))
    said = row_at(model, ('shades', 'colour')).conversion
    assert 'PURPLE is not one of' in said


def test_list_unconverted() -> None:
    """Test a value inside a list never has a converter of its own."""
    assert row_at(EditModel(ListCfg()), ('tags', '0')).converter is None


def test_containers_open() -> None:
    """Test a container short enough for a window opens with the editor."""
    model = EditModel(ListCfg())
    assert shown_paths(model) == row_paths(model)
    assert not row_at(model, ('tags',)).folded


def test_long_one_folded() -> None:
    """Test a container of more rows than a window can spare opens folded."""
    model = EditModel(BigListCfg())
    assert row_at(model, ('many',)).folded
    assert not row_at(model, ('few',)).folded
    assert shown_paths(model) == [('many',), ('few',), ('few', '0'),
                                  ('few', '1')]
    assert len(row_paths(model)) > OPEN_AT_MOST


def test_fold_hides_inside() -> None:
    """Test folding a container hides its rows and leaves its own."""
    model = EditModel(TreeCfg())
    model.toggle_fold(('rules',))
    assert ('rules',) in shown_paths(model)
    assert ('rules', '0') not in shown_paths(model)
    assert ('rules', '0', 'low') not in shown_paths(model)
    assert ('groups', 'red') in shown_paths(model)


def test_fold_is_a_toggle() -> None:
    """Test the same action opens a container that is folded away."""
    model = EditModel(ListCfg())
    model.toggle_fold(('tags',))
    model.toggle_fold(('tags',))
    assert shown_paths(model) == row_paths(model)


def test_fold_needs_a_list() -> None:
    """Test a value that holds nothing cannot be folded."""
    model = EditModel(ListCfg())
    with pytest.raises(ValueError, match='is not a list or a dict'):
        model.toggle_fold(('answer',))


def test_fold_all_then_open() -> None:
    """Test the one action folds everything and then opens everything."""
    model = EditModel(TreeCfg())
    model.toggle_fold_all()
    assert shown_paths(model) == [('rules',), ('groups',), ('answer',)]
    model.toggle_fold_all()
    assert shown_paths(model) == row_paths(model)


def test_fold_all_after_one() -> None:
    """Test folding everything while one is folded folds the rest as well.

    The action does what its name says, which is decided by whether anything
    is open, so a press always changes something.
    """
    model = EditModel(TreeCfg())
    model.toggle_fold(('rules',))
    model.toggle_fold_all()
    assert shown_paths(model) == [('rules',), ('groups',), ('answer',)]


def test_open_all_opens() -> None:
    """Test opening everything opens what the editor started folded."""
    model = EditModel(BigListCfg())
    model.open_all()
    assert not row_at(model, ('many',)).folded
    assert shown_paths(model) == row_paths(model)
    assert fold_hides(model)


def _grown_stage(model: EditModel, stage: int) -> None:
    """Run one pass that fills in the labels of one stage of a model.

    Args:
        model: Model of a `GrowingCfg`, which fills in the stage it is told.
        stage: Stage to ask for, which is a container the model has no node
            for until the pass has run.
    """
    model.set_text(path=('stage',), text=str(stage))
    assert model.validate().valid


def test_new_one_folds() -> None:
    """Test a long container a pass created is folded the ordinary way.

    It is decided the way every container is decided when the editor opens,
    which is what a user looking at a window wants: one that would flood it
    starts folded, whatever created it.
    """
    model = EditModel(GrowingCfg())
    model.open_all()
    _grown_stage(model, GROWN_STAGE)
    assert row_at(model, GROWN_PATH).folded


def test_open_all_stays_open() -> None:
    """Test a buffer opened for good is open after a pass creates a container.

    That is what a program printing the buffer once needs: it validates before
    it prints, so a container the pass created would be folded away in the one
    printout there is.
    """
    model = EditModel(GrowingCfg())
    model.open_all(no_more_folding=True)
    _grown_stage(model, GROWN_STAGE)
    assert shown_paths(model) == row_paths(model)
    assert GROWN_PATH + ('0',) in shown_paths(model)


def test_open_all_holds_on() -> None:
    """Test folding by hand still works after everything was opened for good.

    What was asked for is that nothing folds itself, and not that the model
    stops answering: a container the user folded is what the user asked for,
    and a pass leaves it exactly as it was.
    """
    model = EditModel(GrowingCfg())
    model.open_all(no_more_folding=True)
    model.toggle_fold(('groups',))
    _grown_stage(model, GROWN_STAGE)
    assert row_at(model, ('groups',)).folded
    assert GROWN_PATH not in shown_paths(model)


def test_nothing_to_fold() -> None:
    """Test a configuration of plain values offers no folding at all."""
    model = EditModel(FlatCfg())
    assert not can_fold(model)
    assert not fold_hides(model)


def test_fold_name_follows() -> None:
    """Test what the fold action would do next is what the model says."""
    model = EditModel(ListCfg())
    assert can_fold(model)
    assert fold_hides(model)
    model.toggle_fold_all()
    assert not fold_hides(model)


def test_folded_is_saved(tmp_path: Path) -> None:
    """Test a change inside a folded container is still written.

    A container holds what its rows hold whether they are on the screen or
    not, so folding hides a change and never loses one.
    """
    out_file = tmp_path / 'out.json'
    model = EditModel(ListCfg(), out_file=out_file)
    model.set_text(path=('tags', '0'), text='changed')
    model.toggle_fold(('tags',))
    assert model.dirty
    assert model.save().saved
    assert written(out_file) == {'answer': 3, 'limits': {'high': 9, 'low': 1},
                                 'tags': ['changed', 'second']}


def test_validator_shortens() -> None:
    """Test a validator that removes a duplicate removes a row.

    The rows after such a pass are not the rows before it, which is why the
    model builds them again rather than writing into the ones it had.
    """
    model = EditModel(NormalizeCfg())
    assert row_at(model, ('words', '0')).value == 'alpha'
    model.set_text(path=('words', '1'), text='alpha')
    assert row_paths(model) == [('words',), ('words', '0'), ('words', '1')]
    assert model.validate().valid
    assert row_paths(model) == [('words',), ('words', '0')]
    assert row_at(model, ('words',)).value == ['alpha']
    assert row_at(model, ('words',)).changed_by_validator


def test_normalized_edited() -> None:
    """Test a member a validator normalized is still worth saving."""
    model = EditModel(NormalizeCfg())
    model.set_text(path=('words', '1'), text='alpha')
    model.validate()
    assert model.dirty
    assert row_at(model, ('words',)).edited


def test_fold_survives_pass() -> None:
    """Test a container the user folded is still folded after a pass."""
    model = EditModel(TreeCfg())
    model.toggle_fold(('rules',))
    assert model.validate().valid
    assert row_at(model, ('rules',)).folded
    assert not row_at(model, ('groups',)).folded
