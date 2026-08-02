## Main entry points

Everything a user of this package needs is re-exported from the top-level
`{{import_name}}` package, so it can be imported directly:

````python
from {{import_name}} import TkEditor
````

`TkEditor` is the Tkinter implementation of the `EditorBackend` protocol of
`edit-cfg-json`. It has the one method that protocol asks for:

````python
from edit_cfg_json import EditModel, load_config
from {{import_name}} import TkEditor

loaded = load_config(config=config, in_file='my_config.json')
TkEditor().run_editor(EditModel(config=loaded.config, report=loaded.report))
````

The package is under construction. This version opens a window with one
edit field per configuration member, a Validate button and a Close button.
Every change of a field goes straight into the model, and the label above
the fields is marked while the model holds a change worth saving. Saving
follows.

Validate runs the validation of the application's own configuration class
and shows below the fields what that class would say about the values that
are in them. A pass is not read only: a validator returns the value that is
stored back into the member, so the fields are written back from the model
afterwards, and a member that a validator rewrote says so beside its field.

What reading the input file did is shown above the fields, when it did
anything, because it is what explains the marks below it: a member that the
file did not hold says so beside its field. Both the message and the marks
are read from the model, so the two backends cannot tell the user two
different things about one file.
