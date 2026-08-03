#! /usr/bin/env python3
"""Library for editing config-as-json.

Every name a user of this package needs is re-exported here, so
that nothing has to be imported from an internal module.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from edit_cfg_json.edit_model import EditModel, MemberRow
from edit_cfg_json.backend import EditorBackend
from edit_cfg_json.editing import edit
from edit_cfg_json.loading import ConfigLoadError, LoadPolicy, LoadReport, \
    LoadedConfig, load_config
from edit_cfg_json.saving import SaveOutcome
from edit_cfg_json.settings import ActionSettings, Settings, SettingsSource
from edit_cfg_json.validation import ValidationVerdict
from edit_cfg_json.model_text import load_text, model_as_text, model_title, \
    row_marks, row_value_text, save_text, verdict_text

__all__ = ['EditModel', 'MemberRow', 'EditorBackend', 'edit',
           'ConfigLoadError', 'LoadPolicy', 'LoadReport', 'LoadedConfig',
           'load_config', 'SaveOutcome', 'ActionSettings', 'Settings',
           'SettingsSource', 'ValidationVerdict', 'load_text',
           'model_as_text', 'model_title', 'row_marks', 'row_value_text',
           'save_text', 'verdict_text']
