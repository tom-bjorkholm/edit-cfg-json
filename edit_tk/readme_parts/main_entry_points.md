## Main entry points

Everything a user of this package needs is re-exported from the top-level
`{{import_name}}` package, so it can be imported directly:

````python
from {{import_name}} import TkEditor
````

`TkEditor` is the Tkinter implementation of the `EditorBackend` protocol of
`edit-cfg-json`. It has the one method that protocol asks for:

````python
from edit_cfg_json import EditModel
from {{import_name}} import TkEditor

TkEditor().run_editor(EditModel(config))
````

The package is under construction. This version opens a window with one
edit field per configuration member, and a button to close it. Every change
of a field goes straight into the model, and the label above the fields is
marked while the model holds a change worth saving. Validation, reading a
file and saving follow.
