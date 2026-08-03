#! /usr/bin/env python3
"""Tests for the translation into the notation that Tk binds by.

This needs no display and no Tk at all: it is text going in and text coming
out, which is why the translation is a module of its own.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
import pytest
from edit_cfg_json import ActionSettings
from edit_cfg_json_tk.key_names import tk_sequence


@pytest.mark.parametrize('combination, expected', [
    ('ctrl+q', '<Control-q>'),
    ('ctrl+r', '<Control-r>'),
    ('ctrl+s', '<Control-s>'),
    ('ctrl+shift+s', '<Control-Shift-S>'),
    ('shift+a', '<Shift-A>'),
    ('alt+x', '<Alt-x>'),
    ('meta+x', '<Meta-x>'),
    ('f5', '<F5>'),
    ('f12', '<F12>'),
    ('escape', '<Escape>'),
    ('enter', '<Return>'),
    ('pageup', '<Prior>'),
    ('ctrl+alt+delete', '<Control-Alt-Delete>'),
    ('CTRL+Q', '<Control-q>')])
def test_translated(combination: str, expected: str) -> None:
    """Test a combination this backend knows becomes a Tk sequence."""
    assert tk_sequence(combination) == expected


@pytest.mark.parametrize('combination', ['', 'super+x', 'ctrl+nonsense',
                                         'ctrl+', 'fx'])
def test_not_translated(combination: str) -> None:
    """Test a combination this backend does not know is left alone.

    None is not an error. The action it belongs to keeps its button and
    loses only that way of reaching it, which is the same choice the whole
    editor makes about anything it cannot work out.
    """
    assert tk_sequence(combination) is None


def test_every_default_known() -> None:
    """Test every key the editor chooses by default can be bound in Tk.

    A default that this backend could not translate would be a key that
    works in one editor and silently not in the other.
    """
    defaults = ActionSettings()
    every: list[Optional[str]] = [tk_sequence(key)
                                  for keys in (defaults.quit,
                                               defaults.validate,
                                               defaults.save,
                                               defaults.save_as,
                                               defaults.cancel)
                                  for key in keys]
    assert every and all(sequence is not None for sequence in every)
