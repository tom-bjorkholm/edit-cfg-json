# Table of Contents

* [edit\_cfg\_json\_textual.textual\_editor](#edit_cfg_json_textual.textual_editor)
  * [VALUE\_ID\_PREFIX](#edit_cfg_json_textual.textual_editor.VALUE_ID_PREFIX)
  * [MARK\_ID\_PREFIX](#edit_cfg_json_textual.textual_editor.MARK_ID_PREFIX)
  * [DESCRIPTION\_ID\_PREFIX](#edit_cfg_json_textual.textual_editor.DESCRIPTION_ID_PREFIX)
  * [DOCSTRING\_ID](#edit_cfg_json_textual.textual_editor.DOCSTRING_ID)
  * [VERDICT\_ID](#edit_cfg_json_textual.textual_editor.VERDICT_ID)
  * [SAVE\_ID](#edit_cfg_json_textual.textual_editor.SAVE_ID)
  * [LOAD\_ID](#edit_cfg_json_textual.textual_editor.LOAD_ID)
  * [BODY\_ID](#edit_cfg_json_textual.textual_editor.BODY_ID)
  * [SAVE\_AS\_BOX\_ID](#edit_cfg_json_textual.textual_editor.SAVE_AS_BOX_ID)
  * [SAVE\_AS\_ID](#edit_cfg_json_textual.textual_editor.SAVE_AS_ID)
  * [NAME\_CLASS](#edit_cfg_json_textual.textual_editor.NAME_CLASS)
  * [VALUE\_CLASS](#edit_cfg_json_textual.textual_editor.VALUE_CLASS)
  * [MARK\_CLASS](#edit_cfg_json_textual.textual_editor.MARK_CLASS)
  * [ROW\_CLASS](#edit_cfg_json_textual.textual_editor.ROW_CLASS)
  * [MEMBER\_CLASS](#edit_cfg_json_textual.textual_editor.MEMBER_CLASS)
  * [DESCRIPTION\_CLASS](#edit_cfg_json_textual.textual_editor.DESCRIPTION_CLASS)
  * [NAME\_WIDTH](#edit_cfg_json_textual.textual_editor.NAME_WIDTH)
  * [DESCRIPTION\_INDENT](#edit_cfg_json_textual.textual_editor.DESCRIPTION_INDENT)
  * [LEAST\_VALUE\_WIDTH](#edit_cfg_json_textual.textual_editor.LEAST_VALUE_WIDTH)
  * [QUIT\_COMMAND](#edit_cfg_json_textual.textual_editor.QUIT_COMMAND)
  * [CANCEL\_COMMAND](#edit_cfg_json_textual.textual_editor.CANCEL_COMMAND)
  * [VALIDATE\_COMMAND](#edit_cfg_json_textual.textual_editor.VALIDATE_COMMAND)
  * [SAVE\_COMMAND](#edit_cfg_json_textual.textual_editor.SAVE_COMMAND)
  * [SAVE\_AS\_COMMAND](#edit_cfg_json_textual.textual_editor.SAVE_AS_COMMAND)
  * [EXPLAIN\_COMMAND](#edit_cfg_json_textual.textual_editor.EXPLAIN_COMMAND)
  * [HIDE\_COMMAND](#edit_cfg_json_textual.textual_editor.HIDE_COMMAND)
  * [VALIDATE\_HELP](#edit_cfg_json_textual.textual_editor.VALIDATE_HELP)
  * [SAVE\_HELP](#edit_cfg_json_textual.textual_editor.SAVE_HELP)
  * [SAVE\_AS\_HELP](#edit_cfg_json_textual.textual_editor.SAVE_AS_HELP)
  * [EXPLAIN\_HELP](#edit_cfg_json_textual.textual_editor.EXPLAIN_HELP)
  * [EMPHASIS\_CLASSES](#edit_cfg_json_textual.textual_editor.EMPHASIS_CLASSES)
  * [SAVE\_AS\_PROMPT](#edit_cfg_json_textual.textual_editor.SAVE_AS_PROMPT)
  * [SAVE\_AS\_LEAVE](#edit_cfg_json_textual.textual_editor.SAVE_AS_LEAVE)
  * [EDITOR\_ACTIONS](#edit_cfg_json_textual.textual_editor.EDITOR_ACTIONS)
  * [COLOUR\_RULES](#edit_cfg_json_textual.textual_editor.COLOUR_RULES)
  * [CSS\_RULES](#edit_cfg_json_textual.textual_editor.CSS_RULES)
  * [plain\_widget](#edit_cfg_json_textual.textual_editor.plain_widget)
  * [show\_emphasis](#edit_cfg_json_textual.textual_editor.show_emphasis)
  * [bind\_action](#edit_cfg_json_textual.textual_editor.bind_action)
  * [SaveAsScreen](#edit_cfg_json_textual.textual_editor.SaveAsScreen)
    * [\_\_init\_\_](#edit_cfg_json_textual.textual_editor.SaveAsScreen.__init__)
    * [compose](#edit_cfg_json_textual.textual_editor.SaveAsScreen.compose)
    * [on\_input\_changed](#edit_cfg_json_textual.textual_editor.SaveAsScreen.on_input_changed)
    * [on\_input\_submitted](#edit_cfg_json_textual.textual_editor.SaveAsScreen.on_input_submitted)
    * [action\_leave](#edit_cfg_json_textual.textual_editor.SaveAsScreen.action_leave)
  * [EditorApp](#edit_cfg_json_textual.textual_editor.EditorApp)
    * [CSS](#edit_cfg_json_textual.textual_editor.EditorApp.CSS)
    * [\_\_init\_\_](#edit_cfg_json_textual.textual_editor.EditorApp.__init__)
    * [compose](#edit_cfg_json_textual.textual_editor.EditorApp.compose)
    * [get\_system\_commands](#edit_cfg_json_textual.textual_editor.EditorApp.get_system_commands)
    * [on\_input\_changed](#edit_cfg_json_textual.textual_editor.EditorApp.on_input_changed)
    * [action\_validate](#edit_cfg_json_textual.textual_editor.EditorApp.action_validate)
    * [action\_save](#edit_cfg_json_textual.textual_editor.EditorApp.action_save)
    * [action\_explain](#edit_cfg_json_textual.textual_editor.EditorApp.action_explain)
    * [action\_save\_as](#edit_cfg_json_textual.textual_editor.EditorApp.action_save_as)
    * [check\_action](#edit_cfg_json_textual.textual_editor.EditorApp.check_action)
  * [TextualEditor](#edit_cfg_json_textual.textual_editor.TextualEditor)
    * [run\_editor](#edit_cfg_json_textual.textual_editor.TextualEditor.run_editor)
  * [edit](#edit_cfg_json_textual.textual_editor.edit)

<a id="edit_cfg_json_textual.textual_editor"></a>

# edit\_cfg\_json\_textual.textual\_editor

Textual view of an edit model, with one editable field per member.

Everything this backend takes from the core is reached through `core`, which is
`edit_cfg_json` itself. A backend may use the public API of the core and
nothing else, and naming it at every call site is what makes that visible; it
also keeps the two backends from each holding the same block of twenty
imported names, which is a duplication with nothing to factor out, since
neither backend may import the other.

<a id="edit_cfg_json_textual.textual_editor.VALUE_ID_PREFIX"></a>

#### VALUE\_ID\_PREFIX

Prefix of the identifier of the widget that shows one member value.

<a id="edit_cfg_json_textual.textual_editor.MARK_ID_PREFIX"></a>

#### MARK\_ID\_PREFIX

Prefix of the identifier of the widget that marks one member.

<a id="edit_cfg_json_textual.textual_editor.DESCRIPTION_ID_PREFIX"></a>

#### DESCRIPTION\_ID\_PREFIX

Prefix of the identifier of the widget that describes one member.

<a id="edit_cfg_json_textual.textual_editor.DOCSTRING_ID"></a>

#### DOCSTRING\_ID

Identifier of the widget that shows what the configuration class says.

<a id="edit_cfg_json_textual.textual_editor.VERDICT_ID"></a>

#### VERDICT\_ID

Identifier of the widget that shows what validation found.

<a id="edit_cfg_json_textual.textual_editor.SAVE_ID"></a>

#### SAVE\_ID

Identifier of the widget that shows what saving did or would do.

<a id="edit_cfg_json_textual.textual_editor.LOAD_ID"></a>

#### LOAD\_ID

Identifier of the widget that shows what reading the file did.

<a id="edit_cfg_json_textual.textual_editor.BODY_ID"></a>

#### BODY\_ID

Identifier of the part of the screen that scrolls.

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

<a id="edit_cfg_json_textual.textual_editor.MEMBER_CLASS"></a>

#### MEMBER\_CLASS

Style class of the container that holds one member and its description.

<a id="edit_cfg_json_textual.textual_editor.DESCRIPTION_CLASS"></a>

#### DESCRIPTION\_CLASS

Style class of the widget that says what one member is for.

<a id="edit_cfg_json_textual.textual_editor.NAME_WIDTH"></a>

#### NAME\_WIDTH

Width in cells of the column that holds the member names.

<a id="edit_cfg_json_textual.textual_editor.DESCRIPTION_INDENT"></a>

#### DESCRIPTION\_INDENT

Indentation in cells of the description of one member.

The indentation is what says that the line belongs to the member above it
rather than being a member of its own.

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

<a id="edit_cfg_json_textual.textual_editor.EXPLAIN_COMMAND"></a>

#### EXPLAIN\_COMMAND

What the explain action is called while the explanations are hidden.

<a id="edit_cfg_json_textual.textual_editor.HIDE_COMMAND"></a>

#### HIDE\_COMMAND

What it is called while they are shown.

The name says what the next press does rather than what the action is about,
because "Explain" beside explanations that are already there reads as an offer
to do something that has been done. The Tk backend answers the same question
with a tick-box, which is what a button row can do and a footer cannot.

<a id="edit_cfg_json_textual.textual_editor.VALIDATE_HELP"></a>

#### VALIDATE\_HELP

What the command palette says the validate entry does.

<a id="edit_cfg_json_textual.textual_editor.SAVE_HELP"></a>

#### SAVE\_HELP

What the command palette says the save entry does.

<a id="edit_cfg_json_textual.textual_editor.SAVE_AS_HELP"></a>

#### SAVE\_AS\_HELP

What the command palette says the save as entry does.

<a id="edit_cfg_json_textual.textual_editor.EXPLAIN_HELP"></a>

#### EXPLAIN\_HELP

What the command palette says the explain entry does.

<a id="edit_cfg_json_textual.textual_editor.EMPHASIS_CLASSES"></a>

#### EMPHASIS\_CLASSES

The style class of every reason the core has to show something differently.

One class per member of `edit_cfg_json.Emphasis`, and the style sheet gives
each of them a theme colour, so that the editor follows the terminal into its
light or dark
mode instead of naming colours of its own. What each kind of text is comes
from the core, so the two backends cannot colour one thing two ways.

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

<a id="edit_cfg_json_textual.textual_editor.COLOUR_RULES"></a>

#### COLOUR\_RULES

What each reason to stand out looks like, as a colour of the theme.

Theme colours and not colours of this backend's own: they are what follows the
terminal into its light or dark mode, and an editor that named colours itself
would be legible in one of the two and a guess in the other.

The values and their names are left alone, so the thing the user came to edit
is the most legible thing on the screen. Everything else is either secondary
text or a state to act on, which is what `edit_cfg_json.Emphasis` names.

<a id="edit_cfg_json_textual.textual_editor.CSS_RULES"></a>

#### CSS\_RULES

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

The question about the output file sits in the middle of the screen and takes
most of its width, so that a long path is still readable in a narrow
terminal. Its own field is untouched by the rule above, which reaches only
the fields inside a member row.

<a id="edit_cfg_json_textual.textual_editor.plain_widget"></a>

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

<a id="edit_cfg_json_textual.textual_editor.show_emphasis"></a>

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
def __init__(model: core.EditModel) -> None
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

What the configuration class says about itself comes above everything
else, because what the whole configuration is for is what the members
below it are read in the light of. What reading the input file did
comes next, because it is what explains the marks on them. Both are
created only when there is something to say: the file was read before
the model was built, and a class either has a docstring or has not, so
neither of the two can arrive later and an empty widget would take a
line of the screen for good.

Those and the members are the part that scrolls, because they are the
part that a configuration of any size makes as tall as it likes. What
the application makes of the values and where they would be written
stay below it, where a user who has just edited something looks for
them.

<a id="edit_cfg_json_textual.textual_editor.EditorApp.get_system_commands"></a>

#### get\_system\_commands

```python
def get_system_commands(screen: Screen[object]) -> Iterable[SystemCommand]
```

Offer the actions of the editor in the command palette as well.

Every terminal can reach the palette, because it is opened with one
key and then typed into. That is what makes it the answer for
`SAVE_AS_KEY`, which a terminal without the Kitty keyboard protocol
cannot tell apart from `SAVE_KEY`. The other actions are here for the
same reason a menu lists what has a shortcut: a user who has not
learnt the keys should still be able to work.

**Arguments**:

- `screen` - Screen the palette was opened from.
  

**Returns**:

  The commands of Textual itself, and then the ones of the editor.

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

<a id="edit_cfg_json_textual.textual_editor.EditorApp.action_explain"></a>

#### action\_explain

```python
def action_explain() -> None
```

Show or hide what the application says about these values.

The action is renamed as well, because what it is called says what the
next press will do: "Explain" beside explanations that are already
there would read as an offer to do something that has been done.

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
- `out_file` - File to write, or None to write the input file.
- `policy` - What to do about declared keys the input file does not hold.
- `settings` - What this application has already decided about key
  combinations and file names, or a callable that answers with it.
- `stderr_file` - Stream used for user-facing diagnostics.
  

**Returns**:

  The configuration object that was written, or None when nothing was.
  

**Raises**:

- `ConfigLoadError` - The input file cannot be opened for editing.

