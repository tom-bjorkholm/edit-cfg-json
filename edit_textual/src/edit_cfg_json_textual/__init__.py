#! /usr/bin/env python3
"""Library for editing config-as-json with textual.

Every name a user of this package needs is re-exported here, so
that nothing has to be imported from an internal module.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from edit_cfg_json_textual.textual_editor import TextualEditor, edit
from edit_cfg_json_textual.textual_mount import EditorPanel, EditorScreen
from edit_cfg_json_textual.textual_version import TextualVersionReporter
from edit_cfg_json_textual.textual_ui import TEXTUAL_UI, textual_can_run

__all__ = ['EditorPanel', 'EditorScreen', 'TEXTUAL_UI', 'TextualEditor',
           'TextualVersionReporter', 'edit', 'textual_can_run']
