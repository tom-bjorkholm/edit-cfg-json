# Table of Contents

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
  * [OLD\_FORMAT\_FORM](#edit_cfg_json.loading.OLD_FORMAT_FORM)
  * [SUPPLIED\_FORM](#edit_cfg_json.loading.SUPPLIED_FORM)
  * [LoadPolicy](#edit_cfg_json.loading.LoadPolicy)
    * [STRICT](#edit_cfg_json.loading.LoadPolicy.STRICT)
    * [DEFAULTS](#edit_cfg_json.loading.LoadPolicy.DEFAULTS)
    * [STRICT\_THEN\_DEFAULTS](#edit_cfg_json.loading.LoadPolicy.STRICT_THEN_DEFAULTS)
  * [DEFAULT\_POLICY](#edit_cfg_json.loading.DEFAULT_POLICY)
  * [LoadReport](#edit_cfg_json.loading.LoadReport)
    * [message](#edit_cfg_json.loading.LoadReport.message)
    * [filled](#edit_cfg_json.loading.LoadReport.filled)
    * [changed](#edit_cfg_json.loading.LoadReport.changed)
  * [LoadedConfig](#edit_cfg_json.loading.LoadedConfig)
    * [config](#edit_cfg_json.loading.LoadedConfig.config)
    * [report](#edit_cfg_json.loading.LoadedConfig.report)
  * [ConfigLoadError](#edit_cfg_json.loading.ConfigLoadError)
    * [\_\_init\_\_](#edit_cfg_json.loading.ConfigLoadError.__init__)
  * [\_explained](#edit_cfg_json.loading._explained)
  * [\_no\_defaults](#edit_cfg_json.loading._no_defaults)
  * [\_type\_refusal](#edit_cfg_json.loading._type_refusal)
  * [\_attempt](#edit_cfg_json.loading._attempt)
  * [\_named](#edit_cfg_json.loading._named)
  * [\_change\_lines](#edit_cfg_json.loading._change_lines)
  * [\_report](#edit_cfg_json.loading._report)
  * [\_permissive](#edit_cfg_json.loading._permissive)
  * [\_rescue](#edit_cfg_json.loading._rescue)
  * [\_load\_text](#edit_cfg_json.loading._load_text)
  * [default\_config](#edit_cfg_json.loading.default_config)
  * [\_file\_text](#edit_cfg_json.loading._file_text)
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
  * [\_failed](#edit_cfg_json.saving._failed)
  * [reload\_refusal](#edit_cfg_json.saving.reload_refusal)
  * [write\_config](#edit_cfg_json.saving.write_config)
* [edit\_cfg\_json.converting](#edit_cfg_json.converting)
  * [CONVERSION\_ERRORS](#edit_cfg_json.converting.CONVERSION_ERRORS)
  * [Converted](#edit_cfg_json.converting.Converted)
    * [value](#edit_cfg_json.converting.Converted.value)
    * [message](#edit_cfg_json.converting.Converted.message)
  * [member\_converters](#edit_cfg_json.converting.member_converters)
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
  * [\_Refusal](#edit_cfg_json.cli._Refusal)
    * [\_\_init\_\_](#edit_cfg_json.cli._Refusal.__init__)
  * [\_default\_policy\_name](#edit_cfg_json.cli._default_policy_name)
  * [named\_policy](#edit_cfg_json.cli.named_policy)
  * [add\_file\_options](#edit_cfg_json.cli.add_file_options)
  * [\_create\_parser](#edit_cfg_json.cli._create_parser)
  * [\_said](#edit_cfg_json.cli._said)
  * [\_imported\_module](#edit_cfg_json.cli._imported_module)
  * [\_python\_file](#edit_cfg_json.cli._python_file)
  * [\_module\_from\_file](#edit_cfg_json.cli._module_from_file)
  * [\_class\_in](#edit_cfg_json.cli._class_in)
  * [\_loader\_in](#edit_cfg_json.cli._loader_in)
  * [\_named\_module](#edit_cfg_json.cli._named_module)
  * [\_constructed](#edit_cfg_json.cli._constructed)
  * [\_loader\_config](#edit_cfg_json.cli._loader_config)
  * [\_target\_config](#edit_cfg_json.cli._target_config)
  * [\_checked\_class](#edit_cfg_json.cli._checked_class)
  * [\_built\_model](#edit_cfg_json.cli._built_model)
  * [\_outcome](#edit_cfg_json.cli._outcome)
  * [\_session](#edit_cfg_json.cli._session)
  * [run\_cli](#edit_cfg_json.cli.run_cli)
* [edit\_cfg\_json.leaf\_value](#edit_cfg_json.leaf_value)
  * [value\_as\_text](#edit_cfg_json.leaf_value.value_as_text)
  * [text\_as\_value](#edit_cfg_json.leaf_value.text_as_value)
  * [values\_differ](#edit_cfg_json.leaf_value.values_differ)
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
* [edit\_cfg\_json.settings](#edit_cfg_json.settings)
  * [DUPLICATE\_KEY](#edit_cfg_json.settings.DUPLICATE_KEY)
  * [NOT\_AN\_EXTENSION](#edit_cfg_json.settings.NOT_AN_EXTENSION)
  * [WRONG\_EXTENSION](#edit_cfg_json.settings.WRONG_EXTENSION)
  * [\_duplicate](#edit_cfg_json.settings._duplicate)
  * [ActionSettings](#edit_cfg_json.settings.ActionSettings)
    * [quit](#edit_cfg_json.settings.ActionSettings.quit)
    * [validate](#edit_cfg_json.settings.ActionSettings.validate)
    * [save](#edit_cfg_json.settings.ActionSettings.save)
    * [save\_as](#edit_cfg_json.settings.ActionSettings.save_as)
    * [cancel](#edit_cfg_json.settings.ActionSettings.cancel)
    * [explain](#edit_cfg_json.settings.ActionSettings.explain)
    * [\_\_post\_init\_\_](#edit_cfg_json.settings.ActionSettings.__post_init__)
  * [Settings](#edit_cfg_json.settings.Settings)
    * [actions](#edit_cfg_json.settings.Settings.actions)
    * [file\_extension](#edit_cfg_json.settings.Settings.file_extension)
    * [extension\_enforced](#edit_cfg_json.settings.Settings.extension_enforced)
    * [\_\_post\_init\_\_](#edit_cfg_json.settings.Settings.__post_init__)
  * [current\_settings](#edit_cfg_json.settings.current_settings)
  * [CheckedFile](#edit_cfg_json.settings.CheckedFile)
    * [name](#edit_cfg_json.settings.CheckedFile.name)
    * [message](#edit_cfg_json.settings.CheckedFile.message)
  * [\_matches](#edit_cfg_json.settings._matches)
  * [\_refused](#edit_cfg_json.settings._refused)
  * [checked\_file](#edit_cfg_json.settings.checked_file)
  * [chosen\_file](#edit_cfg_json.settings.chosen_file)
* [edit\_cfg\_json.model\_text](#edit_cfg_json.model_text)
  * [NOT\_EDITABLE\_FORM](#edit_cfg_json.model_text.NOT_EDITABLE_FORM)
  * [EDITED\_MARK](#edit_cfg_json.model_text.EDITED_MARK)
  * [VALIDATOR\_MARK](#edit_cfg_json.model_text.VALIDATOR_MARK)
  * [FILLED\_MARK](#edit_cfg_json.model_text.FILLED_MARK)
  * [LOAD\_MARK](#edit_cfg_json.model_text.LOAD_MARK)
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
  * [row\_value\_text](#edit_cfg_json.model_text.row_value_text)
  * [row\_marks](#edit_cfg_json.model_text.row_marks)
  * [docstring\_text](#edit_cfg_json.model_text.docstring_text)
  * [row\_description](#edit_cfg_json.model_text.row_description)
  * [row\_diagnostic](#edit_cfg_json.model_text.row_diagnostic)
  * [\_indented](#edit_cfg_json.model_text._indented)
  * [\_row\_as\_text](#edit_cfg_json.model_text._row_as_text)
  * [\_state\_line](#edit_cfg_json.model_text._state_line)
  * [verdict\_text](#edit_cfg_json.model_text.verdict_text)
  * [load\_text](#edit_cfg_json.model_text.load_text)
  * [save\_text](#edit_cfg_json.model_text.save_text)
  * [\_head\_text](#edit_cfg_json.model_text._head_text)
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
  * [NOT\_EDITABLE\_ERROR](#edit_cfg_json.edit_model.NOT_EDITABLE_ERROR)
  * [MemberRow](#edit_cfg_json.edit_model.MemberRow)
    * [path](#edit_cfg_json.edit_model.MemberRow.path)
    * [value](#edit_cfg_json.edit_model.MemberRow.value)
    * [original](#edit_cfg_json.edit_model.MemberRow.original)
    * [changed\_by\_validator](#edit_cfg_json.edit_model.MemberRow.changed_by_validator)
    * [filled\_from\_default](#edit_cfg_json.edit_model.MemberRow.filled_from_default)
    * [changed\_by\_load](#edit_cfg_json.edit_model.MemberRow.changed_by_load)
    * [description](#edit_cfg_json.edit_model.MemberRow.description)
    * [converter](#edit_cfg_json.edit_model.MemberRow.converter)
    * [conversion](#edit_cfg_json.edit_model.MemberRow.conversion)
    * [name](#edit_cfg_json.edit_model.MemberRow.name)
    * [editable](#edit_cfg_json.edit_model.MemberRow.editable)
    * [is\_text](#edit_cfg_json.edit_model.MemberRow.is_text)
    * [edited](#edit_cfg_json.edit_model.MemberRow.edited)
  * [\_ordered\_names](#edit_cfg_json.edit_model._ordered_names)
  * [\_row\_of](#edit_cfg_json.edit_model._row_of)
  * [\_rows\_from\_config](#edit_cfg_json.edit_model._rows_from_config)
  * [\_refreshed](#edit_cfg_json.edit_model._refreshed)
  * [EditModel](#edit_cfg_json.edit_model.EditModel)
    * [\_\_init\_\_](#edit_cfg_json.edit_model.EditModel.__init__)
    * [\_config\_type](#edit_cfg_json.edit_model.EditModel._config_type)
    * [config\_type\_name](#edit_cfg_json.edit_model.EditModel.config_type_name)
    * [summary](#edit_cfg_json.edit_model.EditModel.summary)
    * [docstring](#edit_cfg_json.edit_model.EditModel.docstring)
    * [explanations\_shown](#edit_cfg_json.edit_model.EditModel.explanations_shown)
    * [toggle\_explanations](#edit_cfg_json.edit_model.EditModel.toggle_explanations)
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
    * [\_validation\_pass](#edit_cfg_json.edit_model.EditModel._validation_pass)
    * [\_check\_fields](#edit_cfg_json.edit_model.EditModel._check_fields)
    * [\_record](#edit_cfg_json.edit_model.EditModel._record)
    * [\_keep\_saved](#edit_cfg_json.edit_model.EditModel._keep_saved)
    * [\_buffer](#edit_cfg_json.edit_model.EditModel._buffer)
    * [\_take\_validated](#edit_cfg_json.edit_model.EditModel._take_validated)
* [edit\_cfg\_json.constructing](#edit_cfg_json.constructing)
  * [HOOK\_NAME](#edit_cfg_json.constructing.HOOK_NAME)
  * [STREAM\_NAME](#edit_cfg_json.constructing.STREAM_NAME)
  * [FILE\_NAME](#edit_cfg_json.constructing.FILE_NAME)
  * [JSON\_TEXT\_NAMES](#edit_cfg_json.constructing.JSON_TEXT_NAMES)
  * [\_arguments](#edit_cfg_json.constructing._arguments)
  * [built\_config](#edit_cfg_json.constructing.built_config)
  * [parsed\_config](#edit_cfg_json.constructing.parsed_config)
* [edit\_cfg\_json.\_\_main\_\_](#edit_cfg_json.__main__)
  * [PROGRAM](#edit_cfg_json.__main__.PROGRAM)
  * [main](#edit_cfg_json.__main__.main)
* [edit\_cfg\_json.descriptions](#edit_cfg_json.descriptions)
  * [EVERY\_ELEMENT](#edit_cfg_json.descriptions.EVERY_ELEMENT)
  * [CHOICES\_FORM](#edit_cfg_json.descriptions.CHOICES_FORM)
  * [\_selects](#edit_cfg_json.descriptions._selects)
  * [\_named\_steps](#edit_cfg_json.descriptions._named_steps)
  * [path\_description](#edit_cfg_json.descriptions.path_description)
  * [class\_docstring](#edit_cfg_json.descriptions.class_docstring)
  * [class\_summary](#edit_cfg_json.descriptions.class_summary)
  * [\_enum\_type](#edit_cfg_json.descriptions._enum_type)
  * [enum\_text](#edit_cfg_json.descriptions.enum_text)
  * [member\_description](#edit_cfg_json.descriptions.member_description)
* [edit\_cfg\_json.auto\_change](#edit_cfg_json.auto_change)
  * [WRITE\_ERRORS](#edit_cfg_json.auto_change.WRITE_ERRORS)
  * [PARSE\_ERRORS](#edit_cfg_json.auto_change.PARSE_ERRORS)
  * [KEY\_METHOD](#edit_cfg_json.auto_change.KEY_METHOD)
  * [RECORDED](#edit_cfg_json.auto_change.RECORDED)
  * [ChangeReport](#edit_cfg_json.auto_change.ChangeReport)
    * [\_\_deepcopy\_\_](#edit_cfg_json.auto_change.ChangeReport.__deepcopy__)
  * [FileChanges](#edit_cfg_json.auto_change.FileChanges)
    * [filled](#edit_cfg_json.auto_change.FileChanges.filled)
    * [dropped](#edit_cfg_json.auto_change.FileChanges.dropped)
    * [changed](#edit_cfg_json.auto_change.FileChanges.changed)
    * [old\_keys](#edit_cfg_json.auto_change.FileChanges.old_keys)
    * [supplied](#edit_cfg_json.auto_change.FileChanges.supplied)
    * [anything](#edit_cfg_json.auto_change.FileChanges.anything)
  * [\_canonical](#edit_cfg_json.auto_change._canonical)
  * [\_written](#edit_cfg_json.auto_change._written)
  * [\_held](#edit_cfg_json.auto_change._held)
  * [\_altered](#edit_cfg_json.auto_change._altered)
  * [\_ParsedKeys](#edit_cfg_json.auto_change._ParsedKeys)
    * [\_\_init\_\_](#edit_cfg_json.auto_change._ParsedKeys.__init__)
  * [\_record\_keys](#edit_cfg_json.auto_change._record_keys)
  * [\_filled](#edit_cfg_json.auto_change._filled)
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
  * [\_told](#edit_cfg_json.validation._told)
  * [PLAN\_METHOD](#edit_cfg_json.validation.PLAN_METHOD)
  * [\_no\_plan](#edit_cfg_json.validation._no_plan)
  * [\_probe](#edit_cfg_json.validation._probe)
  * [\_unconverted](#edit_cfg_json.validation._unconverted)
  * [\_attribute\_member](#edit_cfg_json.validation._attribute_member)
  * [\_attribute\_step](#edit_cfg_json.validation._attribute_step)
  * [\_step\_refusal](#edit_cfg_json.validation._step_refusal)
  * [\_plan\_failures](#edit_cfg_json.validation._plan_failures)
  * [\_attribution](#edit_cfg_json.validation._attribution)
  * [\_refused\_verdict](#edit_cfg_json.validation._refused_verdict)
  * [\_no\_pass](#edit_cfg_json.validation._no_pass)
  * [validate\_buffer](#edit_cfg_json.validation.validate_buffer)

<a id="edit_cfg_json.loading"></a>

# edit\_cfg\_json.loading

Reading the configuration to edit from one input file.

The editor constructs the configuration object rather than receiving one that
is already loaded. Both of the things a load has to be told are given to a
constructor and to nothing else: the hook that reports the automatic changes
of an old format file, and the policy for declared keys the file does not
contain.

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

<a id="edit_cfg_json.loading.OLD_FORMAT_FORM"></a>

#### OLD\_FORMAT\_FORM

Form of the line that names the older keys that the load accepted.

It says what the line above it says and says why as well, so the two are never
both shown: a class that reported its own automatic changes has explained the
keys of its file, and the editor's own reading of them would only repeat it.

<a id="edit_cfg_json.loading.SUPPLIED_FORM"></a>

#### SUPPLIED\_FORM

Form of the line naming what the rules for an older format supplied.

Neither the file nor the declared defaults gave these values. The
configuration class did, because the file is too old to hold them at all.

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

<a id="edit_cfg_json.loading.LoadReport.changed"></a>

#### changed

Names of the members whose value the load itself put there or altered.

Reading a file is not always only reading it: the rules a class declares
for an older format may have supplied a value or renamed a key into a
member, and parsing or validating may have normalized one. The model marks
the row of each of these too, so that a value which is not the one in the
file can be seen to be one. A member the declared defaults filled in is
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

<a id="edit_cfg_json.loading._explained"></a>

#### \_explained

```python
def _explained(said: StringIO, error: Exception) -> str
```

Return what a failed load has to say for itself.

A failure that wrote nothing has only its exception left to report,
which is better than no explanation at all.

**Arguments**:

- `said` - Stream that collected what the configuration class said.
- `error` - The failure that the class reported.
  

**Returns**:

  The diagnostics of one failure.

<a id="edit_cfg_json.loading._no_defaults"></a>

#### \_no\_defaults

```python
def _no_defaults(source: ConfigSource, said: StringIO,
                 error: Exception) -> ConfigLoadError
```

Return the refusal of a configuration the editor cannot construct.

**Arguments**:

- `source` - Configuration being loaded, and how it is constructed.
- `said` - Stream that collected what the construction said.
- `error` - The failure that it reported.
  

**Returns**:

  The refusal to report for it.

<a id="edit_cfg_json.loading._type_refusal"></a>

#### \_type\_refusal

```python
def _type_refusal(source: ConfigSource, said: StringIO,
                  error: TypeError) -> ConfigLoadError
```

Return what one `TypeError` during a load amounts to.

It can mean two quite different things: a configuration this editor cannot
construct at all, and a value of the file that is of a type the class
refuses. The two are told apart the same way the two kinds of `KeyError`
are, by trying the construction that answers it — here a construction with
no file at all, which succeeds for a class whose own values are fine and
fails for one that needs an argument nobody has.

**Arguments**:

- `source` - Configuration being loaded, and how it is constructed.
- `said` - Stream that collected what the load said.
- `error` - The failure that the load reported.
  

**Returns**:

  The refusal to report for it.

<a id="edit_cfg_json.loading._attempt"></a>

#### \_attempt

```python
def _attempt(source: ConfigSource, text: str, ok_to_use_defaults: bool,
             said: StringIO, hook: ChangeReport) -> Config
```

Try once to build one configuration object from one file text.

The stream is the caller's, because a key that does not match is
reported to the caller and what was said about it is needed there. The
hook is the caller's for the same reason: what it collects is what the
caller reports about the load that succeeded.

**Arguments**:

- `source` - Configuration being loaded, and how it is constructed.
- `text` - The whole text of the input file.
- `ok_to_use_defaults` - Whether the declared defaults may fill in the
  keys the file does not hold.
- `said` - Stream that collects what the class says about the file.
- `hook` - Hook that collects the automatic changes of this attempt.
  

**Returns**:

  A configuration object holding the values of the file.
  

**Raises**:

- `KeyError` - The keys of the file do not match the declared members.
- `ConfigLoadError` - The file cannot be opened for editing.

<a id="edit_cfg_json.loading._named"></a>

#### \_named

```python
def _named(names: Iterable[str]) -> str
```

Return several names as one piece of text, in a settled order.

The order is the sorted one and not the one they were collected in,
because a list of names that is read is easier to look something up in
than one that records the order in which rules happened to run.

**Arguments**:

- `names` - Names to write out.
  

**Returns**:

  Those names, separated by commas.

<a id="edit_cfg_json.loading._change_lines"></a>

#### \_change\_lines

```python
def _change_lines(changes: FileChanges) -> list[str]
```

Return what a load that changed its file has to say about that.

**Arguments**:

- `changes` - What the load did to the file it read.
  

**Returns**:

  The lines to tell the user, and nothing at all for a load that left
  the file as it found it.

<a id="edit_cfg_json.loading._report"></a>

#### \_report

```python
def _report(config: Config, text: str, said: str, hook: ChangeReport,
            permissive: bool) -> LoadReport
```

Return what one load did beyond reading the values of its file.

The order of what is said follows the order in which it happened: what the
file did not hold, then what reading it changed, and then whatever the
configuration class itself said while it read.

**Arguments**:

- `config` - Configuration object that the load built.
- `text` - The whole text of the input file.
- `said` - What the configuration class said about the file.
- `hook` - Hook that collected the automatic changes of this load.
- `permissive` - Whether the load was allowed to fill in what the file
  left out.
  

**Returns**:

  The report of one load.

<a id="edit_cfg_json.loading._permissive"></a>

#### \_permissive

```python
def _permissive(source: ConfigSource, text: str) -> LoadedConfig
```

Load one file text with the defaults filling in what it lacks.

A key the configuration does not declare is still refused, because
filling in governs the keys that are missing and nothing else. Dropping
an unknown key would lose whatever the file meant by it, and such a file
is either from a newer version or has a misspelled key in it.

**Arguments**:

- `source` - Configuration being loaded, and how it is constructed.
- `text` - The whole text of the input file.
  

**Returns**:

  The configuration object, and what filling in did to its values.
  

**Raises**:

- `ConfigLoadError` - The file cannot be opened for editing.

<a id="edit_cfg_json.loading._rescue"></a>

#### \_rescue

```python
def _rescue(source: ConfigSource, text: str, policy: LoadPolicy,
            said: str) -> LoadedConfig
```

Retry a load that the keys of the file made fail.

The retry is what tells the two failures apart that `check_key_match`
reports as the same `KeyError`. A retry that succeeds says the file was
incomplete, and a retry that fails again says the file holds a key that
is not declared here. An incomplete file is opened under
`STRICT_THEN_DEFAULTS` and refused under `STRICT`, which is the whole
difference between those two policies.

**Arguments**:

- `source` - Configuration being loaded, and how it is constructed.
- `text` - The whole text of the input file.
- `policy` - What to do about declared keys the file does not hold.
- `said` - What the class said about the load that failed.
  

**Returns**:

  The configuration object of the retry, and what the retry did.
  

**Raises**:

- `ConfigLoadError` - The file cannot be opened for editing.

<a id="edit_cfg_json.loading._load_text"></a>

#### \_load\_text

```python
def _load_text(source: ConfigSource, text: str,
               policy: LoadPolicy) -> LoadedConfig
```

Load one file text under one policy, or refuse to open the file.

**Arguments**:

- `source` - Configuration being loaded, and how it is constructed.
- `text` - The whole text of the input file.
- `policy` - What to do about declared keys the file does not hold.
  

**Returns**:

  The configuration object, and what the load did to its values.
  

**Raises**:

- `ConfigLoadError` - The file cannot be opened for editing.

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
with the same diagnostics, and the hook that reports the automatic changes
of an old format file reaches a class that declares it. Nothing reads that
hook here, because there is no file to read and therefore nothing for it to
report.

An application whose class needs a constructor argument this library knows
nothing about has a loader instead, and calls that with no JSON source.

**Arguments**:

- `config_type` - Class to construct with no JSON source, which leaves it
  holding only what it declares.
  

**Returns**:

  A configuration object holding the declared defaults of that class.
  

**Raises**:

- `ConfigLoadError` - The editor cannot construct this class.

<a id="edit_cfg_json.loading._file_text"></a>

#### \_file\_text

```python
def _file_text(in_file: PathOrStr) -> str
```

Return the whole text of one input file, or refuse to open it.

The file is read here and not by `Config.read()`, which ends the process
with `sys.exit` when the file is missing. An editor has to say so and
stay alive.

**Arguments**:

- `in_file` - File to read.
  

**Returns**:

  The whole text of that file.
  

**Raises**:

- `ConfigLoadError` - The file cannot be read.

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

<a id="edit_cfg_json.saving._failed"></a>

#### \_failed

```python
def _failed(name: PathOrStr, error: Exception) -> str
```

Return what a save that could not write the file has to say.

**Arguments**:

- `name` - File that the save was trying to write.
- `error` - The failure that writing it reported.
  

**Returns**:

  The message of one refused save.

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

<a id="edit_cfg_json.cli._Refusal"></a>

## \_Refusal Objects

```python
class _Refusal(Exception)
```

Refusal to run, with what to say about it and what to exit with.

It is internal because it exists only to carry the two together from
wherever the refusal is decided out to the one place that reports it.

<a id="edit_cfg_json.cli._Refusal.__init__"></a>

#### \_\_init\_\_

```python
def __init__(message: str, code: ExitCode) -> None
```

Say why the program cannot run and how it should end.

**Arguments**:

- `message` - What the user has to be told.
- `code` - What this run of the program ends with.

<a id="edit_cfg_json.cli._default_policy_name"></a>

#### \_default\_policy\_name

```python
def _default_policy_name() -> str
```

Return the `--policy` value that the editor uses when none is named.

It is looked up rather than written out, so that the default of the
editor stays the one and only source of it.

**Returns**:

  The name of the default load policy.

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

<a id="edit_cfg_json.cli._create_parser"></a>

#### \_create\_parser

```python
def _create_parser(prog: str, interactive: bool) -> ArgumentParser
```

Return the parser of one program of this library.

`--save` belongs to a program whose backend prints once and returns,
because there is then no later moment at which a user could press Save.
A program that opens an editor does not offer the option at all, so it is
`argparse` that refuses it rather than a check written by hand; the
default is set instead, so that the rest of this module can read it
either way.

**Arguments**:

- `prog` - Name that this program is installed under.
- `interactive` - Whether the backend of this program gives the user a
  session in which they could ask for a save themselves.
  

**Returns**:

  The parser for one program.

<a id="edit_cfg_json.cli._said"></a>

#### \_said

```python
def _said(message: str, error: Exception, captured: str = '') -> str
```

Return one refusal with what Python said about it below it.

**Arguments**:

- `message` - What the program has to tell the user.
- `error` - The failure that Python reported.
- `captured` - What the code that failed wrote to its own diagnostics
  stream, empty when it wrote nothing or was given none.
  

**Returns**:

  The message, whatever was said, and the failure below both.

<a id="edit_cfg_json.cli._imported_module"></a>

#### \_imported\_module

```python
def _imported_module(name: str) -> ModuleType
```

Return one importable module, or refuse to run.

**Arguments**:

- `name` - Name of the module, as an import statement would write it.
  

**Returns**:

  That module, imported.
  

**Raises**:

- `_Refusal` - The module cannot be imported.

<a id="edit_cfg_json.cli._python_file"></a>

#### \_python\_file

```python
def _python_file(path: Path) -> Path
```

Return one path that can be tried as a Python module, or refuse.

A file that is missing is a different mistake from a file that is not
Python, so the two are told apart before either of them is imported.

**Arguments**:

- `path` - Path that `--file` named.
  

**Returns**:

  That path.
  

**Raises**:

- `_Refusal` - The path is no Python file to import.

<a id="edit_cfg_json.cli._module_from_file"></a>

#### \_module\_from\_file

```python
def _module_from_file(path: Path) -> ModuleType
```

Return the module of one Python file, and leave no trace of it.

The folder of the file goes to the front of the path and the file is
imported by its own stem, so that a module which imports its siblings
works. Both of those are undone afterwards: the folder is taken off the
path again, and a module that was not already imported is forgotten, so
that a second file of the same stem is really imported rather than found
among the modules of the first. The class that was reached keeps working
either way, because a class carries the namespace it was defined in.

**Arguments**:

- `path` - Python file to import, which exists and ends in `.py`.
  

**Returns**:

  That file, imported as a module.
  

**Raises**:

- `_Refusal` - The file cannot be imported.

<a id="edit_cfg_json.cli._class_in"></a>

#### \_class\_in

```python
def _class_in(module: ModuleType, name: str) -> type[Config]
```

Return one configuration class of one module, or refuse to run.

**Arguments**:

- `module` - Module that was named on the command line.
- `name` - Name of the class that was asked for.
  

**Returns**:

  That class.
  

**Raises**:

- `_Refusal` - The module holds no such class.

<a id="edit_cfg_json.cli._loader_in"></a>

#### \_loader\_in

```python
def _loader_in(module: ModuleType, name: str) -> ConfigLoader
```

Return one configuration loader of one module, or refuse to run.

What can be checked here is that the name can be called at all. Whether it
takes the five keyword arguments of a loader is answered by calling it,
which is what `_loader_config` below does and reports.

**Arguments**:

- `module` - Module that was named on the command line.
- `name` - Name of the loader that was asked for.
  

**Returns**:

  That loader.
  

**Raises**:

- `_Refusal` - The module holds no such name, or it is nothing to call.

<a id="edit_cfg_json.cli._named_module"></a>

#### \_named\_module

```python
def _named_module(parsed: Namespace) -> ModuleType
```

Return the module that one command line names, or refuse to run.

**Arguments**:

- `parsed` - Parsed command line of one run.
  

**Returns**:

  That module, imported.
  

**Raises**:

- `_Refusal` - The module cannot be reached.

<a id="edit_cfg_json.cli._constructed"></a>

#### \_constructed

```python
def _constructed(config_type: type[Config]) -> Config
```

Return the declared defaults of one class, or refuse to run.

**Arguments**:

- `config_type` - Class that the command line named.
  

**Returns**:

  A configuration object holding what the class declares.
  

**Raises**:

- `_Refusal` - The editor cannot construct that class. An application
  whose class needs constructor arguments this library knows
  nothing about names a loader with `--loader` instead.

<a id="edit_cfg_json.cli._loader_config"></a>

#### \_loader\_config

```python
def _loader_config(loader: ConfigLoader, name: str) -> Config
```

Return what one loader answers with when there is no file, or refuse.

**Arguments**:

- `loader` - Loader that the command line named.
- `name` - Name it was named under, which is what a refusal says.
  

**Returns**:

  The configuration object that the loader constructed.
  

**Raises**:

- `_Refusal` - The loader cannot be called by a program, or it answered
  with nothing.

<a id="edit_cfg_json.cli._target_config"></a>

#### \_target\_config

```python
def _target_config(wanted: Optional[type[Config]],
                   loader: Optional[ConfigLoader],
                   name: Optional[str]) -> Config
```

Return the configuration object that one command line starts from.

A class alone is constructed on the values it declares. A loader is asked
instead, with no JSON source, which is what `ConfigLoader` says a loader
answers. Which class that is is not checked here, because it is not settled
yet: a loader may choose its class by looking at the input file, and the
class of the session is the class of the object the load produced.

**Arguments**:

- `wanted` - Class that `--class` named, or None when it named none. It is
  never None when there is no loader, because a command line that
  names neither is refused before this.
- `loader` - Loader that the command line named, or None when it named
  none.
- `name` - Name the loader was named under, which a refusal says.
  

**Returns**:

  The configuration object to start the session from.
  

**Raises**:

- `_Refusal` - There is no configuration object to edit.

<a id="edit_cfg_json.cli._checked_class"></a>

#### \_checked\_class

```python
def _checked_class(config: Config, wanted: Optional[type[Config]],
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

- `_Refusal` - The class is not the one that was asked for.

<a id="edit_cfg_json.cli._built_model"></a>

#### \_built\_model

```python
def _built_model(parsed: Namespace, config: Config,
                 loader: Optional[ConfigLoader],
                 wanted: Optional[type[Config]]) -> EditModel
```

Return the model of one session, on the files that were named.

The output file is set only when it was named, because the model already
writes the input file when nothing else was chosen. Naming it here counts
as choosing it, so it gets the extension of the application when it has
none of its own, exactly as `edit` does with the same argument.

Building the model serializes the configuration object, which is how the
editor reads the values it shows, and a class that cannot write itself as
JSON therefore has nothing for the editor to show. That is the class of a
configuration and not a mistake on the command line, so it is a refusal
here rather than the exception that `EditModel` documents for an
application that builds the model itself and knows its own class.

**Arguments**:

- `parsed` - Parsed command line of one run.
- `config` - Configuration object holding the values to start from.
- `loader` - Loader that the command line named, or None when it named
  none.
- `wanted` - Class that `--class` named, or None when it named none.
  

**Returns**:

  The model of one editing session.
  

**Raises**:

- `_Refusal` - The input file cannot be opened, the loaded class is not the
  one that was asked for, or the class cannot be shown at all.

<a id="edit_cfg_json.cli._outcome"></a>

#### \_outcome

```python
def _outcome(model: EditModel, save_asked: bool,
             interactive: bool) -> ExitCode
```

Return what one finished session says about how the run went.

A session the user was given ends when the user closes it, and closing an
editor is not a failure whatever is left in the fields. A program that
printed once has nobody to read a verdict for it, so there the verdict is
the answer.

**Arguments**:

- `model` - Model of the session that has just ended.
- `save_asked` - Whether the run was asked to write the output file.
- `interactive` - Whether the backend gave the user a session.
  

**Returns**:

  What this run of the program ends with.

<a id="edit_cfg_json.cli._session"></a>

#### \_session

```python
def _session(backend: EditorBackend, parsed: Namespace,
             interactive: bool) -> ExitCode
```

Run one editing session and return what it says about the run.

Saving happens before the backend runs, because a program that is asked
to save has no user to press Save and the backend has to be able to
report what the save did.

**Arguments**:

- `backend` - User interface to run this session in.
- `parsed` - Parsed command line of one run.
- `interactive` - Whether the backend gives the user a session.
  

**Returns**:

  What this run of the program ends with.
  

**Raises**:

- `_Refusal` - The session cannot be started.

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

<a id="edit_cfg_json.loader"></a>

# edit\_cfg\_json.loader

How the application says that its configuration is constructed.

Most applications say nothing: their configuration class takes the keyword
arguments that `config_as_json` documents, and the editor constructs it from
the signature it reads. An application whose class needs an argument this
library knows nothing about — a folder, a connection, the list of names its own
validators accept — has to say so, and a loader is how it says it.

**The signature of a loader is closed.** The editor passes the five things it
owns, all of them keyword arguments, and everything else is bound before the
callable reaches the editor, with a closure or `functools.partial`. That is
what keeps this protocol from growing a parameter for every application that
has one: what the editor does not know about is not the editor's to pass.

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

This is `config_as_json.ConfigFactory` plus the two parameters it lacks, so
a factory an application already has is nearly one of these. The two that
are added are the ones a load has to be told: the hook that reports what
reading an old format file changed, and whether the declared defaults may
fill in what the file leaves out.

It is checkable at runtime because a program of this library is told the
name of one on a command line, and a name that turns out to be something
else has to be refused rather than called. What that check can see is that
the object can be called at all; whether it takes these five keyword
arguments is answered by calling it.

<a id="edit_cfg_json.loader.ConfigLoader.__call__"></a>

#### \_\_call\_\_

```python
def __call__(*,
             from_json_data_text: Optional[str] = None,
             from_json_filename: Optional[PathOrStr] = None,
             ok_to_use_defaults: bool = False,
             auto_ch_hook: Optional[ConfigAutoChangeHook] = None,
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
- `auto_ch_hook` - Hook that the class reports its automatic changes
  through, or None when the caller wants none.
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
               ok_to_use_defaults: bool = False,
               hook: Optional[ConfigAutoChangeHook] = None) -> Config
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
- `hook` - Hook that reports the automatic changes of an old format file.
  

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
         ok_to_use_defaults: bool = False,
         hook: Optional[ConfigAutoChangeHook] = None) -> Config
```

Return one configuration object of this session's class.

**Arguments**:

- `stream` - Stream that collects what the construction says.
- `text` - JSON text to apply, or None for the declared values.
- `ok_to_use_defaults` - Whether the declared defaults may fill in what
  the text does not hold.
- `hook` - Hook that reports the automatic changes of an old format
  file.
  

**Returns**:

  The configuration object that was constructed.
  

**Raises**:

- `ValueError` - The values are ones the configuration refuses.
- `KeyError` - The keys of the text do not match the declared members.
- `TypeError` - The configuration cannot be constructed this way.
- `AttributeError` - The class declares no public member at all.

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

<a id="edit_cfg_json.settings._duplicate"></a>

#### \_duplicate

```python
def _duplicate(key: str, first: str, second: str) -> ValueError
```

Return the refusal of one key combination given to two actions.

**Arguments**:

- `key` - The combination that both of them hold.
- `first` - Name of the action that was seen holding it first.
- `second` - Name of the other action that holds it.
  

**Returns**:

  The failure to raise where the settings were built.

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

<a id="edit_cfg_json.settings.ActionSettings.__post_init__"></a>

#### \_\_post\_init\_\_

```python
def __post_init__() -> None
```

Refuse one key combination that two actions would both run.

Only one of the two can ever run, which one it is depends on the
toolkit, and the symptom is an action that mysteriously does
nothing. The case of a combination is ignored here, because it is
ignored where the combination is used.

**Raises**:

- `ValueError` - Two actions hold the same key combination.

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

<a id="edit_cfg_json.settings.Settings.__post_init__"></a>

#### \_\_post\_init\_\_

```python
def __post_init__() -> None
```

Normalize the extension, and refuse text that is not one.

The dot is added here rather than everywhere the extension is read,
so that every user of a `Settings` sees one form of it. Writing to a
frozen instance is what normalizing in place costs, and it is done
the one way a frozen dataclass allows.

**Raises**:

- `ValueError` - The extension is text that names no extension.

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

<a id="edit_cfg_json.settings._matches"></a>

#### \_matches

```python
def _matches(name: PathOrStr, extension: str) -> bool
```

Return whether one file name already has one extension.

The comparison ignores the case of both, because the file systems of
Windows and of macOS do not distinguish it either, and refusing `.CFG`
while accepting `.cfg` would be a difference that the file the name
stands for does not make.

**Arguments**:

- `name` - File name to look at.
- `extension` - Extension of the application, beginning with its dot.
  

**Returns**:

  Whether the name ends with that extension.

<a id="edit_cfg_json.settings._refused"></a>

#### \_refused

```python
def _refused(name: PathOrStr, extension: str) -> CheckedFile
```

Return the refusal of one file name an extension forbids.

**Arguments**:

- `name` - File name that the application cannot use.
- `extension` - Extension that this application enforces.
  

**Returns**:

  That name, and why it cannot be used.

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

<a id="edit_cfg_json.model_text.NOT_EDITABLE_FORM"></a>

#### NOT\_EDITABLE\_FORM

Form of the value text of a member this version cannot edit.

<a id="edit_cfg_json.model_text.EDITED_MARK"></a>

#### EDITED\_MARK

Mark that follows the value of a member the user has changed.

<a id="edit_cfg_json.model_text.VALIDATOR_MARK"></a>

#### VALIDATOR\_MARK

Mark that follows the value of a member a validation pass rewrote.

<a id="edit_cfg_json.model_text.FILLED_MARK"></a>

#### FILLED\_MARK

Mark that follows the value of a member the input file did not hold.

<a id="edit_cfg_json.model_text.LOAD_MARK"></a>

#### LOAD\_MARK

Mark that follows a value that reading the input file put there.

A file in an older format is what puts one there in practice: a key of it was
renamed into this member, or the rules for that format supplied the value. A
value that parsing or validating normalized is marked with this too.

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

Form of the line that names the members the application refused.

They are named here as well as marked below, because a configuration of any
size does not fit a window: a user who has just asked what the application
makes of these values should be told where to look rather than have to go
looking.

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

What is written below a member is indented by this much.

The indentation is what says that the line belongs to the member above it
rather than being a member of its own. Every line of it gets one, because
what the type of a member says about it runs to more than one line.

<a id="edit_cfg_json.model_text.row_value_text"></a>

#### row\_value\_text

```python
def row_value_text(row: MemberRow) -> str
```

Return the value of one member as the text a field would show.

A member that this version of the model cannot edit is named by its kind
instead of by its value, because a list or a dict needs more than one
field. Every other member shows the text of the value it holds.

**Arguments**:

- `row` - Member to render.
  

**Returns**:

  The value text of one member.

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

<a id="edit_cfg_json.model_text.row_description"></a>

#### row\_description

```python
def row_description(model: EditModel, row: MemberRow) -> str
```

Return what the application says about one member, as it is shown.

It is the description of the member while the explanations are shown, and
nothing while they are hidden. Which of the two it is belongs to the
model, so that the two backends cannot hide different things.

**Arguments**:

- `model` - Model that the member belongs to.
- `row` - Member to describe.
  

**Returns**:

  The description of one member, empty while it is not being shown or
  when the application said nothing about that member.

<a id="edit_cfg_json.model_text.row_diagnostic"></a>

#### row\_diagnostic

```python
def row_diagnostic(model: EditModel, row: MemberRow) -> str
```

Return what is wrong with one member, and nothing when nothing is.

Two things can be wrong with a member and they are not the same thing.
Its text may mean no value of that member at all, which is answered by
the member alone and stays true until the member is edited again; or the
application may have refused the value it holds, which is answered by the
whole configuration and is only known for as long as the rest of the
buffer stands still. The first is preferred when both are there, because
a value that does not exist yet is what has to be corrected first.

Both backends read this from here, so that neither of them decides on its
own what a refused member is told.

**Arguments**:

- `model` - Model that the member belongs to.
- `row` - Member to report.
  

**Returns**:

  What is wrong with that member, empty when nothing is known to be.

<a id="edit_cfg_json.model_text._indented"></a>

#### \_indented

```python
def _indented(text: str) -> str
```

Return one text that belongs to a member, with every line indented.

A line with nothing on it is left alone, because indenting it would put
blank space where there is nothing to line up.

<a id="edit_cfg_json.model_text._row_as_text"></a>

#### \_row\_as\_text

```python
def _row_as_text(model: EditModel, row: MemberRow) -> str
```

Return the line that shows one member, and what is said below it.

The description comes before what is wrong with the member, because the
description is part of the member and what is wrong comes and goes: a
line that appears below everything moves nothing that is above it.

<a id="edit_cfg_json.model_text._state_line"></a>

#### \_state\_line

```python
def _state_line(verdict: ValidationVerdict) -> str
```

Return the one line that says what the application made of a buffer.

**Arguments**:

- `verdict` - What the last validation pass found.
  

**Returns**:

  The state of the buffer, naming the members that were refused.

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

<a id="edit_cfg_json.model_text._head_text"></a>

#### \_head\_text

```python
def _head_text(model: EditModel) -> str
```

Return the label of the configuration and what its class says.

The two share a line while the explanations are hidden and take a line
each while they are shown, because the whole docstring is more than one
line whenever it is more than the summary.

**Arguments**:

- `model` - Model whose configuration object is labelled.
  

**Returns**:

  The label of the configuration, with as much of its docstring as is
  being shown.

<a id="edit_cfg_json.model_text.model_as_text"></a>

#### model\_as\_text

```python
def model_as_text(model: EditModel) -> str
```

Return the whole model as text, one line per configuration member.

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
  

**Returns**:

  The label of the configuration and what its class says about itself,
  what the load did, one line per member with its description and
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

<a id="edit_cfg_json.edit_model.NOT_EDITABLE_ERROR"></a>

#### NOT\_EDITABLE\_ERROR

Message of the error raised when a member cannot be edited.

<a id="edit_cfg_json.edit_model.MemberRow"></a>

## MemberRow Objects

```python
class MemberRow(NamedTuple)
```

One configuration member as it appears in the JSON file.

<a id="edit_cfg_json.edit_model.MemberRow.path"></a>

#### path

Path that addresses this member in the model.

Every path of a flat configuration has one step. The further steps that
lists, dicts and nested configuration objects need arrive together with
those, and no call site has to change when they do.

<a id="edit_cfg_json.edit_model.MemberRow.value"></a>

#### value

Current value of the member in JSON space, as the user edits it.

<a id="edit_cfg_json.edit_model.MemberRow.original"></a>

#### original

Value that this member had when the file was last agreed with.

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

<a id="edit_cfg_json.edit_model.MemberRow.changed_by_validator"></a>

#### changed\_by\_validator

Whether a validation pass rewrote this value.

A validation pass sets the flag and the next edit of this member clears
it, so it always answers the same question: is the value shown here
something a validator made of what was typed? It belongs to the model
rather than to a backend, so that two backends cannot show it
differently.

<a id="edit_cfg_json.edit_model.MemberRow.filled_from_default"></a>

#### filled\_from\_default

Whether the declared defaults supplied this value.

It is set when a load that was allowed to use the defaults filled in a
member the input file did not hold, and it stays set for the rest of the
session: that the file did not hold this value remains true whatever the
user then types into it. It belongs to the model for the same reason as
the flag above, so that two backends cannot show it differently.

<a id="edit_cfg_json.edit_model.MemberRow.changed_by_load"></a>

#### changed\_by\_load

Whether reading the input file put this value here or altered it.

Reading a file is not always only reading it. A class that declares rules
for reading an older format may have supplied this value or renamed a key
of the file into this member, and parsing or validating may have
normalized what the file held. The user has to be told, because the value
shown is then not the value in the file.

It stays set for the rest of the session, exactly as the flag above does
and for the same reason, and the two are never both set: what the declared
defaults filled in is said by that flag, which says more than this one
would.

<a id="edit_cfg_json.edit_model.MemberRow.description"></a>

#### description

What is said about this member, empty when nothing is.

The application says most of it, in the description mapping, and the type
of the member says the rest where it has a type that says anything, which
today means an enum. It is read once, when the model is built, because it
says what the member is for and that does not change while it is edited. A
member that nothing is said about keeps an empty description and is shown
without one, which is all that an unexplained member costs.

<a id="edit_cfg_json.edit_model.MemberRow.converter"></a>

#### converter

How the text of this member becomes the value that is stored in it.

It is None for a member that holds what the file holds, which is most of
them. It is what says that a member holds an enum, and that answers two
questions: which names the description of the member lists, and whether
the text the field holds means a value of this member at all.

<a id="edit_cfg_json.edit_model.MemberRow.conversion"></a>

#### conversion

Why the text of this member means no value of it, empty when it does.

It is answered by this member alone, which is what makes it a different
thing from what a validation pass says about it: it stays true until this
member is edited again, whatever happens to the rest of the buffer. It is
set when the user leaves the field and again by every validation pass, and
the next edit of this member clears it.

<a id="edit_cfg_json.edit_model.MemberRow.name"></a>

#### name

```python
@property
def name() -> str
```

Return the name of the member, the last step of its path.

<a id="edit_cfg_json.edit_model.MemberRow.editable"></a>

#### editable

```python
@property
def editable() -> bool
```

Return whether this member is a scalar that can be edited.

A list or a dict value is ordinary JSON structure that needs a tree
of fields rather than a single field, which this version of the
model does not have. Such a member is still reported as a row, so
that no configuration member can silently go missing.

<a id="edit_cfg_json.edit_model.MemberRow.is_text"></a>

#### is\_text

```python
@property
def is_text() -> bool
```

Return whether this member holds text.

This is the difference between a value that is text and a value
whose text is a rendering of it. The text of a text member is the
value itself, while the text of a number is how the number is
written.

<a id="edit_cfg_json.edit_model.MemberRow.edited"></a>

#### edited

```python
@property
def edited() -> bool
```

Return whether this member holds something that is not saved yet.

A member is changed when it would now be written to the file
differently, and not when it merely was typed in. Typing a value
back to what it was leaves nothing to save, and an editor that still
claimed to have changes would be telling the user something untrue.
Saving says the same thing about every member at once.

<a id="edit_cfg_json.edit_model._ordered_names"></a>

#### \_ordered\_names

```python
def _ordered_names(config: Config, members: dict[str, JsonType]) -> list[str]
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

<a id="edit_cfg_json.edit_model._row_of"></a>

#### \_row\_of

```python
def _row_of(name: str, value: JsonType, report: LoadReport,
            descriptions: Descriptions,
            converter: Optional[ParseConverter]) -> MemberRow
```

Return the row of one serialized member of a configuration.

**Arguments**:

- `name` - Name of the member, which is the one step of its path while
  every member of the configuration is a scalar.
- `value` - JSON space value that the member holds.
- `report` - What reading the input file did, which says whether this
  member holds a value that came from the file.
- `descriptions` - What the application says about its members.
- `converter` - How the text of this member becomes a value, or None.
  

**Returns**:

  The row of that member, as the model starts out holding it.

<a id="edit_cfg_json.edit_model._rows_from_config"></a>

#### \_rows\_from\_config

```python
def _rows_from_config(config: Config, report: LoadReport,
                      descriptions: Descriptions,
                      converters: Mapping[str, ParseConverter],
                      stderr_file: TextIO) -> dict[ConfigPath, MemberRow]
```

Return one row per serialized member, by path, in declaration order.

A mapping by path is what the design asks for, because every leaf is
addressed by its path and no other name for it is needed. A dictionary
keeps the order it was built in, so the declaration order the rows are
shown in survives being a mapping.

<a id="edit_cfg_json.edit_model._refreshed"></a>

#### \_refreshed

```python
def _refreshed(row: MemberRow, members: Mapping[str, JsonType]) -> MemberRow
```

Return one row as a validated configuration object left it.

A member that the validated object does not serialize keeps the value
the buffer holds. That happens when a validator sets a member the class
leaves out of JSON while it is None, and there is then no value to read
back rather than a value that changed.

**Arguments**:

- `row` - Member as the buffer holds it.
- `members` - One JSON space value per member of the validated object.
  

**Returns**:

  The row, marked as rewritten when the validation changed its value.

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

This version of the model handles scalar members only. A member whose
value is a list or a dict is reported as a row that is not editable.

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

<a id="edit_cfg_json.edit_model.EditModel._config_type"></a>

#### \_config\_type

```python
@property
def _config_type() -> type[Config]
```

Return the class of the configuration that is being edited.

It is the class of the object the model was built on, whatever else
an application's loader might have made of another file: which class
this session is about was settled when that object was loaded.

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

Return one row per configuration member, in declaration order.

Declaration order is the order the configuration class assigns its
members in, and not the sorted order that the JSON file has. How
the file is written is an implementation detail of saving; what the
application declared is what the user thinks about.

The rows are a snapshot. Editing a member replaces its row, so a row
that a caller kept is the state at the time it was read.

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

Set one member of the buffer from the text of an edit field.

Text that the field already shows changes nothing, because it is not
an edit. That is not only tidiness: a field posts a change when it is
given its initial text, and a model that counted that as an edit
would report unsaved changes before the user had touched anything.
It is also what lets a backend write the buffer back into its fields
after a validation pass without that counting as an edit.

**Arguments**:

- `path` - Path of the member to set.
- `text` - Text that the edit field holds.
  

**Raises**:

- `KeyError` - The path is not a member of this configuration.
- `ValueError` - The member is not one that this version can edit.

<a id="edit_cfg_json.edit_model.EditModel.check_field"></a>

#### check\_field

```python
def check_field(path: ConfigPath) -> None
```

Report whether the text of one member means a value of it at all.

This is what a backend calls when a field loses the focus, which is
the moment at which the user has moved on from that field. It is
deliberately not done on every change: the name of an enum member is
no name of one for most of the time it takes to type it, and a field
that reported that would be reporting a failure that is not one yet.

Nor is it the validation of the whole configuration. It needs no
candidate configuration and it answers a different question, which is
whether this text means a value at all rather than whether the
configuration is one the application would accept. Both are needed: a
member this refuses is one the whole configuration would refuse too,
but with a message about JSON that a person editing a field never
asked about.

**Arguments**:

- `path` - Path of the member to check.
  

**Raises**:

- `KeyError` - The path is not a member of this configuration.

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
the configuration object that was accepted, and every member the
pass rewrote is marked: accepting the rewrite silently and showing
the user the text they typed would be the worst available behaviour.

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
rewrites it here too and the member says so afterwards. What reaches
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

<a id="edit_cfg_json.edit_model.EditModel._validation_pass"></a>

#### \_validation\_pass

```python
def _validation_pass() -> ValidationPass
```

Validate the buffer, refresh it, and keep what the pass found.

<a id="edit_cfg_json.edit_model.EditModel._check_fields"></a>

#### \_check\_fields

```python
def _check_fields() -> None
```

Report every member whose text means no value of that member.

A validation pass answers this for the whole buffer at once, so the
answer that one field gives when it is left is refreshed for all of
them here. A member the user never visited is then reported exactly
as one they typed into and left.

<a id="edit_cfg_json.edit_model.EditModel._record"></a>

#### \_record

```python
def _record(outcome: SaveOutcome) -> SaveOutcome
```

Keep what one attempt to save did, and hand it back.

<a id="edit_cfg_json.edit_model.EditModel._keep_saved"></a>

#### \_keep\_saved

```python
def _keep_saved(candidate: Config) -> None
```

Make what was written the values that the buffer is compared to.

The mark of a member a validator rewrote is deliberately left alone.
That a value is not literally the one the user typed stays true after
it has been saved, and it is the mark that says so.

<a id="edit_cfg_json.edit_model.EditModel._buffer"></a>

#### \_buffer

```python
def _buffer() -> dict[str, JsonType]
```

Return the buffer as one JSON space value per member.

Every member of a flat configuration is named by the single step of
its path. The members inside lists, dicts and nested configuration
objects arrive together with the further steps that address them.

<a id="edit_cfg_json.edit_model.EditModel._take_validated"></a>

#### \_take\_validated

```python
def _take_validated(members: Mapping[str, JsonType]) -> None
```

Refresh the buffer from the configuration object that was built.

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

<a id="edit_cfg_json.constructing.HOOK_NAME"></a>

#### HOOK\_NAME

Name of the constructor parameter that reports automatic changes.

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

<a id="edit_cfg_json.constructing._arguments"></a>

#### \_arguments

```python
def _arguments(factory: Callable[..., Config], stream: TextIO,
               hook: Optional[ConfigAutoChangeHook]) -> dict[str, object]
```

Return what to call one configuration class with.

The values are a stream, a hook and `None`, and which parameter each of
them belongs to differs from class to class, so there is no one type that
they share.

**Arguments**:

- `factory` - Class, or callable with its own arguments already bound,
  that constructs the configuration.
- `stream` - Stream that collects what the class says about itself.
- `hook` - Hook that reports the automatic changes of an old format file,
  or None when the caller wants none.
  

**Returns**:

  The keyword arguments for one construction of that class.

<a id="edit_cfg_json.constructing.built_config"></a>

#### built\_config

```python
def built_config(factory: Callable[..., Config],
                 *,
                 stream: TextIO,
                 hook: Optional[ConfigAutoChangeHook] = None) -> Config
```

Construct one configuration holding the values that its class declares.

**Arguments**:

- `factory` - Class to construct, or a callable that constructs it with
  arguments of its own already bound. A signature is all this needs,
  and `functools.partial` over a class has one.
- `stream` - Stream that collects what the class says about itself. It is
  passed only to a class that declares it; one that does not writes
  wherever it writes, which is less pleasant and not a refusal.
- `hook` - Hook that reports the automatic changes of an old format file.
  It reaches a class that declares the parameter and is dropped for
  one that does not, which is what `config_as_json` leaves to the
  application to opt into: a class that collects further keyword
  arguments could be forwarding them or refusing them, and offering
  the hook to it would turn a load that works into one that fails,
  for a report that is a nicety.
  

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
class does while it reads a file.

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

<a id="edit_cfg_json.__main__"></a>

# edit\_cfg\_json.\_\_main\_\_

The `edit-cfg-json` program: say what a configuration file amounts to.

It is the program of the package that imports no user interface library, so it
needs no display: it prints the configuration as text, with what the
application's own validators make of it, and with `--save` it writes the
validated file. That makes it a configuration checker for a terminal or for a
continuous integration job as much as a way of looking at a class.

Run it as `edit-cfg-json`, or as `python -m edit_cfg_json` on a machine whose
script folder is not on the path.

<a id="edit_cfg_json.__main__.PROGRAM"></a>

#### PROGRAM

Name that this program is installed under.

<a id="edit_cfg_json.__main__.main"></a>

#### main

```python
def main(args: Optional[Sequence[str]] = None) -> int
```

Run this program and return what it ends with.

**Arguments**:

- `args` - Optional replacement for `sys.argv[1:]`, mainly for tests.
  

**Returns**:

  What this run ends with, as one of `edit_cfg_json.ExitCode`.

<a id="edit_cfg_json.descriptions"></a>

# edit\_cfg\_json.descriptions

The explanatory text that the editor shows about a configuration.

There are three sources of it, they are independent, and all of them are
optional. The docstring of the configuration class labels the configuration
object, a mapping supplied by the application labels the individual members,
and the type of a member says the rest where the member has a type that says
anything, which today means an enum.

It takes a mapping for the members because a member has no docstring at
runtime. A class has one and every reader of the code can see it, while a
string literal written after an assignment is discarded by the compiler and a
PEP 526 annotation on an instance attribute is recorded nowhere at all. So the
members are described by the application in a mapping, and the editor invents
nothing: what it adds to that mapping is read from the enum class of the
member, which is a fact about the type and not a constraint read out of a
validator.

<a id="edit_cfg_json.descriptions.EVERY_ELEMENT"></a>

#### EVERY\_ELEMENT

The path step that means every list element or dictionary value here.

It is the step that `config_as_json` gives this meaning to, and it keeps it
here, which is what stops an application from having to repeat one
description once per list index or once per dictionary key.

<a id="edit_cfg_json.descriptions.CHOICES_FORM"></a>

#### CHOICES\_FORM

What the editor says about the names one enum member accepts.

<a id="edit_cfg_json.descriptions._selects"></a>

#### \_selects

```python
def _selects(selector: ConfigPath, path: ConfigPath) -> bool
```

Return whether one selector of the mapping addresses one member.

**Arguments**:

- `selector` - One key of the description mapping.
- `path` - Path of the member that is being described.
  

**Returns**:

  Whether that selector is about that member.

<a id="edit_cfg_json.descriptions._named_steps"></a>

#### \_named\_steps

```python
def _named_steps(selector: ConfigPath) -> tuple[bool, ...]
```

Return which steps of one selector name a step rather than all of them.

This is how two selectors that both address one member are compared, and
the more specific of them is the greater: a step that names one key is
more specific than the step that means every element, and an earlier step
decides before a later one. Two different selectors can never compare
equal here, because two selectors with the same pattern of named steps
that both address one member are the same selector.

**Arguments**:

- `selector` - One key of the description mapping.
  

**Returns**:

  One value per step, saying whether that step names a single step.

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

<a id="edit_cfg_json.descriptions._enum_type"></a>

#### \_enum\_type

```python
def _enum_type(converter: Optional[ParseConverter]) -> Optional[type[Enum]]
```

Return the enum class one member holds, or None when it holds none.

**Arguments**:

- `converter` - How the text of this member becomes a value, or None.
  

**Returns**:

  The enum class of that member, or None for every other member.

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

<a id="edit_cfg_json.descriptions.member_description"></a>

#### member\_description

```python
def member_description(descriptions: Descriptions, path: ConfigPath,
                       converter: Optional[ParseConverter]) -> str
```

Return everything the editor has to say about one member.

What the application says comes first, because it is what this member is
for in this application, and what the type of the member says comes after
it. The second is appended rather than used only where the first is
missing: the names an enum accepts are true whatever the application
wrote, and an application that explains what its members mean should not
have to list the names as well.

**Arguments**:

- `descriptions` - What the application says about its members.
- `path` - Path of the member that is being described.
- `converter` - How the text of this member becomes a value, or None.
  

**Returns**:

  The description of that member, and an empty text when neither the
  application nor the type of the member says anything about it.

<a id="edit_cfg_json.auto_change"></a>

# edit\_cfg\_json.auto\_change

What reading one input file did to the values that it holds.

Reading a file can change what the values are, and from three directions: the
rules a configuration class declares for reading a file of an older format,
the normalization that parsing and validating do, and the declared defaults
filling in what the file left out. The user has to be told, because the values
on the screen are then not the values in the file, and an editor that said
nothing about that would look broken.

**What changed is found by comparing, and not by asking.** The values the load
produced are written back to JSON and compared with the text of the file, key
by key. That is exact, it needs nothing of the configuration class, and it
covers all three directions at once, which is why it is the mechanism rather
than the fallback: the report below is one that a class has to opt into, and
most classes do not.

**Why it changed is asked of the class, where the class answers.**
`ConfigAutoChangeHook` is what `config_as_json` reports its own automatic
changes through, and it reaches a class only where that class declares
`auto_ch_hook` and hands it on. What it adds is what the comparison cannot
know: the older keys the file was read with. A key that was renamed is simply
gone from the file, and nothing in the file says which member it became.

**What the declared defaults filled in is asked of the parse.** It is the one
of the three that has a mark of its own, so it has to be exact, and the keys
of the file do not answer it: a key the rules for an older format renamed into
a member was in the file under another name, and a value those rules supplied
was in the file under no name at all. What the defaults filled in is exactly
what the key check of the parse was not given, so the parse is what is asked,
into a copy of the loaded object whose key check records and stops.

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

<a id="edit_cfg_json.auto_change.ChangeReport"></a>

## ChangeReport Objects

```python
class ChangeReport(ConfigAutoChangeHook)
```

The automatic changes of one load, as the load itself reports them.

`Config.__init__` deep copies the hook it is given and records into the
copy, so a hook that is read afterwards would answer with nothing at all.
This one is read afterwards, and `__deepcopy__` is how it says so: the
object is a channel back to the editor, and a copy of a channel is the
channel.

What that costs is that every copy of a configuration object reports into
this same hook, so a second parse of the same file records what the first
one recorded a second time. `file_changes` reads the hook before it parses
anything, which is where that is dealt with.

<a id="edit_cfg_json.auto_change.ChangeReport.__deepcopy__"></a>

#### \_\_deepcopy\_\_

```python
def __deepcopy__(memo: dict[int, object]) -> 'ChangeReport'
```

Return this very hook, so that the load reports to the editor.

**Arguments**:

- `memo` - What `copy.deepcopy` has copied already, which a copy that
  copies nothing has no use for.
  

**Returns**:

  This object, which is then the one the load records into.

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

Keys of the file that this configuration does not write back.

A key the rules for an older format renamed or removed is one of these,
and so is one whose member the class leaves out of JSON while it is None.
None of them has a row, because none of them is a member of this
configuration, so the message is the only place they can be reported.

<a id="edit_cfg_json.auto_change.FileChanges.changed"></a>

#### changed

Members whose value the load itself put there or altered.

A member the declared defaults filled in is deliberately not one of them.
It is marked already, by a mark that says more than this one would, and
one member carrying two marks about the same thing would be worse than
either of them alone.

<a id="edit_cfg_json.auto_change.FileChanges.old_keys"></a>

#### old\_keys

Older keys the load accepted, as the configuration class reported them.

Empty for a class that does not declare the hook, and empty for a file
that is in the current format. A key that was moved rather than renamed is
reported as `old.path -> new.path`, which is what `config_as_json` puts
there.

<a id="edit_cfg_json.auto_change.FileChanges.supplied"></a>

#### supplied

Paths the rules for an older format supplied values for.

These are the values that neither the file nor the declared defaults gave:
the configuration class supplied them, because the file is too old to hold
them at all.

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

<a id="edit_cfg_json.auto_change._canonical"></a>

#### \_canonical

```python
def _canonical(value: JsonType) -> str
```

Return one value as the text that decides whether it is unchanged.

The keys of a dictionary are sorted, because `config_as_json` writes them
sorted while a file is written by hand, and a file that holds the same
values in another order holds the same values. Everything else is compared
as it is written, which is what tells `1` from `1.0` and from `true`: all
three of them reach the file differently.

**Arguments**:

- `value` - One value in JSON space.
  

**Returns**:

  The text that stands for that value.

<a id="edit_cfg_json.auto_change._written"></a>

#### \_written

```python
def _written(config: Config) -> Mapping[str, JsonType]
```

Return the values that one loaded configuration would write to a file.

The object is copied first, because writing it validates it and a member
validator returns the value that is stored back into the member. What is
said while it is written is dropped, because the load has already reported
whatever there was to say about this file.

**Arguments**:

- `config` - Configuration object that the load produced.
  

**Returns**:

  One JSON space value per member that this object writes.
  

**Raises**:

- `TypeError` - A value of this class is no JSON value.
- `ValueError` - This class refuses to write the values it holds.

<a id="edit_cfg_json.auto_change._held"></a>

#### \_held

```python
def _held(text: str) -> Mapping[str, JsonType]
```

Return the values that the text of one input file holds.

The text has already been read as configuration by the time this is asked,
so it is JSON and it is an object.

**Arguments**:

- `text` - The whole text of the input file.
  

**Returns**:

  One value per key of that file.

<a id="edit_cfg_json.auto_change._altered"></a>

#### \_altered

```python
def _altered(written: Mapping[str, JsonType],
             held: Mapping[str, JsonType]) -> frozenset[str]
```

Return the members whose value is not the one the file holds.

A member whose key the file does not hold at all is one of them, because
the value shown for it came from somewhere other than the file: the
declared defaults, the rules for an older format, or a key that was
renamed into it.

**Arguments**:

- `written` - What the load would write back to a file.
- `held` - What the file holds.
  

**Returns**:

  The names of the members that are not as the file has them.

<a id="edit_cfg_json.auto_change._ParsedKeys"></a>

## \_ParsedKeys Objects

```python
class _ParsedKeys(Exception)
```

The keys of one parse, carried out of the parse that recorded them.

It is internal because it exists only to carry two lists of names out of
one method of one throwaway object, and it is an exception because the
parse it comes from is not wanted beyond that point.

<a id="edit_cfg_json.auto_change._ParsedKeys.__init__"></a>

#### \_\_init\_\_

```python
def __init__(declared: Sequence[str], held: Sequence[str]) -> None
```

Say which keys were declared and which the parsed data held.

**Arguments**:

- `declared` - The members that the configuration class declares.
- `held` - The keys the data held once the rules for an older format
  had finished with it.

<a id="edit_cfg_json.auto_change._record_keys"></a>

#### \_record\_keys

```python
def _record_keys(expected_keys: list[str],
                 j_keys: list[str],
                 ok_to_use_defaults: bool,
                 stderr_file: TextIO,
                 allowed_missing_keys: Optional[list[str]] = None) -> None
```

Record the keys of one parse, and stop that parse there.

This stands in for `Config.check_key_match` on the probe below, so the
parameters are that method's and in its order, because that is how
`Config.parse_json` calls it. There is no object among them for the same
reason as in `validation`: an attribute of an object is not a bound method,
and the real method is a static one in any case.

**Arguments**:

- `expected_keys` - The members that the configuration class declares.
- `j_keys` - The keys of the data that the parse is about to apply.
- `ok_to_use_defaults` - Whether missing keys may keep their default, which
  is the caller's own answer and is not what is being asked here.
- `stderr_file` - Stream for diagnostics, which a check that refuses
  nothing writes nothing to.
- `allowed_missing_keys` - Keys that may be missing whatever the policy is,
  which a check that refuses nothing has no use for either.
  

**Raises**:

- `_ParsedKeys` - Always, carrying the two sets of keys.

<a id="edit_cfg_json.auto_change._filled"></a>

#### \_filled

```python
def _filled(config: Config, text: str) -> frozenset[str]
```

Return the members whose value the declared defaults supplied.

A load that was allowed to fill in what the file left out cannot afterwards
be asked which of its values came from the file, and the keys of the file
do not answer it either: the rules for an older format may have renamed a
key of the file into a member, or supplied a value for a member the file
never had. What the defaults filled in is exactly what the key check of
the parse was not given, so the parse is what is asked.

The file is therefore parsed a second time, into a copy of the loaded
object whose key check records what it was given and stops the parse there.
Stopping is what keeps this from repeating anything: everything after the
key check is what the real load has already done, so the application's own
validators still run once, on the object that is really being edited.

**Arguments**:

- `config` - Configuration object that the load produced.
- `text` - The whole text of the input file.
  

**Returns**:

  The names of the members that the declared defaults supplied, and
  nothing at all when the parse did not reach the key check.

<a id="edit_cfg_json.auto_change.file_changes"></a>

#### file\_changes

```python
def file_changes(config: Config, text: str, hook: ChangeReport,
                 permissive: bool) -> FileChanges
```

Return what one successful load did to the file that it read.

**Arguments**:

- `config` - Configuration object that the load produced.
- `text` - The whole text of the input file.
- `hook` - Hook the load was given, which a configuration class that
  declares it has reported its own automatic changes through.
- `permissive` - Whether the load was allowed to fill in what the file left
  out. A load that was not fills nothing in, so there is nothing to
  ask the parse about.
  

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

What the application refused about each member, by member name.

Empty for a buffer that was accepted, and empty for one that was refused
for a reason that is about no single member. A member is named here when
its own text means no value of it at all, or when its own validators
refused the value it holds.

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

What each member's own validators said, by member name.

<a id="edit_cfg_json.validation.Attribution.remaining"></a>

#### remaining

What a step that is about no single member said, empty when none.

<a id="edit_cfg_json.validation._told"></a>

#### \_told

```python
def _told(captured: str, error: Exception) -> str
```

Return what one refusal says, and its exception when it said nothing.

The captured text is what the application itself would have printed, so
it is what the user is shown. A failure that printed nothing has only
its exception left to report, which is better than no explanation.

**Arguments**:

- `captured` - What the refusing code wrote to its diagnostics stream.
- `error` - The failure that it reported.
  

**Returns**:

  What to tell the user about that refusal.

<a id="edit_cfg_json.validation.PLAN_METHOD"></a>

#### PLAN\_METHOD

Name of the method that the probe below has replaced with nothing.

<a id="edit_cfg_json.validation._no_plan"></a>

#### \_no\_plan

```python
def _no_plan(stderr_file: TextIO) -> ValidationPlan
```

Return no validation steps at all, for the probe object.

It is an attribute of one object rather than a method of a class, so it is
called without the object, exactly as `parse_converters` and the rest of
the parse call the real method.

<a id="edit_cfg_json.validation._probe"></a>

#### \_probe

```python
def _probe(config: Config, members: dict[str, JsonType]) -> Optional[Config]
```

Return the buffer in an object that has not been validated.

A configuration object normally cannot hold a buffer without being
validated: `Config.parse_json` ends in `validate()`, which raises at the
first step that refuses. So the object that could say which member was
refused is exactly the object that a refusal keeps the editor from ever
holding.

A copy whose validation plan is empty is that object. Everything else the
parse does still happens — the keys are matched, the dict shapes are
checked, the parse converters run, the nested configuration objects are
built — and only the plan is left out, which is what the walk below then
applies itself, one member at a time.

That is also why the buffer is parsed rather than assigned onto the object
member by member. Assigning would mean applying the parse converters here,
which is a second implementation of what `config_as_json` does while it
parses, and it would put a plain dict where a nested configuration object
belongs. The one method left out is the whole of what this borrows.

**Arguments**:

- `config` - Configuration object of this session. It is not modified.
- `members` - The edit buffer, as one JSON space value per member.
  

**Returns**:

  An object holding the buffer, or None when the buffer is not a
  configuration of this class at all.

<a id="edit_cfg_json.validation._unconverted"></a>

#### \_unconverted

```python
def _unconverted(converters: Mapping[str, ParseConverter],
                 members: dict[str, JsonType]) -> dict[str, str]
```

Return why each value of the buffer means no value of its member.

**Arguments**:

- `converters` - One converter per member that has one.
- `members` - The edit buffer, as one JSON space value per member.
  

**Returns**:

  One message per member whose text means no value of it, and nothing
  at all for a buffer every value of which means something.

<a id="edit_cfg_json.validation._attribute_member"></a>

#### \_attribute\_member

```python
def _attribute_member(validator: MemberValidator, probe: Config, name: str,
                      refused: dict[str, str]) -> None
```

Run one validator over one member, keeping what it refused.

The value the validator returns is stored back into the member, because
that is what the real pass does with it and what a later validator of the
same member is then given.

**Arguments**:

- `validator` - Validator to run.
- `probe` - Configuration object holding the buffer. It is modified.
- `name` - Name of the member to validate.
- `refused` - What each member has been refused for so far, added to.

<a id="edit_cfg_json.validation._attribute_step"></a>

#### \_attribute\_step

```python
def _attribute_step(step: MemberValidationStep, probe: Config,
                    refused: dict[str, str]) -> None
```

Run one member validator over each of the members that step names.

A member that has already been refused is left alone, so that what is
reported about it is the first thing that was wrong with it, which is
also the one the real pass would have reported.

**Arguments**:

- `step` - Validation step to apply.
- `probe` - Configuration object holding the buffer. It is modified.
- `refused` - What each member has been refused for so far, added to.

<a id="edit_cfg_json.validation._step_refusal"></a>

#### \_step\_refusal

```python
def _step_refusal(step: ValidationStep, probe: Config) -> str
```

Return what one step that is about no single member refused, if any.

**Arguments**:

- `step` - Validation step to apply.
- `probe` - Configuration object holding the buffer. It is modified, as a
  whole-configuration validator is free to modify one.
  

**Returns**:

  What that step said when it refused, and nothing when it did not.

<a id="edit_cfg_json.validation._plan_failures"></a>

#### \_plan\_failures

```python
def _plan_failures(probe: Config) -> Attribution
```

Walk the validation plan far enough to say which members are refused.

`Config.validate()` stops at the first step that refuses, so the pass
that decides the verdict can report one failure and cannot say which
member it was about. This walks the same plan and differs in two ways: a
member that is refused is recorded and the walk goes on, so that every
member the user has to correct is named at once, and a step that is about
no single member is applied only while no member has been refused,
because that is the only case in which the real pass would have reached
it.

No validator class is recognised by type in any of this. What is read is
`MemberValidationStep.member_names` and `MemberValidationStep.validator`,
both of which are public, so an application's own `MemberValidator`
subclass is attributed exactly as the ones `config_as_json` ships are.

The plan is asked of the class and not of the object, because it is the
object that has no plan: what was replaced on it is the very method that
answers this. The class of the probe is the class being edited, so what is
applied here is the application's own plan, step by step, which is the
whole point.

**Arguments**:

- `probe` - Configuration object holding the buffer, not yet validated. It
  is modified: a member validator returns the value that is stored
  back into the member, exactly as the real pass stores it.
  

**Returns**:

  What each member was refused for, and what could not be attributed to
  any member at all.

<a id="edit_cfg_json.validation._attribution"></a>

#### \_attribution

```python
def _attribution(config: Config, members: dict[str, JsonType]) -> Attribution
```

Return what the validators of one refused buffer were about.

**Arguments**:

- `config` - Configuration object of this session. It is not modified.
- `members` - The edit buffer, as one JSON space value per member.
  

**Returns**:

  What each member was refused for, and what could not be attributed.
  Both are empty when the buffer is not a configuration of this class
  at all, which is a refusal about no member and no value.

<a id="edit_cfg_json.validation._refused_verdict"></a>

#### \_refused\_verdict

```python
def _refused_verdict(config: Config, members: dict[str, JsonType],
                     captured: str, error: Exception) -> ValidationVerdict
```

Return the verdict of a pass that the configuration class refused.

What the class printed is kept only when nothing at all could be
attributed to a member, which is what happens when the refusal was about
the shape of the buffer rather than about a value: a key that does not
match, text that is not JSON, a class that cannot be constructed. What
the attribution did explain is shown beside the member it is about
instead, so that the same sentence is not on the screen twice.

**Arguments**:

- `config` - Configuration object of this session. It is not modified.
- `members` - The edit buffer, as one JSON space value per member.
- `captured` - What the refused parse wrote to its stream.
- `error` - The failure that the parse reported.
  

**Returns**:

  A verdict saying that the buffer is not a configuration, and why.

<a id="edit_cfg_json.validation._no_pass"></a>

#### \_no\_pass

```python
def _no_pass(verdict: ValidationVerdict) -> ValidationPass
```

Return the pass of a buffer that never became a configuration.

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

