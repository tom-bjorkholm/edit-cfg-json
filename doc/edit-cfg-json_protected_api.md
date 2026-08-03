# Table of Contents

* [edit\_cfg\_json.loading](#edit_cfg_json.loading)
  * [HOOK\_NAME](#edit_cfg_json.loading.HOOK_NAME)
  * [DEFAULTS\_ERRORS](#edit_cfg_json.loading.DEFAULTS_ERRORS)
  * [NO\_FILE](#edit_cfg_json.loading.NO_FILE)
  * [NOT\_TEXT](#edit_cfg_json.loading.NOT_TEXT)
  * [NOT\_CONFIG](#edit_cfg_json.loading.NOT_CONFIG)
  * [UNKNOWN\_KEY](#edit_cfg_json.loading.UNKNOWN_KEY)
  * [INCOMPLETE](#edit_cfg_json.loading.INCOMPLETE)
  * [BAD\_VALUES](#edit_cfg_json.loading.BAD_VALUES)
  * [NO\_DEFAULTS](#edit_cfg_json.loading.NO_DEFAULTS)
  * [FILLED\_MESSAGE](#edit_cfg_json.loading.FILLED_MESSAGE)
  * [LoadPolicy](#edit_cfg_json.loading.LoadPolicy)
    * [STRICT](#edit_cfg_json.loading.LoadPolicy.STRICT)
    * [DEFAULTS](#edit_cfg_json.loading.LoadPolicy.DEFAULTS)
    * [STRICT\_THEN\_DEFAULTS](#edit_cfg_json.loading.LoadPolicy.STRICT_THEN_DEFAULTS)
  * [DEFAULT\_POLICY](#edit_cfg_json.loading.DEFAULT_POLICY)
  * [LoadReport](#edit_cfg_json.loading.LoadReport)
    * [message](#edit_cfg_json.loading.LoadReport.message)
    * [filled](#edit_cfg_json.loading.LoadReport.filled)
  * [LoadedConfig](#edit_cfg_json.loading.LoadedConfig)
    * [config](#edit_cfg_json.loading.LoadedConfig.config)
    * [report](#edit_cfg_json.loading.LoadedConfig.report)
  * [ConfigLoadError](#edit_cfg_json.loading.ConfigLoadError)
    * [\_\_init\_\_](#edit_cfg_json.loading.ConfigLoadError.__init__)
  * [\_takes\_hook](#edit_cfg_json.loading._takes_hook)
  * [\_defaults](#edit_cfg_json.loading._defaults)
  * [\_explained](#edit_cfg_json.loading._explained)
  * [\_attempt](#edit_cfg_json.loading._attempt)
  * [\_declared](#edit_cfg_json.loading._declared)
  * [\_absent](#edit_cfg_json.loading._absent)
  * [\_filled\_report](#edit_cfg_json.loading._filled_report)
  * [\_permissive](#edit_cfg_json.loading._permissive)
  * [\_rescue](#edit_cfg_json.loading._rescue)
  * [\_load\_text](#edit_cfg_json.loading._load_text)
  * [\_file\_text](#edit_cfg_json.loading._file_text)
  * [load\_config](#edit_cfg_json.loading.load_config)
* [edit\_cfg\_json.backend](#edit_cfg_json.backend)
  * [EditorBackend](#edit_cfg_json.backend.EditorBackend)
    * [run\_editor](#edit_cfg_json.backend.EditorBackend.run_editor)
* [edit\_cfg\_json.editing](#edit_cfg_json.editing)
  * [edit](#edit_cfg_json.editing.edit)
* [edit\_cfg\_json.saving](#edit_cfg_json.saving)
  * [NO\_DESTINATION](#edit_cfg_json.saving.NO_DESTINATION)
  * [NOT\_VALID](#edit_cfg_json.saving.NOT_VALID)
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
  * [write\_config](#edit_cfg_json.saving.write_config)
* [edit\_cfg\_json.leaf\_value](#edit_cfg_json.leaf_value)
  * [value\_as\_text](#edit_cfg_json.leaf_value.value_as_text)
  * [text\_as\_value](#edit_cfg_json.leaf_value.text_as_value)
  * [values\_differ](#edit_cfg_json.leaf_value.values_differ)
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
  * [DIRTY\_MARK](#edit_cfg_json.model_text.DIRTY_MARK)
  * [VERDICT\_FORM](#edit_cfg_json.model_text.VERDICT_FORM)
  * [VALID\_STATE](#edit_cfg_json.model_text.VALID_STATE)
  * [INVALID\_STATE](#edit_cfg_json.model_text.INVALID_STATE)
  * [UNKNOWN\_STATE](#edit_cfg_json.model_text.UNKNOWN_STATE)
  * [SAVE\_TO\_FORM](#edit_cfg_json.model_text.SAVE_TO_FORM)
  * [NO\_DESTINATION\_TEXT](#edit_cfg_json.model_text.NO_DESTINATION_TEXT)
  * [SUMMARY\_SEPARATOR](#edit_cfg_json.model_text.SUMMARY_SEPARATOR)
  * [DESCRIPTION\_INDENT](#edit_cfg_json.model_text.DESCRIPTION_INDENT)
  * [row\_value\_text](#edit_cfg_json.model_text.row_value_text)
  * [row\_marks](#edit_cfg_json.model_text.row_marks)
  * [docstring\_text](#edit_cfg_json.model_text.docstring_text)
  * [row\_description](#edit_cfg_json.model_text.row_description)
  * [\_row\_as\_text](#edit_cfg_json.model_text._row_as_text)
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
    * [description](#edit_cfg_json.edit_model.MemberRow.description)
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
    * [set\_out\_file](#edit_cfg_json.edit_model.EditModel.set_out_file)
    * [validate](#edit_cfg_json.edit_model.EditModel.validate)
    * [save](#edit_cfg_json.edit_model.EditModel.save)
    * [\_validation\_pass](#edit_cfg_json.edit_model.EditModel._validation_pass)
    * [\_record](#edit_cfg_json.edit_model.EditModel._record)
    * [\_keep\_saved](#edit_cfg_json.edit_model.EditModel._keep_saved)
    * [\_buffer](#edit_cfg_json.edit_model.EditModel._buffer)
    * [\_take\_validated](#edit_cfg_json.edit_model.EditModel._take_validated)
* [edit\_cfg\_json.descriptions](#edit_cfg_json.descriptions)
  * [EVERY\_ELEMENT](#edit_cfg_json.descriptions.EVERY_ELEMENT)
  * [\_selects](#edit_cfg_json.descriptions._selects)
  * [\_named\_steps](#edit_cfg_json.descriptions._named_steps)
  * [path\_description](#edit_cfg_json.descriptions.path_description)
  * [class\_docstring](#edit_cfg_json.descriptions.class_docstring)
  * [class\_summary](#edit_cfg_json.descriptions.class_summary)
* [edit\_cfg\_json.validation](#edit_cfg_json.validation)
  * [BUFFER\_ERRORS](#edit_cfg_json.validation.BUFFER_ERRORS)
  * [ValidationVerdict](#edit_cfg_json.validation.ValidationVerdict)
    * [valid](#edit_cfg_json.validation.ValidationVerdict.valid)
    * [diagnostics](#edit_cfg_json.validation.ValidationVerdict.diagnostics)
  * [ValidationPass](#edit_cfg_json.validation.ValidationPass)
    * [verdict](#edit_cfg_json.validation.ValidationPass.verdict)
    * [members](#edit_cfg_json.validation.ValidationPass.members)
    * [candidate](#edit_cfg_json.validation.ValidationPass.candidate)
  * [\_refused](#edit_cfg_json.validation._refused)
  * [validate\_buffer](#edit_cfg_json.validation.validate_buffer)

<a id="edit_cfg_json.loading"></a>

# edit\_cfg\_json.loading

Reading the configuration to edit from one input file.

The editor constructs the configuration object rather than receiving one that
is already loaded. Both of the things a load has to be told are given to a
constructor and to nothing else: the hook that reports the automatic changes
of an old format file, and the policy for declared keys the file does not
contain.

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

<a id="edit_cfg_json.loading.HOOK_NAME"></a>

#### HOOK\_NAME

Name of the constructor keyword that reports automatic changes.

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

<a id="edit_cfg_json.loading._takes_hook"></a>

#### \_takes\_hook

```python
def _takes_hook(config_type: type[Config]) -> bool
```

Return whether one configuration class takes the change hook.

`Config.__init__` takes it, but a subclass has to declare it and hand it
on, and the three keyword constructor that `config_as_json` documents
does not. Only a class that names the keyword itself counts as taking
it. A class that collects further keyword arguments could be forwarding
them or refusing them, and offering the hook to it would turn a load
that works into one that fails, for a report that is a nicety.

**Arguments**:

- `config_type` - Class of the configuration that is being loaded.
  

**Returns**:

  Whether the hook can be passed to this class.

<a id="edit_cfg_json.loading._defaults"></a>

#### \_defaults

```python
def _defaults(config_type: type[Config], said: StringIO) -> Config
```

Return one configuration object holding its declared defaults.

The hook reaches a class that declares it and is dropped for a class
that does not, which is what `config_as_json` leaves to the application
to opt into. Nothing reads the hook yet; forwarding it is what a later
step needs to explain the automatic changes of an old format file.

**Arguments**:

- `config_type` - Class of the configuration that is being loaded.
- `said` - Stream that collects what the class says about itself.
  

**Returns**:

  A configuration object holding only what the class declares.
  

**Raises**:

- `ConfigLoadError` - The editor cannot construct this class.

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

<a id="edit_cfg_json.loading._attempt"></a>

#### \_attempt

```python
def _attempt(config_type: type[Config], text: str, ok_to_use_defaults: bool,
             said: StringIO) -> Config
```

Try once to build one configuration object from one file text.

The stream is the caller's, because a key that does not match is
reported to the caller and what was said about it is needed there.

**Arguments**:

- `config_type` - Class of the configuration that is being loaded.
- `text` - The whole text of the input file.
- `ok_to_use_defaults` - Whether the declared defaults may fill in the
  keys the file does not hold.
- `said` - Stream that collects what the class says about the file.
  

**Returns**:

  A configuration object holding the values of the file.
  

**Raises**:

- `KeyError` - The keys of the file do not match the declared members.
- `ConfigLoadError` - The file cannot be opened for editing.

<a id="edit_cfg_json.loading._declared"></a>

#### \_declared

```python
def _declared(config: Config) -> list[str]
```

Return the names of the public members of one configuration object.

This is the rule `config_as_json` itself uses to decide what a
configuration object consists of: every attribute that is public and is
not a method.

**Arguments**:

- `config` - Configuration object to read the member names of.
  

**Returns**:

  The name of every member of that object.

<a id="edit_cfg_json.loading._absent"></a>

#### \_absent

```python
def _absent(config: Config, text: str) -> frozenset[str]
```

Return the declared members that one file text does not hold.

The names are read from the file text, because a load that was allowed
to use the defaults cannot afterwards say which of its values came from
the file. The text has already been read as configuration by the time
this is asked, so it is JSON and it is an object.

**Arguments**:

- `config` - Configuration object that was loaded from the text.
- `text` - The whole text of the input file.
  

**Returns**:

  The names of the members the declared defaults supplied.

<a id="edit_cfg_json.loading._filled_report"></a>

#### \_filled\_report

```python
def _filled_report(config: Config, text: str, said: str) -> LoadReport
```

Return what a load that was allowed to use the defaults did.

**Arguments**:

- `config` - Configuration object that the load built.
- `text` - The whole text of the input file.
- `said` - What the configuration class said about the file.
  

**Returns**:

  The report of one permissive load.

<a id="edit_cfg_json.loading._permissive"></a>

#### \_permissive

```python
def _permissive(config_type: type[Config], text: str) -> LoadedConfig
```

Load one file text with the defaults filling in what it lacks.

A key the configuration does not declare is still refused, because
filling in governs the keys that are missing and nothing else. Dropping
an unknown key would lose whatever the file meant by it, and such a file
is either from a newer version or has a misspelled key in it.

**Arguments**:

- `config_type` - Class of the configuration that is being loaded.
- `text` - The whole text of the input file.
  

**Returns**:

  The configuration object, and what filling in did to its values.
  

**Raises**:

- `ConfigLoadError` - The file cannot be opened for editing.

<a id="edit_cfg_json.loading._rescue"></a>

#### \_rescue

```python
def _rescue(config_type: type[Config], text: str, policy: LoadPolicy,
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

- `config_type` - Class of the configuration that is being loaded.
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
def _load_text(config_type: type[Config], text: str,
               policy: LoadPolicy) -> LoadedConfig
```

Load one file text under one policy, or refuse to open the file.

**Arguments**:

- `config_type` - Class of the configuration that is being loaded.
- `text` - The whole text of the input file.
- `policy` - What to do about declared keys the file does not hold.
  

**Returns**:

  The configuration object, and what the load did to its values.
  

**Raises**:

- `ConfigLoadError` - The file cannot be opened for editing.

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
def load_config(
    config: Config,
    in_file: Optional[PathOrStr] = None,
    policy: LoadPolicy = DEFAULT_POLICY,
    settings: SettingsSource = Settings()
) -> LoadedConfig
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
  

**Returns**:

  The configuration object to edit, and what the load did to its
  values beyond reading them.
  

**Raises**:

- `ConfigLoadError` - The file cannot be opened for editing.

<a id="edit_cfg_json.backend"></a>

# edit\_cfg\_json.backend

The protocol that every user interface backend implements.

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

The file name is whatever the application asked for. This library has no
opinion about the extension: some applications use `.cfg`, some use `.json`,
and others use something else again.

<a id="edit_cfg_json.saving.NO_DESTINATION"></a>

#### NO\_DESTINATION

Message of a save that has nowhere to write to.

<a id="edit_cfg_json.saving.NOT_VALID"></a>

#### NOT\_VALID

Message of a save refused because the buffer is not a configuration.

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

What the description of a member is indented by, below that member.

The indentation is what says that the line belongs to the member above it
rather than being a member of its own.

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

Every mark can be shown at once, because they say three different things
that can all be true: the input file did not hold this member, the user
changed it, and a validator then changed what the user had written. They
are in the order in which they can happen. Both backends read the marks
from here, so that neither of them decides on its own what a member the
load, the user or a validator touched looks like.

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

<a id="edit_cfg_json.model_text._row_as_text"></a>

#### \_row\_as\_text

```python
def _row_as_text(model: EditModel, row: MemberRow) -> str
```

Return the line that shows one member, and its description below it.

<a id="edit_cfg_json.model_text.verdict_text"></a>

#### verdict\_text

```python
def verdict_text(model: EditModel) -> str
```

Return what the last validation pass found, as text.

A buffer that has not been validated since it last changed says so,
because that is a third state and not a kind of success. The
diagnostics follow on the lines below, and they can be present for an
accepted buffer too, since a validator may remark on a value without
refusing it.

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
  what the load did, one line per member with its description below it,
  and then the validation state and the saving, without a trailing line
  break.

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

<a id="edit_cfg_json.edit_model.MemberRow.description"></a>

#### description

What the application says about this member, empty when nothing.

It is read once, when the model is built, because it says what the member
is for and that does not change while it is edited. A member the
application said nothing about keeps an empty description and is shown
without one, which is all that an unexplained member costs.

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
def _row_of(name: str, value: JsonType, filled: frozenset[str],
            descriptions: Descriptions) -> MemberRow
```

Return the row of one serialized member of a configuration.

**Arguments**:

- `name` - Name of the member, which is the one step of its path while
  every member of the configuration is a scalar.
- `value` - JSON space value that the member holds.
- `filled` - Names of the members the declared defaults supplied.
- `descriptions` - What the application says about its members.
  

**Returns**:

  The row of that member, as the model starts out holding it.

<a id="edit_cfg_json.edit_model._rows_from_config"></a>

#### \_rows\_from\_config

```python
def _rows_from_config(config: Config, filled: frozenset[str],
                      descriptions: Descriptions,
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
have failed at the one thing it is for. Nor is anything written when
no destination has been chosen; the editor asks for one instead. Nor
when the destination is a file name that the application does not
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

<a id="edit_cfg_json.descriptions"></a>

# edit\_cfg\_json.descriptions

The explanatory text that the editor shows about a configuration.

There are two sources of it, they are independent, and both of them are
optional. The docstring of the configuration class labels the configuration
object, and a mapping supplied by the application labels the individual
members.

It takes two sources because only one of them exists. A class has a
docstring and every reader of the code can see it, while a member has
nothing of the kind at runtime: a string literal written after an assignment
is discarded by the compiler, and a PEP 526 annotation on an instance
attribute is recorded nowhere at all. So the members are described by the
application in a mapping, and the editor invents nothing.

<a id="edit_cfg_json.descriptions.EVERY_ELEMENT"></a>

#### EVERY\_ELEMENT

The path step that means every list element or dictionary value here.

It is the step that `config_as_json` gives this meaning to, and it keeps it
here, which is what stops an application from having to repeat one
description once per list index or once per dictionary key.

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
def class_docstring(config_type: type[Config]) -> str
```

Return the whole docstring of one configuration class, or nothing.

`config_type.__doc__` and deliberately not `inspect.getdoc()`, which
inherits from the base classes: a configuration class without a docstring
of its own would then be labelled with the docstring of `Config`, and a
label that describes the library rather than the configuration is worse
than no label at all.

**Arguments**:

- `config_type` - Class of the configuration that is being described.
  

**Returns**:

  The docstring of that class as `inspect.cleandoc` leaves it, and an
  empty text when the class has none of its own.

<a id="edit_cfg_json.descriptions.class_summary"></a>

#### class\_summary

```python
def class_summary(config_type: type[Config]) -> str
```

Return the first paragraph of the docstring, as a single line.

The first paragraph is the summary a docstring is written to begin with,
and one line is what a label of one row can show. The line breaks inside
that paragraph belong to the width of a source file and not to the text,
so they are not kept.

**Arguments**:

- `config_type` - Class of the configuration that is being described.
  

**Returns**:

  The summary of that class, and an empty text when it has no docstring.

<a id="edit_cfg_json.validation"></a>

# edit\_cfg\_json.validation

Running the application's own validation over one edit buffer.

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

What the application itself would tell the user about the buffer.

An accepted buffer can have diagnostics too, because a validator may
remark on a value without refusing it.

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

<a id="edit_cfg_json.validation._refused"></a>

#### \_refused

```python
def _refused(captured: str, error: Exception) -> ValidationVerdict
```

Return the verdict of a pass that the configuration class refused.

The captured text is what the application itself would have printed, so
it is what the user is shown. A failure that printed nothing has only
its exception left to report, which is better than no explanation.

**Arguments**:

- `captured` - What the candidate wrote to its diagnostics stream.
- `error` - The failure that the candidate reported.
  

**Returns**:

  A verdict saying that the buffer is not a configuration, and why.

<a id="edit_cfg_json.validation.validate_buffer"></a>

#### validate\_buffer

```python
def validate_buffer(config_type: type[Config],
                    members: dict[str, JsonType]) -> ValidationPass
```

Validate one edit buffer by constructing a candidate configuration.

Constructing a configuration object runs the whole chain that the
application runs when it reads its own file: key matching, the recursive
check of dict shapes against the defaults, the parse converters, the
nested configuration objects and then the validation plan. So the user
sees exactly the diagnostics that the application would produce, there
is no second implementation of validation anywhere, and there is no way
for the editor to accept something the application would then refuse.

The stream the candidate writes to is captured rather than passed on,
because these diagnostics are the answer to a question the user asked
and belong on the screen and not in the terminal behind it.

**Arguments**:

- `config_type` - Class of the configuration that is being edited.
- `members` - The edit buffer, as one JSON space value per member.
  

**Returns**:

  What the pass found, and the members of the configuration object it
  built. The members are empty when the buffer was refused.

