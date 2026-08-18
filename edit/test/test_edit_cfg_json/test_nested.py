#! /usr/bin/env python3
"""Tests for editing a configuration built out of nested configuration objects.

What is tested here is what such an object is to the model: a declared
nested `Config` object is a node with a class and a docstring of its own, its
members are the rows below it, and everything inside it belongs to its own
class rather than to the class holding it.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import pytest
from edit_cfg_json import Descriptions, EditModel, model_as_text, \
    row_describes, row_description, row_diagnostic, row_subtree_text, \
    row_validates, row_value_text
from .model_helpers import row_at, row_paths, shown_paths, written
from .container_cfg import CROSS_REFUSAL, ConfigDictCfg, ConfigListCfg, \
    DeepConfigCfg, DeepSubtreeCfg, FlagTreeCfg, INNER_LIMIT, InnerCfg, \
    NestedCfg, NoDocNestedCfg, NullNestedCfg, ORDER_REFUSAL, OmitNestedCfg, \
    OwnedEnumCfg, OwnedOptionCfg, RangedObjectsCfg, SubtreeCfg

TOO_WIDE = str(INNER_LIMIT + 1)
"""A width that the nested class of `SubtreeCfg` refuses."""

OUT_OF_ORDER = '99'
"""A low value above the high value of the other nested class."""

ABOUT_ANY_WIDTH = 'What the width of any one of these is for.'
"""What an application says once about a member of every repeated object."""

ABOUT_ONE_WIDTH = 'What the width of the second one is for.'
"""What it says about that member of one of those objects in particular."""

ABOUT_ANY_OBJECT = 'What one of these objects is for.'
"""What it says about every repeated object itself rather than a member."""

INSIDE_VALID = ' [valid inside]'
"""What a container of objects says when every one of them passes.

A list or a dict is no configuration and says nothing about itself, so what it
says is about the objects it holds. That row is what a folded container leaves
on the screen, where every object it is about is hidden.
"""

INSIDE_REFUSED = ' [refused inside]'
"""What such a container says when one of the objects it holds is refused."""

FIRST_WIDTH = ('outputs', '0', 'width')
"""The member of the first object of the list that its class has a rule for."""

OTHER_WIDTH = ('outputs', '1', 'width')
"""The same member of the second object of that list."""


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


def test_one_text_per_object() -> None:
    """Test one `'['` selector describes that member of every object.

    A list of objects is the ordinary shape of a real configuration, so an
    application that had to write one description per index would be writing
    text that stopped being true the moment the list grew.
    """
    said: Descriptions = {('outputs', '[', 'width'): ABOUT_ANY_WIDTH}
    model = EditModel(ConfigListCfg(), descriptions=said)
    assert row_at(model, ('outputs', '0', 'width')).description.startswith(
        ABOUT_ANY_WIDTH)
    assert row_at(model, ('outputs', '1', 'width')).description.startswith(
        ABOUT_ANY_WIDTH)
    assert not row_at(model, ('outputs', '0', 'height')).description.\
        startswith(ABOUT_ANY_WIDTH)


def test_every_dict_value() -> None:
    """Test the same selector reaches every value of a dict of objects."""
    said: Descriptions = {('outputs', '[', 'width'): ABOUT_ANY_WIDTH}
    model = EditModel(ConfigDictCfg(), descriptions=said)
    assert row_at(model, ('outputs', 'first', 'width')).description.\
        startswith(ABOUT_ANY_WIDTH)


def test_object_described() -> None:
    """Test the selector describes the object itself as readily as a member.

    What the application says about one of these objects comes above what its
    own class says about itself, exactly as it does for a nested object that a
    member holds.
    """
    said: Descriptions = {('outputs', '['): ABOUT_ANY_OBJECT}
    model = EditModel(ConfigListCfg(), descriptions=said)
    row = row_at(model, ('outputs', '0'))
    assert row_describes(row)
    assert row_description(model=model, row=row).startswith(ABOUT_ANY_OBJECT)


def test_named_element_wins() -> None:
    """Test a selector naming one element beats one that says `'['`.

    Both address that member and the more specific of the two describes it,
    so one element of a repeated object can be singled out while every other
    keeps the general text.
    """
    said: Descriptions = {('outputs', '[', 'width'): ABOUT_ANY_WIDTH,
                          ('outputs', '1', 'width'): ABOUT_ONE_WIDTH}
    model = EditModel(ConfigListCfg(), descriptions=said)
    assert row_at(model, ('outputs', '1', 'width')).description.startswith(
        ABOUT_ONE_WIDTH)
    assert row_at(model, ('outputs', '0', 'width')).description.startswith(
        ABOUT_ANY_WIDTH)


def test_deep_every_element() -> None:
    """Test a selector says `'['` at each depth it has to.

    A list of objects each holding a dict of more of them is the shape this
    library is written for, and one selector reaches the bottom of it without
    the application naming an index or a key anywhere.
    """
    said: Descriptions = {('outputs', '[', 'parts', '[', 'width'):
                          ABOUT_ANY_WIDTH}
    model = EditModel(DeepConfigCfg(), descriptions=said)
    deep = ('outputs', '0', 'parts', 'one', 'width')
    assert row_at(model, deep).description.startswith(ABOUT_ANY_WIDTH)


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


def test_unasked_says_nothing() -> None:
    """Test an object that has not been asked says nothing about itself.

    Not being asked is a third state and not a kind of failure, exactly as it
    is for the validation of the whole configuration, so nothing at all is
    said until something asks.
    """
    row = row_at(EditModel(SubtreeCfg()), ('ranged',))
    assert row.subtree_valid is None
    assert row_subtree_text(row) == ''
    assert row_validates(row)


def test_fold_asks_the_object() -> None:
    """Test folding a nested object asks whether it is one on its own.

    That is the cheap local question: it needs no candidate configuration and
    says nothing about whether the file could be written.
    """
    model = EditModel(SubtreeCfg())
    model.toggle_fold(('ranged',))
    assert row_at(model, ('ranged',)).subtree_valid is True
    assert model.verdict is None


def test_open_asks_again() -> None:
    """Test opening a nested object asks it as well as folding it does.

    Changing how much of an object is on the screen is the moment at which
    the user is looking at it, whichever way it changed.
    """
    model = EditModel(SubtreeCfg())
    model.toggle_fold(('ranged',))
    model.set_text(path=('ranged', 'width'), text=TOO_WIDE)
    model.toggle_fold(('ranged',))
    assert row_at(model, ('ranged',)).subtree_valid is False


def test_flag_inside_object() -> None:
    """Test a member of a nested object takes a beginning of a word."""
    model = EditModel(FlagTreeCfg())
    model.set_text(path=('inner', 'enabled'), text='f')
    assert row_at(model, ('inner', 'enabled')).value is False
    assert model.validate().valid


def test_flag_refused_inside() -> None:
    """Test folding such an object refuses a text that means neither word.

    The object is asked about its own part of the buffer, so what it takes is
    what the rows inside it hold, and the refusal is kept at the member it is
    about rather than at the object holding it.
    """
    model = EditModel(FlagTreeCfg())
    model.set_text(path=('inner', 'enabled'), text='maybe')
    model.toggle_fold(('inner',))
    assert row_at(model, ('inner',)).subtree_valid is False
    assert row_at(model, ('inner', 'enabled')).subtree_refusal == \
        'maybe is not one of: true, false'


def test_edit_inside_unasks() -> None:
    """Test an edit inside an object takes back what was said about it.

    The answer was about the values the object held, and one of them has
    just changed. It is a different lifetime from the verdict of the whole
    configuration, which any edit anywhere takes away.
    """
    model = EditModel(SubtreeCfg())
    model.validate()
    assert row_at(model, ('ordered',)).subtree_valid is True
    model.set_text(path=('ranged', 'width'), text='5')
    assert row_at(model, ('ranged',)).subtree_valid is None
    assert row_at(model, ('ordered',)).subtree_valid is True


def test_pass_asks_objects() -> None:
    """Test a validation pass answers for every nested object at once."""
    model = EditModel(DeepSubtreeCfg())
    model.validate()
    assert row_at(model, ('outer',)).subtree_valid is True
    assert row_at(model, ('outer', 'ranged')).subtree_valid is True


def test_fold_all_asks_all() -> None:
    """Test folding everything asks every nested object about itself."""
    model = EditModel(SubtreeCfg())
    model.toggle_fold_all()
    assert row_at(model, ('ranged',)).subtree_valid is True
    assert row_at(model, ('ordered',)).subtree_valid is True


def test_missing_not_asked() -> None:
    """Test a declared member holding no object is never asked about one.

    There is no object there, so there is nothing to ask and nothing that
    could ever be said, which is what a backend reads before it creates the
    widget that would say it.
    """
    model = EditModel(NullNestedCfg())
    model.validate()
    row = row_at(model, ('inner',))
    assert not row_validates(row)
    assert row.subtree_valid is None


def test_container_unasked() -> None:
    """Test a container of values has no object at it or inside it.

    A list of numbers holds no configuration that could be asked anything, so
    nothing can ever be said about it and a backend creates no widget for it.
    A container of objects is the other case, and it says what it holds.
    """
    model = EditModel(NestedCfg())
    model.validate()
    assert not row_validates(row_at(model, ('limits',)))
    assert row_validates(row_at(model, ('inner',)))
    assert row_validates(row_at(EditModel(RangedObjectsCfg()), ('outputs',)))


def test_fold_says_why() -> None:
    """Test folding an object keeps what it refused and not only that it did.

    A badge saying that something is wrong while nothing says what would leave
    the user to validate the whole configuration to find out, which is a
    second question about something they have just been told.
    """
    model = EditModel(SubtreeCfg())
    model.set_text(path=('ranged', 'width'), text=TOO_WIDE)
    model.toggle_fold(('ranged',))
    assert model.verdict is None
    wrong = row_diagnostic(model=model, row=row_at(model, ('ranged', 'width')))
    assert 'width' in wrong
    assert TOO_WIDE in wrong


def test_fold_says_own_why() -> None:
    """Test what an object refuses about no member of it is said at it."""
    model = EditModel(SubtreeCfg())
    model.set_text(path=('ordered', 'low'), text=OUT_OF_ORDER)
    model.toggle_fold(('ordered',))
    said = row_diagnostic(model=model, row=row_at(model, ('ordered',)))
    assert ORDER_REFUSAL.format(low=99, high=9) in said


def test_edit_forgets_why() -> None:
    """Test an edit inside an object takes back what it said and why at once.

    The two are one answer and have one lifetime, so a state saying that
    something is wrong must not outlive the sentence that says what. An object
    beside it is left alone, because nothing inside that one has changed.
    """
    model = EditModel(SubtreeCfg())
    model.set_text(path=('ranged', 'width'), text=TOO_WIDE)
    model.toggle_fold_all()
    assert row_diagnostic(model=model, row=row_at(model, ('ranged', 'width')))
    model.set_text(path=('ranged', 'width'), text='3')
    assert row_at(model, ('ranged',)).subtree_valid is None
    assert not row_diagnostic(model=model,
                              row=row_at(model, ('ranged', 'width')))
    assert row_at(model, ('ordered',)).subtree_valid is True


def test_fold_asks_inside() -> None:
    """Test folding a list of objects asks every object that it holds.

    The member itself is a list and is no configuration, so asking only the
    node that was folded would ask nothing at all, while folding it is exactly
    what hides every object that does have something to say.
    """
    model = EditModel(RangedObjectsCfg())
    model.set_text(path=OTHER_WIDTH, text=TOO_WIDE)
    model.toggle_fold(('outputs',))
    assert model.verdict is None
    assert row_at(model, ('outputs', '1')).subtree_valid is False
    assert row_at(model, ('outputs', '0')).subtree_valid is True
    assert row_diagnostic(model=model, row=row_at(model, OTHER_WIDTH))


def test_container_inside() -> None:
    """Test a container says what the objects it holds are, not what it is.

    That row is the only one a folded container leaves on the screen, so
    without it folding a member would hide the one thing the user has to act
    on and leave nothing at all in its place.
    """
    model = EditModel(RangedObjectsCfg())
    model.toggle_fold(('outputs',))
    assert row_subtree_text(row_at(model, ('outputs',))) == INSIDE_VALID
    model.set_text(path=FIRST_WIDTH, text=TOO_WIDE)
    assert row_subtree_text(row_at(model, ('outputs',))) == ''
    model.toggle_fold(('outputs',))
    assert row_subtree_text(row_at(model, ('outputs',))) == INSIDE_REFUSED


def test_member_refused_in() -> None:
    """Test a member a nested class refuses is named at that member.

    That is what asking the object on its own reaches and reading the whole
    configuration cannot: such an object validates itself while `parse_json`
    builds it, so the object that could say which member was refused is one
    that was never built.
    """
    model = EditModel(SubtreeCfg())
    model.set_text(path=('ranged', 'width'), text=TOO_WIDE)
    verdict = model.validate()
    assert not verdict.valid
    assert set(verdict.refused) == {('ranged', 'width')}
    assert row_at(model, ('ranged',)).subtree_valid is False
    assert row_at(model, ('ordered',)).subtree_valid is True


def test_object_refuses_own() -> None:
    """Test what a nested class refuses about no member of it is at it.

    It is about the object, and the object is a node with a row, so it is
    said there rather than in the block below the members: a message that
    names no place sends the user looking for one.
    """
    model = EditModel(SubtreeCfg())
    model.set_text(path=('ordered', 'low'), text=OUT_OF_ORDER)
    verdict = model.validate()
    assert set(verdict.refused) == {('ordered',)}
    assert ORDER_REFUSAL.format(low=99, high=9) in verdict.refused[
        ('ordered',)]
    assert verdict.diagnostics == ''


def test_valid_object_refused() -> None:
    """Test an object valid on its own inside a configuration that is not.

    This is what the two states are kept apart for. The rule that refuses
    this configuration is about both objects and therefore about neither, so
    each of them is a perfectly good configuration on its own while the
    configuration holding them cannot be saved.
    """
    model = EditModel(SubtreeCfg())
    model.set_text(path=('ranged', 'width'), text='1')
    verdict = model.validate()
    assert not verdict.valid
    assert not verdict.refused
    assert CROSS_REFUSAL.format(width=1) in verdict.diagnostics
    assert row_at(model, ('ranged',)).subtree_valid is True
    assert row_at(model, ('ordered',)).subtree_valid is True


def test_refused_once_deep() -> None:
    """Test one mistake deep inside is reported once and at its own object.

    An object holding a refused object is refused as well, and it is not
    asked again, so the outer one carries no message of its own.
    """
    model = EditModel(DeepSubtreeCfg())
    model.set_text(path=('outer', 'ranged', 'width'), text=TOO_WIDE)
    verdict = model.validate()
    assert set(verdict.refused) == {('outer', 'ranged', 'width')}
    assert row_at(model, ('outer', 'ranged')).subtree_valid is False
    assert row_at(model, ('outer',)).subtree_valid is False


def test_own_state_in_dump() -> None:
    """Test the text rendering says what each object is on its own."""
    model = EditModel(SubtreeCfg())
    model.set_text(path=('ranged', 'width'), text=TOO_WIDE)
    model.validate()
    printed = model_as_text(model)
    assert 'ranged: RangedInnerCfg (edited) [refused on its own]' in printed
    assert 'ordered: OrderedInnerCfg [valid on its own]' in printed


def test_key_order_no_change() -> None:
    """Test a nested object is not marked for the order its members are in.

    The editor holds the members of such an object in the order its class
    declares them and `config_as_json` writes them sorted, so the two orders
    differ for every nested object there is. A file that holds the same
    values in another order holds the same values, so neither the user nor a
    validator has changed anything here.
    """
    model = EditModel(SubtreeCfg())
    model.set_text(path=('ordered', 'high'), text='8')
    model.set_text(path=('ordered', 'high'), text='9')
    model.validate()
    assert not model.dirty
    assert not row_at(model, ('ordered',)).changed_by_validator
