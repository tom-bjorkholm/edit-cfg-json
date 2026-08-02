# Table of Contents

* [edit\_cfg\_json\_tk.tk\_editor](#edit_cfg_json_tk.tk_editor)
  * [NAME\_COLUMN\_WIDTH](#edit_cfg_json_tk.tk_editor.NAME_COLUMN_WIDTH)
  * [PADDING](#edit_cfg_json_tk.tk_editor.PADDING)
  * [\_add\_row](#edit_cfg_json_tk.tk_editor._add_row)
  * [build\_editor\_widgets](#edit_cfg_json_tk.tk_editor.build_editor_widgets)
  * [TkEditor](#edit_cfg_json_tk.tk_editor.TkEditor)
    * [run\_editor](#edit_cfg_json_tk.tk_editor.TkEditor.run_editor)

<a id="edit_cfg_json_tk.tk_editor"></a>

# edit\_cfg\_json\_tk.tk\_editor

Read-only Tkinter view of an edit model.

<a id="edit_cfg_json_tk.tk_editor.NAME_COLUMN_WIDTH"></a>

#### NAME\_COLUMN\_WIDTH

Width in characters of the column that holds the member names.

<a id="edit_cfg_json_tk.tk_editor.PADDING"></a>

#### PADDING

Padding in pixels around the widgets of the editor.

<a id="edit_cfg_json_tk.tk_editor._add_row"></a>

#### \_add\_row

```python
def _add_row(parent: tkinter.Misc, row: MemberRow) -> None
```

Create the name and the value widget for one configuration member.

<a id="edit_cfg_json_tk.tk_editor.build_editor_widgets"></a>

#### build\_editor\_widgets

```python
def build_editor_widgets(parent: tkinter.Misc, model: EditModel) -> None
```

Create the read-only rows and a close button under one parent.

The parent is a widget and not a window, so that the same rows can later
be mounted inside a window that an application owns itself.

**Arguments**:

- `parent` - Widget that becomes the parent of the created widgets.
- `model` - Model to show.

<a id="edit_cfg_json_tk.tk_editor.TkEditor"></a>

## TkEditor Objects

```python
class TkEditor()
```

Tkinter user interface backend for an edit model.

The class has the single method that `EditorBackend` asks for, and
deliberately nothing else: everything worth testing without a display
lives in the core.

<a id="edit_cfg_json_tk.tk_editor.TkEditor.run_editor"></a>

#### run\_editor

```python
def run_editor(model: EditModel) -> None
```

Show the model in a Tk window until the user closes it.

**Arguments**:

- `model` - Model to show.

