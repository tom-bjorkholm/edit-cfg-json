#! /usr/bin/env python3
"""Tests for editing a configuration whose members hold lists and dicts.

What is tested here is the whole of what step 10 of the delivery plan added
to the model: the tree of rows, editing a value inside a container, folding
one away, and what a validator that changes how many values a list holds
does to the rows.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import json
from config_as_json import ConfigPath, JsonType
import pytest
from edit_cfg_json import EditModel, MemberRow, can_fold, fold_hides, \
    model_as_text
from edit_cfg_json.tree import OPEN_AT_MOST
from .container_cfg import BigListCfg, ConfigDictCfg, ConfigListCfg, \
    EmptyCfg, KeyedEnumCfg, NestedCfg, NormalizeCfg, RangedListCfg, \
    SMALL_LIMIT, TreeCfg
from .sample_cfg import FlatCfg, ListCfg


def _row(model: EditModel, path: ConfigPath) -> MemberRow:
    """Return the row of one node of one model."""
    return {row.path: row for row in model.rows}[path]


def _paths(model: EditModel) -> list[ConfigPath]:
    """Return the path of every row of one model, in the order shown."""
    return [row.path for row in model.rows]


def _shown(model: EditModel) -> list[ConfigPath]:
    """Return the path of every row that is not folded away."""
    return [row.path for row in model.rows if row.shown]


def _written(out_file: Path) -> JsonType:
    """Return what one output file holds, as JSON space values."""
    value: JsonType = json.loads(out_file.read_text(encoding='UTF-8'))
    return value


def test_tree_of_rows() -> None:
    """Test a container inside a container is a tree of rows."""
    assert _paths(EditModel(TreeCfg())) == [
        ('rules',), ('rules', '0'), ('rules', '0', 'low'), ('rules', '1'),
        ('rules', '1', 'high'), ('groups',), ('groups', 'blue'),
        ('groups', 'blue', '0'), ('groups', 'red'), ('groups', 'red', '0'),
        ('groups', 'red', '1'), ('answer',)]


def test_depth_of_a_row() -> None:
    """Test a node says how far inside a member of the configuration it is."""
    model = EditModel(TreeCfg())
    assert _row(model, ('rules',)).depth == 0
    assert _row(model, ('rules', '0')).depth == 1
    assert _row(model, ('rules', '0', 'low')).depth == 2


def test_empty_container_rows() -> None:
    """Test a container that holds nothing is one row that can be folded."""
    model = EditModel(EmptyCfg())
    assert _paths(model) == [('tags',), ('limits',)]
    assert _row(model, ('tags',)).foldable
    assert _row(model, ('tags',)).value_text == '0 elements'
    assert _row(model, ('limits',)).value_text == '0 entries'


def test_leaf_is_editable() -> None:
    """Test a value inside a container is edited like any other value."""
    model = EditModel(ListCfg())
    assert _row(model, ('tags', '0')).editable
    assert _row(model, ('limits', 'low')).editable
    assert not _row(model, ('tags',)).editable


def test_edit_reaches_member() -> None:
    """Test editing a value writes it up into the container that holds it."""
    model = EditModel(ListCfg())
    model.set_text(path=('tags', '1'), text='changed')
    assert _row(model, ('tags',)).value == ['first', 'changed']
    assert _row(model, ('tags',)).edited
    assert model.dirty


def test_deep_edit_reaches_up() -> None:
    """Test an edit deep inside reaches every container it is inside."""
    model = EditModel(TreeCfg())
    model.set_text(path=('rules', '0', 'low'), text='5')
    assert _row(model, ('rules', '0')).value == {'low': 5}
    assert _row(model, ('rules',)).value == [{'low': 5}, {'high': 9}]


def test_container_not_edited() -> None:
    """Test a container cannot be typed into, because it holds no value."""
    model = EditModel(ListCfg())
    with pytest.raises(ValueError, match='cannot be edited'):
        model.set_text(path=('tags',), text='[]')


def test_leaf_back_unmarked() -> None:
    """Test a value typed back to what it was leaves nothing to save."""
    model = EditModel(ListCfg())
    model.set_text(path=('tags', '0'), text='changed')
    model.set_text(path=('tags', '0'), text='first')
    assert not _row(model, ('tags',)).edited
    assert not model.dirty


def test_saves_the_whole_tree(tmp_path: Path) -> None:
    """Test what is written is what every row of the tree now holds."""
    out_file = tmp_path / 'out.json'
    model = EditModel(TreeCfg(), out_file=out_file)
    model.set_text(path=('groups', 'red', '1'), text='z')
    assert model.save().saved
    assert _written(out_file) == {'answer': 3,
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
    said = _row(model, ('shades', 'colour')).conversion
    assert 'PURPLE is not one of' in said


def test_list_unconverted() -> None:
    """Test a value inside a list never has a converter of its own."""
    assert _row(EditModel(ListCfg()), ('tags', '0')).converter is None


def test_nested_is_one_row() -> None:
    """Test a declared nested configuration object stays one row.

    It serializes as a dict and is not one, so this version leaves it alone.
    Step 11 of the delivery plan is what makes it a node of its own.
    """
    model = EditModel(NestedCfg())
    assert _paths(model) == [('inner',), ('limits',), ('limits', 'low')]
    assert not _row(model, ('inner',)).foldable
    assert not _row(model, ('inner',)).editable
    assert '<nested configuration, not editable yet>' in model_as_text(model)


def test_containers_open() -> None:
    """Test a container short enough for a window opens with the editor."""
    model = EditModel(ListCfg())
    assert _shown(model) == _paths(model)
    assert not _row(model, ('tags',)).folded


def test_long_one_folded() -> None:
    """Test a container of more rows than a window can spare opens folded."""
    model = EditModel(BigListCfg())
    assert _row(model, ('many',)).folded
    assert not _row(model, ('few',)).folded
    assert _shown(model) == [('many',), ('few',), ('few', '0'), ('few', '1')]
    assert len(_paths(model)) > OPEN_AT_MOST


def test_fold_hides_inside() -> None:
    """Test folding a container hides its rows and leaves its own."""
    model = EditModel(TreeCfg())
    model.toggle_fold(('rules',))
    assert ('rules',) in _shown(model)
    assert ('rules', '0') not in _shown(model)
    assert ('rules', '0', 'low') not in _shown(model)
    assert ('groups', 'red') in _shown(model)


def test_fold_is_a_toggle() -> None:
    """Test the same action opens a container that is folded away."""
    model = EditModel(ListCfg())
    model.toggle_fold(('tags',))
    model.toggle_fold(('tags',))
    assert _shown(model) == _paths(model)


def test_fold_needs_a_list() -> None:
    """Test a value that holds nothing cannot be folded."""
    model = EditModel(ListCfg())
    with pytest.raises(ValueError, match='is not a list or a dict'):
        model.toggle_fold(('answer',))


def test_fold_all_then_open() -> None:
    """Test the one action folds everything and then opens everything."""
    model = EditModel(TreeCfg())
    model.toggle_fold_all()
    assert _shown(model) == [('rules',), ('groups',), ('answer',)]
    model.toggle_fold_all()
    assert _shown(model) == _paths(model)


def test_fold_all_after_one() -> None:
    """Test folding everything while one is folded folds the rest as well.

    The action does what its name says, which is decided by whether anything
    is open, so a press always changes something.
    """
    model = EditModel(TreeCfg())
    model.toggle_fold(('rules',))
    model.toggle_fold_all()
    assert _shown(model) == [('rules',), ('groups',), ('answer',)]


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
    assert _written(out_file) == {'answer': 3, 'limits': {'high': 9, 'low': 1},
                                  'tags': ['changed', 'second']}


def test_validator_shortens() -> None:
    """Test a validator that removes a duplicate removes a row.

    The rows after such a pass are not the rows before it, which is why the
    model builds them again rather than writing into the ones it had.
    """
    model = EditModel(NormalizeCfg())
    assert _row(model, ('words', '0')).value == 'alpha'
    model.set_text(path=('words', '1'), text='alpha')
    assert _paths(model) == [('words',), ('words', '0'), ('words', '1')]
    assert model.validate().valid
    assert _paths(model) == [('words',), ('words', '0')]
    assert _row(model, ('words',)).value == ['alpha']
    assert _row(model, ('words',)).changed_by_validator


def test_normalized_edited() -> None:
    """Test a member a validator normalized is still worth saving."""
    model = EditModel(NormalizeCfg())
    model.set_text(path=('words', '1'), text='alpha')
    model.validate()
    assert model.dirty
    assert _row(model, ('words',)).edited


def test_fold_survives_pass() -> None:
    """Test a container the user folded is still folded after a pass."""
    model = EditModel(TreeCfg())
    model.toggle_fold(('rules',))
    assert model.validate().valid
    assert _row(model, ('rules',)).folded
    assert not _row(model, ('groups',)).folded


def test_list_of_configs() -> None:
    """Test a list of configuration objects is a container of one row each.

    That is the ordinary shape of a real configuration rather than a special
    case: the member is a container that can be folded and says how much it
    holds, and each object inside it is one row that this version cannot edit.
    """
    model = EditModel(ConfigListCfg())
    assert _paths(model) == [('outputs',), ('outputs', '0'),
                             ('outputs', '1'), ('answer',)]
    assert _row(model, ('outputs',)).foldable
    assert _row(model, ('outputs',)).value_text == '2 elements'
    assert not _row(model, ('outputs', '0')).foldable
    assert not _row(model, ('outputs', '0')).editable


def test_dict_of_configs() -> None:
    """Test a dict of configuration objects is the same thing by key."""
    model = EditModel(ConfigDictCfg())
    assert _paths(model) == [('outputs',), ('outputs', 'first')]
    assert _row(model, ('outputs',)).value_text == '1 entry'
    assert not _row(model, ('outputs', 'first')).foldable


def test_fold_config_list() -> None:
    """Test the member that holds them is folded like any other container."""
    model = EditModel(ConfigListCfg())
    model.toggle_fold(('outputs',))
    assert _shown(model) == [('outputs',), ('answer',)]


def test_configs_saved(tmp_path: Path) -> None:
    """Test what a nested object holds is written back exactly as it was.

    This version edits nothing inside one, so the whole of what it holds has
    to reach the file unchanged, whatever the rows above it say.
    """
    out_file = tmp_path / 'out.json'
    model = EditModel(ConfigListCfg(), out_file=out_file)
    model.set_text(path=('answer',), text='7')
    assert model.save().saved
    assert _written(out_file) == {'answer': 7,
                                  'outputs': [{'height': 6, 'width': 4},
                                              {'height': 6, 'width': 4}]}
