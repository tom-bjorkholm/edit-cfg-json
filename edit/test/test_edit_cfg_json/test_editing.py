#! /usr/bin/env python3
"""Tests for the convenience wrapper around a model and a backend.

The backends here are the smallest thing that satisfies `EditorBackend`, which
is the point: `edit()` is what an application calls, and what it does to a
model has to be visible without a display. A backend that does nothing stands
in for a user who closed the editor, and one that saves stands in for a user
who pressed Save.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import json
import pytest
from edit_cfg_json import ConfigLoadError, EditModel, LoadPolicy, Settings, \
    edit, editor_model
from .sample_cfg import PICKED_NAME, ExtraArgCfg, FlatCfg, RangeCfg, \
    RewriteCfg, extra_arg_loader, picking_loader

COMPLETE = '{"name": "From a file", "answer": 7}'
"""An input file that holds every declared value."""

INCOMPLETE = '{"name": "Only a name"}'
"""An input file that leaves the number member out."""

UNKNOWN_KEY = '{"name": "n", "answer": 1, "colour": "red"}'
"""An input file with a key that the configuration does not declare."""


class Closer:  # pylint: disable=too-few-public-methods
    """A backend standing in for a user who closed the editor at once."""

    def __init__(self) -> None:
        """Start with no model seen yet."""
        self.seen: list[EditModel] = []

    def run_editor(self, model: EditModel) -> None:
        """Record the model and return without saving anything."""
        self.seen.append(model)


class Saver:  # pylint: disable=too-few-public-methods
    """A backend standing in for a user who edited and then pressed Save."""

    def __init__(self, name: str, text: str) -> None:
        """Say which member to edit and what to type into it.

        Args:
            name: Member the stand-in user edits.
            text: Text they type into it.
        """
        self._name = name
        self._text = text

    def run_editor(self, model: EditModel) -> None:
        """Edit the one member and save."""
        model.set_text(path=(self._name,), text=self._text)
        model.save()


def _input_file(tmp_path: Path, text: str) -> Path:
    """Write one input file and return where it is."""
    in_file = tmp_path / 'in.json'
    in_file.write_text(text, encoding='UTF-8')
    return in_file


def _written(out_file: Path) -> object:
    """Return what one output file holds, as JSON space values."""
    return json.loads(out_file.read_text(encoding='UTF-8'))


def test_round_trip(tmp_path: Path) -> None:
    """Test the whole way from an input file to an output file."""
    in_file = _input_file(tmp_path, COMPLETE)
    out_file = tmp_path / 'out.json'
    saved = edit(config=FlatCfg(), backend=Saver('answer', '9'),
                 in_file=in_file, out_file=out_file)
    assert isinstance(saved, FlatCfg)
    assert saved.answer == 9
    assert _written(out_file) == {'name': 'From a file', 'answer': 9}


def test_out_file_defaults(tmp_path: Path) -> None:
    """Test the input file is what is written when no output file is named.

    That is what an editor is normally asked to do, and saying it twice on
    every call would be the more usual case made the more tiresome one.
    """
    in_file = _input_file(tmp_path, COMPLETE)
    assert edit(config=FlatCfg(), backend=Saver('answer', '9'),
                in_file=in_file) is not None
    assert _written(in_file) == {'name': 'From a file', 'answer': 9}


def test_no_files_no_saving(tmp_path: Path) -> None:
    """Test a session with neither file has no destination to write to.

    The model says so and the backends turn that into a question. Nothing is
    invented, because a file name is not something a library can guess.
    """
    _ = tmp_path
    backend = Closer()
    assert edit(config=FlatCfg(), backend=backend) is None
    assert backend.seen[0].out_file is None


def test_closed_saves_none(tmp_path: Path) -> None:
    """Test a session that ends without saving writes no output file."""
    in_file = _input_file(tmp_path, COMPLETE)
    out_file = tmp_path / 'out.json'
    assert edit(config=FlatCfg(), backend=Closer(), in_file=in_file,
                out_file=out_file) is None
    assert not out_file.exists()


def test_caller_object_kept(tmp_path: Path) -> None:
    """Test the caller's own configuration object is never modified."""
    config = FlatCfg()
    saved = edit(config=config, backend=Saver('answer', '9'),
                 out_file=tmp_path / 'out.json')
    assert config.answer == 42
    assert saved is not None
    assert saved is not config


def test_values_from_the_file(tmp_path: Path) -> None:
    """Test the model a backend is given holds the values of the file."""
    backend = Closer()
    edit(config=FlatCfg(), backend=backend,
         in_file=_input_file(tmp_path, COMPLETE))
    assert [row.value for row in backend.seen[0].rows] == ['From a file', 7]


def test_report_reaches_model(tmp_path: Path) -> None:
    """Test what a permissive load did is in the model the backend gets."""
    backend = Closer()
    edit(config=FlatCfg(), backend=backend,
         in_file=_input_file(tmp_path, INCOMPLETE))
    model = backend.seen[0]
    assert 'filled in from the defaults' in model.load_message
    assert [row.filled_from_default for row in model.rows] == [False, True]


def test_strict_refuses(tmp_path: Path) -> None:
    """Test the policy reaches the load, so a strict run refuses this file."""
    with pytest.raises(ConfigLoadError):
        edit(config=FlatCfg(), backend=Closer(),
             in_file=_input_file(tmp_path, INCOMPLETE),
             policy=LoadPolicy.STRICT)


def test_load_error_raised(tmp_path: Path) -> None:
    """Test a file that cannot be opened is a refusal and not an editor.

    The exception reaches the application, which is the only place that
    knows how it wants to tell its user about a file.
    """
    with pytest.raises(ConfigLoadError):
        edit(config=FlatCfg(), backend=Closer(),
             in_file=_input_file(tmp_path, UNKNOWN_KEY))


def test_backend_not_run(tmp_path: Path) -> None:
    """Test a refused input file never reaches the user interface at all."""
    backend = Closer()
    with pytest.raises(ConfigLoadError):
        edit(config=FlatCfg(), backend=backend,
             in_file=_input_file(tmp_path, UNKNOWN_KEY))
    assert not backend.seen


def test_invalid_not_saved(tmp_path: Path) -> None:
    """Test a session whose buffer the application refuses saves nothing."""
    out_file = tmp_path / 'out.json'
    assert edit(config=RangeCfg(), backend=Saver('answer', '500'),
                out_file=out_file) is None
    assert not out_file.exists()


def test_descriptions_given() -> None:
    """Test what the application says about its members reaches the model."""
    backend = Closer()
    about = 'What the name of this configuration is for.'
    edit(config=FlatCfg(), backend=backend, descriptions={('name',): about})
    rows = {row.name: row for row in backend.seen[0].rows}
    assert rows['name'].description.startswith(about)
    assert 'whole number' in rows['answer'].description


def test_settings_reach_model() -> None:
    """Test the settings of the application reach the model a backend gets."""
    backend = Closer()
    settings = Settings(file_extension='.cfg')
    edit(config=FlatCfg(), backend=backend, settings=settings)
    assert backend.seen[0].settings is settings


def test_callable_reaches() -> None:
    """Test a callable is handed on rather than resolved on the way."""
    backend = Closer()
    edit(config=FlatCfg(), backend=backend,
         settings=lambda: Settings(file_extension='.cfg'))
    assert backend.seen[0].settings.file_extension == '.cfg'


def test_chosen_out_completed(tmp_path: Path) -> None:
    """Test an output file this call names gets the extension it lacks.

    A destination the call names is one that was chosen for this session,
    which is the case the completion is for.
    """
    saved = edit(config=FlatCfg(), backend=Saver('answer', '9'),
                 out_file=tmp_path / 'out',
                 settings=Settings(file_extension='.cfg'))
    assert saved is not None
    assert _written(tmp_path / 'out.cfg') == {'name': 'flat text',
                                              'answer': 9}


def test_input_out_kept(tmp_path: Path) -> None:
    """Test the input file is written as it is when no output was named.

    Reading one file and writing another because the two names differ by an
    extension would be a surprise, so a destination that was inherited is
    never completed.
    """
    in_file = tmp_path / 'in'
    in_file.write_text(COMPLETE, encoding='UTF-8')
    assert edit(config=FlatCfg(), backend=Saver('answer', '9'),
                in_file=in_file,
                settings=Settings(file_extension='.cfg')) is not None
    assert not (tmp_path / 'in.cfg').exists()
    assert _written(in_file) == {'name': 'From a file', 'answer': 9}


def test_enforced_in_refused(tmp_path: Path) -> None:
    """Test an input file without the enforced extension cannot be opened."""
    settings = Settings(file_extension='.cfg', extension_enforced=True)
    with pytest.raises(ConfigLoadError, match='.cfg extension'):
        edit(config=FlatCfg(), backend=Closer(), settings=settings,
             in_file=_input_file(tmp_path, COMPLETE))


def test_enforced_out_refused(tmp_path: Path) -> None:
    """Test an output file without the enforced extension is not written."""
    out_file = tmp_path / 'out.json'
    settings = Settings(file_extension='.cfg', extension_enforced=True)
    assert edit(config=FlatCfg(), backend=Saver('answer', '9'),
                out_file=out_file, settings=settings) is None
    assert not out_file.exists()


def test_saved_is_validated(tmp_path: Path) -> None:
    """Test the object handed back is the one the validators rewrote.

    An application that took the buffer at face value would disagree with
    its own file about the value of this member.
    """
    out_file = tmp_path / 'out.json'
    saved = edit(config=RewriteCfg(), backend=Saver('name', 'typed text'),
                 out_file=out_file)
    assert isinstance(saved, RewriteCfg)
    assert saved.name == 'Typed text'
    assert _written(out_file) == {'name': 'Typed text'}


def test_loader_round_trip(tmp_path: Path) -> None:
    """Test the whole way through, for a class the editor cannot construct.

    Only the reading of the input file needs the loader. Everything after it
    works on the object the load produced, which is why a class like this can
    be edited, validated and saved at all.
    """
    in_file = _input_file(tmp_path, '{"home": "from a file"}')
    out_file = tmp_path / 'out.json'
    saved = edit(config=ExtraArgCfg(home='here'), loader=extra_arg_loader,
                 backend=Saver('home', 'typed home'), in_file=in_file,
                 out_file=out_file)
    assert isinstance(saved, ExtraArgCfg)
    assert _written(out_file) == {'home': 'typed home'}


def test_no_loader_refuses_it(tmp_path: Path) -> None:
    """Test the same class without a loader cannot open the same file."""
    in_file = _input_file(tmp_path, '{"home": "from a file"}')
    with pytest.raises(ConfigLoadError):
        edit(config=ExtraArgCfg(home='here'), backend=Closer(),
             in_file=in_file)


def test_chosen_class_edited(tmp_path: Path) -> None:
    """Test a loader that chooses its class decides what is edited.

    The model is built on the object the load produced, so the class the file
    selected is the class whose members are the rows.
    """
    in_file = _input_file(tmp_path, json.dumps({'name': PICKED_NAME,
                                                'answer': 5}))
    backend = Closer()
    assert edit(config=FlatCfg(), backend=backend, loader=picking_loader,
                in_file=in_file) is None
    assert backend.seen[0].config_type_name == 'PickedCfg'


def test_other_class_kept(tmp_path: Path) -> None:
    """Test a value that would select another class is not written.

    The values are ones the class being edited accepts, so only the loader can
    say that the file they would write is a file of the other class. It is
    asked once, before anything is written.
    """
    out_file = tmp_path / 'out.json'
    saved = edit(config=FlatCfg(), loader=picking_loader,
                 backend=Saver('name', PICKED_NAME), out_file=out_file)
    assert saved is None
    assert not out_file.exists()


def test_model_holds_the_file(tmp_path: Path) -> None:
    """Test `editor_model` reads the file and answers with a model of it.

    It is what an application that mounts the editor in a window of its own
    reaches through the entry point of its backend, and what `edit` does
    before it runs one, so the two cannot differ about a session.
    """
    model = editor_model(FlatCfg(), in_file=_input_file(tmp_path, COMPLETE))
    assert isinstance(model, EditModel)
    assert [row.value for row in model.rows] == ['From a file', 7]
    assert not model.dirty


def test_model_report_reaches(tmp_path: Path) -> None:
    """Test what a permissive load did is on the model it answers with."""
    model = editor_model(FlatCfg(), in_file=_input_file(tmp_path, INCOMPLETE))
    assert 'filled in from the defaults' in model.load_message
    assert [row.filled_from_default for row in model.rows] == [False, True]


def test_model_file_refused(tmp_path: Path) -> None:
    """Test a file that cannot be opened is refused here as well."""
    with pytest.raises(ConfigLoadError):
        editor_model(FlatCfg(), in_file=_input_file(tmp_path, INCOMPLETE),
                     policy=LoadPolicy.STRICT)


def test_model_out_completed(tmp_path: Path) -> None:
    """Test a destination this call names gets the extension it lacks.

    That is the one rule `edit` applies to its arguments beyond handing them
    on, so it has to be here rather than in `edit`.
    """
    model = editor_model(FlatCfg(), out_file=tmp_path / 'out',
                         settings=Settings(file_extension='.cfg'))
    assert str(model.out_file) == str(tmp_path / 'out.cfg')


def test_model_writes_input(tmp_path: Path) -> None:
    """Test the input file is what a save writes when nothing else is named."""
    in_file = _input_file(tmp_path, COMPLETE)
    assert str(editor_model(FlatCfg(),
                            in_file=in_file).out_file) == str(in_file)


def test_model_is_described() -> None:
    """Test what the application says about its members reaches the model.

    What the editor says about a member is what the application said plus what
    kind of value it holds, which the core decides and tests of its own cover.
    """
    about_name = 'What the name is for.'
    model = editor_model(FlatCfg(), descriptions={('name',): about_name})
    assert model.rows[0].description.startswith(about_name)
