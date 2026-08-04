#! /usr/bin/env python3
"""Tests for writing a validated configuration object to a file.

These are the tests of the writing alone, and of the one question that is asked
just before it: whether the application would be able to read back the file
that is about to be written. What decides whether there is anything to write at
all belongs to the model, and is tested with it.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import json
import pytest
from edit_cfg_json import derived_loader
from edit_cfg_json.saving import NOT_LOADABLE, OTHER_CLASS, reload_refusal, \
    write_config
from .sample_cfg import PICKED_NAME, FlatCfg, PickedCfg, RangeCfg, \
    picking_loader

READ_ONLY = 0o444
"""Permission bits of a file that its owner may read and not write."""


def test_written_file_holds(tmp_path: Path) -> None:
    """Test the values of the configuration object reach the file."""
    out_file = tmp_path / 'out.json'
    outcome = write_config(config=FlatCfg('{"name": "text", "answer": 7}'),
                           out_file=out_file)
    assert outcome.saved
    assert str(out_file) in outcome.message
    assert json.loads(out_file.read_text(encoding='UTF-8')) == \
        {'name': 'text', 'answer': 7}


@pytest.mark.parametrize('extension', ['.json', '.cfg', '.conf', ''])
def test_any_extension(tmp_path: Path, extension: str) -> None:
    """Test the name of the output file is the caller's business alone.

    Applications differ over what a configuration file is called, so this
    library has no opinion about it and nothing here may start having one.
    """
    out_file = tmp_path / f'settings{extension}'
    assert write_config(config=FlatCfg(), out_file=out_file).saved
    assert out_file.exists()


def test_no_such_folder(tmp_path: Path) -> None:
    """Test a destination that cannot be written is a refusal, not a crash."""
    out_file = tmp_path / 'nowhere' / 'out.json'
    outcome = write_config(config=FlatCfg(), out_file=out_file)
    assert not outcome.saved
    assert str(out_file) in outcome.message
    assert 'FileNotFoundError' in outcome.message


def test_read_only_file(tmp_path: Path) -> None:
    """Test a file that may not be written is a refusal that keeps it.

    The file is left exactly as it was, which matters more than the message:
    an editor that emptied the file it could not write would be worse than
    one that could not save at all.
    """
    out_file = tmp_path / 'out.json'
    out_file.write_text('kept', encoding='UTF-8')
    out_file.chmod(READ_ONLY)
    try:
        outcome = write_config(config=FlatCfg(), out_file=out_file)
    finally:
        out_file.chmod(0o644)
    assert not outcome.saved
    assert 'PermissionError' in outcome.message
    assert out_file.read_text(encoding='UTF-8') == 'kept'


def test_nothing_printed(tmp_path: Path,
                         capsys: pytest.CaptureFixture[str]) -> None:
    """Test writing says nothing in the terminal behind the editor.

    Writing validates once more, and whatever that has to say belongs on the
    screen the editor owns. The verdict of the pass that has just run is
    already showing it.
    """
    write_config(config=FlatCfg(), out_file=tmp_path / 'out.json')
    assert capsys.readouterr() == ('', '')


def test_no_loader_no_ask() -> None:
    """Test an application that said nothing about loading is asked nothing."""
    assert reload_refusal(loader=None, config=FlatCfg()) == ''


def test_loader_rereads() -> None:
    """Test nothing stands in the way when the loader reads what is written."""
    assert reload_refusal(loader=picking_loader, config=FlatCfg()) == ''


def test_other_class_refused() -> None:
    """Test values that would select another class are not written.

    Which class is being edited was settled when the file was opened, and the
    rows are that class's members. A file that this application would read as
    another class is therefore not something the editor can write and go on
    showing what it is showing.
    """
    text = json.dumps({'name': PICKED_NAME, 'answer': 1})
    refusal = reload_refusal(loader=picking_loader,
                             config=FlatCfg(from_json_data_text=text))
    assert refusal == OTHER_CLASS.format(other='PickedCfg', own='FlatCfg')


class _MoreFlatCfg(FlatCfg):
    """The class being edited, in a more specific class of the same shape."""


def test_subclass_accepted() -> None:
    """Test a loader that answers with a subclass is answering with the class.

    `isinstance` is what the check asks, so an application that loads its own
    configuration as a more specific class than the one being edited is not
    stopped by this.
    """
    assert reload_refusal(loader=derived_loader(_MoreFlatCfg),
                          config=FlatCfg()) == ''


def test_chosen_class_is_kept() -> None:
    """Test the class a loader chose for a file is the one it is checked as."""
    text = json.dumps({'name': PICKED_NAME, 'answer': 1})
    assert reload_refusal(loader=picking_loader,
                          config=PickedCfg(from_json_data_text=text)) == ''


def test_loader_refuses_file() -> None:
    """Test a loader that could not read the file back stops the save.

    What the loader said is shown below the message, because that is the only
    thing that says why: the values are ones the class being edited accepts,
    and it is the way the application loads them that would not have them.
    """
    refusal = reload_refusal(loader=picking_loader, config=RangeCfg())
    assert refusal.startswith(NOT_LOADABLE)
    assert 'No value for name' in refusal
