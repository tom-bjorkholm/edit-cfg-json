#! /usr/bin/env python3
"""Tests for what the model does about the file it writes.

Saving, what becomes of the file that a save is about to overwrite, where a
save writes, and what the file name settings of the application make of that.
They are here rather than with the rest of the model because one module of a
thousand lines is one nobody reads to the end, and because these are the tests
that have a file system in them: every one of them writes something.

What is refused about the values themselves belongs to the validation, and the
words of every one of these answers belong to the rendering, so both of those
are tested in the modules of their own.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import pytest
from edit_cfg_json import EditModel, MemberRow, Settings
from .model_helpers import written as _written
from .sample_cfg import FlatCfg, ListCfg, RangeCfg, RewriteCfg


def _row(model: EditModel, name: str) -> MemberRow:
    """Return the row of one member of a model."""
    return {row.name: row for row in model.rows}[name]


def _there(tmp_path: Path, name: str = 'out.json') -> Path:
    """Return an output file that already holds a configuration.

    It holds values that this class accepts, so that a save over it is
    refused by nothing but what the test is about.

    Args:
        tmp_path: Folder of one test.
        name: What the file is called inside it.

    Returns:
        That file.
    """
    out_file = tmp_path / name
    out_file.write_text('{"name": "was there", "answer": 1}', encoding='UTF-8')
    return out_file


def test_no_destination_yet() -> None:
    """Test a model built without an output file has none, and says nothing."""
    model = EditModel(FlatCfg())
    assert model.out_file is None
    assert model.save_message == ''
    assert model.saved_config is None


def test_save_needs_a_file() -> None:
    """Test a save with nowhere to write refuses and says why.

    The two editors turn this into a question, but the model has to answer
    it for a caller that cannot ask one, such as the non-interactive backend.
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
    assert 'greater than maximum 100' in verdict.refused[('answer',)]


def test_write_that_fails(tmp_path: Path) -> None:
    """Test a save the file system refuses leaves the session as it was.

    The buffer was valid and the values are perfectly good; what failed is the
    writing. So nothing about this save is kept: the model is still dirty, it
    has written nothing this session, and there is no saved object to hand
    back to the application.
    """
    out_file = tmp_path / 'no_such_folder' / 'out.json'
    model = EditModel(FlatCfg(), out_file=out_file)
    model.set_text(path=('answer',), text='7')
    outcome = model.save()
    assert not outcome.saved
    assert str(out_file) in outcome.message
    assert model.saved_config is None
    assert model.save_message == outcome.message
    assert model.dirty


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


def test_save_keeps_previous(tmp_path: Path) -> None:
    """Test a save over a file this session did not write keeps that file."""
    out_file = _there(tmp_path)
    outcome = EditModel(FlatCfg(), out_file=out_file).save()
    assert outcome.saved
    assert str(tmp_path / 'out.json.bak') in outcome.message
    assert _written(tmp_path / 'out.json.bak') == {'name': 'was there',
                                                   'answer': 1}


def test_kept_once_a_session(tmp_path: Path) -> None:
    """Test the second save over one destination keeps nothing.

    What it would keep is the first save of this same session, and keeping
    that would push the configuration that was really there one number
    further from being found.
    """
    model = EditModel(FlatCfg(), out_file=_there(tmp_path),
                      settings=Settings(backup_count=3))
    assert model.save().saved
    model.set_text(path=('answer',), text='7')
    outcome = model.save()
    assert outcome.saved
    assert 'previous content' not in outcome.message
    assert not (tmp_path / 'out.json.bak_2').exists()
    assert _written(tmp_path / 'out.json.bak_1') == {'name': 'was there',
                                                     'answer': 1}


def test_kept_per_destination(tmp_path: Path) -> None:
    """Test a session that writes two files keeps what each of them held."""
    first = _there(tmp_path, 'first.json')
    second = _there(tmp_path, 'second.json')
    model = EditModel(FlatCfg(), out_file=first)
    assert model.save().saved
    model.set_out_file(second)
    assert model.save().saved
    assert (tmp_path / 'first.json.bak').exists()
    assert (tmp_path / 'second.json.bak').exists()


def test_keeping_none(tmp_path: Path) -> None:
    """Test an application that keeps nothing is not given a kept file."""
    out_file = _there(tmp_path)
    model = EditModel(FlatCfg(), out_file=out_file,
                      settings=Settings(backup_suffix=None))
    outcome = model.save()
    assert outcome.saved
    assert 'previous content' not in outcome.message
    assert list(tmp_path.iterdir()) == [out_file]


def test_keeping_stops_save(tmp_path: Path) -> None:
    """Test a save that could not keep the previous content writes nothing.

    Overwriting cannot be undone, so a save that has just found it cannot
    keep what is there is the last moment at which anything can be done
    about it.
    """
    out_file = _there(tmp_path)
    (tmp_path / 'out.json.bak').mkdir()
    model = EditModel(FlatCfg(), out_file=out_file)
    outcome = model.save()
    assert not outcome.saved
    assert 'cannot be kept as' in outcome.message
    assert _written(out_file) == {'name': 'was there', 'answer': 1}
    assert model.saved_config is None


def test_nothing_overwritten(tmp_path: Path) -> None:
    """Test a destination that holds no file is nothing to ask about."""
    assert EditModel(FlatCfg()).overwritten_file is None
    assert EditModel(FlatCfg(),
                     out_file=tmp_path / 'out.json').overwritten_file is None


def test_overwritten_file(tmp_path: Path) -> None:
    """Test the file a save would overwrite is named until this one wrote it.

    A file this session has written is the user's own earlier save, and there
    is nothing to ask them about overwriting one of those.
    """
    out_file = _there(tmp_path)
    model = EditModel(FlatCfg(), out_file=out_file)
    assert model.overwritten_file == out_file
    assert model.save().saved
    assert model.overwritten_file is None


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


def test_settings_default() -> None:
    """Test a model built without settings has an application with none."""
    assert EditModel(FlatCfg()).settings == Settings()


def test_settings_asked_again() -> None:
    """Test a callable is asked again every time the settings are read.

    That is the whole of what handing a callable over buys, so a model that
    remembered the first answer would make the two forms the same thing.
    """
    answers = [Settings(file_extension='.one'),
               Settings(file_extension='.two')]
    model = EditModel(FlatCfg(), settings=answers.pop)
    assert model.settings.file_extension == '.two'
    assert model.settings.file_extension == '.one'


def test_chosen_gets_ext(tmp_path: Path) -> None:
    """Test a chosen destination without an extension gets the one used."""
    model = EditModel(FlatCfg(), settings=Settings(file_extension='.cfg'))
    model.set_out_file(tmp_path / 'chosen')
    assert model.out_file == f'{tmp_path / "chosen"}.cfg'
    assert model.save().saved
    assert (tmp_path / 'chosen.cfg').exists()


def test_other_extension_kept(tmp_path: Path) -> None:
    """Test a default extension leaves another extension alone."""
    out_file = tmp_path / 'chosen.json'
    model = EditModel(FlatCfg(), settings=Settings(file_extension='.cfg'))
    model.set_out_file(out_file)
    assert model.out_file == out_file
    assert model.save().saved


def test_given_out_file_kept(tmp_path: Path) -> None:
    """Test a destination this model was built with is taken as it is.

    The model cannot know whether it was chosen for this session or
    inherited from the input file, so it completes only what is chosen
    through `set_out_file` and takes what it is handed.
    """
    out_file = tmp_path / 'given'
    model = EditModel(FlatCfg(), out_file=out_file,
                      settings=Settings(file_extension='.cfg'))
    assert model.out_file == out_file
    assert model.save().saved
    assert not (tmp_path / 'given.cfg').exists()


@pytest.mark.parametrize('name', ['refused.json', 'refused'])
def test_enforced_refuses(tmp_path: Path, name: str) -> None:
    """Test an enforced extension refuses to write any other file."""
    out_file = tmp_path / name
    settings = Settings(file_extension='.cfg', extension_enforced=True)
    model = EditModel(FlatCfg(), out_file=out_file, settings=settings)
    outcome = model.save()
    assert not outcome.saved
    assert '.cfg extension' in outcome.message
    assert not out_file.exists()
    assert model.saved_config is None


def test_enforced_completes(tmp_path: Path) -> None:
    """Test an enforced extension still completes a name that has none."""
    settings = Settings(file_extension='.cfg', extension_enforced=True)
    model = EditModel(FlatCfg(), settings=settings)
    model.set_out_file(tmp_path / 'chosen')
    assert model.save().saved
    assert (tmp_path / 'chosen.cfg').exists()


def test_settings_at_save(tmp_path: Path) -> None:
    """Test the file name settings are read at the moment of the save.

    They are the ones a later answer from a callable can change, which is
    the difference between them and the key combinations.
    """
    answers = [Settings(), Settings(file_extension='.cfg',
                                    extension_enforced=True)]
    out_file = tmp_path / 'out.json'
    model = EditModel(FlatCfg(), out_file=out_file, settings=answers.pop)
    assert not model.save().saved
    assert model.save().saved


def test_save_containers(tmp_path: Path) -> None:
    """Test a member this version cannot edit is still saved as it was."""
    out_file = tmp_path / 'out.json'
    model = EditModel(ListCfg(), out_file=out_file)
    assert model.save().saved
    assert _written(out_file) == {'tags': ['first', 'second'], 'answer': 3,
                                  'limits': {'low': 1, 'high': 9}}
