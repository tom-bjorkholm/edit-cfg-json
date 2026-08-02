#! /usr/bin/env python3
"""Tests for the placeholder greeting of edit_cfg_json_textual."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from edit_cfg_json import core_greeting
import edit_cfg_json_textual
from edit_cfg_json_textual import textual_greeting


def test_greeting_has_core() -> None:
    """Test the backend greeting builds on the core greeting."""
    greeting = textual_greeting()
    assert greeting.startswith(core_greeting())
    assert greeting.endswith('backend ready.')
    assert ' Textual ' in greeting


def test_greeting_is_exported() -> None:
    """Test the greeting is reachable from the top-level package."""
    assert 'textual_greeting' in edit_cfg_json_textual.__all__
    assert edit_cfg_json_textual.textual_greeting is textual_greeting
