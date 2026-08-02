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
edit field per configuration member, a Validate button and a Close button.
Every change of a field goes straight into the model, and the label above
the fields is marked while the model holds a change worth saving. Reading a
file and saving follow.

Validate runs the validation of the application's own configuration class
and shows below the fields what that class would say about the values that
are in them. A pass is not read only: a validator returns the value that is
stored back into the member, so the fields are written back from the model
afterwards, and a member that a validator rewrote says so beside its field.
