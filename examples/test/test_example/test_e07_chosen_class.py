#! /usr/bin/env python3
"""Tests for example e07_chosen_class.

What this example adds is a loader that chooses its class by looking at the
JSON, so what is asserted here is the two rules that make that work: the class
of the session is the class the file selected, and a value that would select
another class is refused by the save rather than followed.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import json
import pytest
from example import e07_chosen_class
from example.e07_chosen_class import FINEST_MODEL_GRID, MODE_2D, MODE_3D, \
    Cad2DConfig, Cad3DConfig, chosen_config
from .helpers import data_file, dump, head, open_tk_ui, saved_tail, \
    textual_titles

VALID_LINE = 'validation: valid'
"""Line that `--ui dump` ends with for a buffer the example accepts."""

DRAWING_FILE = 'e07_drawing.json'
"""Input file that the loader reads as a drawing configuration."""

MODEL_FILE = 'e07_model.json'
"""Input file that the loader reads as a model configuration."""


def _dump(capsys: pytest.CaptureFixture[str], *settings: str) -> str:
    """Run this example with `--ui dump` and return what it printed."""
    return dump(e07_chosen_class.main, capsys, *settings)


def test_default_class(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the class of a configuration that does not exist yet is used.

    A loader answers a call with no JSON source, and there is nothing to look
    at then, so this loader names the class it uses for a new configuration.
    """
    printed = _dump(capsys)
    assert printed.startswith(head(Cad2DConfig()))
    assert f'mode = {MODE_2D}' in printed
    assert VALID_LINE in printed


def test_file_chooses_2d(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a drawing file is edited as the drawing class."""
    printed = _dump(capsys, '-i', data_file(DRAWING_FILE))
    assert printed.startswith(head(Cad2DConfig()))
    assert 'project_name = bracket-outline' in printed
    assert VALID_LINE in printed


def test_file_chooses_3d(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a model file of the same shape is edited as the model class.

    The two classes hold the same three members, so nothing but the loader
    could have told them apart, and the label of the configuration is what
    says which of them the session is about.
    """
    printed = _dump(capsys, '-i', data_file(MODEL_FILE))
    assert printed.startswith(head(Cad3DConfig()))
    assert 'project_name = bracket-solid' in printed
    assert VALID_LINE in printed


def test_finest_grid_differs(capsys: pytest.CaptureFixture[str]) -> None:
    """Test each class applies its own rule to the grid it is given.

    The grid of the drawing file is finer than a model may use, so the one
    value is accepted by one class and refused by the other. That is the whole
    reason an application would choose its class by the file.
    """
    printed = _dump(capsys, '-i', data_file(MODEL_FILE), '--set',
                    'grid_size_mm=0.05')
    assert f'minimum {FINEST_MODEL_GRID}' in printed
    assert 'validation: invalid, see grid_size_mm' in printed


def test_other_class_refused(tmp_path: Path,
                             capsys: pytest.CaptureFixture[str]) -> None:
    """Test a mode that selects the other class is refused by the save.

    Both values are ones the class being edited accepts, so the validation
    says valid and only the loader can say that the file these values would
    write is a file of the other class.
    """
    out_file = tmp_path / 'out.json'
    printed = _dump(capsys, '-i', data_file(MODEL_FILE), '-o', str(out_file),
                    '--set', f'mode={MODE_2D}', '--save')
    assert VALID_LINE in printed
    assert 'would read the file' in printed
    assert 'Cad2DConfig' in printed
    assert not out_file.exists()


def test_unreadable_refused(tmp_path: Path,
                            capsys: pytest.CaptureFixture[str]) -> None:
    """Test a file the application could not read at all is not written.

    The other way round from the test above: the drawing values are ones the
    model class refuses, so the loader does not reach the point of answering
    with a class at all and says what its own rule said instead.
    """
    out_file = tmp_path / 'out.json'
    printed = _dump(capsys, '-i', data_file(DRAWING_FILE), '-o', str(out_file),
                    '--set', f'mode={MODE_3D}', '--save')
    assert VALID_LINE in printed
    assert 'would not be able to read back' in printed
    assert not out_file.exists()


def test_round_trip(tmp_path: Path,
                    capsys: pytest.CaptureFixture[str]) -> None:
    """Test a file whose class stays the same is written as it should be."""
    out_file = tmp_path / 'out.json'
    printed = _dump(capsys, '-i', data_file(MODEL_FILE), '-o', str(out_file),
                    '--set', 'project_name=other-part', '--save')
    assert printed.endswith(saved_tail(out_file, 'Cad3DConfig'))
    assert json.loads(out_file.read_text(encoding='UTF-8')) == \
        {'mode': MODE_3D, 'project_name': 'other-part', 'grid_size_mm': 2.0}


def test_loader_takes_no_file() -> None:
    """Test the loader of this example refuses a file name it cannot read.

    The editor reads its own input files and never passes one, so a name is a
    mistake in the application rather than something to be ignored.
    """
    with pytest.raises(ValueError):
        chosen_config(from_json_filename=data_file(MODEL_FILE))


def test_tk_ui_opens(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui tk builds the window and returns when it is closed."""
    open_tk_ui(e07_chosen_class.main, monkeypatch, '-i', data_file(MODEL_FILE))


def test_textual_ui_opens(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui textual starts an application named after the chosen class."""
    assert textual_titles(e07_chosen_class.main, monkeypatch, '-i',
                          data_file(MODEL_FILE)) == ['Cad3DConfig']
