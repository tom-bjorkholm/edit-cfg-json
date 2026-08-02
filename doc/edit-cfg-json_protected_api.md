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
* [edit\_cfg\_json.leaf\_value](#edit_cfg_json.leaf_value)
  * [value\_as\_text](#edit_cfg_json.leaf_value.value_as_text)
  * [text\_as\_value](#edit_cfg_json.leaf_value.text_as_value)
  * [values\_differ](#edit_cfg_json.leaf_value.values_differ)
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
  * [row\_value\_text](#edit_cfg_json.model_text.row_value_text)
  * [row\_marks](#edit_cfg_json.model_text.row_marks)
  * [\_row\_as\_text](#edit_cfg_json.model_text._row_as_text)
  * [verdict\_text](#edit_cfg_json.model_text.verdict_text)
  * [load\_text](#edit_cfg_json.model_text.load_text)
  * [model\_as\_text](#edit_cfg_json.model_text.model_as_text)
  * [model\_title](#edit_cfg_json.model_text.model_title)
* [edit\_cfg\_json.edit\_model](#edit_cfg_json.edit_model)
  * [NOT\_EDITABLE\_ERROR](#edit_cfg_json.edit_model.NOT_EDITABLE_ERROR)
  * [MemberRow](#edit_cfg_json.edit_model.MemberRow)
    * [path](#edit_cfg_json.edit_model.MemberRow.path)
    * [value](#edit_cfg_json.edit_model.MemberRow.value)
    * [original](#edit_cfg_json.edit_model.MemberRow.original)
    * [changed\_by\_validator](#edit_cfg_json.edit_model.MemberRow.changed_by_validator)
    * [filled\_from\_default](#edit_cfg_json.edit_model.MemberRow.filled_from_default)
    * [name](#edit_cfg_json.edit_model.MemberRow.name)
    * [editable](#edit_cfg_json.edit_model.MemberRow.editable)
    * [is\_text](#edit_cfg_json.edit_model.MemberRow.is_text)
    * [edited](#edit_cfg_json.edit_model.MemberRow.edited)
  * [\_ordered\_names](#edit_cfg_json.edit_model._ordered_names)
  * [\_rows\_from\_config](#edit_cfg_json.edit_model._rows_from_config)
  * [EditModel](#edit_cfg_json.edit_model.EditModel)
    * [\_\_init\_\_](#edit_cfg_json.edit_model.EditModel.__init__)
    * [config\_type\_name](#edit_cfg_json.edit_model.EditModel.config_type_name)
    * [load\_message](#edit_cfg_json.edit_model.EditModel.load_message)
    * [rows](#edit_cfg_json.edit_model.EditModel.rows)
    * [dirty](#edit_cfg_json.edit_model.EditModel.dirty)
    * [verdict](#edit_cfg_json.edit_model.EditModel.verdict)
    * [set\_text](#edit_cfg_json.edit_model.EditModel.set_text)
    * [validate](#edit_cfg_json.edit_model.EditModel.validate)
    * [\_buffer](#edit_cfg_json.edit_model.EditModel._buffer)
    * [\_take\_validated](#edit_cfg_json.edit_model.EditModel._take_validated)
* [edit\_cfg\_json.validation](#edit_cfg_json.validation)
  * [BUFFER\_ERRORS](#edit_cfg_json.validation.BUFFER_ERRORS)
  * [ValidationVerdict](#edit_cfg_json.validation.ValidationVerdict)
    * [valid](#edit_cfg_json.validation.ValidationVerdict.valid)
    * [diagnostics](#edit_cfg_json.validation.ValidationVerdict.diagnostics)
  * [ValidationPass](#edit_cfg_json.validation.ValidationPass)
    * [verdict](#edit_cfg_json.validation.ValidationPass.verdict)
    * [members](#edit_cfg_json.validation.ValidationPass.members)
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
def load_config(config: Config,
                in_file: Optional[PathOrStr] = None,
                policy: LoadPolicy = DEFAULT_POLICY) -> LoadedConfig
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
- `in_file` - File to read, or None to edit the declared defaults.
- `policy` - What to do about declared keys the file does not hold.
  

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

The protocol is phrased against the model and not against a convenience
wrapper, so that an application that already runs its own event loop can
build the model itself and mount the backend as a widget. The outcome of
the session is read from the model afterwards rather than returned here,
so that the protocol does not have to change when saving is added.

<a id="edit_cfg_json.backend.EditorBackend.run_editor"></a>

#### run\_editor

```python
def run_editor(model: EditModel) -> None
```

Run the user interface for one model until the user is done.

**Arguments**:

- `model` - Model to show. The backend reads and edits the model, and
  never touches the caller's configuration object.

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

<a id="edit_cfg_json.model_text._row_as_text"></a>

#### \_row\_as\_text

```python
def _row_as_text(row: MemberRow) -> str
```

Return the one line of text that shows the state of one member.

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

<a id="edit_cfg_json.model_text.model_as_text"></a>

#### model\_as\_text

```python
def model_as_text(model: EditModel) -> str
```

Return the whole model as text, one line per configuration member.

What reading the input file did comes before the members, because it is
what explains the marks on them. The validation state of the buffer
follows them, so that a rendering never leaves it unsaid what the
application would make of what is shown. This is the rendering used by
the examples and by the tests, so that every step of the editor can be
observed without a display. It belongs to the core rather than to a
backend because it is user interface agnostic.

**Arguments**:

- `model` - Model to render.
  

**Returns**:

  What the load did, one line per member and then the validation
  state, without a trailing line break.

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

Value that this member had when the model was built.

It is what the current value is compared against, and it is also the only
type information that the model has. A PEP 526 annotation on an instance
attribute is recorded nowhere at runtime, so the value that the
configuration object holds is the only source of the type. Reading the
type from the current value instead would not work: a number member that
the user has half typed holds text for as long as the text is not a
number yet, and the member would then stop being a number member.

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

Return whether the user changed this member.

A member is changed when it would now be written to the file
differently, and not when it merely was typed in. Typing a value
back to what it was leaves nothing to save, and an editor that still
claimed to have changes would be telling the user something untrue.

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

<a id="edit_cfg_json.edit_model._rows_from_config"></a>

#### \_rows\_from\_config

```python
def _rows_from_config(config: Config, filled: frozenset[str],
                      stderr_file: TextIO) -> list[MemberRow]
```

Return one row per serialized member, in declaration order.

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
accept anything the application would refuse.

This version of the model handles scalar members only. A member whose
value is a list or a dict is reported as a row that is not editable.

<a id="edit_cfg_json.edit_model.EditModel.__init__"></a>

#### \_\_init\_\_

```python
def __init__(config: Config,
             report: LoadReport = LoadReport(),
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

A member the validated object does not serialize keeps the value the
buffer holds. That happens when a validator sets a member that the
class leaves out of JSON while it is None, and there is then no
value to read back rather than a value that changed.

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

