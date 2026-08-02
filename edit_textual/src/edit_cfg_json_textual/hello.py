#! /usr/bin/env python3
"""Placeholder greeting for the Textual backend package."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import textual
from edit_cfg_json import core_greeting


def textual_greeting() -> str:
    """Return a greeting naming this backend and the Textual version.

    This is a placeholder until the real editor exists. It starts no
    application, so it also works outside a terminal.
    """
    return (f'{core_greeting()} Textual {textual.__version__} '
            'backend ready.')
