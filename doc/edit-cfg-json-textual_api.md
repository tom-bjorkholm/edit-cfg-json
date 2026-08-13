# Table of Contents

* [edit\_cfg\_json\_textual.textual\_elements](#edit_cfg_json_textual.textual_elements)
  * [ADD\_ACTION](#edit_cfg_json_textual.textual_elements.ADD_ACTION)
  * [REMOVE\_ACTION](#edit_cfg_json_textual.textual_elements.REMOVE_ACTION)
  * [EARLIER\_ACTION](#edit_cfg_json_textual.textual_elements.EARLIER_ACTION)
  * [LATER\_ACTION](#edit_cfg_json_textual.textual_elements.LATER_ACTION)
  * [ADD\_LABEL](#edit_cfg_json_textual.textual_elements.ADD_LABEL)
  * [REMOVE\_LABEL](#edit_cfg_json_textual.textual_elements.REMOVE_LABEL)
  * [EARLIER\_LABEL](#edit_cfg_json_textual.textual_elements.EARLIER_LABEL)
  * [LATER\_LABEL](#edit_cfg_json_textual.textual_elements.LATER_LABEL)
  * [ELEMENT\_LABELS](#edit_cfg_json_textual.textual_elements.ELEMENT_LABELS)
  * [ASK\_KEY\_ID](#edit_cfg_json_textual.textual_elements.ASK_KEY_ID)
  * [ASK\_KEY\_PROMPT](#edit_cfg_json_textual.textual_elements.ASK_KEY_PROMPT)
  * [ASK\_KEY\_LEAVE](#edit_cfg_json_textual.textual_elements.ASK_KEY_LEAVE)
  * [offered\_actions](#edit_cfg_json_textual.textual_elements.offered_actions)
  * [element\_id](#edit_cfg_json_textual.textual_elements.element_id)
  * [element\_button](#edit_cfg_json_textual.textual_elements.element_button)
* [edit\_cfg\_json\_textual.textual\_ask](#edit_cfg_json_textual.textual_ask)
  * [CANCEL\_COMMAND](#edit_cfg_json_textual.textual_ask.CANCEL_COMMAND)
  * [YES\_ID](#edit_cfg_json_textual.textual_ask.YES_ID)
  * [NO\_ID](#edit_cfg_json_textual.textual_ask.NO_ID)
  * [DISCARD\_LABEL](#edit_cfg_json_textual.textual_ask.DISCARD_LABEL)
  * [KEEP\_LABEL](#edit_cfg_json_textual.textual_ask.KEEP_LABEL)
  * [OVERWRITE\_LABEL](#edit_cfg_json_textual.textual_ask.OVERWRITE_LABEL)
  * [NO\_SAVE\_LABEL](#edit_cfg_json_textual.textual_ask.NO_SAVE_LABEL)
  * [AskScreen](#edit_cfg_json_textual.textual_ask.AskScreen)
    * [DEFAULT\_CSS](#edit_cfg_json_textual.textual_ask.AskScreen.DEFAULT_CSS)
    * [\_\_init\_\_](#edit_cfg_json_textual.textual_ask.AskScreen.__init__)
    * [compose](#edit_cfg_json_textual.textual_ask.AskScreen.compose)
    * [on\_input\_changed](#edit_cfg_json_textual.textual_ask.AskScreen.on_input_changed)
    * [on\_input\_blurred](#edit_cfg_json_textual.textual_ask.AskScreen.on_input_blurred)
    * [on\_input\_submitted](#edit_cfg_json_textual.textual_ask.AskScreen.on_input_submitted)
    * [action\_leave](#edit_cfg_json_textual.textual_ask.AskScreen.action_leave)
  * [ConfirmScreen](#edit_cfg_json_textual.textual_ask.ConfirmScreen)
    * [DEFAULT\_CSS](#edit_cfg_json_textual.textual_ask.ConfirmScreen.DEFAULT_CSS)
    * [AUTO\_FOCUS](#edit_cfg_json_textual.textual_ask.ConfirmScreen.AUTO_FOCUS)
    * [\_\_init\_\_](#edit_cfg_json_textual.textual_ask.ConfirmScreen.__init__)
    * [compose](#edit_cfg_json_textual.textual_ask.ConfirmScreen.compose)
    * [on\_button\_pressed](#edit_cfg_json_textual.textual_ask.ConfirmScreen.on_button_pressed)
    * [action\_leave](#edit_cfg_json_textual.textual_ask.ConfirmScreen.action_leave)
  * [QUESTION\_SCREENS](#edit_cfg_json_textual.textual_ask.QUESTION_SCREENS)
* [edit\_cfg\_json\_textual.textual\_editor](#edit_cfg_json_textual.textual_editor)
  * [QUIT\_ACTION](#edit_cfg_json_textual.textual_editor.QUIT_ACTION)
  * [EditorApp](#edit_cfg_json_textual.textual_editor.EditorApp)
    * [\_\_init\_\_](#edit_cfg_json_textual.textual_editor.EditorApp.__init__)
    * [get\_default\_screen](#edit_cfg_json_textual.textual_editor.EditorApp.get_default_screen)
    * [action\_quit](#edit_cfg_json_textual.textual_editor.EditorApp.action_quit)
    * [check\_action](#edit_cfg_json_textual.textual_editor.EditorApp.check_action)
  * [TextualEditor](#edit_cfg_json_textual.textual_editor.TextualEditor)
    * [run\_editor](#edit_cfg_json_textual.textual_editor.TextualEditor.run_editor)
  * [edit](#edit_cfg_json_textual.textual_editor.edit)
* [edit\_cfg\_json\_textual.textual\_look](#edit_cfg_json_textual.textual_look)
  * [VALUE\_ID\_PREFIX](#edit_cfg_json_textual.textual_look.VALUE_ID_PREFIX)
  * [MARK\_ID\_PREFIX](#edit_cfg_json_textual.textual_look.MARK_ID_PREFIX)
  * [SUBTREE\_ID\_PREFIX](#edit_cfg_json_textual.textual_look.SUBTREE_ID_PREFIX)
  * [DESCRIPTION\_ID\_PREFIX](#edit_cfg_json_textual.textual_look.DESCRIPTION_ID_PREFIX)
  * [DIAGNOSTIC\_ID\_PREFIX](#edit_cfg_json_textual.textual_look.DIAGNOSTIC_ID_PREFIX)
  * [FOLD\_ID\_PREFIX](#edit_cfg_json_textual.textual_look.FOLD_ID_PREFIX)
  * [MEMBER\_ID\_PREFIX](#edit_cfg_json_textual.textual_look.MEMBER_ID_PREFIX)
  * [TITLE\_ID](#edit_cfg_json_textual.textual_look.TITLE_ID)
  * [DOCSTRING\_ID](#edit_cfg_json_textual.textual_look.DOCSTRING_ID)
  * [VERDICT\_ID](#edit_cfg_json_textual.textual_look.VERDICT_ID)
  * [SAVE\_ID](#edit_cfg_json_textual.textual_look.SAVE_ID)
  * [LOAD\_ID](#edit_cfg_json_textual.textual_look.LOAD_ID)
  * [BODY\_ID](#edit_cfg_json_textual.textual_look.BODY_ID)
  * [MEMBERS\_ID](#edit_cfg_json_textual.textual_look.MEMBERS_ID)
  * [SAVE\_AS\_ID](#edit_cfg_json_textual.textual_look.SAVE_AS_ID)
  * [ASK\_BOX\_ID](#edit_cfg_json_textual.textual_look.ASK_BOX_ID)
  * [NAME\_CLASS](#edit_cfg_json_textual.textual_look.NAME_CLASS)
  * [VALUE\_CLASS](#edit_cfg_json_textual.textual_look.VALUE_CLASS)
  * [MARK\_CLASS](#edit_cfg_json_textual.textual_look.MARK_CLASS)
  * [SUBTREE\_CLASS](#edit_cfg_json_textual.textual_look.SUBTREE_CLASS)
  * [ROW\_CLASS](#edit_cfg_json_textual.textual_look.ROW_CLASS)
  * [MEMBER\_CLASS](#edit_cfg_json_textual.textual_look.MEMBER_CLASS)
  * [DESCRIPTION\_CLASS](#edit_cfg_json_textual.textual_look.DESCRIPTION_CLASS)
  * [DIAGNOSTIC\_CLASS](#edit_cfg_json_textual.textual_look.DIAGNOSTIC_CLASS)
  * [FOLD\_CLASS](#edit_cfg_json_textual.textual_look.FOLD_CLASS)
  * [ELEMENT\_CLASS](#edit_cfg_json_textual.textual_look.ELEMENT_CLASS)
  * [TYPE\_MARK](#edit_cfg_json_textual.textual_look.TYPE_MARK)
  * [ANSWER\_CLASS](#edit_cfg_json_textual.textual_look.ANSWER_CLASS)
  * [NAME\_WIDTH](#edit_cfg_json_textual.textual_look.NAME_WIDTH)
  * [FOLD\_WIDTH](#edit_cfg_json_textual.textual_look.FOLD_WIDTH)
  * [TREE\_INDENT](#edit_cfg_json_textual.textual_look.TREE_INDENT)
  * [DESCRIPTION\_INDENT](#edit_cfg_json_textual.textual_look.DESCRIPTION_INDENT)
  * [LEAST\_VALUE\_WIDTH](#edit_cfg_json_textual.textual_look.LEAST_VALUE_WIDTH)
  * [FOLD\_SHUT\_TEXT](#edit_cfg_json_textual.textual_look.FOLD_SHUT_TEXT)
  * [FOLD\_OPEN\_TEXT](#edit_cfg_json_textual.textual_look.FOLD_OPEN_TEXT)
  * [EMPHASIS\_CLASSES](#edit_cfg_json_textual.textual_look.EMPHASIS_CLASSES)
  * [COLOUR\_RULES](#edit_cfg_json_textual.textual_look.COLOUR_RULES)
  * [PANEL\_CSS](#edit_cfg_json_textual.textual_look.PANEL_CSS)
  * [QUESTION\_CSS](#edit_cfg_json_textual.textual_look.QUESTION_CSS)
  * [value\_id](#edit_cfg_json_textual.textual_look.value_id)
  * [mark\_id](#edit_cfg_json_textual.textual_look.mark_id)
  * [subtree\_id](#edit_cfg_json_textual.textual_look.subtree_id)
  * [description\_id](#edit_cfg_json_textual.textual_look.description_id)
  * [diagnostic\_id](#edit_cfg_json_textual.textual_look.diagnostic_id)
  * [fold\_id](#edit_cfg_json_textual.textual_look.fold_id)
  * [member\_id](#edit_cfg_json_textual.textual_look.member_id)
  * [fold\_glyph](#edit_cfg_json_textual.textual_look.fold_glyph)
  * [plain\_widget](#edit_cfg_json_textual.textual_look.plain_widget)
  * [show\_emphasis](#edit_cfg_json_textual.textual_look.show_emphasis)
  * [bind\_action](#edit_cfg_json_textual.textual_look.bind_action)
* [edit\_cfg\_json\_textual.textual\_screen](#edit_cfg_json_textual.textual_screen)
  * [EditorCommands](#edit_cfg_json_textual.textual_screen.EditorCommands)
    * [discover](#edit_cfg_json_textual.textual_screen.EditorCommands.discover)
    * [search](#edit_cfg_json_textual.textual_screen.EditorCommands.search)
  * [EditorScreen](#edit_cfg_json_textual.textual_screen.EditorScreen)
    * [COMMANDS](#edit_cfg_json_textual.textual_screen.EditorScreen.COMMANDS)
    * [\_\_init\_\_](#edit_cfg_json_textual.textual_screen.EditorScreen.__init__)
    * [panel](#edit_cfg_json_textual.textual_screen.EditorScreen.panel)
    * [compose](#edit_cfg_json_textual.textual_screen.EditorScreen.compose)
* [edit\_cfg\_json\_textual.textual\_panel](#edit_cfg_json_textual.textual_panel)
  * [CLOSE\_COMMAND](#edit_cfg_json_textual.textual_panel.CLOSE_COMMAND)
  * [VALIDATE\_COMMAND](#edit_cfg_json_textual.textual_panel.VALIDATE_COMMAND)
  * [SAVE\_COMMAND](#edit_cfg_json_textual.textual_panel.SAVE_COMMAND)
  * [SAVE\_AS\_COMMAND](#edit_cfg_json_textual.textual_panel.SAVE_AS_COMMAND)
  * [EXPLAIN\_COMMAND](#edit_cfg_json_textual.textual_panel.EXPLAIN_COMMAND)
  * [HIDE\_COMMAND](#edit_cfg_json_textual.textual_panel.HIDE_COMMAND)
  * [VALIDATE\_HELP](#edit_cfg_json_textual.textual_panel.VALIDATE_HELP)
  * [SAVE\_HELP](#edit_cfg_json_textual.textual_panel.SAVE_HELP)
  * [SAVE\_AS\_HELP](#edit_cfg_json_textual.textual_panel.SAVE_AS_HELP)
  * [EXPLAIN\_HELP](#edit_cfg_json_textual.textual_panel.EXPLAIN_HELP)
  * [FOLD\_COMMAND](#edit_cfg_json_textual.textual_panel.FOLD_COMMAND)
  * [OPEN\_COMMAND](#edit_cfg_json_textual.textual_panel.OPEN_COMMAND)
  * [FOLD\_HELP](#edit_cfg_json_textual.textual_panel.FOLD_HELP)
  * [SAVE\_AS\_PROMPT](#edit_cfg_json_textual.textual_panel.SAVE_AS_PROMPT)
  * [SAVE\_AS\_LEAVE](#edit_cfg_json_textual.textual_panel.SAVE_AS_LEAVE)
  * [EDITOR\_ACTIONS](#edit_cfg_json_textual.textual_panel.EDITOR_ACTIONS)
  * [EditorCommand](#edit_cfg_json_textual.textual_panel.EditorCommand)
    * [name](#edit_cfg_json_textual.textual_panel.EditorCommand.name)
    * [help\_text](#edit_cfg_json_textual.textual_panel.EditorCommand.help_text)
    * [run](#edit_cfg_json_textual.textual_panel.EditorCommand.run)
  * [EditorPanel](#edit_cfg_json_textual.textual_panel.EditorPanel)
    * [DEFAULT\_CSS](#edit_cfg_json_textual.textual_panel.EditorPanel.DEFAULT_CSS)
    * [\_\_init\_\_](#edit_cfg_json_textual.textual_panel.EditorPanel.__init__)
    * [compose](#edit_cfg_json_textual.textual_panel.EditorPanel.compose)
    * [command\_entries](#edit_cfg_json_textual.textual_panel.EditorPanel.command_entries)
    * [on\_input\_changed](#edit_cfg_json_textual.textual_panel.EditorPanel.on_input_changed)
    * [on\_input\_blurred](#edit_cfg_json_textual.textual_panel.EditorPanel.on_input_blurred)
    * [action\_close](#edit_cfg_json_textual.textual_panel.EditorPanel.action_close)
    * [close](#edit_cfg_json_textual.textual_panel.EditorPanel.close)
    * [action\_validate](#edit_cfg_json_textual.textual_panel.EditorPanel.action_validate)
    * [action\_save](#edit_cfg_json_textual.textual_panel.EditorPanel.action_save)
    * [action\_explain](#edit_cfg_json_textual.textual_panel.EditorPanel.action_explain)
    * [action\_fold](#edit_cfg_json_textual.textual_panel.EditorPanel.action_fold)
    * [on\_button\_pressed](#edit_cfg_json_textual.textual_panel.EditorPanel.on_button_pressed)
    * [action\_save\_as](#edit_cfg_json_textual.textual_panel.EditorPanel.action_save_as)
    * [check\_action](#edit_cfg_json_textual.textual_panel.EditorPanel.check_action)

<a id="edit_cfg_json_textual.textual_elements"></a>

# edit\_cfg\_json\_textual.textual\_elements

The Textual controls that change how many elements a node holds.

They are here rather than in the module that builds the screen for the reason
every other split of this backend was made: one module of a thousand lines is
one nobody reads to the end. What is here is one row's worth of controls, the
identifiers that let a press be traced back to the node it was made on, and
the words of the one question this backend has to ask about them.

Nothing here decides *whether* a node offers anything. That is
`edit_cfg_json.MemberRow.offer`, which the core works out once so that the two
backends cannot offer different things.

<a id="edit_cfg_json_textual.textual_elements.ADD_ACTION"></a>

#### ADD\_ACTION

Name of the action that puts one more element into a node.

<a id="edit_cfg_json_textual.textual_elements.REMOVE_ACTION"></a>

#### REMOVE\_ACTION

Name of the action that takes one element out of what holds it.

<a id="edit_cfg_json_textual.textual_elements.EARLIER_ACTION"></a>

#### EARLIER\_ACTION

Name of the action that moves one element towards the front.

<a id="edit_cfg_json_textual.textual_elements.LATER_ACTION"></a>

#### LATER\_ACTION

Name of the action that moves one element towards the back.

<a id="edit_cfg_json_textual.textual_elements.ADD_LABEL"></a>

#### ADD\_LABEL

Label of the control that puts one more element into a node.

It is a word and not the `+` of the fold control beside it, because the two do
different things and one row can have both: a list of configuration objects
folds away and grows, and two controls saying `+` on one line would be two
offers that could not be told apart.

<a id="edit_cfg_json_textual.textual_elements.REMOVE_LABEL"></a>

#### REMOVE\_LABEL

Label of the control that takes one element out of what holds it.

<a id="edit_cfg_json_textual.textual_elements.EARLIER_LABEL"></a>

#### EARLIER\_LABEL

Label of the control that moves one element towards the front.

<a id="edit_cfg_json_textual.textual_elements.LATER_LABEL"></a>

#### LATER\_LABEL

Label of the control that moves one element towards the back.

<a id="edit_cfg_json_textual.textual_elements.ELEMENT_LABELS"></a>

#### ELEMENT\_LABELS

What the control of each action says on it.

<a id="edit_cfg_json_textual.textual_elements.ASK_KEY_ID"></a>

#### ASK\_KEY\_ID

Identifier of the field that a new entry of a dict is named in.

<a id="edit_cfg_json_textual.textual_elements.ASK_KEY_PROMPT"></a>

#### ASK\_KEY\_PROMPT

What the screen that asks for a new key says.

<a id="edit_cfg_json_textual.textual_elements.ASK_KEY_LEAVE"></a>

#### ASK\_KEY\_LEAVE

What that screen says while there is a key that leaves it.

The key is named from the settings and not written into the sentence, for the
same reason the question about the output file names it: an application that
took `escape` for itself would otherwise be telling its users to press a key
that does nothing.

<a id="edit_cfg_json_textual.textual_elements.offered_actions"></a>

#### offered\_actions

```python
def offered_actions(row: core.MemberRow) -> tuple[str, ...]
```

Return the actions that one node offers about its elements.

**Arguments**:

- `row` - Node to ask about.
  

**Returns**:

  The name of each action that node offers, in the order the controls
  are shown, and nothing at all for a node that offers none, which is
  most nodes of most configurations.

<a id="edit_cfg_json_textual.textual_elements.element_id"></a>

#### element\_id

```python
def element_id(index: int, action: str) -> str
```

Return the identifier of one control of one node.

**Arguments**:

- `index` - Place of the node among the rows, which every widget of a node
  is identified by: two values inside two different dicts can have
  one name, and a dictionary key holds whatever a dictionary key
  holds, which Textual does not always accept as an identifier.
- `action` - Name of the action that control runs.
  

**Returns**:

  The identifier that press is found by.

<a id="edit_cfg_json_textual.textual_elements.element_button"></a>

#### element\_button

```python
def element_button(widget_id: str, action: str) -> Button
```

Return one control that changes how many elements there are.

**Arguments**:

- `widget_id` - Identifier the application finds this control by.
- `action` - Name of the action it runs.
  

**Returns**:

  A control that says what it does.

<a id="edit_cfg_json_textual.textual_ask"></a>

# edit\_cfg\_json\_textual.textual\_ask

The screens this backend asks the user a question on.

There are two shapes of question. One is answered with text — which file to
write, and what a new entry of a dict is to be called — and one is answered
yes or no, which is whether an existing file may be overwritten and whether
the changes that have not been saved may be dropped. Each shape is one screen
serving every question of that shape, because two screens differing in a
prompt would be the same code twice and the questions would then be free to
drift apart in how they behave.

A question is a screen of its own rather than a field or a row in the editor,
because it is asked, answered and gone: something that was always there would
be one more thing to read in every session, for a question that is asked once
or never.

Neither screen decides *whether* it is asked. Which file to write is what a
backend is asked for when the model has no destination, what a new entry is
called is asked where `edit_cfg_json.MemberRow.offer` says a key is needed,
whether a file may be overwritten is `edit_cfg_json.overwrite_question`, and
whether there is anything to lose by closing is
`edit_cfg_json.close_question`. All four are the core's, so that the two
backends cannot ask one user something and another user nothing.

<a id="edit_cfg_json_textual.textual_ask.CANCEL_COMMAND"></a>

#### CANCEL\_COMMAND

Name of the action that leaves a question of the editor unanswered.

<a id="edit_cfg_json_textual.textual_ask.YES_ID"></a>

#### YES\_ID

Identifier of the control that answers a question with yes.

<a id="edit_cfg_json_textual.textual_ask.NO_ID"></a>

#### NO\_ID

Identifier of the control that answers it with no.

<a id="edit_cfg_json_textual.textual_ask.DISCARD_LABEL"></a>

#### DISCARD\_LABEL

Label of the control that drops the changes and closes the editor.

<a id="edit_cfg_json_textual.textual_ask.KEEP_LABEL"></a>

#### KEEP\_LABEL

Label of the control that leaves the editor as it was.

It says what happens next rather than answering the question with a word, in
the same way as the actions this backend renames: a control saying No beside a
question about closing leaves the user working out what No was about.

<a id="edit_cfg_json_textual.textual_ask.OVERWRITE_LABEL"></a>

#### OVERWRITE\_LABEL

Label of the control that writes over the file that is there.

<a id="edit_cfg_json_textual.textual_ask.NO_SAVE_LABEL"></a>

#### NO\_SAVE\_LABEL

Label of the control that leaves that file exactly as it is.

It says what happens next for the same reason the one above it does: what No
means here is that nothing is written, and a user reading a control should not
have to work that out from the question.

<a id="edit_cfg_json_textual.textual_ask.AskScreen"></a>

## AskScreen Objects

```python
class AskScreen(ModalScreen[Optional[str]])
```

Ask one question, and give back None when it is left unanswered.

<a id="edit_cfg_json_textual.textual_ask.AskScreen.DEFAULT_CSS"></a>

#### DEFAULT\_CSS

How this screen is laid out. See `QUESTION_CSS`.

It is declared on the screen rather than on the application, because the
application may be one that mounted this editor in a window of its own and
would then have no style sheet of this editor's at all. The name of the
class is written into it, because a widget styles itself by its type name.

<a id="edit_cfg_json_textual.textual_ask.AskScreen.__init__"></a>

#### \_\_init\_\_

```python
def __init__(prompt: str,
             field_id: str,
             cancel_keys: Sequence[str],
             answer: str = '') -> None
```

Ask the question, with the field holding what it starts from.

The keys that leave the question are bound here rather than declared
as a class variable, because which keys they are is the application's
decision and not this screen's.

**Arguments**:

- `prompt` - What this screen asks, as the user reads it.
- `field_id` - Identifier that the field is found by, which is what
  lets a test and a caller reach the one that is being asked.
- `cancel_keys` - Key combinations that leave the question unanswered,
  empty when the application gave it none.
- `answer` - What the field starts out holding, which is what makes
  changing an answer a matter of changing a few characters.

<a id="edit_cfg_json_textual.textual_ask.AskScreen.compose"></a>

#### compose

```python
def compose() -> ComposeResult
```

Create the question and the field that answers it.

<a id="edit_cfg_json_textual.textual_ask.AskScreen.on_input_changed"></a>

#### on\_input\_changed

```python
def on_input_changed(event: Input.Changed) -> None
```

Keep what happens in this field to this screen.

The editor underneath writes every field change into the model, and
this field is not a member of the configuration: it is the name of a
file or of a new entry. A message that reached the editor would be
looked for among the members and found nowhere.

<a id="edit_cfg_json_textual.textual_ask.AskScreen.on_input_blurred"></a>

#### on\_input\_blurred

```python
def on_input_blurred(event: Input.Blurred) -> None
```

Keep leaving this field to this screen, for the same reason.

The editor underneath asks the model about the member whose field was
left, and neither of these fields is a member of the configuration.

<a id="edit_cfg_json_textual.textual_ask.AskScreen.on_input_submitted"></a>

#### on\_input\_submitted

```python
def on_input_submitted(event: Input.Submitted) -> None
```

Give back what was typed, and leave the screen.

<a id="edit_cfg_json_textual.textual_ask.AskScreen.action_leave"></a>

#### action\_leave

```python
def action_leave() -> None
```

Leave the screen without answering the question.

<a id="edit_cfg_json_textual.textual_ask.ConfirmScreen"></a>

## ConfirmScreen Objects

```python
class ConfirmScreen(ModalScreen[bool])
```

Ask one question that is answered by one of two controls.

It is a screen and not a field, exactly as the question above it is, and
it is answered with controls rather than with text because what the user
is being asked for is a decision and not a value.

One screen serves every question of this shape, and each of them says what
its own two answers do: what the user is agreeing to is different for a
question about the changes in the buffer and one about the file on disk,
and Yes beside either of them would be a word to work out rather than read.

<a id="edit_cfg_json_textual.textual_ask.ConfirmScreen.DEFAULT_CSS"></a>

#### DEFAULT\_CSS

How this screen is laid out, which is how the one above it is.

<a id="edit_cfg_json_textual.textual_ask.ConfirmScreen.AUTO_FOCUS"></a>

#### AUTO\_FOCUS

The control that the screen opens with, which is the safe one.

A screen that opened on the control which loses something would lose it
for a user who pressed Enter without reading, and the whole reason for
asking is that what is lost cannot be got back. The Tk backend opens its
dialog on the same answer and for the same reason.

<a id="edit_cfg_json_textual.textual_ask.ConfirmScreen.__init__"></a>

#### \_\_init\_\_

```python
def __init__(question: str, cancel_keys: Sequence[str], yes_text: str,
             no_text: str) -> None
```

Ask the question, with the keys that leave it unanswered.

**Arguments**:

- `question` - What this screen asks, as the user reads it.
- `cancel_keys` - Key combinations that leave the question unanswered,
  which is the same as answering it with no, empty when the
  application gave it none.
- `yes_text` - What the control that agrees to the question does.
- `no_text` - What the control that leaves everything as it is does.

<a id="edit_cfg_json_textual.textual_ask.ConfirmScreen.compose"></a>

#### compose

```python
def compose() -> ComposeResult
```

Create the question and the two controls that answer it.

<a id="edit_cfg_json_textual.textual_ask.ConfirmScreen.on_button_pressed"></a>

#### on\_button\_pressed

```python
def on_button_pressed(event: Button.Pressed) -> None
```

Give back what was pressed, and leave the screen.

The message is stopped here because the editor underneath reads every
press for a control of a row, and neither of these is one.

<a id="edit_cfg_json_textual.textual_ask.ConfirmScreen.action_leave"></a>

#### action\_leave

```python
def action_leave() -> None
```

Leave the screen, which is the same as changing nothing.

<a id="edit_cfg_json_textual.textual_ask.QUESTION_SCREENS"></a>

#### QUESTION\_SCREENS

The screens on which this backend asks the user something.

The editor turns its own actions off while one of them is up, because Textual
offers an application's priority bindings the key from the whole binding chain
rather than from the part of it above the last modal screen. What makes a
question modal is therefore the editor answering for its own actions, and this
is what it asks about.

<a id="edit_cfg_json_textual.textual_editor"></a>

# edit\_cfg\_json\_textual.textual\_editor

The editor of this package as a Textual application of its own.

It is the shortest of the three modules that make up this backend, and that is
the point of the split: `textual_panel` holds the whole editor, and
`textual_screen` gives it a header, a footer and a command palette. What is
left here is the one thing only an application may do, which is to own the
terminal and to end the process.

Everything this backend takes from the core is reached through `core`, which is
`edit_cfg_json` itself. A backend may use the public API of the core and
nothing else, and naming it at every call site is what makes that visible; it
also keeps the two backends from each holding the same block of twenty
imported names, which is a duplication with nothing to factor out, since
neither backend may import the other.

<a id="edit_cfg_json_textual.textual_editor.QUIT_ACTION"></a>

#### QUIT\_ACTION

Name of the action of Textual itself that would end the application.

The editor answers for it as well as for its own, because the command palette
of Textual offers it and a way out that dropped the changes without a word
would be the one thing an editor must not do.

<a id="edit_cfg_json_textual.textual_editor.EditorApp"></a>

## EditorApp Objects

```python
class EditorApp(App[None])
```

Textual application that edits one edit model and nothing else.

<a id="edit_cfg_json_textual.textual_editor.EditorApp.__init__"></a>

#### \_\_init\_\_

```python
def __init__(model: core.EditModel) -> None
```

Remember the model and name the terminal after its class.

The title is the name of the class and not the label of the model,
because the label says whether there is something unsaved and belongs
beside the values that are unsaved. The Tk backend names its window
the same way and for the same reason.

**Arguments**:

- `model` - Model to show and to edit.

<a id="edit_cfg_json_textual.textual_editor.EditorApp.get_default_screen"></a>

#### get\_default\_screen

```python
def get_default_screen() -> Screen[None]
```

Return the screen this application shows, which holds the editor.

**Returns**:

  One editor on a screen of its own, which ends this application
  when the session ends: there is nothing else for the application
  to show, so an editor that had gone would leave an empty terminal.

<a id="edit_cfg_json_textual.textual_editor.EditorApp.action_quit"></a>

#### action\_quit

```python
async def action_quit() -> None
```

End the session, asking first where there is something to lose.

This is the action of Textual itself, which its command palette offers
and which the editor would otherwise have no say in. It is the Close
of the editor, so that every way out of this application asks the one
question in the one place.

<a id="edit_cfg_json_textual.textual_editor.EditorApp.check_action"></a>

#### check\_action

```python
def check_action(action: str, parameters: tuple[object,
                                                ...]) -> Optional[bool]
```

Turn ending the application off while the editor asks something.

The editor answers the same way for its own actions, and for the same
reason: a priority binding is offered the key from the whole binding
chain and not from the part of it above the last modal screen, so a
question is only really modal if what is under it says so.

**Arguments**:

- `action` - Name of the action that is about to run.
- `parameters` - Arguments of that action, of which this has none.
  

**Returns**:

  None while a question of the editor is open and the action is the
  one that would end the application, and True otherwise.

<a id="edit_cfg_json_textual.textual_editor.TextualEditor"></a>

## TextualEditor Objects

```python
class TextualEditor()
```

Textual user interface backend for an edit model.

The class has the single method that `EditorBackend` asks for, and
deliberately nothing else: everything worth testing without a terminal
lives in the core.

It runs an application of its own, which is what that protocol promises
and what an application that already runs Textual cannot use.
`edit_cfg_json_textual.EditorPanel` and
`edit_cfg_json_textual.EditorScreen` are for that one instead.

<a id="edit_cfg_json_textual.textual_editor.TextualEditor.run_editor"></a>

#### run\_editor

```python
def run_editor(model: core.EditModel) -> None
```

Show the model in a Textual screen until the user quits.

**Arguments**:

- `model` - Model to show and to edit.

<a id="edit_cfg_json_textual.textual_editor.edit"></a>

#### edit

```python
def edit(config: Config,
         *,
         descriptions: Optional[core.Descriptions] = None,
         in_file: Optional[PathOrStr] = None,
         loader: Optional[core.ConfigLoader] = None,
         out_file: Optional[PathOrStr] = None,
         policy: core.LoadPolicy = core.LoadPolicy.STRICT_THEN_DEFAULTS,
         settings: core.SettingsSource = core.Settings(),
         stderr_file: TextIO = sys.stderr) -> Optional[Config]
```

Edit one configuration in the terminal, and return what was saved.

This is `edit_cfg_json.edit` with this package's backend filled in, for
an application that has already chosen Textual. Everything it does is
documented there.

**Arguments**:

- `config` - Configuration object to edit. It is never modified.
- `descriptions` - What the application says about the members it
  declares, or None when it says nothing.
- `in_file` - File to read, or None to start from the declared defaults.
- `loader` - How this application constructs its configuration, or None for
  a class the editor can construct on its own.
- `out_file` - File to write, or None to write the input file.
- `policy` - What to do about declared keys the input file does not hold.
- `settings` - What this application has already decided about key
  combinations and file names, or a callable that answers with it.
- `stderr_file` - Stream used for user-facing diagnostics.
  

**Returns**:

  The configuration object that was written, or None when nothing was.
  

**Raises**:

- `ConfigLoadError` - The input file cannot be opened for editing.

<a id="edit_cfg_json_textual.textual_look"></a>

# edit\_cfg\_json\_textual.textual\_look

How the Textual backend names, styles and identifies its widgets.

The identifiers, the style classes, the sizes, the style sheet and the colours
of this backend are here rather than in the modules that build the screen,
because they are what one has to look at to know how the editor will look.
Nothing here knows what an edit model is beyond the row it is given, and
nothing here imports another module of this backend, so everything that builds
a widget can read its own identifier and its own style class from here.

What each kind of text is stays in the core, as `edit_cfg_json.Emphasis`, and
what a kind looks like belongs here: a colour of the terminal's own theme, so
that the editor follows it into a light or a dark mode instead of naming
colours of its own.

<a id="edit_cfg_json_textual.textual_look.VALUE_ID_PREFIX"></a>

#### VALUE\_ID\_PREFIX

Prefix of the identifier of the widget that shows one node value.

Every identifier of a node is that prefix and the place of the node among the
rows, and not the name of the node: two values inside two different dicts can
have one name, and a path holds whatever a dictionary key holds, which is not
always something Textual accepts as an identifier.

<a id="edit_cfg_json_textual.textual_look.MARK_ID_PREFIX"></a>

#### MARK\_ID\_PREFIX

Prefix of the identifier of the widget that marks one node.

<a id="edit_cfg_json_textual.textual_look.SUBTREE_ID_PREFIX"></a>

#### SUBTREE\_ID\_PREFIX

Prefix of the identifier of the widget that says what one object is.

<a id="edit_cfg_json_textual.textual_look.DESCRIPTION_ID_PREFIX"></a>

#### DESCRIPTION\_ID\_PREFIX

Prefix of the identifier of the widget that describes one node.

<a id="edit_cfg_json_textual.textual_look.DIAGNOSTIC_ID_PREFIX"></a>

#### DIAGNOSTIC\_ID\_PREFIX

Prefix of the identifier of the widget that refuses one node.

<a id="edit_cfg_json_textual.textual_look.FOLD_ID_PREFIX"></a>

#### FOLD\_ID\_PREFIX

Prefix of the identifier of the control that folds one container.

<a id="edit_cfg_json_textual.textual_look.MEMBER_ID_PREFIX"></a>

#### MEMBER\_ID\_PREFIX

Prefix of the identifier of everything that one node owns.

<a id="edit_cfg_json_textual.textual_look.TITLE_ID"></a>

#### TITLE\_ID

Identifier of the widget that names the configuration being edited.

It is a widget of the editor and not the title of an application, because an
editor mounted in a window an application owns has no business writing there.
The Tk backend has always had it as a label of its own, and this is the same
label.

<a id="edit_cfg_json_textual.textual_look.DOCSTRING_ID"></a>

#### DOCSTRING\_ID

Identifier of the widget that shows what the configuration class says.

<a id="edit_cfg_json_textual.textual_look.VERDICT_ID"></a>

#### VERDICT\_ID

Identifier of the widget that shows what validation found.

<a id="edit_cfg_json_textual.textual_look.SAVE_ID"></a>

#### SAVE\_ID

Identifier of the widget that shows what saving did or would do.

<a id="edit_cfg_json_textual.textual_look.LOAD_ID"></a>

#### LOAD\_ID

Identifier of the widget that shows what reading the file did.

<a id="edit_cfg_json_textual.textual_look.BODY_ID"></a>

#### BODY\_ID

Identifier of the part of the screen that scrolls.

<a id="edit_cfg_json_textual.textual_look.MEMBERS_ID"></a>

#### MEMBERS\_ID

Identifier of the part of the body that holds the nodes.

They have a container of their own inside the part that scrolls, because a
validation pass can leave the model with other rows than it had and they are
then mounted afresh. What is above them is not, so it is not in here.

<a id="edit_cfg_json_textual.textual_look.SAVE_AS_ID"></a>

#### SAVE\_AS\_ID

Identifier of the field that the file to write is typed into.

<a id="edit_cfg_json_textual.textual_look.ASK_BOX_ID"></a>

#### ASK\_BOX\_ID

Identifier of the box that holds one question and its answer.

<a id="edit_cfg_json_textual.textual_look.NAME_CLASS"></a>

#### NAME\_CLASS

Style class of the widget that shows one member name.

<a id="edit_cfg_json_textual.textual_look.VALUE_CLASS"></a>

#### VALUE\_CLASS

Style class of the widget that shows or edits one member value.

<a id="edit_cfg_json_textual.textual_look.MARK_CLASS"></a>

#### MARK\_CLASS

Style class of the widget that marks one member.

<a id="edit_cfg_json_textual.textual_look.SUBTREE_CLASS"></a>

#### SUBTREE\_CLASS

Style class of the widget that says what one object is on its own.

<a id="edit_cfg_json_textual.textual_look.ROW_CLASS"></a>

#### ROW\_CLASS

Style class of the container that holds the widgets of one member.

<a id="edit_cfg_json_textual.textual_look.MEMBER_CLASS"></a>

#### MEMBER\_CLASS

Style class of the container that holds one member and its description.

<a id="edit_cfg_json_textual.textual_look.DESCRIPTION_CLASS"></a>

#### DESCRIPTION\_CLASS

Style class of the widget that says what one member is for.

<a id="edit_cfg_json_textual.textual_look.DIAGNOSTIC_CLASS"></a>

#### DIAGNOSTIC\_CLASS

Style class of the widget that says what is wrong with one member.

<a id="edit_cfg_json_textual.textual_look.FOLD_CLASS"></a>

#### FOLD\_CLASS

Style class of the control that folds one container.

<a id="edit_cfg_json_textual.textual_look.ELEMENT_CLASS"></a>

#### ELEMENT\_CLASS

Style class of a control that changes how many elements there are.

<a id="edit_cfg_json_textual.textual_look.TYPE_MARK"></a>

#### TYPE\_MARK

Where a widget of this backend writes its own class name.

A widget styles *itself* by its type name and not by a style class of its own:
Textual scopes the sheet a widget declares to that widget and what is inside
it, so a class selector reaches the inside and never the widget the sheet
belongs to. Each sheet below therefore leaves this where its own name belongs
and the widget puts its name there, which is what `ModalScreen` above the
question screens does with its own name too.

<a id="edit_cfg_json_textual.textual_look.ANSWER_CLASS"></a>

#### ANSWER\_CLASS

Style class of the row of controls that answers a question.

<a id="edit_cfg_json_textual.textual_look.NAME_WIDTH"></a>

#### NAME\_WIDTH

Width in cells of the column that holds the member names.

<a id="edit_cfg_json_textual.textual_look.FOLD_WIDTH"></a>

#### FOLD\_WIDTH

Width in cells of the control that folds one container.

Every row has one that wide, and the rows that hold nothing to fold have an
empty one, so that the names of a container and of a value beside it line up.

<a id="edit_cfg_json_textual.textual_look.TREE_INDENT"></a>

#### TREE\_INDENT

Indentation in cells of each step inside a list or a dict.

The whole node is indented and not only its name, so that a name inside a
container is never cut off by the column that the names share. What that costs
is a value column that steps to the right with the tree, which is what a tree
looks like. The Tk backend indents by the same amount and for the same reason.

<a id="edit_cfg_json_textual.textual_look.DESCRIPTION_INDENT"></a>

#### DESCRIPTION\_INDENT

Indentation in cells of the description of one member.

The indentation is what says that the line belongs to the member above it
rather than being a member of its own.

<a id="edit_cfg_json_textual.textual_look.LEAST_VALUE_WIDTH"></a>

#### LEAST\_VALUE\_WIDTH

Smallest width in cells that the value of a member is given.

A row that does not fit the terminal has to give way somewhere, and it is
the marks that are cut rather than the field: the field is what the user
edits, and `model_as_text` shows every mark in full whatever the terminal.

<a id="edit_cfg_json_textual.textual_look.FOLD_SHUT_TEXT"></a>

#### FOLD\_SHUT\_TEXT

Label of the control of a container that is folded away.

<a id="edit_cfg_json_textual.textual_look.FOLD_OPEN_TEXT"></a>

#### FOLD\_OPEN\_TEXT

Label of the control of a container that is open.

The two are what a tree has always used for this, and they are one cell wide
in every terminal, which the arrows that a modern tree draws are not.

<a id="edit_cfg_json_textual.textual_look.EMPHASIS_CLASSES"></a>

#### EMPHASIS\_CLASSES

The style class of every reason the core has to show something differently.

One class per member of `edit_cfg_json.Emphasis`, and the style sheet gives
each of them a theme colour, so that the editor follows the terminal into its
light or dark mode instead of naming colours of its own. What each kind of
text is comes from the core, so the two backends cannot colour one thing two
ways.

<a id="edit_cfg_json_textual.textual_look.COLOUR_RULES"></a>

#### COLOUR\_RULES

What each reason to stand out looks like, as a colour of the theme.

Theme colours and not colours of this backend's own: they are what follows the
terminal into its light or dark mode, and an editor that named colours itself
would be legible in one of the two and a guess in the other.

The values and their names are left alone, so the thing the user came to edit
is the most legible thing on the screen. Everything else is either secondary
text or a state to act on, which is what `edit_cfg_json.Emphasis` names.

<a id="edit_cfg_json_textual.textual_look.PANEL_CSS"></a>

#### PANEL\_CSS

The width and the height of every part of one member row.

Rows are one cell high, so that the footer stays visible below them. A field
is one cell high as well, which needs its border and its padding taken away,
because both of them are part of how tall a field is.

A member is as high as it needs to be rather than one cell, because it is the
row and the description below it, and the explanatory text is as high as the
lines it takes: a container of Textual's own accord takes an equal share of
the height it is given, which would leave two members holding half a screen
each.

The body takes whatever height is left over, which is what makes it the part
that scrolls: a configuration of any size fits a terminal of any size, and the
verdict, the saving and the footer stay where the user left them, because they
are what a user reaches for after editing rather than something to scroll to.

The widths are the part that has to be said rather than left to Textual. A
`Input` is a full width widget of its own accord, so it would take the whole
line and lay the marks of the member out beyond the right edge of the screen,
where they are there and cannot be seen. The value therefore takes what is
left over and the marks take what they need, which is the opposite way round
from the default and the only way round that shows both.

It is the style sheet of the widget that holds the editor and not of an
application, because an application that mounts that widget in a window of its
own has a style sheet of its own and would not have this one. Textual scopes
the rules a widget declares to that widget and what is inside it, which is
what keeps a rule of this editor from reaching a widget of the application.

<a id="edit_cfg_json_textual.textual_look.QUESTION_CSS"></a>

#### QUESTION\_CSS

How a screen that asks the user a question is laid out.

Each of those screens fills `TYPE_MARK` in with its own class name before
this becomes its style sheet.

It sits in the middle of the screen and takes most of its width, so that a
long path or a long file name is still readable in a narrow terminal. Its own
field is untouched by the rule about the fields of a member row, which reaches
only inside the widget that holds the editor, and the controls that answer it
take the width they need rather than a share of the box.

It is apart from the rules above because a question of this editor is a screen
of the application and never a part of the editor widget, so the two are
declared on different widgets and neither style sheet can reach the other.

<a id="edit_cfg_json_textual.textual_look.value_id"></a>

#### value\_id

```python
def value_id(index: int) -> str
```

Return the identifier of the widget that shows one node value.

<a id="edit_cfg_json_textual.textual_look.mark_id"></a>

#### mark\_id

```python
def mark_id(index: int) -> str
```

Return the identifier of the widget that marks one node.

<a id="edit_cfg_json_textual.textual_look.subtree_id"></a>

#### subtree\_id

```python
def subtree_id(index: int) -> str
```

Return the identifier of the widget that says what one object is.

<a id="edit_cfg_json_textual.textual_look.description_id"></a>

#### description\_id

```python
def description_id(index: int) -> str
```

Return the identifier of the widget that describes one node.

<a id="edit_cfg_json_textual.textual_look.diagnostic_id"></a>

#### diagnostic\_id

```python
def diagnostic_id(index: int) -> str
```

Return the identifier of the widget that refuses one node.

<a id="edit_cfg_json_textual.textual_look.fold_id"></a>

#### fold\_id

```python
def fold_id(index: int) -> str
```

Return the identifier of the control that folds one container.

<a id="edit_cfg_json_textual.textual_look.member_id"></a>

#### member\_id

```python
def member_id(index: int) -> str
```

Return the identifier of everything that one node owns.

<a id="edit_cfg_json_textual.textual_look.fold_glyph"></a>

#### fold\_glyph

```python
def fold_glyph(row: core.MemberRow) -> str
```

Return what the control of one container shows as things stand.

<a id="edit_cfg_json_textual.textual_look.plain_widget"></a>

#### plain\_widget

```python
def plain_widget(text: str,
                 widget_id: str,
                 classes: Optional[str] = None,
                 emphasis: Optional[core.Emphasis] = None) -> Static
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
- `emphasis` - Why this text stands out from the values, or None for a
  widget that is shown in the ordinary text colour.
  

**Returns**:

  A widget showing that text.

<a id="edit_cfg_json_textual.textual_look.show_emphasis"></a>

#### show\_emphasis

```python
def show_emphasis(widget: Widget, emphasis: Optional[core.Emphasis]) -> None
```

Show one widget in the way that one reason to stand out asks for.

Every class of `EMPHASIS_CLASSES` is set or unset, so that a widget whose
emphasis changes as the model changes cannot end up carrying two of them
at once.

**Arguments**:

- `widget` - Widget to show.
- `emphasis` - Why the text of that widget stands out from the values, or
  None for the ordinary text colour.

<a id="edit_cfg_json_textual.textual_look.bind_action"></a>

#### bind\_action

```python
def bind_action(bindings: BindingsMap,
                keys: Sequence[str],
                action: str,
                description: str,
                priority: bool = True) -> None
```

Bind every key combination that the application gave one action.

The first combination is the one the footer names and the rest work
without being named, because a footer that named one action twice would
suggest that they were two actions. An action the application gave no
combination at all is bound to nothing and stays reachable through the
command palette.

A priority binding is acted on before the widget that has the focus is
offered the key, which is what an editor wants of its own keys: a user
who presses Save while typing into a field means Save. It is also why
these cannot be made with `App.bind`, which cannot make one and which
says of itself that it may be removed.

**Arguments**:

- `bindings` - The bindings of the widget, the screen or the application
  that the action belongs to.
- `keys` - Key combinations that run the action, in the order that
  decides which of them is named.
- `action` - Name of the action, without its `action_` prefix.
- `description` - What the footer and the key panel call the action.
- `priority` - Whether the key is offered here before the widget that has
  the focus is offered it, which is
  `edit_cfg_json.Settings.priority_keys` for the actions of the
  editor and always true for leaving a question of its own.

<a id="edit_cfg_json_textual.textual_screen"></a>

# edit\_cfg\_json\_textual.textual\_screen

One editor as a screen of a Textual application.

A screen is what a widget cannot be: it has a header and a footer of its own,
and it can offer entries in the command palette, which `Screen.COMMANDS` is
for and which a widget has no equivalent of at all. So this is what an
application pushes when it wants the editor to take the whole terminal for a
while, and it is what `EditorApp` shows when the editor is the whole program.

An application that wants the editor in an area of its own screen mounts
`EditorPanel` instead and keeps its own header, its own footer and its own
palette. That is the difference between the two, and it is the whole of it.

<a id="edit_cfg_json_textual.textual_screen.EditorCommands"></a>

## EditorCommands Objects

```python
class EditorCommands(Provider)
```

The actions of the editor, as the command palette offers them.

It asks the panel of its screen rather than holding a table of its own,
because the name of two of those actions says what the next press will do
and is therefore only true at the moment it is read.

<a id="edit_cfg_json_textual.textual_screen.EditorCommands.discover"></a>

#### discover

```python
async def discover() -> Hits
```

Offer every action of the editor before anything is typed.

**Yields**:

  One hit per action the editor offers.

<a id="edit_cfg_json_textual.textual_screen.EditorCommands.search"></a>

#### search

```python
async def search(query: str) -> Hits
```

Offer the actions whose names match what the user is typing.

**Arguments**:

- `query` - What the user has typed into the palette.
  

**Yields**:

  One hit per action whose name matches, as the matcher of the
  palette scores it.

<a id="edit_cfg_json_textual.textual_screen.EditorScreen"></a>

## EditorScreen Objects

```python
class EditorScreen(Screen[None])
```

A screen holding one editor, with a header and a footer of its own.

<a id="edit_cfg_json_textual.textual_screen.EditorScreen.COMMANDS"></a>

#### COMMANDS

The actions of the editor, offered in the command palette.

They are declared here and not on an application, because an application
that pushed this screen has a palette of its own and would otherwise be
made to name the actions of a screen it did not write.

<a id="edit_cfg_json_textual.textual_screen.EditorScreen.__init__"></a>

#### \_\_init\_\_

```python
def __init__(model: core.EditModel,
             *,
             on_close: Optional[Callable[[], None]] = None) -> None
```

Show one model on a screen of its own.

**Arguments**:

- `model` - Model to show and to edit.
- `on_close` - What the application does once the session has ended,
  or None for an application that reads the outcome some other
  way. An application that pushed this screen usually pops it
  here.

<a id="edit_cfg_json_textual.textual_screen.EditorScreen.panel"></a>

#### panel

```python
@property
def panel() -> EditorPanel
```

Return the editor that this screen is showing.

<a id="edit_cfg_json_textual.textual_screen.EditorScreen.compose"></a>

#### compose

```python
def compose() -> ComposeResult
```

Create the header, the editor and the footer, in that order.

<a id="edit_cfg_json_textual.textual_panel"></a>

# edit\_cfg\_json\_textual.textual\_panel

The whole editor of this backend, as one widget.

It is a widget and not an application, so that the same editor serves both
ways of running it: `EditorApp` composes a screen that holds one of these and
owns the terminal, and an application that already runs Textual mounts one of
these in an area of its own and goes on running its own event loop. One body,
so that the two cannot drift apart, and everything that only an application
may do — the title of the terminal, ending the process, the entries of the
command palette — is deliberately not here.

Everything this backend takes from the core is reached through `core`, which is
`edit_cfg_json` itself. A backend may use the public API of the core and
nothing else, and naming it at every call site is what makes that visible; it
also keeps the two backends from each holding the same block of twenty
imported names, which is a duplication with nothing to factor out, since
neither backend may import the other.

<a id="edit_cfg_json_textual.textual_panel.CLOSE_COMMAND"></a>

#### CLOSE\_COMMAND

Name of the action that ends the editing session.

It is Close and not Quit because this editor may be one panel of an
application that goes on running, and because closing writes nothing of its
own: it is the "cancel" of the design, exactly as the button of the Tk
backend that carries the same word.

<a id="edit_cfg_json_textual.textual_panel.VALIDATE_COMMAND"></a>

#### VALIDATE\_COMMAND

Name of the command palette entry that validates the buffer.

<a id="edit_cfg_json_textual.textual_panel.SAVE_COMMAND"></a>

#### SAVE\_COMMAND

Name of the command palette entry that writes the output file.

<a id="edit_cfg_json_textual.textual_panel.SAVE_AS_COMMAND"></a>

#### SAVE\_AS\_COMMAND

Name of the command palette entry that chooses a file and writes it.

<a id="edit_cfg_json_textual.textual_panel.EXPLAIN_COMMAND"></a>

#### EXPLAIN\_COMMAND

What the explain action is called while the explanations are hidden.

<a id="edit_cfg_json_textual.textual_panel.HIDE_COMMAND"></a>

#### HIDE\_COMMAND

What it is called while they are shown.

The name says what the next press does rather than what the action is about,
because "Explain" beside explanations that are already there reads as an offer
to do something that has been done. The Tk backend answers the same question
with a tick-box, which is what a button row can do and a footer cannot.

<a id="edit_cfg_json_textual.textual_panel.VALIDATE_HELP"></a>

#### VALIDATE\_HELP

What the command palette says the validate entry does.

<a id="edit_cfg_json_textual.textual_panel.SAVE_HELP"></a>

#### SAVE\_HELP

What the command palette says the save entry does.

<a id="edit_cfg_json_textual.textual_panel.SAVE_AS_HELP"></a>

#### SAVE\_AS\_HELP

What the command palette says the save as entry does.

<a id="edit_cfg_json_textual.textual_panel.EXPLAIN_HELP"></a>

#### EXPLAIN\_HELP

What the command palette says the explain entry does.

<a id="edit_cfg_json_textual.textual_panel.FOLD_COMMAND"></a>

#### FOLD\_COMMAND

What the fold action is called while at least one container is open.

<a id="edit_cfg_json_textual.textual_panel.OPEN_COMMAND"></a>

#### OPEN\_COMMAND

What it is called once every container is folded.

The name says what the next press does, exactly as the explain action above
is named. The Tk backend answers the same question by renaming its button.

<a id="edit_cfg_json_textual.textual_panel.FOLD_HELP"></a>

#### FOLD\_HELP

What the command palette says the fold entry does.

<a id="edit_cfg_json_textual.textual_panel.SAVE_AS_PROMPT"></a>

#### SAVE\_AS\_PROMPT

What the screen that asks for the output file says.

<a id="edit_cfg_json_textual.textual_panel.SAVE_AS_LEAVE"></a>

#### SAVE\_AS\_LEAVE

What that screen says while there is a key that leaves it.

The key is named from the settings and not written into the sentence,
because an application that took `escape` for itself would otherwise be
telling its users to press a key that does nothing.

<a id="edit_cfg_json_textual.textual_panel.EDITOR_ACTIONS"></a>

#### EDITOR\_ACTIONS

The actions of the editor, which a question of its own turns off.

Textual offers a priority binding the key before the widget that has the focus
gets it, and it goes on doing that while a modal screen is up: the dispatch of
a priority binding walks the whole chain and not the part of it above the last
modal screen. So a modal screen is only really modal if the editor says that
its own actions do not apply while it is there.

<a id="edit_cfg_json_textual.textual_panel.EditorCommand"></a>

## EditorCommand Objects

```python
class EditorCommand(NamedTuple)
```

One action of the editor, as a command palette offers it.

<a id="edit_cfg_json_textual.textual_panel.EditorCommand.name"></a>

#### name

What the palette calls it, which says what the next press will do.

<a id="edit_cfg_json_textual.textual_panel.EditorCommand.help_text"></a>

#### help\_text

What the palette says it does.

<a id="edit_cfg_json_textual.textual_panel.EditorCommand.run"></a>

#### run

What choosing it in the palette runs.

<a id="edit_cfg_json_textual.textual_panel.EditorPanel"></a>

## EditorPanel Objects

```python
class EditorPanel(Widget)
```

The whole editor of one edit model, as one widget.

It holds the label of the configuration, what the class says about itself,
what reading the input file did, one row per node, and below those the
validation verdict and the saving line. What does not scroll with the rest
is what a user reaches for after editing, exactly as in the Tk backend.

The keys of the editor are bound on this widget, so they are acted on
while the focus is inside the editor and not while it is elsewhere in a
window that an application owns.

<a id="edit_cfg_json_textual.textual_panel.EditorPanel.DEFAULT_CSS"></a>

#### DEFAULT\_CSS

The widths and the heights that make one member fit on one line.

See `PANEL_CSS`, which is where each of them is explained. It is
`DEFAULT_CSS` and not `CSS` because Textual ignores a `CSS` class variable
on a widget and says so, and the name of the class is written into it
because a widget styles itself by its type name.

<a id="edit_cfg_json_textual.textual_panel.EditorPanel.__init__"></a>

#### \_\_init\_\_

```python
def __init__(model: core.EditModel,
             *,
             on_close: Optional[Callable[[], None]] = None) -> None
```

Remember the model and bind the keys the application chose.

**Arguments**:

- `model` - Model to show and to edit.
- `on_close` - What the application does once the session has ended,
  or None for an application that reads the outcome some other
  way. It is called after the editor has taken itself off the
  screen, so that `edit_cfg_json.EditModel.saved_config` can be
  read from it.

<a id="edit_cfg_json_textual.textual_panel.EditorPanel.compose"></a>

#### compose

```python
def compose() -> ComposeResult
```

Create the label, one row per member, the verdict and the saving.

The label of the configuration comes first and is a widget of this
editor rather than the title of an application, because an editor
mounted in a window an application owns has no business writing there.
What the configuration class says about itself comes next, because
what the whole configuration is for is what the members below it are
read in the light of, and what reading the input file did comes after
that, because it is what explains the marks on them. Both are created
only when there is something to say: the file was read before the
model was built, and a class either has a docstring or has not, so
neither of the two can arrive later and an empty widget would take a
line of the screen for good.

Those and the members are the part that scrolls, because they are the
part that a configuration of any size makes as tall as it likes. What
the application makes of the values and where they would be written
stay below it, where a user who has just edited something looks for
them.

<a id="edit_cfg_json_textual.textual_panel.EditorPanel.command_entries"></a>

#### command\_entries

```python
def command_entries() -> tuple[EditorCommand, ...]
```

Return the actions of the editor, for a command palette.

Every terminal can reach the palette, because it is opened with one
key and then typed into. That is what makes it the answer for the key
of Save as, which a terminal without the Kitty keyboard protocol
cannot tell apart from the key of Save. The other actions are here for
the same reason a menu lists what has a shortcut: a user who has not
learnt the keys should still be able to work.

The names of two of them say what the next press will do, so this is
asked afresh whenever the palette is opened rather than being a table
that was written once.

**Returns**:

  One entry per action this editor offers as things stand.

<a id="edit_cfg_json_textual.textual_panel.EditorPanel.on_input_changed"></a>

#### on\_input\_changed

```python
def on_input_changed(event: Input.Changed) -> None
```

Write one field into the model and show what the model says.

A field posts this message when it is given its initial value as
well, which the model handles by treating a set that changes no text
as no edit at all.

<a id="edit_cfg_json_textual.textual_panel.EditorPanel.on_input_blurred"></a>

#### on\_input\_blurred

```python
def on_input_blurred(event: Input.Blurred) -> None
```

Ask the model about the member whose field the user has just left.

Leaving a field is when the user has moved on from it, and it is
therefore when the editor says whether what they typed means a value
of that member at all. Nothing is validated here: the whole
configuration is what a validation pass is about, and this is one
field answering for itself.

<a id="edit_cfg_json_textual.textual_panel.EditorPanel.action_close"></a>

#### action\_close

```python
def action_close() -> None
```

End the session, asking first where there is something to lose.

<a id="edit_cfg_json_textual.textual_panel.EditorPanel.close"></a>

#### close

```python
def close(ask_about_unsaved: bool = True) -> None
```

End the session and take the editor off the screen.

Closing writes nothing, so a buffer holding something that has not
reached the file loses it. Whether that is so and what is asked about
it are the core's, so that this backend and the Tk one cannot ask one
user something and another user nothing; how the question is put is
this backend's, and a modal screen is how a Textual application asks
anything.

Whether the user is asked at all is the application's to decide,
because only the application knows what it is closing the editor for.
The Close button and the quit key of the editor are this method with
the default, so the question is put in the same words whichever of the
three ended the session.

Calling this again once the session has ended does nothing, so an
application need not keep track of whether the user has closed the
editor already.

**Arguments**:

- `ask_about_unsaved` - Whether the user is asked before a buffer that
  holds something unsaved is dropped. The default asks, which is
  the way a default about something that cannot be undone should
  lean.

<a id="edit_cfg_json_textual.textual_panel.EditorPanel.action_validate"></a>

#### action\_validate

```python
def action_validate() -> None
```

Validate the buffer and show what the application would say.

<a id="edit_cfg_json_textual.textual_panel.EditorPanel.action_save"></a>

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

A destination that holds a file this session did not write is asked
about as well, because that file is about to stop existing. Nothing is
shown when the user says no: they have just been asked and answered,
and a line saying that nothing was written would be telling them what
they decided.

<a id="edit_cfg_json_textual.textual_panel.EditorPanel.action_explain"></a>

#### action\_explain

```python
def action_explain() -> None
```

Show or hide what the application says about these values.

The action is renamed as well, because what it is called says what the
next press will do: "Explain" beside explanations that are already
there would read as an offer to do something that has been done.

<a id="edit_cfg_json_textual.textual_panel.EditorPanel.action_fold"></a>

#### action\_fold

```python
def action_fold() -> None
```

Fold every container away, or open every one of them.

<a id="edit_cfg_json_textual.textual_panel.EditorPanel.on_button_pressed"></a>

#### on\_button\_pressed

```python
def on_button_pressed(event: Button.Pressed) -> None
```

Do what the control the user pressed is for.

There are two kinds of them and the identifier says which: the control
that folds one container, and the ones that change how many elements
a node holds. The message is stopped here because nothing above them
has any use for it.

<a id="edit_cfg_json_textual.textual_panel.EditorPanel.action_save_as"></a>

#### action\_save\_as

```python
def action_save_as() -> None
```

Ask which file to write, and write it when one was named.

<a id="edit_cfg_json_textual.textual_panel.EditorPanel.check_action"></a>

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

