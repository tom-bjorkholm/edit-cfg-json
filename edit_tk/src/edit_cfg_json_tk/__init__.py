#! /usr/bin/env python3
"""Library for editing config-as-json with Tkinter.

Every name a user of this package needs is re-exported here, so
that nothing has to be imported from an internal module.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from edit_cfg_json_tk.tk_panel import TkEditor, TkEditorPanel, edit
from edit_cfg_json_tk.tk_version import TkVersionReporter
from edit_cfg_json_tk.tk_ui import TK_UI, tk_can_run

__all__ = ['TK_UI', 'TkEditor', 'TkEditorPanel', 'TkVersionReporter',
           'edit', 'tk_can_run']
