#! /usr/bin/env python3
"""Tests for writing a validated configuration object to a file.

These are the tests of the writing alone. What decides whether there is
anything to write belongs to the model, and is tested with it.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import json
import pytest
from edit_cfg_json.saving import write_config
from .sample_cfg import FlatCfg

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
