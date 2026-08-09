#! /usr/bin/env python3
"""Library for editing config-as-json.

Every name a user of this package needs is re-exported here, so
that nothing has to be imported from an internal module.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from edit_cfg_json.edit_model import EditModel
from edit_cfg_json.rows import MemberRow
from edit_cfg_json.backend import DumpEditor, EditorBackend
from edit_cfg_json.descriptions import Descriptions
from edit_cfg_json.editing import edit
from edit_cfg_json.loader import ConfigLoader, derived_loader
from edit_cfg_json.loading import ConfigLoadError, LoadPolicy, LoadReport, \
    LoadedConfig, default_config, load_config
from edit_cfg_json.emphasis import EXPLANATION, Emphasis, LOAD_REMARK, \
    MEMBER_DIAGNOSTIC, MEMBER_MARK, save_emphasis, subtree_emphasis, \
    verdict_emphasis
from edit_cfg_json.saving import SaveOutcome
from edit_cfg_json.settings import ActionSettings, Settings, SettingsSource
from edit_cfg_json.validation import ValidationVerdict
from edit_cfg_json.model_text import can_fold, docstring_text, fold_hides, \
    load_text, model_as_text, model_title, row_describes, row_description, \
    row_diagnostic, row_fold_text, row_marks, row_subtree_text, \
    row_validates, row_value_text, save_text, verdict_text
from edit_cfg_json.tree import path_text, text_path
from edit_cfg_json.cli import ExitCode, add_file_options, named_policy, \
    run_cli

__all__ = ['EditModel', 'MemberRow', 'EditorBackend', 'Descriptions', 'edit',
           'ConfigLoadError', 'ConfigLoader', 'LoadPolicy', 'LoadReport',
           'LoadedConfig', 'derived_loader', 'load_config', 'SaveOutcome',
           'ActionSettings', 'Settings',
           'SettingsSource', 'ValidationVerdict', 'Emphasis', 'EXPLANATION',
           'LOAD_REMARK', 'MEMBER_DIAGNOSTIC', 'MEMBER_MARK', 'save_emphasis',
           'subtree_emphasis', 'verdict_emphasis', 'can_fold',
           'docstring_text', 'fold_hides', 'load_text', 'model_as_text',
           'model_title', 'row_describes', 'row_description', 'row_diagnostic',
           'row_fold_text', 'row_marks', 'row_subtree_text', 'row_validates',
           'row_value_text',
           'save_text', 'verdict_text', 'path_text', 'text_path',
           'DumpEditor', 'ExitCode', 'add_file_options', 'default_config',
           'named_policy', 'run_cli']
