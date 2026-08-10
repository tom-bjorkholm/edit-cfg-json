#! /usr/bin/env python3
"""Tests for what `python3 -m edit_cfg_json.dump` does when it runs.

What the shared command line does is tested in `test_cli`, and that each of the
three packages ships the program it promises is tested in `test_programs`. What
is left is this one program's own behaviour: it prints the configuration it was
asked for, and with `--save` it writes the file, both of which it can do on a
machine with no display at all.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import json
import pytest
from edit_cfg_json import ExitCode
from edit_cfg_json.dump import main

SAMPLE = 'test_edit_cfg_json.sample_cfg'
"""Module that these tests reach a configuration class through."""


def test_prints_the_model(capsys: pytest.CaptureFixture[str]) -> None:
    """Test running the program prints the model of that class."""
    assert main(['--module', SAMPLE, '--class', 'FlatCfg']) == ExitCode.OK
    printed = capsys.readouterr().out
    assert 'FlatCfg' in printed
    assert 'name = flat text' in printed
    assert 'validation: valid' in printed


def test_saves_when_asked(tmp_path: Path) -> None:
    """Test the program writes a file the configuration class can read back."""
    out_file = tmp_path / 'written.json'
    assert main(['--module', SAMPLE, '--class', 'FlatCfg', '-o', str(out_file),
                 '--save']) == ExitCode.OK
    assert json.loads(out_file.read_text(encoding='UTF-8')) == {
        'name': 'flat text', 'answer': 42}


def test_normalizes_a_file(tmp_path: Path) -> None:
    """Test the program can put a file into the form the class writes.

    That is what `--save` is for beyond the round trip: a file that is
    incomplete, or written in an order of its own, comes back as the file the
    configuration class would have written.
    """
    in_file = tmp_path / 'partial.json'
    in_file.write_text(json.dumps({'name': 'only a name'}), encoding='UTF-8')
    assert main(['--module', SAMPLE, '--class', 'FlatCfg', '-i', str(in_file),
                 '--save']) == ExitCode.OK
    assert json.loads(in_file.read_text(encoding='UTF-8')) == {
        'name': 'only a name', 'answer': 42}
