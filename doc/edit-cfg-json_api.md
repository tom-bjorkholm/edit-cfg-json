# Table of Contents

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
  * [DIRTY\_MARK](#edit_cfg_json.model_text.DIRTY_MARK)
  * [row\_value\_text](#edit_cfg_json.model_text.row_value_text)
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
  * [EditModel](#edit_cfg_json.edit_model.EditModel)
    * [\_\_init\_\_](#edit_cfg_json.edit_model.EditModel.__init__)
    * [config\_type\_name](#edit_cfg_json.edit_model.EditModel.config_type_name)
    * [rows](#edit_cfg_json.edit_model.EditModel.rows)
    * [dirty](#edit_cfg_json.edit_model.EditModel.dirty)
    * [set\_text](#edit_cfg_json.edit_model.EditModel.set_text)

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

<a id="edit_cfg_json.model_text.DIRTY_MARK"></a>

#### DIRTY\_MARK

Mark that follows the model label while the buffer has changes.

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

<a id="edit_cfg_json.model_text.model_as_text"></a>

#### model\_as\_text

```python
def model_as_text(model: EditModel) -> str
```

Return the whole model as one text line per configuration member.

This is the rendering used by the examples and by the tests, so that
every step of the editor can be observed without a display. It belongs
to the core rather than to a backend because it is user interface
agnostic.

**Arguments**:

- `model` - Model to render.
  

**Returns**:

  One line per member, without a trailing line break.

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

This is storage for a flag that validation sets, which arrives in a later
step. It belongs to the model rather than to a backend, so that two
backends cannot end up showing it differently.

<a id="edit_cfg_json.edit_model.MemberRow.filled_from_default"></a>

#### filled\_from\_default

Whether a permissive load supplied this value.

This is storage for a flag that loading sets, which arrives in a later
step, and it belongs to the model for the same reason as the flag above.

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

This version of the model handles scalar members only. A member whose
value is a list or a dict is reported as a row that is not editable.

<a id="edit_cfg_json.edit_model.EditModel.__init__"></a>

#### \_\_init\_\_

```python
def __init__(config: Config, stderr_file: TextIO = sys.stderr) -> None
```

Read the JSON space values of one configuration object.

The object is deep copied before it is serialized, because
`Config.as_json_string()` validates, and a member validator returns
the value that is stored back into the member. Serializing the
caller's object directly could therefore change it, and the editor
never mutates the caller's configuration object.

**Arguments**:

- `config` - Configuration object to edit. It is the source of both
  the member names and their values, and is not modified.
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

**Arguments**:

- `path` - Path of the member to set.
- `text` - Text that the edit field holds.
  

**Raises**:

- `KeyError` - The path is not a member of this configuration.
- `ValueError` - The member is not one that this version can edit.

