#! /usr/bin/env python3
"""Tests for the placeholder greeting of edit_cfg_json_tk."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from edit_cfg_json import core_greeting
import edit_cfg_json_tk
from edit_cfg_json_tk import tk_greeting


def test_greeting_has_core() -> None:
    """Test the backend greeting builds on the core greeting."""
    greeting = tk_greeting()
    assert greeting.startswith(core_greeting())
    assert greeting.endswith('backend ready.')
    assert ' Tk ' in greeting


def test_greeting_is_exported() -> None:
    """Test the greeting is reachable from the top-level package."""
    assert 'tk_greeting' in edit_cfg_json_tk.__all__
    assert edit_cfg_json_tk.tk_greeting is tk_greeting
