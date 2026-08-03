#! /usr/bin/env python3
"""Library for editing config-as-json with Tkinter.

Every name a user of this package needs is re-exported here, so
that nothing has to be imported from an internal module.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from edit_cfg_json_tk.tk_editor import TkEditor, edit

__all__ = ['TkEditor', 'edit']
