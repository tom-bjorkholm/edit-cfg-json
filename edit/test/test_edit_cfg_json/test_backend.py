#! /usr/bin/env python3
"""Tests for the one backend that this package ships.

`DumpEditor` needs no display, so what it does can be read straight off the
output it prints. What is worth testing is that it validates rather than
printing whatever the buffer happens to hold, and that a save the caller
already asked for is still reported afterwards: the backend is what shows the
user what the save did, and it runs after the save rather than before it.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import pytest
from edit_cfg_json import DumpEditor, EditModel, model_as_text
from .sample_cfg import FlatCfg, RangeCfg


def test_dump_validates() -> None:
    """Test the printed model says what the application makes of it."""
    model = EditModel(FlatCfg())
    assert model.verdict is None
    DumpEditor().run_editor(model)
    assert model.verdict is not None
    assert model.verdict.valid


def test_dump_prints_model(capsys: pytest.CaptureFixture[str]) -> None:
    """Test what is printed is the model rendering and nothing else."""
    model = EditModel(FlatCfg())
    DumpEditor().run_editor(model)
    printed = capsys.readouterr().out
    model.validate()
    assert printed == f'{model_as_text(model)}\n'


def test_dump_shows_refusal(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a buffer the application refuses is printed as refused."""
    model = EditModel(RangeCfg())
    model.set_text(path=('answer',), text='500')
    DumpEditor().run_editor(model)
    assert 'invalid' in capsys.readouterr().out


def test_dump_after_save(tmp_path: Path,
                         capsys: pytest.CaptureFixture[str]) -> None:
    """Test a save the caller asked for is still reported by the dump."""
    out_file = tmp_path / 'saved.json'
    model = EditModel(FlatCfg(), out_file=out_file)
    model.save()
    DumpEditor().run_editor(model)
    assert str(out_file) in capsys.readouterr().out
    assert out_file.is_file()
