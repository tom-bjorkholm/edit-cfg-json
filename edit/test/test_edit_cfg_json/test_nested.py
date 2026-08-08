#! /usr/bin/env python3
"""Tests for editing a configuration built out of nested configuration objects.

What is tested here is what step 11 of the delivery plan added: a declared
nested `Config` object is a node with a class and a docstring of its own, its
members are the rows below it, and everything inside it belongs to its own
class rather than to the class holding it.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import pytest
from edit_cfg_json import EditModel, model_as_text, row_describes, \
    row_description, row_value_text
from .model_helpers import row_at, row_paths, shown_paths, written
from .container_cfg import ConfigDictCfg, ConfigListCfg, DeepConfigCfg, \
    InnerCfg, NestedCfg, NoDocNestedCfg, NullNestedCfg, OmitNestedCfg, \
    OwnedEnumCfg, OwnedOptionCfg


def test_nested_holds_rows() -> None:
    """Test a nested object holds the rows of its own members."""
    model = EditModel(NestedCfg())
    assert row_paths(model) == [('inner',), ('inner', 'width'),
                                ('inner', 'height'), ('limits',),
                                ('limits', 'low')]
    assert row_at(model, ('inner',)).foldable
    assert not row_at(model, ('inner',)).editable
    assert row_at(model, ('inner', 'width')).editable


def test_row_says_the_class() -> None:
    """Test the row of a nested object says its class, not its entry count.

    It serializes as a dict and is not one, so saying how many entries it has
    would be showing it as something it is not.
    """
    row = row_at(EditModel(NestedCfg()), ('inner',))
    assert row.config_type is InnerCfg
    assert row.value_text == 'InnerCfg'
    assert row_value_text(row) == 'InnerCfg'


def test_class_is_real() -> None:
    """Test the class of the row is the class of the object that is there."""
    assert row_at(EditModel(NestedCfg()), ('inner',)).config_type is InnerCfg
    assert row_at(EditModel(NestedCfg()), ('limits',)).config_type is None


def test_open_says_docstring() -> None:
    """Test an open nested object says the whole docstring of its class."""
    model = EditModel(NestedCfg())
    row = row_at(model, ('inner',))
    assert row_describes(row)
    said = row_description(model=model, row=row)
    assert said.startswith('A nested configuration object with two members')
    assert 'It derives from the base class' in said


def test_folded_says_summary() -> None:
    """Test a folded nested object says the summary and no more.

    An object that is showing less of itself says less about itself, which is
    the same thing folding does to the values inside it.
    """
    model = EditModel(NestedCfg())
    model.toggle_fold(('inner',))
    said = row_description(model=model, row=row_at(model, ('inner',)))
    assert said == 'A nested configuration object with two members of its own.'


def test_hidden_says_nothing() -> None:
    """Test the explain toggle hides what a nested class says as well."""
    model = EditModel(NestedCfg())
    model.toggle_explanations()
    assert row_description(model=model, row=row_at(model, ('inner',))) == ''


def test_no_docstring_no_text() -> None:
    """Test a nested class without a docstring of its own says nothing.

    The docstring of its base class is deliberately not used in its place: a
    label describing something else would be worse than no label at all.
    """
    model = EditModel(NoDocNestedCfg())
    row = row_at(model, ('inner',))
    assert not row_describes(row)
    assert row_description(model=model, row=row) == ''


def test_fold_hides_members() -> None:
    """Test folding a nested object hides the rows of its members."""
    model = EditModel(NestedCfg())
    model.toggle_fold(('inner',))
    assert shown_paths(model) == [('inner',), ('limits',), ('limits', 'low')]


def test_edit_inside_object() -> None:
    """Test a member of a nested object is edited by the path to it."""
    model = EditModel(NestedCfg())
    model.set_text(path=('inner', 'width'), text='9')
    assert row_at(model, ('inner', 'width')).value == 9
    assert row_at(model, ('inner',)).value == {'height': 6, 'width': 9}
    assert model.dirty


def test_object_not_edited() -> None:
    """Test a nested object is edited through its rows and not as one."""
    model = EditModel(NestedCfg())
    with pytest.raises(ValueError, match='not a value'):
        model.set_text(path=('inner',), text='{}')


def test_saved_from_inside(tmp_path: Path) -> None:
    """Test a value edited inside a nested object reaches the file."""
    out_file = tmp_path / 'out.json'
    model = EditModel(NestedCfg(), out_file=out_file)
    model.set_text(path=('inner', 'height'), text='11')
    assert model.save().saved
    assert written(out_file) == {'inner': {'height': 11, 'width': 4},
                                 'limits': {'low': 1}}


def test_own_declared_order() -> None:
    """Test a nested object shows its members in its own declared order.

    The dict it writes is sorted, so the file has `height` first and the
    editor has `width` first: the class that owns the members is what says
    in which order they are read.
    """
    model = EditModel(NestedCfg())
    assert row_paths(model)[1:3] == [('inner', 'width'), ('inner', 'height')]


def test_own_converter() -> None:
    """Test a parse converter belongs to the class that owns the subtree.

    Both classes have a member called `colour` and only the nested one
    declares a converter for it, so only the member inside the nested object
    is answered by that converter.
    """
    model = EditModel(OwnedEnumCfg())
    assert row_at(model, ('inner', 'colour')).converter is not None
    assert row_at(model, ('colour',)).converter is None


def test_own_converter_bad() -> None:
    """Test the refusal of a nested converter is shown at that member."""
    model = EditModel(OwnedEnumCfg())
    model.set_text(path=('inner', 'colour'), text='PURPLE')
    verdict = model.validate()
    assert not verdict.valid
    assert set(verdict.refused) == {('inner', 'colour')}
    assert 'RED, GREEN' in verdict.refused[('inner', 'colour')]


def test_own_optional_member() -> None:
    """Test which members may be left out belongs to the owning class.

    `note` is optional inside the nested object and mandatory in the class
    holding it, so only the one inside says that it may be left out.
    """
    model = EditModel(OwnedOptionCfg())
    said = 'left out of the file'
    assert said in row_at(model, ('inner', 'note')).description
    assert said not in row_at(model, ('note',)).description


def test_missing_object_row() -> None:
    """Test a declared member that holds no object says which class is gone."""
    model = EditModel(NullNestedCfg())
    row = row_at(model, ('inner',))
    assert row.config_type is InnerCfg
    assert not row.foldable
    assert not row.editable
    assert row.value_text == 'no InnerCfg'


def test_missing_not_edited() -> None:
    """Test no text typed into a field becomes a configuration object."""
    model = EditModel(NullNestedCfg())
    with pytest.raises(ValueError, match='not a value'):
        model.set_text(path=('inner',), text='{}')


def test_omitted_has_no_row() -> None:
    """Test a member the class leaves out of JSON has no row at all.

    Nothing is written for it, so there is nothing for a row to show, which
    is what any member a class omits already does.
    """
    assert row_paths(EditModel(OmitNestedCfg())) == [('answer',)]


def test_missing_object_saved(tmp_path: Path) -> None:
    """Test a member that holds no object is written as holding none."""
    out_file = tmp_path / 'out.json'
    model = EditModel(NullNestedCfg(), out_file=out_file)
    model.set_text(path=('answer',), text='5')
    assert model.save().saved
    assert written(out_file) == {'answer': 5, 'inner': None}


def test_list_of_configs() -> None:
    """Test every object of a list of them holds rows of its own.

    That is the ordinary shape of a real configuration rather than a special
    case: the member is a container that can be folded and says how much it
    holds, and each object inside it is a node with its own members.
    """
    model = EditModel(ConfigListCfg())
    assert row_paths(model) == [('outputs',), ('outputs', '0'),
                                ('outputs', '0', 'width'),
                                ('outputs', '0', 'height'), ('outputs', '1'),
                                ('outputs', '1', 'width'),
                                ('outputs', '1', 'height'), ('answer',)]
    assert row_at(model, ('outputs',)).value_text == '2 elements'
    assert row_at(model, ('outputs', '0')).value_text == 'InnerCfg'


def test_dict_of_configs() -> None:
    """Test a dict of configuration objects is the same thing by key."""
    model = EditModel(ConfigDictCfg())
    assert row_paths(model) == [('outputs',), ('outputs', 'first'),
                                ('outputs', 'first', 'width'),
                                ('outputs', 'first', 'height')]
    assert row_at(model, ('outputs',)).value_text == '1 entry'


def test_fold_config_list() -> None:
    """Test the member that holds them is folded like any other container."""
    model = EditModel(ConfigListCfg())
    model.toggle_fold(('outputs',))
    assert shown_paths(model) == [('outputs',), ('answer',)]


def test_deep_nesting() -> None:
    """Test a nested object inside a nested object holds rows as well."""
    model = EditModel(DeepConfigCfg())
    assert ('outputs', '0', 'parts', 'one', 'width') in row_paths(model)
    assert row_at(model, ('outputs', '0', 'parts', 'one')).value_text == \
        'InnerCfg'


def test_deep_edit_saved(tmp_path: Path) -> None:
    """Test a value edited at the bottom of a deep tree reaches the file."""
    out_file = tmp_path / 'out.json'
    model = EditModel(DeepConfigCfg(), out_file=out_file)
    model.set_text(path=('outputs', '0', 'parts', 'one', 'width'), text='42')
    assert model.save().saved
    assert written(out_file) == {
        'outputs': [{'label': 'deep',
                     'parts': {'one': {'height': 6, 'width': 42}}}]}


def test_configs_kept_on_save(tmp_path: Path) -> None:
    """Test what a nested object holds is written back exactly as it was."""
    out_file = tmp_path / 'out.json'
    model = EditModel(ConfigListCfg(), out_file=out_file)
    model.set_text(path=('answer',), text='7')
    assert model.save().saved
    assert written(out_file) == {'answer': 7,
                                 'outputs': [{'height': 6, 'width': 4},
                                             {'height': 6, 'width': 4}]}


def test_dump_shows_the_tree() -> None:
    """Test the text rendering shows a nested object as a node with rows."""
    printed = model_as_text(EditModel(NestedCfg()))
    assert 'inner: InnerCfg\n' in printed
    assert '    width = 4' in printed
    assert 'limits: 1 entry' in printed
