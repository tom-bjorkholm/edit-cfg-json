#! /usr/bin/env python3
"""Tests of adding, removing and moving the elements of a container.

What a node offers is tested first, because that is what a backend creates its
controls from and what the user is told when nothing can be offered. What each
of the three changes does to the buffer, to the rows and to the configuration
object of the session comes after it.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional
import pytest
from config_as_json import ConfigPath
from edit_cfg_json import EditModel, model_as_text, row_description
from edit_cfg_json.elements import BY_KEY_SCOPE, FIXED_KEYS, NO_PATTERN, \
    UNCHECKED_SCOPE
from .container_cfg import ByKeyCfg, ConfigDictCfg, ConfigListCfg, \
    ElementCfg, EmptyObjectsCfg, NullNestedCfg, OmitNestedCfg, TreeCfg
from .model_helpers import row_at, row_paths, written
from .sample_cfg import FlatCfg

TAGS: ConfigPath = ('tags',)
"""Path of the list of `ElementCfg` that a new element can be copied for."""

GROWS: ConfigPath = ('grows',)
"""Path of the empty list of `ElementCfg` whose type says its elements."""

SPARE: ConfigPath = ('spare',)
"""Path of the list of `ElementCfg` that nothing says anything about."""

OUTPUTS: ConfigPath = ('outputs',)
"""Path of the member that holds nested objects in the samples above."""

OMITTED_JSON = '{"inner": {"width": 4, "height": 6}, "answer": 3}'
"""A file that gives the omitted optional member of a sample an object.

The declared defaults leave it holding none, and a member that holds none and
is left out of JSON has no row, so this is the only way to reach the one shape
in which it has one.
"""


@pytest.mark.parametrize('path, extend, refusal',
                         [(TAGS, True, ''), (GROWS, True, ''),
                          (SPARE, False, NO_PATTERN),
                          (('limits',), False, FIXED_KEYS),
                          (('labels',), False, UNCHECKED_SCOPE)])
def test_offer_to_extend(path: ConfigPath, extend: bool, refusal: str) -> None:
    """Test each container says whether it can grow, and why it cannot.

    The five members of the sample are the five different answers: a list with
    an element to copy, an empty list whose declared type says what an element
    of it would be, one that nothing says anything about, an ordinary dict
    whose keys its class declares, and a dict whose key policy the application
    defines with validators of its own.
    """
    offer = row_at(model=EditModel(ElementCfg()), path=path).offer
    assert offer.extend is extend
    assert offer.refusal == refusal


def test_by_key_out_of_scope() -> None:
    """Test a dict with one named object in it says so and offers nothing."""
    offer = row_at(model=EditModel(ByKeyCfg()), path=('hooks',)).offer
    assert not offer.extend
    assert offer.refusal == BY_KEY_SCOPE


def test_refusal_explains() -> None:
    """Test why a container cannot grow is shown with the explanations.

    It says what this member is, in the same way as the line saying what kind
    of value a member holds, so a user who has asked for the explanations to
    go gets this out of the way with them.
    """
    model = EditModel(ElementCfg())
    row = row_at(model=model, path=('limits',))
    assert FIXED_KEYS in row_description(model=model, row=row)
    model.toggle_explanations()
    assert row_description(model=model, row=row) == ''


def test_value_offers_none() -> None:
    """Test an ordinary value neither grows nor says anything about it."""
    offer = row_at(model=EditModel(FlatCfg()), path=('answer',)).offer
    assert not offer.extend
    assert not offer.remove
    assert offer.refusal == ''


def test_declared_is_enough() -> None:
    """Test an empty list of objects can still be given one.

    What an element of it is comes from the declaration and not from what the
    member holds, so a declaration is enough where a container of plain values
    would have nothing to copy.
    """
    model = EditModel(EmptyObjectsCfg())
    assert row_at(model=model, path=OUTPUTS).offer.extend
    model.add_element(OUTPUTS)
    assert row_paths(model) == [OUTPUTS, (*OUTPUTS, '0'),
                                (*OUTPUTS, '0', 'width'),
                                (*OUTPUTS, '0', 'height')]


def test_added_is_a_node() -> None:
    """Test a new element of a list of objects is shown as the object it is.

    The tree finds the nested objects by walking the real ones, so an element
    that existed only in the buffer would be shown as the dictionary it
    serializes to. This is what says that the object was really made.
    """
    model = EditModel(ConfigListCfg())
    model.add_element(OUTPUTS)
    row = row_at(model=model, path=(*OUTPUTS, '2'))
    assert row.config_type is not None
    assert row.config_type.__name__ == 'InnerCfg'
    assert row.children == ((*OUTPUTS, '2', 'width'),
                            (*OUTPUTS, '2', 'height'))


def test_added_is_sorted() -> None:
    """Test a new entry of a dict appears where the sorted order puts it.

    A dict is written in the sorted order of its keys, so the order the rows
    are shown in is the order a save writes.
    """
    model = EditModel(ConfigDictCfg())
    model.add_element(path=OUTPUTS, key='alpha')
    assert row_paths(model)[1] == (*OUTPUTS, 'alpha')


def test_copy_is_its_own() -> None:
    """Test editing a new element does not reach what it was copied from."""
    model = EditModel(TreeCfg())
    model.add_element(('rules',))
    model.set_text(path=('rules', '2', 'low'), text='7')
    assert row_at(model=model, path=('rules', '0', 'low')).value == 1


def test_added_is_dirty() -> None:
    """Test adding an element is a change that is worth saving."""
    model = EditModel(ElementCfg())
    assert not model.dirty
    model.add_element(TAGS)
    assert model.dirty
    assert row_at(model=model, path=TAGS).edited


def test_added_is_not_written() -> None:
    """Test a row the user added is not marked as one a validator wrote.

    The rows are built again after a change of the elements exactly as they
    are after a validation pass, and only one of the two is a validator's
    work.
    """
    model = EditModel(ElementCfg())
    model.add_element(TAGS)
    assert not row_at(model=model, path=(*TAGS, '2')).changed_by_validator


@pytest.mark.parametrize('key, message',
                         [('', 'needs a key'), ('first', 'already holds')])
def test_key_is_checked(key: str, message: str) -> None:
    """Test a new entry needs a key of its own that the dict does not hold.

    A new entry that quietly took the place of an existing one would lose
    what the user had, so a key the dict already holds is refused rather than
    used.
    """
    model = EditModel(ConfigDictCfg())
    with pytest.raises(ValueError, match=message):
        model.add_element(path=OUTPUTS, key=key)


def test_typed_element_added() -> None:
    """Test a list its class declares empty grows by what its type says.

    There is nothing to copy an element from, so what an element of this list
    would be is read from `list[str]`, and the empty text is the one value of
    that kind which says no more than which kind it is.
    """
    model = EditModel(ElementCfg())
    model.add_element(GROWS)
    assert row_at(model=model, path=(*GROWS, '0')).value == ''


def test_list_takes_no_key() -> None:
    """Test an element of a list is refused a key rather than given one."""
    with pytest.raises(ValueError, match='no key'):
        EditModel(ElementCfg()).add_element(path=TAGS, key='named')


@pytest.mark.parametrize('path', [SPARE, ('limits',), ('labels',)])
def test_refused_extend(path: ConfigPath) -> None:
    """Test a container that offers nothing refuses to be given anything."""
    with pytest.raises(ValueError, match='Nothing can be added'):
        EditModel(ElementCfg()).add_element(path)


def test_removed_is_gone() -> None:
    """Test removing one element leaves the ones after it shifted down."""
    model = EditModel(ElementCfg())
    model.remove_element((*TAGS, '0'))
    assert row_paths(model)[:2] == [TAGS, (*TAGS, '0')]
    assert row_at(model=model, path=(*TAGS, '0')).value == 'second'


def test_shift_is_no_edit() -> None:
    """Test the elements a removal shifted are not reported as edited.

    Everything the buffer holds about a node is held under the path of that
    node, and an element of a list is addressed by where it is, so a removal
    moves what each row is compared against along with the values. Without
    that, removing the first element would report every element after it as
    edited by a user who touched none of them.
    """
    model = EditModel(ElementCfg())
    model.remove_element((*TAGS, '0'))
    assert not row_at(model=model, path=(*TAGS, '0')).edited


def test_entry_is_gone() -> None:
    """Test one entry of a dict of objects can be taken out of it."""
    model = EditModel(ConfigDictCfg())
    model.remove_element((*OUTPUTS, 'first'))
    assert row_paths(model) == [OUTPUTS]


def test_member_not_removed() -> None:
    """Test a member of a configuration object is not an element.

    Its members are the ones its class declares, and its class is what would
    have to be changed to have another one.
    """
    model = EditModel(ConfigListCfg())
    assert not row_at(model=model, path=(*OUTPUTS, '0', 'width')).offer.remove
    with pytest.raises(ValueError, match='not something that can be removed'):
        model.remove_element((*OUTPUTS, '0', 'width'))


def test_optional_added() -> None:
    """Test a declared member holding no object can be given one.

    No text typed into a field becomes a configuration object, so making one
    is adding, and the member then has the rows of the object it holds.
    """
    model = EditModel(NullNestedCfg())
    assert row_at(model=model, path=('inner',)).offer.extend
    model.add_element(('inner',))
    assert row_paths(model) == [('inner',), ('inner', 'width'),
                                ('inner', 'height'), ('answer',)]


def test_optional_cleared() -> None:
    """Test a declared optional member can be put back to holding none."""
    model = EditModel(NullNestedCfg())
    model.add_element(('inner',))
    model.remove_element(('inner',))
    assert row_paths(model) == [('inner',), ('answer',)]
    assert not model.dirty


def test_omitted_no_row() -> None:
    """Test a member the class leaves out of the file offers nothing.

    Such a member has no row at all while it holds no object, which is what
    any omitted member already does, so there is nothing to press to give it
    one. A class that writes `null` for it is what makes the member editable
    that way, and that is the class's decision rather than the editor's.
    """
    model = EditModel(OmitNestedCfg())
    assert row_paths(model) == [('answer',)]


def test_omitted_not_cleared() -> None:
    """Test an omitted member holding an object is not offered a clearing.

    It has a row while it holds one, and clearing it would take that row off
    the screen for good: the member would then be left out of the file, and
    the test above says that such a member cannot be given an object again.
    """
    held = OmitNestedCfg(from_json_data_text=OMITTED_JSON)
    model = EditModel(held)
    assert row_at(model=model, path=('inner',)).config_type is not None
    assert not row_at(model=model, path=('inner',)).offer.remove


def test_moved_changes_place() -> None:
    """Test one element of a list changes places with a neighbour."""
    model = EditModel(ElementCfg())
    model.move_element(path=(*TAGS, '0'), later=True)
    assert row_at(model=model, path=(*TAGS, '0')).value == 'second'
    assert row_at(model=model, path=(*TAGS, '1')).value == 'first'


def test_ends_do_not_move() -> None:
    """Test the first element cannot move up and the last cannot move down."""
    model = EditModel(ElementCfg())
    assert not row_at(model=model, path=(*TAGS, '0')).offer.earlier
    assert not row_at(model=model, path=(*TAGS, '1')).offer.later
    with pytest.raises(ValueError, match='cannot be moved'):
        model.move_element(path=(*TAGS, '0'), later=False)


def test_objects_move() -> None:
    """Test moving an element of a list of objects moves the object too.

    The rows of a nested object come from the object at that path, so an
    object that stayed where it was would leave the values of one element
    under the rows of another.
    """
    model = EditModel(ConfigListCfg())
    model.set_text(path=(*OUTPUTS, '0', 'width'), text='11')
    model.move_element(path=(*OUTPUTS, '0'), later=True)
    assert row_at(model=model, path=(*OUTPUTS, '1', 'width')).value == 11
    assert model.validate().valid


def test_added_reaches_file(tmp_path: Path) -> None:
    """Test what was added is validated and written like anything else."""
    out_file = tmp_path / 'added.json'
    model = EditModel(ConfigListCfg(), out_file=out_file)
    model.add_element(OUTPUTS)
    model.set_text(path=(*OUTPUTS, '2', 'width'), text='12')
    assert model.save().saved
    assert written(out_file) == {'answer': 3,
                                 'outputs': [{'width': 4, 'height': 6},
                                             {'width': 4, 'height': 6},
                                             {'width': 12, 'height': 6}]}


def test_dump_shows_added() -> None:
    """Test what was added is in the rendering the examples and tests read."""
    model = EditModel(ConfigListCfg())
    model.add_element(OUTPUTS)
    assert '2: InnerCfg' in model_as_text(model)


def _folded_of(model: EditModel, path: ConfigPath) -> Optional[bool]:
    """Return whether one node of one model is folded."""
    return row_at(model=model, path=path).folded


def test_fold_moves() -> None:
    """Test the fold of a container follows the element it belongs to.

    A container inside an element of a list is addressed through the index of
    that element, so a removal that shifts the elements has to take the fold
    state with it or the wrong element would be folded afterwards.
    """
    model = EditModel(TreeCfg())
    model.toggle_fold(('rules', '1'))
    assert _folded_of(model, ('rules', '1'))
    model.remove_element(('rules', '0'))
    assert _folded_of(model, ('rules', '0'))
