# Table of Contents

* [edit\_cfg\_json\_tk.tk\_editor](#edit_cfg_json_tk.tk_editor)
  * [NAME\_COLUMN\_WIDTH](#edit_cfg_json_tk.tk_editor.NAME_COLUMN_WIDTH)
  * [PADDING](#edit_cfg_json_tk.tk_editor.PADDING)
  * [VALIDATE\_TEXT](#edit_cfg_json_tk.tk_editor.VALIDATE_TEXT)
  * [CLOSE\_TEXT](#edit_cfg_json_tk.tk_editor.CLOSE_TEXT)
  * [RowWidgets](#edit_cfg_json_tk.tk_editor.RowWidgets)
    * [field](#edit_cfg_json_tk.tk_editor.RowWidgets.field)
    * [mark](#edit_cfg_json_tk.tk_editor.RowWidgets.mark)
  * [EditorWidgets](#edit_cfg_json_tk.tk_editor.EditorWidgets)
    * [\_\_init\_\_](#edit_cfg_json_tk.tk_editor.EditorWidgets.__init__)
    * [label\_text](#edit_cfg_json_tk.tk_editor.EditorWidgets.label_text)
    * [verdict\_text\_shown](#edit_cfg_json_tk.tk_editor.EditorWidgets.verdict_text_shown)
    * [\_add\_load\_message](#edit_cfg_json_tk.tk_editor.EditorWidgets._add_load_message)
    * [\_add\_buttons](#edit_cfg_json_tk.tk_editor.EditorWidgets._add_buttons)
    * [\_add\_row](#edit_cfg_json_tk.tk_editor.EditorWidgets._add_row)
    * [\_add\_value](#edit_cfg_json_tk.tk_editor.EditorWidgets._add_value)
    * [\_writer](#edit_cfg_json_tk.tk_editor.EditorWidgets._writer)
    * [\_validate](#edit_cfg_json_tk.tk_editor.EditorWidgets._validate)
    * [\_show\_state](#edit_cfg_json_tk.tk_editor.EditorWidgets._show_state)
  * [TkEditor](#edit_cfg_json_tk.tk_editor.TkEditor)
    * [\_\_init\_\_](#edit_cfg_json_tk.tk_editor.TkEditor.__init__)
    * [run\_editor](#edit_cfg_json_tk.tk_editor.TkEditor.run_editor)

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

<a id="edit_cfg_json_tk.tk_editor.CLOSE_TEXT"></a>

#### CLOSE\_TEXT

Text of the button that ends the editor.

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
def __init__(parent: tkinter.Misc, model: EditModel) -> None
```

Create the label, one row per member, the verdict and the buttons.

The parent is a widget and not a window, so that the same rows can
later be mounted inside a window that an application owns itself.

**Arguments**:

- `parent` - Widget that becomes the parent of the created widgets.
- `model` - Model to show and to edit.

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

Create the button that validates and the one that ends the run.

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

The fields are written back from the model afterwards, because a
validation pass is not read only: a member validator returns the
value that is stored back into the member, so a value can end up
different from the one the user typed. Writing the text the model
already holds into a field is not an edit, so this refresh does not
undo the marks that the pass has just set.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._show_state"></a>

#### \_show\_state

```python
def _show_state() -> None
```

Show the label, the verdict and the mark of every member.

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
own the fields that the Tcl variables belong to.

**Arguments**:

- `model` - Model to show and to edit.

