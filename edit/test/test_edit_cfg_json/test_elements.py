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
from config_as_json import ConfigPath, JsonType
from edit_cfg_json import EditModel, model_as_text, row_description
from edit_cfg_json.elements import BY_KEY_PATTERN, FIXED_KEYS, NO_DICT_YET, \
    NO_ENTRY_PATTERN, NO_PATTERN
from .container_cfg import ByKeyCfg, ByKeyDictCfg, ConfigDictCfg, \
    ConfigListCfg, DictPlaceCfg, ElementCfg, EmptyObjectsCfg, NullNestedCfg, \
    OmitNestedCfg, OnlyNamedCfg, TreeCfg, UncheckedCfg
from .model_helpers import row_at, row_paths, written
from .sample_cfg import FlatCfg, OmitKindsCfg

TAGS: ConfigPath = ('tags',)
"""Path of the list of `ElementCfg` that a new element can be copied for."""

GROWS: ConfigPath = ('grows',)
"""Path of the empty list of `ElementCfg` whose type says its elements."""

SPARE: ConfigPath = ('spare',)
"""Path of the list of `ElementCfg` that nothing says anything about."""

LABELS: ConfigPath = ('labels',)
"""Path of the dict whose keys `_unchecked_dicts` leaves to the class."""

OUTPUTS: ConfigPath = ('outputs',)
"""Path of the member that holds nested objects in the samples above."""

HOOKS: ConfigPath = ('hooks',)
"""Path of the dict where one named key holds a configuration object."""

MATRIX_0: ConfigPath = ('matrix', '0')
"""Path of the dict inside a list element its class declares an entry for."""

MATRIX_1: ConfigPath = ('matrix', '1')
"""Path of the dict inside a list element that its class declares empty."""

NAMED: ConfigPath = ('hooks', 'main')
"""Path of the key of that dict which the class declares an object at."""

ONE_ENTRY_JSON = ('{"hooks": {"main": {"width": 4, "height": 6}, '
                  '"note": "keep"}}')
"""A file that puts an ordinary entry into a dict that declares none.

The class of `OnlyNamedCfg` declares nothing but the key that holds an object,
so this is what makes that member extendable: what it holds now says what an
entry of it looks like where the class said nothing.
"""

NO_NAMED_JSON = '{"hooks": {"note": "nothing"}}'
"""A file of that class which holds no key for the declared object.

Nothing in `config_as_json` requires the key to be there, so this is the state
such a dict is in whenever the application has not written the object, and it
is the state the row has to be able to give the object back in.
"""

OMITTED_JSON = '{"inner": {"width": 4, "height": 6}, "answer": 3}'
"""A file that gives the omitted optional member of a sample an object.

The declared defaults leave it holding none, so this is how the state in which
it holds one is reached without pressing anything first.
"""


@pytest.mark.parametrize('path, extend, refusal',
                         [(TAGS, True, ''), (GROWS, True, ''),
                          (SPARE, False, NO_PATTERN),
                          (('limits',), False, FIXED_KEYS),
                          (LABELS, True, '')])
def test_offer_to_extend(path: ConfigPath, extend: bool, refusal: str) -> None:
    """Test each container says whether it can grow, and why it cannot.

    The five members of the sample are the five different answers: a list with
    an element to copy, an empty list whose declared type says what an element
    of it would be, one that nothing says anything about, an ordinary dict
    whose keys its class declares, and a dict whose key policy the application
    defines with validators of its own, which is the one dict of the five that
    nothing here checks.
    """
    offer = row_at(model=EditModel(ElementCfg()), path=path).offer
    assert offer.extend is extend
    assert offer.refusal == refusal


def test_by_key_offers_both() -> None:
    """Test both halves of a dict with one named object in it are offered.

    Nothing checks which keys such a member has, because `config_as_json`
    reads a member named in `nested_configs()` whole instead of matching it
    against the keys the class declares. So the member takes an entry of its
    own like any other dict, and the key that holds the object is a place
    beside those entries rather than one of them.
    """
    model = EditModel(ByKeyCfg())
    member = row_at(model=model, path=HOOKS).offer
    assert member.extend and member.keyed and member.refusal == ''
    named = row_at(model=model, path=NAMED).offer
    assert named.remove and named.cleared and not named.extend
    ordinary = row_at(model=model, path=(*HOOKS, 'note')).offer
    assert ordinary.remove and not ordinary.cleared


def test_named_key_cleared() -> None:
    """Test the named key of such a dict is put back to holding nothing.

    It keeps its row, which says which class is missing and offers to make
    one, exactly as a member that may hold no object does. Without the row
    there would be nowhere to ask for the object again.
    """
    model = EditModel(ByKeyCfg())
    model.remove_element(NAMED)
    row = row_at(model=model, path=NAMED)
    assert not row.is_object
    assert row.offer.extend
    assert row_paths(model) == [HOOKS, (*HOOKS, 'main'), (*HOOKS, 'note')]
    assert model.validate().valid


def test_named_key_given() -> None:
    """Test a dict with no such key is given the object it declares."""
    model = EditModel(ByKeyCfg(from_json_data_text=NO_NAMED_JSON))
    assert not row_at(model=model, path=NAMED).is_object
    model.add_element(NAMED)
    assert row_at(model=model, path=NAMED).is_object
    assert row_at(model=model, path=(*NAMED, 'width')).value == 4
    assert model.validate().valid


def test_named_key_no_file(tmp_path: Path) -> None:
    """Test the file of a cleared named key holds no such key at all.

    That is what holding nothing means for such a key: a member that may hold
    none is written as `null` or left out by its own class, and this one is
    simply not there.
    """
    out_file = tmp_path / 'out.json'
    model = EditModel(ByKeyCfg(), out_file=out_file)
    model.remove_element(NAMED)
    assert model.save().saved
    assert written(out_file) == {'hooks': {'note': 'nothing'}}


def test_by_key_entry_added() -> None:
    """Test a key that no declaration names is copied like any entry.

    What one of those holds is the same three questions a list element is
    answered by, asked of the entries that no declaration names, so the entry
    this class declares beside its named key is what a new one is.
    """
    model = EditModel(ByKeyCfg())
    model.add_element(path=HOOKS, key='extra')
    assert row_at(model=model, path=(*HOOKS, 'extra')).value == 'nothing'
    assert model.validate().valid


def test_by_key_entry_gone() -> None:
    """Test a key that no declaration names is taken out of the dict."""
    model = EditModel(ByKeyCfg())
    model.remove_element((*HOOKS, 'note'))
    assert row_paths(model) == [HOOKS, NAMED, (*NAMED, 'width'),
                                (*NAMED, 'height')]
    assert model.validate().valid


def test_named_key_is_taken() -> None:
    """Test the named key is asked for at its own row and not as an entry.

    It has a row whether the dict holds it or not, so a new entry under that
    name is a key the dict already holds, and the row beside the refusal is
    the one that makes the object.
    """
    model = EditModel(ByKeyCfg())
    model.remove_element(NAMED)
    with pytest.raises(ValueError, match='already holds'):
        model.add_element(path=HOOKS, key='main')


def test_by_key_file_pattern() -> None:
    """Test a file that holds an ordinary entry says what a new one is.

    What the class declares is asked first and what the member holds after it,
    so a dict that declares nothing but its named key can be given an entry as
    soon as a file has put one in it.
    """
    model = EditModel(OnlyNamedCfg(from_json_data_text=ONE_ENTRY_JSON))
    assert row_at(model=model, path=HOOKS).offer.extend
    model.add_element(path=HOOKS, key='another')
    assert row_at(model=model, path=(*HOOKS, 'another')).value == 'keep'
    assert model.validate().valid


def test_only_named_says_why() -> None:
    """Test a dict of nothing but named keys says why it takes no entry.

    Half of such a member is answered by the class each of its keys names and
    the other half by nothing at all, so the member says so and the key that
    holds an object is offered all the same.
    """
    model = EditModel(OnlyNamedCfg())
    member = row_at(model=model, path=HOOKS).offer
    assert not member.extend
    assert member.refusal == BY_KEY_PATTERN
    model.remove_element(NAMED)
    assert row_at(model=model, path=NAMED).offer.extend


def test_unchecked_grows() -> None:
    """Test a dict whose keys its class does not check takes an entry.

    `_unchecked_dicts` is how a class takes the declared-keys check away and
    defines the key policy of one member with validators of its own, so such a
    member is an ordinary container here. What a new entry of it holds is the
    three questions every other container is answered by, and the entry the
    class declares is the first of them.
    """
    model = EditModel(ElementCfg())
    model.add_element(path=LABELS, key='owner')
    assert row_at(model=model, path=(*LABELS, 'owner')).value == 'platform'
    assert model.validate().valid


def test_unchecked_shrinks() -> None:
    """Test an entry of such a dict is taken out and not merely cleared.

    Nothing checks which keys the member has, so its entries are elements of a
    container in both directions: one goes in under a key the user gives and
    one comes out again, leaving no row behind.
    """
    model = EditModel(ElementCfg())
    entry = (*LABELS, 'team')
    offer = row_at(model=model, path=entry).offer
    assert offer.remove and not offer.cleared
    model.remove_element(entry)
    assert entry not in row_paths(model)
    assert row_at(model=model, path=LABELS).value == {}
    assert model.validate().valid


def test_typed_entry() -> None:
    """Test an unchecked dict its class declares empty is extendable.

    Nothing it holds says what an entry of it would be, so the declared type
    of the member answers, exactly as it does for an empty list.
    """
    model = EditModel(UncheckedCfg())
    model.add_element(path=('plain',), key='first')
    assert row_at(model=model, path=('plain', 'first')).value == ''
    assert model.validate().valid


def test_no_entry_pattern() -> None:
    """Test an unchecked dict nothing says anything about says so.

    A member with no annotation, no declared entry and no entry of its own has
    none of the three answers, so it says so rather than being given a value
    that nobody ever mentioned.
    """
    offer = row_at(model=EditModel(UncheckedCfg()), path=('blank',)).offer
    assert not offer.extend
    assert offer.refusal == NO_ENTRY_PATTERN


def test_inside_unchecked() -> None:
    """Test a dict inside an unchecked member takes an entry as well.

    The whole of such a member is unchecked and not only its outermost
    dictionary, because the check returns at the member rather than recursing
    into it.
    """
    model = EditModel(UncheckedCfg())
    inner = ('deep', 'eu')
    assert row_at(model=model, path=inner).offer.keyed
    model.add_element(path=inner, key='tier')
    assert row_at(model=model, path=(*inner, 'tier')).value == 'platform'
    assert model.validate().valid


@pytest.mark.parametrize('path, grows, refusal',
                         [(MATRIX_0, True, ''), (MATRIX_1, True, ''),
                          (('regions', 'eu', '0'), True, ''),
                          (('regions',), False, FIXED_KEYS),
                          (('nested',), False, FIXED_KEYS),
                          (('nested', 'eu'), False, FIXED_KEYS),
                          (('zero_key',), False, FIXED_KEYS),
                          (('zero_key', '0'), False, FIXED_KEYS)])
def test_where_a_dict_sits(path: ConfigPath, grows: bool,
                           refusal: str) -> None:
    """Test what a dict offers follows from where it sits in the tree.

    `Config.check_dict_parse` is applied once per member and steps only into
    the dict values of that member, so a list between the member and the dict
    stops it and the dict below is an ordinary container. The ones that say why
    they cannot grow are the ones the check really reaches: a dict member, a
    dict inside one, and one under a key called `0`, which is a key of a dict
    and not the index of a list.
    """
    offer = row_at(model=EditModel(DictPlaceCfg()), path=path).offer
    assert offer.extend is grows
    assert offer.keyed is grows
    assert offer.refusal == refusal


def test_under_list_grows() -> None:
    """Test a dict inside a list element takes an entry the class accepts.

    The verdict is what makes this a test of `config_as_json` and not of the
    rule alone: the pass runs `parse_json`, which is where the check that
    would have refused the key lives.
    """
    model = EditModel(DictPlaceCfg())
    model.add_element(path=MATRIX_0, key='gpu')
    assert row_at(model=model, path=(*MATRIX_0, 'gpu')).value == 2
    assert model.validate().valid


def test_under_list_typed() -> None:
    """Test one of those dicts that is empty is answered by its type.

    Nothing it holds says what an entry of it would be, so `dict[str, int]`
    says it, exactly as `list[str]` answers for an empty list.
    """
    model = EditModel(DictPlaceCfg())
    model.add_element(path=MATRIX_1, key='gpu')
    assert row_at(model=model, path=(*MATRIX_1, 'gpu')).value == 0
    assert model.validate().valid


def test_under_list_shrinks() -> None:
    """Test an entry of such a dict can be taken out of it again.

    A dict that can gain a key can lose one: it is the same question about
    the same dict, and it is asked in one place.
    """
    model = EditModel(DictPlaceCfg())
    model.remove_element((*MATRIX_0, 'cpu'))
    assert row_at(model=model, path=MATRIX_0).value == {}
    assert model.validate().valid


def test_deep_under_list() -> None:
    """Test a list anywhere above a dict is enough to stop the check.

    The member here is a dict and the list is inside it, so what the check
    stopped at is a step of the path and not the member.
    """
    model = EditModel(DictPlaceCfg())
    inner = ('regions', 'eu', '0')
    model.add_element(path=inner, key='gpu')
    assert row_at(model=model, path=(*inner, 'gpu')).value == 2
    assert model.validate().valid


def test_by_key_dict_grows() -> None:
    """Test a dict at a key that no declaration names takes an entry.

    `config_as_json` reads a member named in `nested_configs()` whole, so the
    check is never applied to it and nothing inside it is checked either,
    however deep that is.
    """
    model = EditModel(ByKeyDictCfg())
    inner = ('hooks', 'limits')
    model.add_element(path=inner, key='gpu')
    assert row_at(model=model, path=(*inner, 'gpu')).value == 2
    assert model.validate().valid


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


@pytest.mark.parametrize('path', [SPARE, ('limits',)])
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


def test_omitted_gets_object() -> None:
    """Test a member the class leaves out of the file is given an object.

    Such a member has a row while it holds no object, because the object it
    belongs to is asked for the members it left out of the file, and the row
    offers what any declared member holding no object offers. How the class
    writes the member is not part of the question.
    """
    model = EditModel(OmitNestedCfg())
    assert row_paths(model) == [('inner',), ('answer',)]
    assert row_at(model=model, path=('inner',)).offer.extend
    model.add_element(path=('inner',))
    assert row_at(model=model, path=('inner',)).is_object
    assert model.validate().valid


def test_omitted_is_cleared() -> None:
    """Test an omitted member holding an object is put back to holding none.

    Clearing it leaves the member out of the file and leaves the row where it
    was, saying that the member holds no object and offering to give it one
    again, so nothing is lost by clearing it.
    """
    held = OmitNestedCfg(from_json_data_text=OMITTED_JSON)
    model = EditModel(held)
    assert row_at(model=model, path=('inner',)).offer.remove
    model.remove_element(path=('inner',))
    assert not row_at(model=model, path=('inner',)).is_object
    assert row_at(model=model, path=('inner',)).offer.extend
    assert model.validate().valid


def test_omitted_gone_saved(tmp_path: Path) -> None:
    """Test the file of a cleared omitted member holds nothing about it.

    That is the whole difference between the two states of such a member: one
    of them is a key of the file and the other is no key at all. It is also
    what the row that stays is for, because the file that holds no key is one
    the editor has to be able to give the key back.
    """
    out_file = tmp_path / 'out.json'
    model = EditModel(OmitNestedCfg(from_json_data_text=OMITTED_JSON),
                      out_file=out_file)
    model.remove_element(path=('inner',))
    assert model.save().saved
    assert written(out_file) == {'answer': 3}


@pytest.mark.parametrize('name, value', [('note', ''), ('hosts', [])])
def test_omitted_leaf_grows(name: str, value: JsonType) -> None:
    """Test a member left out of the file is given the value of its kind.

    How the class writes such a member decides nothing about the two states:
    it holds nothing, and adding gives it the value of its kind that says no
    more than which kind it is.
    """
    model = EditModel(OmitKindsCfg())
    assert row_at(model=model, path=(name,)).holds_nothing
    model.add_element(path=(name,))
    assert row_at(model=model, path=(name,)).value == value
    assert model.validate().valid


def test_omitted_leaf_cleared(tmp_path: Path) -> None:
    """Test such a member is put back to holding nothing, and to no key.

    The row stays where it was, which is what makes clearing it safe, and the
    file it writes then holds nothing at all about the member.
    """
    out_file = tmp_path / 'out.json'
    model = EditModel(OmitKindsCfg(), out_file=out_file)
    model.add_element(path=('note',))
    model.remove_element(path=('note',))
    assert row_at(model=model, path=('note',)).holds_nothing
    assert model.save().saved
    assert written(out_file) == {'answer': 3}


def test_omitted_dict_refused() -> None:
    """Test a member holding no dict says why it cannot be given one.

    `Config.check_dict_parse` refuses a dict written for a member whose value
    is not one, whatever keys it has and even where it has none, so the
    control would produce a refusal and there is none.
    """
    row = row_at(model=EditModel(OmitKindsCfg()), path=('limits',))
    assert not row.offer.extend
    assert row.offer.refusal == NO_DICT_YET


def test_omitted_dict_fails() -> None:
    """Test the refusal above is the class's and not this library's rule.

    The empty dict is put into the buffer the only way that is left, which is
    the buffer of the model itself, and the pass then refuses it. Without the
    rule above, that is what pressing the control would have produced.
    """
    model = EditModel(OmitKindsCfg())
    model.set_text(path=('legacy',), text='{}')
    assert not model.validate().valid


def test_omitted_no_kind() -> None:
    """Test a member with no annotation is an ordinary field showing null.

    Nothing says what it would hold, so it has one state rather than two, and
    it is reachable all the same: the field takes a value and takes the text
    of `null` back as the JSON it is.
    """
    model = EditModel(OmitKindsCfg())
    row = row_at(model=model, path=('legacy',))
    assert row.editable
    assert not row.holds_nothing
    assert not row.offer.extend and not row.offer.remove
    model.set_text(path=('legacy',), text='kept')
    assert row_at(model=model, path=('legacy',)).value == 'kept'
    model.set_text(path=('legacy',), text='null')
    assert row_at(model=model, path=('legacy',)).value is None


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
