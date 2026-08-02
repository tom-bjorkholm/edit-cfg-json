#! /usr/bin/env python3
"""Tests for example e01_hello."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest
from example import e01_hello


def test_main_prints_three(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the example prints one greeting per package."""
    e01_hello.main()
    lines = capsys.readouterr().out.splitlines()
    assert len(lines) == 3
    assert all(line.startswith('Hello from edit_cfg_json.')
               for line in lines)


def test_backends_extend_core(capsys: pytest.CaptureFixture[str]) -> None:
    """Test both backend lines are longer than the plain core line."""
    e01_hello.main()
    core, tk_line, textual_line = capsys.readouterr().out.splitlines()
    assert tk_line.startswith(core)
    assert textual_line.startswith(core)
