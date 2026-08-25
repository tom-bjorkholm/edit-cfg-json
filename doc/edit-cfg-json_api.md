# Table of Contents

* [edit\_cfg\_json.finding](#edit_cfg_json.finding)
  * [FindOptions](#edit_cfg_json.finding.FindOptions)
    * [in\_path](#edit_cfg_json.finding.FindOptions.in_path)
    * [in\_value](#edit_cfg_json.finding.FindOptions.in_value)
    * [cased](#edit_cfg_json.finding.FindOptions.cased)
    * [whole](#edit_cfg_json.finding.FindOptions.whole)
  * [FindState](#edit_cfg_json.finding.FindState)
    * [text](#edit_cfg_json.finding.FindState.text)
    * [reached](#edit_cfg_json.finding.FindState.reached)
    * [options](#edit_cfg_json.finding.FindState.options)
  * [FindReport](#edit_cfg_json.finding.FindReport)
    * [text](#edit_cfg_json.finding.FindReport.text)
    * [options](#edit_cfg_json.finding.FindReport.options)
    * [total](#edit_cfg_json.finding.FindReport.total)
    * [place](#edit_cfg_json.finding.FindReport.place)
  * [LOOKS\_IN\_PATH](#edit_cfg_json.finding.LOOKS_IN_PATH)
  * [LOOKS\_IN\_VALUE](#edit_cfg_json.finding.LOOKS_IN_VALUE)
  * [MATCHES\_CASE](#edit_cfg_json.finding.MATCHES_CASE)
  * [MATCHES\_WHOLE](#edit_cfg_json.finding.MATCHES_WHOLE)
  * [FIND\_OPTION\_HELP](#edit_cfg_json.finding.FIND_OPTION_HELP)
  * [looks\_nowhere](#edit_cfg_json.finding.looks_nowhere)
  * [matched](#edit_cfg_json.finding.matched)
  * [next\_match](#edit_cfg_json.finding.next_match)
  * [find\_report](#edit_cfg_json.finding.find_report)
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
  * [member\_values](#edit_cfg_json.tree.member_values)
  * [shown\_values](#edit_cfg_json.tree.shown_values)
  * [shown\_entries](#edit_cfg_json.tree.shown_entries)
  * [file\_values](#edit_cfg_json.tree.file_values)
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
  * [member\_nestings](#edit_cfg_json.tree.member_nestings)
  * [by\_key\_nestings](#edit_cfg_json.tree.by_key_nestings)
  * [unchecked\_members](#edit_cfg_json.tree.unchecked_members)
  * [optional\_members](#edit_cfg_json.tree.optional_members)
  * [optional\_paths](#edit_cfg_json.tree.optional_paths)
  * [omitted\_paths](#edit_cfg_json.tree.omitted_paths)
  * [owner\_path](#edit_cfg_json.tree.owner_path)
  * [ordered\_names](#edit_cfg_json.tree.ordered_names)
  * [flat\_values](#edit_cfg_json.tree.flat_values)
  * [under\_dict](#edit_cfg_json.tree.under_dict)
  * [assembled](#edit_cfg_json.tree.assembled)
* [edit\_cfg\_json.exit\_code](#edit_cfg_json.exit_code)
  * [ExitCode](#edit_cfg_json.exit_code.ExitCode)
    * [OK](#edit_cfg_json.exit_code.ExitCode.OK)
    * [LOAD\_REFUSED](#edit_cfg_json.exit_code.ExitCode.LOAD_REFUSED)
    * [USAGE](#edit_cfg_json.exit_code.ExitCode.USAGE)
    * [NO\_MODULE](#edit_cfg_json.exit_code.ExitCode.NO_MODULE)
    * [NO\_FILE](#edit_cfg_json.exit_code.ExitCode.NO_FILE)
    * [NOT\_PYTHON](#edit_cfg_json.exit_code.ExitCode.NOT_PYTHON)
    * [NOT\_IMPORTABLE](#edit_cfg_json.exit_code.ExitCode.NOT_IMPORTABLE)
    * [NO\_NAME](#edit_cfg_json.exit_code.ExitCode.NO_NAME)
    * [NOT\_CONFIG](#edit_cfg_json.exit_code.ExitCode.NOT_CONFIG)
    * [NO\_DEFAULTS](#edit_cfg_json.exit_code.ExitCode.NO_DEFAULTS)
    * [INVALID](#edit_cfg_json.exit_code.ExitCode.INVALID)
    * [NOT\_WRITTEN](#edit_cfg_json.exit_code.ExitCode.NOT_WRITTEN)
    * [NOT\_SHOWABLE](#edit_cfg_json.exit_code.ExitCode.NOT_SHOWABLE)
    * [NOT\_LOADER](#edit_cfg_json.exit_code.ExitCode.NOT_LOADER)
    * [LOADER\_ARGS](#edit_cfg_json.exit_code.ExitCode.LOADER_ARGS)
    * [WRONG\_CLASS](#edit_cfg_json.exit_code.ExitCode.WRONG_CLASS)
    * [NOT\_DESCRIPTIONS](#edit_cfg_json.exit_code.ExitCode.NOT_DESCRIPTIONS)
    * [NO\_SETTINGS](#edit_cfg_json.exit_code.ExitCode.NO_SETTINGS)
  * [Refusal](#edit_cfg_json.exit_code.Refusal)
    * [\_\_init\_\_](#edit_cfg_json.exit_code.Refusal.__init__)
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
  * [editor\_model](#edit_cfg_json.editing.editor_model)
  * [edit](#edit_cfg_json.editing.edit)
* [edit\_cfg\_json.elements](#edit_cfg_json.elements)
  * [BUILD\_ERRORS](#edit_cfg_json.elements.BUILD_ERRORS)
  * [CLEARED\_KINDS](#edit_cfg_json.elements.CLEARED_KINDS)
  * [NO\_PATTERN](#edit_cfg_json.elements.NO_PATTERN)
  * [NO\_CLASS\_FORM](#edit_cfg_json.elements.NO_CLASS_FORM)
  * [FIXED\_KEYS](#edit_cfg_json.elements.FIXED_KEYS)
  * [BY\_KEY\_PATTERN](#edit_cfg_json.elements.BY_KEY_PATTERN)
  * [NO\_DICT\_YET](#edit_cfg_json.elements.NO_DICT_YET)
  * [NO\_ENTRY\_PATTERN](#edit_cfg_json.elements.NO_ENTRY_PATTERN)
  * [NOT\_EXTENDABLE](#edit_cfg_json.elements.NOT_EXTENDABLE)
  * [NOT\_REMOVABLE](#edit_cfg_json.elements.NOT_REMOVABLE)
  * [NOT\_MOVABLE](#edit_cfg_json.elements.NOT_MOVABLE)
  * [KEY\_NEEDED](#edit_cfg_json.elements.KEY_NEEDED)
  * [KEY\_UNWANTED](#edit_cfg_json.elements.KEY_UNWANTED)
  * [KEY\_TAKEN](#edit_cfg_json.elements.KEY_TAKEN)
  * [ElementOffer](#edit_cfg_json.elements.ElementOffer)
    * [extend](#edit_cfg_json.elements.ElementOffer.extend)
    * [keyed](#edit_cfg_json.elements.ElementOffer.keyed)
    * [remove](#edit_cfg_json.elements.ElementOffer.remove)
    * [cleared](#edit_cfg_json.elements.ElementOffer.cleared)
    * [earlier](#edit_cfg_json.elements.ElementOffer.earlier)
    * [later](#edit_cfg_json.elements.ElementOffer.later)
    * [refusal](#edit_cfg_json.elements.ElementOffer.refusal)
    * [template](#edit_cfg_json.elements.ElementOffer.template)
  * [TreeFacts](#edit_cfg_json.elements.TreeFacts)
    * [values](#edit_cfg_json.elements.TreeFacts.values)
    * [nodes](#edit_cfg_json.elements.TreeFacts.nodes)
    * [nestings](#edit_cfg_json.elements.TreeFacts.nestings)
    * [by\_key](#edit_cfg_json.elements.TreeFacts.by_key)
    * [unchecked](#edit_cfg_json.elements.TreeFacts.unchecked)
    * [types](#edit_cfg_json.elements.TreeFacts.types)
    * [defaults](#edit_cfg_json.elements.TreeFacts.defaults)
    * [made](#edit_cfg_json.elements.TreeFacts.made)
  * [declared\_values](#edit_cfg_json.elements.declared_values)
  * [tree\_facts](#edit_cfg_json.elements.tree_facts)
  * [element\_offers](#edit_cfg_json.elements.element_offers)
  * [grown](#edit_cfg_json.elements.grown)
  * [shrunk](#edit_cfg_json.elements.shrunk)
  * [swapped](#edit_cfg_json.elements.swapped)
  * [moved\_paths](#edit_cfg_json.elements.moved_paths)
  * [kept\_order](#edit_cfg_json.elements.kept_order)
  * [checked\_key](#edit_cfg_json.elements.checked_key)
  * [refused](#edit_cfg_json.elements.refused)
* [edit\_cfg\_json.saving](#edit_cfg_json.saving)
  * [NO\_DESTINATION](#edit_cfg_json.saving.NO_DESTINATION)
  * [NOT\_VALID](#edit_cfg_json.saving.NOT_VALID)
  * [NOT\_LOADABLE](#edit_cfg_json.saving.NOT_LOADABLE)
  * [OTHER\_CLASS](#edit_cfg_json.saving.OTHER_CLASS)
  * [RELOAD\_ERRORS](#edit_cfg_json.saving.RELOAD_ERRORS)
  * [WRITE\_FAILED](#edit_cfg_json.saving.WRITE_FAILED)
  * [BACKUP\_FAILED](#edit_cfg_json.saving.BACKUP_FAILED)
  * [SAVED](#edit_cfg_json.saving.SAVED)
  * [KEPT\_FORM](#edit_cfg_json.saving.KEPT_FORM)
  * [WRITE\_ERRORS](#edit_cfg_json.saving.WRITE_ERRORS)
  * [SaveOutcome](#edit_cfg_json.saving.SaveOutcome)
    * [saved](#edit_cfg_json.saving.SaveOutcome.saved)
    * [message](#edit_cfg_json.saving.SaveOutcome.message)
  * [SaveState](#edit_cfg_json.saving.SaveState)
    * [out\_file](#edit_cfg_json.saving.SaveState.out_file)
    * [outcome](#edit_cfg_json.saving.SaveState.outcome)
    * [written](#edit_cfg_json.saving.SaveState.written)
    * [written\_files](#edit_cfg_json.saving.SaveState.written_files)
  * [KeptFile](#edit_cfg_json.saving.KeptFile)
    * [name](#edit_cfg_json.saving.KeptFile.name)
    * [message](#edit_cfg_json.saving.KeptFile.message)
  * [NOTHING\_KEPT](#edit_cfg_json.saving.NOTHING_KEPT)
  * [kept\_file](#edit_cfg_json.saving.kept_file)
  * [keep\_previous](#edit_cfg_json.saving.keep_previous)
  * [reload\_refusal](#edit_cfg_json.saving.reload_refusal)
  * [write\_config](#edit_cfg_json.saving.write_config)
* [edit\_cfg\_json.converting](#edit_cfg_json.converting)
  * [CONVERSION\_ERRORS](#edit_cfg_json.converting.CONVERSION_ERRORS)
  * [NOT\_A\_BOOL\_FORM](#edit_cfg_json.converting.NOT_A_BOOL_FORM)
  * [Converted](#edit_cfg_json.converting.Converted)
    * [value](#edit_cfg_json.converting.Converted.value)
    * [message](#edit_cfg_json.converting.Converted.message)
  * [member\_converters](#edit_cfg_json.converting.member_converters)
  * [node\_converters](#edit_cfg_json.converting.node_converters)
  * [convert\_member](#edit_cfg_json.converting.convert_member)
  * [refusal\_text](#edit_cfg_json.converting.refusal_text)
* [edit\_cfg\_json.dump](#edit_cfg_json.dump)
  * [PROGRAM](#edit_cfg_json.dump.PROGRAM)
  * [main](#edit_cfg_json.dump.main)
* [edit\_cfg\_json.member\_types](#edit_cfg_json.member_types)
  * [SELF\_NAME](#edit_cfg_json.member_types.SELF_NAME)
  * [SOURCE\_ERRORS](#edit_cfg_json.member_types.SOURCE_ERRORS)
  * [HINT\_ERRORS](#edit_cfg_json.member_types.HINT_ERRORS)
  * [attribute\_texts](#edit_cfg_json.member_types.attribute_texts)
  * [declared\_hints](#edit_cfg_json.member_types.declared_hints)
  * [leaf\_type](#edit_cfg_json.member_types.leaf_type)
  * [member\_types](#edit_cfg_json.member_types.member_types)
  * [node\_types](#edit_cfg_json.member_types.node_types)
* [edit\_cfg\_json.cli](#edit_cfg_json.cli)
  * [DESCRIPTION](#edit_cfg_json.cli.DESCRIPTION)
  * [POLICY\_NAMES](#edit_cfg_json.cli.POLICY_NAMES)
  * [named\_policy](#edit_cfg_json.cli.named_policy)
  * [add\_file\_options](#edit_cfg_json.cli.add_file_options)
  * [run\_cli](#edit_cfg_json.cli.run_cli)
* [edit\_cfg\_json.leaf\_value](#edit_cfg_json.leaf_value)
  * [TEXT\_KIND](#edit_cfg_json.leaf_value.TEXT_KIND)
  * [WHOLE\_NUMBER\_KIND](#edit_cfg_json.leaf_value.WHOLE_NUMBER_KIND)
  * [NUMBER\_KIND](#edit_cfg_json.leaf_value.NUMBER_KIND)
  * [BOOL\_KIND](#edit_cfg_json.leaf_value.BOOL_KIND)
  * [LIST\_KIND](#edit_cfg_json.leaf_value.LIST_KIND)
  * [DICT\_KIND](#edit_cfg_json.leaf_value.DICT_KIND)
  * [VALUE\_KINDS](#edit_cfg_json.leaf_value.VALUE_KINDS)
  * [EMPTY\_VALUES](#edit_cfg_json.leaf_value.EMPTY_VALUES)
  * [NO\_KIND](#edit_cfg_json.leaf_value.NO_KIND)
  * [NO\_VALUE\_TEXT](#edit_cfg_json.leaf_value.NO_VALUE_TEXT)
  * [BOOL\_WORDS](#edit_cfg_json.leaf_value.BOOL_WORDS)
  * [BOOL\_CHOICES](#edit_cfg_json.leaf_value.BOOL_CHOICES)
  * [LeafType](#edit_cfg_json.leaf_value.LeafType)
    * [kind](#edit_cfg_json.leaf_value.LeafType.kind)
    * [nothing](#edit_cfg_json.leaf_value.LeafType.nothing)
    * [inside](#edit_cfg_json.leaf_value.LeafType.inside)
  * [empty\_value](#edit_cfg_json.leaf_value.empty_value)
  * [kind\_of](#edit_cfg_json.leaf_value.kind_of)
  * [leaf\_kind](#edit_cfg_json.leaf_value.leaf_kind)
  * [bool\_word](#edit_cfg_json.leaf_value.bool_word)
  * [value\_as\_text](#edit_cfg_json.leaf_value.value_as_text)
  * [text\_as\_value](#edit_cfg_json.leaf_value.text_as_value)
  * [canonical\_text](#edit_cfg_json.leaf_value.canonical_text)
  * [values\_differ](#edit_cfg_json.leaf_value.values_differ)
  * [kind\_text](#edit_cfg_json.leaf_value.kind_text)
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
    * [bool\_nodes](#edit_cfg_json.buffer.EditBuffer.bool_nodes)
    * [dirty](#edit_cfg_json.buffer.EditBuffer.dirty)
    * [anything\_open](#edit_cfg_json.buffer.EditBuffer.anything_open)
    * [values](#edit_cfg_json.buffer.EditBuffer.values)
    * [set\_text](#edit_cfg_json.buffer.EditBuffer.set_text)
    * [check\_field](#edit_cfg_json.buffer.EditBuffer.check_field)
    * [check\_all](#edit_cfg_json.buffer.EditBuffer.check_all)
    * [toggle\_fold](#edit_cfg_json.buffer.EditBuffer.toggle_fold)
    * [toggle\_fold\_all](#edit_cfg_json.buffer.EditBuffer.toggle_fold_all)
    * [open\_all](#edit_cfg_json.buffer.EditBuffer.open_all)
    * [search](#edit_cfg_json.buffer.EditBuffer.search)
    * [find](#edit_cfg_json.buffer.EditBuffer.find)
    * [set\_find\_options](#edit_cfg_json.buffer.EditBuffer.set_find_options)
    * [find\_next](#edit_cfg_json.buffer.EditBuffer.find_next)
    * [add\_element](#edit_cfg_json.buffer.EditBuffer.add_element)
    * [remove\_element](#edit_cfg_json.buffer.EditBuffer.remove_element)
    * [move\_element](#edit_cfg_json.buffer.EditBuffer.move_element)
    * [take\_subtrees](#edit_cfg_json.buffer.EditBuffer.take_subtrees)
    * [keep\_saved](#edit_cfg_json.buffer.EditBuffer.keep_saved)
    * [take\_validated](#edit_cfg_json.buffer.EditBuffer.take_validated)
* [edit\_cfg\_json.settings\_file](#edit_cfg_json.settings_file)
  * [SETTINGS\_VARIABLE](#edit_cfg_json.settings_file.SETTINGS_VARIABLE)
  * [SHARED\_SETTINGS](#edit_cfg_json.settings_file.SHARED_SETTINGS)
  * [NO\_SETTINGS\_FILE](#edit_cfg_json.settings_file.NO_SETTINGS_FILE)
  * [SETTINGS\_REFUSED](#edit_cfg_json.settings_file.SETTINGS_REFUSED)
  * [OLDER\_SETTINGS](#edit_cfg_json.settings_file.OLDER_SETTINGS)
  * [settings\_file](#edit_cfg_json.settings_file.settings_file)
  * [load\_settings](#edit_cfg_json.settings_file.load_settings)
* [edit\_cfg\_json.placing](#edit_cfg_json.placing)
  * [OBJECT\_KINDS](#edit_cfg_json.placing.OBJECT_KINDS)
  * [ObjectPlace](#edit_cfg_json.placing.ObjectPlace)
    * [holder](#edit_cfg_json.placing.ObjectPlace.holder)
    * [nesting](#edit_cfg_json.placing.ObjectPlace.nesting)
    * [member](#edit_cfg_json.placing.ObjectPlace.member)
    * [key](#edit_cfg_json.placing.ObjectPlace.key)
  * [new\_object](#edit_cfg_json.placing.new_object)
  * [object\_added](#edit_cfg_json.placing.object_added)
  * [object\_removed](#edit_cfg_json.placing.object_removed)
  * [object\_moved](#edit_cfg_json.placing.object_moved)
* [edit\_cfg\_json.settings](#edit_cfg_json.settings)
  * [DUPLICATE\_KEY](#edit_cfg_json.settings.DUPLICATE_KEY)
  * [NOT\_AN\_EXTENSION](#edit_cfg_json.settings.NOT_AN_EXTENSION)
  * [NOT\_A\_SUFFIX](#edit_cfg_json.settings.NOT_A_SUFFIX)
  * [NOT\_A\_COUNT](#edit_cfg_json.settings.NOT_A_COUNT)
  * [MIN\_BACKUPS](#edit_cfg_json.settings.MIN_BACKUPS)
  * [names\_a\_file](#edit_cfg_json.settings.names_a_file)
  * [with\_dot](#edit_cfg_json.settings.with_dot)
  * [BACKUP\_SUFFIX](#edit_cfg_json.settings.BACKUP_SUFFIX)
  * [WRONG\_EXTENSION](#edit_cfg_json.settings.WRONG_EXTENSION)
  * [ActionSettings](#edit_cfg_json.settings.ActionSettings)
    * [quit](#edit_cfg_json.settings.ActionSettings.quit)
    * [validate](#edit_cfg_json.settings.ActionSettings.validate)
    * [save](#edit_cfg_json.settings.ActionSettings.save)
    * [save\_as](#edit_cfg_json.settings.ActionSettings.save_as)
    * [cancel](#edit_cfg_json.settings.ActionSettings.cancel)
    * [explain](#edit_cfg_json.settings.ActionSettings.explain)
    * [fold](#edit_cfg_json.settings.ActionSettings.fold)
    * [find](#edit_cfg_json.settings.ActionSettings.find)
    * [find\_next](#edit_cfg_json.settings.ActionSettings.find_next)
  * [Settings](#edit_cfg_json.settings.Settings)
    * [actions](#edit_cfg_json.settings.Settings.actions)
    * [file\_extension](#edit_cfg_json.settings.Settings.file_extension)
    * [extension\_enforced](#edit_cfg_json.settings.Settings.extension_enforced)
    * [backup\_suffix](#edit_cfg_json.settings.Settings.backup_suffix)
    * [backup\_count](#edit_cfg_json.settings.Settings.backup_count)
    * [priority\_keys](#edit_cfg_json.settings.Settings.priority_keys)
    * [confirm\_overwrite](#edit_cfg_json.settings.Settings.confirm_overwrite)
  * [current\_settings](#edit_cfg_json.settings.current_settings)
  * [CheckedFile](#edit_cfg_json.settings.CheckedFile)
    * [name](#edit_cfg_json.settings.CheckedFile.name)
    * [message](#edit_cfg_json.settings.CheckedFile.message)
  * [checked\_file](#edit_cfg_json.settings.checked_file)
  * [chosen\_file](#edit_cfg_json.settings.chosen_file)
* [edit\_cfg\_json.cli\_target](#edit_cfg_json.cli_target)
  * [PYTHON\_SUFFIX](#edit_cfg_json.cli_target.PYTHON_SUFFIX)
  * [NO\_MODULE\_MESSAGE](#edit_cfg_json.cli_target.NO_MODULE_MESSAGE)
  * [NO\_FILE\_MESSAGE](#edit_cfg_json.cli_target.NO_FILE_MESSAGE)
  * [NOT\_PYTHON\_MESSAGE](#edit_cfg_json.cli_target.NOT_PYTHON_MESSAGE)
  * [NOT\_IMPORTABLE\_MESSAGE](#edit_cfg_json.cli_target.NOT_IMPORTABLE_MESSAGE)
  * [NO\_NAME\_MESSAGE](#edit_cfg_json.cli_target.NO_NAME_MESSAGE)
  * [NOT\_CONFIG\_MESSAGE](#edit_cfg_json.cli_target.NOT_CONFIG_MESSAGE)
  * [NO\_TARGET\_MESSAGE](#edit_cfg_json.cli_target.NO_TARGET_MESSAGE)
  * [OWN\_TARGET\_MESSAGE](#edit_cfg_json.cli_target.OWN_TARGET_MESSAGE)
  * [NOT\_LOADER\_MESSAGE](#edit_cfg_json.cli_target.NOT_LOADER_MESSAGE)
  * [LOADER\_ARGS\_MESSAGE](#edit_cfg_json.cli_target.LOADER_ARGS_MESSAGE)
  * [NO\_LOADER\_CONFIG](#edit_cfg_json.cli_target.NO_LOADER_CONFIG)
  * [WRONG\_CLASS\_MESSAGE](#edit_cfg_json.cli_target.WRONG_CLASS_MESSAGE)
  * [NOT\_DESCRIPTIONS](#edit_cfg_json.cli_target.NOT_DESCRIPTIONS)
  * [NOT\_SHOWABLE\_MESSAGE](#edit_cfg_json.cli_target.NOT_SHOWABLE_MESSAGE)
  * [explained](#edit_cfg_json.cli_target.explained)
  * [checked\_class](#edit_cfg_json.cli_target.checked_class)
  * [Target](#edit_cfg_json.cli_target.Target)
    * [config](#edit_cfg_json.cli_target.Target.config)
    * [descriptions](#edit_cfg_json.cli_target.Target.descriptions)
    * [loader](#edit_cfg_json.cli_target.Target.loader)
    * [wanted](#edit_cfg_json.cli_target.Target.wanted)
  * [target\_of](#edit_cfg_json.cli_target.target_of)
* [edit\_cfg\_json.settings\_config](#edit_cfg_json.settings_config)
  * [UNKNOWN\_ACTION](#edit_cfg_json.settings_config.UNKNOWN_ACTION)
  * [REFUSED\_KEYS](#edit_cfg_json.settings_config.REFUSED_KEYS)
  * [declared\_actions](#edit_cfg_json.settings_config.declared_actions)
  * [ADDED\_ACTIONS](#edit_cfg_json.settings_config.ADDED_ACTIONS)
  * [SettingsConfig](#edit_cfg_json.settings_config.SettingsConfig)
    * [\_\_init\_\_](#edit_cfg_json.settings_config.SettingsConfig.__init__)
    * [as\_settings](#edit_cfg_json.settings_config.SettingsConfig.as_settings)
    * [get\_validation\_plan](#edit_cfg_json.settings_config.SettingsConfig.get_validation_plan)
  * [ACTION\_DESCRIPTIONS](#edit_cfg_json.settings_config.ACTION_DESCRIPTIONS)
  * [EVERY\_ACTION](#edit_cfg_json.settings_config.EVERY_ACTION)
  * [SETTINGS\_DESCRIPTIONS](#edit_cfg_json.settings_config.SETTINGS_DESCRIPTIONS)
  * [described\_below](#edit_cfg_json.settings_config.described_below)
* [edit\_cfg\_json.model\_text](#edit_cfg_json.model_text)
  * [FOLDED\_MARK](#edit_cfg_json.model_text.FOLDED_MARK)
  * [EDITED\_MARK](#edit_cfg_json.model_text.EDITED_MARK)
  * [VALIDATOR\_MARK](#edit_cfg_json.model_text.VALIDATOR_MARK)
  * [FILLED\_MARK](#edit_cfg_json.model_text.FILLED_MARK)
  * [LOAD\_FORM](#edit_cfg_json.model_text.LOAD_FORM)
  * [FOUND\_MARK](#edit_cfg_json.model_text.FOUND_MARK)
  * [DIRTY\_MARK](#edit_cfg_json.model_text.DIRTY_MARK)
  * [VERDICT\_FORM](#edit_cfg_json.model_text.VERDICT_FORM)
  * [VALID\_STATE](#edit_cfg_json.model_text.VALID_STATE)
  * [INVALID\_STATE](#edit_cfg_json.model_text.INVALID_STATE)
  * [UNKNOWN\_STATE](#edit_cfg_json.model_text.UNKNOWN_STATE)
  * [REFUSED\_FORM](#edit_cfg_json.model_text.REFUSED_FORM)
  * [FIND\_FORM](#edit_cfg_json.model_text.FIND_FORM)
  * [FIND\_COUNT\_FORM](#edit_cfg_json.model_text.FIND_COUNT_FORM)
  * [NOT\_FOUND\_FORM](#edit_cfg_json.model_text.NOT_FOUND_FORM)
  * [FIND\_NOWHERE\_FORM](#edit_cfg_json.model_text.FIND_NOWHERE_FORM)
  * [SAVE\_TO\_FORM](#edit_cfg_json.model_text.SAVE_TO_FORM)
  * [NO\_DESTINATION\_TEXT](#edit_cfg_json.model_text.NO_DESTINATION_TEXT)
  * [SUMMARY\_SEPARATOR](#edit_cfg_json.model_text.SUMMARY_SEPARATOR)
  * [DESCRIPTION\_INDENT](#edit_cfg_json.model_text.DESCRIPTION_INDENT)
  * [TREE\_INDENT](#edit_cfg_json.model_text.TREE_INDENT)
  * [LEAF\_FORM](#edit_cfg_json.model_text.LEAF_FORM)
  * [CONTAINER\_FORM](#edit_cfg_json.model_text.CONTAINER_FORM)
  * [CLOSE\_QUESTION](#edit_cfg_json.model_text.CLOSE_QUESTION)
  * [OVERWRITE\_QUESTION](#edit_cfg_json.model_text.OVERWRITE_QUESTION)
  * [KEPT\_QUESTION](#edit_cfg_json.model_text.KEPT_QUESTION)
  * [SUBTREE\_VALID\_MARK](#edit_cfg_json.model_text.SUBTREE_VALID_MARK)
  * [SUBTREE\_REFUSED\_MARK](#edit_cfg_json.model_text.SUBTREE_REFUSED_MARK)
  * [INSIDE\_VALID\_MARK](#edit_cfg_json.model_text.INSIDE_VALID_MARK)
  * [INSIDE\_REFUSED\_MARK](#edit_cfg_json.model_text.INSIDE_REFUSED_MARK)
  * [row\_value\_text](#edit_cfg_json.model_text.row_value_text)
  * [row\_marks](#edit_cfg_json.model_text.row_marks)
  * [docstring\_text](#edit_cfg_json.model_text.docstring_text)
  * [row\_describes](#edit_cfg_json.model_text.row_describes)
  * [row\_description](#edit_cfg_json.model_text.row_description)
  * [row\_validates](#edit_cfg_json.model_text.row_validates)
  * [row\_subtree\_text](#edit_cfg_json.model_text.row_subtree_text)
  * [row\_fold\_text](#edit_cfg_json.model_text.row_fold_text)
  * [rows\_shape](#edit_cfg_json.model_text.rows_shape)
  * [can\_fold](#edit_cfg_json.model_text.can_fold)
  * [fold\_hides](#edit_cfg_json.model_text.fold_hides)
  * [row\_diagnostic](#edit_cfg_json.model_text.row_diagnostic)
  * [verdict\_text](#edit_cfg_json.model_text.verdict_text)
  * [find\_text](#edit_cfg_json.model_text.find_text)
  * [load\_text](#edit_cfg_json.model_text.load_text)
  * [save\_text](#edit_cfg_json.model_text.save_text)
  * [close\_question](#edit_cfg_json.model_text.close_question)
  * [overwrite\_question](#edit_cfg_json.model_text.overwrite_question)
  * [model\_as\_text](#edit_cfg_json.model_text.model_as_text)
  * [model\_title](#edit_cfg_json.model_text.model_title)
* [edit\_cfg\_json.version\_report](#edit_cfg_json.version_report)
  * [MAIN\_PACKAGE](#edit_cfg_json.version_report.MAIN_PACKAGE)
  * [EcajVersionReporter](#edit_cfg_json.version_report.EcajVersionReporter)
    * [package\_names](#edit_cfg_json.version_report.EcajVersionReporter.package_names)
    * [get\_app\_support\_expires](#edit_cfg_json.version_report.EcajVersionReporter.get_app_support_expires)
    * [get\_main\_package\_name](#edit_cfg_json.version_report.EcajVersionReporter.get_main_package_name)
    * [recommended\_python](#edit_cfg_json.version_report.EcajVersionReporter.recommended_python)
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
  * [subtree\_emphasis](#edit_cfg_json.emphasis.subtree_emphasis)
  * [find\_emphasis](#edit_cfg_json.emphasis.find_emphasis)
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
    * [open\_all](#edit_cfg_json.edit_model.EditModel.open_all)
    * [search](#edit_cfg_json.edit_model.EditModel.search)
    * [find](#edit_cfg_json.edit_model.EditModel.find)
    * [set\_find\_options](#edit_cfg_json.edit_model.EditModel.set_find_options)
    * [find\_next](#edit_cfg_json.edit_model.EditModel.find_next)
    * [settings](#edit_cfg_json.edit_model.EditModel.settings)
    * [load\_message](#edit_cfg_json.edit_model.EditModel.load_message)
    * [rows](#edit_cfg_json.edit_model.EditModel.rows)
    * [dirty](#edit_cfg_json.edit_model.EditModel.dirty)
    * [out\_file](#edit_cfg_json.edit_model.EditModel.out_file)
    * [overwritten\_file](#edit_cfg_json.edit_model.EditModel.overwritten_file)
    * [save\_outcome](#edit_cfg_json.edit_model.EditModel.save_outcome)
    * [save\_message](#edit_cfg_json.edit_model.EditModel.save_message)
    * [saved\_config](#edit_cfg_json.edit_model.EditModel.saved_config)
    * [verdict](#edit_cfg_json.edit_model.EditModel.verdict)
    * [set\_text](#edit_cfg_json.edit_model.EditModel.set_text)
    * [add\_element](#edit_cfg_json.edit_model.EditModel.add_element)
    * [remove\_element](#edit_cfg_json.edit_model.EditModel.remove_element)
    * [move\_element](#edit_cfg_json.edit_model.EditModel.move_element)
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
    * [subtree\_valid](#edit_cfg_json.rows.MemberRow.subtree_valid)
    * [subtree\_refusal](#edit_cfg_json.rows.MemberRow.subtree_refusal)
    * [has\_objects](#edit_cfg_json.rows.MemberRow.has_objects)
    * [found](#edit_cfg_json.rows.MemberRow.found)
    * [declared](#edit_cfg_json.rows.MemberRow.declared)
    * [offer](#edit_cfg_json.rows.MemberRow.offer)
    * [name](#edit_cfg_json.rows.MemberRow.name)
    * [depth](#edit_cfg_json.rows.MemberRow.depth)
    * [foldable](#edit_cfg_json.rows.MemberRow.foldable)
    * [is\_object](#edit_cfg_json.rows.MemberRow.is_object)
    * [holds\_nothing](#edit_cfg_json.rows.MemberRow.holds_nothing)
    * [editable](#edit_cfg_json.rows.MemberRow.editable)
    * [kind](#edit_cfg_json.rows.MemberRow.kind)
    * [is\_text](#edit_cfg_json.rows.MemberRow.is_text)
    * [is\_bool](#edit_cfg_json.rows.MemberRow.is_bool)
    * [edited](#edit_cfg_json.rows.MemberRow.edited)
    * [value\_text](#edit_cfg_json.rows.MemberRow.value_text)
  * [RowContext](#edit_cfg_json.rows.RowContext)
    * [report](#edit_cfg_json.rows.RowContext.report)
    * [descriptions](#edit_cfg_json.rows.RowContext.descriptions)
    * [nodes](#edit_cfg_json.rows.RowContext.nodes)
    * [converters](#edit_cfg_json.rows.RowContext.converters)
    * [optional](#edit_cfg_json.rows.RowContext.optional)
    * [offers](#edit_cfg_json.rows.RowContext.offers)
    * [types](#edit_cfg_json.rows.RowContext.types)
    * [refreshing](#edit_cfg_json.rows.RowContext.refreshing)
  * [built\_rows](#edit_cfg_json.rows.built_rows)
  * [BufferState](#edit_cfg_json.rows.BufferState)
    * [folded](#edit_cfg_json.rows.BufferState.folded)
    * [answers](#edit_cfg_json.rows.BufferState.answers)
    * [found](#edit_cfg_json.rows.BufferState.found)
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
  * [NOTHING\_TEXT](#edit_cfg_json.descriptions.NOTHING_TEXT)
  * [path\_description](#edit_cfg_json.descriptions.path_description)
  * [class\_docstring](#edit_cfg_json.descriptions.class_docstring)
  * [class\_summary](#edit_cfg_json.descriptions.class_summary)
  * [enum\_text](#edit_cfg_json.descriptions.enum_text)
  * [MemberFacts](#edit_cfg_json.descriptions.MemberFacts)
    * [value](#edit_cfg_json.descriptions.MemberFacts.value)
    * [declared](#edit_cfg_json.descriptions.MemberFacts.declared)
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
  * [SubtreeAnswer](#edit_cfg_json.validation.SubtreeAnswer)
    * [valid](#edit_cfg_json.validation.SubtreeAnswer.valid)
    * [refused](#edit_cfg_json.validation.SubtreeAnswer.refused)
  * [NO\_SUBTREES](#edit_cfg_json.validation.NO_SUBTREES)
  * [ValidationVerdict](#edit_cfg_json.validation.ValidationVerdict)
    * [valid](#edit_cfg_json.validation.ValidationVerdict.valid)
    * [diagnostics](#edit_cfg_json.validation.ValidationVerdict.diagnostics)
    * [refused](#edit_cfg_json.validation.ValidationVerdict.refused)
  * [ValidationPass](#edit_cfg_json.validation.ValidationPass)
    * [verdict](#edit_cfg_json.validation.ValidationPass.verdict)
    * [members](#edit_cfg_json.validation.ValidationPass.members)
    * [candidate](#edit_cfg_json.validation.ValidationPass.candidate)
    * [subtrees](#edit_cfg_json.validation.ValidationPass.subtrees)
  * [Attribution](#edit_cfg_json.validation.Attribution)
    * [refused](#edit_cfg_json.validation.Attribution.refused)
    * [remaining](#edit_cfg_json.validation.Attribution.remaining)
  * [PLAN\_METHOD](#edit_cfg_json.validation.PLAN_METHOD)
  * [subtree\_answers](#edit_cfg_json.validation.subtree_answers)
  * [validate\_buffer](#edit_cfg_json.validation.validate_buffer)

<a id="edit_cfg_json.finding"></a>

# edit\_cfg\_json.finding

Looking for one node of a configuration that does not fit a window.

A configuration of any interesting size does not fit a window (section 4.6 of
`doc/detailed_design.md`), so the node a user wants is often one they cannot
see. This module is the whole of what looking for it means: what is being
looked for, how a piece of text is compared with one node, which nodes that
reaches and which of them the search has got to.

Nothing here opens a folded container, gives a field the focus or scrolls
anything. What is being looked for is state of the model, by the same rule as
the explain toggle of section 4.4, and reaching what was found is the buffer's
and each backend's: this module answers only which nodes the text is about.

<a id="edit_cfg_json.finding.FindOptions"></a>

## FindOptions Objects

```python
class FindOptions(NamedTuple)
```

How the text being looked for is compared with one node.

Four independent answers, each of which the user changes with a control of
its own, and the defaults are what a person looking for a member wants
without being asked anything: both of the texts a node has, the case
ignored, and a part of one of them enough.

They belong to the model rather than to a backend for the same reason the
fold state does: two user interfaces of one application that looked in
different places would each be right about a different search.

<a id="edit_cfg_json.finding.FindOptions.in_path"></a>

#### in\_path

Whether the path of the node is looked in.

The whole path and not the name alone, so that `ports.http` finds that one
value and `ports` finds the member and everything in it. It is also the
notation the verdict names a refused node in and the one an example
program's command line writes, so what a user has just read can be typed
straight in.

<a id="edit_cfg_json.finding.FindOptions.in_value"></a>

#### in\_value

Whether the value of the node is looked in.

It is the text a field shows, which is what the user is looking at, and it
is only a node that *has* one: a list, a dict and a nested configuration
object each have their value on the rows below them, so there is nothing
of their own to look in.

<a id="edit_cfg_json.finding.FindOptions.cased"></a>

#### cased

Whether the case of the text has to match.

Ignoring it is the default because a member name is written in one case
and remembered in another, and it is the comparison `config_as_json` makes
for the name of an enum member.

<a id="edit_cfg_json.finding.FindOptions.whole"></a>

#### whole

Whether the text has to be the whole of what it is compared with.

A part of it is the default, because a user who knows the whole name of
what they are looking for is the user who least needs a search.

<a id="edit_cfg_json.finding.FindState"></a>

## FindState Objects

```python
class FindState(NamedTuple)
```

What is being looked for, and which node the search has got to.

<a id="edit_cfg_json.finding.FindState.text"></a>

#### text

What is being looked for, empty while nothing is.

Empty is not a text that matches everything but a search that has not been
made: nothing is reached and nothing is said about it, which is what a
cleared field means.

<a id="edit_cfg_json.finding.FindState.reached"></a>

#### reached

Path of the node the search has got to, None when it is at none.

It is a path and not a place among the matches, because a validation pass
can leave the model with other rows than it had (section 4.8): a place
would then be a different node, and a path that is gone is simply gone.

<a id="edit_cfg_json.finding.FindState.options"></a>

#### options

How the text is compared with one node.

<a id="edit_cfg_json.finding.FindReport"></a>

## FindReport Objects

```python
class FindReport(NamedTuple)
```

What the editor says about the search, for a user to read.

<a id="edit_cfg_json.finding.FindReport.text"></a>

#### text

What is being looked for, empty while nothing is.

<a id="edit_cfg_json.finding.FindReport.options"></a>

#### options

How the text is being compared, which is what the controls show.

<a id="edit_cfg_json.finding.FindReport.total"></a>

#### total

How many nodes the text reaches.

It is not called a count, because a `NamedTuple` is a tuple and `count` is
a method of every one of them.

<a id="edit_cfg_json.finding.FindReport.place"></a>

#### place

Which of them the search has got to, counting from one.

It is zero where the search is at no node at all, which is a search that
reaches nothing and a search whose node a validation pass has taken away.

<a id="edit_cfg_json.finding.LOOKS_IN_PATH"></a>

#### LOOKS\_IN\_PATH

What looking in the path of a node means, for a user to read.

<a id="edit_cfg_json.finding.LOOKS_IN_VALUE"></a>

#### LOOKS\_IN\_VALUE

What looking in the value of a node means.

<a id="edit_cfg_json.finding.MATCHES_CASE"></a>

#### MATCHES\_CASE

What matching the case means.

<a id="edit_cfg_json.finding.MATCHES_WHOLE"></a>

#### MATCHES\_WHOLE

What matching the whole of one of them means.

<a id="edit_cfg_json.finding.FIND_OPTION_HELP"></a>

#### FIND\_OPTION\_HELP

What each answer of `FindOptions` means, in the order of its members.

It is here rather than in each backend for the reason the type of a member is:
what a piece of the model *means* is the model's to say, and two backends
explaining one control two ways would be explaining two different controls.
What each backend owns is the label on it — one or two characters, since the
width of that row belongs to the field — and where the explanation is put,
which is a tooltip in both toolkits and the only place a label that short has
to say what it is.

<a id="edit_cfg_json.finding.looks_nowhere"></a>

#### looks\_nowhere

```python
def looks_nowhere(options: FindOptions) -> bool
```

Return whether these options leave nothing at all to look in.

A user who unticks both of the places a search looks has asked for
something that can never reach a node, and telling them that no member
matches would be untrue: nothing was compared with anything.

**Arguments**:

- `options` - How the comparison would be made.
  

**Returns**:

  Whether neither the path nor the value is being looked in.

<a id="edit_cfg_json.finding.matched"></a>

#### matched

```python
def matched(rows: Mapping[ConfigPath, MemberRow],
            state: FindState) -> tuple[ConfigPath, ...]
```

Return the path of every node that the search is about, in row order.

**Arguments**:

- `rows` - The rows of the configuration, by path.
- `state` - What is being looked for and how.
  

**Returns**:

  The nodes the text reaches, in the order they are shown, and none at
  all for a search that has not been made or has nowhere to look.

<a id="edit_cfg_json.finding.next_match"></a>

#### next\_match

```python
def next_match(matches: Sequence[ConfigPath],
               reached: Optional[ConfigPath]) -> Optional[ConfigPath]
```

Return the match after one node, wrapping round to the first.

A search that is at no node at all, and one whose node is not a match any
more, both go to the first: that is a search starting from the top, which
is what a new text and a changed option ask for and what is left of a
search whose node a validation pass took away.

**Arguments**:

- `matches` - The nodes the text reaches, in the order they are shown.
- `reached` - Node the search has got to, or None when it is at none.
  

**Returns**:

  The node to go to, and None when the text reaches none.

<a id="edit_cfg_json.finding.find_report"></a>

#### find\_report

```python
def find_report(state: FindState, matches: Sequence[ConfigPath]) -> FindReport
```

Return what the editor says about one search.

**Arguments**:

- `state` - What is being looked for and where the search has got to.
- `matches` - The nodes that text reaches, in the order they are shown.
  

**Returns**:

  What is being looked for, how, how many nodes it reaches and which of
  them the search is at.

<a id="edit_cfg_json.tree"></a>

# edit\_cfg\_json.tree

The shape of the JSON structure that one configuration owns.

A configuration member is not always a value. It may be a list or a dict, and
what is inside it may be a list or a dict again, so what the editor shows is a
tree and not a row per member. This module owns the two operations that make
that tree, and they are inverses of each other: taking the values of one
configuration apart into one entry per node, and putting the edit buffer back
together into the values of one configuration. Where those values come from in
the first place is `member_values`, which is what the object would write.

**A node the file holds no key for has a row all the same.** Two of them do.
`_omit_none_from_json()` names the members a class writes nothing at all for
while they hold nothing, and a `DICT_VALUE_BY_KEY` declaration names a key of
a dict that holds a configuration object and is allowed not to be there. Both
directions therefore differ from the file by exactly those nodes:
`shown_values` and `shown_entries` add them back on the way in, each of them
holding nothing, so that a node with no value has a row to be given one at,
and `file_values` takes them out again on the way to the class, so that what a
validation pass is given is the document a save would write. Giving such a
node a value is what design section 4.9 of `doc/detailed_design.md` calls
adding.

Every node is addressed by a `config_as_json.ConfigPath`, which is what
section 4.2 of `doc/detailed_design.md` asks for: a member inside a list or a
dict needs no second way of naming it, and the description mapping already
names one that way. A list element is addressed by its index written out, which
is what makes `('retry_delays', '0')` a path and lets `('retry_delays', '[')`
describe every element of it.

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

An `OPTIONAL_MEMBER` is what holds none, and it has a row whether its class
writes `null` for it or leaves it out of the file altogether. The row says
which class would be there and that there is nothing there, because both of
those are worth knowing and neither is a value: no text typed into a field
becomes a configuration object, so the row cannot be edited. Making one is
adding, and belongs with adding an element of a list.

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

<a id="edit_cfg_json.tree.member_values"></a>

#### member\_values

```python
def member_values(config: Config, stderr_file: TextIO) -> dict[str, JsonType]
```

Return one JSON space value per serialized member of one object.

This is where the values that the tree is built from come from, and it is
the values the object would write rather than the attributes it holds: the
serialize converters have run, and a nested configuration object has
written itself as the dictionary a file holds it as.

**Arguments**:

- `config` - Configuration object to read. It is not modified, because
  what is read is the text it writes and not the object.
- `stderr_file` - Stream used for user-facing diagnostics.
  

**Returns**:

  The values that this object would write to a file.
  

**Raises**:

- `InvalidConfiguration` - The configuration object is not valid.
- `InvalidConfigurationValue` - A member does not hold a valid value.

<a id="edit_cfg_json.tree.shown_values"></a>

#### shown\_values

```python
def shown_values(config: Config,
                 members: Mapping[str, JsonType]) -> dict[str, JsonType]
```

Return the members of one object, the ones it left out included.

A class writes nothing at all for a member that `_omit_none_from_json()`
names while that member holds nothing, so the values one object writes are
fewer than the members it has. The ones it left out are added back here,
each of them holding nothing, because a member with no row could never be
given a value and giving one a value is what design section 4.9 of
`doc/detailed_design.md` calls adding.

Which members those are is asked of the object rather than of the class:
a member the object holds and did not write is a member it left out, and
that needs no protected name to answer. The declaration is asked for
whether such a member may be left out at all, which is a different
question and is `optional_members` below.

**Arguments**:

- `config` - Configuration object these values belong to. It is not
  modified.
- `members` - One JSON space value per member that object wrote.
  

**Returns**:

  Those values, with nothing at all for every member the object left
  out of them.

<a id="edit_cfg_json.tree.shown_entries"></a>

#### shown\_entries

```python
def shown_entries(path: ConfigPath, value: dict[str, JsonType],
                  named: Iterable[ConfigPath]) -> dict[str, JsonType]
```

Return one dict with the declared keys it does not hold added back.

A `DICT_VALUE_BY_KEY` declaration names one key of a dict that holds a
configuration object, and nothing in `config_as_json` requires the file to
have that key: what it refuses is a declared key holding something other
than an object of the declared class. So such a key is a place that holds
an object or holds nothing, exactly as an `OPTIONAL_MEMBER` is, and it is
added back holding nothing for the reason `shown_values` adds an omitted
member back: a key with no row could never be given an object again, so
taking the object away would be a way of losing it.

The dict is written again in the sorted order of its keys, which is the
order a file holds it in and therefore the order the rows are shown in.

**Arguments**:

- `path` - Path of the dict these values belong to.
- `value` - What that dict holds now.
- `named` - Path of every key that a class declared an object at, anywhere
  in the tree, which `by_key_nestings` answers with.
  

**Returns**:

  Those values, with nothing at all for every declared key of this dict
  that is not among them.

<a id="edit_cfg_json.tree.file_values"></a>

#### file\_values

```python
def file_values(members: Mapping[str, JsonType],
                omitted: frozenset[ConfigPath]) -> dict[str, JsonType]
```

Return the values of one edit buffer as a file would hold them.

It is the inverse of what `shown_values` and `shown_entries` add, and what
it is for is that **what is validated is the document that would be
written**. A save writes the object that a validation pass built, and that
object leaves such a member out, so a pass given `null` for it would be
reaching its verdict about a document that no save of this configuration
produces. A class is free to make something of a key it does not find —
rules for reading an older file are given the keys of the document before
anything else looks at them — so the two documents are not promised to be
read alike, and the one that matters is the one the file will hold.

Every level of the tree is asked, because the class that may leave a
member out is the class that owns it: a nested configuration object reads
its own JSON.

**Arguments**:

- `members` - The edit buffer, as one JSON space value per member.
- `omitted` - Every node that the file holds no key for while it holds
  nothing, by the absolute path of that node, which `omitted_paths`
  answers with.
  

**Returns**:

  The values that a file of this configuration would hold.

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

An `OPTIONAL_MEMBER` is what holds none, and so is a key that a
`DICT_VALUE_BY_KEY` declaration names and the dict does not hold.
Everything the editor asks of a node below this one is asked of this
object, so a node that has none has nothing below it either.

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

<a id="edit_cfg_json.tree.member_nestings"></a>

#### member\_nestings

```python
def member_nestings(
        nodes: Mapping[ConfigPath,
                       ConfigNode]) -> dict[ConfigPath, ConfigNesting]
```

Return what each object of the tree declares about a member of its own.

A declaration is the question a member holding several things is answered
by: a list whose elements are configuration objects can be given another
one, made from the class the declaration names, and a list of plain values
is a different question altogether. `config_nodes` answers where the
objects *are* and this answers what the class *said*, which is what a
member that holds none of them yet has instead.

Only the first declaration of a member is answered with. More than one is
`DICT_VALUE_BY_KEY`, and every one of those says the same thing about the
member that holds them, which is that its keys are not all one kind of
thing. What each of them says about its own key is `by_key_nestings`.

**Arguments**:

- `nodes` - Every configuration object of the tree, by its path.
  

**Returns**:

  One declaration per declared member, under the absolute path of that
  member, which is the path of the object holding it and its own name.

<a id="edit_cfg_json.tree.by_key_nestings"></a>

#### by\_key\_nestings

```python
def by_key_nestings(
        nodes: Mapping[ConfigPath,
                       ConfigNode]) -> dict[ConfigPath, ConfigNesting]
```

Return every key of a dict that a class declared an object at.

`DICT_VALUE_BY_KEY` is the one declaration that is about a key inside a
member rather than about the member itself: the named key holds a
configuration object and every other key of the same dict holds an
ordinary value. One member may name several of them, each with a class of
its own, which is what the list form of `nested_configs()` is for, so this
answers per key where `member_nestings` answers per member.

**Arguments**:

- `nodes` - Every configuration object of the tree, by its path.
  

**Returns**:

  One declaration per declared key, under the absolute path of that key,
  which is the path of the member holding it and the key itself.

<a id="edit_cfg_json.tree.unchecked_members"></a>

#### unchecked\_members

```python
def unchecked_members(
        nodes: Mapping[ConfigPath, ConfigNode]) -> frozenset[ConfigPath]
```

Return every dict member whose keys its own class does not check.

`config_as_json` checks a dict member of a configuration against the keys
the class declares for it, and `_unchecked_dicts` is how a class takes that
check away and defines the key policy with validators of its own instead.
It is read here for the same reason `_omit_none_from_json()` is read: it is
a protected name, nothing else answers the question, and the answer decides
what the editor may offer.

The whole of such a member is unchecked and not only its outermost
dictionary, because the check returns at the member rather than recursing
into it.

**Arguments**:

- `nodes` - Every configuration object of the tree, by its path.
  

**Returns**:

  The absolute path of every member whose keys are the application's own
  to decide.

<a id="edit_cfg_json.tree.optional_members"></a>

#### optional\_members

```python
def optional_members(config: Config) -> frozenset[str]
```

Return the members that one configuration may leave out of a file.

The class is asked, because only the class knows: a member that holds
nothing right now may be one that has to hold something, and one that
holds something may still be allowed to hold nothing. It is a protected
name of `config_as_json` and it is read for the same reason
`_unchecked_dicts` is: nothing else answers the question, section 4.1 of
`doc/detailed_design.md` names it as one of the sources of the structure,
and the answer decides what the editor may offer. It needs no checking
here, because constructing the object checked it.

**Arguments**:

- `config` - Configuration object being edited. It is not modified.
  

**Returns**:

  The names of the members that are genuinely optional.

<a id="edit_cfg_json.tree.optional_paths"></a>

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

<a id="edit_cfg_json.tree.omitted_paths"></a>

#### omitted\_paths

```python
def omitted_paths(
        nodes: Mapping[ConfigPath, ConfigNode]) -> frozenset[ConfigPath]
```

Return every node that a file holds no key for while it holds nothing.

Two kinds of node are: a member that its own class may leave out of the
file, and a key that a class declared a configuration object at, which the
file is free not to have. Both are shown as a row that holds nothing and
both are taken back out on the way to the class, so both are asked for in
one place.

**Arguments**:

- `nodes` - Every configuration object of the tree, by its path.
  

**Returns**:

  The path of every node whose absence from the file is what holding
  nothing means.

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

A member that the class omits from JSON while its value is `None` is not
serialized, and `shown_values` puts it back before this is asked, so it
keeps the place its own declaration gives it. A serialized name that is
not an attribute of the object is appended instead of dropped, so that no
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

A member that the configuration leaves out of the file while it holds
nothing is one of them, at every level of the tree, because it is a member
of that object whether or not the file holds it. So is a key that a class
declared an object at and the file has not got.

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

<a id="edit_cfg_json.exit_code"></a>

# edit\_cfg\_json.exit\_code

What one run of a program of this library ends with.

The numbers are part of what the programs promise, so they are written down in
one place that everything reporting one reads, and `Refusal` is how a refusal
carries its number out to the one place that prints it.

<a id="edit_cfg_json.exit_code.ExitCode"></a>

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

<a id="edit_cfg_json.exit_code.ExitCode.OK"></a>

#### OK

Everything the program was asked to do was done.

<a id="edit_cfg_json.exit_code.ExitCode.LOAD_REFUSED"></a>

#### LOAD\_REFUSED

The input file cannot be opened for editing.

<a id="edit_cfg_json.exit_code.ExitCode.USAGE"></a>

#### USAGE

The command line itself is wrong.

It is `argparse` that reports this and ends the process, so `run_cli`
never returns it. The number is written down here because it is part of
the same promise as the rest, and because the tests compare against it.

<a id="edit_cfg_json.exit_code.ExitCode.NO_MODULE"></a>

#### NO\_MODULE

The module that `--module` names cannot be imported.

<a id="edit_cfg_json.exit_code.ExitCode.NO_FILE"></a>

#### NO\_FILE

The file that `--file` names cannot be read.

<a id="edit_cfg_json.exit_code.ExitCode.NOT_PYTHON"></a>

#### NOT\_PYTHON

The file that `--file` names is not Python that can be imported.

<a id="edit_cfg_json.exit_code.ExitCode.NOT_IMPORTABLE"></a>

#### NOT\_IMPORTABLE

The file needs the package it belongs to in order to be imported.

<a id="edit_cfg_json.exit_code.ExitCode.NO_NAME"></a>

#### NO\_NAME

The module does not hold the name that was asked for.

<a id="edit_cfg_json.exit_code.ExitCode.NOT_CONFIG"></a>

#### NOT\_CONFIG

That name is not a class based on `config_as_json.Config`.

<a id="edit_cfg_json.exit_code.ExitCode.NO_DEFAULTS"></a>

#### NO\_DEFAULTS

The editor cannot construct that configuration class on its own.

<a id="edit_cfg_json.exit_code.ExitCode.INVALID"></a>

#### INVALID

The configuration is not one that the application would accept.

This is what makes a program with no user interface a check that a script
or a continuous integration job can run: a file the application would
refuse is a failure of the run and not merely a remark in the output.

<a id="edit_cfg_json.exit_code.ExitCode.NOT_WRITTEN"></a>

#### NOT\_WRITTEN

The output file was asked for and was not written.

The values were valid, so what stopped the writing is the destination: a
name that was not given at all, one the application does not use for its
configuration, or a file that cannot be written.

<a id="edit_cfg_json.exit_code.ExitCode.NOT_SHOWABLE"></a>

#### NOT\_SHOWABLE

The values of that configuration class cannot be written as JSON.

There is then nothing to edit at all: the editor reads what it shows by
serializing the configuration object.

<a id="edit_cfg_json.exit_code.ExitCode.NOT_LOADER"></a>

#### NOT\_LOADER

The name that `--loader` names cannot be called at all.

<a id="edit_cfg_json.exit_code.ExitCode.LOADER_ARGS"></a>

#### LOADER\_ARGS

The loader needs arguments that a command line cannot supply.

A loader takes the four keyword arguments of `ConfigLoader` and nothing
else, so whatever it needs besides them is bound where it is written. A
program cannot bind an argument it knows nothing about, and saying so
plainly is better than a half answer.

<a id="edit_cfg_json.exit_code.ExitCode.WRONG_CLASS"></a>

#### WRONG\_CLASS

The loader did not construct the class that `--class` asked for.

<a id="edit_cfg_json.exit_code.ExitCode.NOT_DESCRIPTIONS"></a>

#### NOT\_DESCRIPTIONS

The name that `--descriptions` names is no mapping of any kind.

<a id="edit_cfg_json.exit_code.ExitCode.NO_SETTINGS"></a>

#### NO\_SETTINGS

The settings of the program itself cannot be read.

A file that `-c/--cfg` or the environment named is not there, or the file
the lookup found does not hold settings of this editor. Running with other
settings than the ones that were asked for is what this number exists to
stop, because a user who named a settings file wants that one.

<a id="edit_cfg_json.exit_code.Refusal"></a>

## Refusal Objects

```python
class Refusal(Exception)
```

Refusal to run, with what to say about it and what to exit with.

It is internal to this package because it exists only to carry the two
together from wherever the refusal is decided out to the one place that
reports it.

<a id="edit_cfg_json.exit_code.Refusal.__init__"></a>

#### \_\_init\_\_

```python
def __init__(message: str, code: ExitCode) -> None
```

Say why the program cannot run and how it should end.

**Arguments**:

- `message` - What the user has to be told.
- `code` - What this run of the program ends with.

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

The editors this library is for are the Textual one and the Tkinter one, and
each of them lives in a package of its own, because this package imports no
user interface library.

What is here beside the protocol is `DumpEditor`, which is a very limited
non-interactive backend: it prints the model once and returns. It is the one
backend that needs no user interface library at all, which is what makes it
useful for exercising this API without a display and for printing what a short
sequence of editor actions left behind. It is not an editor and is not the way
to see what one does.

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
`doc/detailed_design.md` is where it is designed.

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

A backend that offers the user a way out asks `close_question` on
every one of them before it takes it, because closing writes nothing
and a session that is closed with something in the buffer loses it.
What is asked is the model's to say and how it is asked is the
backend's, which is the same split as everything else here.

**Arguments**:

- `model` - Model to show. The backend reads and edits the model, and
  never touches the caller's configuration object.

<a id="edit_cfg_json.backend.DumpEditor"></a>

## DumpEditor Objects

```python
class DumpEditor()
```

A very limited non-interactive backend: it prints the model once.

It is not one of this library's editors and is not how one is looked at.
The editors are `edit_cfg_json_textual.TextualEditor` and
`edit_cfg_json_tk.TkEditor`, and everything a user does — typing into a
field, leaving one, pressing a control on a row, answering a question —
happens in one of those and in neither this nor any other printout.

What this is good for is the two things a non-interactive backend can do:
exercising a feature over this API without a display, which is what a
quick check, a script and an automated test need, and printing what a
short sequence of editor actions left behind. Those are real uses, and
they are the whole of them.

It satisfies `EditorBackend` and is not a special case beside an
interactive backend, which is worth noticing: the protocol asks for one
method, so anything with that method can be handed to `edit`. That is also
how an application writes a backend of its own, and this is the shortest
one there is to read.

It runs to completion in the sense the protocol asks for, and there is
simply nothing for the user to do while it runs. So whoever runs it has no
later moment at which to press Save, and saving is the caller's to ask
for, before the model is handed over.

For the same reason it asks nothing before it ends. There is no session
for a user to close and nobody to answer a question, so what a session
that ends here does with a buffer that was never saved is settled: it
ends, which is the only thing it could ever have done.

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

An interactive backend does the opposite and waits to be asked, with a
button or a key, because a user halfway through typing a value has not
asked anything. Validating here is the consequence of having no later
moment to be asked in, and not a different opinion about when a buffer
should be validated.

**Arguments**:

- `model` - Model to print.

<a id="edit_cfg_json.editing"></a>

# edit\_cfg\_json.editing

One editing session, from the input file to what was saved.

`editor_model` reads the input file and returns the model of one session.
`edit` is that model run in a backend that owns a window, and the embedding
entry points of the two backend packages are that model mounted in a window
an application owns. All three take the same few keywords, so an application
says the same things about a session however it opens the editor.

<a id="edit_cfg_json.editing.editor_model"></a>

#### editor\_model

```python
def editor_model(config: Config,
                 *,
                 descriptions: Optional[Descriptions] = None,
                 in_file: Optional[PathOrStr] = None,
                 loader: Optional[ConfigLoader] = None,
                 out_file: Optional[PathOrStr] = None,
                 policy: LoadPolicy = DEFAULT_POLICY,
                 settings: SettingsSource = Settings(),
                 stderr_file: TextIO = sys.stderr) -> EditModel
```

Read one configuration from a file and return the model to edit it.

**Arguments**:

- `config` - Configuration object saying which class to edit and what its
  declared defaults are. It is never modified.
- `descriptions` - What the application says about the members it
  declares, or None when it says nothing.
- `in_file` - File to read, or None to start from the declared defaults.
- `loader` - How this application constructs its configuration, or None for
  a class the editor can construct from the signature it declares.
- `out_file` - File to write, or None to write the input file.
- `policy` - What to do about declared keys the input file does not hold.
- `settings` - What the application around the editor has already decided,
  or a callable that answers with it.
- `stderr_file` - Stream used for user-facing diagnostics.
  

**Returns**:

  The model of one editing session, ready to be shown.
  

**Raises**:

- `ConfigLoadError` - The input file cannot be opened for editing.

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
an application that has already chosen its user interface. An application
that already runs that user interface mounts the editor instead, with the
entry point of its backend package, and `editor_model` is what those two
ways of opening the editor have in common.

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

<a id="edit_cfg_json.elements"></a>

# edit\_cfg\_json.elements

What a container offers, and what adding or removing an element does.

A member that holds several of something is not finished when its values can
be edited. A list of report outputs is a list because the number of them is a
decision of whoever configures the application, so an editor that could change
every one of them and add none would be refusing the decision the shape of the
member exists to allow.

**A new element is copied and never invented.** Where the class declares that
every element of a list or every value of a dict is a configuration object,
the declaration says which class to make one of, and one of that class holding
its own declared values is what a new element is. Where it declares nothing,
the values the class declares for the member itself are the pattern: the first
element of them, and failing that the first element the member holds now. A
member that has neither is a member the editor has nothing to copy for, and it
says so rather than inventing a value that the application never mentioned.

**What cannot be done is said and not left to be discovered.** A dict whose
keys are the ones its class declares cannot gain or lose one at all —
`config_as_json` checks a dict against those keys while it parses — so that is
a sentence below that dict, in the same place and under the same toggle as
everything else explanatory.

**Which dicts those are is a question about where the dict sits.**
`Config.check_dict_parse` is applied once per member and recurses from there
into the dict values of that member, so it reaches a dict only where it was
applied to the member at all and where every step down was into a dict. Three
things stop it, and `_holds_elements` is where all three are asked: a member
named in `nested_configs()`, which `config_as_json` reads whole instead; a
member named in `_unchecked_dicts`, whose key policy the class defines with
validators of its own; and a list between the member and the dict, which the
recursion cannot step into. A dict the check does not reach is an ordinary
container here, and what the application's own validators make of a new key is
the ordinary verdict.

**A member whose values are of two kinds is asked twice.** A
`DICT_VALUE_BY_KEY` declaration names one key of a dict that holds a
configuration object, and every other key of that dict holds an ordinary
value. Nothing checks which keys such a member has, nor which keys anything
inside it has, because the check above is never applied to it at all, so both
halves of it are answerable: the named key is a place that holds an object or
holds nothing, and the rest of the dict is an ordinary container whose new
entry is copied from what its own entries look like.

**Where an object is added, an object is made.** `placing` is where that
happens, because the model's own configuration object gains and loses the real
objects as the buffer gains and loses their values.

**How a member is written is not what decides whether it can be cleared.** A
member the class leaves out of the file while it holds nothing has a row all
the same, which `tree.shown_values` gives it, and so has a named key the dict
has not got, which `tree.shown_entries` gives it; putting either of them back
to holding nothing is therefore not a way of losing it. What the class does
decide is what a value of it would be: a declared object for a place that
holds one, and the emptiest value of its kind for a member declared to allow
no value.

<a id="edit_cfg_json.elements.BUILD_ERRORS"></a>

#### BUILD\_ERRORS

Every way in which constructing a configuration class can fail.

A class that needs a constructor argument this library knows nothing about
raises `TypeError`, one that declares no public member raises `AttributeError`,
and declared values that a validator refuses raise a `ValueError` subclass.
`NotImplementedError` is deliberately not one of them, for the same reason as
in the validation of a buffer: it says the configuration class is incomplete,
which is a defect of the application that no editing can put right.

<a id="edit_cfg_json.elements.CLEARED_KINDS"></a>

#### CLEARED\_KINDS

The declarations of a place that holds one object or holds nothing.

They are the two that have the pair of states of design section 4.9 of
`doc/detailed_design.md`: a member that may hold none, and a named key that the
file need not have. `MEMBER` holds one always, and `LIST_ELEMENT` and
`DICT_VALUE` are about everything inside a member rather than about one place
in it.

<a id="edit_cfg_json.elements.NO_PATTERN"></a>

#### NO\_PATTERN

What a list nothing says anything about says instead of growing.

It is the one case that design section 11 of `doc/detailed_design.md` puts out
of scope for good rather than for now, because the missing thing cannot be
supplied by any amount of work here: only the application knows what an element
of its own list looks like, and a member it never gave one for and never
declared a type for has never said. A member with an ordinary annotation is
answered by that annotation and never reaches this.

<a id="edit_cfg_json.elements.NO_CLASS_FORM"></a>

#### NO\_CLASS\_FORM

What a container of objects says when their class cannot be constructed.

`config_as_json` asks a nested class for the constructor that it builds one
with while it parses, so this is a class that could not be read from a file
either. It is said here rather than found out when the control is pressed,
because a control that refuses every press is worse than no control.

<a id="edit_cfg_json.elements.FIXED_KEYS"></a>

#### FIXED\_KEYS

What a dict the declared-keys check reaches says instead of growing.

`Config.check_dict_parse` matches such a dict against the keys the class
declares for it, so one that gained or lost a key would be refused by
`config_as_json` itself on the next validation pass. The editor says so rather
than offering a control that produces a refusal. Which dicts the check reaches
is `_holds_elements`, and a dict it does not reach is offered the entry
instead of this sentence.

<a id="edit_cfg_json.elements.BY_KEY_PATTERN"></a>

#### BY\_KEY\_PATTERN

What a dict with named objects in it says instead of gaining a key.

It is `NO_PATTERN` for the half of such a member that is not declared: the
declared keys of it are answered by the class each of them names, and every
other key holds an ordinary value that only the application can have said
anything about. A member that says this can still be given the objects its
declarations name, at the row of each of those keys.

<a id="edit_cfg_json.elements.NO_DICT_YET"></a>

#### NO\_DICT\_YET

What a member declared to allow no value says instead of taking a dict.

`Config.check_dict_parse` refuses a dict written for a member whose value is
not one — *Unexpected dictionary for X in JSON data* — whatever keys it has and
even where it has none, so the empty dict of design section 4.2 of
`doc/detailed_design.md` is the one kind of value that such a member cannot be
given. It is the first bullet of section 4.9 one step up: what refuses a dict
here is the same check that refuses a new key of one, and offering the control
anyway would be offering one that produces a refusal.

<a id="edit_cfg_json.elements.NO_ENTRY_PATTERN"></a>

#### NO\_ENTRY\_PATTERN

What a dict whose keys nothing checks says instead of gaining one.

It is `NO_PATTERN` for a dict, and it is reached by every dict the
declared-keys check does not reach and that has no declared key of its own:
the keys of such a dict are the application's own to decide, so the editor
offers an entry as soon as anything says what one would hold, and says this
where nothing does. `BY_KEY_PATTERN` is the same sentence for a member that
has declared keys beside the entries.

<a id="edit_cfg_json.elements.NOT_EXTENDABLE"></a>

#### NOT\_EXTENDABLE

Message of the error raised when a node that offers no element is grown.

<a id="edit_cfg_json.elements.NOT_REMOVABLE"></a>

#### NOT\_REMOVABLE

Message of the error raised when a node that is no element is removed.

<a id="edit_cfg_json.elements.NOT_MOVABLE"></a>

#### NOT\_MOVABLE

Message of the error raised when a node that is no element is moved.

<a id="edit_cfg_json.elements.KEY_NEEDED"></a>

#### KEY\_NEEDED

Message of the error raised when a dict is grown without a key.

<a id="edit_cfg_json.elements.KEY_UNWANTED"></a>

#### KEY\_UNWANTED

Message of the error raised when a list is grown with a key.

<a id="edit_cfg_json.elements.KEY_TAKEN"></a>

#### KEY\_TAKEN

Message of the error raised when a new key is one the dict has.

<a id="edit_cfg_json.elements.ElementOffer"></a>

## ElementOffer Objects

```python
class ElementOffer(NamedTuple)
```

What one node of the tree offers to do with the elements it holds.

It is one object rather than one attribute each on the row, because the
five of them are read together and answer one question between them: what
can be done here about how many things there are.

A backend reads it to decide which controls one row gets, and creates none
where nothing is offered: there is no column to keep clear, because these
controls sit at the end of the line where a row without them needs no
space held for it.

<a id="edit_cfg_json.elements.ElementOffer.extend"></a>

#### extend

Whether an element can be added here.

It is true for a list that something can be copied for, for a dict whose
class says that every value in it is a configuration object, for a dict
where one named key of it does and something can be copied for the rest,
and for a declared place that holds no object yet, where adding is making
the one object that place is for.

<a id="edit_cfg_json.elements.ElementOffer.keyed"></a>

#### keyed

Whether adding here needs a key that only the user can give.

A new entry of a dict has to be called something, and nothing but the
person configuring the application knows what. The two backends ask, each
in the way its own toolkit asks a question, and a list is never keyed
because an element of a list is addressed by where it is.

<a id="edit_cfg_json.elements.ElementOffer.remove"></a>

#### remove

Whether removing this node is something the user may ask for.

An element of a list and an entry of a dict whose keys its class does not
check can be taken out of what holds them. A declared place that holds an
object, and a member that its class declared to allow no value, are put
back to holding nothing instead, which `cleared` is what says. How the
class writes such a member is not asked: one it leaves out of the file
altogether keeps its row, which says that it holds nothing and offers to
give it something.

<a id="edit_cfg_json.elements.ElementOffer.cleared"></a>

#### cleared

Whether removing puts this node back to holding nothing.

The two ways of removing something differ in what is left behind, and the
difference is not visible in the row: a declared place keeps its row and
holds nothing, and an element of a container is gone. A declared key of a
dict is the case that needs both to be said, because it is a place that
keeps its row while being one key of a container beside the ordinary keys
that are taken out of it.

<a id="edit_cfg_json.elements.ElementOffer.earlier"></a>

#### earlier

Whether this element can change places with the one before it.

<a id="edit_cfg_json.elements.ElementOffer.later"></a>

#### later

Whether this element can change places with the one after it.

The order of a list is part of what the file says, so it is part of what
an editor of that file has to be able to change. A dict has no such
question: it is written in the sorted order of its keys, so where an entry
is shown follows from what it is called.

<a id="edit_cfg_json.elements.ElementOffer.refusal"></a>

#### refusal

Why nothing can be added here, empty where something can.

It is empty for every node that is no container as well, because a value
that holds nothing is not a member somebody expected to be able to grow.
It is explanatory text and is shown with the explanations, below the
member it is about, rather than as something to act on: it says what this
member is, in the same way as the line saying what kind of value a member
holds.

<a id="edit_cfg_json.elements.ElementOffer.template"></a>

#### template

What a new element here would hold, None where none can be added.

It is kept with the offer because it is the same answer: what can be added
is exactly what there is something to copy. A backend never reads it, and
the buffer copies it rather than using it, since a list and a dict are
values that the next edit would otherwise reach through both of them.

<a id="edit_cfg_json.elements.TreeFacts"></a>

## TreeFacts Objects

```python
class TreeFacts(NamedTuple)
```

Everything that saying what one tree offers needs.

It is one object rather than one argument each, because every one of them
is read once per node and none of them changes while the offers are made.

<a id="edit_cfg_json.elements.TreeFacts.values"></a>

#### values

The value of every node of the tree, by its path.

<a id="edit_cfg_json.elements.TreeFacts.nodes"></a>

#### nodes

Every configuration object of the tree, by its path.

<a id="edit_cfg_json.elements.TreeFacts.nestings"></a>

#### nestings

What each object declares about a member of its own, by that path.

<a id="edit_cfg_json.elements.TreeFacts.by_key"></a>

#### by\_key

What each object declares about one key of a dict, by that path.

It is the declaration that is about a key inside a member rather than
about the member itself, so it is asked for by the path of that key and
the mapping above answers for the member holding it.

<a id="edit_cfg_json.elements.TreeFacts.unchecked"></a>

#### unchecked

Every dict member whose keys its own class does not check.

<a id="edit_cfg_json.elements.TreeFacts.types"></a>

#### types

What the class owning each node says the value there is.

It is what a member allowed to hold nothing is known by, and what says
what an element of a list its class declares empty would be.

<a id="edit_cfg_json.elements.TreeFacts.defaults"></a>

#### defaults

The values that the class of the configuration declares.

They are what a new element of an ordinary list is copied from, and they
are empty for a class the editor could not construct at all, which costs
that configuration the offer and nothing else.

<a id="edit_cfg_json.elements.TreeFacts.made"></a>

#### made

What one of each declared class holds, once it has been made.

The offers are worked out again whenever the rows are, so a class that is
declared in three places would otherwise be constructed three times per
rebuild. None is a class that could not be constructed at all.

<a id="edit_cfg_json.elements.declared_values"></a>

#### declared\_values

```python
def declared_values(source: ConfigSource,
                    stream: TextIO) -> dict[str, JsonType]
```

Return the values that the class of one session declares.

They are asked for through the loader of the application where there is
one, because that is what the loader protocol promises to answer with when
it is given no JSON source, and a class that needs a constructor argument
this library knows nothing about is reached no other way.

A class that cannot be constructed answers with nothing, which is principle
4 of section 3 of `doc/detailed_design.md`: what the editor cannot find out
it does without, and here that costs the offer to grow an ordinary list and
nothing else.

**Arguments**:

- `source` - The configuration of this session and how it is constructed.
- `stream` - Stream that collects what the construction says.
  

**Returns**:

  One JSON space value per declared member, and nothing at all for a
  class the editor could not construct.

<a id="edit_cfg_json.elements.tree_facts"></a>

#### tree\_facts

```python
def tree_facts(nodes: Mapping[ConfigPath, ConfigNode],
               flat: Sequence[tuple[ConfigPath, JsonType]],
               defaults: Mapping[str, JsonType]) -> TreeFacts
```

Return everything that saying what one tree offers needs.

**Arguments**:

- `nodes` - Every configuration object of the tree, by its path.
- `flat` - The path and the value of every node, in row order.
- `defaults` - The values that the class of the configuration declares.
  

**Returns**:

  The facts that one offer per node is made from.

<a id="edit_cfg_json.elements.element_offers"></a>

#### element\_offers

```python
def element_offers(facts: TreeFacts) -> dict[ConfigPath, ElementOffer]
```

Return what every node of one tree offers, by the path of that node.

**Arguments**:

- `facts` - What the tree is, and what its class declares.
  

**Returns**:

  One offer per node, most of them offering nothing at all: a value is
  not something that holds elements, and neither is a node of a
  configuration object, whose members are the ones its class declares.

<a id="edit_cfg_json.elements.grown"></a>

#### grown

```python
def grown(value: JsonType, key: str, template: JsonType) -> JsonType
```

Return one container with one more element in it.

A list grows at the end, because that is where a new element is put when
nothing says otherwise, and it can be moved from there. A dict is written
again in the sorted order of its keys, which is the order a file holds it
in and therefore the order the rows are shown in.

**Arguments**:

- `value` - Value of the container as it is now.
- `key` - Name of the new entry of a dict, empty for a list.
- `template` - What the new element holds, which is copied rather than
  used, so that editing it cannot reach whatever it came from.
  

**Returns**:

  That container with the new element in it.

<a id="edit_cfg_json.elements.shrunk"></a>

#### shrunk

```python
def shrunk(value: JsonType, step: str) -> JsonType
```

Return one container with one element taken out of it.

**Arguments**:

- `value` - Value of the container as it is now.
- `step` - Last step of the path of the element, which is the index of a
  list element written out or the key of a dictionary entry.
  

**Returns**:

  That container without that element.

<a id="edit_cfg_json.elements.swapped"></a>

#### swapped

```python
def swapped(value: JsonType, index: int, later: bool) -> JsonType
```

Return one list with one element in the place of a neighbour.

**Arguments**:

- `value` - Value of the list as it is now.
- `index` - Where the element to move is now.
- `later` - Whether it changes places with the one after it rather than
  with the one before it.
  

**Returns**:

  That list in its new order.

<a id="edit_cfg_json.elements.moved_paths"></a>

#### moved\_paths

```python
def moved_paths(paths: Iterable[ConfigPath], container: ConfigPath,
                order: Sequence[int]) -> dict[ConfigPath, ConfigPath]
```

Return where each node under one list goes when its order changes.

Everything the editor holds about a node is held under the path of that
node — what it is compared against, whether its container is folded, what
the object at it said about itself — and an element of a list is addressed
by where it is. So a change to how many elements there are, or to the order
of them, moves all of that along with the values.

Without it a removal would leave every element after it comparing itself
with the element that used to be there, and would report every one of them
as edited by a user who touched none of them.

**Arguments**:

- `paths` - Path of every node there is.
- `container` - Path of the list whose elements have moved.
- `order` - The index each element of the new list had in the old one, one
  entry per element the list holds now.
  

**Returns**:

  The new path of every node whose path has changed, by its old path.
  An element that stayed where it was is not in it, and neither is one
  that has gone.

<a id="edit_cfg_json.elements.kept_order"></a>

#### kept\_order

```python
def kept_order(count: int, without: int) -> list[int]
```

Return the order of one list with one element taken out of it.

<a id="edit_cfg_json.elements.checked_key"></a>

#### checked\_key

```python
def checked_key(offer: ElementOffer, value: JsonType, key: str,
                path: ConfigPath) -> None
```

Refuse a key that cannot name the new element of one container.

**Arguments**:

- `offer` - What that container offers, which says whether it is keyed.
- `value` - Value of the container as it is now.
- `key` - Name that the new entry was asked to have.
- `path` - Path of the container, for the message.
  

**Raises**:

- `ValueError` - A list was given a key, a dict was given none, or the key
  is one that dict already holds. The last of those is a refusal and
  not a replacement: a new entry that quietly overwrote an existing
  one would lose what the user had.

<a id="edit_cfg_json.elements.refused"></a>

#### refused

```python
def refused(offered: bool, form: str, path: ConfigPath) -> None
```

Raise the refusal of one change that a node does not offer.

**Arguments**:

- `offered` - Whether the node offers it after all.
- `form` - Form of the message that says it does not.
- `path` - Path of the node that was asked.
  

**Raises**:

- `ValueError` - The node does not offer that change.

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

A file that is about to be overwritten is kept first, under the name the
application chose for it, so that a session which writes over a configuration
somebody else wrote does not take it away from them. It is kept once per
destination per session: the file that a user is overwriting is their own
earlier save from the second press of Save onwards, and a backup of every
press would be a backup of nothing.

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

<a id="edit_cfg_json.saving.BACKUP_FAILED"></a>

#### BACKUP\_FAILED

Message of a save that could not keep what the destination held.

Such a save writes nothing. The whole reason for keeping the previous content
is that overwriting it cannot be undone, so a save that has just found it
cannot keep it is the last moment at which anything can be done about that.

<a id="edit_cfg_json.saving.SAVED"></a>

#### SAVED

Message of a save that wrote the output file.

<a id="edit_cfg_json.saving.KEPT_FORM"></a>

#### KEPT\_FORM

What is added to the message of a save that kept what the file held.

It is said on the way out as well as on the way in: a save that kept the
previous content and then could not write the file has left it under another
name, and a user who was not told would look for it where it no longer is.

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

<a id="edit_cfg_json.saving.SaveState.written_files"></a>

#### written\_files

Every destination that this session has already written.

What a save keeps and what it asks about is what the file held before this
session reached it, so a destination that is in here is written straight
over: what would be kept is the user's own earlier save, and what would be
asked about is a file the user made a minute ago.

<a id="edit_cfg_json.saving.KeptFile"></a>

## KeptFile Objects

```python
class KeptFile(NamedTuple)
```

What keeping what one destination holds now did.

<a id="edit_cfg_json.saving.KeptFile.name"></a>

#### name

Where the previous content went, None when there was none to keep.

<a id="edit_cfg_json.saving.KeptFile.message"></a>

#### message

Why it could not be kept, empty when there was nothing in the way.

<a id="edit_cfg_json.saving.NOTHING_KEPT"></a>

#### NOTHING\_KEPT

The answer of a save that had nothing to keep, or was not to keep it.

<a id="edit_cfg_json.saving.kept_file"></a>

#### kept\_file

```python
def kept_file(name: PathOrStr, settings: Settings) -> Optional[Path]
```

Return where what one destination holds now would be kept.

**Arguments**:

- `name` - File that a save is about to write.
- `settings` - What the application has decided about its files.
  

**Returns**:

  The file that the previous content would be kept as, and None where
  there would be none: an application that keeps no backup, and a
  destination that holds no file to keep. A destination that is not a
  file at all, a folder being the case that arises, is left to the
  write to refuse in its own words.

<a id="edit_cfg_json.saving.keep_previous"></a>

#### keep\_previous

```python
def keep_previous(name: PathOrStr, settings: Settings) -> KeptFile
```

Move what one destination holds now out of the way of a save.

By renaming and not by copying, so that what is kept is the file that was
there rather than a second reading of it, and so that a failure leaves the
previous content whole under one name or the other. A kept file of the
same name is replaced, which is how the oldest of several falls off the
end.

Whether a destination is to be kept at all is the caller's question, and
the model answers it: a file this session has already written is the
user's own earlier save.

**Arguments**:

- `name` - File that a save is about to write.
- `settings` - What the application has decided about its files.
  

**Returns**:

  Where the previous content went, or why it could not be kept.

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
def write_config(config: Config,
                 out_file: PathOrStr,
                 kept: Optional[PathOrStr] = None) -> SaveOutcome
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
- `kept` - File that what this destination held was kept as, or None when
  there was nothing to keep. It is said whether the write succeeds
  or fails, because a user whose file has been moved has to be told
  where it went either way.
  

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

<a id="edit_cfg_json.converting.NOT_A_BOOL_FORM"></a>

#### NOT\_A\_BOOL\_FORM

Why the text of a member holding true or false means neither of them.

It is worded as `config_as_json` words the same refusal about the name of an
enum member, because it is the same refusal: the member holds one of a known
set of values and the text names none of them. Such a member has no parse
converter to answer it — there is nothing to convert true into — so this is
the one refusal of a leaf that the editor makes itself, and it makes it about
the type of the member and never about a rule of the application.

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
                   value: JsonType,
                   is_bool_member: bool = False) -> Converted
```

Return one leaf value as its member holds it, or why it cannot.

A value that already has the type the converter produces is left alone,
and so is a value that is `None`: a member that its class leaves out of
JSON while it is None has nothing to convert, and a `None` that is wrong
is refused by the validation of the whole configuration, which has a
message of its own for it.

A member holding true or false is answered without a converter, because
it has none and needs none: `text_as_value` has already made the value of
every text that means one of the two words, so a value that is neither
means neither and is refused here as an enum member name that names no
member is.

**Arguments**:

- `converter` - How the text of this member becomes a value, or None for a
  member that holds what the file holds.
- `value` - JSON space value that the buffer holds for that member.
- `is_bool_member` - Whether this member held true or false when the file
  was last agreed with, which is what makes those the two values it
  takes.
  

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

<a id="edit_cfg_json.dump"></a>

# edit\_cfg\_json.dump

A small utility for whoever is writing a program on top of this package.

It runs `DumpEditor` over the command line of `edit_cfg_json.cli`, so it needs
no display: it prints what a configuration class makes of a file, with what
the application's own validators say about the values, and with `--save` it
writes the validated file. That is worth having while a program of one's own
is being written, and it is worth having in a continuous integration job,
where an exit code is the whole of what can be read.

**It is no editor, and the editors are `edit-cfg-json-tk` and
`edit-cfg-json-textual`.** They take the very same command line and open a
window and a terminal screen. This utility has no field to type into and
nobody to press Save, which is why it is the one of the three that offers
`--save` at all.

`--unfold` is there for the same reason. A container that would flood a window
opens folded, so a printout of a configuration of any size is mostly a line
saying that it holds more, and there is no control here to open it with. With
`--unfold` every container is open and stays open, which is what says what this
library makes of a whole configuration: every value of it, and the explanation
that every one of its nodes is shown with.

**It reads a settings file of its own, and has no file in the home folder.**
`-c/--cfg` and the environment variable name one, and the shared
`.edit-cfg-json.cfg` is the last thing looked for; the step between those two
is skipped, because that step is there to let the two editors differ and what
they differ about is their keys and their questions, of which this has neither.
What a settings file still says here is what a file is called and what happens
to the one a save writes over.

Run it as `python3 -m edit_cfg_json.dump`. This package installs no command of
its own, and the name `edit-cfg-json` in particular is deliberately free: it
promises the editor this library is for, and a user who typed it and got a
printout would have been misled by the name rather than by anything the
program did.

<a id="edit_cfg_json.dump.PROGRAM"></a>

#### PROGRAM

How this program is run, which is what its own help text says.

<a id="edit_cfg_json.dump.main"></a>

#### main

```python
def main(args: Optional[Sequence[str]] = None) -> int
```

Run this program and return what it ends with.

**Arguments**:

- `args` - Optional replacement for `sys.argv[1:]`, mainly for tests.
  

**Returns**:

  What this run ends with, as one of `edit_cfg_json.ExitCode`.

<a id="edit_cfg_json.member_types"></a>

# edit\_cfg\_json.member\_types

What the class of a configuration says the type of each member is.

The value a member held when the file was last agreed with says a great deal
about it, and there are two things it cannot say. A member that holds nothing
says nothing at all about what it would hold, and a member declared `float`
whose default is written `0` says the wrong thing. Both are answered by the
declaration, which is what this module reads.

**Three sources, in order of authority.** A class built on the dataclass
pattern, and any class with class level annotations, records real types that
`typing.get_type_hints` answers with. The ordinary `Config` pattern records
nothing at all: `self.answer: int = 42` inside `__init__` is a PEP 526
annotation on an instance attribute, and Python keeps it nowhere, so the
source of the class is read and its annotations are taken from there.
Where neither answers, the value is still what says the kind, exactly as
before, and that is what makes every one of these optional: a class whose
source cannot be read costs the editor what a declaration would have added
and nothing else.

**Nothing here is evaluated by this module.** An annotation read from source
is a text, and the text is given to `inspect.get_annotations`, which is the
standard library's own resolver for one — the same resolution
`typing.get_type_hints` does, in the namespace of the module that class was
written in. One annotation that will not resolve costs that member its
declaration and leaves every other member of the class alone.

**What is made of the answer is deliberately little.** An annotation says one
of the kinds of `leaf_value`, or it says nothing this editor can use. A class
of the application's own is nothing it can use: what the editor does with a
kind is say what it is and make an empty one of it, and it can do neither with
a class it has never seen. Where the member holds a nested configuration
object, the object itself is what answers (section 4.1 of
`doc/detailed_design.md`), and where it holds an enum, the parse converter of
the class answers.

<a id="edit_cfg_json.member_types.SELF_NAME"></a>

#### SELF\_NAME

What the first argument of a method is called, by every convention.

<a id="edit_cfg_json.member_types.SOURCE_ERRORS"></a>

#### SOURCE\_ERRORS

Every way in which the source of one method can fail to be read.

`inspect.getsource` raises `OSError` for a class defined where there is no
source to read — an interactive session, `exec`, and a frozen program are the
three — and `TypeError` for an object it cannot take source from at all.
Parsing what it did read is what raises the other two.

<a id="edit_cfg_json.member_types.HINT_ERRORS"></a>

#### HINT\_ERRORS

Every way in which one annotation can fail to say what it means.

A name that is not in the namespace of its own module is the ordinary one, and
it arises for real: a name imported under `if TYPE_CHECKING` exists while the
type checker reads the file and never at runtime. An annotation that fails
costs that member its declaration and nothing else.

<a id="edit_cfg_json.member_types.attribute_texts"></a>

#### attribute\_texts

```python
def attribute_texts(described: type[object]) -> dict[str, str]
```

Return the annotation of every attribute one class sets on `self`.

The whole of the class is read and not only its `__init__`, because a
class is free to declare its members in a method of its own that
`__init__` calls, and the annotations are just as real there. Only the
source this class writes itself: a class further up is asked in its own
right, and its own module is where the names of its annotations mean
something.

**Arguments**:

- `described` - Class to read the source of.
  

**Returns**:

  One annotation per annotated attribute of `self`, as the text it is
  written as, and nothing at all for a class whose source cannot be
  read.

<a id="edit_cfg_json.member_types.declared_hints"></a>

#### declared\_hints

```python
def declared_hints(described: type[object]) -> dict[str, object]
```

Return what every declaration of one class says its members are.

The bases are walked from the top down, so a class that annotates a member
its base also annotates is the one that answers for it, which is what
Python itself does with the value.

**Arguments**:

- `described` - Class of the configuration object being asked.
  

**Returns**:

  One annotation per member that has one, as what it means.

<a id="edit_cfg_json.member_types.leaf_type"></a>

#### leaf\_type

```python
def leaf_type(hint: object) -> LeafType
```

Return what one annotation says about the value it is about.

**Arguments**:

- `hint` - What one annotation means.
  

**Returns**:

  What that says about the value, which is empty for an annotation
  naming anything the editor cannot make a value of.

<a id="edit_cfg_json.member_types.member_types"></a>

#### member\_types

```python
def member_types(described: type[object]) -> dict[str, LeafType]
```

Return what one class says about the type of each member it declares.

**Arguments**:

- `described` - Class of the configuration object being asked.
  

**Returns**:

  One answer per member whose declaration says anything, by the name of
  that member. A private attribute is never one, because a member of a
  configuration is a public attribute of it.

<a id="edit_cfg_json.member_types.node_types"></a>

#### node\_types

```python
def node_types(
        nodes: Mapping[ConfigPath, ConfigNode],
        flat: Sequence[tuple[ConfigPath,
                             JsonType]]) -> dict[ConfigPath, LeafType]
```

Return what the classes of one tree say about each node of it.

**Arguments**:

- `nodes` - Every configuration object of the tree, by its path.
- `flat` - The path and the value of every node, in row order.
  

**Returns**:

  One answer per node whose declaration says anything, by the path of
  that node.

<a id="edit_cfg_json.cli"></a>

# edit\_cfg\_json.cli

The command line of a program that edits any configuration class.

An application author should get an editor for their own configuration class
without writing a line of user interface code, and every one of the three
distributions therefore ships a program. What differs between the three
programs is the backend and nothing else, so everything else lives here: the
parsing, one editing session and the exit code. Each package is then a program
of a few statements, which is also what makes this testable with no display and
no toolkit, by handing `run_cli` a backend that is a stub.

`run_cli` takes the backend for exactly the reason `edit` does: this package
never imports a user interface library, so it cannot name one.

**Where the class comes from is `edit_cfg_json.cli_target`**, which owns the
three doors to it — an importable module, a Python file, and this library's own
settings class — and the class, the loader and the descriptions that are named
inside the first two. What every one of them ends with is a `Target`, so this
module is about a session and not about where its configuration came from.

**What settings the program itself runs with is a different question**, and
`-c/--cfg` is the first of the five answers that
`edit_cfg_json.settings_file` gives to it. The settings of a program are read
before anything else the command line names, because they are what the whole
run behaves according to.

**It is also the only option about them.** A command line here says what to
edit and which files, and never how the editor behaves: every setting there is
is a member of `edit_cfg_json.SettingsConfig`, so an option for one of them
would be a second way of saying what a settings file says, inside one run, with
nothing to decide which of the two wins. A run that wants other settings names
another file, and one that wants the defaults of the editor names a file that
says nothing.

**`--version` is a fourth thing a run does instead of editing**, so it is an
alternative to the three doors above rather than an option beside them, and it
answers before anything else the command line names is looked at. What it
answers with is each program's own `versionreporter.VersionReporter`, which is
the third thing a program supplies for itself: the backend is what shows a
model, the name is what its help text says, and the reporter is the
distribution it was installed from.

<a id="edit_cfg_json.cli.DESCRIPTION"></a>

#### DESCRIPTION

What the program says about itself above its own options.

<a id="edit_cfg_json.cli.POLICY_NAMES"></a>

#### POLICY\_NAMES

What a `--policy` value on a command line means to the editor.

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
            version_reporter: VersionReporter,
            args: Optional[Sequence[str]] = None,
            interactive: bool = True,
            home_settings: Optional[str] = None) -> int
```

Run one program of this library from the command line.

This is the whole of what each of the three programs does. The backend and
the reporter are what differ between them, and everything that could be
written twice is therefore here.

**Arguments**:

- `backend` - User interface to run the session in. Each package supplies
  its own, which is the one user interface this package cannot name.
- `prog` - Name that this program is installed under, used in its help and
  in its refusals.
- `version_reporter` - What `--version` is answered with. Each program
  supplies the one of its own distribution, because what a report is
  about is the package the program was installed from.
- `args` - Optional replacement for `sys.argv[1:]`, mainly for tests.
- `interactive` - Whether this backend gives the user a session. A backend
  that prints once and returns does not, so its program offers
  `--save` and `--unfold` and answers with the verdict in its exit
  code, because there is nobody to press Save, nobody to open a
  container that is folded away and nobody to read a verdict.
- `home_settings` - Name of this program's own settings file in the home
  folder, which is the third step of the lookup that
  `edit_cfg_json.settings_file` makes. None is a program that has
  none of its own and reads the shared file or nothing.
  

**Returns**:

  What this run of the program ends with, as one of `ExitCode`.
  

**Raises**:

- `SystemExit` - The command line itself is wrong, or help was asked for.
  That is `argparse` reporting it, with `ExitCode.USAGE`.

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

<a id="edit_cfg_json.leaf_value.LIST_KIND"></a>

#### LIST\_KIND

What is said about a member that holds a list and holds none now.

A member that really holds one says nothing here, because its row already says
how many elements there are. It is only worth saying where the row says that
the member holds nothing at all, which is where the kind of the value comes
from the declaration and not from a value.

<a id="edit_cfg_json.leaf_value.DICT_KIND"></a>

#### DICT\_KIND

The same for a member that holds a dict and holds none now.

<a id="edit_cfg_json.leaf_value.VALUE_KINDS"></a>

#### VALUE\_KINDS

What each kind of leaf value is called, in the order they are asked.

The order is what makes `True` say what it is: `bool` is a subclass of `int` in
Python, so a value that is asked in the other order would be a whole number.
Nothing else here depends on the order.

<a id="edit_cfg_json.leaf_value.EMPTY_VALUES"></a>

#### EMPTY\_VALUES

What a value of each kind is before anything has been put into it.

It is what a member that holds nothing is given when the user asks for it to
hold something, and what an element of a list that the class declares empty
is. Nothing here is invented about the *application*: the kind is what the
class declared, and the value is the one value of that kind that says nothing
more than which kind it is.

<a id="edit_cfg_json.leaf_value.NO_KIND"></a>

#### NO\_KIND

What is said about a member whose kind nothing says.

The kind of a member is what the class declared for it, and failing that the
kind of the value it held when the file was last agreed with (section 4.2 of
`doc/detailed_design.md`). A member that has neither gave none.

<a id="edit_cfg_json.leaf_value.NO_VALUE_TEXT"></a>

#### NO\_VALUE\_TEXT

What the row of a member holding nothing says where a value would be.

It is worded as the `no {name}` of a declared member holding no configuration
object, because it is the same state one step down: the member is one the
class allows to hold nothing, and it holds nothing. Showing the `null` that
the file holds would be showing the notation of the file as if it were a value
the user had typed, and it is exactly the confusion between that `null` and an
empty text that this state exists to end.

<a id="edit_cfg_json.leaf_value.BOOL_WORDS"></a>

#### BOOL\_WORDS

The two words a member holding true or false is written with.

They are the JSON notation of the two values, which is what the file holds and
what the user therefore types. Nothing else means one of them: `yes` and `1`
are values of other kinds, and a member that holds one of those is a member of
another kind.

<a id="edit_cfg_json.leaf_value.BOOL_CHOICES"></a>

#### BOOL\_CHOICES

The two words as they are listed to the user, in the order asked.

<a id="edit_cfg_json.leaf_value.LeafType"></a>

## LeafType Objects

```python
class LeafType(NamedTuple)
```

What the class of a configuration says one leaf of it holds.

It is what the declaration of a member says, and it is empty where the
declaration says nothing this editor can use: an annotation naming a class
of the application's own, a member with no annotation at all, and a class
whose source cannot be read all answer with this holding nothing.

<a id="edit_cfg_json.leaf_value.LeafType.kind"></a>

#### kind

Which kind of value belongs here, None where nothing says.

It is one of the types of `VALUE_KINDS` and never a class of the
application: what the editor does with a kind is say what it is and make
an empty one of it, and it can do neither with a class it has never seen.

<a id="edit_cfg_json.leaf_value.LeafType.nothing"></a>

#### nothing

Whether this member may hold no value at all.

`Optional[str]` says it, and so does `str | None`. It is never true where
`kind` says nothing, because the two states of such a member are *holds a
value* and *holds nothing*, and a member the editor cannot make a value
for has only one of them.

It is set for a member that a class declares and never for a value inside
a list or a dict. What may hold nothing is something a class says about a
member of its own, and an element that could be taken out of what holds it
already has a control that means that.

<a id="edit_cfg_json.leaf_value.LeafType.inside"></a>

#### inside

What one value inside this one is, None where nothing says.

It is the element of a list and the value of a dict, which is what says
what an element of a list that its class declares empty would be.

<a id="edit_cfg_json.leaf_value.empty_value"></a>

#### empty\_value

```python
def empty_value(kind: Optional[type]) -> JsonType
```

Return the value of one kind that says no more than its kind.

**Arguments**:

- `kind` - Kind of value to make one of, None for a kind nothing says.
  

**Returns**:

  That value, and None where nothing says which kind it would be. A
  fresh one every time, because a list and a dict are values that the
  next edit would otherwise reach through.

<a id="edit_cfg_json.leaf_value.kind_of"></a>

#### kind\_of

```python
def kind_of(value: JsonType) -> Optional[type]
```

Return the kind of one value, None for a value that has no kind.

**Arguments**:

- `value` - One leaf value of the edit buffer, in JSON space.
  

**Returns**:

  The kind of that value, which is None only for `null`.

<a id="edit_cfg_json.leaf_value.leaf_kind"></a>

#### leaf\_kind

```python
def leaf_kind(declared: LeafType, original: JsonType) -> Optional[type]
```

Return the kind of value that one leaf takes.

What the class declared wins over what the leaf held, because a member
declared `float` whose default is written `0` is a number member whatever
the value says, and a member declared `Optional[str]` says that it takes
text while it holds nothing at all. The value answers where the class said
nothing, which is a class whose source cannot be read and a member with no
annotation.

**Arguments**:

- `declared` - What the class says the value here is.
- `original` - Value that the leaf held when the file was last agreed with.
  

**Returns**:

  The kind of value that leaf takes, None where nothing says.

<a id="edit_cfg_json.leaf_value.bool_word"></a>

#### bool\_word

```python
def bool_word(text: str) -> Optional[bool]
```

Return the value that the beginning of one of those words means.

The case is ignored and a beginning is enough, which is what
`config_as_json` already does for the name of an enum member: its
`string_to_enum_best_match` tries the case variants of what was typed and
then accepts a beginning that only one member has. A member holding true
or false has no such converter, because there is nothing to convert it
into, so it is answered here and by the same rules.

A beginning that both words have is no answer, exactly as an ambiguous
beginning of two enum member names is none. The empty text is the only one
there is, and it is what a cleared field holds.

**Arguments**:

- `text` - Text that the edit field holds.
  

**Returns**:

  The value that text means, and None when it means neither of them.

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
def text_as_value(
    text: str, original: JsonType,
    declared: LeafType = LeafType()) -> JsonType
```

Return the value that the text of one edit field stands for.

A member that takes text keeps exactly what the user typed, so that a
text member can hold the digits of a number without becoming a number. A
member that takes true or false takes any beginning of either word, as
`bool_word` says. Every other member has its text read as JSON, which is
the inverse of how `value_as_text` writes it.

Text that is not JSON at all is kept as a string rather than refused. A
value being typed passes through states that are not valid, and a field
that refused them could not be typed in at all. The string that a number
member then holds is not hidden: it is the wrong type, and validation
reports it as the wrong type.

**A field cannot put a member into the state that holds nothing.** Where a
member has that state it has a control that means it, and `null` typed
into the field is text that means no value of the member, exactly as any
other text of the wrong type is. Without that, the four characters of
`null` would take the field away from under the cursor that typed them. A
member with no such state reads `null` as the JSON it is, as before.

**Arguments**:

- `text` - Text that the edit field holds.
- `original` - Value that this member held when the file was last agreed
  with, which says how the text is read where the class said
  nothing. It never says what the text becomes.
- `declared` - What the class says the value here is, which says how the
  text is read wherever it says anything (section 4.2 of
  `doc/detailed_design.md`).
  

**Returns**:

  The JSON space value that the text stands for.

<a id="edit_cfg_json.leaf_value.canonical_text"></a>

#### canonical\_text

```python
def canonical_text(value: JsonType) -> str
```

Return one value as the text that decides whether it is unchanged.

The keys of a dictionary are sorted, because `config_as_json` writes them
sorted and a file that holds the same values in another order holds the
same values. The editor does hold them in another order: the members of a
nested configuration object are kept in the order its class declares them,
which is the order they are read in and not the order they are written in.

Everything else is compared as it is written, which is what tells `1` from
`1.0` and from `true`: all three of them reach the file differently.

**Arguments**:

- `value` - One value in JSON space.
  

**Returns**:

  The text that stands for that value.

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

<a id="edit_cfg_json.leaf_value.kind_text"></a>

#### kind\_text

```python
def kind_text(declared: LeafType, value: JsonType) -> str
```

Return what kind of value one node holds, as a line to read.

It is what the editor knows about a member without being told anything by
the application: which kind of value belongs there, which is what tells
the digits of a number from a text that happens to be digits. What the
class declared is asked first and the value answers where it said nothing,
which is what `leaf_kind` decides.

A node that really holds a list or a dict answers with nothing, because
its row already says how many things are in it and the rows below it say
what each of them is. One that holds nothing does say which of the two it
would be, because its row then says only that it holds nothing.

**Arguments**:

- `declared` - What the class says the value here is.
- `value` - Value that the node holds, in JSON space.
  

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
becomes one, and so is a member in the state of holding nothing, because that
state is asked for with a control and never typed.

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
             stderr_file: TextIO, defaults: Mapping[str, JsonType]) -> None
```

Read the JSON space values of one configuration object.

**Arguments**:

- `config` - Configuration object to read. It is not modified, because
  what is read is the text it writes and not the object.
- `report` - What reading the input file did beyond reading the values.
- `descriptions` - What the application says about its members.
- `stderr_file` - Stream used for user-facing diagnostics.
- `defaults` - The values that the class declares, which is what a new
  element of an ordinary list is copied from. They are empty for
  a class the editor could not construct at all, which costs
  that configuration the offer to grow such a list and nothing
  else.
  

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

<a id="edit_cfg_json.buffer.EditBuffer.bool_nodes"></a>

#### bool\_nodes

```python
@property
def bool_nodes() -> frozenset[ConfigPath]
```

Return the path of every node that holds true or false.

It is the type information of those nodes, which the rows own and a
validation pass needs: the values it is given are JSON space values,
and nothing in `true` and `1` says which of the two a member takes.

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

<a id="edit_cfg_json.buffer.EditBuffer.open_all"></a>

#### open\_all

```python
def open_all(no_more_folding: bool = False) -> None
```

Open every container of the buffer, whatever is folded now.

**Arguments**:

- `no_more_folding` - Whether a container that appears later is to be
  open as well. It stays on once it has been asked for, because
  what asks for it is a program that shows the buffer once: a
  validation pass can create a container, and the rule that
  decides the fold of a new one would fold a big one away again
  after the only moment at which anything is shown.

<a id="edit_cfg_json.buffer.EditBuffer.search"></a>

#### search

```python
@property
def search() -> FindReport
```

Return what is being looked for and what it has reached.

<a id="edit_cfg_json.buffer.EditBuffer.find"></a>

#### find

```python
def find(text: str) -> bool
```

Look for one text, starting again from the top.

**Arguments**:

- `text` - What to look for, empty to look for nothing at all.
  

**Returns**:

  Whether a container was opened to make what was found reachable,
  which is what says that the objects there are worth asking about.

<a id="edit_cfg_json.buffer.EditBuffer.set_find_options"></a>

#### set\_find\_options

```python
def set_find_options(options: FindOptions) -> bool
```

Change how the text is compared, and look again from the top.

**Arguments**:

- `options` - How the text being looked for is compared with one node.
  

**Returns**:

  Whether a container was opened, as above.

<a id="edit_cfg_json.buffer.EditBuffer.find_next"></a>

#### find\_next

```python
def find_next() -> bool
```

Go to the next node the text reaches, wrapping round to the first.

**Returns**:

  Whether a container was opened, as above.

<a id="edit_cfg_json.buffer.EditBuffer.add_element"></a>

#### add\_element

```python
def add_element(config: Config, path: ConfigPath, key: str = '') -> None
```

Put one more element into a node that holds them.

A new element is what the class of the configuration said one is: an
object of the declared class where the class declares one, a copy of
what it declares for the member where it does not, and the emptiest
value of the kind the member is annotated with where it declares
neither. A member that holds nothing is grown by being given a value,
which is what design sections 4.1 and 4.9 of `doc/detailed_design.md`
call adding, whether that value is a configuration object or not.

**Arguments**:

- `config` - Configuration object of the session. It is modified where
  the new element is a configuration object, because the tree
  finds those objects by walking the real ones. It is the
  editor's own copy and never the caller's.
- `path` - Path of the node to put an element into.
- `key` - Name of the new entry of a dict, empty for everything else.
  

**Raises**:

- `KeyError` - The path is not a node of this configuration.
- `ValueError` - Nothing can be added there, or the key is missing,
  unwanted or one that dict already holds.

<a id="edit_cfg_json.buffer.EditBuffer.remove_element"></a>

#### remove\_element

```python
def remove_element(config: Config, path: ConfigPath) -> None
```

Take one element out of the node that holds it.

A node that a class declared a place for is put back to holding
nothing instead of being taken out of what holds it, which is what
`ElementOffer.cleared` says: such a node keeps its row, and a key that
a `DICT_VALUE_BY_KEY` member declares keeps it while being one key of
a dict whose other keys are taken out of it.

**Arguments**:

- `config` - Configuration object of the session, modified as above.
- `path` - Path of the element to remove, or of the place to put back
  to holding nothing at all.
  

**Raises**:

- `KeyError` - The path is not a node of this configuration.
- `ValueError` - That node is not one that can be removed.

<a id="edit_cfg_json.buffer.EditBuffer.move_element"></a>

#### move\_element

```python
def move_element(config: Config, path: ConfigPath, later: bool) -> None
```

Make one element of a list change places with a neighbour.

**Arguments**:

- `config` - Configuration object of the session, modified as above.
- `path` - Path of the element to move.
- `later` - Whether it changes places with the one after it rather than
  with the one before it.
  

**Raises**:

- `KeyError` - The path is not a node of this configuration.
- `ValueError` - That node cannot be moved that way.

<a id="edit_cfg_json.buffer.EditBuffer.take_subtrees"></a>

#### take\_subtrees

```python
def take_subtrees(answers: Mapping[ConfigPath, SubtreeAnswer]) -> None
```

Keep what asking these objects about themselves found.

Only the objects that were asked are replaced, and what every other
one said is left exactly as it was: folding one node asks the objects
at and inside it, and a validation pass asks all of them.

**Arguments**:

- `answers` - What each of them said about itself, by the path of its
  node.

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

<a id="edit_cfg_json.settings_file"></a>

# edit\_cfg\_json.settings\_file

Where a program of this library reads its own settings from.

An application that calls `edit` knows its own settings and passes them. A
*program* has no application around it to ask, so it reads them from a file,
and this is the order it looks in: the file the command line names, the file
the environment names, the file of that program in the home folder, the file
of this library in the home folder, and finally no file at all.

**A file that was named must be there, and a file that was looked for need not
be.** `-c/--cfg` and the environment variable are somebody saying which file to
use, so a name that no file answers to is a mistake worth stopping for: running
with other settings than the ones that were asked for is the one thing a lookup
must not do quietly. The two files of the home folder are the lookup itself,
and a step of a lookup that finds nothing is the lookup working.

The file is read with `LoadPolicy.DEFAULTS`, because a settings file is
something somebody writes by hand to change one or two things, and what it does
not name is what the editor would have chosen anyway.

**A file that names nothing is the last step written down**, which follows from
that and is what a program has instead of an option for ignoring the lookup:
naming one is how a run asks for the values the editor would have chosen
anyway, past a file of the home folder that says something else.

**A file of an earlier release is read, and the run says so.** What such a file
does not hold is supplied by the rules of `SettingsConfig` rather than refused,
and a run that needed those rules tells the user which file it was and how to
write it again, because a compatibility path is something a future version may
take away. It says that the rules were needed rather than that an earlier
version wrote the file, because a file trimmed by hand needs them as well. The
words are printed here and not by a
`config_as_json.MigrateCfgWarnHook`: a hook prints while the file is parsed,
and `load_config` collects what a parse says into diagnostics that it shows
only when the load failed, so a hook's warning about a load that succeeded
would never reach anybody.

<a id="edit_cfg_json.settings_file.SETTINGS_VARIABLE"></a>

#### SETTINGS\_VARIABLE

Environment variable naming the settings file of every program here.

It is one variable for all of them rather than one each, because what it is for
is a machine or a session that has decided how this editor behaves, and an
answer that had to be given three times would come to be given twice.

<a id="edit_cfg_json.settings_file.SHARED_SETTINGS"></a>

#### SHARED\_SETTINGS

File of the home folder that every program of this library reads.

It is the last step of the lookup, so a user who wants one answer for the
window and for the terminal writes it once here, and a user who wants the two
to differ writes the file of one of them beside it.

<a id="edit_cfg_json.settings_file.NO_SETTINGS_FILE"></a>

#### NO\_SETTINGS\_FILE

Message of the refusal of a named settings file that is not there.

<a id="edit_cfg_json.settings_file.SETTINGS_REFUSED"></a>

#### SETTINGS\_REFUSED

Message of the refusal of a settings file that cannot be read as one.

<a id="edit_cfg_json.settings_file.OLDER_SETTINGS"></a>

#### OLDER\_SETTINGS

What a run says about a settings file that those rules were needed for.

It says that the rules were needed and not that an earlier version wrote the
file, because those are not the same statement: a file somebody trimmed by hand
needs them too, and telling such a user where their file came from would be
telling them something untrue. What follows is the same either way, which is
that saving the file writes every value this version has.

It names the file because the lookup has five steps and the user who sees this
did not necessarily choose the one that answered. It asks for the file to be
opened and saved rather than for a migration command of its own, because saving
is what writes those values and the editor is what the two programs are.

<a id="edit_cfg_json.settings_file.settings_file"></a>

#### settings\_file

```python
def settings_file(named: Optional[PathOrStr] = None,
                  home_settings: Optional[str] = None) -> Optional[Path]
```

Return the file that one program reads its settings from.

**Arguments**:

- `named` - File that `-c/--cfg` named, or None when it named none.
- `home_settings` - Name of this program's own file in the home folder, or
  None for a program that has none. A backend that prints once and
  returns is such a program: the settings that differ between the two
  editors are their keys and their questions, and it has neither.
  

**Returns**:

  The file to read the settings from, and None where the lookup found no
  file and the defaults of the editor are what is used.
  

**Raises**:

- `ConfigLoadError` - A file was named and is not there.

<a id="edit_cfg_json.settings_file.load_settings"></a>

#### load\_settings

```python
def load_settings(named: Optional[PathOrStr] = None,
                  home_settings: Optional[str] = None,
                  stderr_file: TextIO = sys.stderr) -> Settings
```

Return the settings that one program runs with.

**Arguments**:

- `named` - File that `-c/--cfg` named, or None when it named none.
- `home_settings` - Name of this program's own file in the home folder, or
  None for a program that has none.
- `stderr_file` - Stream that a file of an earlier release is reported on.
  

**Returns**:

  What the settings file says, or the defaults of the editor where the
  lookup found no file.
  

**Raises**:

- `ConfigLoadError` - A file was named and is not there, or the file the
  lookup found cannot be read as settings of this editor.

<a id="edit_cfg_json.placing"></a>

# edit\_cfg\_json.placing

Where a configuration object that a class declared is held, and putting one.

Adding an element and removing one are changes of the edit buffer, and one of
them is more: where the class of a configuration declares that something is a
configuration object, the object of the session gains one or loses one with
the values. The tree finds those objects by walking the real objects rather
than by matching a declaration, so an element that existed only in the buffer
would be shown as the dictionary it serializes to, with the member order of
nobody, the parse converters of nobody and no badge of its own.

The object that changes is the model's own copy, which the caller never sees,
so principle 5 of section 3 of `doc/detailed_design.md` is untouched.

**A declaration names a place and not always a member.** `LIST_ELEMENT` and
`DICT_VALUE` say that everything inside one member is an object, `MEMBER` and
`OPTIONAL_MEMBER` say that the member itself is one, and `DICT_VALUE_BY_KEY`
names one key of a dict, leaving every other key of it an ordinary value. So
where an object goes is asked as a path, and `ObjectPlace` is what the answer
is: the object that declared it, what was declared, the member holding it and
the key inside that member where there is one.

<a id="edit_cfg_json.placing.OBJECT_KINDS"></a>

#### OBJECT\_KINDS

The declarations that say every value inside one member is an object.

They are what makes a member of that shape extendable at all, and they are the
two that a new element is made from the declared class for. The other three
declarations are about the member itself, or about one key of it, rather than
about everything inside it.

<a id="edit_cfg_json.placing.ObjectPlace"></a>

## ObjectPlace Objects

```python
class ObjectPlace(NamedTuple)
```

Where one configuration object that a class declared is held.

<a id="edit_cfg_json.placing.ObjectPlace.holder"></a>

#### holder

The object whose class declared it.

<a id="edit_cfg_json.placing.ObjectPlace.nesting"></a>

#### nesting

What that class declared about the place.

<a id="edit_cfg_json.placing.ObjectPlace.member"></a>

#### member

Name of the member of that object which holds it.

<a id="edit_cfg_json.placing.ObjectPlace.key"></a>

#### key

Key of the dict that holds it, empty for the member itself.

It is what tells the two things a `DICT_VALUE_BY_KEY` declaration is about
apart: the member, which is a dict of ordinary values with named objects
in it, and one of those named keys.

<a id="edit_cfg_json.placing.new_object"></a>

#### new\_object

```python
def new_object(nesting: ConfigNesting, stream: TextIO) -> Config
```

Return one new configuration object of a declared class.

The factory the declaration names is asked where it named one, exactly as
`config_as_json` asks it while it reads a file, so an application that
answers with a subclass answers with it here too.

**Arguments**:

- `nesting` - What the class declared about the member that holds these.
- `stream` - Stream that collects what the construction says.
  

**Returns**:

  One object of that class, holding the values it declares.
  

**Raises**:

- `TypeError` - The class cannot be constructed this way.
- `ValueError` - The declared values are ones the class refuses.
- `AttributeError` - The class declares no public member at all.

<a id="edit_cfg_json.placing.object_added"></a>

#### object\_added

```python
def object_added(config: Config, path: ConfigPath, key: str,
                 stream: TextIO) -> None
```

Put a new configuration object where one has just been added.

Nothing happens where the member holds no configuration objects, because
there is then nothing about it that the object of the session says: what a
list of numbers holds is what the buffer holds, and the tree asks the
object only about the objects inside it.

**Arguments**:

- `config` - Configuration object of the session, which this modifies. It
  is the editor's own copy and never the caller's.
- `path` - Path of the member that has gained an element.
- `key` - Name of the new entry of a dict, empty for a list.
- `stream` - Stream that collects what the construction says.
  

**Raises**:

- `TypeError` - The declared class cannot be constructed this way.
- `ValueError` - Its declared values are ones it refuses.
- `AttributeError` - It declares no public member at all.

<a id="edit_cfg_json.placing.object_removed"></a>

#### object\_removed

```python
def object_removed(config: Config, path: ConfigPath) -> None
```

Take the configuration object of a removed element out of the tree.

**Arguments**:

- `config` - Configuration object of the session, which this modifies. It
  is the editor's own copy and never the caller's.
- `path` - Path of the element that has been removed, or of the declared
  place that has been put back to holding no object.

<a id="edit_cfg_json.placing.object_moved"></a>

#### object\_moved

```python
def object_moved(config: Config, path: ConfigPath, later: bool) -> None
```

Move the configuration object of a moved element with its values.

**Arguments**:

- `config` - Configuration object of the session, which this modifies. It
  is the editor's own copy and never the caller's.
- `path` - Path of the element that has been moved.
- `later` - Whether it changed places with the one after it.

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

Where it is the person running the application who decides rather than the
application, the same answers are `edit_cfg_json.SettingsConfig`, which is a
configuration class of their own and can be read from a file. Both classes here
stay frozen: what the editor is given it has no business changing, and the one
thing that would have wanted them unfrozen — bridging them into a `Config` —
turns out to be impossible for a reason of its own. See `settings_config`.

<a id="edit_cfg_json.settings.DUPLICATE_KEY"></a>

#### DUPLICATE\_KEY

Message of the refusal of one key combination given to two actions.

<a id="edit_cfg_json.settings.NOT_AN_EXTENSION"></a>

#### NOT\_AN\_EXTENSION

Message of the refusal of an extension setting that names none.

<a id="edit_cfg_json.settings.NOT_A_SUFFIX"></a>

#### NOT\_A\_SUFFIX

Message of the refusal of a backup suffix that names no file of its own.

<a id="edit_cfg_json.settings.NOT_A_COUNT"></a>

#### NOT\_A\_COUNT

Message of the refusal of a backup count that keeps no file at all.

Keeping no backup is what an empty `backup_suffix` says, and saying it twice
would leave two answers that could disagree with each other.

<a id="edit_cfg_json.settings.MIN_BACKUPS"></a>

#### MIN\_BACKUPS

Fewest backup files that `backup_count` may ask for.

<a id="edit_cfg_json.settings.names_a_file"></a>

#### names\_a\_file

```python
def names_a_file(value: str) -> bool
```

Return whether one piece of text adds anything to a file name.

Text that does not is neither an extension nor a backup suffix: a name
with it added would be the name it was added to, so the file it stands for
would be the file it was made from.

**Arguments**:

- `value` - Text that is to be added to a file name.
  

**Returns**:

  Whether adding it makes another name.

<a id="edit_cfg_json.settings.with_dot"></a>

#### with\_dot

```python
def with_dot(extension: str) -> str
```

Return one file name extension beginning with its dot.

**Arguments**:

- `extension` - Extension as it was written, with or without its dot.
  

**Returns**:

  That extension with a dot in front of it, so that `cfg` and `.cfg`
  mean the same thing.

<a id="edit_cfg_json.settings.BACKUP_SUFFIX"></a>

#### BACKUP\_SUFFIX

What is added to the name of a file whose previous content is kept.

It is added to the whole name rather than put in place of the extension, so
that a configuration called `xx.cfg` is kept as `xx.cfg.bak` and the name still
says what kind of file it was. That is also what lets one attribute express
every shape an application may want, `.old` and `~` among them.

<a id="edit_cfg_json.settings.WRONG_EXTENSION"></a>

#### WRONG\_EXTENSION

Message of the refusal of a file name an enforced extension forbids.

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
`ctrl+f`, which is the `find` action below.

An application whose configuration has no list and no dict in it is never
offered this action at all, because there would be nothing for it to do.

<a id="edit_cfg_json.settings.ActionSettings.find"></a>

#### find

Keys that put the cursor in the field a search is typed into.

`ctrl+f` because it is what opens a search everywhere else, and it was kept
free from the first version of this editor for exactly this action: an
action added later is an added attribute here and breaks no application,
but a *key* that moved would break every user who had learnt it, and no
version number protects a habit.

It puts the cursor in the field rather than asking a question, because the
field is part of the editor and stays: a user who has found one member and
wants another comes back to text that is already there.

<a id="edit_cfg_json.settings.ActionSettings.find_next"></a>

#### find\_next

Keys that go to the next node the search reaches.

`f3` because it is what finds the next one everywhere else, and it was kept
free for this action beside `ctrl+f` and for the same reason.

A function key is the one a keyboard or a terminal is most likely not to
deliver, and this action is reached without it in both backends: this one
is the whole tuple rather than the second of two because the control
letters a field does not claim are spoken for, and because the button and
the command palette entry are what an action without its key still has.

<a id="edit_cfg_json.settings.Settings"></a>

## Settings Objects

```python
@dataclass(frozen=True)
class Settings()
```

What the application around the editor has already decided.

Which keys its own user interface has taken and how hard the editor may
hold them, what one of its configuration files is called, and how the file
that is about to be overwritten is looked after. The last of those is the
application's for the same reason as the others: whether an old
configuration is worth keeping, and under what name, is something an
application knows about its own files and the editor cannot find out.

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

<a id="edit_cfg_json.settings.Settings.backup_suffix"></a>

#### backup\_suffix

What the file that is about to be overwritten is kept as, or None.

It is added to the whole file name, so `.bak` keeps `xx.cfg` as
`xx.cfg.bak`, `.old` keeps it as `xx.cfg.old` and `~` keeps it as
`xx.cfg~`. It is taken exactly as it is given, unlike `file_extension`,
because a suffix that is not an extension is one of the shapes an
application may want.

None keeps nothing, for an application that looks after its own files in
some other way. The default keeps one, because overwriting a file the user
has not written in this session is the one moment at which the previous
content is about to stop existing, and an editor that has it in its hands
is the cheapest place there will ever be to keep it.

<a id="edit_cfg_json.settings.Settings.backup_count"></a>

#### backup\_count

How many of them are kept, the newest first.

One is kept under the plain name that `backup_suffix` gives, because a
number in it would say that there are others when there are not. Two or
more are numbered from `_1`, which is the file that was overwritten last,
and each save moves every one of them one number further back until the
oldest falls off the end.

<a id="edit_cfg_json.settings.Settings.priority_keys"></a>

#### priority\_keys

Whether the keys of the editor are offered the key press first.

True is what an editor that owns its window wants: a key of the editor is
acted on before the field that has the focus is offered it, so that the
action runs wherever the user was typing. It is also what an editor
mounted in an application's own window wants most of the time, because
the keys of such an editor reach only the part of the window the editor
was given.

False is for an application that has already taken one of these
combinations for a widget of its own inside that part. The widget with
the focus is then offered the key first and the editor gets what is left
of it, which is the other way of answering the question that emptying one
tuple of `ActionSettings` answers by taking the key away altogether.

<a id="edit_cfg_json.settings.Settings.confirm_overwrite"></a>

#### confirm\_overwrite

Whether the user is asked before an existing file is overwritten.

They are asked once per destination per session, at the same moment as the
previous content would be kept, because that is the moment at which the
file on disk stops being what it was. A session that has already written
that file is not asked again: it is the user's own earlier save that is
being overwritten, and asking about it would be asking about nothing.

The two interactive editors put the question. A backend that prints once
and returns has nobody to answer it and writes what it was asked to write,
which is the same answer such a backend gives to the question about
closing.

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

<a id="edit_cfg_json.cli_target"></a>

# edit\_cfg\_json.cli\_target

What one command line says is to be edited, and how it is reached.

**The class is told and never guessed.** `--module` names an importable
module, `--file` names a Python file that is not, and `--edit-settings` says
that the class is this library's own settings. Exactly one of the three is
required, which is what makes them one group of `argparse` rather than a check
written by hand; a single `module:Class` argument reads well and would have to
guess which of them it was given, which is what section 8.2.1 of
`doc/detailed_design.md` settled for this library as a whole.

**What to edit is then either a class or a loader**, and `--class` and
`--loader` name them in the module or file that was reached. At least one of
the two is needed and both are allowed: a class alone is constructed on the
values it declares, a loader alone is asked for a configuration and its class
is whatever it answers with, and the two together mean that the loader has to
answer with that class or the program stops.

**Importing a module runs it.** That is the same exposure as running the file
with Python, and it is not guarded against, because a guard could only be a
pretence: a configuration class is Python and reaching it means importing the
module it is in.

<a id="edit_cfg_json.cli_target.PYTHON_SUFFIX"></a>

#### PYTHON\_SUFFIX

File name extension of the files that the `--file` door accepts.

<a id="edit_cfg_json.cli_target.NO_MODULE_MESSAGE"></a>

#### NO\_MODULE\_MESSAGE

Message of the refusal of a `--module` that names no importable module.

<a id="edit_cfg_json.cli_target.NO_FILE_MESSAGE"></a>

#### NO\_FILE\_MESSAGE

Message of the refusal of a `--file` that names no readable file.

<a id="edit_cfg_json.cli_target.NOT_PYTHON_MESSAGE"></a>

#### NOT\_PYTHON\_MESSAGE

Message of the refusal of a `--file` that Python cannot compile.

It covers both a name that is not a `.py` file at all and a `.py` file that
does not compile, because both mean the same thing to whoever ran the program:
what was named is not a Python module.

<a id="edit_cfg_json.cli_target.NOT_IMPORTABLE_MESSAGE"></a>

#### NOT\_IMPORTABLE\_MESSAGE

Message of the refusal of a file that only its own package can import.

A module that uses a relative import is the case that arises in practice, and
there is nothing a bare path can do about it: the import needs the package
that the module belongs to, and a path names no package.

<a id="edit_cfg_json.cli_target.NO_NAME_MESSAGE"></a>

#### NO\_NAME\_MESSAGE

Message of the refusal of a class name that the module does not hold.

<a id="edit_cfg_json.cli_target.NOT_CONFIG_MESSAGE"></a>

#### NOT\_CONFIG\_MESSAGE

Message of the refusal of a name that is not a configuration class.

<a id="edit_cfg_json.cli_target.NO_TARGET_MESSAGE"></a>

#### NO\_TARGET\_MESSAGE

Message of the refusal of a command line that says what to edit nowhere.

`argparse` cannot be asked for at least one of two options, only for exactly
one of them, and either alone is a perfectly good command line here.

<a id="edit_cfg_json.cli_target.OWN_TARGET_MESSAGE"></a>

#### OWN\_TARGET\_MESSAGE

Message of the refusal of a class named beside the editor's own class.

`argparse` refuses `--module` and `--file` beside it, because the three of them
are the one place a class comes from. The three that name something inside such
a module cannot be in that group, because they are not alternatives to it, so
this is the refusal that is written by hand.

<a id="edit_cfg_json.cli_target.NOT_LOADER_MESSAGE"></a>

#### NOT\_LOADER\_MESSAGE

Message of the refusal of a `--loader` that names something else.

<a id="edit_cfg_json.cli_target.LOADER_ARGS_MESSAGE"></a>

#### LOADER\_ARGS\_MESSAGE

Message of the refusal of a loader whose own arguments are not bound.

<a id="edit_cfg_json.cli_target.NO_LOADER_CONFIG"></a>

#### NO\_LOADER\_CONFIG

Message of the refusal of a loader that refused to answer at all.

The editor asks a loader for a configuration with no JSON source, which is what
`edit_cfg_json.ConfigLoader` says a loader answers. A loader that chooses its
class by looking at the JSON has to name the class it uses for a configuration
that does not exist yet, and this is the refusal of one that names none.

<a id="edit_cfg_json.cli_target.WRONG_CLASS_MESSAGE"></a>

#### WRONG\_CLASS\_MESSAGE

Message of the refusal of a loader that answered with another class.

A loader may choose its class by looking at the JSON, and `--class` beside it
is how a script says which class it is prepared to go on with. The check is
what `isinstance` answers, so a loader that answers with a subclass of the
class that was named is accepted.

<a id="edit_cfg_json.cli_target.NOT_DESCRIPTIONS"></a>

#### NOT\_DESCRIPTIONS

Message of the refusal of a `--descriptions` that names something else.

What the keys and the values of the mapping are is not checked, for the reason
section 4.3 of `doc/detailed_design.md` gives: a selector that addresses no
member of this configuration is simply never used, and a wrong description is a
cosmetic mistake that is not worth refusing to open an editor over.

<a id="edit_cfg_json.cli_target.NOT_SHOWABLE_MESSAGE"></a>

#### NOT\_SHOWABLE\_MESSAGE

Message of the refusal of a class that cannot be turned into a buffer.

The editor reads the values it edits by serializing the configuration object,
so a class that cannot serialize itself has no values to show. A class that
leaves part of its own writing to code outside itself is the case that arises
in practice, and there is nothing the editor can do with one.

<a id="edit_cfg_json.cli_target.explained"></a>

#### explained

```python
def explained(message: str, error: Exception, captured: str = '') -> str
```

Return one refusal with what Python said about it below it.

**Arguments**:

- `message` - What the program has to tell the user.
- `error` - The failure that Python reported.
- `captured` - What the code that failed wrote to its own diagnostics
  stream, empty when it wrote nothing or was given none.
  

**Returns**:

  The message, whatever was said, and the failure below both.

<a id="edit_cfg_json.cli_target.checked_class"></a>

#### checked\_class

```python
def checked_class(config: Config, wanted: Optional[type[Config]],
                  name: Optional[str]) -> None
```

Refuse a loaded configuration that is not the class that was asked for.

`--class` beside a `--loader` is a question rather than an instruction: is
this the class you are prepared to go on with? It is asked of the object
that is really going to be edited, so a loader that chose its class by
looking at the input file is answered for that file. `isinstance` is what
answers it, so a subclass of the class that was named is accepted.

**Arguments**:

- `config` - Configuration object that the load produced.
- `wanted` - Class that `--class` named, or None when it named none.
- `name` - Name of the loader, or None when the command line named none
  and there is therefore nothing to check.
  

**Raises**:

- `Refusal` - The class is not the one that was asked for.

<a id="edit_cfg_json.cli_target.Target"></a>

## Target Objects

```python
class Target(NamedTuple)
```

What one command line said is to be edited, and what explains it.

The two doors to it answer with the same four things: the object to start
from, what its application says about its members, and the loader and the
class that a save and a load are checked against where the command line
named them.

<a id="edit_cfg_json.cli_target.Target.config"></a>

#### config

Configuration object holding the values to start from.

<a id="edit_cfg_json.cli_target.Target.descriptions"></a>

#### descriptions

What the application says about its own members, or None.

<a id="edit_cfg_json.cli_target.Target.loader"></a>

#### loader

Loader the command line named, or None when it named none.

<a id="edit_cfg_json.cli_target.Target.wanted"></a>

#### wanted

Class that `--class` named, or None when it named none.

<a id="edit_cfg_json.cli_target.target_of"></a>

#### target\_of

```python
def target_of(parsed: Namespace) -> Target
```

Return what one command line says is to be edited.

**Arguments**:

- `parsed` - Parsed command line of one run.
  

**Returns**:

  The object to start from, and what says what about it.
  

**Raises**:

- `Refusal` - There is no configuration object to edit.

<a id="edit_cfg_json.settings_config"></a>

# edit\_cfg\_json.settings\_config

The settings of the editor, written as a configuration class of its own.

`Settings` is what an application decides in Python. This is the same thing
written as a `config_as_json.Config`, so that it can be read from a file, shown
in this editor like any other configuration, and declared as one member of an
application's own configuration class.

**It mirrors `Settings` and does not derive from it.** Deriving is what the
"third-party parameter class" pattern of `config_as_json` is for, and it is
impossible here for one reason: `ActionSettings` declares a member called
`validate`, which would shadow `Config.validate()` on every object of the
bridged class. `config_as_json` calls that method while it constructs and
while it parses, so such a class cannot be built at all. That is why `Settings`
and `ActionSettings` stay frozen, which is what section 9.1 of
`doc/detailed_design.md` asks of them for reasons of its own.

**The key combinations are a dict of lists and not a nested object.** A nested
`Config` object is read whole — `config_as_json` constructs one from its own
JSON without the permissive flag of the parse around it — so every settings
file would have had to name every action. A dict member is filled in per key
instead, its keys are checked against the ones this class declares, and a
member validator completes what a file left out. So a settings file may name
one action and the editor still shows all of them.

**Nothing here restates what a valid setting is.** Each member validator hands
the value to `Settings` or `ActionSettings` and reports what the dataclass
refused, which is principle 1 of section 3 of `doc/detailed_design.md` applied
to the editor's own settings: there is one place that says a key combination
cannot belong to two actions, and it is the place the editor itself is built
on.

**An action added to `ActionSettings` is a change of file format**, because
the keys of a dict member are matched against the ones this class declares
before any validator of this class is asked anything, and they are matched
whatever policy the parse was given. So every settings file written before that
action existed would be refused, and a whole application would fail to start
over a key of the editor it embeds. `ADDED_ACTIONS` is what those files are
read by, and section 9.10 of `doc/detailed_design.md` is what says that an
action added later belongs in it.

<a id="edit_cfg_json.settings_config.UNKNOWN_ACTION"></a>

#### UNKNOWN\_ACTION

Message of the refusal of an action name that this editor does not have.

<a id="edit_cfg_json.settings_config.REFUSED_KEYS"></a>

#### REFUSED\_KEYS

The same for the combinations, whose value is every action there is.

Writing the value out would name every action of the editor to say something
about two of them, and the sentence that `ActionSettings` refuses them with
names those two itself.

<a id="edit_cfg_json.settings_config.declared_actions"></a>

#### declared\_actions

```python
def declared_actions() -> dict[str, list[str]]
```

Return the key combinations of every action, as a file holds them.

They are read from `ActionSettings` rather than written out again, so that
an action added there is an action this configuration class has without
anything here being changed, and so that the two cannot disagree about a
default.

**Returns**:

  The combinations of each action, by the name of that action.

<a id="edit_cfg_json.settings_config.ADDED_ACTIONS"></a>

#### ADDED\_ACTIONS

Actions that previous released versions did not write into a file.

Supplying these is what makes a settings file of an earlier release readable,
and only an action added after a release belongs here. An action that has
always been here is named by every file that any released version wrote, so
supplying that one would accept a file no version ever produced, and would put
a key back that somebody had deliberately taken out.

<a id="edit_cfg_json.settings_config.SettingsConfig"></a>

## SettingsConfig Objects

```python
class SettingsConfig(Config)
```

What has been decided about the editor itself.

Which key combinations run the actions of the editor, what a configuration
file of this application is called, and how the file that a save writes
over is looked after. It is the same set of answers as `Settings`, in the
form that can be read from a file and edited in this editor.

A file of these need name only what it changes: what it leaves out keeps
the answer the editor would have chosen anyway, and the editor shows every
setting whatever the file held.

<a id="edit_cfg_json.settings_config.SettingsConfig.__init__"></a>

#### \_\_init\_\_

```python
def __init__(from_json_data_text: Optional[str] = None,
             from_json_filename: Optional[PathOrStr] = None,
             stderr_file: TextIO = sys.stderr) -> None
```

Declare every setting of the editor, and read the file there is.

The declared values are read from `Settings` and `ActionSettings`
rather than written out again, so that the default of a setting is
stated once and the two cannot come to disagree.

**Arguments**:

- `from_json_data_text` - Optional JSON text to parse directly.
- `from_json_filename` - Optional path to a JSON file to read.
- `stderr_file` - Stream used for user-facing diagnostics.

<a id="edit_cfg_json.settings_config.SettingsConfig.as_settings"></a>

#### as\_settings

```python
def as_settings() -> Settings
```

Return these values as the editor is given them.

**Returns**:

  What this configuration says, as the frozen object every entry
  point of this library takes.
  

**Raises**:

- `ValueError` - One key combination is set for two actions, which
  cannot happen for a validated object and can for one whose
  members were assigned by hand.

<a id="edit_cfg_json.settings_config.SettingsConfig.get_validation_plan"></a>

#### get\_validation\_plan

```python
def get_validation_plan(stderr_file: TextIO) -> ValidationPlan
```

Return what every setting of the editor is checked against.

**Arguments**:

- `stderr_file` - Stream used for user-facing diagnostics, which the
  validators of this plan are given when they run.
  

**Returns**:

  One step per kind of setting there is.

<a id="edit_cfg_json.settings_config.ACTION_DESCRIPTIONS"></a>

#### ACTION\_DESCRIPTIONS

What each action of the editor is, by the name it is set under.

Every action of `ActionSettings` has an entry, and one that is added later
without one is described by the line that reaches every action instead.

<a id="edit_cfg_json.settings_config.EVERY_ACTION"></a>

#### EVERY\_ACTION

What is said about an action that has nothing said about it.

It is what the `[` selector reaches, so it is the whole of what is said below
an action added to `ActionSettings` and not to `ACTION_DESCRIPTIONS`, and it is
never seen beside one of those: a selector naming the action is the more
specific of the two and wins.

<a id="edit_cfg_json.settings_config.SETTINGS_DESCRIPTIONS"></a>

#### SETTINGS\_DESCRIPTIONS

What this configuration class says about each of its own members.

It is what an application hands to the editor beside `SettingsConfig`, and an
application that has this class as one member of its own configuration puts
its own path in front of every one of these paths.

<a id="edit_cfg_json.settings_config.described_below"></a>

#### described\_below

```python
def described_below(prefix: ConfigPath) -> Descriptions
```

Return what this class says about its members, below one member.

An application that declares a `SettingsConfig` as one member of its own
configuration describes that member's members with this, because a
description addresses the whole path to what it is about.

**Arguments**:

- `prefix` - Path of the member that holds the `SettingsConfig`, which is
  `('editor',)` for a member called `editor`.
  

**Returns**:

  The same descriptions, each of them below that member.

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

<a id="edit_cfg_json.model_text.FOUND_MARK"></a>

#### FOUND\_MARK

Mark that follows the value of the node a search has got to.

A search reaches one node at a time, so exactly one row can carry it. The two
backends bring that row into view and put the focus in its field as well, which
is what a printout has no way of doing and is why this mark is what a printout
has instead.

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

<a id="edit_cfg_json.model_text.FIND_FORM"></a>

#### FIND\_FORM

Form of the line that says where a search has got to.

How many nodes the text reaches and which of them is being shown, because a
search of a configuration too big for a window is a search whose other answers
are off the screen: a user who is told only that something was found has no way
of knowing that there is more to look at.

<a id="edit_cfg_json.model_text.FIND_COUNT_FORM"></a>

#### FIND\_COUNT\_FORM

The same for a search that reaches nodes and is at none of them.

A validation pass can leave the model with other rows than it had, and can
rewrite a value into something the text no longer reaches, so the node a search
had got to is not always still there. What the text reaches is still true, and
the next press of the find key starts again from the top.

<a id="edit_cfg_json.model_text.NOT_FOUND_FORM"></a>

#### NOT\_FOUND\_FORM

Form of the line that says a search reaches nothing at all.

<a id="edit_cfg_json.model_text.FIND_NOWHERE_FORM"></a>

#### FIND\_NOWHERE\_FORM

Form of the line about a search that has nowhere to look.

Both of the places a search looks can be turned off, and nothing is then
compared with anything. Saying that no member matches would be untrue, which is
why it is said as what it is.

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

<a id="edit_cfg_json.model_text.CLOSE_QUESTION"></a>

#### CLOSE\_QUESTION

What the user is asked before closing an editor with unsaved changes.

Closing writes nothing of its own, so a session that is closed with something
in the buffer loses it. What is lost is the one thing the editor knows and the
user may not, which is why it is said rather than left to be discovered.

<a id="edit_cfg_json.model_text.OVERWRITE_QUESTION"></a>

#### OVERWRITE\_QUESTION

What the user is asked before a save writes over a file they did not.

It is asked once per destination per session, because from the second save
onwards the file being written over is the user's own earlier save and there
is nothing there to lose.

<a id="edit_cfg_json.model_text.KEPT_QUESTION"></a>

#### KEPT\_QUESTION

What the same question adds where the previous content is kept.

The user is answering a question about losing a file, so whether it is really
lost is part of what they are answering about. An application that keeps no
backup says nothing here, which is the honest thing for it to say.

<a id="edit_cfg_json.model_text.SUBTREE_VALID_MARK"></a>

#### SUBTREE\_VALID\_MARK

What a nested object that is a configuration on its own says.

*On its own* is the whole of what it claims, and the words are there because
of what it must not be read as. The configuration holding this object may be
refused for a reason that is about nothing inside it — a rule of the class
above relating this object to another one is exactly that — so this says
nothing at all about whether the file can be written. That is the line below
the members, and it is the only thing that answers it.

<a id="edit_cfg_json.model_text.SUBTREE_REFUSED_MARK"></a>

#### SUBTREE\_REFUSED\_MARK

What a nested object that its own class refuses says.

The other way round holds without qualification: an object its own class
refuses cannot be part of a configuration that is saved. What is wrong with it
is at the member it is about, or below the object where it is about no member
of it.

<a id="edit_cfg_json.model_text.INSIDE_VALID_MARK"></a>

#### INSIDE\_VALID\_MARK

What a list or a dict of configuration objects says when all of them pass.

A container is no configuration and can say nothing about itself, so what it
says is about the objects it holds. *Inside* is what keeps the two apart: a
rule of the class above may refuse the configuration while every object in this
container is a perfectly good one, exactly as it may for a single object.

<a id="edit_cfg_json.model_text.INSIDE_REFUSED_MARK"></a>

#### INSIDE\_REFUSED\_MARK

What such a container says when one of the objects it holds is refused.

It is on the row of the container because that row is what a folded container
leaves on the screen. Without it, folding a member would hide the one thing the
user has to act on and leave nothing at all in its place, and a user who folds
a member to get it out of the way is not asking to be told that everything in
it is fine.

What is wrong is still at the object it is about, and is read by opening the
container: this says that there is something to open it for.

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
changed it, a validator then changed what the user had written, and a
search has got to it. They are in the order in which they can happen. The
two that a load sets are never both there, because the more precise of the
two is the one it sets.

The last of them is about the search rather than about the member, and it
is here because it belongs where the others are: it says that something
has happened to this member which the user should see, which is what every
mark of a member says.

Both backends read the marks from here, so that neither of them decides on
its own what a member the load, the user, a validator or a search touched
looks like.

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

  Whether the application, the type of the node, the class of the object
  at it or what cannot be added to it has anything to say.

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

A member that holds several of something and cannot be given another says
so last. It is explanation and not a refusal to act on: it says what this
member is, in the same way as the line saying what kind of value a member
holds, and a user who knows this configuration wants it out of the way
with the rest.

**Arguments**:

- `model` - Model that the node belongs to.
- `row` - Node to describe.
  

**Returns**:

  What is said below that node, empty while it is not being shown or
  when there is nothing to say about it.

<a id="edit_cfg_json.model_text.row_validates"></a>

#### row\_validates

```python
def row_validates(row: MemberRow) -> bool
```

Return whether one node can ever say what its objects amount to.

A backend asks this before it creates the widget that says it, by the same
rule as `row_describes`: a widget that could never hold anything is a
piece of the window spent on nothing.

A declared nested configuration object that is really there can, and so
can a list or a dict that holds such objects at any depth, which is the
ordinary shape of a configuration worth editing. A value cannot, an empty
container cannot, and a declared member that holds no object has no object
to ask.

**Arguments**:

- `row` - Node to ask about.
  

**Returns**:

  Whether a configuration object is at that node or inside it.

<a id="edit_cfg_json.model_text.row_subtree_text"></a>

#### row\_subtree\_text

```python
def row_subtree_text(row: MemberRow) -> str
```

Return what the objects at or inside one node amount to, as shown.

A node that has not been asked since something inside it last changed says
nothing, because that is a state and not an answer, and a line saying so
under every object would be a line spent on nothing.

A container of objects is worded differently from an object, because it is
saying a different thing: an object answers for itself and a container
answers for what it holds. Nothing else could tell them apart, since a
folded container shows none of the objects the words are about.

Both backends read it from here, so that neither of them decides on its
own how a valid object and a refused one are told apart.

**Arguments**:

- `row` - Node to render.
  

**Returns**:

  What that node is on its own or what it holds, and nothing for a node
  that has no object at it or inside it and for one not asked yet.

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

<a id="edit_cfg_json.model_text.rows_shape"></a>

#### rows\_shape

```python
def rows_shape(model: EditModel) -> tuple[tuple[ConfigPath, bool], ...]
```

Return what the widgets a backend builds for the rows depend on.

A validation pass is not read only, and neither is it only about values.
It can leave the model with other rows than it had, which a validator
that normalizes a list does, and it can leave one row a different thing
from what it was, which a validator that answers `None` for a member
allowed to hold nothing does: that row had a field and now has none. A
backend that only wrote the values back would then be showing a field for
a member that holds nothing, and the next key typed into it would be
refused.

So a backend compares this before and after, and makes its widgets again
where it differs. It is here rather than in each backend for the same
reason every other question about a row is: two user interfaces of one
application that rebuilt at different moments would each be right about a
different editor.

**Arguments**:

- `model` - Model to ask about.
  

**Returns**:

  The path of every row and whether that row is a value with a field,
  in the order the rows are shown.

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

Three things can be wrong with a node and they are not the same thing.
Its text may mean no value of that node at all, which is answered by
the node alone and stays true until the node is edited again; the
application may have refused the value it holds, which is answered by the
whole configuration and is only known for as long as the rest of the
buffer stands still; or the nested configuration object that owns the node
may have refused it when it was asked about itself, which is known for as
long as nothing inside that object changes. The first is preferred when
more than one is there, because a value that does not exist yet is what
has to be corrected first, and the verdict comes before the answer of one
object because a pass over the whole buffer is the more recent of the two
whenever both are there.

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

<a id="edit_cfg_json.model_text.find_text"></a>

#### find\_text

```python
def find_text(model: EditModel) -> str
```

Return what the search has reached, and nothing when there is none.

A search that has not been made says nothing at all, which is what an empty
field means: it is a third state and not a search that found nothing, and a
line under every session that nobody searched in would be a line spent on
nothing.

The three ways a search says something are three different things, and each
is said as what it is: it has got to one of several nodes, it reaches nodes
and is at none of them, or it reaches nothing. A search that has nowhere to
look is the fourth, and it is not the same as reaching nothing, because
nothing was compared with anything.

Both backends read it from here, so that neither of them decides on its own
what a user who is looking for something is told.

**Arguments**:

- `model` - Model whose search is reported.
  

**Returns**:

  What is being looked for and what it has reached, and nothing at all
  while nothing is being looked for.

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

<a id="edit_cfg_json.model_text.close_question"></a>

#### close\_question

```python
def close_question(model: EditModel) -> str
```

Return what to ask before closing, and nothing when there is nothing.

Closing writes nothing, so a session with something in the buffer that has
not reached the file loses it. Whether that is so and what is asked about
it belong here rather than to a backend, by the same rule as the verdict
and the saving: two user interfaces of one application, one of which asked
and one of which did not, would be worse than either behaviour. How the
question is put is each backend's own, because that is where the toolkits
differ.

A backend that prints once and returns is not asking anybody: there is no
session for a user to close, so it consults nothing here and its answer is
the one it always had, which is that there is nothing to keep.

**Arguments**:

- `model` - Model that is about to be closed.
  

**Returns**:

  The question to put to the user, and nothing at all when the buffer
  holds nothing that closing would lose.

<a id="edit_cfg_json.model_text.overwrite_question"></a>

#### overwrite\_question

```python
def overwrite_question(model: EditModel) -> str
```

Return what to ask before saving, and nothing when there is nothing.

A save writes over whatever the destination holds, and what it holds may
be a configuration this session never read. Whether the user is asked
about that is the application's decision, because only an application
knows how its own files are looked after; whether there is anything to ask
about is this model's, by the same rule as the question about closing. How
the question is put is each backend's own.

A backend that prints once and returns is asking nobody. It writes what it
was asked to write, which is the answer such a backend gives to every
question, and the previous content is kept exactly as it is for a user who
answered.

**Arguments**:

- `model` - Model that is about to be saved.
  

**Returns**:

  The question to put to the user, and nothing at all when saving would
  overwrite nothing that this session did not write itself.

<a id="edit_cfg_json.model_text.model_as_text"></a>

#### model\_as\_text

```python
def model_as_text(model: EditModel) -> str
```

Return the whole model as text, one line per node of it.

The configuration object labels itself first, because what the whole
configuration is for is what the members below it are read in the light
of. What reading the input file did comes next, because it is what
explains the marks on those members. What a search has reached follows
them, then the validation state of the buffer, and the saving after that,
in the order in which a session reaches them, so that a rendering never
leaves it unsaid what the application would make of what is shown or where
it would be written. It belongs to the core rather than to a backend
because it is user interface agnostic.

What it renders is what the model holds, and that is the whole of what it
can testify to. The two interactive backends draw the same model and add
everything a printout has none of — a field with the focus in it, a
control to press, a question to answer — so this is what a test and a
script read to check the core without a display, and never a substitute
for looking at an editor.

**Arguments**:

- `model` - Model to render.
  
  A container that is folded away is one line saying so, and what is inside
  it is not shown at all, which is the same thing the two backends do with
  it. What is inside a list or a dict is indented below it.
  

**Returns**:

  The label of the configuration and what its class says about itself,
  what the load did, one line per shown node with its description and
  anything wrong with it below it, and then what a search has reached,
  the validation state and the saving, without a trailing line break.

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

<a id="edit_cfg_json.version_report"></a>

# edit\_cfg\_json.version\_report

What one program of this library answers `--version` with.

Whoever is about to report a problem, and whoever is about to upgrade, has to
know which versions are really installed and whether newer ones exist.
[`versionreporter`](https://pypi.org/project/versionreporter/) answers both, so
`--version` is one call to it rather than a version string of this library's
own: it reads the installed version of every package named below, asks PyPI
what is available for this Python version and for a newer one, and says which
of them are worth upgrading to.

**What a program reports is the distribution it was installed from**, and the
packages that distribution is built on. So this class is derived once per
distribution, each editor package putting its own name in front of what the
core already lists, which is what keeps one list of dependencies from becoming
three. The name in front is not only for reading: `versionreporter` takes the
first of them as the package its upgrade instructions name.

**It has to be a class and not a name handed to one.**
`get_main_package_name` and `recommended_python` are class methods of
`versionreporter`, so two instances of one class cannot answer them
differently, and a class per distribution is what that leaves.

<a id="edit_cfg_json.version_report.MAIN_PACKAGE"></a>

#### MAIN\_PACKAGE

Distribution that the core of this library is installed from.

<a id="edit_cfg_json.version_report.EcajVersionReporter"></a>

## EcajVersionReporter Objects

```python
class EcajVersionReporter(VersionReporter)
```

Report what this package and everything it is built on are.

It is what `python3 -m edit_cfg_json.dump` answers `--version` with, and
the base class of the reporter of each editor package, which is what lets
a backend name itself without repeating what this package depends on.

<a id="edit_cfg_json.version_report.EcajVersionReporter.package_names"></a>

#### package\_names

```python
def package_names() -> list[str]
```

Return the distributions whose versions are reported.

**Returns**:

  This distribution first, because that is the one an upgrade
  instruction names, and then everything it declares.

<a id="edit_cfg_json.version_report.EcajVersionReporter.get_app_support_expires"></a>

#### get\_app\_support\_expires

```python
def get_app_support_expires() -> SupportExpires
```

Return when these packages stop being released for an old Python.

The dates follow the cadence `versionreporter` uses for itself, which
drops a Python version well before that version's own end of life:
what these packages promise is a release for a new Python and not a
bug fix for an old one.

**Returns**:

  For each date, the newest Python version that is no longer
  supported once that date has passed.

<a id="edit_cfg_json.version_report.EcajVersionReporter.get_main_package_name"></a>

#### get\_main\_package\_name

```python
@classmethod
def get_main_package_name(cls) -> str
```

Return the distribution that the upgrade instructions name.

**Returns**:

  What to install to upgrade the program that is running.

<a id="edit_cfg_json.version_report.EcajVersionReporter.recommended_python"></a>

#### recommended\_python

```python
@classmethod
def recommended_python(cls) -> Version
```

Return the Python version these packages are meant to run on.

**Returns**:

  The newest Python version every one of them is released for.

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

<a id="edit_cfg_json.emphasis.subtree_emphasis"></a>

#### subtree\_emphasis

```python
def subtree_emphasis(row: MemberRow) -> Emphasis
```

Return how what the objects at or inside one node amount to is shown.

The same three states as the validation of the whole configuration, and
the same three ways of showing them, because they are the same kind of
answer about a smaller thing: a node that has not been asked since
something inside it changed is what has not happened yet rather than
something wrong.

A list or a dict of configuration objects is shown the same way, and says
the same three things about the objects it holds rather than about itself.

**Arguments**:

- `row` - Node whose own state is shown.
  

**Returns**:

  The emphasis of what that node is on its own, or of what it holds.

<a id="edit_cfg_json.emphasis.find_emphasis"></a>

#### find\_emphasis

```python
def find_emphasis(model: EditModel) -> Emphasis
```

Return how what a search has reached is shown.

A search that has not been made says nothing at all, so the emphasis is
what has not happened yet, exactly as it is for a validation nobody has
asked for. A search that reaches at least one node has reached something
the user should see, and one that reaches nothing — because the text is
about no node, or because there is nowhere left to look — is the one thing
on that line to act on.

**Arguments**:

- `model` - Model whose search is shown.
  

**Returns**:

  The emphasis of the line that says what the search has reached.

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

How many things such a member holds is editable as well, because that is
what a member of that shape exists to let the application's user decide. A
new element is copied from what the class declares and never invented, and
a node the editor has nothing to copy for offers nothing and says so.

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

Such an object is also asked whether it is a configuration on its own,
which folding it and every validation pass answer. That is a different
state from the verdict of the whole configuration and is kept apart from
it: a rule of the class above may relate two of these objects across the
boundary between them, so both of them can be valid on their own while the
configuration holding them cannot be saved.

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
  when it did not say. The model needs it for two things. A save
  asks it whether the application would read back the file that
  is about to be written, which is the one question the
  validation of a buffer cannot answer; and it is asked here,
  with no JSON source, for the values the class declares, which
  is what a new element of an ordinary list is copied from. A
  class the editor cannot construct answers with nothing and
  loses that offer and nothing else.
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

Every nested configuration object at or inside that container is asked
whether it is a configuration on its own at the same time, and what it
refused is kept with the answer. That is the cheap local question, it
needs no candidate configuration, and changing how much of a node is
on the screen is the moment at which a user is looking at it.

Every object inside it and not only the node itself, because the
member that holds several objects is a list or a dict and is no
configuration of its own. Folding one of those hides every object in
it, so folding one of those has to ask every object in it.

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

Every nested configuration object is asked about itself, for the same
reason folding one of them asks that one.

<a id="edit_cfg_json.edit_model.EditModel.open_all"></a>

#### open\_all

```python
def open_all(no_more_folding: bool = False) -> None
```

Open every container, whatever is folded now.

It is what a backend that shows the model once asks for, and the
toggle above is what a user interface with a control offers: the
toggle answers what the next press does, which is a question only a
session that goes on can ask.

Every nested configuration object is asked about itself, for the same
reason folding one of them asks that one.

**Arguments**:

- `no_more_folding` - Whether a container that a later pass creates is
  to be open as well. A validation pass can add one, and a new
  container is folded away when it is large, so a program that
  shows the buffer once and then ends asks for this and a
  session that a user is looking at does not.

<a id="edit_cfg_json.edit_model.EditModel.search"></a>

#### search

```python
@property
def search() -> FindReport
```

Return what is being looked for and what it has reached.

What is being looked for is state of this model, by the same rule as
the explain toggle and the fold state: two user interfaces of one
application that were looking for different things, or looking in
different places, would each be right about a different search. Every
row says whether it is the node the search has got to, which is where
a backend reads that.

<a id="edit_cfg_json.edit_model.EditModel.find"></a>

#### find

```python
def find(text: str) -> bool
```

Look for one text, starting again from the top.

A configuration of any interesting size does not fit a window, so the
node a user wants is often one they cannot see. What is found has to be
reachable, so every folded container hiding it is opened; bringing the
row into view and giving its field the focus are each backend's, since
that is where the two toolkits differ.

**Arguments**:

- `text` - What to look for, empty to look for nothing at all, which is
  what a cleared field means.
  

**Returns**:

  Whether a container was opened, which is what says that the rows a
  backend shows are not the rows it was showing.

<a id="edit_cfg_json.edit_model.EditModel.set_find_options"></a>

#### set\_find\_options

```python
def set_find_options(options: FindOptions) -> bool
```

Change how the text is compared, and look again from the top.

Whether the path is looked in, whether the value is, whether the case
has to match and whether the whole of one of them has to are four
independent answers, and they belong to this model for the same reason
the text does.

**Arguments**:

- `options` - How the text being looked for is compared with one node.
  

**Returns**:

  Whether a container was opened, as above.

<a id="edit_cfg_json.edit_model.EditModel.find_next"></a>

#### find\_next

```python
def find_next() -> bool
```

Go to the next node the text reaches, wrapping round to the first.

A text that reaches nothing leaves the search where it was, which is
at no node at all, and the line about the search says so.

**Returns**:

  Whether a container was opened, as above.

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

<a id="edit_cfg_json.edit_model.EditModel.overwritten_file"></a>

#### overwritten\_file

```python
@property
def overwritten_file() -> Optional[PathOrStr]
```

Return the existing file that saving now would overwrite, or None.

There is one where a destination has been chosen, a file of that name
is really there, and this session has not written it yet. That last
condition is what makes this a question about the user's *own* work: a
file this session has written is the user's earlier save, and there is
nothing to say about overwriting one of those.

It is what says whether a backend has anything to ask before it saves,
and what the previous content is kept as is decided at the same moment
and for the same file.

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

<a id="edit_cfg_json.edit_model.EditModel.add_element"></a>

#### add\_element

```python
def add_element(path: ConfigPath, key: str = '') -> None
```

Put one more element into a node that holds them.

A new element is what the class of the configuration said one is,
because it is the only thing that knows: an object of the declared
class where a class declares that every element of a list or every
value of a dict is one, a copy of what the class declares for the
member itself where it declares no such thing, and failing both of
those the emptiest value of the kind the member is annotated with. The
editor invents no value that the application never mentioned, and a
node that says none of the three offers nothing and says why.

A member holding nothing is grown by being given a value. That is
adding rather than editing, for the reason a field cannot do it: no
text typed into a field becomes a configuration object, and holding
nothing is a state of a member rather than a text in a field. It is
the same pair of actions for a declared member holding no
configuration object and for one the declaration allows to hold no
value at all.

Which nodes offer this is on the rows, as `MemberRow.offer`, so that
two user interfaces of one application cannot offer different things.

**Arguments**:

- `path` - Path of the node to put an element into.
- `key` - Name of the new entry of a dict, which only the user can
  give. It is empty for everything else, because an element of a
  list is addressed by where it is.
  

**Raises**:

- `KeyError` - The path is not a node of this configuration.
- `ValueError` - Nothing can be added there, or the key is missing,
  unwanted, or one that dict already holds.

<a id="edit_cfg_json.edit_model.EditModel.remove_element"></a>

#### remove\_element

```python
def remove_element(path: ConfigPath) -> None
```

Take one element out of the node that holds it.

A member that may hold nothing and holds something is put back to
holding nothing, which is the other half of what adding does. It is
what tells a value the class allowed to be absent apart from an empty
text of the same member, which no field could do. A member that its
class leaves out of the file altogether is not offered this: it would
then have no row at all, and a member the editor had taken off the
screen could never be given a value again.

**Arguments**:

- `path` - Path of the element to remove.
  

**Raises**:

- `KeyError` - The path is not a node of this configuration.
- `ValueError` - That node is not one that can be removed.

<a id="edit_cfg_json.edit_model.EditModel.move_element"></a>

#### move\_element

```python
def move_element(path: ConfigPath, later: bool) -> None
```

Make one element of a list change places with a neighbour.

The order of a list is part of what the file says, so it is part of
what an editor of that file has to be able to change. A dict has no
such question, because it is written in the sorted order of its keys.

**Arguments**:

- `path` - Path of the element to move.
- `later` - Whether it changes places with the one after it rather than
  with the one before it.
  

**Raises**:

- `KeyError` - The path is not a node of this configuration.
- `ValueError` - That node cannot be moved that way.

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

What the destination held before this session reached it is kept
first, under the name the application chose for it, so that a save
over somebody else's configuration does not take it away from them.

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

It is what the current value is compared against, and it is the type
information of every node whose declaration says nothing. Reading the type
from the current value instead would not work: a number member that the
user has half typed holds text for as long as the text is not a number
yet, and the member would then stop being a number member. A save is safe
to move it to, because only a validated value is ever written.

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

<a id="edit_cfg_json.rows.MemberRow.subtree_valid"></a>

#### subtree\_valid

Whether the object here is a configuration on its own, None if unasked.

It is set for a declared nested configuration object and for nothing else,
because nothing else is a configuration that can be asked about itself. A
list, a dict and an ordinary value have no class of their own to ask, and a
declared member holding no object has no object to ask.

None is a third state rather than a kind of failure, exactly as it is for
the verdict of the whole configuration: this object has not been asked
since something inside it last changed. It is answered by folding the node
or opening it, and by every validation pass, and an edit anywhere inside it
takes the answer away again.

It says nothing about whether the configuration could be saved, and it is
deliberately not the same question: a rule of the class above may relate
two of these objects across the boundary between them, so both of them can
be valid on their own while the configuration holding them is refused.

A list or a dict of such objects carries it too, and there it is about the
objects inside rather than about the container, which is no configuration
and has nothing to say about itself. It is false as soon as one of them is
refused, true once every one of them has been asked and accepted, and None
while any of them is unasked and none is refused. Folding such a member
hides every object in it, so folding it asks every object in it.

<a id="edit_cfg_json.rows.MemberRow.subtree_refusal"></a>

#### subtree\_refusal

Why the object owning this node refused it, empty when it did not.

It is what asking one nested configuration object about itself found, kept
at the node that answer was about: a member of that object where a member
validator refused one, and the object itself where its class refused it
for a reason that is about no member of it.

It is a third thing beside the two that `conversion` and the verdict of the
whole configuration answer, because it lives for a third length of time. A
conversion is answered by one node alone and stays true until that node is
edited; a verdict is dropped by any edit anywhere; and this is dropped by
an edit inside the object it came from and by nothing else, which is the
same lifetime as the state above it and for the same reason.

<a id="edit_cfg_json.rows.MemberRow.has_objects"></a>

#### has\_objects

Whether a configuration object is at this node or inside it.

A nested configuration object has it, and so does a list or a dict that
holds them, at any depth. It is what a backend asks before it creates the
widget that says what those objects are: a widget which could never hold
anything is a piece of the window spent on nothing.

A member declared to hold an object and holding none has it false, because
there is no object there to ask about.

<a id="edit_cfg_json.rows.MemberRow.found"></a>

#### found

Whether this is the node that the search has got to.

A search is what a configuration too big for a window needs, and what it
reaches is one node at a time: this is that node, and every other node of
a search that reaches several of them says nothing. It is written onto the
rows rather than carried by them, exactly as the fold state is, because a
search outlives the rows that a validation pass replaces.

<a id="edit_cfg_json.rows.MemberRow.declared"></a>

#### declared

What the class that owns this node says the value here is.

A member of a configuration is declared by the class that owns it, and
what the declaration says is read from the attribute type rather than from
the value: `self.ratio: float = 0` is a number member however its default
is written, and `self.title: Optional[str] = None` is a text member that
may hold nothing while it holds nothing at all. A value inside a list or a
dict is answered by what the declaration of the member says is inside it.

It is empty wherever nothing says anything, which is a member with no
annotation, a class whose source cannot be read, and an annotation naming
a class of the application's own. The value the node held is what answers
then, exactly as it always did.

<a id="edit_cfg_json.rows.MemberRow.offer"></a>

#### offer

What can be done here about how many things this node holds.

Whether an element can be added, whether this node is an element that can
be taken out of what holds it, whether it can change places with a
neighbour, and why none of that is offered where none of it is. Most nodes
offer nothing: a value is not something that holds elements, and the
members of a configuration object are the ones its class declares.

It belongs to the model rather than to a backend for the same reason the
fold state does: two user interfaces of one application that offered to
change different things would be worse than either behaviour.

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

<a id="edit_cfg_json.rows.MemberRow.is_object"></a>

#### is\_object

```python
@property
def is_object() -> bool
```

Return whether a configuration object is really at this node.

A member declared to hold one and holding none is not, because it has
a class and no object, and everything the editor asks of such a node
is asked of the object that is not there.

<a id="edit_cfg_json.rows.MemberRow.holds_nothing"></a>

#### holds\_nothing

```python
@property
def holds_nothing() -> bool
```

Return whether this member is in the state of holding no value.

A member whose class declares that it may hold nothing has two states
rather than one, and this is the second of them. It is not a value
being typed and it is not a value of the wrong kind: it is the member
holding nothing, which is what the class allowed it to do, and it is
told apart from an empty text by being a state and not a text.

Which state it is in is changed by the two controls that change how
many things a node holds and by nothing else, so a field can never
take itself away from under the cursor that is typing in it.

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
becomes a configuration object, and neither is a member that holds
nothing, because the value it would hold is asked for and not typed.

The rows below it are asked as well as the value it was compared
against, because a member that may hold nothing held nothing then and
holds a list of rows now. Neither of them is the value it holds this
moment, which is what every keystroke changes: text that happens to be
JSON for a list would otherwise take the field away while it was being
typed.

<a id="edit_cfg_json.rows.MemberRow.kind"></a>

#### kind

```python
@property
def kind() -> Optional[type]
```

Return which kind of value this node takes, None where unknown.

What the class declared wins over what the node held, which is the
whole of what more type information buys: a member declared `float`
takes a number however its default was written, and a member that
holds nothing still says what it would hold.

<a id="edit_cfg_json.rows.MemberRow.is_text"></a>

#### is\_text

```python
@property
def is_text() -> bool
```

Return whether this node takes text.

This is the difference between a value that is text and a value
whose text is a rendering of it. The text of a text value is the
value itself, while the text of a number is how the number is
written.

<a id="edit_cfg_json.rows.MemberRow.is_bool"></a>

#### is\_bool

```python
@property
def is_bool() -> bool
```

Return whether this node takes true or false.

It is what makes the two words the values this node takes, so that
any beginning of either of them is one of them and anything else is
neither. A node whose kind nothing says is not one of these: nothing
is known, so nothing is refused.

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
class is missing, and a member that holds no value says that it holds
none. A list or a dict says how much it holds, because its value is on
the rows below it. Every other node shows the text of the value it
holds.

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

Every node that the file holds no key for while it holds nothing.

A member its own class may leave out is one, and a key that a class
declared a configuration object at is the other.

<a id="edit_cfg_json.rows.RowContext.offers"></a>

#### offers

What each node offers about the elements it holds, by its path.

<a id="edit_cfg_json.rows.RowContext.types"></a>

#### types

What the class owning each node says the value there is.

<a id="edit_cfg_json.rows.RowContext.refreshing"></a>

#### refreshing

Whether these rows are what a validation pass left behind.

A pass is not read only, so a node whose value it changed is marked, and a
node it created is marked as well: a validator that normalizes a list can
make one. Every other rebuild is a change the user asked for — an element
added, removed or moved — and marking that as a validator's work would be
telling the user that something happened to what they just did.

<a id="edit_cfg_json.rows.built_rows"></a>

#### built\_rows

```python
def built_rows(config: Config,
               *,
               members: Mapping[str, JsonType],
               report: LoadReport,
               descriptions: Descriptions,
               previous: Mapping[ConfigPath, MemberRow],
               defaults: Mapping[str, JsonType] = MappingProxyType({}),
               refreshing: bool = False) -> dict[ConfigPath, MemberRow]
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
- `defaults` - The values that the class of the configuration declares,
  which is what a new element of an ordinary list is copied from.
- `refreshing` - Whether these rows are what a validation pass left behind,
  which is what decides whether a node it changed is marked.
  

**Returns**:

  The rows of that configuration, by path.

<a id="edit_cfg_json.rows.BufferState"></a>

## BufferState Objects

```python
class BufferState(NamedTuple)
```

What the buffer knows about the rows rather than about one row.

Each of these outlives the rows it is about, because the rows are built
again after every validation pass and after every change of how many
elements a container holds: what the user folded, what each object said
about itself and what a search has got to are all older than the rows they
are written onto.

<a id="edit_cfg_json.rows.BufferState.folded"></a>

#### folded

Paths of the containers that are folded away.

<a id="edit_cfg_json.rows.BufferState.answers"></a>

#### answers

What each object that has been asked said about itself, by path.

<a id="edit_cfg_json.rows.BufferState.found"></a>

#### found

Path of the node the search has got to, None when it is at none.

<a id="edit_cfg_json.rows.stamped"></a>

#### stamped

```python
def stamped(rows: Mapping[ConfigPath, MemberRow],
            state: BufferState) -> dict[ConfigPath, MemberRow]
```

Return the rows with the state of the buffer written onto them.

A backend reads what is folded, what is shown, what the configuration
objects amount to and what a search has got to from the row each of those
is about, exactly as it reads the marks and the description from there, so
that the two backends cannot fold, hide, judge or find different things.

They are written here rather than carried by the rows they are about,
because they belong to the buffer: the rows are built again after every
validation pass, and a fold the user asked for, an answer an object gave
and a node a search reached all outlive the rows that were there then.

**Arguments**:

- `rows` - The rows of the configuration, by path.
- `state` - What the buffer knows that is written onto them.
  

**Returns**:

  The same rows, each saying whether it is folded, whether it shows,
  what the configuration objects at or inside it are on their own, and
  whether it is the node the search has got to.

<a id="edit_cfg_json.constructing"></a>

# edit\_cfg\_json.constructing

Building the configuration objects that the editor works with.

There are two of them, and only one of them asks the class for anything.

**An object that did not exist before.** The declared defaults and the values
of an input file both need one, and only the class can make one. More than one
constructor shape is in use, so every parameter this module knows the meaning
of is passed when the class declares it and left out when it does not, which is
principle 4 of section 3 of `doc/detailed_design.md` applied to a constructor:
what cannot be said is not said, and the editor is then only less pleasant
rather than unusable.

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
any member and it is never nothing, which is what it is for: a program that is
told a class and no mapping would otherwise show the members with nothing under
them at all, and the editor does know something about each of them.

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

What the editor says about a node the file need not hold a key for.

`_omit_none_from_json()` says which members those are and a
`DICT_VALUE_BY_KEY` declaration says which keys of a dict are, and
`tree.omitted_paths` is what reads both: they are sources of the structure by
section 4.1 of `doc/detailed_design.md`, so they are read where the rest of the
structure is. What is worth saying here is that a node which may be left out
is a node a user may leave empty.

<a id="edit_cfg_json.descriptions.NOTHING_TEXT"></a>

#### NOTHING\_TEXT

What the editor says about a member declared to allow no value.

`Optional[str]` is what says it, and the member then has two states rather
than one: it holds a value, or it holds nothing, and which of them it is in is
something the user can change. It is not said together with the line above it,
which says the same thing about the file and says more: a member left out of
the file is a member holding nothing, written the way that class writes it.

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

It is what says the kind of the value wherever the declaration of the
member says nothing, which is a class whose source cannot be read and a
member with no annotation at all.

<a id="edit_cfg_json.descriptions.MemberFacts.declared"></a>

#### declared

What the class that owns this node says the value here is.

It wins over the value, because a member declared `float` whose default is
written `0` is a number member whatever the value says, and a member that
holds nothing has a kind only if its declaration gives it one.

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
leave it out of the file altogether, or that it may hold nothing.

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

There are four passes here and they answer four different questions. What
the text of each member means is answered first, by the parse converter the
class declared for that member, because a value that does not exist cannot be
validated and the message the configuration class prints for one is about
JSON rather than about the member. What the application makes of the whole
buffer is answered next, by applying it to a candidate configuration, which is
the pass that decides whether the buffer is valid at all. And when that pass
refuses, the plan is walked a third time to say which members it was about,
because `Config.validate()` stops at the first step that refuses and can
therefore report one failure and never say whose it was.

The fourth is every nested configuration object asked on its own, and it
answers what the third one cannot reach. Such an object validates itself while
`parse_json` builds it, so a refusal from inside it keeps the walk above from
ever holding an object to walk: the probe is a copy of the configuration with
one method left out, and the nested objects inside that copy are built by the
library and validate themselves as they always do. Applying one subtree of the
buffer to the object that owns it is what reaches them, and it answers the
other question a nested object raises as well — whether it is a configuration
on its own, which is what its row says while the whole configuration is
refused for a reason that is about something else entirely.

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

<a id="edit_cfg_json.validation.SubtreeAnswer"></a>

## SubtreeAnswer Objects

```python
class SubtreeAnswer(NamedTuple)
```

What asking one nested configuration object about itself found.

<a id="edit_cfg_json.validation.SubtreeAnswer.valid"></a>

#### valid

Whether that object is a configuration on its own.

<a id="edit_cfg_json.validation.SubtreeAnswer.refused"></a>

#### refused

What it refused, by the absolute path of the node it is about.

It is a member of that object wherever a member validator refused one, and
the object itself where its class refused it for a reason that is about no
member of it. It is empty for an object that was accepted, and empty for
one that is refused only because an object inside it is: that mistake is
reported once, at the object it is really about.

It is kept beside the state rather than thrown away, because the state on
its own says that something is wrong and never says what, and a user who
folds an object to be told that much has to open it again and ask a second
question to find out.

<a id="edit_cfg_json.validation.NO_SUBTREES"></a>

#### NO\_SUBTREES

What a pass over a configuration with no nested object at all reports.

It cannot be written to, for the same reason as the mapping above.

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

<a id="edit_cfg_json.validation.ValidationPass.subtrees"></a>

#### subtrees

What each nested object is on its own, by the path of its node.

A subtree can be valid while the whole configuration is not, which is what
a rule relating two of them across the boundary does, and that is the
honest state rather than a contradiction. It is a different question from
the verdict and it is answered separately, so a row can say what its own
object amounts to without saying anything about the file.

A member declared to hold an object and holding none is not here, because
there is nothing to validate; and a pass the class accepted answers for
every one of them at once, since `parse_json` built and validated each of
them while it read the buffer.

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

<a id="edit_cfg_json.validation.subtree_answers"></a>

#### subtree\_answers

```python
def subtree_answers(
    config: Config,
    members: dict[str, JsonType],
    inside: ConfigPath = (),
    bool_nodes: frozenset[ConfigPath] = frozenset()
) -> dict[ConfigPath, SubtreeAnswer]
```

Return what every nested object of one region says about itself.

This is what folding asks, and it is the cheap local question that
section 6.2 of `doc/detailed_design.md` makes folding the trigger for: it
needs no candidate configuration and says nothing about the file.

A region and not a single node, because the member that holds several
configuration objects is a list or a dict and is no configuration itself.
Folding one of those hides every object in it, so folding one of those has
to ask every object in it; asking only the node that was folded would
answer nothing at all for exactly the shape a real configuration has.

**Arguments**:

- `config` - Configuration object of this session, which says which nodes
  are configuration objects of their own. It is not modified.
- `members` - The edit buffer, as one JSON space value per member.
- `inside` - Path of the node being asked about, the empty path for the
  whole configuration. Every object at or inside it is asked.
- `bool_nodes` - Path of every node that holds true or false, empty for a
  caller that knows of none.
  

**Returns**:

  One answer per nested object of that region that is really there. A
  member declared to hold an object and holding none is not here,
  because there is nothing to ask.

<a id="edit_cfg_json.validation.validate_buffer"></a>

#### validate\_buffer

```python
def validate_buffer(
    config: Config,
    members: dict[str, JsonType],
    bool_nodes: frozenset[ConfigPath] = frozenset()
) -> ValidationPass
```

Validate one edit buffer, and every nested object of it on its own.

The whole buffer decides the verdict, by `_single_pass`, which is the
application's own reading of its own file and the only thing that says
whether these values could be saved. Each nested configuration object is
then asked the same question about the part of the buffer it owns, which
answers the two things that pass cannot.

It says whether that object is a configuration on its own, which is a
different state from the verdict and has to be shown as one: a rule of the
class above relates two objects across the boundary between them, so both
of them can be valid while the configuration is refused.

And it says which member of a nested object was refused. Such an object
validates itself while `parse_json` builds it, so the walk of section 6.3
of `doc/detailed_design.md` never gets an object to walk and would leave
the message in the block below the members. Applying the subtree to the
object that owns it is what reaches the member.

None of that is asked of a pass the class accepted: `parse_json` built and
validated every nested object while it read the buffer, so all of them are
valid and there is nothing left to find out.

**Arguments**:

- `config` - Configuration object of this session, which says which class
  the buffer belongs to and holds everything about it that is not a
  member. It is not modified.
- `members` - The edit buffer, as one JSON space value per member.
- `bool_nodes` - Path of every node that holds true or false, empty for a
  caller that knows of none. The values are in JSON space, where
  nothing says which member takes those two and only those two.
  

**Returns**:

  What the pass found, the members of the configuration object it built,
  and what each nested object is on its own.

