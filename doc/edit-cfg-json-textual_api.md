# Table of Contents

* [edit\_cfg\_json\_textual.textual\_editor](#edit_cfg_json_textual.textual_editor)
  * [VALUE\_ID\_PREFIX](#edit_cfg_json_textual.textual_editor.VALUE_ID_PREFIX)
  * [MARK\_ID\_PREFIX](#edit_cfg_json_textual.textual_editor.MARK_ID_PREFIX)
  * [VERDICT\_ID](#edit_cfg_json_textual.textual_editor.VERDICT_ID)
  * [LOAD\_ID](#edit_cfg_json_textual.textual_editor.LOAD_ID)
  * [NAME\_CLASS](#edit_cfg_json_textual.textual_editor.NAME_CLASS)
  * [VALUE\_CLASS](#edit_cfg_json_textual.textual_editor.VALUE_CLASS)
  * [MARK\_CLASS](#edit_cfg_json_textual.textual_editor.MARK_CLASS)
  * [ROW\_CLASS](#edit_cfg_json_textual.textual_editor.ROW_CLASS)
  * [NAME\_WIDTH](#edit_cfg_json_textual.textual_editor.NAME_WIDTH)
  * [LEAST\_VALUE\_WIDTH](#edit_cfg_json_textual.textual_editor.LEAST_VALUE_WIDTH)
  * [QUIT\_KEY](#edit_cfg_json_textual.textual_editor.QUIT_KEY)
  * [VALIDATE\_KEY](#edit_cfg_json_textual.textual_editor.VALIDATE_KEY)
  * [VALIDATE\_ALT\_KEY](#edit_cfg_json_textual.textual_editor.VALIDATE_ALT_KEY)
  * [CSS\_RULES](#edit_cfg_json_textual.textual_editor.CSS_RULES)
  * [plain\_widget](#edit_cfg_json_textual.textual_editor.plain_widget)
  * [EditorApp](#edit_cfg_json_textual.textual_editor.EditorApp)
    * [BINDINGS](#edit_cfg_json_textual.textual_editor.EditorApp.BINDINGS)
    * [CSS](#edit_cfg_json_textual.textual_editor.EditorApp.CSS)
    * [\_\_init\_\_](#edit_cfg_json_textual.textual_editor.EditorApp.__init__)
    * [compose](#edit_cfg_json_textual.textual_editor.EditorApp.compose)
    * [on\_input\_changed](#edit_cfg_json_textual.textual_editor.EditorApp.on_input_changed)
    * [action\_validate](#edit_cfg_json_textual.textual_editor.EditorApp.action_validate)
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

<a id="edit_cfg_json_textual.textual_editor.LOAD_ID"></a>

#### LOAD\_ID

Identifier of the widget that shows what reading the file did.

<a id="edit_cfg_json_textual.textual_editor.NAME_CLASS"></a>

#### NAME\_CLASS

Style class of the widget that shows one member name.

<a id="edit_cfg_json_textual.textual_editor.VALUE_CLASS"></a>

#### VALUE\_CLASS

Style class of the widget that shows or edits one member value.

<a id="edit_cfg_json_textual.textual_editor.MARK_CLASS"></a>

#### MARK\_CLASS

Style class of the widget that marks one member.

<a id="edit_cfg_json_textual.textual_editor.ROW_CLASS"></a>

#### ROW\_CLASS

Style class of the container that holds the widgets of one member.

<a id="edit_cfg_json_textual.textual_editor.NAME_WIDTH"></a>

#### NAME\_WIDTH

Width in cells of the column that holds the member names.

<a id="edit_cfg_json_textual.textual_editor.LEAST_VALUE_WIDTH"></a>

#### LEAST\_VALUE\_WIDTH

Smallest width in cells that the value of a member is given.

A row that does not fit the terminal has to give way somewhere, and it is
the marks that are cut rather than the field: the field is what the user
edits, and `model_as_text` shows every mark in full whatever the terminal.

<a id="edit_cfg_json_textual.textual_editor.QUIT_KEY"></a>

#### QUIT\_KEY

Key that ends the editor.

A single letter cannot be used for this any more, now that the value of a
member is edited in a field: an unmodified letter belongs to whichever field
has the focus, and a user who typed it would expect to see it appear.

<a id="edit_cfg_json_textual.textual_editor.VALIDATE_KEY"></a>

#### VALIDATE\_KEY

Key that validates the buffer, and the one the footer names.

Not a plain letter, for the same reason as the quit key. This letter in
particular because a field claims most of the others: `Input` already reads
`ctrl+a`, `ctrl+c`, `ctrl+d`, `ctrl+e`, `ctrl+k`, `ctrl+u`, `ctrl+v`,
`ctrl+w` and `ctrl+x`, and the terminal itself claims `ctrl+c`, `ctrl+d`,
`ctrl+s`, `ctrl+z` and the four that are Backspace, Tab, Return and Escape.
Of what is left, `r` is the one that means something: re-check.

<a id="edit_cfg_json_textual.textual_editor.VALIDATE_ALT_KEY"></a>

#### VALIDATE\_ALT\_KEY

The other key that validates the buffer.

Function keys are what other editors use to ask a tool to check what has
been written, so the key is kept. It is not shown in the footer, because a
footer that named the same action twice would suggest they were two
actions, and because a function key is the one of the two that a keyboard
or a terminal is most likely not to deliver.

<a id="edit_cfg_json_textual.textual_editor.CSS_RULES"></a>

#### CSS\_RULES

The width and the height of every part of one member row.

Rows are one cell high, so that the footer stays visible below them. A field
is one cell high as well, which needs its border and its padding taken away,
because both of them are part of how tall a field is.

The widths are the part that has to be said rather than left to Textual. A
`Input` is a full width widget of its own accord, so it would take the whole
line and lay the marks of the member out beyond the right edge of the screen,
where they are there and cannot be seen. The value therefore takes what is
left over and the marks take what they need, which is the opposite way round
from the default and the only way round that shows both.

<a id="edit_cfg_json_textual.textual_editor.plain_widget"></a>

#### plain\_widget

```python
def plain_widget(text: str,
                 widget_id: str,
                 classes: Optional[str] = None) -> Static
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
- `classes` - Style classes of the widget, or None for a widget that the
  style sheet does not have to reach.
  

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

What the keys of the editor do, and which of them the footer names.

They are priority bindings, so that they are acted on before the field
that has the focus is offered the key. The two keys that validate are
two bindings rather than one binding of two keys, because that is what
lets the footer name one of them and still leave the other working.

<a id="edit_cfg_json_textual.textual_editor.EditorApp.CSS"></a>

#### CSS

The widths and heights that make one member fit on one line.

See `CSS_RULES`, which is where each of them is explained.

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

What reading the input file did comes above the members, because it
is what explains the marks on them. It is created only when there is
something to say: the file was read before the model was built, so
the message cannot arrive later, and an empty widget would take a
line of the screen for a message that will never come.

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

