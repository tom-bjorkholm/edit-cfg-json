# Table of Contents

* [edit\_cfg\_json\_tk.tk\_editor](#edit_cfg_json_tk.tk_editor)
  * [NAME\_COLUMN\_WIDTH](#edit_cfg_json_tk.tk_editor.NAME_COLUMN_WIDTH)
  * [PADDING](#edit_cfg_json_tk.tk_editor.PADDING)
  * [VALIDATE\_TEXT](#edit_cfg_json_tk.tk_editor.VALIDATE_TEXT)
  * [SAVE\_TEXT](#edit_cfg_json_tk.tk_editor.SAVE_TEXT)
  * [SAVE\_AS\_TEXT](#edit_cfg_json_tk.tk_editor.SAVE_AS_TEXT)
  * [CLOSE\_TEXT](#edit_cfg_json_tk.tk_editor.CLOSE_TEXT)
  * [SAVE\_AS\_TITLE](#edit_cfg_json_tk.tk_editor.SAVE_AS_TITLE)
  * [CONFIG\_FILES](#edit_cfg_json_tk.tk_editor.CONFIG_FILES)
  * [ALL\_FILES](#edit_cfg_json_tk.tk_editor.ALL_FILES)
  * [\_file\_types](#edit_cfg_json_tk.tk_editor._file_types)
  * [\_key\_handler](#edit_cfg_json_tk.tk_editor._key_handler)
  * [\_bind\_key](#edit_cfg_json_tk.tk_editor._bind_key)
  * [RowWidgets](#edit_cfg_json_tk.tk_editor.RowWidgets)
    * [field](#edit_cfg_json_tk.tk_editor.RowWidgets.field)
    * [mark](#edit_cfg_json_tk.tk_editor.RowWidgets.mark)
  * [EditorWidgets](#edit_cfg_json_tk.tk_editor.EditorWidgets)
    * [\_\_init\_\_](#edit_cfg_json_tk.tk_editor.EditorWidgets.__init__)
    * [label\_text](#edit_cfg_json_tk.tk_editor.EditorWidgets.label_text)
    * [verdict\_text\_shown](#edit_cfg_json_tk.tk_editor.EditorWidgets.verdict_text_shown)
    * [save\_text\_shown](#edit_cfg_json_tk.tk_editor.EditorWidgets.save_text_shown)
    * [\_add\_load\_message](#edit_cfg_json_tk.tk_editor.EditorWidgets._add_load_message)
    * [\_add\_buttons](#edit_cfg_json_tk.tk_editor.EditorWidgets._add_buttons)
    * [\_bind\_keys](#edit_cfg_json_tk.tk_editor.EditorWidgets._bind_keys)
    * [\_add\_row](#edit_cfg_json_tk.tk_editor.EditorWidgets._add_row)
    * [\_add\_value](#edit_cfg_json_tk.tk_editor.EditorWidgets._add_value)
    * [\_writer](#edit_cfg_json_tk.tk_editor.EditorWidgets._writer)
    * [\_validate](#edit_cfg_json_tk.tk_editor.EditorWidgets._validate)
    * [\_save](#edit_cfg_json_tk.tk_editor.EditorWidgets._save)
    * [\_save\_as](#edit_cfg_json_tk.tk_editor.EditorWidgets._save_as)
    * [\_refresh](#edit_cfg_json_tk.tk_editor.EditorWidgets._refresh)
    * [\_show\_state](#edit_cfg_json_tk.tk_editor.EditorWidgets._show_state)
  * [TkEditor](#edit_cfg_json_tk.tk_editor.TkEditor)
    * [\_\_init\_\_](#edit_cfg_json_tk.tk_editor.TkEditor.__init__)
    * [run\_editor](#edit_cfg_json_tk.tk_editor.TkEditor.run_editor)
  * [edit](#edit_cfg_json_tk.tk_editor.edit)
* [edit\_cfg\_json\_tk.key\_names](#edit_cfg_json_tk.key_names)
  * [MODIFIERS](#edit_cfg_json_tk.key_names.MODIFIERS)
  * [KEY\_NAMES](#edit_cfg_json_tk.key_names.KEY_NAMES)
  * [\_tk\_key](#edit_cfg_json_tk.key_names._tk_key)
  * [tk\_sequence](#edit_cfg_json_tk.key_names.tk_sequence)

<a id="edit_cfg_json_tk.tk_editor"></a>

# edit\_cfg\_json\_tk.tk\_editor

Tkinter view of an edit model, with one editable field per member.

<a id="edit_cfg_json_tk.tk_editor.NAME_COLUMN_WIDTH"></a>

#### NAME\_COLUMN\_WIDTH

Width in characters of the column that holds the member names.

<a id="edit_cfg_json_tk.tk_editor.PADDING"></a>

#### PADDING

Padding in pixels around the widgets of the editor.

<a id="edit_cfg_json_tk.tk_editor.VALIDATE_TEXT"></a>

#### VALIDATE\_TEXT

Text of the button that runs the validation of the application.

<a id="edit_cfg_json_tk.tk_editor.SAVE_TEXT"></a>

#### SAVE\_TEXT

Text of the button that writes the output file.

<a id="edit_cfg_json_tk.tk_editor.SAVE_AS_TEXT"></a>

#### SAVE\_AS\_TEXT

Text of the button that chooses an output file and then writes it.

<a id="edit_cfg_json_tk.tk_editor.CLOSE_TEXT"></a>

#### CLOSE\_TEXT

Text of the button that ends the editor.

Closing writes nothing of its own. It is the "cancel" of the design, and it
is called Close because saving leaves the editor open: a button called Cancel
beside values that have already been written would read as an offer to undo
the writing, which it is not.

<a id="edit_cfg_json_tk.tk_editor.SAVE_AS_TITLE"></a>

#### SAVE\_AS\_TITLE

Title of the dialog that asks which file to write.

<a id="edit_cfg_json_tk.tk_editor.CONFIG_FILES"></a>

#### CONFIG\_FILES

What the dialog calls the files of the extension the application uses.

<a id="edit_cfg_json_tk.tk_editor.ALL_FILES"></a>

#### ALL\_FILES

What the dialog calls every other file.

<a id="edit_cfg_json_tk.tk_editor._file_types"></a>

#### \_file\_types

```python
def _file_types(settings: Settings) -> list[tuple[str, str]]
```

Return what the dialog that asks for a file offers to filter by.

An application that enforces its extension has that one filter and no
other, because a name with another extension cannot be saved and a
dialog that offered to look for one would be inviting a refusal. An
application whose extension is a default offers it first and everything
else after it, because a name with another extension can be saved. An
application with no opinion offers nothing, which is what this dialog
did before there were settings at all.

**Arguments**:

- `settings` - What the application has decided about file names.
  

**Returns**:

  The file types of the dialog, empty when it has no opinion.

<a id="edit_cfg_json_tk.tk_editor._key_handler"></a>

#### \_key\_handler

```python
def _key_handler(command: Callable[[], None]) -> Callable[..., str]
```

Return the callback that runs one command for one key event.

**Arguments**:

- `command` - What that key does.
  

**Returns**:

  A callback that Tk can bind, which stops the event from being
  handled a second time by whatever else the window is bound to.

<a id="edit_cfg_json_tk.tk_editor._bind_key"></a>

#### \_bind\_key

```python
def _bind_key(window: tkinter.Misc, key: str, command: Callable[[],
                                                                None]) -> None
```

Bind one key combination of one action, if Tk can bind it.

A combination that the translation does not know, or that Tk refuses,
leaves that action without that key rather than without an editor: every
action of this backend has a button as well.

**Arguments**:

- `window` - Window that the binding is made on.
- `key` - One key combination, as `ActionSettings` writes them.
- `command` - What that key does.

<a id="edit_cfg_json_tk.tk_editor.RowWidgets"></a>

## RowWidgets Objects

```python
class RowWidgets(NamedTuple)
```

The widgets that one configuration member owns.

<a id="edit_cfg_json_tk.tk_editor.RowWidgets.field"></a>

#### field

The field of an editable member, and None for every other member.

<a id="edit_cfg_json_tk.tk_editor.RowWidgets.mark"></a>

#### mark

The widget that says what has happened to this member.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets"></a>

## EditorWidgets Objects

```python
class EditorWidgets()
```

The widgets that show one edit model below one parent widget.

This is a class rather than a function because the fields have to be
kept: a `tkinter.StringVar` unsets its Tcl variable when it is collected,
and the field it belongs to would then lose both its text and the
callback that writes it into the model. Keeping them together also gives
an application that mounts these widgets in a window of its own a single
object to hold on to.

The widgets of the members are kept in the order the model reports its
rows in, which is the order they were created in. This version of the
model neither adds nor removes a row, so the two orders stay the same
one and the pairing is checked rather than assumed.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets.__init__"></a>

#### \_\_init\_\_

```python
def __init__(parent: tkinter.Misc,
             model: EditModel,
             *,
             on_close: Optional[Callable[[], None]] = None) -> None
```

Create the label, one row per member, the verdict and the buttons.

The parent is a widget and not a window, so that the same rows can
later be mounted inside a window that an application owns itself.

**Arguments**:

- `parent` - Widget that becomes the parent of the created widgets.
- `model` - Model to show and to edit.
- `on_close` - What closing the editor does, or None to destroy the
  window these widgets are in. None is for a caller that owns
  that window, which is what `TkEditor` does. A caller that
  mounts these widgets in a window of an application says what
  closing does, because the editor must never destroy a window
  it did not create.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets.label_text"></a>

#### label\_text

```python
@property
def label_text() -> str
```

Return the text that the label of the whole model shows.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets.verdict_text_shown"></a>

#### verdict\_text\_shown

```python
@property
def verdict_text_shown() -> str
```

Return the text that the validation part of the editor shows.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets.save_text_shown"></a>

#### save\_text\_shown

```python
@property
def save_text_shown() -> str
```

Return the text that the saving part of the editor shows.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._add_load_message"></a>

#### \_add\_load\_message

```python
def _add_load_message(parent: tkinter.Misc) -> None
```

Show what reading the input file did, when it did anything.

The widget is created only when there is something to say. The file
was read before the model was built, so the message cannot arrive
later, and an empty widget would take a line of the window for a
message that will never come.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._add_buttons"></a>

#### \_add\_buttons

```python
def _add_buttons(parent: tkinter.Misc) -> None
```

Create the buttons that validate, save and end the run.

They share one row, because four buttons stacked above each other
would push the values of a real configuration off the window.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._bind_keys"></a>

#### \_bind\_keys

```python
def _bind_keys(window: tkinter.Misc) -> None
```

Bind the key combinations that the application chose.

The bindings are made on the window and not on each field, because
a key that a field does not use for itself reaches the window that
the field is in. Nothing is bound for the cancel action: the only
question this backend asks is the toolkit's own file dialog, which
answers that key itself.

The keys are read once, here, which is the whole of what a later
answer from a settings callable cannot change.

**Arguments**:

- `window` - Window that the bindings are made on.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._add_row"></a>

#### \_add\_row

```python
def _add_row(parent: tkinter.Misc, row: MemberRow) -> RowWidgets
```

Create the name widget, the value widget and the mark widget.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._add_value"></a>

#### \_add\_value

```python
def _add_value(parent: tkinter.Misc,
               row: MemberRow) -> Optional[tkinter.StringVar]
```

Create the value widget of one member and wire it to the model.

A member that the model cannot edit yet gets a widget that only
shows text, because there is nothing the user could do to it.

The variable is given the parent as its master, so that it is
created in the same Tcl interpreter as the field that reads it. A
variable constructed without one is created in the first interpreter
of the process instead, which is the wrong one as soon as the editor
is not the only Tk in the application: the field would then show
nothing and the callback below would never run.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._writer"></a>

#### \_writer

```python
def _writer(row: MemberRow, field: tkinter.StringVar) -> Callable[..., None]
```

Return the callback that writes one field into the model.

Tk reports a change of the variable and not of the widget, so the
callback reads the field itself. Every change is written through,
including the ones that no key press caused, such as a paste.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._validate"></a>

#### \_validate

```python
def _validate() -> None
```

Validate the buffer and show what the application would say.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._save"></a>

#### \_save

```python
def _save() -> None
```

Write the output file, and say what came of trying.

Saving validates, so it can rewrite a value exactly as validating
can, and the fields are refreshed for the same reason.

A session that has no file to write yet is asked where to write,
which is what every editor does and what the design asks a backend
for. There is no way round to loop back here, because the question
is what gives the session a file.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._save_as"></a>

#### \_save\_as

```python
def _save_as() -> None
```

Ask which file to write, and write it when one was named.

What the dialog offers is what the application decided: the
extension it uses for its configuration is the one the dialog adds
to a name that has none, and the one it offers to filter by. An
application with no opinion gets a dialog with none, which is what
this dialog had before there were settings at all.

The name that comes back is handed to the model, which is what
completes it and what refuses it, so that a user of this backend and
a user of the other one are told the same thing about one name.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._refresh"></a>

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

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._show_state"></a>

#### \_show\_state

```python
def _show_state() -> None
```

Show the label, the verdict, the saving and every member mark.

<a id="edit_cfg_json_tk.tk_editor.TkEditor"></a>

## TkEditor Objects

```python
class TkEditor()
```

Tkinter user interface backend for an edit model.

The class has the single method that `EditorBackend` asks for, and
deliberately nothing else: everything worth testing without a display
lives in the core.

<a id="edit_cfg_json_tk.tk_editor.TkEditor.__init__"></a>

#### \_\_init\_\_

```python
def __init__() -> None
```

Create a backend that has not shown a model yet.

<a id="edit_cfg_json_tk.tk_editor.TkEditor.run_editor"></a>

#### run\_editor

```python
def run_editor(model: EditModel) -> None
```

Show the model in a Tk window until the user closes it.

The widgets are held for as long as the window lives, because they
own the fields that the Tcl variables belong to. The window is this
backend's own, which is why closing the editor destroys it.

This is for an application that has no Tk of its own yet, because a
second `tkinter.Tk` is a second Tcl interpreter and nothing can be
shared between the two. An application that already runs Tk gets the
entry point of section 8.2 of `doc/design.md` instead, which mounts
the editor in a widget that application owns.

**Arguments**:

- `model` - Model to show and to edit.

<a id="edit_cfg_json_tk.tk_editor.edit"></a>

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

Edit one configuration in a Tk window, and return what was saved.

This is `edit_cfg_json.edit` with this package's backend filled in, for
an application that has already chosen Tkinter. Everything it does is
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

<a id="edit_cfg_json_tk.key_names"></a>

# edit\_cfg\_json\_tk.key\_names

Translating a key combination into the notation that Tk binds by.

The application writes its key combinations once, in the notation that
`edit_cfg_json.ActionSettings` documents, and each backend translates them
into whatever its own toolkit binds by. Tk needs a translation whatever
notation is chosen, because `<Control-Shift-S>` is a form that no other
toolkit shares.

A combination this module does not know leaves that action without that key
rather than without an editor: every action of this backend has a button as
well.

<a id="edit_cfg_json_tk.key_names.MODIFIERS"></a>

#### MODIFIERS

What Tk calls each modifier that a combination can name.

<a id="edit_cfg_json_tk.key_names.KEY_NAMES"></a>

#### KEY\_NAMES

What Tk calls each named key, where the two notations differ.

The keys of this mapping are the names that `ActionSettings` documents, and
the values are the keysyms of Tk. The two of them agree about nothing but
`Tab`, which is in here anyway so that the mapping answers for every name
the notation has rather than for the ones that happen to differ.

<a id="edit_cfg_json_tk.key_names._tk_key"></a>

#### \_tk\_key

```python
def _tk_key(key: str, shifted: bool) -> Optional[str]
```

Return the keysym that Tk knows one key by.

A single character is that character, in upper case when the
combination also names the shift, because Tk reads `<Control-S>` as the
shifted key and `<Control-s>` as the unshifted one.

**Arguments**:

- `key` - The part of a combination that is not a modifier.
- `shifted` - Whether the combination also names the shift.
  

**Returns**:

  The keysym of that key, or None when this module does not know it.

<a id="edit_cfg_json_tk.key_names.tk_sequence"></a>

#### tk\_sequence

```python
def tk_sequence(combination: str) -> Optional[str]
```

Return one key combination as the event sequence that Tk binds by.

**Arguments**:

- `combination` - One key combination, as `ActionSettings` writes them.
  

**Returns**:

  The Tk event sequence of that combination, or None when it names a
  modifier or a key that this module does not know. None is not an
- `error` - the action it belongs to keeps its button and loses only
  this way of reaching it.

