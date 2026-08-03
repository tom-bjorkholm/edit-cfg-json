#! /usr/bin/env python3
"""Tests for the user interface agnostic edit model."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import json
import pytest
from config_as_json import JsonType
from edit_cfg_json import EditModel, MemberRow
from .sample_cfg import ExtraArgCfg, FlatCfg, IntEnumCfg, ListCfg, NoneCfg, \
    OmitCfg, RangeCfg, RewriteCfg


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
    assert [row.name for row in model.rows] == ['tags', 'limits', 'answer']


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
    """Test a list member and a dict member are rows that are not editable."""
    model = EditModel(ListCfg())
    assert {row.name for row in model.rows} == {'answer', 'limits', 'tags'}
    assert not _row(model, 'tags').editable
    assert not _row(model, 'limits').editable
    assert _row(model, 'answer').editable


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
    """Test a value the application refuses is reported as it refused it."""
    model = EditModel(RangeCfg())
    model.set_text(path=('answer',), text='500')
    verdict = model.validate()
    assert not verdict.valid
    assert 'greater than maximum 100' in verdict.diagnostics


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
    assert 'greater than maximum 100' in verdict.diagnostics
    assert capsys.readouterr().err == ''


def test_validate_unbuildable() -> None:
    """Test a class the editor cannot construct is refused, not crashed on.

    The editor knows nothing about the extra constructor argument until the
    explicit loader of a later step exists, so a pass has to report that as
    a verdict rather than let the exception reach the user interface.
    """
    model = EditModel(ExtraArgCfg(home='here'))
    verdict = model.validate()
    assert not verdict.valid
    assert 'TypeError' in verdict.diagnostics


def test_no_destination_yet() -> None:
    """Test a model built without an output file has none, and says nothing."""
    model = EditModel(FlatCfg())
    assert model.out_file is None
    assert model.save_message == ''
    assert model.saved_config is None


def test_save_needs_a_file() -> None:
    """Test a save with nowhere to write refuses and says why.

    The backends turn this into a question, but the model has to answer it
    for a caller that cannot ask one, such as the text dump of the examples.
    """
    model = EditModel(FlatCfg())
    outcome = model.save()
    assert not outcome.saved
    assert 'no file to save to' in outcome.message
    assert model.save_message == outcome.message
    assert model.saved_config is None


def test_save_writes(tmp_path: Path) -> None:
    """Test saving writes the edited values and gives the object back."""
    out_file = tmp_path / 'out.json'
    model = EditModel(FlatCfg(), out_file=out_file)
    model.set_text(path=('answer',), text='7')
    assert model.save().saved
    assert _written(out_file) == {'name': 'flat text', 'answer': 7}
    saved = model.saved_config
    assert isinstance(saved, FlatCfg)
    assert saved.answer == 7


def test_save_leaves_caller(tmp_path: Path) -> None:
    """Test the caller's own object is untouched by a save.

    This is why `edit()` gives the saved object back at all: the caller's
    object would otherwise be the stale one and there would be no other.
    """
    config = FlatCfg()
    model = EditModel(config, out_file=tmp_path / 'out.json')
    model.set_text(path=('answer',), text='7')
    assert model.save().saved
    assert config.answer == 42
    assert model.saved_config is not config


def test_save_refuses_invalid(tmp_path: Path) -> None:
    """Test an invalid buffer is not written, and the verdict says why."""
    out_file = tmp_path / 'out.json'
    model = EditModel(RangeCfg(), out_file=out_file)
    model.set_text(path=('answer',), text='500')
    outcome = model.save()
    assert not outcome.saved
    assert 'cannot be saved' in outcome.message
    assert not out_file.exists()
    assert model.saved_config is None
    verdict = model.verdict
    assert verdict is not None
    assert 'greater than maximum 100' in verdict.diagnostics


def test_save_keeps_old_file(tmp_path: Path) -> None:
    """Test a refused save leaves an existing output file as it was.

    A user who saves an invalid buffer over their own configuration file has
    to still have the file afterwards.
    """
    out_file = tmp_path / 'out.json'
    out_file.write_text('kept', encoding='UTF-8')
    model = EditModel(RangeCfg(), out_file=out_file)
    model.set_text(path=('answer',), text='500')
    assert not model.save().saved
    assert out_file.read_text(encoding='UTF-8') == 'kept'


def test_save_validates(tmp_path: Path) -> None:
    """Test saving runs the same pass as validating, and marks a rewrite.

    A validator that rewrites a value rewrites it on the way to the file as
    well, so the value that was written is the value the editor shows.
    """
    out_file = tmp_path / 'out.json'
    model = EditModel(RewriteCfg(), out_file=out_file)
    model.set_text(path=('name',), text='typed text')
    assert model.save().saved
    assert _row(model, 'name').value == 'Typed text'
    assert _row(model, 'name').changed_by_validator
    assert _written(out_file) == {'name': 'Typed text'}


def test_save_leaves_nothing(tmp_path: Path) -> None:
    """Test a save answers the question of what is worth saving.

    What has just been written is not waiting to be written, so the values
    that reached the file become the ones the buffer is compared against.
    """
    model = EditModel(FlatCfg(), out_file=tmp_path / 'out.json')
    model.set_text(path=('answer',), text='7')
    assert model.dirty
    assert model.save().saved
    assert not model.dirty
    assert not _row(model, 'answer').edited
    assert _row(model, 'answer').value == 7


def test_edit_after_save(tmp_path: Path) -> None:
    """Test the next edit is worth saving again and drops the message."""
    model = EditModel(FlatCfg(), out_file=tmp_path / 'out.json')
    assert model.save().saved
    model.set_text(path=('answer',), text='7')
    assert model.dirty
    assert model.save_message == ''
    assert model.verdict is None


def test_saved_object_stays(tmp_path: Path) -> None:
    """Test a file that was written stays written after a further edit.

    `edit()` gives back what really reached the file, and an edit that came
    afterwards and was not saved does not take that back.
    """
    model = EditModel(FlatCfg(), out_file=tmp_path / 'out.json')
    assert model.save().saved
    model.set_text(path=('name',), text='typed later')
    assert model.saved_config is not None


def test_save_twice(tmp_path: Path) -> None:
    """Test a second save writes the values as they are by then."""
    out_file = tmp_path / 'out.json'
    model = EditModel(FlatCfg(), out_file=out_file)
    model.set_text(path=('answer',), text='7')
    assert model.save().saved
    model.set_text(path=('answer',), text='8')
    assert model.save().saved
    assert _written(out_file) == {'name': 'flat text', 'answer': 8}


def test_set_out_file(tmp_path: Path) -> None:
    """Test choosing a destination is what saving to it takes."""
    out_file = tmp_path / 'chosen.cfg'
    model = EditModel(FlatCfg())
    model.set_out_file(out_file)
    assert model.out_file == out_file
    assert model.save().saved
    assert out_file.exists()


def test_new_destination_text(tmp_path: Path) -> None:
    """Test choosing another destination drops what the last save said.

    "Saved to the other file" beside a destination that is now a different
    one would be true of nothing the user can see.
    """
    model = EditModel(FlatCfg(), out_file=tmp_path / 'first.json')
    assert model.save().saved
    model.set_out_file(tmp_path / 'second.json')
    assert model.save_message == ''


def test_save_containers(tmp_path: Path) -> None:
    """Test a member this version cannot edit is still saved as it was."""
    out_file = tmp_path / 'out.json'
    model = EditModel(ListCfg(), out_file=out_file)
    assert model.save().saved
    assert _written(out_file) == {'tags': ['first', 'second'], 'answer': 3,
                                  'limits': {'low': 1, 'high': 9}}
