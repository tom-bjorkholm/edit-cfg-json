#! /usr/bin/env python3
"""Tests for the placeholder greeting of edit_cfg_json."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import edit_cfg_json
from edit_cfg_json import core_greeting


def test_greeting_names_pkg() -> None:
    """Test the greeting names this package and the library it builds on."""
    greeting = core_greeting()
    assert greeting.startswith('Hello from edit_cfg_json.')
    assert 'config-as-json' in greeting


def test_greeting_is_exported() -> None:
    """Test the greeting is reachable from the top-level package."""
    assert 'core_greeting' in edit_cfg_json.__all__
    assert edit_cfg_json.core_greeting is core_greeting
