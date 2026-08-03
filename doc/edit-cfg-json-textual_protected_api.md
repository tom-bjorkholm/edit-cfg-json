# Table of Contents

* [edit\_cfg\_json\_textual.textual\_editor](#edit_cfg_json_textual.textual_editor)
  * [VALUE\_ID\_PREFIX](#edit_cfg_json_textual.textual_editor.VALUE_ID_PREFIX)
  * [MARK\_ID\_PREFIX](#edit_cfg_json_textual.textual_editor.MARK_ID_PREFIX)
  * [VERDICT\_ID](#edit_cfg_json_textual.textual_editor.VERDICT_ID)
  * [SAVE\_ID](#edit_cfg_json_textual.textual_editor.SAVE_ID)
  * [LOAD\_ID](#edit_cfg_json_textual.textual_editor.LOAD_ID)
  * [SAVE\_AS\_BOX\_ID](#edit_cfg_json_textual.textual_editor.SAVE_AS_BOX_ID)
  * [SAVE\_AS\_ID](#edit_cfg_json_textual.textual_editor.SAVE_AS_ID)
  * [NAME\_CLASS](#edit_cfg_json_textual.textual_editor.NAME_CLASS)
  * [VALUE\_CLASS](#edit_cfg_json_textual.textual_editor.VALUE_CLASS)
  * [MARK\_CLASS](#edit_cfg_json_textual.textual_editor.MARK_CLASS)
  * [ROW\_CLASS](#edit_cfg_json_textual.textual_editor.ROW_CLASS)
  * [NAME\_WIDTH](#edit_cfg_json_textual.textual_editor.NAME_WIDTH)
  * [LEAST\_VALUE\_WIDTH](#edit_cfg_json_textual.textual_editor.LEAST_VALUE_WIDTH)
  * [QUIT\_COMMAND](#edit_cfg_json_textual.textual_editor.QUIT_COMMAND)
  * [CANCEL\_COMMAND](#edit_cfg_json_textual.textual_editor.CANCEL_COMMAND)
  * [VALIDATE\_COMMAND](#edit_cfg_json_textual.textual_editor.VALIDATE_COMMAND)
  * [SAVE\_COMMAND](#edit_cfg_json_textual.textual_editor.SAVE_COMMAND)
  * [SAVE\_AS\_COMMAND](#edit_cfg_json_textual.textual_editor.SAVE_AS_COMMAND)
  * [VALIDATE\_HELP](#edit_cfg_json_textual.textual_editor.VALIDATE_HELP)
  * [SAVE\_HELP](#edit_cfg_json_textual.textual_editor.SAVE_HELP)
  * [SAVE\_AS\_HELP](#edit_cfg_json_textual.textual_editor.SAVE_AS_HELP)
  * [SAVE\_AS\_PROMPT](#edit_cfg_json_textual.textual_editor.SAVE_AS_PROMPT)
  * [SAVE\_AS\_LEAVE](#edit_cfg_json_textual.textual_editor.SAVE_AS_LEAVE)
  * [EDITOR\_ACTIONS](#edit_cfg_json_textual.textual_editor.EDITOR_ACTIONS)
  * [CSS\_RULES](#edit_cfg_json_textual.textual_editor.CSS_RULES)
  * [\_value\_id](#edit_cfg_json_textual.textual_editor._value_id)
  * [\_mark\_id](#edit_cfg_json_textual.textual_editor._mark_id)
  * [plain\_widget](#edit_cfg_json_textual.textual_editor.plain_widget)
  * [bind\_action](#edit_cfg_json_textual.textual_editor.bind_action)
  * [SaveAsScreen](#edit_cfg_json_textual.textual_editor.SaveAsScreen)
    * [\_\_init\_\_](#edit_cfg_json_textual.textual_editor.SaveAsScreen.__init__)
    * [compose](#edit_cfg_json_textual.textual_editor.SaveAsScreen.compose)
    * [\_prompt](#edit_cfg_json_textual.textual_editor.SaveAsScreen._prompt)
    * [on\_input\_changed](#edit_cfg_json_textual.textual_editor.SaveAsScreen.on_input_changed)
    * [on\_input\_submitted](#edit_cfg_json_textual.textual_editor.SaveAsScreen.on_input_submitted)
    * [action\_leave](#edit_cfg_json_textual.textual_editor.SaveAsScreen.action_leave)
  * [EditorApp](#edit_cfg_json_textual.textual_editor.EditorApp)
    * [CSS](#edit_cfg_json_textual.textual_editor.EditorApp.CSS)
    * [\_\_init\_\_](#edit_cfg_json_textual.textual_editor.EditorApp.__init__)
    * [\_bind\_editor\_keys](#edit_cfg_json_textual.textual_editor.EditorApp._bind_editor_keys)
    * [compose](#edit_cfg_json_textual.textual_editor.EditorApp.compose)
    * [get\_system\_commands](#edit_cfg_json_textual.textual_editor.EditorApp.get_system_commands)
    * [\_load\_widgets](#edit_cfg_json_textual.textual_editor.EditorApp._load_widgets)
    * [\_value\_widget](#edit_cfg_json_textual.textual_editor.EditorApp._value_widget)
    * [on\_input\_changed](#edit_cfg_json_textual.textual_editor.EditorApp.on_input_changed)
    * [action\_validate](#edit_cfg_json_textual.textual_editor.EditorApp.action_validate)
    * [action\_save](#edit_cfg_json_textual.textual_editor.EditorApp.action_save)
    * [action\_save\_as](#edit_cfg_json_textual.textual_editor.EditorApp.action_save_as)
    * [check\_action](#edit_cfg_json_textual.textual_editor.EditorApp.check_action)
    * [\_out\_file\_text](#edit_cfg_json_textual.textual_editor.EditorApp._out_file_text)
    * [\_save\_to](#edit_cfg_json_textual.textual_editor.EditorApp._save_to)
    * [\_refresh](#edit_cfg_json_textual.textual_editor.EditorApp._refresh)
    * [\_field](#edit_cfg_json_textual.textual_editor.EditorApp._field)
    * [\_show\_state](#edit_cfg_json_textual.textual_editor.EditorApp._show_state)
  * [TextualEditor](#edit_cfg_json_textual.textual_editor.TextualEditor)
    * [run\_editor](#edit_cfg_json_textual.textual_editor.TextualEditor.run_editor)
  * [edit](#edit_cfg_json_textual.textual_editor.edit)

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

<a id="edit_cfg_json_textual.textual_editor.SAVE_ID"></a>

#### SAVE\_ID

Identifier of the widget that shows what saving did or would do.

<a id="edit_cfg_json_textual.textual_editor.LOAD_ID"></a>

#### LOAD\_ID

Identifier of the widget that shows what reading the file did.

<a id="edit_cfg_json_textual.textual_editor.SAVE_AS_BOX_ID"></a>

#### SAVE\_AS\_BOX\_ID

Identifier of the box that asks which file to write.

<a id="edit_cfg_json_textual.textual_editor.SAVE_AS_ID"></a>

#### SAVE\_AS\_ID

Identifier of the field that the file to write is typed into.

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

<a id="edit_cfg_json_textual.textual_editor.QUIT_COMMAND"></a>

#### QUIT\_COMMAND

Name of the action that ends the editor.

<a id="edit_cfg_json_textual.textual_editor.CANCEL_COMMAND"></a>

#### CANCEL\_COMMAND

Name of the action that leaves the question about the output file.

<a id="edit_cfg_json_textual.textual_editor.VALIDATE_COMMAND"></a>

#### VALIDATE\_COMMAND

Name of the command palette entry that validates the buffer.

<a id="edit_cfg_json_textual.textual_editor.SAVE_COMMAND"></a>

#### SAVE\_COMMAND

Name of the command palette entry that writes the output file.

<a id="edit_cfg_json_textual.textual_editor.SAVE_AS_COMMAND"></a>

#### SAVE\_AS\_COMMAND

Name of the command palette entry that chooses a file and writes it.

<a id="edit_cfg_json_textual.textual_editor.VALIDATE_HELP"></a>

#### VALIDATE\_HELP

What the command palette says the validate entry does.

<a id="edit_cfg_json_textual.textual_editor.SAVE_HELP"></a>

#### SAVE\_HELP

What the command palette says the save entry does.

<a id="edit_cfg_json_textual.textual_editor.SAVE_AS_HELP"></a>

#### SAVE\_AS\_HELP

What the command palette says the save as entry does.

<a id="edit_cfg_json_textual.textual_editor.SAVE_AS_PROMPT"></a>

#### SAVE\_AS\_PROMPT

What the screen that asks for the output file says.

<a id="edit_cfg_json_textual.textual_editor.SAVE_AS_LEAVE"></a>

#### SAVE\_AS\_LEAVE

What that screen says while there is a key that leaves it.

The key is named from the settings and not written into the sentence,
because an application that took `escape` for itself would otherwise be
telling its users to press a key that does nothing.

<a id="edit_cfg_json_textual.textual_editor.EDITOR_ACTIONS"></a>

#### EDITOR\_ACTIONS

The actions of the editor, which a question of its own turns off.

Textual offers a priority binding of an application the key before the screen
that has the focus, and it goes on doing that while a modal screen is up: the
dispatch of a priority binding walks the whole chain and not the part of it
above the last modal screen. So a modal screen is only really modal if the
application says that its own actions do not apply while it is there.

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

The question about the output file sits in the middle of the screen and takes
most of its width, so that a long path is still readable in a narrow
terminal. Its own field is untouched by the rule above, which reaches only
the fields inside a member row.

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

<a id="edit_cfg_json_textual.textual_editor.bind_action"></a>

#### bind\_action

```python
def bind_action(bindings: BindingsMap, keys: Sequence[str], action: str,
                description: str) -> None
```

Bind every key combination that the application gave one action.

The first combination is the one the footer names and the rest work
without being named, because a footer that named one action twice would
suggest that they were two actions. An action the application gave no
combination at all is bound to nothing and stays reachable through the
command palette.

Every binding is a priority binding, so that it is acted on before the
field that has the focus is offered the key. That is also why the
bindings cannot be made with `App.bind`, which cannot make one and which
says of itself that it may be removed.

**Arguments**:

- `bindings` - The bindings of the application or of the screen that the
  action belongs to.
- `keys` - Key combinations that run the action, in the order that
  decides which of them is named.
- `action` - Name of the action, without its `action_` prefix.
- `description` - What the footer and the key panel call the action.

<a id="edit_cfg_json_textual.textual_editor.SaveAsScreen"></a>

## SaveAsScreen Objects

```python
class SaveAsScreen(ModalScreen[Optional[str]])
```

Ask which file to write, and give back None when none was named.

The question is a screen of its own rather than a field in the editor,
because it is asked, answered and gone: a field that was always there
would be a fifth thing to read on every row of every session, for a
question that is asked once or never.

<a id="edit_cfg_json_textual.textual_editor.SaveAsScreen.__init__"></a>

#### \_\_init\_\_

```python
def __init__(out_file: str, cancel_keys: Sequence[str]) -> None
```

Start the field at the file that would be written now.

The keys that leave the question are bound here rather than declared
as a class variable, because which keys they are is the
application's decision and not this screen's.

**Arguments**:

- `out_file` - File that saving would write, empty when there is none
  yet. Starting from it is what makes saving a copy beside the
  original a matter of changing a few characters.
- `cancel_keys` - Key combinations that leave the question
  unanswered, empty when the application gave it none.

<a id="edit_cfg_json_textual.textual_editor.SaveAsScreen.compose"></a>

#### compose

```python
def compose() -> ComposeResult
```

Create the question and the field that answers it.

<a id="edit_cfg_json_textual.textual_editor.SaveAsScreen._prompt"></a>

#### \_prompt

```python
def _prompt() -> str
```

Return what this screen says, naming the key that leaves it.

<a id="edit_cfg_json_textual.textual_editor.SaveAsScreen.on_input_changed"></a>

#### on\_input\_changed

```python
def on_input_changed(event: Input.Changed) -> None
```

Keep what happens in this field to this screen.

The editor underneath writes every field change into the model, and
this field is not a member of the configuration: it is the name of a
file. A message that reached the editor would be looked for among the
members and found nowhere.

<a id="edit_cfg_json_textual.textual_editor.SaveAsScreen.on_input_submitted"></a>

#### on\_input\_submitted

```python
def on_input_submitted(event: Input.Submitted) -> None
```

Give back the file that was named, and leave the screen.

<a id="edit_cfg_json_textual.textual_editor.SaveAsScreen.action_leave"></a>

#### action\_leave

```python
def action_leave() -> None
```

Leave the screen without naming a file.

<a id="edit_cfg_json_textual.textual_editor.EditorApp"></a>

## EditorApp Objects

```python
class EditorApp(App[None])
```

Textual application that edits one edit model.

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

<a id="edit_cfg_json_textual.textual_editor.EditorApp._bind_editor_keys"></a>

#### \_bind\_editor\_keys

```python
def _bind_editor_keys() -> None
```

Bind the key combinations that the application chose.

The bindings are made on this instance rather than declared as a
class variable, because which keys the editor takes is not the
editor's decision any more: the application it runs inside has
already given some of them to itself. They are read once, here,
which is the whole of what a later answer from a settings callable
cannot change.

A footer too narrow for all of them shows what fits, which costs
nothing: the key panel of the command palette lists every binding,
including the ones the footer never shows.

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

<a id="edit_cfg_json_textual.textual_editor.EditorApp.get_system_commands"></a>

#### get\_system\_commands

```python
def get_system_commands(screen: Screen[object]) -> Iterable[SystemCommand]
```

Offer the actions of the editor in the command palette as well.

Every terminal can reach the palette, because it is opened with one
key and then typed into. That is what makes it the answer for
`SAVE_AS_KEY`, which a terminal without the Kitty keyboard protocol
cannot tell apart from `SAVE_KEY`. The other two actions are here for
the same reason a menu lists what has a shortcut: a user who has not
learnt the keys should still be able to work.

**Arguments**:

- `screen` - Screen the palette was opened from.
  

**Returns**:

  The commands of Textual itself, and then the ones of the editor.

<a id="edit_cfg_json_textual.textual_editor.EditorApp._load_widgets"></a>

#### \_load\_widgets

```python
def _load_widgets() -> ComposeResult
```

Create the widget that says what reading the input file did.

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

<a id="edit_cfg_json_textual.textual_editor.EditorApp.action_save"></a>

#### action\_save

```python
def action_save() -> None
```

Write the output file, and say what came of trying.

Saving validates, so it can rewrite a value exactly as validating
can, and the fields are refreshed for the same reason.

A session that has no file to write yet is asked where to write,
which is what every editor does and what the design asks a backend
for. There is no way round to loop back here, because the question
is what gives the session a file.

<a id="edit_cfg_json_textual.textual_editor.EditorApp.action_save_as"></a>

#### action\_save\_as

```python
def action_save_as() -> None
```

Ask which file to write, and write it when one was named.

<a id="edit_cfg_json_textual.textual_editor.EditorApp.check_action"></a>

#### check\_action

```python
def check_action(action: str, parameters: tuple[object,
                                                ...]) -> Optional[bool]
```

Turn the actions of the editor off while it is asking a question.

See `EDITOR_ACTIONS` for why this is needed at all. The answer is
None rather than False, so that the footer shows the actions greyed
out instead of losing them: a user who is answering a question should
be able to see that the rest of the editor is waiting for them.

**Arguments**:

- `action` - Name of the action that is about to run.
- `parameters` - Arguments of that action, of which these have none.
  

**Returns**:

  None while the question is open and the action is the editor's
  own, and True for every other action at every other time.

<a id="edit_cfg_json_textual.textual_editor.EditorApp._out_file_text"></a>

#### \_out\_file\_text

```python
def _out_file_text() -> str
```

Return the file saving would write now, as text to be edited.

<a id="edit_cfg_json_textual.textual_editor.EditorApp._save_to"></a>

#### \_save\_to

```python
def _save_to(chosen: Optional[str]) -> None
```

Write the file that was named, and nothing when none was.

**Arguments**:

- `chosen` - File the user named, or None when the question was left
  unanswered. An empty answer is the same as no answer: there
  is no file whose name is nothing.

<a id="edit_cfg_json_textual.textual_editor.EditorApp._refresh"></a>

#### \_refresh

```python
def _refresh() -> None
```

Write the buffer back into the fields and show the new state.

A pass over the buffer is not read only: a member validator returns
the value that is stored back into the member, so a value can end up
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

Show the title, the verdict, the saving and every member mark.

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

<a id="edit_cfg_json_textual.textual_editor.edit"></a>

#### edit

```python
def edit(config: Config,
         *,
         in_file: Optional[PathOrStr] = None,
         out_file: Optional[PathOrStr] = None,
         policy: LoadPolicy = LoadPolicy.STRICT_THEN_DEFAULTS,
         settings: SettingsSource = Settings(),
         stderr_file: TextIO = sys.stderr) -> Optional[Config]
```

Edit one configuration in the terminal, and return what was saved.

This is `edit_cfg_json.edit` with this package's backend filled in, for
an application that has already chosen Textual. Everything it does is
documented there.

**Arguments**:

- `config` - Configuration object to edit. It is never modified.
- `in_file` - File to read, or None to start from the declared defaults.
- `out_file` - File to write, or None to write the input file.
- `policy` - What to do about declared keys the input file does not hold.
- `settings` - What this application has already decided about key
  combinations and file names, or a callable that answers with it.
- `stderr_file` - Stream used for user-facing diagnostics.
  

**Returns**:

  The configuration object that was written, or None when nothing was.
  

**Raises**:

- `ConfigLoadError` - The input file cannot be opened for editing.

