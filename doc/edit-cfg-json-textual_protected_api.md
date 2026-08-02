# Table of Contents

* [edit\_cfg\_json\_textual.textual\_editor](#edit_cfg_json_textual.textual_editor)
  * [VALUE\_ID\_PREFIX](#edit_cfg_json_textual.textual_editor.VALUE_ID_PREFIX)
  * [MARK\_ID\_PREFIX](#edit_cfg_json_textual.textual_editor.MARK_ID_PREFIX)
  * [VERDICT\_ID](#edit_cfg_json_textual.textual_editor.VERDICT_ID)
  * [NAME\_CLASS](#edit_cfg_json_textual.textual_editor.NAME_CLASS)
  * [ROW\_CLASS](#edit_cfg_json_textual.textual_editor.ROW_CLASS)
  * [NAME\_WIDTH](#edit_cfg_json_textual.textual_editor.NAME_WIDTH)
  * [QUIT\_KEY](#edit_cfg_json_textual.textual_editor.QUIT_KEY)
  * [VALIDATE\_KEY](#edit_cfg_json_textual.textual_editor.VALIDATE_KEY)
  * [\_value\_id](#edit_cfg_json_textual.textual_editor._value_id)
  * [\_mark\_id](#edit_cfg_json_textual.textual_editor._mark_id)
  * [plain\_widget](#edit_cfg_json_textual.textual_editor.plain_widget)
  * [EditorApp](#edit_cfg_json_textual.textual_editor.EditorApp)
    * [BINDINGS](#edit_cfg_json_textual.textual_editor.EditorApp.BINDINGS)
    * [CSS](#edit_cfg_json_textual.textual_editor.EditorApp.CSS)
    * [\_\_init\_\_](#edit_cfg_json_textual.textual_editor.EditorApp.__init__)
    * [compose](#edit_cfg_json_textual.textual_editor.EditorApp.compose)
    * [\_value\_widget](#edit_cfg_json_textual.textual_editor.EditorApp._value_widget)
    * [on\_input\_changed](#edit_cfg_json_textual.textual_editor.EditorApp.on_input_changed)
    * [action\_validate](#edit_cfg_json_textual.textual_editor.EditorApp.action_validate)
    * [\_field](#edit_cfg_json_textual.textual_editor.EditorApp._field)
    * [\_show\_state](#edit_cfg_json_textual.textual_editor.EditorApp._show_state)
  * [TextualEditor](#edit_cfg_json_textual.textual_editor.TextualEditor)
    * [run\_editor](#edit_cfg_json_textual.textual_editor.TextualEditor.run_editor)

<a id="edit_cfg_json_textual.textual_editor"></a>

# edit\_cfg\_json\_textual.textual\_editor

Textual view of an edit model, with one editable field per member.

<a id="edit_cfg_json_textual.textual_editor.VALUE_ID_PREFIX"></a>

#### VALUE\_ID\_PREFIX

Prefix of the identifier of the widget that shows one member value.

<a id="edit_cfg_json_textual.textual_editor.MARK_ID_PREFIX"></a>

#### MARK\_ID\_PREFIX

Prefix of the identifier of the widget that marks one member.

<a id="edit_cfg_json_textual.textual_editor.VERDICT_ID"></a>

#### VERDICT\_ID

Identifier of the widget that shows what validation found.

<a id="edit_cfg_json_textual.textual_editor.NAME_CLASS"></a>

#### NAME\_CLASS

Style class of the widget that shows one member name.

<a id="edit_cfg_json_textual.textual_editor.ROW_CLASS"></a>

#### ROW\_CLASS

Style class of the container that holds the widgets of one member.

<a id="edit_cfg_json_textual.textual_editor.NAME_WIDTH"></a>

#### NAME\_WIDTH

Width in cells of the column that holds the member names.

<a id="edit_cfg_json_textual.textual_editor.QUIT_KEY"></a>

#### QUIT\_KEY

Key that ends the editor.

A single letter cannot be used for this any more, now that the value of a
member is edited in a field: an unmodified letter belongs to whichever field
has the focus, and a user who typed it would expect to see it appear.

<a id="edit_cfg_json_textual.textual_editor.VALIDATE_KEY"></a>

#### VALIDATE\_KEY

Key that validates the buffer.

A function key for the same reason as the quit key, and this one in
particular because it is what a user of other editors reaches for to ask a
tool to check what has been written.

<a id="edit_cfg_json_textual.textual_editor._value_id"></a>

#### \_value\_id

```python
def _value_id(row: MemberRow) -> str
```

Return the identifier of the widget that shows one member value.

<a id="edit_cfg_json_textual.textual_editor._mark_id"></a>

#### \_mark\_id

```python
def _mark_id(row: MemberRow) -> str
```

Return the identifier of the widget that marks one member.

<a id="edit_cfg_json_textual.textual_editor.plain_widget"></a>

#### plain\_widget

```python
def plain_widget(text: str, widget_id: str) -> Static
```

Return a widget that shows text of the configuration as it is.

Textual reads console markup in the text of a widget, so a square
bracket in a configuration value or in a diagnostic would be taken for
the beginning of a style and the text between brackets would silently
disappear. Nothing here is written by this editor, so nothing here is
markup.

**Arguments**:

- `text` - Text to show exactly as it is.
- `widget_id` - Identifier the application finds this widget by.
  

**Returns**:

  A widget showing that text.

<a id="edit_cfg_json_textual.textual_editor.EditorApp"></a>

## EditorApp Objects

```python
class EditorApp(App[None])
```

Textual application that edits one edit model.

<a id="edit_cfg_json_textual.textual_editor.EditorApp.BINDINGS"></a>

#### BINDINGS

The keys the footer shows, so that they can be found.

They are priority bindings, so that they are acted on before the field
that has the focus is offered the key.

<a id="edit_cfg_json_textual.textual_editor.EditorApp.CSS"></a>

#### CSS

One cell high rows, so that the footer stays visible below them.

A field is one cell high as well, which needs its border and its padding
taken away, because both of them are part of how tall a field is.

<a id="edit_cfg_json_textual.textual_editor.EditorApp.__init__"></a>

#### \_\_init\_\_

```python
def __init__(model: EditModel) -> None
```

Remember the model and name the application after it.

**Arguments**:

- `model` - Model to show and to edit.

<a id="edit_cfg_json_textual.textual_editor.EditorApp.compose"></a>

#### compose

```python
def compose() -> ComposeResult
```

Create one row per member, the verdict, a header and a footer.

<a id="edit_cfg_json_textual.textual_editor.EditorApp._value_widget"></a>

#### \_value\_widget

```python
def _value_widget(row: MemberRow) -> Widget
```

Return the widget that shows the value of one member.

A member that the model cannot edit yet gets a widget that only
shows text, because there is nothing the user could do to it.

<a id="edit_cfg_json_textual.textual_editor.EditorApp.on_input_changed"></a>

#### on\_input\_changed

```python
def on_input_changed(event: Input.Changed) -> None
```

Write one field into the model and show what the model says.

A field posts this message when it is given its initial value as
well, which the model handles by treating a set that changes no text
as no edit at all.

<a id="edit_cfg_json_textual.textual_editor.EditorApp.action_validate"></a>

#### action\_validate

```python
def action_validate() -> None
```

Validate the buffer and show what the application would say.

The fields are written back from the model afterwards, because a
validation pass is not read only: a member validator returns the
value that is stored back into the member, so a value can end up
different from the one the user typed. Writing the text the model
already holds into a field is not an edit, so this refresh does not
undo the marks that the pass has just set.

<a id="edit_cfg_json_textual.textual_editor.EditorApp._field"></a>

#### \_field

```python
def _field(row: MemberRow) -> Input
```

Return the field that this application shows for one member.

<a id="edit_cfg_json_textual.textual_editor.EditorApp._show_state"></a>

#### \_show\_state

```python
def _show_state() -> None
```

Show the title, the verdict and the mark of every member.

<a id="edit_cfg_json_textual.textual_editor.TextualEditor"></a>

## TextualEditor Objects

```python
class TextualEditor()
```

Textual user interface backend for an edit model.

The class has the single method that `EditorBackend` asks for, and
deliberately nothing else: everything worth testing without a terminal
lives in the core.

<a id="edit_cfg_json_textual.textual_editor.TextualEditor.run_editor"></a>

#### run\_editor

```python
def run_editor(model: EditModel) -> None
```

Show the model in a Textual screen until the user quits.

**Arguments**:

- `model` - Model to show and to edit.

