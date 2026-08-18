#! /usr/bin/env python3
"""Tests for the user interface agnostic edit model."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import json
import pytest
from config_as_json import JsonType
from edit_cfg_json import Descriptions, EditModel, MemberRow
from .sample_cfg import PICKED_NAME, DocumentedCfg, ExtraArgCfg, FlagCfg, \
    FlatCfg, IntEnumCfg, ListCfg, NoneCfg, OmitCfg, RangeCfg, RewriteCfg, \
    picking_loader

TEXT_KIND = 'Text.'
"""What the type of a text member says about it.

The editor says what kind of value every member holds, because that is the one
thing it knows about every member of every configuration without being told.
"""

WHOLE_KIND = 'A whole number.'
"""What the type of a member holding a whole number says about it."""

ABOUT_NAME = 'What the name of this configuration is for.'
"""Description of the one member that the tests below describe."""

DESCRIPTIONS: Descriptions = {('name',): ABOUT_NAME}
"""What an application says about the members of a flat configuration."""


def _row(model: EditModel, name: str) -> MemberRow:
    """Return the row of one member of a model."""
    return {row.name: row for row in model.rows}[name]


def _written(out_file: Path) -> JsonType:
    """Return what one output file holds, as JSON space values."""
    value: JsonType = json.loads(out_file.read_text(encoding='UTF-8'))
    return value


def test_flat_rows() -> None:
    """Test a flat configuration gives one row per member."""
    model = EditModel(FlatCfg())
    assert [row.name for row in model.rows] == ['name', 'answer']
    assert [row.value for row in model.rows] == ['flat text', 42]
    assert all(row.editable for row in model.rows)


def test_row_paths() -> None:
    """Test every member of a flat configuration has a one step path."""
    assert [row.path for row in EditModel(FlatCfg()).rows] == \
        [('name',), ('answer',)]


def test_declaration_order() -> None:
    """Test the rows keep the order the configuration class declares.

    The JSON file has its keys sorted, so a model that took its order from
    the file would show these three members as answer, limits, tags.
    """
    model = EditModel(ListCfg())
    assert [row.name for row in model.rows if row.depth == 0] == \
        ['tags', 'limits', 'answer']


def test_omitted_none_no_row() -> None:
    """Test a member left out of JSON while it is None gets no row."""
    model = EditModel(OmitCfg())
    assert [row.name for row in model.rows] == ['first', 'last']


def test_type_name() -> None:
    """Test the model reports the class name of the configuration."""
    assert EditModel(FlatCfg()).config_type_name == 'FlatCfg'


def test_none_is_a_value() -> None:
    """Test a member defaulting to None is an editable row holding None."""
    row = _row(EditModel(NoneCfg()), 'name')
    assert row.value is None
    assert row.editable
    assert not row.is_text


def test_containers_reported() -> None:
    """Test a list member and a dict member are trees of rows.

    The member itself is a row that is not edited in a field, because what it
    holds is on the rows below it, and each of those is edited like any other
    value.
    """
    model = EditModel(ListCfg())
    assert [row.path for row in model.rows] == \
        [('tags',), ('tags', '0'), ('tags', '1'), ('limits',),
         ('limits', 'high'), ('limits', 'low'), ('answer',)]
    assert not _row(model, 'tags').editable
    assert not _row(model, 'limits').editable
    assert _row(model, 'answer').editable
    assert all(model.rows[index].editable for index in (1, 2, 4, 5))


def test_text_kept_as_text() -> None:
    """Test a string member is held as a string and not as JSON notation."""
    model = EditModel(FlatCfg())
    assert _row(model, 'name').is_text
    assert _row(model, 'name').value == 'flat text'
    assert not _row(model, 'answer').is_text


def test_enum_is_a_name() -> None:
    """Test an enum member is an ordinary text row holding its name.

    The model knows nothing about enums and needs to know nothing: what the
    file holds for such a member is the name of the member, so the row is a
    text row like any other and is edited in one ordinary field.
    """
    row = _row(EditModel(IntEnumCfg()), 'level')
    assert row.value == 'LOWEST'
    assert row.is_text
    assert row.editable


def test_enum_completed() -> None:
    """Test text naming one enum member is completed and marked as such.

    This is the same behaviour as a validator that rewrites a value, and it
    reaches the model the same way, which is why the model needs no rule of
    its own for it.
    """
    model = EditModel(IntEnumCfg())
    model.set_text(path=('level',), text='HI')
    assert model.validate().valid
    assert _row(model, 'level').value == 'HIGH'
    assert _row(model, 'level').changed_by_validator


def test_enum_keeps_typing() -> None:
    """Test a field holds text that names no enum member yet.

    Every name of an enum is text that names no member for as long as it is
    half typed, so a buffer that refused such text could not be typed in.
    """
    model = EditModel(IntEnumCfg())
    model.set_text(path=('level',), text='LO')
    assert not model.validate().valid
    assert _row(model, 'level').value == 'LO'
    assert not _row(model, 'level').changed_by_validator


def test_caller_not_changed() -> None:
    """Test building a model does not change the caller's own object."""
    config = RewriteCfg()
    config.name = 'raw text'
    model = EditModel(config)
    assert config.name == 'raw text'
    assert model.rows[0].value == 'Raw text'


def test_edit_stays_in_model() -> None:
    """Test editing the buffer does not touch the caller's own object."""
    config = FlatCfg()
    model = EditModel(config)
    model.set_text(path=('name',), text='edited')
    assert config.name == 'flat text'
    assert _row(model, 'name').value == 'edited'


def test_clean_at_start() -> None:
    """Test a model that was just built has nothing worth saving."""
    model = EditModel(FlatCfg())
    assert not model.dirty
    assert not any(row.edited for row in model.rows)


def test_set_text_member() -> None:
    """Test setting a text member keeps exactly what was typed."""
    model = EditModel(FlatCfg())
    model.set_text(path=('name',), text='other text')
    assert _row(model, 'name').value == 'other text'
    assert _row(model, 'name').edited
    assert model.dirty


def test_set_number_member() -> None:
    """Test setting a number member gives a number and not its text."""
    model = EditModel(FlatCfg())
    model.set_text(path=('answer',), text='7')
    assert _row(model, 'answer').value == 7
    assert not _row(model, 'answer').is_text


def test_set_digits_as_text() -> None:
    """Test a text member holding digits stays text and does not become one.

    This is the case the type information of a row exists for. The member is
    a text member because that is what the configuration object declared,
    and not because of what it happens to hold right now.
    """
    model = EditModel(FlatCfg())
    model.set_text(path=('name',), text='10')
    assert _row(model, 'name').value == '10'


def test_set_invalid_number() -> None:
    """Test a number member tolerates text that is not a number yet.

    A value that is being typed is not valid for most of the time it takes
    to type it, so a buffer that refused such a value could not be typed in.
    """
    model = EditModel(FlatCfg())
    model.set_text(path=('answer',), text='not-a-number')
    assert _row(model, 'answer').value == 'not-a-number'
    assert _row(model, 'answer').edited


def test_set_empty_text() -> None:
    """Test both kinds of member accept an empty field."""
    model = EditModel(FlatCfg())
    model.set_text(path=('name',), text='')
    model.set_text(path=('answer',), text='')
    assert _row(model, 'name').value == ''
    assert _row(model, 'answer').value == ''


def test_set_recovers() -> None:
    """Test a member set to text that is no number can be set to one."""
    model = EditModel(FlatCfg())
    model.set_text(path=('answer',), text='4x')
    model.set_text(path=('answer',), text='4')
    assert _row(model, 'answer').value == 4


def test_set_twice() -> None:
    """Test the last of several edits of one member is what is kept."""
    model = EditModel(FlatCfg())
    for text in ['first', 'second', 'third']:
        model.set_text(path=('name',), text=text)
    assert _row(model, 'name').value == 'third'


def test_set_same_text() -> None:
    """Test setting the text a field already shows is not an edit.

    A field posts a change when it is given its initial text, so a model
    that counted that as an edit would report unsaved changes before the
    user had touched anything.
    """
    model = EditModel(FlatCfg())
    model.set_text(path=('answer',), text='42')
    assert not model.dirty


def test_set_back_to_start() -> None:
    """Test typing a value back to what it was leaves nothing to save."""
    model = EditModel(FlatCfg())
    model.set_text(path=('name',), text='other text')
    model.set_text(path=('name',), text='flat text')
    assert not _row(model, 'name').edited
    assert not model.dirty


def test_dirty_per_model() -> None:
    """Test one edited member is enough to make the whole model dirty."""
    model = EditModel(FlatCfg())
    model.set_text(path=('answer',), text='7')
    assert model.dirty
    assert not _row(model, 'name').edited


def test_set_unknown_member() -> None:
    """Test setting a member that does not exist is refused."""
    model = EditModel(FlatCfg())
    with pytest.raises(KeyError):
        model.set_text(path=('missing',), text='text')
    assert not model.dirty


def test_set_wrong_path() -> None:
    """Test a path with more steps than a flat member has is refused."""
    model = EditModel(FlatCfg())
    with pytest.raises(KeyError):
        model.set_text(path=('name', 'inner'), text='text')


def test_set_container() -> None:
    """Test a member that cannot be edited yet is refused, not half done."""
    model = EditModel(ListCfg())
    with pytest.raises(ValueError):
        model.set_text(path=('tags',), text='[]')
    assert _row(model, 'tags').value == ['first', 'second']
    assert not model.dirty


def test_rows_are_a_snapshot() -> None:
    """Test a row that was read before an edit is not changed by it."""
    model = EditModel(FlatCfg())
    before = _row(model, 'name')
    model.set_text(path=('name',), text='other text')
    assert before.value == 'flat text'
    assert _row(model, 'name').value == 'other text'


@pytest.mark.parametrize('value, editable',
                         [(1, True), (1.5, True), ('text', True),
                          (True, True), (None, True), ([1, 2], False),
                          ({'key': 1}, False), ([], False), ({}, False)])
def test_row_editable(value: JsonType, editable: bool) -> None:
    """Test which kinds of JSON value a row reports as editable."""
    row = MemberRow(path=('member',), value=value, original=value)
    assert row.editable is editable


@pytest.mark.parametrize('value, is_text',
                         [('text', True), ('', True), ('42', True),
                          (42, False), (1.5, False), (True, False),
                          (None, False), (['a'], False), ({'a': 1}, False)])
def test_row_is_text(value: JsonType, is_text: bool) -> None:
    """Test which kinds of member a row reports as holding text."""
    row = MemberRow(path=('member',), value=value, original=value)
    assert row.is_text is is_text


@pytest.mark.parametrize('value, original, edited',
                         [(1, 1, False), (2, 1, True), (1.0, 1, True),
                          (True, 1, True), ('42', 42, True),
                          ('', None, True), (None, None, False)])
def test_row_edited(value: JsonType, original: JsonType, edited: bool) -> None:
    """Test a row is edited when it would be written to the file anew."""
    row = MemberRow(path=('member',), value=value, original=original)
    assert row.edited is edited


def test_row_name_is_last() -> None:
    """Test the name of a member is the last step of its path."""
    row = MemberRow(path=('outer', 'inner'), value=1, original=1)
    assert row.name == 'inner'


def test_row_flags_start_off() -> None:
    """Test the flags that later steps set are off in a new row."""
    row = MemberRow(path=('member',), value=1, original=1)
    assert not row.changed_by_validator
    assert not row.filled_from_default
    assert row.description == ''


def test_described_rows() -> None:
    """Test the description of a member reaches the row of that member.

    What the type of the member says follows it, on a line of its own, and a
    member the application says nothing about has that alone.
    """
    model = EditModel(FlatCfg(), descriptions=DESCRIPTIONS)
    assert _row(model, 'name').description == f'{ABOUT_NAME}\n{TEXT_KIND}'
    assert _row(model, 'answer').description == WHOLE_KIND


def test_no_descriptions() -> None:
    """Test an application that describes nothing still explains the types.

    That is what a program which is told a class and no mapping shows, and it
    is the least the editor can say about a member: what kind of value it is.
    """
    described = [row.description for row in EditModel(FlatCfg()).rows]
    assert described == [TEXT_KIND, WHOLE_KIND]


def test_description_stays() -> None:
    """Test what a member is for is still said after it has been edited.

    A description says what the member is for, which is not something the
    user can change by typing a value into it or by saving one.
    """
    model = EditModel(FlatCfg(), descriptions=DESCRIPTIONS)
    model.set_text(path=('name',), text='other text')
    model.validate()
    assert _row(model, 'name').description == f'{ABOUT_NAME}\n{TEXT_KIND}'


def test_class_docstring() -> None:
    """Test the model reports the docstring of the configuration class."""
    model = EditModel(DocumentedCfg())
    assert model.summary == \
        'One line that says what this configuration is for.'
    assert model.docstring.startswith(model.summary)
    assert model.docstring.endswith('the detail of this class.')


def test_explanations_shown() -> None:
    """Test the editor starts by explaining itself.

    An application that wrote descriptions wrote them to be read, and a user
    who does not want them presses one key.
    """
    assert EditModel(FlatCfg()).explanations_shown


def test_toggle_explanations() -> None:
    """Test the toggle hides the explanations and shows them again."""
    model = EditModel(FlatCfg())
    model.toggle_explanations()
    assert not model.explanations_shown
    model.toggle_explanations()
    assert model.explanations_shown


def test_verdict_unknown() -> None:
    """Test a model that was just built has not been validated."""
    assert EditModel(FlatCfg()).verdict is None


def test_validate_accepts() -> None:
    """Test the values a configuration object starts with are accepted."""
    verdict = EditModel(FlatCfg()).validate()
    assert verdict.valid
    assert verdict.diagnostics == ''


def test_verdict_kept() -> None:
    """Test the verdict of the last pass is what the model reports."""
    model = EditModel(FlatCfg())
    verdict = model.validate()
    assert model.verdict == verdict


def test_validate_refuses() -> None:
    """Test a value the application refuses is reported as it refused it.

    It is reported for the member it is about, because the rule that refused
    it is about that one member and nothing else.
    """
    model = EditModel(RangeCfg())
    model.set_text(path=('answer',), text='500')
    verdict = model.validate()
    assert not verdict.valid
    assert 'greater than maximum 100' in verdict.refused[('answer',)]


def test_refused_keeps_typed() -> None:
    """Test a refused buffer still holds exactly what the user typed."""
    model = EditModel(RangeCfg())
    model.set_text(path=('answer',), text='not-a-number')
    model.validate()
    assert _row(model, 'answer').value == 'not-a-number'
    assert not _row(model, 'answer').changed_by_validator


def test_edit_clears_verdict() -> None:
    """Test editing drops a verdict that was reached from another buffer."""
    model = EditModel(FlatCfg())
    model.validate()
    model.set_text(path=('answer',), text='7')
    assert model.verdict is None


def test_same_text_verdict() -> None:
    """Test writing the text a field already shows does not drop a verdict.

    This is what lets a backend write the buffer back into its fields after
    a validation pass without that pass undoing itself.
    """
    model = EditModel(FlatCfg())
    model.validate()
    model.set_text(path=('answer',), text='42')
    assert model.verdict is not None


def test_rewrite_marked() -> None:
    """Test a value that a validation pass rewrote is marked as rewritten."""
    model = EditModel(RewriteCfg())
    model.set_text(path=('name',), text='typed text')
    model.validate()
    assert _row(model, 'name').value == 'Typed text'
    assert _row(model, 'name').changed_by_validator


def test_rewrite_mark_cleared() -> None:
    """Test the next edit of a rewritten member clears its mark."""
    model = EditModel(RewriteCfg())
    model.set_text(path=('name',), text='typed text')
    model.validate()
    model.set_text(path=('name',), text='typed text again')
    assert not _row(model, 'name').changed_by_validator


def test_no_rewrite_no_mark() -> None:
    """Test a pass that changed nothing marks nothing."""
    model = EditModel(RewriteCfg())
    model.set_text(path=('name',), text='Typed text')
    model.validate()
    assert not _row(model, 'name').changed_by_validator


def test_rewrite_is_a_change() -> None:
    """Test a value a validator wrote is worth saving like any other."""
    model = EditModel(RewriteCfg())
    model.set_text(path=('name',), text='typed text')
    model.validate()
    assert model.dirty
    assert _row(model, 'name').edited


def test_validate_containers() -> None:
    """Test a list member and a dict member survive a validation pass."""
    model = EditModel(ListCfg())
    assert model.validate().valid
    assert _row(model, 'tags').value == ['first', 'second']
    assert not model.dirty


def test_omitted_none_ok() -> None:
    """Test a member left out of JSON while None does not fail a pass."""
    model = EditModel(OmitCfg())
    assert model.validate().valid
    assert [row.name for row in model.rows] == ['first', 'last']


def test_no_stderr_output(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the diagnostics of a pass are reported and not printed.

    An application that runs the editor has a screen and not a terminal
    behind it, so a diagnostic that the user asked for belongs in the
    verdict, where the editor can show it.
    """
    model = EditModel(RangeCfg())
    model.set_text(path=('answer',), text='500')
    verdict = model.validate()
    assert 'greater than maximum 100' in verdict.refused[('answer',)]
    assert capsys.readouterr().err == ''


def test_validate_unbuildable() -> None:
    """Test a class the editor cannot construct is edited and validated.

    Nothing here could construct `ExtraArgCfg`, because its constructor needs
    an argument this library knows nothing about. It does not have to: a buffer
    is applied to a copy of the object the application handed over, so the
    class validates it exactly as it validates any other. A loader is what such
    a class needs for reading a file, and for nothing else.
    """
    model = EditModel(ExtraArgCfg(home='here'))
    model.set_text(path=('home',), text='elsewhere')
    assert model.validate().valid
    assert next(row.value for row in model.rows) == 'elsewhere'


def test_leaving_field() -> None:
    """Test leaving a field says whether its text means a value at all.

    It is the moment the user has moved on from that field, and it is
    deliberately not every change: the name of an enum member is no name of
    one for most of the time it takes to type it.
    """
    model = EditModel(IntEnumCfg())
    model.set_text(path=('level',), text='MIDDLE')
    assert _row(model, 'level').conversion == ''
    model.check_field(('level',))
    assert 'MIDDLE is not one of' in _row(model, 'level').conversion


def test_leaving_good_field() -> None:
    """Test leaving a field whose text means a value says nothing."""
    model = EditModel(IntEnumCfg())
    model.set_text(path=('level',), text='HI')
    model.check_field(('level',))
    assert _row(model, 'level').conversion == ''


def test_edit_clears_report() -> None:
    """Test the next edit of that member takes the report away again.

    A name that is being typed passes through text that names no member, and
    the report of the name before it says nothing true about the one now.
    """
    model = EditModel(IntEnumCfg())
    model.set_text(path=('level',), text='MIDDLE')
    model.check_field(('level',))
    model.set_text(path=('level',), text='MIDDL')
    assert _row(model, 'level').conversion == ''


def test_other_edit_keeps_it() -> None:
    """Test an edit of another member leaves the report alone.

    Whether this text means a value of this member is answered by the member
    alone, so it stays true until this member is edited again.
    """
    model = EditModel(FlatCfg())
    model.set_text(path=('name',), text='typed')
    model.check_field(('name',))
    model.set_text(path=('answer',), text='7')
    assert _row(model, 'name').conversion == ''


def test_pass_checks_fields() -> None:
    """Test a validation pass answers for every member at once.

    A member the user never visited is then reported exactly as one they
    typed into and left, which is what makes the two ways of asking agree.
    """
    model = EditModel(IntEnumCfg())
    model.set_text(path=('level',), text='MIDDLE')
    model.validate()
    assert 'MIDDLE is not one of' in _row(model, 'level').conversion


@pytest.mark.parametrize('name, typed, expected',
                         [('plain', 'T', True), ('plain', 'tr', True),
                          ('checked', 'f', False),
                          ('checked', 'FALSE', False)])
def test_flag_typed(name: str, typed: str, expected: bool) -> None:
    """Test a beginning of either word is that value in such a member.

    The value is made on the change and not when the field is left, so a
    validation pass and a save see the value the user meant, and the field is
    written back as the whole word by the refresh that follows the pass.
    """
    model = EditModel(FlagCfg())
    model.set_text(path=(name,), text=typed)
    row = _row(model, name)
    assert row.value is expected
    assert row.value_text == ('true' if expected else 'false')


def test_flag_word_saved(tmp_path: Path) -> None:
    """Test what such a member reaches the file as is the whole word."""
    out_file = tmp_path / 'out.json'
    model = EditModel(FlagCfg(), out_file=out_file)
    model.set_text(path=('checked',), text='f')
    assert model.save().saved
    assert _written(out_file) == {'checked': False, 'plain': False,
                                  'answer': 1}


@pytest.mark.parametrize('name', ['checked', 'plain'])
def test_flag_left_field(name: str) -> None:
    """Test leaving such a field says so when it means neither word.

    The member whose type no validator checks is answered exactly as the one
    it checks, because what is said is about the type of the member and not
    about a rule of the application.
    """
    model = EditModel(FlagCfg())
    model.set_text(path=(name,), text='yes')
    assert _row(model, name).conversion == ''
    model.check_field((name,))
    assert 'yes is not one of: true, false' in _row(model, name).conversion


@pytest.mark.parametrize('name', ['checked', 'plain'])
def test_flag_refused(name: str) -> None:
    """Test a pass refuses such a text and names the member it is about."""
    model = EditModel(FlagCfg())
    model.set_text(path=(name,), text='1')
    verdict = model.validate()
    assert not verdict.valid
    assert verdict.refused[(name,)] == '1 is not one of: true, false'


def test_flag_refused_save(tmp_path: Path) -> None:
    """Test nothing is written while such a member means neither word."""
    out_file = tmp_path / 'out.json'
    model = EditModel(FlagCfg(), out_file=out_file)
    model.set_text(path=('plain',), text='yes')
    assert not model.save().saved
    assert not out_file.exists()


def test_flag_kind_said() -> None:
    """Test the type of such a member is what says which values it takes."""
    assert _row(EditModel(FlagCfg()), 'plain').description == 'True or false.'


def test_unknown_field() -> None:
    """Test checking a member that does not exist is an error, not a shrug."""
    model = EditModel(FlatCfg())
    with pytest.raises(KeyError):
        model.check_field(('ghost',))


def test_enum_described() -> None:
    """Test the type of a member is part of what is said about it.

    No description mapping is passed here at all, so everything below the
    member comes from its own enum class.
    """
    assert _row(EditModel(IntEnumCfg()), 'level').description.endswith(
        'One of: LOWEST, LOW, HIGH.')


def test_converter_on_row() -> None:
    """Test a member that holds no enum carries no converter."""
    assert _row(EditModel(FlatCfg()), 'name').converter is None
    assert _row(EditModel(IntEnumCfg()), 'level').converter is not None


def test_loader_refuses_save(tmp_path: Path) -> None:
    """Test a save asks the loader whether the file could be read back.

    The buffer is valid, and the class being edited is the class the rows are
    of, so nothing but the loader can say that this file is a file of another
    class. The model reports it as a save that did not happen, exactly as it
    reports every other one.
    """
    out_file = tmp_path / 'out.json'
    model = EditModel(FlatCfg(), loader=picking_loader, out_file=out_file)
    model.set_text(path=('name',), text=PICKED_NAME)
    outcome = model.save()
    assert not outcome.saved
    assert 'PickedCfg' in outcome.message
    assert model.save_message == outcome.message
    assert not out_file.exists()
    assert model.saved_config is None


def test_loader_allows_save(tmp_path: Path) -> None:
    """Test the same model saves what that loader does read back."""
    out_file = tmp_path / 'out.json'
    model = EditModel(FlatCfg(), loader=picking_loader, out_file=out_file)
    model.set_text(path=('name',), text='still flat')
    assert model.save().saved
    assert json.loads(out_file.read_text(encoding='UTF-8')) == \
        {'name': 'still flat', 'answer': 42}
