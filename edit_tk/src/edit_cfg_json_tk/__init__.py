#! /usr/bin/env python3
"""Library for editing config-as-json with Tkinter.

Every name a user of this package needs is re-exported here, so
that nothing has to be imported from an internal module.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from edit_cfg_json_tk.tk_panel import TkEditor, TkEditorPanel, edit
from edit_cfg_json_tk.tk_version import TkVersionReporter

__all__ = ['TkEditor', 'TkEditorPanel', 'TkVersionReporter', 'edit']
