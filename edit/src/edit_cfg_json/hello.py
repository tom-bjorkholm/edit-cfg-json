#! /usr/bin/env python3
"""Placeholder greeting for the user interface agnostic core package."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from importlib.metadata import version
from config_as_json import Config

CONFIG_PACKAGE = 'config-as-json'


def core_greeting() -> str:
    """Return a greeting naming this package and the library it builds on.

    This is a placeholder until the real editor exists. It imports and
    names `config_as_json` so that a greeting that can be produced at all
    is evidence that the declared dependency resolved in the environment
    the greeting runs in.
    """
    return (f'Hello from edit_cfg_json. It edits {Config.__name__} objects '
            f'from {CONFIG_PACKAGE} {version(CONFIG_PACKAGE)}.')
