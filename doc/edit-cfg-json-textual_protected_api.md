# Table of Contents

* [edit\_cfg\_json\_textual.textual\_editor](#edit_cfg_json_textual.textual_editor)
  * [VALUE\_ID\_PREFIX](#edit_cfg_json_textual.textual_editor.VALUE_ID_PREFIX)
  * [NAME\_CLASS](#edit_cfg_json_textual.textual_editor.NAME_CLASS)
  * [ROW\_CLASS](#edit_cfg_json_textual.textual_editor.ROW_CLASS)
  * [NAME\_WIDTH](#edit_cfg_json_textual.textual_editor.NAME_WIDTH)
  * [EditorApp](#edit_cfg_json_textual.textual_editor.EditorApp)
    * [BINDINGS](#edit_cfg_json_textual.textual_editor.EditorApp.BINDINGS)
    * [CSS](#edit_cfg_json_textual.textual_editor.EditorApp.CSS)
    * [\_\_init\_\_](#edit_cfg_json_textual.textual_editor.EditorApp.__init__)
    * [compose](#edit_cfg_json_textual.textual_editor.EditorApp.compose)
  * [TextualEditor](#edit_cfg_json_textual.textual_editor.TextualEditor)
    * [run\_editor](#edit_cfg_json_textual.textual_editor.TextualEditor.run_editor)

<a id="edit_cfg_json_textual.textual_editor"></a>

# edit\_cfg\_json\_textual.textual\_editor

Read-only Textual view of an edit model.

<a id="edit_cfg_json_textual.textual_editor.VALUE_ID_PREFIX"></a>

#### VALUE\_ID\_PREFIX

Prefix of the identifier of the widget that shows one member value.

<a id="edit_cfg_json_textual.textual_editor.NAME_CLASS"></a>

#### NAME\_CLASS

Style class of the widget that shows one member name.

<a id="edit_cfg_json_textual.textual_editor.ROW_CLASS"></a>

#### ROW\_CLASS

Style class of the container that holds the widgets of one member.

<a id="edit_cfg_json_textual.textual_editor.NAME_WIDTH"></a>

#### NAME\_WIDTH

Width in cells of the column that holds the member names.

<a id="edit_cfg_json_textual.textual_editor.EditorApp"></a>

## EditorApp Objects

```python
class EditorApp(App[None])
```

Textual application that shows one edit model read-only.

<a id="edit_cfg_json_textual.textual_editor.EditorApp.BINDINGS"></a>

#### BINDINGS

The quit key, which the footer shows so that it can be found.

<a id="edit_cfg_json_textual.textual_editor.EditorApp.CSS"></a>

#### CSS

One cell high rows, so that the footer stays visible below them.

<a id="edit_cfg_json_textual.textual_editor.EditorApp.__init__"></a>

#### \_\_init\_\_

```python
def __init__(model: EditModel) -> None
```

Remember the model and name the application after it.

**Arguments**:

- `model` - Model to show.

<a id="edit_cfg_json_textual.textual_editor.EditorApp.compose"></a>

#### compose

```python
def compose() -> ComposeResult
```

Create one row per configuration member, with header and footer.

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

- `model` - Model to show.

