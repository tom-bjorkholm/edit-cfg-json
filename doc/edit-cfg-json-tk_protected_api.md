# Table of Contents

* [edit\_cfg\_json\_tk.tk\_editor](#edit_cfg_json_tk.tk_editor)
  * [NAME\_COLUMN\_WIDTH](#edit_cfg_json_tk.tk_editor.NAME_COLUMN_WIDTH)
  * [PADDING](#edit_cfg_json_tk.tk_editor.PADDING)
  * [EditorWidgets](#edit_cfg_json_tk.tk_editor.EditorWidgets)
    * [\_\_init\_\_](#edit_cfg_json_tk.tk_editor.EditorWidgets.__init__)
    * [label\_text](#edit_cfg_json_tk.tk_editor.EditorWidgets.label_text)
    * [\_add\_row](#edit_cfg_json_tk.tk_editor.EditorWidgets._add_row)
    * [\_add\_field](#edit_cfg_json_tk.tk_editor.EditorWidgets._add_field)
    * [\_writer](#edit_cfg_json_tk.tk_editor.EditorWidgets._writer)
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

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets.__init__"></a>

#### \_\_init\_\_

```python
def __init__(parent: tkinter.Misc, model: EditModel) -> None
```

Create the label, one row per member and a close button.

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

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._add_row"></a>

#### \_add\_row

```python
def _add_row(parent: tkinter.Misc, row: MemberRow) -> None
```

Create the name widget and the value widget of one member.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._add_field"></a>

#### \_add\_field

```python
def _add_field(parent: tkinter.Misc, row: MemberRow) -> None
```

Create the field of one member and wire it to the model.

<a id="edit_cfg_json_tk.tk_editor.EditorWidgets._writer"></a>

#### \_writer

```python
def _writer(row: MemberRow, field: tkinter.StringVar) -> Callable[..., None]
```

Return the callback that writes one field into the model.

Tk reports a change of the variable and not of the widget, so the
callback reads the field itself. Every change is written through,
including the ones that no key press caused, such as a paste.

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

