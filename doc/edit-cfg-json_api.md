# Table of Contents

* [edit\_cfg\_json.tree](#edit_cfg_json.tree)
  * [EVERY\_ELEMENT](#edit_cfg_json.tree.EVERY_ELEMENT)
  * [PATH\_SEPARATOR](#edit_cfg_json.tree.PATH_SEPARATOR)
  * [ELEMENTS\_FORM](#edit_cfg_json.tree.ELEMENTS_FORM)
  * [ELEMENT\_FORM](#edit_cfg_json.tree.ELEMENT_FORM)
  * [ENTRIES\_FORM](#edit_cfg_json.tree.ENTRIES_FORM)
  * [ENTRY\_FORM](#edit_cfg_json.tree.ENTRY_FORM)
  * [NO\_OBJECT\_FORM](#edit_cfg_json.tree.NO_OBJECT_FORM)
  * [OPEN\_AT\_MOST](#edit_cfg_json.tree.OPEN_AT_MOST)
  * [path\_text](#edit_cfg_json.tree.path_text)
  * [text\_path](#edit_cfg_json.tree.text_path)
  * [is\_container](#edit_cfg_json.tree.is_container)
  * [container\_text](#edit_cfg_json.tree.container_text)
  * [rows\_below](#edit_cfg_json.tree.rows_below)
  * [starts\_folded](#edit_cfg_json.tree.starts_folded)
  * [child\_values](#edit_cfg_json.tree.child_values)
  * [selects](#edit_cfg_json.tree.selects)
  * [ConfigNode](#edit_cfg_json.tree.ConfigNode)
    * [config\_type](#edit_cfg_json.tree.ConfigNode.config_type)
    * [config](#edit_cfg_json.tree.ConfigNode.config)
  * [config\_nodes](#edit_cfg_json.tree.config_nodes)
  * [owner\_path](#edit_cfg_json.tree.owner_path)
  * [ordered\_names](#edit_cfg_json.tree.ordered_names)
  * [flat\_values](#edit_cfg_json.tree.flat_values)
  * [under\_dict](#edit_cfg_json.tree.under_dict)
  * [assembled](#edit_cfg_json.tree.assembled)
* [edit\_cfg\_json.loading](#edit_cfg_json.loading)
  * [DEFAULTS\_ERRORS](#edit_cfg_json.loading.DEFAULTS_ERRORS)
  * [NO\_FILE](#edit_cfg_json.loading.NO_FILE)
  * [NOT\_TEXT](#edit_cfg_json.loading.NOT_TEXT)
  * [NOT\_CONFIG](#edit_cfg_json.loading.NOT_CONFIG)
  * [UNKNOWN\_KEY](#edit_cfg_json.loading.UNKNOWN_KEY)
  * [INCOMPLETE](#edit_cfg_json.loading.INCOMPLETE)
  * [BAD\_VALUES](#edit_cfg_json.loading.BAD_VALUES)
  * [NO\_DEFAULTS](#edit_cfg_json.loading.NO_DEFAULTS)
  * [FILLED\_MESSAGE](#edit_cfg_json.loading.FILLED_MESSAGE)
  * [AUTO\_CHANGED](#edit_cfg_json.loading.AUTO_CHANGED)
  * [DROPPED\_FORM](#edit_cfg_json.loading.DROPPED_FORM)
  * [SUPPLIED\_FORM](#edit_cfg_json.loading.SUPPLIED_FORM)
  * [VALUED\_FORM](#edit_cfg_json.loading.VALUED_FORM)
  * [NORMALIZED\_REASON](#edit_cfg_json.loading.NORMALIZED_REASON)
  * [REASON\_FORMS](#edit_cfg_json.loading.REASON_FORMS)
  * [MORE\_REASONS\_FORM](#edit_cfg_json.loading.MORE_REASONS_FORM)
  * [LoadPolicy](#edit_cfg_json.loading.LoadPolicy)
    * [STRICT](#edit_cfg_json.loading.LoadPolicy.STRICT)
    * [DEFAULTS](#edit_cfg_json.loading.LoadPolicy.DEFAULTS)
    * [STRICT\_THEN\_DEFAULTS](#edit_cfg_json.loading.LoadPolicy.STRICT_THEN_DEFAULTS)
  * [DEFAULT\_POLICY](#edit_cfg_json.loading.DEFAULT_POLICY)
  * [LoadReport](#edit_cfg_json.loading.LoadReport)
    * [message](#edit_cfg_json.loading.LoadReport.message)
    * [filled](#edit_cfg_json.loading.LoadReport.filled)
    * [reasons](#edit_cfg_json.loading.LoadReport.reasons)
  * [LoadedConfig](#edit_cfg_json.loading.LoadedConfig)
    * [config](#edit_cfg_json.loading.LoadedConfig.config)
    * [report](#edit_cfg_json.loading.LoadedConfig.report)
  * [ConfigLoadError](#edit_cfg_json.loading.ConfigLoadError)
    * [\_\_init\_\_](#edit_cfg_json.loading.ConfigLoadError.__init__)
  * [default\_config](#edit_cfg_json.loading.default_config)
  * [load\_config](#edit_cfg_json.loading.load_config)
* [edit\_cfg\_json.backend](#edit_cfg_json.backend)
  * [EditorBackend](#edit_cfg_json.backend.EditorBackend)
    * [run\_editor](#edit_cfg_json.backend.EditorBackend.run_editor)
  * [DumpEditor](#edit_cfg_json.backend.DumpEditor)
    * [run\_editor](#edit_cfg_json.backend.DumpEditor.run_editor)
* [edit\_cfg\_json.editing](#edit_cfg_json.editing)
  * [edit](#edit_cfg_json.editing.edit)
* [edit\_cfg\_json.saving](#edit_cfg_json.saving)
  * [NO\_DESTINATION](#edit_cfg_json.saving.NO_DESTINATION)
  * [NOT\_VALID](#edit_cfg_json.saving.NOT_VALID)
  * [NOT\_LOADABLE](#edit_cfg_json.saving.NOT_LOADABLE)
  * [OTHER\_CLASS](#edit_cfg_json.saving.OTHER_CLASS)
  * [RELOAD\_ERRORS](#edit_cfg_json.saving.RELOAD_ERRORS)
  * [WRITE\_FAILED](#edit_cfg_json.saving.WRITE_FAILED)
  * [SAVED](#edit_cfg_json.saving.SAVED)
  * [WRITE\_ERRORS](#edit_cfg_json.saving.WRITE_ERRORS)
  * [SaveOutcome](#edit_cfg_json.saving.SaveOutcome)
    * [saved](#edit_cfg_json.saving.SaveOutcome.saved)
    * [message](#edit_cfg_json.saving.SaveOutcome.message)
  * [SaveState](#edit_cfg_json.saving.SaveState)
    * [out\_file](#edit_cfg_json.saving.SaveState.out_file)
    * [outcome](#edit_cfg_json.saving.SaveState.outcome)
    * [written](#edit_cfg_json.saving.SaveState.written)
  * [reload\_refusal](#edit_cfg_json.saving.reload_refusal)
  * [write\_config](#edit_cfg_json.saving.write_config)
* [edit\_cfg\_json.converting](#edit_cfg_json.converting)
  * [CONVERSION\_ERRORS](#edit_cfg_json.converting.CONVERSION_ERRORS)
  * [Converted](#edit_cfg_json.converting.Converted)
    * [value](#edit_cfg_json.converting.Converted.value)
    * [message](#edit_cfg_json.converting.Converted.message)
  * [member\_converters](#edit_cfg_json.converting.member_converters)
  * [node\_converters](#edit_cfg_json.converting.node_converters)
  * [convert\_member](#edit_cfg_json.converting.convert_member)
  * [refusal\_text](#edit_cfg_json.converting.refusal_text)
* [edit\_cfg\_json.cli](#edit_cfg_json.cli)
  * [DESCRIPTION](#edit_cfg_json.cli.DESCRIPTION)
  * [PYTHON\_SUFFIX](#edit_cfg_json.cli.PYTHON_SUFFIX)
  * [POLICY\_NAMES](#edit_cfg_json.cli.POLICY_NAMES)
  * [NO\_MODULE\_MESSAGE](#edit_cfg_json.cli.NO_MODULE_MESSAGE)
  * [NO\_FILE\_MESSAGE](#edit_cfg_json.cli.NO_FILE_MESSAGE)
  * [NOT\_PYTHON\_MESSAGE](#edit_cfg_json.cli.NOT_PYTHON_MESSAGE)
  * [NOT\_IMPORTABLE\_MESSAGE](#edit_cfg_json.cli.NOT_IMPORTABLE_MESSAGE)
  * [NO\_NAME\_MESSAGE](#edit_cfg_json.cli.NO_NAME_MESSAGE)
  * [NOT\_CONFIG\_MESSAGE](#edit_cfg_json.cli.NOT_CONFIG_MESSAGE)
  * [NO\_TARGET\_MESSAGE](#edit_cfg_json.cli.NO_TARGET_MESSAGE)
  * [NOT\_LOADER\_MESSAGE](#edit_cfg_json.cli.NOT_LOADER_MESSAGE)
  * [LOADER\_ARGS\_MESSAGE](#edit_cfg_json.cli.LOADER_ARGS_MESSAGE)
  * [NO\_LOADER\_CONFIG](#edit_cfg_json.cli.NO_LOADER_CONFIG)
  * [WRONG\_CLASS\_MESSAGE](#edit_cfg_json.cli.WRONG_CLASS_MESSAGE)
  * [NOT\_DESCRIPTIONS](#edit_cfg_json.cli.NOT_DESCRIPTIONS)
  * [NOT\_SHOWABLE\_MESSAGE](#edit_cfg_json.cli.NOT_SHOWABLE_MESSAGE)
  * [ExitCode](#edit_cfg_json.cli.ExitCode)
    * [OK](#edit_cfg_json.cli.ExitCode.OK)
    * [LOAD\_REFUSED](#edit_cfg_json.cli.ExitCode.LOAD_REFUSED)
    * [USAGE](#edit_cfg_json.cli.ExitCode.USAGE)
    * [NO\_MODULE](#edit_cfg_json.cli.ExitCode.NO_MODULE)
    * [NO\_FILE](#edit_cfg_json.cli.ExitCode.NO_FILE)
    * [NOT\_PYTHON](#edit_cfg_json.cli.ExitCode.NOT_PYTHON)
    * [NOT\_IMPORTABLE](#edit_cfg_json.cli.ExitCode.NOT_IMPORTABLE)
    * [NO\_NAME](#edit_cfg_json.cli.ExitCode.NO_NAME)
    * [NOT\_CONFIG](#edit_cfg_json.cli.ExitCode.NOT_CONFIG)
    * [NO\_DEFAULTS](#edit_cfg_json.cli.ExitCode.NO_DEFAULTS)
    * [INVALID](#edit_cfg_json.cli.ExitCode.INVALID)
    * [NOT\_WRITTEN](#edit_cfg_json.cli.ExitCode.NOT_WRITTEN)
    * [NOT\_SHOWABLE](#edit_cfg_json.cli.ExitCode.NOT_SHOWABLE)
    * [NOT\_LOADER](#edit_cfg_json.cli.ExitCode.NOT_LOADER)
    * [LOADER\_ARGS](#edit_cfg_json.cli.ExitCode.LOADER_ARGS)
    * [WRONG\_CLASS](#edit_cfg_json.cli.ExitCode.WRONG_CLASS)
    * [NOT\_DESCRIPTIONS](#edit_cfg_json.cli.ExitCode.NOT_DESCRIPTIONS)
  * [named\_policy](#edit_cfg_json.cli.named_policy)
  * [add\_file\_options](#edit_cfg_json.cli.add_file_options)
  * [run\_cli](#edit_cfg_json.cli.run_cli)
* [edit\_cfg\_json.leaf\_value](#edit_cfg_json.leaf_value)
  * [TEXT\_KIND](#edit_cfg_json.leaf_value.TEXT_KIND)
  * [WHOLE\_NUMBER\_KIND](#edit_cfg_json.leaf_value.WHOLE_NUMBER_KIND)
  * [NUMBER\_KIND](#edit_cfg_json.leaf_value.NUMBER_KIND)
  * [BOOL\_KIND](#edit_cfg_json.leaf_value.BOOL_KIND)
  * [VALUE\_KINDS](#edit_cfg_json.leaf_value.VALUE_KINDS)
  * [NO\_KIND](#edit_cfg_json.leaf_value.NO_KIND)
  * [value\_as\_text](#edit_cfg_json.leaf_value.value_as_text)
  * [text\_as\_value](#edit_cfg_json.leaf_value.text_as_value)
  * [values\_differ](#edit_cfg_json.leaf_value.values_differ)
  * [value\_kind](#edit_cfg_json.leaf_value.value_kind)
* [edit\_cfg\_json.loader](#edit_cfg_json.loader)
  * [NO\_FILE\_NAME](#edit_cfg_json.loader.NO_FILE_NAME)
  * [LOADER\_EXITED](#edit_cfg_json.loader.LOADER_EXITED)
  * [ConfigLoader](#edit_cfg_json.loader.ConfigLoader)
    * [\_\_call\_\_](#edit_cfg_json.loader.ConfigLoader.__call__)
  * [derived\_loader](#edit_cfg_json.loader.derived_loader)
  * [ask\_loader](#edit_cfg_json.loader.ask_loader)
  * [ConfigSource](#edit_cfg_json.loader.ConfigSource)
    * [config](#edit_cfg_json.loader.ConfigSource.config)
    * [loader](#edit_cfg_json.loader.ConfigSource.loader)
    * [config\_type](#edit_cfg_json.loader.ConfigSource.config_type)
    * [made](#edit_cfg_json.loader.ConfigSource.made)
* [edit\_cfg\_json.buffer](#edit_cfg_json.buffer)
  * [NOT\_EDITABLE\_ERROR](#edit_cfg_json.buffer.NOT_EDITABLE_ERROR)
  * [NOT\_A\_CONTAINER](#edit_cfg_json.buffer.NOT_A_CONTAINER)
  * [EditBuffer](#edit_cfg_json.buffer.EditBuffer)
    * [\_\_init\_\_](#edit_cfg_json.buffer.EditBuffer.__init__)
    * [report](#edit_cfg_json.buffer.EditBuffer.report)
    * [rows](#edit_cfg_json.buffer.EditBuffer.rows)
    * [dirty](#edit_cfg_json.buffer.EditBuffer.dirty)
    * [anything\_open](#edit_cfg_json.buffer.EditBuffer.anything_open)
    * [values](#edit_cfg_json.buffer.EditBuffer.values)
    * [set\_text](#edit_cfg_json.buffer.EditBuffer.set_text)
    * [check\_field](#edit_cfg_json.buffer.EditBuffer.check_field)
    * [check\_all](#edit_cfg_json.buffer.EditBuffer.check_all)
    * [toggle\_fold](#edit_cfg_json.buffer.EditBuffer.toggle_fold)
    * [toggle\_fold\_all](#edit_cfg_json.buffer.EditBuffer.toggle_fold_all)
    * [keep\_saved](#edit_cfg_json.buffer.EditBuffer.keep_saved)
    * [take\_validated](#edit_cfg_json.buffer.EditBuffer.take_validated)
* [edit\_cfg\_json.settings](#edit_cfg_json.settings)
  * [DUPLICATE\_KEY](#edit_cfg_json.settings.DUPLICATE_KEY)
  * [NOT\_AN\_EXTENSION](#edit_cfg_json.settings.NOT_AN_EXTENSION)
  * [WRONG\_EXTENSION](#edit_cfg_json.settings.WRONG_EXTENSION)
  * [RESERVED\_KEYS](#edit_cfg_json.settings.RESERVED_KEYS)
  * [ActionSettings](#edit_cfg_json.settings.ActionSettings)
    * [quit](#edit_cfg_json.settings.ActionSettings.quit)
    * [validate](#edit_cfg_json.settings.ActionSettings.validate)
    * [save](#edit_cfg_json.settings.ActionSettings.save)
    * [save\_as](#edit_cfg_json.settings.ActionSettings.save_as)
    * [cancel](#edit_cfg_json.settings.ActionSettings.cancel)
    * [explain](#edit_cfg_json.settings.ActionSettings.explain)
    * [fold](#edit_cfg_json.settings.ActionSettings.fold)
  * [Settings](#edit_cfg_json.settings.Settings)
    * [actions](#edit_cfg_json.settings.Settings.actions)
    * [file\_extension](#edit_cfg_json.settings.Settings.file_extension)
    * [extension\_enforced](#edit_cfg_json.settings.Settings.extension_enforced)
  * [current\_settings](#edit_cfg_json.settings.current_settings)
  * [CheckedFile](#edit_cfg_json.settings.CheckedFile)
    * [name](#edit_cfg_json.settings.CheckedFile.name)
    * [message](#edit_cfg_json.settings.CheckedFile.message)
  * [checked\_file](#edit_cfg_json.settings.checked_file)
  * [chosen\_file](#edit_cfg_json.settings.chosen_file)
* [edit\_cfg\_json.model\_text](#edit_cfg_json.model_text)
  * [FOLDED\_MARK](#edit_cfg_json.model_text.FOLDED_MARK)
  * [EDITED\_MARK](#edit_cfg_json.model_text.EDITED_MARK)
  * [VALIDATOR\_MARK](#edit_cfg_json.model_text.VALIDATOR_MARK)
  * [FILLED\_MARK](#edit_cfg_json.model_text.FILLED_MARK)
  * [LOAD\_FORM](#edit_cfg_json.model_text.LOAD_FORM)
  * [DIRTY\_MARK](#edit_cfg_json.model_text.DIRTY_MARK)
  * [VERDICT\_FORM](#edit_cfg_json.model_text.VERDICT_FORM)
  * [VALID\_STATE](#edit_cfg_json.model_text.VALID_STATE)
  * [INVALID\_STATE](#edit_cfg_json.model_text.INVALID_STATE)
  * [UNKNOWN\_STATE](#edit_cfg_json.model_text.UNKNOWN_STATE)
  * [REFUSED\_FORM](#edit_cfg_json.model_text.REFUSED_FORM)
  * [SAVE\_TO\_FORM](#edit_cfg_json.model_text.SAVE_TO_FORM)
  * [NO\_DESTINATION\_TEXT](#edit_cfg_json.model_text.NO_DESTINATION_TEXT)
  * [SUMMARY\_SEPARATOR](#edit_cfg_json.model_text.SUMMARY_SEPARATOR)
  * [DESCRIPTION\_INDENT](#edit_cfg_json.model_text.DESCRIPTION_INDENT)
  * [TREE\_INDENT](#edit_cfg_json.model_text.TREE_INDENT)
  * [LEAF\_FORM](#edit_cfg_json.model_text.LEAF_FORM)
  * [CONTAINER\_FORM](#edit_cfg_json.model_text.CONTAINER_FORM)
  * [row\_value\_text](#edit_cfg_json.model_text.row_value_text)
  * [row\_marks](#edit_cfg_json.model_text.row_marks)
  * [docstring\_text](#edit_cfg_json.model_text.docstring_text)
  * [row\_describes](#edit_cfg_json.model_text.row_describes)
  * [row\_description](#edit_cfg_json.model_text.row_description)
  * [row\_fold\_text](#edit_cfg_json.model_text.row_fold_text)
  * [can\_fold](#edit_cfg_json.model_text.can_fold)
  * [fold\_hides](#edit_cfg_json.model_text.fold_hides)
  * [row\_diagnostic](#edit_cfg_json.model_text.row_diagnostic)
  * [verdict\_text](#edit_cfg_json.model_text.verdict_text)
  * [load\_text](#edit_cfg_json.model_text.load_text)
  * [save\_text](#edit_cfg_json.model_text.save_text)
  * [model\_as\_text](#edit_cfg_json.model_text.model_as_text)
  * [model\_title](#edit_cfg_json.model_text.model_title)
* [edit\_cfg\_json.emphasis](#edit_cfg_json.emphasis)
  * [Emphasis](#edit_cfg_json.emphasis.Emphasis)
    * [MUTED](#edit_cfg_json.emphasis.Emphasis.MUTED)
    * [ATTENTION](#edit_cfg_json.emphasis.Emphasis.ATTENTION)
    * [WARNING](#edit_cfg_json.emphasis.Emphasis.WARNING)
    * [GOOD](#edit_cfg_json.emphasis.Emphasis.GOOD)
    * [BAD](#edit_cfg_json.emphasis.Emphasis.BAD)
  * [EXPLANATION](#edit_cfg_json.emphasis.EXPLANATION)
  * [MEMBER\_MARK](#edit_cfg_json.emphasis.MEMBER_MARK)
  * [MEMBER\_DIAGNOSTIC](#edit_cfg_json.emphasis.MEMBER_DIAGNOSTIC)
  * [LOAD\_REMARK](#edit_cfg_json.emphasis.LOAD_REMARK)
  * [verdict\_emphasis](#edit_cfg_json.emphasis.verdict_emphasis)
  * [save\_emphasis](#edit_cfg_json.emphasis.save_emphasis)
* [edit\_cfg\_json.edit\_model](#edit_cfg_json.edit_model)
  * [EditModel](#edit_cfg_json.edit_model.EditModel)
    * [\_\_init\_\_](#edit_cfg_json.edit_model.EditModel.__init__)
    * [config\_type\_name](#edit_cfg_json.edit_model.EditModel.config_type_name)
    * [summary](#edit_cfg_json.edit_model.EditModel.summary)
    * [docstring](#edit_cfg_json.edit_model.EditModel.docstring)
    * [explanations\_shown](#edit_cfg_json.edit_model.EditModel.explanations_shown)
    * [toggle\_explanations](#edit_cfg_json.edit_model.EditModel.toggle_explanations)
    * [toggle\_fold](#edit_cfg_json.edit_model.EditModel.toggle_fold)
    * [toggle\_fold\_all](#edit_cfg_json.edit_model.EditModel.toggle_fold_all)
    * [settings](#edit_cfg_json.edit_model.EditModel.settings)
    * [load\_message](#edit_cfg_json.edit_model.EditModel.load_message)
    * [rows](#edit_cfg_json.edit_model.EditModel.rows)
    * [dirty](#edit_cfg_json.edit_model.EditModel.dirty)
    * [out\_file](#edit_cfg_json.edit_model.EditModel.out_file)
    * [save\_outcome](#edit_cfg_json.edit_model.EditModel.save_outcome)
    * [save\_message](#edit_cfg_json.edit_model.EditModel.save_message)
    * [saved\_config](#edit_cfg_json.edit_model.EditModel.saved_config)
    * [verdict](#edit_cfg_json.edit_model.EditModel.verdict)
    * [set\_text](#edit_cfg_json.edit_model.EditModel.set_text)
    * [check\_field](#edit_cfg_json.edit_model.EditModel.check_field)
    * [set\_out\_file](#edit_cfg_json.edit_model.EditModel.set_out_file)
    * [validate](#edit_cfg_json.edit_model.EditModel.validate)
    * [save](#edit_cfg_json.edit_model.EditModel.save)
* [edit\_cfg\_json.rows](#edit_cfg_json.rows)
  * [NOT\_A\_MEMBER](#edit_cfg_json.rows.NOT_A_MEMBER)
  * [MemberRow](#edit_cfg_json.rows.MemberRow)
    * [path](#edit_cfg_json.rows.MemberRow.path)
    * [value](#edit_cfg_json.rows.MemberRow.value)
    * [original](#edit_cfg_json.rows.MemberRow.original)
    * [children](#edit_cfg_json.rows.MemberRow.children)
    * [config\_type](#edit_cfg_json.rows.MemberRow.config_type)
    * [folded](#edit_cfg_json.rows.MemberRow.folded)
    * [shown](#edit_cfg_json.rows.MemberRow.shown)
    * [changed\_by\_validator](#edit_cfg_json.rows.MemberRow.changed_by_validator)
    * [filled\_from\_default](#edit_cfg_json.rows.MemberRow.filled_from_default)
    * [load\_reason](#edit_cfg_json.rows.MemberRow.load_reason)
    * [description](#edit_cfg_json.rows.MemberRow.description)
    * [converter](#edit_cfg_json.rows.MemberRow.converter)
    * [conversion](#edit_cfg_json.rows.MemberRow.conversion)
    * [name](#edit_cfg_json.rows.MemberRow.name)
    * [depth](#edit_cfg_json.rows.MemberRow.depth)
    * [foldable](#edit_cfg_json.rows.MemberRow.foldable)
    * [editable](#edit_cfg_json.rows.MemberRow.editable)
    * [is\_text](#edit_cfg_json.rows.MemberRow.is_text)
    * [edited](#edit_cfg_json.rows.MemberRow.edited)
    * [value\_text](#edit_cfg_json.rows.MemberRow.value_text)
  * [RowContext](#edit_cfg_json.rows.RowContext)
    * [report](#edit_cfg_json.rows.RowContext.report)
    * [descriptions](#edit_cfg_json.rows.RowContext.descriptions)
    * [nodes](#edit_cfg_json.rows.RowContext.nodes)
    * [converters](#edit_cfg_json.rows.RowContext.converters)
    * [optional](#edit_cfg_json.rows.RowContext.optional)
  * [member\_values](#edit_cfg_json.rows.member_values)
  * [built\_rows](#edit_cfg_json.rows.built_rows)
  * [stamped](#edit_cfg_json.rows.stamped)
* [edit\_cfg\_json.constructing](#edit_cfg_json.constructing)
  * [STREAM\_NAME](#edit_cfg_json.constructing.STREAM_NAME)
  * [FILE\_NAME](#edit_cfg_json.constructing.FILE_NAME)
  * [JSON\_TEXT\_NAMES](#edit_cfg_json.constructing.JSON_TEXT_NAMES)
  * [built\_config](#edit_cfg_json.constructing.built_config)
  * [parsed\_config](#edit_cfg_json.constructing.parsed_config)
* [edit\_cfg\_json.descriptions](#edit_cfg_json.descriptions)
  * [CHOICES\_FORM](#edit_cfg_json.descriptions.CHOICES_FORM)
  * [OPTIONAL\_TEXT](#edit_cfg_json.descriptions.OPTIONAL_TEXT)
  * [path\_description](#edit_cfg_json.descriptions.path_description)
  * [class\_docstring](#edit_cfg_json.descriptions.class_docstring)
  * [class\_summary](#edit_cfg_json.descriptions.class_summary)
  * [enum\_text](#edit_cfg_json.descriptions.enum_text)
  * [optional\_members](#edit_cfg_json.descriptions.optional_members)
  * [optional\_paths](#edit_cfg_json.descriptions.optional_paths)
  * [MemberFacts](#edit_cfg_json.descriptions.MemberFacts)
    * [value](#edit_cfg_json.descriptions.MemberFacts.value)
    * [converter](#edit_cfg_json.descriptions.MemberFacts.converter)
    * [optional](#edit_cfg_json.descriptions.MemberFacts.optional)
    * [nested](#edit_cfg_json.descriptions.MemberFacts.nested)
  * [type\_text](#edit_cfg_json.descriptions.type_text)
  * [member\_description](#edit_cfg_json.descriptions.member_description)
* [edit\_cfg\_json.auto\_change](#edit_cfg_json.auto_change)
  * [HOOK\_DATA\_VERSION](#edit_cfg_json.auto_change.HOOK_DATA_VERSION)
  * [WRITE\_ERRORS](#edit_cfg_json.auto_change.WRITE_ERRORS)
  * [PARSE\_ERRORS](#edit_cfg_json.auto_change.PARSE_ERRORS)
  * [KEY\_METHOD](#edit_cfg_json.auto_change.KEY_METHOD)
  * [RECORDED](#edit_cfg_json.auto_change.RECORDED)
  * [NO\_MEMBER](#edit_cfg_json.auto_change.NO_MEMBER)
  * [REMOVING\_KINDS](#edit_cfg_json.auto_change.REMOVING_KINDS)
  * [FileChanges](#edit_cfg_json.auto_change.FileChanges)
    * [filled](#edit_cfg_json.auto_change.FileChanges.filled)
    * [dropped](#edit_cfg_json.auto_change.FileChanges.dropped)
    * [changed](#edit_cfg_json.auto_change.FileChanges.changed)
    * [reasons](#edit_cfg_json.auto_change.FileChanges.reasons)
    * [unplaced](#edit_cfg_json.auto_change.FileChanges.unplaced)
    * [detail](#edit_cfg_json.auto_change.FileChanges.detail)
    * [anything](#edit_cfg_json.auto_change.FileChanges.anything)
  * [file\_changes](#edit_cfg_json.auto_change.file_changes)
* [edit\_cfg\_json.validation](#edit_cfg_json.validation)
  * [BUFFER\_ERRORS](#edit_cfg_json.validation.BUFFER_ERRORS)
  * [NOTHING\_REFUSED](#edit_cfg_json.validation.NOTHING_REFUSED)
  * [ValidationVerdict](#edit_cfg_json.validation.ValidationVerdict)
    * [valid](#edit_cfg_json.validation.ValidationVerdict.valid)
    * [diagnostics](#edit_cfg_json.validation.ValidationVerdict.diagnostics)
    * [refused](#edit_cfg_json.validation.ValidationVerdict.refused)
  * [ValidationPass](#edit_cfg_json.validation.ValidationPass)
    * [verdict](#edit_cfg_json.validation.ValidationPass.verdict)
    * [members](#edit_cfg_json.validation.ValidationPass.members)
    * [candidate](#edit_cfg_json.validation.ValidationPass.candidate)
  * [Attribution](#edit_cfg_json.validation.Attribution)
    * [refused](#edit_cfg_json.validation.Attribution.refused)
    * [remaining](#edit_cfg_json.validation.Attribution.remaining)
  * [PLAN\_METHOD](#edit_cfg_json.validation.PLAN_METHOD)
  * [validate\_buffer](#edit_cfg_json.validation.validate_buffer)

<a id="edit_cfg_json.tree"></a>

# edit\_cfg\_json.tree

The shape of the JSON structure that one configuration owns.

A configuration member is not always a value. It may be a list or a dict, and
what is inside it may be a list or a dict again, so what the editor shows is a
tree and not a row per member. This module owns the two operations that make
that tree, and they are inverses of each other: taking the values of one
configuration apart into one entry per node, and putting the edit buffer back
together into the values of one configuration.

Every node is addressed by a `config_as_json.ConfigPath`, which is what
section 4.2 of `doc/design.md` asks for: a member inside a list or a dict needs
no second way of naming it, and the description mapping already names one that
way. A list element is addressed by its index written out, which is what makes
`('retry_delays', '0')` a path and lets `('retry_delays', '[')` describe every
element of it.

**A declared nested configuration object is a node of its own**, and it is
what segments the tree. It serializes as a dict and it is not one: it has a
class and a docstring of its own, its members are rows below it in the order
that class declares them, and everything below it belongs to that class rather
than to the one above. That last part is the whole of what ownership means
here: a parse converter and an optional member are the owning class's, exactly
as `serialize_converters()` is on the way out.

**Where those objects are is asked of the objects themselves.** A member
holding one nested object is the least interesting case. A real configuration
has a list of nested objects, each of which holds a dict of more of them, and
`ConfigNestingKind` says so: `LIST_ELEMENT` and `DICT_VALUE` declare that every
value *inside* a member is one. So the declarations are walked over the
configuration object, which answers with the absolute path of every nested
object there really is, and with the object at it. The member that holds them
stays an ordinary container that can be folded and says how much it holds.

Walking the objects rather than matching a selector is what makes ownership
answerable at all: `parse_converters()` and `_omit_none_from_json()` are
methods of an object, and the declaration says only which class was expected.
It also tells the truth about a factory that answered with a subclass, and an
`OPTIONAL_MEMBER` that holds nothing: such a member has a class and no object,
which is a different thing from a member that has both.

<a id="edit_cfg_json.tree.EVERY_ELEMENT"></a>

#### EVERY\_ELEMENT

The path step that means every list element or dictionary value here.

It is the step that `config_as_json` gives this meaning to, in the paths of its
write-side converters and of its child-owned subtrees, and it keeps it here: it
is what one description reaches every element of a list with, and what one
nesting declaration says every element of a list is a configuration object
with.

<a id="edit_cfg_json.tree.PATH_SEPARATOR"></a>

#### PATH\_SEPARATOR

What separates the steps of a path where a path is written as text.

A path is a tuple everywhere inside the editor. It becomes text where a person
has to read it or type it, which is the line that names the members a
validation pass refused and the command line of the example programs.

<a id="edit_cfg_json.tree.ELEMENTS_FORM"></a>

#### ELEMENTS\_FORM

What is said about a list, in place of the value a leaf shows.

<a id="edit_cfg_json.tree.ELEMENT_FORM"></a>

#### ELEMENT\_FORM

The same for the one list that holds a single element.

<a id="edit_cfg_json.tree.ENTRIES_FORM"></a>

#### ENTRIES\_FORM

What is said about a dict, in place of the value a leaf shows.

<a id="edit_cfg_json.tree.ENTRY_FORM"></a>

#### ENTRY\_FORM

The same for the one dict that holds a single entry.

<a id="edit_cfg_json.tree.NO_OBJECT_FORM"></a>

#### NO\_OBJECT\_FORM

What a declared nested member that holds no object says instead.

An `OPTIONAL_MEMBER` is what holds none, and a class that writes it as `null`
rather than leaving it out gives it a row. The row says which class would be
there and that there is nothing there, because both of those are worth knowing
and neither is a value: no text typed into a field becomes a configuration
object, so the row cannot be edited. Making one is adding, and belongs with
adding an element of a list.

<a id="edit_cfg_json.tree.OPEN_AT_MOST"></a>

#### OPEN\_AT\_MOST

How many rows a container may add before it starts folded.

A configuration is shown with everything the application put in it, for the
same reason the explanations start shown: what was written was written to be
read. A list of two hundred elements is the case where that stops being true,
because it fills the window before the user has seen the members below it.

It counts every row the container would add and not only its direct children,
because that is what fills the window: a list of three dicts of five entries
each is eighteen rows and not three.

<a id="edit_cfg_json.tree.path_text"></a>

#### path\_text

```python
def path_text(path: ConfigPath) -> str
```

Return one path as the text that a person reads and types.

**Arguments**:

- `path` - Path that addresses one node of the tree.
  

**Returns**:

  The steps of that path, separated by dots.

<a id="edit_cfg_json.tree.text_path"></a>

#### text\_path

```python
def text_path(text: str) -> ConfigPath
```

Return the path that one piece of text addresses.

This is the inverse of `path_text`, and it is why a dictionary key that
holds a dot cannot be addressed as text. Such a key is edited in the
editor like any other; it is only the writing of its path that this
cannot express.

**Arguments**:

- `text` - Path written with a dot between its steps.
  

**Returns**:

  The path that text stands for.

<a id="edit_cfg_json.tree.is_container"></a>

#### is\_container

```python
def is_container(value: JsonType) -> bool
```

Return whether one value holds other values rather than being one.

**Arguments**:

- `value` - One value in JSON space.
  

**Returns**:

  Whether that value is a list or a dict.

<a id="edit_cfg_json.tree.container_text"></a>

#### container\_text

```python
def container_text(value: JsonType) -> str
```

Return what one container says in the place where a value is shown.

How many values it holds and nothing else. What they are is on the rows
below it, and a container that showed them again would be showing the
same thing twice — once in a form that a narrow window cuts off.

**Arguments**:

- `value` - Value of a list or a dict node.
  

**Returns**:

  How much that container holds.

<a id="edit_cfg_json.tree.rows_below"></a>

#### rows\_below

```python
def rows_below(path: ConfigPath, paths: Iterable[ConfigPath]) -> int
```

Return how many rows one container would add if it were opened.

Everything below it and not only its direct children, because that is
what fills the window. It is counted from the rows there are and not from
the value, because a declared configuration object inside it is one row
however much it holds.

**Arguments**:

- `path` - Path of the container.
- `paths` - The path of every node of the configuration.
  

**Returns**:

  The number of rows below that node.

<a id="edit_cfg_json.tree.starts_folded"></a>

#### starts\_folded

```python
def starts_folded(path: ConfigPath, paths: Iterable[ConfigPath]) -> bool
```

Return whether one container is folded when the editor opens.

**Arguments**:

- `path` - Path of the container.
- `paths` - The path of every node of the configuration.
  

**Returns**:

  Whether opening it would add more rows than `OPEN_AT_MOST`.

<a id="edit_cfg_json.tree.child_values"></a>

#### child\_values

```python
def child_values(path: ConfigPath,
                 value: JsonType) -> list[tuple[ConfigPath, JsonType]]
```

Return the nodes that are directly inside one container.

**Arguments**:

- `path` - Path of the container.
- `value` - Value of the container.
  

**Returns**:

  The path and the value of each of its children, in the order the
  container holds them, and nothing at all for a value that holds none.

<a id="edit_cfg_json.tree.selects"></a>

#### selects

```python
def selects(selector: ConfigPath, path: ConfigPath) -> bool
```

Return whether one selector addresses one node.

A selector is a path whose steps are either the name of one step or
`EVERY_ELEMENT`, which stands for every element of a list and every value
of a dict at that point. It is what a description of the application is
written with and what a nesting declaration becomes.

**Arguments**:

- `selector` - Selector to apply.
- `path` - Path of the node it is applied to.
  

**Returns**:

  Whether that selector is about that node.

<a id="edit_cfg_json.tree.ConfigNode"></a>

## ConfigNode Objects

```python
class ConfigNode(NamedTuple)
```

One declared configuration object of the tree, wherever it is.

<a id="edit_cfg_json.tree.ConfigNode.config_type"></a>

#### config\_type

Class of the object, or the class the member would hold.

It is the class of the object itself wherever there is one, which is not
always the declared class: a `factory_function` may answer with a subclass,
and what the object really is is what its docstring and its converters
belong to. It is the declared class only where there is no object.

<a id="edit_cfg_json.tree.ConfigNode.config"></a>

#### config

The object itself, None for a member that holds none.

An `OPTIONAL_MEMBER` is what holds none. Everything the editor asks of a
node below this one is asked of this object, so a node that has none has
nothing below it either.

<a id="edit_cfg_json.tree.config_nodes"></a>

#### config\_nodes

```python
def config_nodes(config: Config) -> dict[ConfigPath, ConfigNode]
```

Return every configuration object of one tree, by its path.

The configuration itself is one of them, under the empty path, so that the
object owning any node is found the same way whether that node is a member
of the configuration or a member of something nested inside it.

**Arguments**:

- `config` - Configuration object being edited. It is not modified.
  

**Returns**:

  One entry per declared nested configuration object, and one for the
  configuration itself.

<a id="edit_cfg_json.tree.owner_path"></a>

#### owner\_path

```python
def owner_path(path: ConfigPath, nodes: Mapping[ConfigPath,
                                                ConfigNode]) -> ConfigPath
```

Return the path of the configuration object that owns one node.

**Arguments**:

- `path` - Path of the node to ask about.
- `nodes` - Every configuration object of the tree, by its path.
  

**Returns**:

  The path of the innermost object that this node is inside, which is
  the empty path for a node of the configuration itself.

<a id="edit_cfg_json.tree.ordered_names"></a>

#### ordered\_names

```python
def ordered_names(config: Config, members: Mapping[str,
                                                   JsonType]) -> list[str]
```

Return the serialized member names in the order they are declared.

The declaration order is the order in which the configuration class
assigns its members, which `vars()` preserves. That is the order the
application thinks about its configuration in, so it is the order the
editor shows. The JSON document cannot supply it, because
`config_as_json` writes its keys sorted.

A member that the class omits from JSON while its value is `None` is
not serialized and so gets no row. A serialized name that is not an
attribute of the object is appended instead of dropped, so that no
member can go missing whatever a validator or a converter did.

Only the members are ordered this way, and a nested configuration object
has members of its own that are ordered by its own class. What is inside a
list is in the order that list holds it, and what is inside a dict is in
the order the file has it, which is the sorted one: a dictionary key has no
declaration to be read from, and the order a save writes is the order that
is shown.

**Arguments**:

- `config` - Configuration object whose members are ordered. It is not
  modified.
- `members` - One JSON space value per serialized member of that object.
  

**Returns**:

  The names of those members, in the order they are shown.

<a id="edit_cfg_json.tree.flat_values"></a>

#### flat\_values

```python
def flat_values(
    members: Mapping[str, JsonType],
    nodes: Mapping[ConfigPath,
                   ConfigNode]) -> list[tuple[ConfigPath, JsonType]]
```

Return every node of one configuration, depth first, in row order.

**Arguments**:

- `members` - One JSON space value per serialized member.
- `nodes` - Every configuration object of the tree, by its path, including
  the configuration itself under the empty path.
  

**Returns**:

  The path and the value of every node, each of them before what is
  inside it.

<a id="edit_cfg_json.tree.under_dict"></a>

#### under\_dict

```python
def under_dict(path: ConfigPath, values: Mapping[ConfigPath,
                                                 JsonType]) -> bool
```

Return whether one node is a value of a dictionary.

A member of the configuration is one, because the configuration itself is
the outermost dictionary of the file, and so is a member of a nested
configuration object, which writes a dictionary of its own. An element of
a list is not. It is the question a parse converter is answered by, since
`config_as_json` applies one while it decodes an object and to nothing
else.

**Arguments**:

- `path` - Path of the node to ask about.
- `values` - The value of every node, by path.
  

**Returns**:

  Whether that node is the value of a dictionary key.

<a id="edit_cfg_json.tree.assembled"></a>

#### assembled

```python
def assembled(children: Sequence[tuple[str, JsonType]],
              as_list: bool) -> JsonType
```

Return the value of one container, built from its children.

**Arguments**:

- `children` - The last step and the current value of each child, in the
  order the container holds them.
- `as_list` - Whether the container is a list rather than a dict.
  

**Returns**:

  The value that the container holds now.

<a id="edit_cfg_json.loading"></a>

# edit\_cfg\_json.loading

Reading the configuration to edit from one input file.

The editor constructs the configuration object rather than receiving one that
is already loaded, because the policy for declared keys the file does not
contain is decided while it is read and cannot be asked afterwards.

How that construction happens is the one thing an application may have to say
for itself, and `loader` is where it says it. Reading a file is also the only
place the answer is needed: everything the editor does afterwards works on the
object this produced, by copying it.

Three things can be wrong with an input file, and `config_as_json` reports
two of them as the same `KeyError`. Which of those two it is follows from
retrying the load with the declared defaults filling in what the file lacks:
that rescues a file which is merely incomplete, and it still refuses a key
the configuration does not declare. So the two are told apart by what the
retry does and never by reading the text of a message.

A file whose values a validator refuses cannot be opened either. That is not
squeamishness: a member validator returns the value that is stored back into
the member, so a load that stopped part way through leaves it unknown which
values were already rewritten and which were not.

A load that succeeded still has something to say when it did not leave the
file as it found it, which happens whenever the class has rules for reading an
older format, and whenever parsing or validating normalized a value. What
changed is found in `auto_change`; the words the user reads for it are here,
beside the words for everything else that one load has to report.

<a id="edit_cfg_json.loading.DEFAULTS_ERRORS"></a>

#### DEFAULTS\_ERRORS

Every way in which constructing the declared defaults can fail.

A class that needs a constructor argument this library knows nothing about
raises `TypeError`, one that declares no public member raises
`AttributeError`, and defaults that a validator refuses raise a `ValueError`
subclass. `NotImplementedError` is deliberately not one of them, for the same
reason as in the validation of a buffer: it says the configuration class is
incomplete, which is a defect of the application that no file can put right.

<a id="edit_cfg_json.loading.NO_FILE"></a>

#### NO\_FILE

Message of the refusal of a file that is missing or unreadable.

<a id="edit_cfg_json.loading.NOT_TEXT"></a>

#### NOT\_TEXT

Message of the refusal of a file that is not text at all.

<a id="edit_cfg_json.loading.NOT_CONFIG"></a>

#### NOT\_CONFIG

Message of the refusal of a file the configuration class cannot read.

This covers text that is not JSON and JSON that cannot be turned into the
values of this configuration, which is what `ConfigBadJson` means. Which of
the two it was is in the diagnostics below the message.

<a id="edit_cfg_json.loading.UNKNOWN_KEY"></a>

#### UNKNOWN\_KEY

Message of the refusal of a file with a key that is not declared.

<a id="edit_cfg_json.loading.INCOMPLETE"></a>

#### INCOMPLETE

Message of the refusal of an incomplete file under a strict policy.

<a id="edit_cfg_json.loading.BAD_VALUES"></a>

#### BAD\_VALUES

Message of the refusal of a file whose values a validator refuses.

<a id="edit_cfg_json.loading.NO_DEFAULTS"></a>

#### NO\_DEFAULTS

Message of the refusal of a class the editor cannot construct.

<a id="edit_cfg_json.loading.FILLED_MESSAGE"></a>

#### FILLED\_MESSAGE

Message that says a load used the declared defaults of the class.

<a id="edit_cfg_json.loading.AUTO_CHANGED"></a>

#### AUTO\_CHANGED

Message that says the load itself changed the values of the file.

It is one message for all three of the ways that can happen, because the user
is being told one thing: the file on the disk and the values on the screen are
not the same, and it is the screen that a save writes.

<a id="edit_cfg_json.loading.DROPPED_FORM"></a>

#### DROPPED\_FORM

Form of the line that names the keys of the file that are not used.

None of them is a member of this configuration, so none of them has a row that
could be marked, and this line is the only place they can be reported.

<a id="edit_cfg_json.loading.SUPPLIED_FORM"></a>

#### SUPPLIED\_FORM

Form of the line naming what the rules for an older format supplied.

It names only what no member of this configuration received, because what a
member received is said at that member. Neither the file nor the declared
defaults gave these values: the configuration class did, because the file is
too old to hold them at all.

<a id="edit_cfg_json.loading.VALUED_FORM"></a>

#### VALUED\_FORM

Form naming one supplied value, where the record carries the value.

`config_as_json` records the value it inserted, except for one entry point that
an application calls itself and that is not given it. The path alone is named
there, which is less and is still true.

<a id="edit_cfg_json.loading.NORMALIZED_REASON"></a>

#### NORMALIZED\_REASON

What is said about a member that only the comparison found.

Parsing and validating are what change a value without any rule for an older
format being involved, and neither of them is recorded anywhere. So this says
that the value is not the one the file holds and does not say why, which is
the whole of what can be known about it.

<a id="edit_cfg_json.loading.REASON_FORMS"></a>

#### REASON\_FORMS

What is said about a member, by the kind of record that produced it.

The kinds that are not here are the ones that produce no member at all: a key
that was pruned, a path that was removed and old data that the application
handled itself leave nothing behind to say it of, and they are named among the
keys that saving leaves out instead. A kind that reaches a member without being
here is said in the one text there is for a member the load changed, which is
less than it deserves and is never wrong.

<a id="edit_cfg_json.loading.MORE_REASONS_FORM"></a>

#### MORE\_REASONS\_FORM

Form used where the load recorded more than one change about one member.

That happens where the record is about a value inside the member rather than
about the member itself, which a nested configuration object has. The first is
named because it is the first rule that ran, and the rest are counted rather
than listed, because a mark shares its line with the field it belongs to.

<a id="edit_cfg_json.loading.LoadPolicy"></a>

## LoadPolicy Objects

```python
class LoadPolicy(Enum)
```

Policy for declared keys that the input file does not contain.

<a id="edit_cfg_json.loading.LoadPolicy.STRICT"></a>

#### STRICT

Refuse a file that does not hold every declared key.

<a id="edit_cfg_json.loading.LoadPolicy.DEFAULTS"></a>

#### DEFAULTS

Fill in what the file leaves out from the declared defaults.

<a id="edit_cfg_json.loading.LoadPolicy.STRICT_THEN_DEFAULTS"></a>

#### STRICT\_THEN\_DEFAULTS

Load strictly, and on failure fill in and say that it was needed.

<a id="edit_cfg_json.loading.DEFAULT_POLICY"></a>

#### DEFAULT\_POLICY

Policy used when the application names none of them.

Loading strictly and retrying with the defaults is the default because
whether a partly specified file is acceptable is an application decision,
and the answer that suits most applications is to open the file and say that
it was incomplete.

<a id="edit_cfg_json.loading.LoadReport"></a>

## LoadReport Objects

```python
class LoadReport(NamedTuple)
```

What one load of an input file did beyond reading the values.

<a id="edit_cfg_json.loading.LoadReport.message"></a>

#### message

What the user has to be told about the load, empty when nothing.

A load that read a complete file and had nothing remarked about it says
nothing, so a backend that shows this shows nothing at all.

<a id="edit_cfg_json.loading.LoadReport.filled"></a>

#### filled

Names of the members the declared defaults supplied.

These are the members the input file did not hold. The model marks the
row of each of them, so the user can see which values are not the ones
the file asked for.

<a id="edit_cfg_json.loading.LoadReport.reasons"></a>

#### reasons

What the load did to each member it put a value into or altered.

Reading a file is not always only reading it: the rules a class declares
for an older format may have supplied a value or renamed a key into a
member, and parsing or validating may have normalized one. The model marks
the row of each of these, so that a value which is not the one in the file
can be seen to be one, and the text says which of those things happened
wherever the load recorded it. A member the declared defaults filled in is
not here but in `filled`, which says the same thing more precisely.

<a id="edit_cfg_json.loading.LoadedConfig"></a>

## LoadedConfig Objects

```python
class LoadedConfig(NamedTuple)
```

The configuration object to edit, and what its load did.

<a id="edit_cfg_json.loading.LoadedConfig.config"></a>

#### config

The object whose values are edited. Never the caller's own object,
unless there was no input file to read.

<a id="edit_cfg_json.loading.LoadedConfig.report"></a>

#### report

What the load did to the values beyond reading them.

<a id="edit_cfg_json.loading.ConfigLoadError"></a>

## ConfigLoadError Objects

```python
class ConfigLoadError(Exception)
```

Refusal to open one input file for editing.

<a id="edit_cfg_json.loading.ConfigLoadError.__init__"></a>

#### \_\_init\_\_

```python
def __init__(message: str, diagnostics: str = '') -> None
```

Say why the file cannot be opened, and what was said about it.

**Arguments**:

- `message` - What the editor has to tell the user about this file.
- `diagnostics` - What the configuration class itself said about it.

<a id="edit_cfg_json.loading.default_config"></a>

#### default\_config

```python
def default_config(config_type: type[Config]) -> Config
```

Return one configuration object holding the declared defaults.

This is the door for a caller that has a configuration class and needs
the object that `edit` and `EditModel` take. A program that is told which
class to edit is the case it exists for: the class is named on a command
line, and the editor wants an instance of it.

It is the same construction that reading an input file starts from, so a
class the editor cannot construct is refused here in the same words and
with the same diagnostics.

An application whose class needs a constructor argument this library knows
nothing about has a loader instead, and calls that with no JSON source.

**Arguments**:

- `config_type` - Class to construct with no JSON source, which leaves it
  holding only what it declares.
  

**Returns**:

  A configuration object holding the declared defaults of that class.
  

**Raises**:

- `ConfigLoadError` - The editor cannot construct this class.

<a id="edit_cfg_json.loading.load_config"></a>

#### load\_config

```python
def load_config(config: Config,
                in_file: Optional[PathOrStr] = None,
                policy: LoadPolicy = DEFAULT_POLICY,
                settings: SettingsSource = Settings(),
                loader: Optional[ConfigLoader] = None) -> LoadedConfig
```

Read the configuration to edit from one file, or use the defaults.

The caller's object is the source of the class and of the declared
defaults, and is not modified. Without an input file it is also the
object to edit, so that a caller has one code path for both cases.

What the load says is captured rather than printed, because an
application that runs the editor has a screen and not a terminal behind
it: what the load has to say belongs where the editor can show it, which
is the report or the refusal.

**Arguments**:

- `config` - Configuration object saying which class to load and what its
  declared defaults are. It is not modified.
- `in_file` - File to read, or None to edit the declared defaults. It is
  refused when the application enforces an extension that this
  name does not have; it is never completed with one, because it
  names a file that already exists and completing it would open a
  different file from the one that was asked for.
- `policy` - What to do about declared keys the file does not hold.
- `settings` - What the application around the editor has already
  decided, or a callable that answers with it. The default is an
  application with no opinion.
- `loader` - How this application constructs its configuration, or None
  for a class the editor can construct from the signature it
  declares. A loader is what a class needing a constructor argument
  this library knows nothing about is reached through, and it is
  also what may answer with a class of its own choosing: the class
  of the object it returns is then the class of the session.
  

**Returns**:

  The configuration object to edit, and what the load did to its
  values beyond reading them.
  

**Raises**:

- `ConfigLoadError` - The file cannot be opened for editing.

<a id="edit_cfg_json.backend"></a>

# edit\_cfg\_json.backend

The protocol that every user interface backend implements.

The one backend this package ships is here as well, because it is the one
that needs no user interface library: it prints the model and returns. That
makes it the backend of a program that judges a configuration file on a
machine with no display, and it is also the shortest thing there is to read
for anybody writing a backend of their own.

<a id="edit_cfg_json.backend.EditorBackend"></a>

## EditorBackend Objects

```python
class EditorBackend(Protocol)
```

Show one edit model to the user and return when the user is done.

The protocol is phrased against the model and not against the `edit`
convenience wrapper, so that an application that has built the model
itself can run a backend over it. A backend that implements this owns a
window and an event loop of its own and runs to completion, which is
what the one method below promises.

Mounting the editor inside a window that an application already owns is
therefore not this protocol. It cannot run to completion, because the
event loop that is running is the application's own, and Textual offers
no way to nest a second one at all. It is a separate, non-blocking entry
point of each backend package, additive to this one, and section 8.2 of
`doc/design.md` is where it is designed.

The outcome of the session is read from the model afterwards rather than
returned here, so that the protocol does not have to change when saving
is added, and so that both ways of showing the editor report what was
saved in the same place.

<a id="edit_cfg_json.backend.EditorBackend.run_editor"></a>

#### run\_editor

```python
def run_editor(model: EditModel) -> None
```

Run the user interface for one model until the user is done.

**Arguments**:

- `model` - Model to show. The backend reads and edits the model, and
  never touches the caller's configuration object.

<a id="edit_cfg_json.backend.DumpEditor"></a>

## DumpEditor Objects

```python
class DumpEditor()
```

A backend that prints the model instead of opening a window.

It satisfies `EditorBackend` and is not a special case beside a real
backend, which is worth noticing: the protocol asks for one method, so
anything with that method can be handed to `edit`. That is also how an
application writes a backend of its own.

It runs to completion in the sense the protocol asks for, and there is
simply nothing for the user to do while it runs: it prints once and
returns. So it is the backend of a program that says what a configuration
file amounts to rather than one that offers to change it, and whoever runs
such a program has no later moment at which to press Save. Saving is
therefore the caller's to ask for, before the model is handed over.

<a id="edit_cfg_json.backend.DumpEditor.run_editor"></a>

#### run\_editor

```python
def run_editor(model: EditModel) -> None
```

Validate the buffer and print the model as text.

Validating is what makes the printed model say what the application
itself would make of the values in it, which is the whole point of
printing them. A save that the caller already asked for has validated
them too, and says so on the line about saving.

**Arguments**:

- `model` - Model to print.

<a id="edit_cfg_json.editing"></a>

# edit\_cfg\_json.editing

One editing session, from the input file to what was saved.

This is the convenience wrapper and deliberately nothing more. Everything it
does an application can do for itself, in three statements, which is what an
application that already runs its own event loop has to do: read the file,
build the model, mount the backend.

<a id="edit_cfg_json.editing.edit"></a>

#### edit

```python
def edit(config: Config,
         backend: EditorBackend,
         *,
         descriptions: Optional[Descriptions] = None,
         in_file: Optional[PathOrStr] = None,
         loader: Optional[ConfigLoader] = None,
         out_file: Optional[PathOrStr] = None,
         policy: LoadPolicy = DEFAULT_POLICY,
         settings: SettingsSource = Settings(),
         stderr_file: TextIO = sys.stderr) -> Optional[Config]
```

Edit one configuration and return the object that was saved.

The backend is a parameter because the core never imports a user
interface library, so it cannot name one. Each backend package also has
an `edit` of its own that supplies itself, which is the shorter door for
an application that has already chosen its user interface.

Without an output file the input file is written, which is what an
editor is normally asked to do. With neither, there is nowhere to write
and the backend asks the user for a destination before it can save.

**Arguments**:

- `config` - Configuration object saying which class to edit and what its
  declared defaults are. It is never modified, which is why the
  saved object is handed back rather than expected to be found in
  this one.
- `backend` - User interface to run this session in.
- `descriptions` - What the application says about the members it
  declares, or None when it says nothing. A configuration explains
  itself as far as it can without this — the docstring of its class
  labels the object — and a member no description reaches is shown
  without one.
- `in_file` - File to read, or None to start from the declared defaults.
- `loader` - How this application constructs its configuration, or None for
  a class the editor can construct from the signature it declares.
  An application whose class needs a constructor argument this
  library knows nothing about says it here, and
  `edit_cfg_json.derived_loader` is the shortest way to say it.
- `out_file` - File to write, or None to write the input file. A name
  that has no extension gets the one the application uses for its
  configuration; the input file never does.
- `policy` - What to do about declared keys the input file does not hold.
- `settings` - What the application around the editor has already
  decided, or a callable that answers with it. The default is an
  application with no opinion, which is what this library had of
  its own before there were settings at all.
- `stderr_file` - Stream used for user-facing diagnostics.
  

**Returns**:

  The configuration object that was written, or None when the session
  ended without anything being saved.
  

**Raises**:

- `ConfigLoadError` - The input file cannot be opened for editing.

<a id="edit_cfg_json.saving"></a>

# edit\_cfg\_json.saving

Writing the edited values to the output file.

Saving is validating and then writing, and it is refused whenever the
validation is. An editor that wrote a file the application would then refuse
to read would have failed at the one thing it exists for.

Where the application said how it loads its own configuration, that is asked
once more before anything is written, with the very text the file would hold.
It is the one thing a validation pass cannot answer: the pass applies the
buffer to the class that is being edited, and a loader that chooses its class
by looking at the JSON may read the same text back as another class
altogether. A value that would do that has to be caught here, because after
the file is written it is the application that meets it.

The file name is whatever the application asked for. This library has no
opinion about the extension: some applications use `.cfg`, some use `.json`,
and others use something else again.

<a id="edit_cfg_json.saving.NO_DESTINATION"></a>

#### NO\_DESTINATION

Message of a save that has nowhere to write to.

<a id="edit_cfg_json.saving.NOT_VALID"></a>

#### NOT\_VALID

Message of a save refused because the buffer is not a configuration.

<a id="edit_cfg_json.saving.NOT_LOADABLE"></a>

#### NOT\_LOADABLE

Message of a save whose file the application's own loader refuses.

<a id="edit_cfg_json.saving.OTHER_CLASS"></a>

#### OTHER\_CLASS

Message of a save whose file the loader would read as another class.

Which class a configuration is was settled when the file was opened, and the
session has been about that class ever since: its members are the rows, and
its docstring is the label. A value that would select another class is
therefore not something the editor can follow, and writing the file anyway
would leave the application with one it may not be able to read at all.

<a id="edit_cfg_json.saving.RELOAD_ERRORS"></a>

#### RELOAD\_ERRORS

Every way the application's own loader can refuse what would be written.

They are the three ways `config_as_json` refuses anything, which is what a
loader built around it refuses with, and `ask_loader` turns a loader that ends
the process into the third of them. A refusal here is a file that is not
written, exactly like a refused validation, and never an exception the
application has to handle.

<a id="edit_cfg_json.saving.WRITE_FAILED"></a>

#### WRITE\_FAILED

Message of a save whose destination could not be written.

<a id="edit_cfg_json.saving.SAVED"></a>

#### SAVED

Message of a save that wrote the output file.

<a id="edit_cfg_json.saving.WRITE_ERRORS"></a>

#### WRITE\_ERRORS

Every way in which writing the output file can fail.

`OSError` is the file itself: a folder that does not exist, a name that
cannot be used, a file that may not be written to. The other three are how
`config_as_json` refuses a configuration, and `Config.write()` validates the
object again before it writes anything. The object written here has just been
validated, so those three can only mean a validator that does not give the
same answer twice. That is a defect of the application rather than of the
values, but the editor still reports it as a file it could not write, because
falling over would cost the user the whole session.

<a id="edit_cfg_json.saving.SaveOutcome"></a>

## SaveOutcome Objects

```python
class SaveOutcome(NamedTuple)
```

What one attempt to save the edited values did.

<a id="edit_cfg_json.saving.SaveOutcome.saved"></a>

#### saved

Whether the output file was written.

<a id="edit_cfg_json.saving.SaveOutcome.message"></a>

#### message

What the user has to be told about this attempt.

There is always something to say, because a save is something the user
asked for and an answer is the least it owes them.

<a id="edit_cfg_json.saving.SaveState"></a>

## SaveState Objects

```python
@dataclass
class SaveState()
```

Where the editor writes, and what has come of writing there.

The three belong together because each of them moves when the others do:
choosing a destination drops what an earlier attempt said, and an
attempt that wrote the file is the only thing there is a written object
to hand back from.

<a id="edit_cfg_json.saving.SaveState.out_file"></a>

#### out\_file

File that saving writes, None while no destination has been chosen.

There is none when the editor was started neither on an input file nor
on an output file, which is what happens when an application offers to
write its very first configuration file.

<a id="edit_cfg_json.saving.SaveState.outcome"></a>

#### outcome

What the last attempt to save did, None when there has been none.

<a id="edit_cfg_json.saving.SaveState.written"></a>

#### written

The configuration object that reached the file, None when none has.

It is never the caller's own object, which the editor does not modify
and which would otherwise be stale.

<a id="edit_cfg_json.saving.reload_refusal"></a>

#### reload\_refusal

```python
def reload_refusal(loader: Optional[ConfigLoader], config: Config) -> str
```

Return why the application would not read back what is to be written.

An application that said nothing about how it loads is not asked anything,
and neither is one whose loader reads back what the editor is showing: both
of those are the ordinary case, and both answer with nothing at all.

**Arguments**:

- `loader` - How this application constructs its configuration, or None
  when it did not say and there is nothing to ask.
- `config` - Validated configuration object that the save would write.
  

**Returns**:

  What to tell the user instead of saving, empty when nothing stands in
  the way of writing the file.

<a id="edit_cfg_json.saving.write_config"></a>

#### write\_config

```python
def write_config(config: Config, out_file: PathOrStr) -> SaveOutcome
```

Write one validated configuration object to one file.

`Config.write()` serializes before it opens the destination, and
serializing validates, so a configuration it refuses leaves the file on
disk exactly as it was. The editor validates first anyway, which makes
this the second of two gates rather than the only one.

What the write says about the configuration is captured rather than
printed, for the same reason as everywhere else here: these diagnostics
belong on the screen the editor owns and not in the terminal behind it.
They are the diagnostics of the validation pass that has just run, so the
verdict is already showing them and this copy is dropped.

**Arguments**:

- `config` - Configuration object to write. It has been validated.
- `out_file` - File to write it to, with whatever extension the
  application chose.
  

**Returns**:

  Whether the file was written, and what to tell the user about it.

<a id="edit_cfg_json.converting"></a>

# edit\_cfg\_json.converting

What the configuration makes of the text of one leaf of the buffer.

The buffer holds JSON space values, and some members do not hold a JSON space
value at all once the configuration class has them: `parse_converters()` says
which of them become a richer Python type and how. An enum is the case that
arises in practice, and it is what makes this worth having. A name that is no
member of an enum cannot be turned into one, and `config_as_json` reports that
inside the message it prints for JSON it could not load — which is right for a
program reading a file and wrong for a person editing a field, who was not
asking about JSON at all.

The converter that the class declared is *run* rather than looked at, exactly
as `config_as_json` runs it while it parses. That is the same rule that
validation follows and for the same reason: an application may declare any
converter it likes, and running the real one is right for every converter that
exists or ever will.

Which class declared it is a question of its own once there are nested
configuration objects, and `node_converters` is where it is answered: a nested
object parses its own JSON, so what is inside it is answered by its own class
and not by the class above it.

<a id="edit_cfg_json.converting.CONVERSION_ERRORS"></a>

#### CONVERSION\_ERRORS

Every way in which a parse converter can refuse one value.

`config_as_json` catches every exception around the parsing it does, so a
converter is not promised to fail in any particular way, and these are the
ways in which the converters it ships do fail: a name that is no member of an
enum raises `KeyError`, and a value that is not text at all trips the
assertion that the enum converter begins with.

`NotImplementedError` is deliberately not one of them, exactly as it is not
one of the failures a validation pass catches: it says that the configuration
class is incomplete, which is a defect of the application that no edit of the
buffer can put right.

<a id="edit_cfg_json.converting.Converted"></a>

## Converted Objects

```python
class Converted(NamedTuple)
```

One leaf value as the configuration class would hold it.

<a id="edit_cfg_json.converting.Converted.value"></a>

#### value

What the converter of that member made of the value, or the value.

It is the value itself for a member that has no converter, and also for
one whose converter refused it, so that there is always something to go
on. The type is genuinely unknown here: a converter may return anything.

<a id="edit_cfg_json.converting.Converted.message"></a>

#### message

Why the converter refused the value, empty when nothing refused it.

<a id="edit_cfg_json.converting.member_converters"></a>

#### member\_converters

```python
def member_converters(config: Config) -> dict[str, ParseConverter]
```

Return the parse converters of the members that one class declares.

A class that declares none inherits a placeholder converter under a key of
the base class's own, so the answer is restricted to the members the
object really has. A converter named after something that is no member of
the configuration could never be applied to anything in any case.

**Arguments**:

- `config` - Configuration object to ask. It is not modified.
  

**Returns**:

  One converter per member that has one.

<a id="edit_cfg_json.converting.node_converters"></a>

#### node\_converters

```python
def node_converters(
    nodes: Mapping[ConfigPath, ConfigNode], flat: Sequence[tuple[ConfigPath,
                                                                 JsonType]]
) -> dict[ConfigPath, ParseConverter]
```

Return the parse converter of every node of one tree that has one.

Two things decide it, and each of them is a rule of `config_as_json`
rather than of this editor. A converter is applied while an object is
decoded, so it reaches the value of a dictionary key at any depth and
never an element of a list. And a converter belongs to the class that owns
the subtree, exactly as a write-side converter does: a nested
configuration object parses its own JSON and applies its own converters,
so the converters of the class above it are not the ones that answer for
what is inside it.

**Arguments**:

- `nodes` - Every configuration object of the tree, by its path.
- `flat` - The path and the value of every node, in row order.
  

**Returns**:

  One converter per node that has one, by the path of that node.

<a id="edit_cfg_json.converting.convert_member"></a>

#### convert\_member

```python
def convert_member(converter: Optional[ParseConverter],
                   value: JsonType) -> Converted
```

Return one leaf value as its member holds it, or why it cannot.

A value that already has the type the converter produces is left alone,
and so is a value that is `None`: a member that its class leaves out of
JSON while it is None has nothing to convert, and a `None` that is wrong
is refused by the validation of the whole configuration, which has a
message of its own for it.

**Arguments**:

- `converter` - How the text of this member becomes a value, or None for a
  member that holds what the file holds.
- `value` - JSON space value that the buffer holds for that member.
  

**Returns**:

  The value the configuration would hold, or the reason it would not.

<a id="edit_cfg_json.converting.refusal_text"></a>

#### refusal\_text

```python
def refusal_text(error: Exception) -> str
```

Return what one refusal says, as the user should read it.

A `KeyError` writes the representation of its argument rather than the
argument itself, so the message about a name that is no member of an enum
would otherwise arrive wrapped in quotation marks that nobody wrote.

**Arguments**:

- `error` - The failure that was reported.
  

**Returns**:

  What that failure says.

<a id="edit_cfg_json.cli"></a>

# edit\_cfg\_json.cli

The command line of a program that edits any configuration class.

An application author should get an editor for their own configuration class
without writing a line of user interface code, and every one of the three
distributions therefore ships a program. What differs between the three
programs is the backend and nothing else, so everything else lives here: the
parsing, the two doors to a class, the construction, one editing session and
the exit code. Each package is then a program of a few statements, which is
also what makes this testable with no display and no toolkit, by handing
`run_cli` a backend that is a stub.

`run_cli` takes the backend for exactly the reason `edit` does: this package
never imports a user interface library, so it cannot name one.

**The class is told and never guessed.** `--module` names an importable module,
`--file` names a Python file that is not, and exactly one of the two is
required. A single `module:Class` argument reads well and would have to guess
which of the two it was given, which is what section 8.2.1 of `doc/design.md`
settled for this library as a whole; it would also make a Windows drive letter
a special case, and it would take the refusal of a missing or a doubled
location away from `argparse`.

**What to edit is either a class or a loader**, and `--class` and `--loader`
name them in the same module or file. At least one of the two is needed and
both are allowed: a class alone is constructed on the values it declares, a
loader alone is asked for a configuration and its class is whatever it answers
with, and the two together mean that the loader has to answer with that class
or the program stops. `--loader` is for a class the editor cannot construct on
its own, so whatever it needs beyond the five keyword arguments of
`edit_cfg_json.ConfigLoader` has to be bound in the module it is named in — a
command line cannot supply an argument this library knows nothing about.

**What the application says about its own members is told the same way.**
`--descriptions NAME` names a `Descriptions` mapping beside the class, because
that is the one thing an application can tell the editor that this program
could not otherwise pass on: a member has no docstring at runtime, so what a
member is for is either in such a mapping or nowhere. The class docstring needs
no option, because the class already carries it.

**Importing a module runs it.** That is the same exposure as running the file
with Python, and it is not guarded against, because a guard could only be a
pretence: a configuration class is Python and reaching it means importing the
module it is in.

<a id="edit_cfg_json.cli.DESCRIPTION"></a>

#### DESCRIPTION

What the program says about itself above its own options.

<a id="edit_cfg_json.cli.PYTHON_SUFFIX"></a>

#### PYTHON\_SUFFIX

File name extension of the files that the `--file` door accepts.

<a id="edit_cfg_json.cli.POLICY_NAMES"></a>

#### POLICY\_NAMES

What a `--policy` value on a command line means to the editor.

<a id="edit_cfg_json.cli.NO_MODULE_MESSAGE"></a>

#### NO\_MODULE\_MESSAGE

Message of the refusal of a `--module` that names no importable module.

<a id="edit_cfg_json.cli.NO_FILE_MESSAGE"></a>

#### NO\_FILE\_MESSAGE

Message of the refusal of a `--file` that names no readable file.

<a id="edit_cfg_json.cli.NOT_PYTHON_MESSAGE"></a>

#### NOT\_PYTHON\_MESSAGE

Message of the refusal of a `--file` that Python cannot compile.

It covers both a name that is not a `.py` file at all and a `.py` file that
does not compile, because both mean the same thing to whoever ran the program:
what was named is not a Python module.

<a id="edit_cfg_json.cli.NOT_IMPORTABLE_MESSAGE"></a>

#### NOT\_IMPORTABLE\_MESSAGE

Message of the refusal of a file that only its own package can import.

A module that uses a relative import is the case that arises in practice, and
there is nothing a bare path can do about it: the import needs the package
that the module belongs to, and a path names no package.

<a id="edit_cfg_json.cli.NO_NAME_MESSAGE"></a>

#### NO\_NAME\_MESSAGE

Message of the refusal of a class name that the module does not hold.

<a id="edit_cfg_json.cli.NOT_CONFIG_MESSAGE"></a>

#### NOT\_CONFIG\_MESSAGE

Message of the refusal of a name that is not a configuration class.

<a id="edit_cfg_json.cli.NO_TARGET_MESSAGE"></a>

#### NO\_TARGET\_MESSAGE

Message of the refusal of a command line that says what to edit nowhere.

`argparse` cannot be asked for at least one of two options, only for exactly
one of them, and either alone is a perfectly good command line here.

<a id="edit_cfg_json.cli.NOT_LOADER_MESSAGE"></a>

#### NOT\_LOADER\_MESSAGE

Message of the refusal of a `--loader` that names something else.

<a id="edit_cfg_json.cli.LOADER_ARGS_MESSAGE"></a>

#### LOADER\_ARGS\_MESSAGE

Message of the refusal of a loader whose own arguments are not bound.

<a id="edit_cfg_json.cli.NO_LOADER_CONFIG"></a>

#### NO\_LOADER\_CONFIG

Message of the refusal of a loader that refused to answer at all.

The editor asks a loader for a configuration with no JSON source, which is what
`edit_cfg_json.ConfigLoader` says a loader answers. A loader that chooses its
class by looking at the JSON has to name the class it uses for a configuration
that does not exist yet, and this is the refusal of one that names none.

<a id="edit_cfg_json.cli.WRONG_CLASS_MESSAGE"></a>

#### WRONG\_CLASS\_MESSAGE

Message of the refusal of a loader that answered with another class.

A loader may choose its class by looking at the JSON, and `--class` beside it
is how a script says which class it is prepared to go on with. The check is
what `isinstance` answers, so a loader that answers with a subclass of the
class that was named is accepted.

<a id="edit_cfg_json.cli.NOT_DESCRIPTIONS"></a>

#### NOT\_DESCRIPTIONS

Message of the refusal of a `--descriptions` that names something else.

What the keys and the values of the mapping are is not checked, for the reason
section 4.3 of `doc/design.md` gives: a selector that addresses no member of
this configuration is simply never used, and a wrong description is a cosmetic
mistake that is not worth refusing to open an editor over.

<a id="edit_cfg_json.cli.NOT_SHOWABLE_MESSAGE"></a>

#### NOT\_SHOWABLE\_MESSAGE

Message of the refusal of a class that cannot be turned into a buffer.

The editor reads the values it edits by serializing the configuration object,
so a class that cannot serialize itself has no values to show. A class that
leaves part of its own writing to code outside itself is the case that arises
in practice, and there is nothing the editor can do with one.

<a id="edit_cfg_json.cli.ExitCode"></a>

## ExitCode Objects

```python
class ExitCode(IntEnum)
```

What one run of a program of this library says about how it went.

A program of this library is meant to be usable from a script and from a
continuous integration job, so each way of refusing has a number of its
own rather than sharing one. The numbers are part of what the programs
promise, so an added way of refusing gets an added number and no existing
one changes.

<a id="edit_cfg_json.cli.ExitCode.OK"></a>

#### OK

Everything the program was asked to do was done.

<a id="edit_cfg_json.cli.ExitCode.LOAD_REFUSED"></a>

#### LOAD\_REFUSED

The input file cannot be opened for editing.

<a id="edit_cfg_json.cli.ExitCode.USAGE"></a>

#### USAGE

The command line itself is wrong.

It is `argparse` that reports this and ends the process, so `run_cli`
never returns it. The number is written down here because it is part of
the same promise as the rest, and because the tests compare against it.

<a id="edit_cfg_json.cli.ExitCode.NO_MODULE"></a>

#### NO\_MODULE

The module that `--module` names cannot be imported.

<a id="edit_cfg_json.cli.ExitCode.NO_FILE"></a>

#### NO\_FILE

The file that `--file` names cannot be read.

<a id="edit_cfg_json.cli.ExitCode.NOT_PYTHON"></a>

#### NOT\_PYTHON

The file that `--file` names is not Python that can be imported.

<a id="edit_cfg_json.cli.ExitCode.NOT_IMPORTABLE"></a>

#### NOT\_IMPORTABLE

The file needs the package it belongs to in order to be imported.

<a id="edit_cfg_json.cli.ExitCode.NO_NAME"></a>

#### NO\_NAME

The module does not hold the name that was asked for.

<a id="edit_cfg_json.cli.ExitCode.NOT_CONFIG"></a>

#### NOT\_CONFIG

That name is not a class based on `config_as_json.Config`.

<a id="edit_cfg_json.cli.ExitCode.NO_DEFAULTS"></a>

#### NO\_DEFAULTS

The editor cannot construct that configuration class on its own.

<a id="edit_cfg_json.cli.ExitCode.INVALID"></a>

#### INVALID

The configuration is not one that the application would accept.

This is what makes a program with no user interface a check that a script
or a continuous integration job can run: a file the application would
refuse is a failure of the run and not merely a remark in the output.

<a id="edit_cfg_json.cli.ExitCode.NOT_WRITTEN"></a>

#### NOT\_WRITTEN

The output file was asked for and was not written.

The values were valid, so what stopped the writing is the destination: a
name that was not given at all, one the application does not use for its
configuration, or a file that cannot be written.

<a id="edit_cfg_json.cli.ExitCode.NOT_SHOWABLE"></a>

#### NOT\_SHOWABLE

The values of that configuration class cannot be written as JSON.

There is then nothing to edit at all: the editor reads what it shows by
serializing the configuration object.

<a id="edit_cfg_json.cli.ExitCode.NOT_LOADER"></a>

#### NOT\_LOADER

The name that `--loader` names cannot be called at all.

<a id="edit_cfg_json.cli.ExitCode.LOADER_ARGS"></a>

#### LOADER\_ARGS

The loader needs arguments that a command line cannot supply.

A loader takes the five keyword arguments of `ConfigLoader` and nothing
else, so whatever it needs besides them is bound where it is written. A
program cannot bind an argument it knows nothing about, and saying so
plainly is better than a half answer.

<a id="edit_cfg_json.cli.ExitCode.WRONG_CLASS"></a>

#### WRONG\_CLASS

The loader did not construct the class that `--class` asked for.

<a id="edit_cfg_json.cli.ExitCode.NOT_DESCRIPTIONS"></a>

#### NOT\_DESCRIPTIONS

The name that `--descriptions` names is no mapping of any kind.

<a id="edit_cfg_json.cli.named_policy"></a>

#### named\_policy

```python
def named_policy(name: str) -> LoadPolicy
```

Return the load policy that one `--policy` value asks for.

**Arguments**:

- `name` - One of the values that `add_file_options` accepts.
  

**Returns**:

  What the editor makes of that value.
  

**Raises**:

- `KeyError` - The name is not one of the accepted values. It cannot come
  from a command line, because `argparse` refuses it first.

<a id="edit_cfg_json.cli.add_file_options"></a>

#### add\_file\_options

```python
def add_file_options(parser: ArgumentParser) -> None
```

Add the file and policy options that every program of this library has.

The three of them say the same thing wherever they appear — which file to
read, which to write, and what to do about a value the file leaves out —
so they are declared here once rather than per program. The examples of
this repository use this as well, which is what keeps the one meaning
from becoming two.

**Arguments**:

- `parser` - Parser that the options are added to.

<a id="edit_cfg_json.cli.run_cli"></a>

#### run\_cli

```python
def run_cli(backend: EditorBackend,
            prog: str,
            *,
            args: Optional[Sequence[str]] = None,
            interactive: bool = True) -> int
```

Run one program of this library from the command line.

This is the whole of what each of the three programs does. The backend is
the only thing that differs between them, and everything that could be
written twice is therefore here.

**Arguments**:

- `backend` - User interface to run the session in. Each package supplies
  its own, which is the one thing this package cannot name.
- `prog` - Name that this program is installed under, used in its help and
  in its refusals.
- `args` - Optional replacement for `sys.argv[1:]`, mainly for tests.
- `interactive` - Whether this backend gives the user a session. A backend
  that prints once and returns does not, so its program offers
  `--save` and answers with the verdict in its exit code, because
  there is nobody to press Save and nobody to read a verdict.
  

**Returns**:

  What this run of the program ends with, as one of `ExitCode`.
  

**Raises**:

- `SystemExit` - The command line itself is wrong, or help was asked for.
  That is `argparse` reporting it, with `ExitCode.USAGE`. A command
  line that names neither a class nor a loader is one of those, and
  it is checked here because `argparse` can be asked for exactly one
  of two options and not for at least one of them.

<a id="edit_cfg_json.leaf_value"></a>

# edit\_cfg\_json.leaf\_value

The JSON space meaning of one leaf value of the edit buffer.

<a id="edit_cfg_json.leaf_value.TEXT_KIND"></a>

#### TEXT\_KIND

What is said about a member that holds text.

<a id="edit_cfg_json.leaf_value.WHOLE_NUMBER_KIND"></a>

#### WHOLE\_NUMBER\_KIND

What is said about a member that holds an integer.

<a id="edit_cfg_json.leaf_value.NUMBER_KIND"></a>

#### NUMBER\_KIND

What is said about a member that holds a floating point number.

<a id="edit_cfg_json.leaf_value.BOOL_KIND"></a>

#### BOOL\_KIND

What is said about a member that holds a boolean.

<a id="edit_cfg_json.leaf_value.VALUE_KINDS"></a>

#### VALUE\_KINDS

What each kind of leaf value is called, in the order they are asked.

The order is what makes `True` say what it is: `bool` is a subclass of `int` in
Python, so a value that is asked in the other order would be a whole number.
Nothing else here depends on the order.

<a id="edit_cfg_json.leaf_value.NO_KIND"></a>

#### NO\_KIND

What is said about a member that holds nothing at all.

The kind of a member is the kind of the value it held when the file was last
agreed with, which is the only type information there is (section 4.2 of
`doc/design.md`), and a member that held nothing gave none.

<a id="edit_cfg_json.leaf_value.value_as_text"></a>

#### value\_as\_text

```python
def value_as_text(value: JsonType) -> str
```

Return the text that an edit field shows for one value.

A string is shown as the string itself. The quotation marks that JSON
puts around a string belong to the file format and not to the value, so
showing them would make the user believe that the text really begins and
ends with a quotation mark. Every other value is shown as its JSON
notation, which is also how the user would type it.

**Arguments**:

- `value` - One leaf value of the edit buffer, in JSON space.
  

**Returns**:

  The text of that value.

<a id="edit_cfg_json.leaf_value.text_as_value"></a>

#### text\_as\_value

```python
def text_as_value(text: str, is_text_member: bool) -> JsonType
```

Return the value that the text of one edit field stands for.

A member that holds text keeps exactly what the user typed, so that a
text member can hold the digits of a number without becoming a number.
Every other member has its text read as JSON, which is the inverse of
how `value_as_text` writes it.

Text that is not JSON at all is kept as a string rather than refused. A
value being typed passes through states that are not valid, and a field
that refused them could not be typed in at all. The string that a number
member then holds is not hidden: it is the wrong type, and validation
reports it as the wrong type.

**Arguments**:

- `text` - Text that the edit field holds.
- `is_text_member` - Whether this member holds text.
  

**Returns**:

  The JSON space value that the text stands for.

<a id="edit_cfg_json.leaf_value.values_differ"></a>

#### values\_differ

```python
def values_differ(value: JsonType, other: JsonType) -> bool
```

Return whether two values would be written to the file differently.

The comparison is made on the JSON notation and not with `==`, because
Python considers `True` equal to `1` and `1` equal to `1.0`, while a
JSON file shows all three of them differently. Changing a member from
`1` to `1.0` changes the file, so it is a change that the user made and
the editor has to say so.

**Arguments**:

- `value` - One value in JSON space.
- `other` - The value to compare it with.
  

**Returns**:

  Whether the two values are different values.

<a id="edit_cfg_json.leaf_value.value_kind"></a>

#### value\_kind

```python
def value_kind(value: JsonType) -> str
```

Return what kind of value one member holds, as a line to read.

It is what the editor knows about a member without being told anything by
the application: what the value is, which is what tells the digits of a
number from a text that happens to be digits. A list and a dict answer with
nothing, because a member the editor cannot edit yet already says which of
the two it is where its value would be.

**Arguments**:

- `value` - One leaf value of the edit buffer, in JSON space.
  

**Returns**:

  What kind of value that is, and an empty text for a value whose kind
  is already said elsewhere.

<a id="edit_cfg_json.loader"></a>

# edit\_cfg\_json.loader

How the application says that its configuration is constructed.

Most applications say nothing: their configuration class takes the keyword
arguments that `config_as_json` documents, and the editor constructs it from
the signature it reads. An application whose class needs an argument this
library knows nothing about — a folder, a connection, the list of names its own
validators accept — has to say so, and a loader is how it says it.

**The signature of a loader is closed.** The editor passes the four things it
owns, all of them keyword arguments, and everything else is bound before the
callable reaches the editor, with a closure or `functools.partial`. That is
what keeps this protocol from growing a parameter for every application that
has one: what the editor does not know about is not the editor's to pass.

What a loader is not asked for is the hook that records what reading an old
format file changed. `Config` gives every configuration object one of its own,
and `Config.auto_change_hook` is where the editor reads it, so a loader that
was never told about it reports exactly as much as one that was.

**A loader answers a call with no JSON source**, with the configuration that
class uses when there is no file yet. The editor asks for that when it is
started on the declared values rather than on a file, so a loader that chooses
its class by looking at the JSON has to name the class it uses for a
configuration that does not exist yet.

**The class is chosen when the file is loaded.** A loader that returns
different classes for different files is supported, and this is the rule that
makes it work: the model is built on the object the load produced, and the
session then edits that class. Nothing asks the loader again while the user
types, because the rows, the descriptions and the marks are that one class's.
What a save does ask is whether the file it is about to write would still be
read as the class being edited, which is where a value that selects another
class is caught.

<a id="edit_cfg_json.loader.NO_FILE_NAME"></a>

#### NO\_FILE\_NAME

Message of the refusal of a file name given to a derived loader.

<a id="edit_cfg_json.loader.LOADER_EXITED"></a>

#### LOADER\_EXITED

Message of a loader that raised `SystemExit` rather than an exception.

Ending the process is never the right answer inside an editor: it costs the
user the whole session. `config_as_json` does it in more than one place, so a
loader written around one of those does it too, and `ask_loader` is where it
becomes a refusal like any other.

<a id="edit_cfg_json.loader.ConfigLoader"></a>

## ConfigLoader Objects

```python
@runtime_checkable
class ConfigLoader(Protocol)
```

Construct the application's configuration object for the editor.

This is `config_as_json.ConfigFactory` plus the one parameter it lacks, so
a factory an application already has is nearly one of these. The one that
is added is the thing a load has to be told and a construction does not:
whether the declared defaults may fill in what the file leaves out.

It is checkable at runtime because a program of this library is told the
name of one on a command line, and a name that turns out to be something
else has to be refused rather than called. What that check can see is that
the object can be called at all; whether it takes these four keyword
arguments is answered by calling it.

<a id="edit_cfg_json.loader.ConfigLoader.__call__"></a>

#### \_\_call\_\_

```python
def __call__(*,
             from_json_data_text: Optional[str] = None,
             from_json_filename: Optional[PathOrStr] = None,
             ok_to_use_defaults: bool = False,
             stderr_file: TextIO = sys.stderr) -> Config
```

Construct one configuration object from the given JSON source.

**Arguments**:

- `from_json_data_text` - JSON text to apply, or None for the values
  that the configuration class declares.
- `from_json_filename` - File to read. The editor reads its own input
  files and never passes this, and it is here so that a callable
  written for `config_as_json` fits without being rewritten.
- `ok_to_use_defaults` - Whether the declared defaults may fill in the
  members that the JSON text does not hold.
- `stderr_file` - Stream used for user-facing diagnostics.
  

**Returns**:

  One configuration object holding the values of that source.

<a id="edit_cfg_json.loader.derived_loader"></a>

#### derived\_loader

```python
def derived_loader(factory: Callable[..., Config]) -> ConfigLoader
```

Return a loader that constructs one configuration with one callable.

This is what the editor does for a class it is given no loader for, offered
to an application that needs the same thing with an argument of its own
bound into it:


The callable is asked for a configuration holding its declared values, and
the JSON text is then applied with `Config.parse_json`. Constructing and
parsing are two steps because the load policy belongs to the second of
them: `Config.__init__` takes no `ok_to_use_defaults` at all.

A loader written by hand is the door for anything this cannot express, and
a class chosen by looking at the JSON is what that means in practice.

````python
loader = derived_loader(partial(TeamConfig, KNOWN_TEAMS))
````

**Arguments**:

- `factory` - Class to construct, or a callable that constructs it with
  arguments of its own already bound.
  

**Returns**:

  A loader for that callable, which satisfies `ConfigLoader`.

<a id="edit_cfg_json.loader.ask_loader"></a>

#### ask\_loader

```python
def ask_loader(loader: ConfigLoader,
               *,
               stream: TextIO,
               text: Optional[str] = None,
               ok_to_use_defaults: bool = False) -> Config
```

Ask one loader for one configuration object of this application.

Every call the editor makes to a loader goes through here, so that a loader
that ends the process is turned into a refusal in one place rather than in
four. It becomes a `ValueError`, which is what every caller already reports
as values the configuration class would not accept.

**Arguments**:

- `loader` - How this application constructs its configuration.
- `stream` - Stream that collects what the loader says.
- `text` - JSON text to apply, or None for the declared values.
- `ok_to_use_defaults` - Whether the declared defaults may fill in what the
  text does not hold.
  

**Returns**:

  The configuration object that the loader made.
  

**Raises**:

- `ValueError` - The loader ended the program, or refused the values.
- `KeyError` - The keys of the text do not match the declared members.
- `TypeError` - The loader cannot construct the configuration this way.
- `AttributeError` - The class declares no public member at all.

<a id="edit_cfg_json.loader.ConfigSource"></a>

## ConfigSource Objects

```python
class ConfigSource(NamedTuple)
```

The configuration of one session, and how it is constructed.

The two belong together because each of them answers what the other cannot.
The object says which class is being edited and is what an edit buffer is
applied to; the loader is how a further object of that class is made, which
only reading a file needs and only an application can say.

<a id="edit_cfg_json.loader.ConfigSource.config"></a>

#### config

An object of the class being edited, which is never modified.

<a id="edit_cfg_json.loader.ConfigSource.loader"></a>

#### loader

How the application constructs it, None when it did not say.

None does not mean that nothing can be constructed: it means the class is
constructed from the signature it declares, which is what almost every
class allows. It is kept apart from a loader that was given, because a save
checks what it is about to write against a loader the application named and
has nothing to check it against otherwise.

<a id="edit_cfg_json.loader.ConfigSource.config_type"></a>

#### config\_type

```python
@property
def config_type() -> type[Config]
```

Return the class of the configuration that is being edited.

<a id="edit_cfg_json.loader.ConfigSource.made"></a>

#### made

```python
def made(*,
         stream: TextIO,
         text: Optional[str] = None,
         ok_to_use_defaults: bool = False) -> Config
```

Return one configuration object of this session's class.

**Arguments**:

- `stream` - Stream that collects what the construction says.
- `text` - JSON text to apply, or None for the declared values.
- `ok_to_use_defaults` - Whether the declared defaults may fill in what
  the text does not hold.
  

**Returns**:

  The configuration object that was constructed.
  

**Raises**:

- `ValueError` - The values are ones the configuration refuses.
- `KeyError` - The keys of the text do not match the declared members.
- `TypeError` - The configuration cannot be constructed this way.
- `AttributeError` - The class declares no public member at all.

<a id="edit_cfg_json.buffer"></a>

# edit\_cfg\_json.buffer

The rows of one configuration, and what the user has done to them.

This is the edit buffer of the model: the values as the user is editing them,
one row per node, and which of the containers are folded away. It is separate
from `EditModel` because the model is a session — where it came from, what the
application decided, what a validation pass found, where a save would go — and
this is the one thing in that session which the user changes by typing.

Nothing here does any input or output, and nothing here knows what a backend
is. What a backend reads is the rows, and what it does is set the text of one
of them and fold one of them away.

<a id="edit_cfg_json.buffer.NOT_EDITABLE_ERROR"></a>

#### NOT\_EDITABLE\_ERROR

Message of the error raised when a node is not a value.

A list, a dict and a nested configuration object are all structure rather than
a value, and each of them is edited through the rows below it. A declared
member that holds no configuration object is refused as well, because no text
becomes one.

<a id="edit_cfg_json.buffer.NOT_A_CONTAINER"></a>

#### NOT\_A\_CONTAINER

Message of the error raised when a node that holds none is folded.

<a id="edit_cfg_json.buffer.EditBuffer"></a>

## EditBuffer Objects

```python
class EditBuffer()
```

The values of one configuration as the user is editing them.

Leaf values are held in JSON space, so that an enum member is held as its
name and a value being typed does not have to be a valid Python value
yet. JSON space is about the kind of the value, not about its notation:
a string member holds the string, and the quotes that the file format
puts around it are added when the file is written and nowhere else.

A member that holds a list, a dict or a nested configuration object is a
tree of rows rather than one row, because what is inside one of those is
edited a value at a time. Every one of them holds what its own rows hold,
which is kept true as they are edited, so a folded node cannot hide a
change.

<a id="edit_cfg_json.buffer.EditBuffer.__init__"></a>

#### \_\_init\_\_

```python
def __init__(config: Config, report: LoadReport, descriptions: Descriptions,
             stderr_file: TextIO) -> None
```

Read the JSON space values of one configuration object.

**Arguments**:

- `config` - Configuration object to read. It is not modified, because
  what is read is the text it writes and not the object.
- `report` - What reading the input file did beyond reading the values.
- `descriptions` - What the application says about its members.
- `stderr_file` - Stream used for user-facing diagnostics.
  

**Raises**:

- `InvalidConfiguration` - The configuration object is not valid.
- `InvalidConfigurationValue` - A member of the configuration object
  does not hold a valid value.

<a id="edit_cfg_json.buffer.EditBuffer.report"></a>

#### report

```python
@property
def report() -> LoadReport
```

Return what reading the input file did beyond reading values.

<a id="edit_cfg_json.buffer.EditBuffer.rows"></a>

#### rows

```python
@property
def rows() -> Sequence[MemberRow]
```

Return one row per node of the configuration, in the order shown.

Every row is here whether it is folded away or not, because a backend
creates its widgets once and hides the ones that are not shown.

<a id="edit_cfg_json.buffer.EditBuffer.dirty"></a>

#### dirty

```python
@property
def dirty() -> bool
```

Return whether the buffer holds anything that is worth saving.

<a id="edit_cfg_json.buffer.EditBuffer.anything_open"></a>

#### anything\_open

```python
@property
def anything_open() -> bool
```

Return whether at least one container is open.

<a id="edit_cfg_json.buffer.EditBuffer.values"></a>

#### values

```python
def values() -> dict[str, JsonType]
```

Return the buffer as one JSON space value per member.

A member that holds a list or a dict holds what its own rows hold,
because every edit of a value inside one is written up into it.

**Returns**:

  One value per member of the configuration.

<a id="edit_cfg_json.buffer.EditBuffer.set_text"></a>

#### set\_text

```python
def set_text(path: ConfigPath, text: str) -> bool
```

Set one node of the buffer from the text of an edit field.

Text that the node already shows changes nothing, because it is not
an edit. That is not only tidiness: a field posts a change when it is
given its initial text, and a buffer that counted that as an edit
would report unsaved changes before the user had touched anything.
It is also what lets a backend write the buffer back into its fields
after a validation pass without that counting as an edit.

Every container the node is inside is brought up to date with it, so
that what the whole configuration holds is always what its rows say.

**Arguments**:

- `path` - Path of the node to set.
- `text` - Text that the edit field holds.
  

**Returns**:

  Whether that was an edit, which is what the rest of the session
- `asks` - a verdict and a save that were reached from this buffer
  still stand while nothing in it has changed.
  

**Raises**:

- `KeyError` - The path is not a node of this configuration.
- `ValueError` - The node is not one that this version can edit.

<a id="edit_cfg_json.buffer.EditBuffer.check_field"></a>

#### check\_field

```python
def check_field(path: ConfigPath) -> None
```

Report whether the text of one node means a value of it at all.

**Arguments**:

- `path` - Path of the node to check.
  

**Raises**:

- `KeyError` - The path is not a node of this configuration.

<a id="edit_cfg_json.buffer.EditBuffer.check_all"></a>

#### check\_all

```python
def check_all() -> None
```

Report every node whose text means no value of that node.

<a id="edit_cfg_json.buffer.EditBuffer.toggle_fold"></a>

#### toggle\_fold

```python
def toggle_fold(path: ConfigPath) -> None
```

Fold one container away, or open it again.

**Arguments**:

- `path` - Path of the container to fold or open.
  

**Raises**:

- `KeyError` - The path is not a node of this configuration.
- `ValueError` - The node is not a container.

<a id="edit_cfg_json.buffer.EditBuffer.toggle_fold_all"></a>

#### toggle\_fold\_all

```python
def toggle_fold_all() -> None
```

Fold every container away, or open every one of them.

One action and not two, because a user who wants the values back
wants all of them back: which of the two it does is decided by what
is on the screen, so a press always changes something.

<a id="edit_cfg_json.buffer.EditBuffer.keep_saved"></a>

#### keep\_saved

```python
def keep_saved() -> None
```

Make what was written the values that the buffer is compared to.

The mark of a node a validator rewrote is deliberately left alone.
That a value is not literally the one the user typed stays true after
it has been saved, and it is the mark that says so.

<a id="edit_cfg_json.buffer.EditBuffer.take_validated"></a>

#### take\_validated

```python
def take_validated(config: Config, members: Mapping[str, JsonType]) -> None
```

Rebuild the buffer from the configuration object that was built.

The rows are built again rather than patched, because a validator
that normalizes a list changes how many rows there are: the paths
after such a pass are not the paths before it. What every row that
is still there knew is carried over, so the rebuild is a refresh.

**Arguments**:

- `config` - Configuration object that the pass accepted, which is
  what says in which order the members are shown and which of
  the nodes are configuration objects of their own. It is the
  object these values were read from, so it is what answers for
  them. It is not modified.
- `members` - One JSON space value per member of the accepted object.

<a id="edit_cfg_json.settings"></a>

# edit\_cfg\_json.settings

What the application around the editor has already decided.

The editor does not run on its own. It runs inside an application that made
decisions before the editor was ever called: which key combinations its own
user interface has taken, and what a configuration file of that application
is called. This module is how the application says so, and it is what the
editor consults instead of deciding those things for itself.

Every attribute has a default, so an application with no opinion passes
nothing at all and gets what the editor would have chosen anyway.

<a id="edit_cfg_json.settings.DUPLICATE_KEY"></a>

#### DUPLICATE\_KEY

Message of the refusal of one key combination given to two actions.

<a id="edit_cfg_json.settings.NOT_AN_EXTENSION"></a>

#### NOT\_AN\_EXTENSION

Message of the refusal of an extension setting that names none.

<a id="edit_cfg_json.settings.WRONG_EXTENSION"></a>

#### WRONG\_EXTENSION

Message of the refusal of a file name an enforced extension forbids.

<a id="edit_cfg_json.settings.RESERVED_KEYS"></a>

#### RESERVED\_KEYS

Key combinations that no default of this editor takes, for later use.

Finding a member of a configuration that does not fit a window is something
this editor is likely to be asked for, and `ctrl+f` opens a search everywhere
while `f3` finds the next one. An action added later is an added attribute of
`ActionSettings` and breaks no application, but a *key* that moved would break
every user who had learnt it, so the two are kept free from the start rather
than taken back afterwards.

Nothing here refuses these keys to an application: which combinations its own
user interface has already taken is the application's to say, and section 9 of
`doc/design.md` is about the editor not overruling that. What this refuses is
the editor's own defaults taking them, which is what the test of this module
checks.

<a id="edit_cfg_json.settings.ActionSettings"></a>

## ActionSettings Objects

```python
@dataclass(frozen=True)
class ActionSettings()
```

The key combinations of every action of the editor.

One attribute per action, so that an action the application says nothing
about keeps the default of its own attribute and there is no merge rule
to explain, and so that a misspelled action name is refused where the
mistake was made rather than becoming a setting nobody reads.

Each attribute holds every combination that runs its action. The first
of them is the one a footer or a menu names, and the rest work without
being named, because naming one action twice would suggest that they
were two actions. An empty tuple takes the key away and not the action:
a button and a command palette entry reach it whatever the keys say.

Combinations are written the way Textual names keys, in lower case: the
modifiers `ctrl`, `shift`, `alt` and `meta` joined with `+`, and then a
single character, `f1` to `f12`, or a name such as `escape`, `enter`,
`tab`, `space`, `backspace`, `delete`, `insert`, `home`, `end`,
`pageup`, `pagedown`, `up`, `down`, `left` or `right`. The Tk backend
translates them into the notation of its own toolkit, and leaves an
action it cannot translate without that key rather than without a
button.

<a id="edit_cfg_json.settings.ActionSettings.quit"></a>

#### quit

Keys that end the editor.

Quitting writes nothing of its own. It is the "cancel" of this design;
saving leaves the editor open, and what has been saved has been saved.

A single unmodified letter cannot be used for this or for any other
action here, now that the value of a member is edited in a field: an
unmodified letter belongs to whichever field has the focus, and a user
who typed it would expect to see it appear.

<a id="edit_cfg_json.settings.ActionSettings.validate"></a>

#### validate

Keys that ask the application what it makes of these values.

`ctrl+r` because a field claims most of the other control letters:
Textual's `Input` already reads `ctrl+a`, `ctrl+c`, `ctrl+d`, `ctrl+e`,
`ctrl+k`, `ctrl+u`, `ctrl+v`, `ctrl+w` and `ctrl+x`, and the terminal
itself claims `ctrl+c` and the four that are Backspace, Tab, Return and
Escape. Of what is left, `r` is the one that means something: re-check.

`f5` because a function key is what other editors use to ask a tool to
check what has been written. It is the second of the two, so it works
without being named, which is what it deserves: a function key is the
one of the two that a keyboard or a terminal is most likely not to
deliver.

<a id="edit_cfg_json.settings.ActionSettings.save"></a>

#### save

Keys that write the output file.

The key every application uses for this, and it does reach a terminal
application: Textual's driver clears `IXON` and `IXOFF` when it puts the
terminal into raw mode, so neither `ctrl+s` nor `ctrl+q` is taken for
flow control any more.

<a id="edit_cfg_json.settings.ActionSettings.save_as"></a>

#### save\_as

Keys that choose an output file and then write it.

The key every application uses for this as well, but unlike the one
above it is not delivered everywhere. A legacy terminal encodes a
control letter as a single byte with nowhere to put the shift, so this
combination arrives as the save key and the wrong action runs. That is
why the action is offered without a key as well.

`f12` because a function key is what other editors use to ask a tool to
write the output file. It is the second of the two, so it works without
being named, which is what it deserves: a function key is the one of the
two that a keyboard or a terminal is most likely not to deliver.

<a id="edit_cfg_json.settings.ActionSettings.cancel"></a>

#### cancel

Keys that leave a question of the editor unanswered.

The question about the output file is the only one so far. The Tk
backend binds nothing for this, because the only question it asks is the
toolkit's own file dialog, which answers this key itself.

<a id="edit_cfg_json.settings.ActionSettings.explain"></a>

#### explain

Keys that show or hide what the application says about the values.

`f1` because a function key is what asks for help everywhere else, and
because it is free: of the keys an editor would want, a field claims most
of the control letters and the application itself claims the rest.

`ctrl+g` because a terminal or a keyboard that does not deliver a function
key would otherwise leave this action to the button and the command
palette. It is one of the few control letters that Textual's own field
does not read for itself.

<a id="edit_cfg_json.settings.ActionSettings.fold"></a>

#### fold

Keys that fold every list and dict away, or open every one of them.

One action for all of them and not one per container: a container is
folded and opened where it is, with a control on its own row, and what a
key is worth is getting the whole configuration back at once.

`f2` because it is the function key beside the one that explains, and the
two actions are the same kind of thing: both of them decide how much of
the configuration is on the screen.

`ctrl+t` for the same reason `explain` has a control letter as well, which
is a terminal or a keyboard that does not deliver a function key, and `t`
because the tree is what this action is about. It is deliberately not
`ctrl+f`: that is find everywhere, and this editor is likely to want one.
See `RESERVED_KEYS`.

An application whose configuration has no list and no dict in it is never
offered this action at all, because there would be nothing for it to do.

<a id="edit_cfg_json.settings.Settings"></a>

## Settings Objects

```python
@dataclass(frozen=True)
class Settings()
```

What the application around the editor has already decided.

Both this class and `ActionSettings` are frozen: the editor is given
what an application decided and has no business changing it.

<a id="edit_cfg_json.settings.Settings.actions"></a>

#### actions

The key combinations of every action of the editor.

<a id="edit_cfg_json.settings.Settings.file_extension"></a>

#### file\_extension

What a configuration file of this application is called, or None.

None is no opinion, and it is the default: some applications use `.cfg`,
some use `.json`, and others use something else again. A value is
normalized to begin with a dot, so `cfg` and `.cfg` mean the same thing.

<a id="edit_cfg_json.settings.Settings.extension_enforced"></a>

#### extension\_enforced

Whether a file name with another extension is refused.

It says nothing at all while `file_extension` is None, because there is
then no extension to enforce.

<a id="edit_cfg_json.settings.current_settings"></a>

#### current\_settings

```python
def current_settings(source: SettingsSource) -> Settings
```

Return the settings of the application as they are now.

**Arguments**:

- `source` - The settings, or a callable that answers with them.
  

**Returns**:

  The settings to use for what is about to be done.

<a id="edit_cfg_json.settings.CheckedFile"></a>

## CheckedFile Objects

```python
class CheckedFile(NamedTuple)
```

One file name as the settings of the application leave it.

<a id="edit_cfg_json.settings.CheckedFile.name"></a>

#### name

The file to use, which is the given name unless an extension was
added to it.

<a id="edit_cfg_json.settings.CheckedFile.message"></a>

#### message

Why this file cannot be used, empty when it can be.

<a id="edit_cfg_json.settings.checked_file"></a>

#### checked\_file

```python
def checked_file(name: PathOrStr, settings: Settings) -> CheckedFile
```

Return one file name, or say why this application cannot use it.

The name is never changed here. An extension that is a default says
nothing about a name that already exists, and an extension that is
enforced can only refuse one: opening or overwriting a different file
because two names differ by an extension would be a surprise, and a
surprise about which file was written is the expensive kind.

**Arguments**:

- `name` - File the editor was asked to read or to write.
- `settings` - What the application has decided about file names.
  

**Returns**:

  That name, and why it cannot be used when it cannot.

<a id="edit_cfg_json.settings.chosen_file"></a>

#### chosen\_file

```python
def chosen_file(name: PathOrStr, settings: Settings) -> CheckedFile
```

Return one newly chosen destination, with the extension it needs.

A name that has no extension at all gets the one the application uses,
because a destination that is being chosen does not name a file that
exists yet and completing it is a service rather than a substitution.
Everything else is what `checked_file` makes of it.

This is for a destination the user or the application chooses while the
editor runs. A destination that was inherited, which is the input file
when the caller named no output file, is only checked and never
completed.

**Arguments**:

- `name` - File the user or the application has just chosen to write.
- `settings` - What the application has decided about file names.
  

**Returns**:

  The name to write, and why it cannot be used when it cannot.

<a id="edit_cfg_json.model_text"></a>

# edit\_cfg\_json.model\_text

Plain text rendering of an edit model and of its individual values.

<a id="edit_cfg_json.model_text.FOLDED_MARK"></a>

#### FOLDED\_MARK

What follows a container whose rows are hidden.

The two backends say this with a control that the user presses instead, which
is the wording each of them owns. This rendering has nowhere to put a control,
so it says it in words: a container that is folded is showing less than it
holds, and a reader who is not told that would read the values as all of them.

<a id="edit_cfg_json.model_text.EDITED_MARK"></a>

#### EDITED\_MARK

Mark that follows the value of a member the user has changed.

<a id="edit_cfg_json.model_text.VALIDATOR_MARK"></a>

#### VALIDATOR\_MARK

Mark that follows the value of a member a validation pass rewrote.

<a id="edit_cfg_json.model_text.FILLED_MARK"></a>

#### FILLED\_MARK

Mark that follows the value of a member the input file did not hold.

<a id="edit_cfg_json.model_text.LOAD_FORM"></a>

#### LOAD\_FORM

Form of the mark that follows a value reading the input file put there.

A file in an older format is what puts one there in practice: a key of it was
renamed into this member, or the rules for that format supplied the value. A
value that parsing or validating normalized is marked with this too. What is
in it is what the model says the load did to that member, which is the words
of the record where the load recorded one.

<a id="edit_cfg_json.model_text.DIRTY_MARK"></a>

#### DIRTY\_MARK

Mark that follows the model label while the buffer has changes.

<a id="edit_cfg_json.model_text.VERDICT_FORM"></a>

#### VERDICT\_FORM

Form of the line that reports what the last validation pass found.

<a id="edit_cfg_json.model_text.VALID_STATE"></a>

#### VALID\_STATE

State of a buffer that the application itself would accept.

<a id="edit_cfg_json.model_text.INVALID_STATE"></a>

#### INVALID\_STATE

State of a buffer that the application itself would refuse.

<a id="edit_cfg_json.model_text.UNKNOWN_STATE"></a>

#### UNKNOWN\_STATE

State of a buffer that has not been validated since it last changed.

<a id="edit_cfg_json.model_text.REFUSED_FORM"></a>

#### REFUSED\_FORM

Form of the line that names the nodes the application refused.

They are named here as well as marked below, because a configuration of any
size does not fit a window: a user who has just asked what the application
makes of these values should be told where to look rather than have to go
looking. A value inside a list or a dict is named by its whole path, because
its own name says nothing about where it is.

<a id="edit_cfg_json.model_text.SAVE_TO_FORM"></a>

#### SAVE\_TO\_FORM

Form of the line that says where saving would write.

<a id="edit_cfg_json.model_text.NO_DESTINATION_TEXT"></a>

#### NO\_DESTINATION\_TEXT

Line shown while no output file has been chosen.

<a id="edit_cfg_json.model_text.SUMMARY_SEPARATOR"></a>

#### SUMMARY\_SEPARATOR

What separates the label of the configuration from its summary.

They share one line while the explanations are hidden, because the summary is
one line for the whole configuration and hiding it would save nothing.

<a id="edit_cfg_json.model_text.DESCRIPTION_INDENT"></a>

#### DESCRIPTION\_INDENT

What is written below a node is indented by this much.

The indentation is what says that the line belongs to the node above it
rather than being a node of its own. Every line of it gets one, because
what the type of a node says about it runs to more than one line.

<a id="edit_cfg_json.model_text.TREE_INDENT"></a>

#### TREE\_INDENT

What each step further inside a list or a dict is indented by.

It is the same width as the indentation of the explanatory text, so that a
value inside a container and a sentence about the container line up. They are
told apart by their shape rather than by their place: a row has a name and a
value, and a sentence has neither.

<a id="edit_cfg_json.model_text.LEAF_FORM"></a>

#### LEAF\_FORM

Form of the line that shows one value of the configuration.

<a id="edit_cfg_json.model_text.CONTAINER_FORM"></a>

#### CONTAINER\_FORM

Form of the line that shows one node that is not edited in a field.

A colon and not an equals sign, because what follows is not the value: for a
list, a dict or a nested configuration object the value is on the rows below,
and this says how many of them there are or which class they belong to.

<a id="edit_cfg_json.model_text.row_value_text"></a>

#### row\_value\_text

```python
def row_value_text(row: MemberRow) -> str
```

Return the value of one node as the text a field would show.

A nested configuration object says its class, a list or a dict says how
much it holds because its value is on the rows below it, and a declared
member holding no object says which class is missing. Every other node
shows the text of the value it holds.

Both backends read it from here, so that neither of them decides on its
own what a node that is not a value looks like.

**Arguments**:

- `row` - Node to render.
  

**Returns**:

  The value text of one node.

<a id="edit_cfg_json.model_text.row_marks"></a>

#### row\_marks

```python
def row_marks(row: MemberRow) -> str
```

Return the marks that follow the value of one member.

They say different things that can all be true at once: the input file did
not hold this member, reading the file changed what it holds, the user
changed it, and a validator then changed what the user had written. They
are in the order in which they can happen. The two that a load sets are
never both there, because the more precise of the two is the one it sets.

Both backends read the marks from here, so that neither of them decides on
its own what a member the load, the user or a validator touched looks like.

**Arguments**:

- `row` - Member to mark.
  

**Returns**:

  The marks of one member, empty when nothing has happened to it.

<a id="edit_cfg_json.model_text.docstring_text"></a>

#### docstring\_text

```python
def docstring_text(model: EditModel) -> str
```

Return what the configuration class says about itself, as it is shown.

The summary while the explanations are hidden and the whole docstring
while they are shown, which is what the toggle of the model is for: the
summary is one line for the whole configuration and is worth keeping,
and the rest of the docstring is what a user who knows this
configuration wants out of the way.

Both backends show this, so that neither of them decides on its own how
much of a docstring the user is offered.

**Arguments**:

- `model` - Model whose configuration class is reported.
  

**Returns**:

  The text to show for the configuration object, and nothing at all
  when its class has no docstring of its own.

<a id="edit_cfg_json.model_text.row_describes"></a>

#### row\_describes

```python
def row_describes(row: MemberRow) -> bool
```

Return whether anything can ever be said below one node.

A backend asks this before it creates the widget that says it, because a
widget which could never hold anything is a line of the window spent on
nothing. It is asked of the core rather than worked out by each backend,
since what is said below a node is the core's to decide: the description
the row carries is not the whole of it once a nested configuration object
has a class docstring of its own.

**Arguments**:

- `row` - Node to ask about.
  

**Returns**:

  Whether the application, the type of the node or the class of the
  object at it has anything to say.

<a id="edit_cfg_json.model_text.row_description"></a>

#### row\_description

```python
def row_description(model: EditModel, row: MemberRow) -> str
```

Return what is said about one node, as it is shown.

It is what the application said about the node and what the type of the
node says, while the explanations are shown, and nothing while they are
hidden. Which of the two it is belongs to the model, so that the two
backends cannot hide different things.

A nested configuration object says what its own class says as well, and
how much of that is said depends on whether the node is open. That is why
it is put together here rather than carried by the row: what a row says
about itself cannot depend on the fold state that is stamped onto it
afterwards.

**Arguments**:

- `model` - Model that the node belongs to.
- `row` - Node to describe.
  

**Returns**:

  What is said below that node, empty while it is not being shown or
  when there is nothing to say about it.

<a id="edit_cfg_json.model_text.row_fold_text"></a>

#### row\_fold\_text

```python
def row_fold_text(row: MemberRow) -> str
```

Return what says that one container is folded, empty when it is not.

**Arguments**:

- `row` - Node to render.
  

**Returns**:

  The mark of a folded container, and nothing for every other node.

<a id="edit_cfg_json.model_text.can_fold"></a>

#### can\_fold

```python
def can_fold(model: EditModel) -> bool
```

Return whether anything in this configuration can be folded.

A configuration of scalar members alone has nothing to fold, and a
backend asks this before it offers the action at all: an editor that
showed a control which could never do anything would be offering
something that is not there.

**Arguments**:

- `model` - Model to ask about.
  

**Returns**:

  Whether the configuration holds a list or a dict.

<a id="edit_cfg_json.model_text.fold_hides"></a>

#### fold\_hides

```python
def fold_hides(model: EditModel) -> bool
```

Return whether folding everything would hide anything.

It is what the one action that folds everything does next, so a backend
that names its actions after what the next press does reads the name
from here. The action folds while anything is open and opens everything
once nothing is, so a press always changes something.

**Arguments**:

- `model` - Model to ask about.
  

**Returns**:

  Whether at least one container is open.

<a id="edit_cfg_json.model_text.row_diagnostic"></a>

#### row\_diagnostic

```python
def row_diagnostic(model: EditModel, row: MemberRow) -> str
```

Return what is wrong with one member, and nothing when nothing is.

Two things can be wrong with a node and they are not the same thing.
Its text may mean no value of that node at all, which is answered by
the node alone and stays true until the node is edited again; or the
application may have refused the value it holds, which is answered by the
whole configuration and is only known for as long as the rest of the
buffer stands still. The first is preferred when both are there, because
a value that does not exist yet is what has to be corrected first.

What a member validator refused is about the whole member, because that
is what the validator is given, so it is shown at the member and not at
one of the values inside it. Both are addressed by their path, which is
what keeps a value called `cpu` inside a dict from being told what the
application said about a member of that name.

Both backends read this from here, so that neither of them decides on its
own what a refused node is told.

**Arguments**:

- `model` - Model that the node belongs to.
- `row` - Node to report.
  

**Returns**:

  What is wrong with that node, empty when nothing is known to be.

<a id="edit_cfg_json.model_text.verdict_text"></a>

#### verdict\_text

```python
def verdict_text(model: EditModel) -> str
```

Return what the last validation pass found, as text.

A buffer that has not been validated since it last changed says so,
because that is a third state and not a kind of success. What was refused
about one member is shown beside that member instead of here, and this
line names those members so that they can be found. What follows on the
lines below is what the application said that is about no single member,
and it can be there for an accepted buffer too, since a validator may
remark on a value without refusing it.

**Arguments**:

- `model` - Model whose validation state is reported.
  

**Returns**:

  The state of the buffer, followed by any diagnostics.

<a id="edit_cfg_json.model_text.load_text"></a>

#### load\_text

```python
def load_text(model: EditModel) -> str
```

Return what reading the input file did, or an empty text.

Both backends show this, so that the two of them cannot tell the user
two different things about one file.

**Arguments**:

- `model` - Model whose load is reported.
  

**Returns**:

  What the load did, and nothing at all when it did nothing worth
  saying.

<a id="edit_cfg_json.model_text.save_text"></a>

#### save\_text

```python
def save_text(model: EditModel) -> str
```

Return what saving did, or where it would write if it were asked.

Before anything has been saved there is still something to say, because
where a save would go is the one thing a user cannot see from the values
themselves, and there is a real difference between a destination that is
waiting and no destination at all.

Both backends show this, so that neither of them decides on its own what
the user is told about the output file.

**Arguments**:

- `model` - Model whose saving is reported.
  

**Returns**:

  What the last attempt to save did, or where saving would write.

<a id="edit_cfg_json.model_text.model_as_text"></a>

#### model\_as\_text

```python
def model_as_text(model: EditModel) -> str
```

Return the whole model as text, one line per node of it.

The configuration object labels itself first, because what the whole
configuration is for is what the members below it are read in the light
of. What reading the input file did comes next, because it is what
explains the marks on those members. The validation state of the buffer
follows them, and the saving after that, in the order in which a session
reaches them, so that a rendering never leaves it unsaid what the
application would make of what is shown or where it would be written.
This is the rendering used by the examples and by the tests, so that
every step of the editor can be observed without a display. It belongs
to the core rather than to a backend because it is user interface
agnostic.

**Arguments**:

- `model` - Model to render.
  
  A container that is folded away is one line saying so, and what is inside
  it is not shown at all, which is the same thing the two backends do with
  it. What is inside a list or a dict is indented below it.
  

**Returns**:

  The label of the configuration and what its class says about itself,
  what the load did, one line per shown node with its description and
  anything wrong with it below it, and then the validation state and
  the saving, without a trailing line break.

<a id="edit_cfg_json.model_text.model_title"></a>

#### model\_title

```python
def model_title(model: EditModel) -> str
```

Return the label of the whole model, marked while it has changes.

Both backends show this, so that neither of them decides on its own how
an unsaved change looks.

**Arguments**:

- `model` - Model to label.
  

**Returns**:

  The class name of the configuration, with a mark while there are
  changes that are worth saving.

<a id="edit_cfg_json.emphasis"></a>

# edit\_cfg\_json.emphasis

How much each part of the editor stands out, and in which direction.

An editor that shows what the values are for shows a great deal of text, and
not all of it is the same kind of thing: a value is what the user came to
change, a description is text about that value, and a refused validation is
something to act on. Telling them apart by colour is what keeps the screen
readable once the explanations are on it.

What each kind of text is stays here, in the core, and what colour a kind is
belongs to each backend: Textual has theme variables that follow the terminal
into its light or dark mode, and Tk has colour names, and neither of them can
be expressed in the other. What the core owns is therefore the vocabulary and
the two decisions that depend on the state of the model, which are the ones
the two backends could otherwise answer differently.

<a id="edit_cfg_json.emphasis.Emphasis"></a>

## Emphasis Objects

```python
class Emphasis(Enum)
```

One reason for a part of the editor to stand out from the rest.

There is no member for ordinary text, which is the values and their names:
they are what the user is editing, and they are the most legible thing on
the screen precisely because nothing is done to them. Every member here is
a reason to be shown differently from them.

<a id="edit_cfg_json.emphasis.Emphasis.MUTED"></a>

#### MUTED

Text about the values rather than the values, and a state not reached.

The explanatory text is this, and so is a validation that has not been run
yet and a file that has not been written yet: what has not happened is
worth saying and is not worth reading first.

<a id="edit_cfg_json.emphasis.Emphasis.ATTENTION"></a>

#### ATTENTION

Something has happened to this member and the user should see it.

<a id="edit_cfg_json.emphasis.Emphasis.WARNING"></a>

#### WARNING

The input file was not quite what was asked for.

<a id="edit_cfg_json.emphasis.Emphasis.GOOD"></a>

#### GOOD

The application accepted this.

<a id="edit_cfg_json.emphasis.Emphasis.BAD"></a>

#### BAD

The application refused this.

<a id="edit_cfg_json.emphasis.EXPLANATION"></a>

#### EXPLANATION

How the docstring of the class and the description of a member are shown.

They are text about the values, so they are shown as the secondary text they
are — but readably, because an explanation nobody can read explains nothing.

<a id="edit_cfg_json.emphasis.MEMBER_MARK"></a>

#### MEMBER\_MARK

How the marks of one member are shown.

Every mark says that something has happened to that member: the file did not
hold it, the user changed it, or a validator changed what the user wrote.

<a id="edit_cfg_json.emphasis.MEMBER_DIAGNOSTIC"></a>

#### MEMBER\_DIAGNOSTIC

How what is wrong with one member is shown.

It is what the application refused, so it is shown as a refusal and not as
text about the member: it is the one thing on the row that has to be acted on,
and it is deliberately not the muted colour that the description beside it
has.

<a id="edit_cfg_json.emphasis.LOAD_REMARK"></a>

#### LOAD\_REMARK

How what reading the input file did is shown.

A load that had nothing to say says nothing at all, so a message that is there
is always a remark about a file that was not quite what was asked for.

<a id="edit_cfg_json.emphasis.verdict_emphasis"></a>

#### verdict\_emphasis

```python
def verdict_emphasis(model: EditModel) -> Emphasis
```

Return how the validation state of one buffer is shown.

A buffer that has not been validated since it last changed is the third
state and not a kind of failure, so it is shown as what has not happened
yet rather than as something wrong.

**Arguments**:

- `model` - Model whose validation state is shown.
  

**Returns**:

  The emphasis of the validation state of that model.

<a id="edit_cfg_json.emphasis.save_emphasis"></a>

#### save\_emphasis

```python
def save_emphasis(model: EditModel) -> Emphasis
```

Return how what saving did, or would do, is shown.

Where a save would write is not a state that has been reached, so it is
shown as one that has not, exactly like a validation nobody has asked for.

**Arguments**:

- `model` - Model whose saving is shown.
  

**Returns**:

  The emphasis of the last attempt to save, or of the destination that
  is waiting when there has been no attempt.

<a id="edit_cfg_json.edit_model"></a>

# edit\_cfg\_json.edit\_model

The user interface agnostic model of one editable configuration.

<a id="edit_cfg_json.edit_model.EditModel"></a>

## EditModel Objects

```python
class EditModel()
```

The editable state of one `config_as_json.Config` object.

The model does no input or output of its own and owns no event loop, so
a backend can either be run by a convenience wrapper or be mounted as a
widget by an application that already runs its own event loop.

Leaf values are held in JSON space, so that an enum member is held as its
name and a value being typed does not have to be a valid Python value
yet. JSON space is about the kind of the value, not about its notation:
a string member holds the string, and the quotes that the file format
puts around it are added when the file is written and nowhere else.

A member that holds a list, a dict or a nested configuration object is a
tree of rows rather than one row, because what is inside one of those is
edited a value at a time. Each of those rows is addressed by its own path,
and every one of those nodes can be folded away, which is state of this
model so that two backends cannot fold different things.

The buffer is validated by running the application's own configuration
class over it rather than by any rule of the editor's own, so the user
sees the diagnostics the application would produce and the editor cannot
accept anything the application would refuse. Saving runs that same pass
and writes the object it accepted, so nothing reaches the file that the
application would not read back.

What the editor says about the values it shows comes from the application
and from its configuration class, and never from the editor: the
docstring of the class labels the configuration object, and the
description mapping labels the individual members. Both are optional, and
whether they are shown is state of this model rather than of a backend.

A member that `nested_configs()` declares is a node with a class and a
docstring of its own, and its members are the rows below it. It is not
shown as the dict it serializes to, because that would be showing it as
something it is not, and everything inside it belongs to its own class:
the parse converters that say what a value there means, and the members
that class may leave out of a file.

<a id="edit_cfg_json.edit_model.EditModel.__init__"></a>

#### \_\_init\_\_

```python
def __init__(config: Config,
             report: LoadReport = LoadReport(),
             *,
             descriptions: Optional[Descriptions] = None,
             loader: Optional[ConfigLoader] = None,
             out_file: Optional[PathOrStr] = None,
             settings: SettingsSource = Settings(),
             stderr_file: TextIO = sys.stderr) -> None
```

Read the JSON space values of one configuration object.

The object is deep copied before it is serialized, because
`Config.as_json_string()` validates, and a member validator returns
the value that is stored back into the member. Serializing the
caller's object directly could therefore change it, and the editor
never mutates the caller's configuration object.

The model does no input or output of its own, so the file was read
before this and what reading it did arrives as the report.

**Arguments**:

- `config` - Configuration object to edit. It is the source of both
  the member names and their values, and is not modified.
- `report` - What reading the input file did beyond reading the
  values. The default says there was no file to read.
- `descriptions` - What the application says about the members it
  declares, or None when it says nothing. A member that no
  description reaches is shown without one, which is all that
  saying nothing costs.
- `loader` - How this application constructs its configuration, or None
  when it did not say. The model needs it for one thing only: a
  save asks it whether the application would read back the file
  that is about to be written, which is the one question the
  validation of a buffer cannot answer.
- `out_file` - File that saving writes, or None when the user has not
  chosen one yet and the editor has to ask before it can save.
  It is taken exactly as it is, because a destination that was
  named in this call may be the input file and reading one
  file while writing another would be a surprise. A
  destination chosen later, with `set_out_file`, gets the
  extension of the application when it has none of its own.
- `settings` - What the application around the editor has already
  decided, or a callable that answers with it. The default is
  an application with no opinion.
- `stderr_file` - Stream used for user-facing diagnostics.
  

**Raises**:

- `InvalidConfiguration` - The configuration object is not valid.
- `InvalidConfigurationValue` - A member of the configuration object
  does not hold a valid value.

<a id="edit_cfg_json.edit_model.EditModel.config_type_name"></a>

#### config\_type\_name

```python
@property
def config_type_name() -> str
```

Return the class name of the edited configuration object.

<a id="edit_cfg_json.edit_model.EditModel.summary"></a>

#### summary

```python
@property
def summary() -> str
```

Return the one line summary of the configuration class.

It is the first paragraph of the docstring of that class, and it is
empty when the class has no docstring of its own. It is short enough
to be shown on a single row, which is why it stays visible while the
rest of the explanatory text is hidden.

<a id="edit_cfg_json.edit_model.EditModel.docstring"></a>

#### docstring

```python
@property
def docstring() -> str
```

Return the whole docstring of the configuration class.

It is empty when the class has none of its own. The docstring of a
base class is deliberately not used in its place: a label that
describes this library rather than the configuration would be worse
than no label at all.

<a id="edit_cfg_json.edit_model.EditModel.explanations_shown"></a>

#### explanations\_shown

```python
@property
def explanations_shown() -> bool
```

Return whether the explanatory text is being shown in full.

The summary of the configuration is shown either way, because it is
one line for the whole configuration. What this answers is whether
the rest of that docstring and the description of every member are
shown as well, which is one line per member and is what a user who
knows this configuration wants back.

It belongs to the model rather than to a backend, so that an
application cannot end up with two user interfaces that disagree
about whether they are explaining themselves.

<a id="edit_cfg_json.edit_model.EditModel.toggle_explanations"></a>

#### toggle\_explanations

```python
def toggle_explanations() -> None
```

Show the explanatory text if it is hidden, and hide it if not.

<a id="edit_cfg_json.edit_model.EditModel.toggle_fold"></a>

#### toggle\_fold

```python
def toggle_fold(path: ConfigPath) -> None
```

Fold one container away, or open it again.

Which containers are folded belongs to the model, so that an
application cannot end up with two user interfaces that are folded
differently. Every row says whether it is folded and whether it is
shown, which is where a backend reads it.

**Arguments**:

- `path` - Path of the container to fold or open.
  

**Raises**:

- `KeyError` - The path is not a node of this configuration.
- `ValueError` - The node is not a container.

<a id="edit_cfg_json.edit_model.EditModel.toggle_fold_all"></a>

#### toggle\_fold\_all

```python
def toggle_fold_all() -> None
```

Fold every container away, or open every one of them.

One action and not two, because a user who wants the values back
wants all of them back: which of the two it does is decided by what
is on the screen, so a press always changes something.

<a id="edit_cfg_json.edit_model.EditModel.settings"></a>

#### settings

```python
@property
def settings() -> Settings
```

Return what the application has decided, as it is now.

A caller that handed over a callable is asked again here, which is
what handing one over is for. What a later answer can change is
worth knowing exactly: the key combinations are read once, when a
backend builds its bindings, while the file name settings are read
at every save and at every choice of a destination.

Both backends read the settings from here rather than being given
them, so that the two of them cannot bind different keys or offer
the user different file names.

<a id="edit_cfg_json.edit_model.EditModel.load_message"></a>

#### load\_message

```python
@property
def load_message() -> str
```

Return what reading the input file did, empty when nothing.

It cannot change while the editor runs, because the file was read
before the model was built. Both backends show it, so that neither of
them decides on its own what the user is told about the file.

<a id="edit_cfg_json.edit_model.EditModel.rows"></a>

#### rows

```python
@property
def rows() -> Sequence[MemberRow]
```

Return one row per node of the configuration, in the order shown.

The members come in declaration order, which is the order the
configuration class assigns them in and not the sorted order that the
JSON file has. How the file is written is an implementation detail of
saving; what the application declared is what the user thinks about.
What a list or a dict holds follows the member that holds it, in the
order that container holds it in.

Every row is here whether it is folded away or not, because a backend
creates its widgets once and hides the ones that are not shown, and
each row says which of the two it is.

The rows are a snapshot. Editing a member replaces its row, and a
validation pass replaces all of them, so a row that a caller kept is
the state at the time it was read.

<a id="edit_cfg_json.edit_model.EditModel.dirty"></a>

#### dirty

```python
@property
def dirty() -> bool
```

Return whether the buffer holds anything that is worth saving.

A save answers this question, so a buffer that has just been written
is no longer dirty however much was typed into it before.

<a id="edit_cfg_json.edit_model.EditModel.out_file"></a>

#### out\_file

```python
@property
def out_file() -> Optional[PathOrStr]
```

Return the file that saving writes, None when there is none yet.

There is none when the editor was started neither on an input file
nor on an output file, which is what happens when an application
offers to write its very first configuration file. The editor then
has to ask for a destination before it can save anything.

<a id="edit_cfg_json.edit_model.EditModel.save_outcome"></a>

#### save\_outcome

```python
@property
def save_outcome() -> Optional[SaveOutcome]
```

Return what the last attempt to save did, or None when none.

None is not a kind of failure but a third state, exactly as it is for
the verdict: nothing has been saved since the buffer last changed.
Whether an attempt succeeded is what a backend cannot read out of the
message, and it is what decides how that message is shown.

<a id="edit_cfg_json.edit_model.EditModel.save_message"></a>

#### save\_message

```python
@property
def save_message() -> str
```

Return what the last attempt to save did, empty when none.

It is dropped as soon as the buffer changes, for the same reason as
the verdict: what an earlier buffer did when it was saved says
nothing true about the buffer that is there now.

<a id="edit_cfg_json.edit_model.EditModel.saved_config"></a>

#### saved\_config

```python
@property
def saved_config() -> Optional[Config]
```

Return the configuration object that was written, or None.

This is what `edit()` gives back to the application, so that a
caller needs no load of its own to work with what was saved. It is
never the caller's own object, which the editor does not modify and
which would otherwise be stale.

<a id="edit_cfg_json.edit_model.EditModel.verdict"></a>

#### verdict

```python
@property
def verdict() -> Optional[ValidationVerdict]
```

Return what the last validation pass found, or None.

None is not a kind of failure but a third state: the buffer has not
been validated since it last changed. A verdict that was reached
from an earlier buffer would say something untrue about the buffer
that is there now, so it is dropped rather than kept.

<a id="edit_cfg_json.edit_model.EditModel.set_text"></a>

#### set\_text

```python
def set_text(path: ConfigPath, text: str) -> None
```

Set one node of the buffer from the text of an edit field.

Text that the field already shows changes nothing, because it is not
an edit. That is not only tidiness: a field posts a change when it is
given its initial text, and a model that counted that as an edit
would report unsaved changes before the user had touched anything.
It is also what lets a backend write the buffer back into its fields
after a validation pass without that counting as an edit.

Every container the node is inside is brought up to date with it, so
that what the whole configuration holds is always what its rows say.

**Arguments**:

- `path` - Path of the node to set.
- `text` - Text that the edit field holds.
  

**Raises**:

- `KeyError` - The path is not a node of this configuration.
- `ValueError` - The node is not one that this version can edit.

<a id="edit_cfg_json.edit_model.EditModel.check_field"></a>

#### check\_field

```python
def check_field(path: ConfigPath) -> None
```

Report whether the text of one node means a value of it at all.

This is what a backend calls when a field loses the focus, which is
the moment at which the user has moved on from that field. It is
deliberately not done on every change: the name of an enum member is
no name of one for most of the time it takes to type it, and a field
that reported that would be reporting a failure that is not one yet.

Nor is it the validation of the whole configuration. It needs no
candidate configuration and it answers a different question, which is
whether this text means a value at all rather than whether the
configuration is one the application would accept. Both are needed: a
node this refuses is one the whole configuration would refuse too,
but with a message about JSON that a person editing a field never
asked about.

**Arguments**:

- `path` - Path of the node to check.
  

**Raises**:

- `KeyError` - The path is not a node of this configuration.

<a id="edit_cfg_json.edit_model.EditModel.set_out_file"></a>

#### set\_out\_file

```python
def set_out_file(out_file: PathOrStr) -> None
```

Choose the file that saving writes from now on.

This is the whole of what a backend's "save as" does before it
saves, so that choosing a destination and writing to it stay two
things and an application that mounts the model in a user interface
of its own can offer them separately.

A name that has no extension at all gets the one the application
uses for its configuration, because a destination that is being
chosen does not name a file that exists yet. A name that has the
wrong extension is kept as it is and refused by the save that
follows, so that the refusal is reported where every other refused
save is reported and not through a second channel of its own.

**Arguments**:

- `out_file` - File to write, with whatever name and extension the
  application and its user want. The editor has an opinion
  about the extension only where the application gave it one.

<a id="edit_cfg_json.edit_model.EditModel.validate"></a>

#### validate

```python
def validate() -> ValidationVerdict
```

Run the application's own validation over the whole buffer.

A validation pass is not read only. `Config.validate()` documents
that a member validator returns the value that shall be stored back
into the member, so a validator that changes the case of a string
rewrites what the user typed. The buffer is therefore refreshed from
the configuration object that was accepted, and every node the pass
rewrote is marked: accepting the rewrite silently and showing the
user the text they typed would be the worst available behaviour.

A validator may also change how many values a container holds, which
one that removes the duplicates of a list does, so the rows the pass
leaves behind are not always the rows it was given.

**Returns**:

  What the pass found. It is also kept, as `verdict`.

<a id="edit_cfg_json.edit_model.EditModel.save"></a>

#### save

```python
def save() -> SaveOutcome
```

Write the buffer to the output file, if it can be written.

Saving is validating and then writing, and it runs the very same
pass that `validate` does, so a validator that rewrites a value
rewrites it here too and the node says so afterwards. What reaches
the file is therefore always what the editor is showing.

A configuration the application would refuse is not written, because
an editor that produced a file its own application cannot read would
have failed at the one thing it is for. An application that said how
it loads is asked that once more, with the text the file would hold,
because a loader that chooses its class by looking at the JSON is the
one case a validation pass cannot answer for. Nor is anything written
when no destination has been chosen; the editor asks for one instead.
Nor when the destination is a file name that the application does not
use for its configuration, whether it was chosen here or named in
the call that built this model.

A save that wrote the file leaves nothing to save, so the values
that were written become the ones the buffer is compared against
and the model stops reporting itself as dirty.

**Returns**:

  Whether the file was written, and what to tell the user. It is
  also kept, as `save_message`.

<a id="edit_cfg_json.rows"></a>

# edit\_cfg\_json.rows

One row of the editor, and the rows of one whole configuration.

A row is one node of the tree that `tree` takes a configuration apart into: a
member of the configuration, or a value inside a list or a dict that one of
its members holds. Every row is addressed by its path, and the rows of a
configuration are one mapping by path in the order they are shown.

The rows are built twice in the life of a model. They are built when the model
is built, from the values the load produced, and they are built again after a
validation pass, from the values the pass accepted: a member validator returns
the value that is stored back into the member, and one that normalizes a list
can change how many values it holds. What the earlier rows knew is carried
over, which is what makes the second build a refresh rather than a new session.

<a id="edit_cfg_json.rows.NOT_A_MEMBER"></a>

#### NOT\_A\_MEMBER

What a node that is not a member of the configuration is named by.

The declared defaults and the records of a load are both about a member of the
configuration and never about one value inside one, so every node below a
member is looked up under this. No member has it for a name, so it cannot
collide with one, and the lookups are then one form rather than a condition
each.

<a id="edit_cfg_json.rows.MemberRow"></a>

## MemberRow Objects

```python
class MemberRow(NamedTuple)
```

One node of the configuration as it appears in the JSON file.

<a id="edit_cfg_json.rows.MemberRow.path"></a>

#### path

Path that addresses this node in the model.

A member of the configuration has one step. A value inside a list or a
dict that a member holds has the steps of that member and then its own,
which is the index of a list element written out or the key of a
dictionary entry. It is the same path that the description mapping names
a member by, so a description of every element of a list is written with
the `'['` step and reaches each of them.

<a id="edit_cfg_json.rows.MemberRow.value"></a>

#### value

Current value of the node in JSON space, as the user edits it.

A container holds what its children hold, and it is kept that way as they
are edited, so that the whole configuration is what the members of the
model say it is and a folded container cannot hide a change.

<a id="edit_cfg_json.rows.MemberRow.original"></a>

#### original

Value that this node had when the file was last agreed with.

That is when the model was built, and again after every save: what has
just been written is what there is no longer anything to save about, so a
save makes the written value the one the buffer is compared against.

It is what the current value is compared against, and it is also the only
type information that the model has. A PEP 526 annotation on an instance
attribute is recorded nowhere at runtime, so the value that the
configuration object holds is the only source of the type. Reading the
type from the current value instead would not work: a number member that
the user has half typed holds text for as long as the text is not a
number yet, and the member would then stop being a number member. A save
is safe to move it to, because only a validated value is ever written.

<a id="edit_cfg_json.rows.MemberRow.children"></a>

#### children

Paths of the nodes inside this one, or None for a node with none.

An empty tuple is a list or a dict that holds nothing, which is a
different thing from a value: it can be folded, it says how much it holds,
and this version of the editor cannot put anything into it.

A declared nested configuration object has the paths of its own members
here, in the order its own class declares them, because it is a node with
members and not the dictionary it happens to serialize as. It is None for
such a member that holds no object at all, which an `OPTIONAL_MEMBER` does.

<a id="edit_cfg_json.rows.MemberRow.config_type"></a>

#### config\_type

Class of the nested object here, None for every other node.

It is what makes a nested configuration object something other than the
dict it serializes as: the row says the class instead of how many entries
there are, and the docstring of that class is what is said below the row.

It is set for a member that holds no object as well, because the class it
would hold is worth saying and is the whole of what is known about it.

<a id="edit_cfg_json.rows.MemberRow.folded"></a>

#### folded

Whether this container is folded, so that its rows are not shown.

It is always false for a node that holds nothing, because there would be
nothing for folding it to hide. A container that the editor opened folded
is one that would have added more rows than the window can spare, and
every other container starts open: what an application put in its
configuration was put there to be read.

<a id="edit_cfg_json.rows.MemberRow.shown"></a>

#### shown

Whether this node is on the screen as things stand.

A node is hidden when any container it is inside has been folded away.
Its own fold says how much of it is shown and not whether it is: a folded
container is still a row, and it is the row the user presses to open it
again.

It is carried by the row rather than worked out by each backend, so that
two backends cannot disagree about what folding a container hides.

<a id="edit_cfg_json.rows.MemberRow.changed_by_validator"></a>

#### changed\_by\_validator

Whether a validation pass rewrote this value.

A validation pass sets the flag and the next edit of this member clears
it, so it always answers the same question: is the value shown here
something a validator made of what was typed? It belongs to the model
rather than to a backend, so that two backends cannot show it
differently.

<a id="edit_cfg_json.rows.MemberRow.filled_from_default"></a>

#### filled\_from\_default

Whether the declared defaults supplied this value.

It is set when a load that was allowed to use the defaults filled in a
member the input file did not hold, and it stays set for the rest of the
session: that the file did not hold this value remains true whatever the
user then types into it. It belongs to the model for the same reason as
the flag above, so that two backends cannot show it differently.

Only a member of the configuration carries it, because the declared
defaults supply a whole member and never one value inside one.

<a id="edit_cfg_json.rows.MemberRow.load_reason"></a>

#### load\_reason

What reading the input file did to this member, empty when nothing.

Reading a file is not always only reading it. A class that declares rules
for reading an older format may have supplied this value or renamed a key
of the file into this member, and parsing or validating may have
normalized what the file held. The user has to be told, because the value
shown is then not the value in the file.

It says which of those things happened wherever the load recorded it, and
says that the value is not the file's where it did not, which is the whole
of what a comparison can know. It stays as it is for the rest of the
session, exactly as the flag above does and for the same reason, and the
two are never both there: what the declared defaults filled in is said by
that flag, which says more than this would.

Only a member of the configuration carries it, for the same reason as the
flag above: what the load recorded is recorded for a member, and a record
about a value inside one is a record about that member.

<a id="edit_cfg_json.rows.MemberRow.description"></a>

#### description

What is said about this node, empty when nothing is.

The application says most of it, in the description mapping, and the type
of the node says the rest: the names an enum accepts, or what kind of
value it holds, and whether the class that owns it may leave it out of the
file. It is read whenever the rows are built, because it says what the node
is for and that does not change while it is edited.

A container is described by the application or not at all: the row of a
container already says how much it holds, and the rows below it say what
each of them is.

The docstring of a nested configuration object is deliberately not here.
How much of it is shown depends on whether that node is open, and what a
row says about itself cannot depend on that: `row_description` is where
the two are put together.

<a id="edit_cfg_json.rows.MemberRow.converter"></a>

#### converter

How the text of this node becomes the value that is stored in it.

It is None for a node that holds what the file holds, which is most of
them. It is what says that a node holds an enum, and that answers two
questions: which names the description of the node lists, and whether the
text the field holds means a value of it at all.

A value inside a list never has one, because `config_as_json` applies a
parse converter to the values of a dictionary and to nothing else.

<a id="edit_cfg_json.rows.MemberRow.conversion"></a>

#### conversion

Why the text of this node means no value of it, empty when it does.

It is answered by this node alone, which is what makes it a different
thing from what a validation pass says about it: it stays true until this
node is edited again, whatever happens to the rest of the buffer. It is
set when the user leaves the field and again by every validation pass, and
the next edit of this node clears it.

<a id="edit_cfg_json.rows.MemberRow.name"></a>

#### name

```python
@property
def name() -> str
```

Return the name of the node, the last step of its path.

<a id="edit_cfg_json.rows.MemberRow.depth"></a>

#### depth

```python
@property
def depth() -> int
```

Return how far inside a member of the configuration this is.

A member of the configuration is at nothing, and a value inside one is
one step further in for every container it is inside. It is what the
backends indent a row by.

<a id="edit_cfg_json.rows.MemberRow.foldable"></a>

#### foldable

```python
@property
def foldable() -> bool
```

Return whether this node holds rows that can be folded away.

A list, a dict and a nested configuration object are all one. A
declared member that holds no object is not: there is nothing below it
for folding to hide.

<a id="edit_cfg_json.rows.MemberRow.editable"></a>

#### editable

```python
@property
def editable() -> bool
```

Return whether this node is a value that can be edited.

A list, a dict and a nested configuration object are all structure
rather than a value, so none of them is edited in a field: each of
them is edited through the rows below it. A declared member that holds
no object is not edited either, because no text typed into a field
becomes a configuration object.

<a id="edit_cfg_json.rows.MemberRow.is_text"></a>

#### is\_text

```python
@property
def is_text() -> bool
```

Return whether this node holds text.

This is the difference between a value that is text and a value
whose text is a rendering of it. The text of a text value is the
value itself, while the text of a number is how the number is
written.

<a id="edit_cfg_json.rows.MemberRow.edited"></a>

#### edited

```python
@property
def edited() -> bool
```

Return whether this node holds something that is not saved yet.

A node is changed when it would now be written to the file
differently, and not when it merely was typed in. Typing a value
back to what it was leaves nothing to save, and an editor that still
claimed to have changes would be telling the user something untrue.
Saving says the same thing about every node at once.

A container answers for everything inside it, because what it holds is
kept as its children hold it: a change the user cannot see, because
the container it is in is folded, is still a change.

<a id="edit_cfg_json.rows.MemberRow.value_text"></a>

#### value\_text

```python
@property
def value_text() -> str
```

Return the value of this node as the text a field would show.

A nested configuration object says its class, because that is what it
is: showing how many entries it serializes to would be showing it as
the dictionary it is not. A member that holds no object says which
class is missing. A list or a dict says how much it holds, because its
value is on the rows below it. Every other node shows the text of the
value it holds.

<a id="edit_cfg_json.rows.RowContext"></a>

## RowContext Objects

```python
class RowContext(NamedTuple)
```

Everything that building the rows of one configuration needs.

It is one object rather than one argument each, because every one of them
is read once per node and none of them changes while the rows are built.

The last three are by path and not by name, because the class that answers
for a node is the class that owns it: a nested configuration object parses
its own JSON, applies its own parse converters and decides for itself which
of its members it may leave out of a file.

<a id="edit_cfg_json.rows.RowContext.report"></a>

#### report

What reading the input file did beyond reading the values.

<a id="edit_cfg_json.rows.RowContext.descriptions"></a>

#### descriptions

What the application says about the members it declares.

<a id="edit_cfg_json.rows.RowContext.nodes"></a>

#### nodes

Every configuration object of the tree, by its path.

The configuration itself is one of them, under the empty path, so a node
is answered the same way whether it is a member of the configuration or a
member of something nested inside it.

<a id="edit_cfg_json.rows.RowContext.converters"></a>

#### converters

One parse converter per node of the tree that has one.

<a id="edit_cfg_json.rows.RowContext.optional"></a>

#### optional

Every member that the object holding it may leave out of the file.

<a id="edit_cfg_json.rows.member_values"></a>

#### member\_values

```python
def member_values(config: Config, stderr_file: TextIO) -> dict[str, JsonType]
```

Return one JSON space value per serialized member of one object.

**Arguments**:

- `config` - Configuration object to read. It is not modified, because
  what is read is the text it writes and not the object.
- `stderr_file` - Stream used for user-facing diagnostics.
  

**Returns**:

  The values that this object would write to a file.
  

**Raises**:

- `InvalidConfiguration` - The configuration object is not valid.
- `InvalidConfigurationValue` - A member does not hold a valid value.

<a id="edit_cfg_json.rows.built_rows"></a>

#### built\_rows

```python
def built_rows(
        config: Config, members: Mapping[str, JsonType], report: LoadReport,
        descriptions: Descriptions,
        previous: Mapping[ConfigPath,
                          MemberRow]) -> dict[ConfigPath, MemberRow]
```

Return one row per node of one configuration, in the order shown.

A mapping by path is what the design asks for, because every node is
addressed by its path and no other name for it is needed. A dictionary
keeps the order it was built in, so the order the rows are shown in
survives being a mapping.

The configuration object is asked again at every build rather than once,
because a validation pass hands back the object it accepted and the nested
configuration objects of that one are the objects that own its values.

**Arguments**:

- `config` - Configuration object whose values these are. It is not
  modified, and it is what says which nodes are configuration
  objects and in which order each of them declares its members.
- `members` - One JSON space value per serialized member.
- `report` - What reading the input file did beyond reading the values.
- `descriptions` - What the application says about its members.
- `previous` - The rows as they were before, empty for the first build.
  A node that had a row keeps what that row was compared against
  and is marked when a validation pass changed it; a node that had
  none is a node a validation pass created.
  

**Returns**:

  The rows of that configuration, by path.

<a id="edit_cfg_json.rows.stamped"></a>

#### stamped

```python
def stamped(rows: Mapping[ConfigPath, MemberRow],
            folded: Container[ConfigPath]) -> dict[ConfigPath, MemberRow]
```

Return the rows with the fold state of the buffer written onto them.

A backend reads what is folded and what is shown from the row it is
about, exactly as it reads the marks and the description from there, so
that the two backends cannot fold or hide different things.

**Arguments**:

- `rows` - The rows of the configuration, by path.
- `folded` - Paths of the containers that are folded away.
  

**Returns**:

  The same rows, each saying whether it is folded and whether it shows.

<a id="edit_cfg_json.constructing"></a>

# edit\_cfg\_json.constructing

Building the configuration objects that the editor works with.

There are two of them, and only one of them asks the class for anything.

**An object that did not exist before.** The declared defaults and the values
of an input file both need one, and only the class can make one. More than one
constructor shape is in use, so every parameter this module knows the meaning
of is passed when the class declares it and left out when it does not, which is
principle 4 of section 3 of `doc/design.md` applied to a constructor: what
cannot be said is not said, and the editor is then only less pleasant rather
than unusable.

**An object holding the edit buffer.** Validating the buffer, and saying which
member of a refused buffer was refused, both need an object holding the values
that are on the screen. There the class is not asked at all: the object the
editor already has is copied, and `Config.parse_json` applies the buffer to the
copy. That runs the whole chain the class runs while it reads a file — the keys
are matched, the dict shapes are checked against the defaults, the parse
converters run, the nested configuration objects are built and the validation
plan is applied — and it needs nothing whatever of the constructor. So a class
that needs an argument this library knows nothing about is edited, validated
and saved exactly as well as any other, and only reading a file needs the
loader that the application supplies for it.

**The JSON text is therefore never given to a constructor**, which is what
makes that true. It would gain nothing if it were: `Config.__init__` passes the
text straight to `parse_json` itself, and the one thing that has to go with it
is the load policy, which `__init__` does not take.

<a id="edit_cfg_json.constructing.STREAM_NAME"></a>

#### STREAM\_NAME

Name of the constructor parameter that takes the diagnostics stream.

<a id="edit_cfg_json.constructing.FILE_NAME"></a>

#### FILE\_NAME

Name of the constructor parameter that names a file to read.

<a id="edit_cfg_json.constructing.JSON_TEXT_NAMES"></a>

#### JSON\_TEXT\_NAMES

Every name a configuration class gives its JSON text parameter.

`Config.__init__` names it `from_json_data_text`, and the example
configuration classes that `config_as_json` ships name it `from_json_text` in
the constructors they declare, as does `ConfigFactory`. Both names are
therefore in use in practice, so both are looked for. Nothing is ever passed
under either of them but `None`: a class that declares the parameter without a
default of its own has to be given one, and a class that declares none is
constructed without it.

<a id="edit_cfg_json.constructing.built_config"></a>

#### built\_config

```python
def built_config(factory: Callable[..., Config], *, stream: TextIO) -> Config
```

Construct one configuration holding the values that its class declares.

Nothing is passed for the automatic changes of an old format file, and
nothing needs to be: `Config` gives every configuration object a hook of
its own where the application named none, and `Config.auto_change_hook`
is where the load that used it is read afterwards. A class that declares
the parameter is constructed exactly like one that does not.

**Arguments**:

- `factory` - Class to construct, or a callable that constructs it with
  arguments of its own already bound. A signature is all this needs,
  and `functools.partial` over a class has one.
- `stream` - Stream that collects what the class says about itself. It is
  passed only to a class that declares it; one that does not writes
  wherever it writes, which is less pleasant and not a refusal.
  

**Returns**:

  A configuration object holding only what the class declares.
  

**Raises**:

- `TypeError` - The class cannot be constructed this way, which a class
  whose constructor needs an argument this library knows nothing
  about is.
- `ValueError` - The declared values are ones the class refuses. Every
  refusal of `config_as_json` is a subclass of this.
- `AttributeError` - The class declares no public member at all.

<a id="edit_cfg_json.constructing.parsed_config"></a>

#### parsed\_config

```python
def parsed_config(config: Config,
                  text: str,
                  *,
                  stream: TextIO,
                  replace: str = '',
                  method: Optional[Callable[..., object]] = None) -> Config
```

Return a copy of one configuration object holding one JSON text.

This is how an edit buffer becomes a configuration object. The copy is what
keeps the editor from ever modifying the object it was given, and
`parse_json` is what applies the buffer, with everything the configuration
class does while it reads a file. The hook that records the automatic
changes of a parse is copied with the object, so what the load of the input
file recorded stays as the load left it however often a buffer is parsed.

One method of the copy can be replaced, on the object and not on the class,
which is how the editor reaches a state that the class does not offer: a
parse that validates nothing, so that the plan can be walked step by step
afterwards, and a parse that stops at the key check, so that what the
declared defaults filled in can be read off it. Replacing it on the object
leaves the class of the application untouched, and `parse_json` does not
mistake the replacement for a member, because it counts only the attributes
that are not callable.

**Arguments**:

- `config` - Configuration object whose class and copy are used. It is not
  modified.
- `text` - JSON text holding one value per member, which is the edit buffer
  or the text of an input file.
- `stream` - Stream that collects what the class says about the text.
- `replace` - Name of the method to replace on the copy, empty for none.
- `method` - What to replace that method with, None to replace nothing. It
  is called as the method is called and without the object, because
  an attribute of the object is not a bound method.
  

**Returns**:

  A copy of that configuration object holding the values of the text.
  

**Raises**:

- `KeyError` - The keys of the text do not match the declared members.
- `TypeError` - A value of the text is of a type the class refuses.
- `ValueError` - A value of the text is one the class refuses. Every
  refusal of `config_as_json` is a subclass of this, and text that
  is not JSON at all raises `ConfigBadJson`, which is one of them.

<a id="edit_cfg_json.descriptions"></a>

# edit\_cfg\_json.descriptions

The explanatory text that the editor shows about a configuration.

There are three sources of it, they are independent, and all of them are
optional. The docstring of a configuration class labels the configuration
object — the one being edited, and every nested one inside it, because each of
those is an object with a class of its own. A mapping supplied by the
application labels the individual members, and the type of a member says the
rest.

What a type says is the names of an enum where the member holds one, and what
kind of value the member holds where it does not: text, a whole number, a
number, or true or false. That last one is the least the editor can say about
any member and it is never nothing, which is what a review of step 9 asked for:
a program that is told a class and no mapping showed the members with nothing
under them at all, and the editor does know something about each of them.

It takes a mapping for the members because a member has no docstring at
runtime. A class has one and every reader of the code can see it, while a
string literal written after an assignment is discarded by the compiler and a
PEP 526 annotation on an instance attribute is recorded nowhere at all. So the
members are described by the application in a mapping, and the editor invents
nothing: what it adds to that mapping is read from the enum class of the
member, which is a fact about the type and not a constraint read out of a
validator.

<a id="edit_cfg_json.descriptions.CHOICES_FORM"></a>

#### CHOICES\_FORM

What the editor says about the names one enum member accepts.

<a id="edit_cfg_json.descriptions.OPTIONAL_TEXT"></a>

#### OPTIONAL\_TEXT

What the editor says about a member that the class treats as optional.

`_omit_none_from_json()` is what says which members those are, and section 4.1
of `doc/design.md` names it as one of the sources of the structure. It is a
protected name of `config_as_json` and it is read anyway, because nothing else
answers the question and the answer is worth having: a member that may be left
out is a member a user may leave empty.

<a id="edit_cfg_json.descriptions.path_description"></a>

#### path\_description

```python
def path_description(descriptions: Descriptions, path: ConfigPath) -> str
```

Return what the application says about one member, or nothing.

A selector that addresses no member of this configuration is simply never
used, and is not an error: a wrong description is a cosmetic mistake, and
refusing to open the editor over one would be a much larger one.

**Arguments**:

- `descriptions` - What the application says about its members.
- `path` - Path of the member that is being described.
  

**Returns**:

  The description of that member, and an empty text when the
  application said nothing about it.

<a id="edit_cfg_json.descriptions.class_docstring"></a>

#### class\_docstring

```python
def class_docstring(described: type[object]) -> str
```

Return the whole docstring of one class, or nothing.

`described.__doc__` and deliberately not `inspect.getdoc()`, which
inherits from the base classes: a configuration class without a docstring
of its own would then be labelled with the docstring of `Config`, and a
label that describes the library rather than the configuration is worse
than no label at all. The same holds for the enum class of a member,
which would otherwise be described as an enumeration.

**Arguments**:

- `described` - Class that is being described, which is the class of the
  configuration or the enum class of one of its members.
  

**Returns**:

  The docstring of that class as `inspect.cleandoc` leaves it, and an
  empty text when the class has none of its own.

<a id="edit_cfg_json.descriptions.class_summary"></a>

#### class\_summary

```python
def class_summary(described: type[object]) -> str
```

Return the first paragraph of the docstring, as a single line.

The first paragraph is the summary a docstring is written to begin with,
and one line is what a label of one row can show. The line breaks inside
that paragraph belong to the width of a source file and not to the text,
so they are not kept.

**Arguments**:

- `described` - Class that is being described.
  

**Returns**:

  The summary of that class, and an empty text when it has no docstring.

<a id="edit_cfg_json.descriptions.enum_text"></a>

#### enum\_text

```python
def enum_text(converter: Optional[ParseConverter]) -> str
```

Return what the type of one member says about it, or nothing.

`parse_converters()` is what says that a member holds an enum, because it
is what turns the name in the file back into a member of that enum. The
enum class then says the rest itself: the summary of its own docstring,
when it has one, and the names it accepts.

Reading the names an enum has is not the reading of a validator that this
library has decided never to do. It is the type of the member, it is as
true as the name of the member itself, and it is the same kind of reading
as the docstring of the configuration class.

The summary of that docstring and not the whole of it, which is the one
place where a class here is treated differently from the class of the
configuration. The reason is what the rest of an enum docstring usually
is: notes for whoever writes the application, about how the members are
numbered or how they reach the file, which is not what somebody choosing
between them needs. What they need is the first line and the names.

**Arguments**:

- `converter` - How the text of this member becomes a value, or None for a
  member that holds what the file holds.
  

**Returns**:

  What that enum class says about itself and which names it accepts,
  and an empty text for a member that holds no enum.

<a id="edit_cfg_json.descriptions.optional_members"></a>

#### optional\_members

```python
def optional_members(config: Config) -> frozenset[str]
```

Return the members that this configuration may leave out of a file.

The class is asked, because only the class knows: a member that holds
nothing right now may be one that has to hold something, and one that holds
something may still be allowed to hold nothing. What it is asked is a
protected method, for the reason `OPTIONAL_TEXT` gives, and the answer
needs no checking here, because constructing the object checked it.

**Arguments**:

- `config` - Configuration object being edited. It is not modified.
  

**Returns**:

  The names of the members that are genuinely optional.

<a id="edit_cfg_json.descriptions.optional_paths"></a>

#### optional\_paths

```python
def optional_paths(
        nodes: Mapping[ConfigPath, ConfigNode]) -> frozenset[ConfigPath]
```

Return every member of one tree that its own class may leave out.

A nested configuration object writes its own JSON, so which of its members
it may leave out of that JSON is its class's to say and not the class's
above it. The paths are absolute, so a member is looked up here by the same
path that addresses it everywhere else.

**Arguments**:

- `nodes` - Every configuration object of the tree, by its path.
  

**Returns**:

  The path of every member that the object holding it may omit.

<a id="edit_cfg_json.descriptions.MemberFacts"></a>

## MemberFacts Objects

```python
class MemberFacts(NamedTuple)
```

What the editor knows about the type of one node of the tree.

It is one object rather than one argument each, because the four of them
are read together and answer one question between them: what can be said
about this node that the application did not say.

<a id="edit_cfg_json.descriptions.MemberFacts.value"></a>

#### value

Value the node held when the file was last agreed with.

It is the only type information there is for an ordinary value, because a
PEP 526 annotation on an instance attribute is recorded nowhere at runtime.

<a id="edit_cfg_json.descriptions.MemberFacts.converter"></a>

#### converter

How the text of this node becomes the value it holds, or None.

<a id="edit_cfg_json.descriptions.MemberFacts.optional"></a>

#### optional

Whether the class that owns this node may leave it out of the file.

<a id="edit_cfg_json.descriptions.MemberFacts.nested"></a>

#### nested

Whether this node is a declared nested configuration object.

Such a node holds no value of its own, so what kind of value it is cannot
be said about it. What is said about it instead is the docstring of its
class, and where that is said depends on whether the node is open, which
is why it is not said here.

<a id="edit_cfg_json.descriptions.type_text"></a>

#### type\_text

```python
def type_text(facts: MemberFacts) -> str
```

Return everything the type of one node says about it.

An enum says the most, so where a node holds one that is what is said and
the kind of the value would only repeat it: the name of an enum member is
text, and knowing that is worth nothing beside knowing which names there
are. Every other value says what kind of value it is, which is the one
thing the editor knows about every member of every configuration.

A declared nested configuration object says neither, because it holds no
value: it says its class, which its row shows, and its docstring, which is
shown below it. What it can still say here is that the class above it may
leave it out of the file altogether.

**Arguments**:

- `facts` - What the editor knows about the type of that node.
  

**Returns**:

  What the type of that node says, and an empty text when it says
  nothing at all.

<a id="edit_cfg_json.descriptions.member_description"></a>

#### member\_description

```python
def member_description(descriptions: Descriptions, path: ConfigPath,
                       facts: MemberFacts) -> str
```

Return everything the editor has to say about one node.

What the application says comes first, because it is what this node is
for in this application, and what the type of the node says comes after
it. The second is appended rather than used only where the first is
missing: what a node holds is true whatever the application wrote, and an
application that explains what its members mean should not have to list the
names of an enum or say that a number is a number.

**Arguments**:

- `descriptions` - What the application says about its members.
- `path` - Path of the node that is being described.
- `facts` - What the editor knows about the type of that node.
  

**Returns**:

  The description of that node, which is never empty for a node the
  editor can edit, because the type of it always says something.

<a id="edit_cfg_json.auto_change"></a>

# edit\_cfg\_json.auto\_change

What reading one input file did to the values that it holds.

Reading a file can change what the values are, and from three directions: the
rules a configuration class declares for reading a file of an older format,
the normalization that parsing and validating do, and the declared defaults
filling in what the file left out. The user has to be told, because the values
on the screen are then not the values in the file, and an editor that said
nothing about that would look broken.

**What changed is found by comparing.** The values the load produced are
written back to JSON and compared with the text of the file, key by key. That
is exact, it needs nothing of the configuration class, and it covers all three
directions at once. It is the only one of the two mechanisms here that sees a
value which parsing or a validator normalized, so it stays the mechanism.

**Why it changed is asked of the load, which records it.**
`Config.auto_change_hook()` is the hook that `config_as_json` recorded the
automatic changes of the most recent parse into, and every configuration object
has one whether the application asked for it or not. Each record says what kind
of change it was, which path of the file it consumed and which path of the
configuration it produced, so the editor can say at the member itself what the
load did to it — which the comparison cannot: a key that was renamed is simply
gone from the file, and nothing in the file says which member it became.

**A record reaches a member or it reaches the message.** That one rule places
all of them. A record that produced a member of this configuration explains
that member and is shown there. A record that produced no member consumed a key
of the file that nothing here holds, so it joins the keys that saving leaves
out. A record that did neither supplied a value this configuration does not
write, and the message is the only place it can be named.

**The records are versioned, and the fallback is text.** `config_as_json` steps
`DATA_STRUCTURE_VERSION` whenever what it records changes, so a future version
records something this module was not written for. That is not worth a refusal:
the comparison still finds every changed member, and what the records would
have added is taken from `print_changes`, which is the library's own report and
is version independent. That text is shown as it stands and is never read.

**What the declared defaults filled in is asked of the parse.** It is the one
of the three that has a mark of its own, so it has to be exact, and the keys
of the file do not answer it: a key the rules for an older format renamed into
a member was in the file under another name, and a value those rules supplied
was in the file under no name at all. What the defaults filled in is exactly
what the key check of the parse was not given, so the parse is what is asked,
into a copy of the loaded object whose key check records and stops.

<a id="edit_cfg_json.auto_change.HOOK_DATA_VERSION"></a>

#### HOOK\_DATA\_VERSION

Version of the recorded automatic changes that this module reads.

`ConfigAutoChangeHook.DATA_STRUCTURE_VERSION` is stepped whenever the records
change, including purely additively, so that a reader of them is made to look
at what is new. This is the version that was looked at.

<a id="edit_cfg_json.auto_change.WRITE_ERRORS"></a>

#### WRITE\_ERRORS

Every way in which writing the values of one load back to JSON can fail.

A class may leave part of its own writing to code outside itself, and there is
then nothing to compare the file with. Such a class cannot be shown at all,
because the editor reads the values it shows the very same way, so saying
nothing about the changes here is what leaves that refusal where it belongs.

<a id="edit_cfg_json.auto_change.PARSE_ERRORS"></a>

#### PARSE\_ERRORS

Every way the parse that records the keys can fail before it records them.

It cannot fail for a text that a load has already read, since the probe differs
from the object that read it in the one method that is not reached until the
keys have been recorded. It is caught because a mark is not worth an exception:
what the defaults filled in is then simply not claimed, and every member of it
is reported as one the load changed instead, which is true of it as well and
says less.

<a id="edit_cfg_json.auto_change.KEY_METHOD"></a>

#### KEY\_METHOD

Name of the method that the probe below has replaced with a recording.

<a id="edit_cfg_json.auto_change.RECORDED"></a>

#### RECORDED

What the exception that carries those keys says for itself.

<a id="edit_cfg_json.auto_change.NO_MEMBER"></a>

#### NO\_MEMBER

What the records that reached no member of this configuration are under.

No member has it for a name, so it cannot collide with one, and grouping the
records that reached a member and the records that did not in one mapping is
what makes the rule of the module docstring one pass over them.

<a id="edit_cfg_json.auto_change.REMOVING_KINDS"></a>

#### REMOVING\_KINDS

The kinds of record that leave the value of an old path nowhere at all.

Only these are keys that saving leaves out. The kinds that are not here move a
value somewhere, and one of those that reached no member moved it to a path
this configuration does not write directly — a step on the way to a member of
it, which the rules for an older format take when a whole object moves. Such a
step is reported at the member the object became and nowhere else, because
naming it among the keys that are left out would be untrue of it.

<a id="edit_cfg_json.auto_change.FileChanges"></a>

## FileChanges Objects

```python
class FileChanges(NamedTuple)
```

What one load did to the file it read, beyond reading it.

Every field is empty for a file whose values the load took exactly as they
were, which is the ordinary case and the one in which the editor says
nothing at all about the load.

<a id="edit_cfg_json.auto_change.FileChanges.filled"></a>

#### filled

Members whose value the declared defaults of the class supplied.

Empty for a load that was not allowed to use the defaults at all, and
empty for a file that held every declared key.

<a id="edit_cfg_json.auto_change.FileChanges.dropped"></a>

#### dropped

Paths of the file that this configuration does not write back.

A key the rules for an older format removed is one of these, and so is one
whose member the class leaves out of JSON while it is None. None of them
has a row, because none of them is a member of this configuration, so the
message is the only place they can be reported.

<a id="edit_cfg_json.auto_change.FileChanges.changed"></a>

#### changed

Members whose value the load itself put there or altered.

This is what the comparison found, so a member that a validator or the
parsing normalized is here and nowhere else. A member the declared defaults
filled in is deliberately not one of them: it is marked already, by a mark
that says more than this one would, and one member carrying two marks about
the same thing would be worse than either of them alone.

<a id="edit_cfg_json.auto_change.FileChanges.reasons"></a>

#### reasons

What the load recorded about each member that it recorded anything for.

These are the records that produced a member of this configuration, which
is what lets the editor say at the member what was done to it rather than
only that something was. A member can have more than one when the record is
about a value inside it, so the records of one member are kept in the order
the rules applied them.

<a id="edit_cfg_json.auto_change.FileChanges.unplaced"></a>

#### unplaced

Records that neither a member nor a key of the file accounts for.

A value that the rules for an older format supplied for something this
configuration does not write is what that means in practice. It consumed no
key of the file and produced no member, so the message is the only place it
can be named, and the record carries the value it supplied.

<a id="edit_cfg_json.auto_change.FileChanges.detail"></a>

#### detail

What the library says about its records, for a version not read here.

It is empty whenever the records were read, and it is the report of
`ConfigAutoChangeHook.print_changes` when they were not. It is shown as it
stands and never read: which version records what is the library's to say,
and a text that was parsed would be a second way of depending on it.

<a id="edit_cfg_json.auto_change.FileChanges.anything"></a>

#### anything

```python
@property
def anything() -> bool
```

Return whether reading the file changed what the file said.

What the declared defaults filled in is deliberately not one of the
things that answer this. A file that did not hold every value is
reported as the incomplete file it is, which is a different thing from
a file that was read as something other than what it says.

<a id="edit_cfg_json.auto_change.file_changes"></a>

#### file\_changes

```python
def file_changes(config: Config, text: str, permissive: bool) -> FileChanges
```

Return what one successful load did to the file that it read.

**Arguments**:

- `config` - Configuration object that the load produced. What the load
  recorded is read from this object, because every configuration
  object holds the hook of its own most recent parse whether the
  application asked for one or not.
- `text` - The whole text of the input file.
- `permissive` - Whether the load was allowed to fill in what the file left
  out.
  

**Returns**:

  What the load did, with every field empty for a file that the load
  took exactly as it stood.

<a id="edit_cfg_json.validation"></a>

# edit\_cfg\_json.validation

Running the application's own validation over one edit buffer.

There are three passes here and they answer three different questions. What
the text of each member means is answered first, by the parse converter the
class declared for that member, because a value that does not exist cannot be
validated and the message the configuration class prints for one is about
JSON rather than about the member. What the application makes of the whole
buffer is answered next, by applying it to a candidate configuration, which is
the pass that decides whether the buffer is valid at all. And when that pass
refuses, the plan is walked a third time to say which members it was about,
because `Config.validate()` stops at the first step that refuses and can
therefore report one failure and never say whose it was.

<a id="edit_cfg_json.validation.BUFFER_ERRORS"></a>

#### BUFFER\_ERRORS

Every way in which a configuration class refuses an edit buffer.

`config_as_json` reports a key that is missing or unknown as `KeyError`,
text that is not JSON as `ConfigBadJson`, and a value that a validator
refuses as `InvalidConfiguration`, `InvalidConfigurationValue` or
`InvalidConfigurationType`. Those four are all `ValueError` subclasses, so
these three classes are exactly those failures and nothing besides them.

`NotImplementedError` is deliberately not one of them. It says that the
configuration class is incomplete, which is a defect of the application that
no edit of the buffer can put right, and hiding it in a verdict would send
the user looking for a mistake that is not theirs.

<a id="edit_cfg_json.validation.NOTHING_REFUSED"></a>

#### NOTHING\_REFUSED

What a pass that refused no individual member reports.

It cannot be written to, because every verdict that names no member shares
this one mapping and a default that could be changed would be a defect
waiting to happen.

<a id="edit_cfg_json.validation.ValidationVerdict"></a>

## ValidationVerdict Objects

```python
class ValidationVerdict(NamedTuple)
```

What one validation pass over a whole edit buffer found.

<a id="edit_cfg_json.validation.ValidationVerdict.valid"></a>

#### valid

Whether the application itself would accept this buffer.

<a id="edit_cfg_json.validation.ValidationVerdict.diagnostics"></a>

#### diagnostics

What the application says that is about no single member.

A whole-configuration validator that refused, a key that does not match,
text that is not JSON, or a class the editor cannot construct at all.
What the application said about one member is under `refused` instead, so
that the same sentence is not shown twice.

An accepted buffer can have diagnostics too, because a validator may
remark on a value without refusing it.

<a id="edit_cfg_json.validation.ValidationVerdict.refused"></a>

#### refused

What the application refused about each node, by the path of that node.

Empty for a buffer that was accepted, and empty for one that was refused
for a reason that is about no single member. A node is named here when
its own text means no value of it at all, or when the validators of its
member refused the value it holds.

A path and not a name, because a value inside a list or a dict is a node
of its own and two of them can share a name. What a member validator
refused is about the whole member, since that is what it is given, so it
is under the one step path of that member and never under a value inside
it.

<a id="edit_cfg_json.validation.ValidationPass"></a>

## ValidationPass Objects

```python
class ValidationPass(NamedTuple)
```

The verdict of one validation pass and what it validated.

<a id="edit_cfg_json.validation.ValidationPass.verdict"></a>

#### verdict

What the pass found.

<a id="edit_cfg_json.validation.ValidationPass.members"></a>

#### members

One JSON space value per member of the accepted configuration.

A member validator returns the value that is stored back into the
member, so these are not necessarily the values the pass was given.
They are empty when the buffer was refused, because there is then no
configuration object to read them from.

<a id="edit_cfg_json.validation.ValidationPass.candidate"></a>

#### candidate

The configuration object the pass built, None when it was refused.

Saving writes this very object rather than building a second one from
the same text, so that what reaches the file is what the verdict was
reached about. It is also what `edit()` gives back to the application,
which then needs no load of its own to see what was saved.

<a id="edit_cfg_json.validation.Attribution"></a>

## Attribution Objects

```python
class Attribution(NamedTuple)
```

What the individual validators of one configuration refused.

<a id="edit_cfg_json.validation.Attribution.refused"></a>

#### refused

What the validators of each member said, by the path of that member.

<a id="edit_cfg_json.validation.Attribution.remaining"></a>

#### remaining

What a step that is about no single member said, empty when none.

<a id="edit_cfg_json.validation.PLAN_METHOD"></a>

#### PLAN\_METHOD

Name of the method that the probe below has replaced with nothing.

<a id="edit_cfg_json.validation.validate_buffer"></a>

#### validate\_buffer

```python
def validate_buffer(config: Config, members: dict[str,
                                                  JsonType]) -> ValidationPass
```

Validate one edit buffer by applying it to a candidate configuration.

The buffer is applied to a copy of the configuration object with
`Config.parse_json`, which runs the whole chain the application runs when
it reads its own file: key matching, the recursive check of dict shapes
against the defaults, the parse converters, the nested configuration
objects and then the validation plan. So the user sees exactly the
diagnostics that the application would produce, there is no second
implementation of validation anywhere, and there is no way for the editor
to accept something the application would then refuse.

The class is not constructed, and it is not asked to be. What a
construction would add is the declaring of the members, which a copy has
already, so a class that needs a constructor argument this library knows
nothing about is validated here exactly as well as any other.

What each value means is settled before that, by running the parse
converter of its member. A value that means nothing is reported as the
one member it is about, and the candidate is not built at all: it would
only report the same thing as text it could not read as JSON, which is
an answer to a question the user did not ask.

The stream the candidate writes to is captured rather than passed on,
because these diagnostics are the answer to a question the user asked
and belong on the screen and not in the terminal behind it.

**Arguments**:

- `config` - Configuration object of this session, which says which class
  the buffer belongs to and holds everything about it that is not a
  member. It is not modified.
- `members` - The edit buffer, as one JSON space value per member.
  

**Returns**:

  What the pass found, and the members of the configuration object it
  built. The members are empty when the buffer was refused.

