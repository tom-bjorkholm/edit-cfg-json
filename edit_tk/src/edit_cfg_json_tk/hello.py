#! /usr/bin/env python3
"""Placeholder greeting for the Tkinter backend package."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from edit_cfg_json import core_greeting


def tk_greeting() -> str:
    """Return a greeting naming this backend and the available Tk version.

    This is a placeholder until the real editor exists. It reads the Tk
    version without creating a window, so it also works on a machine
    with no display.
    """
    return f'{core_greeting()} Tk {tkinter.TkVersion} backend ready.'
