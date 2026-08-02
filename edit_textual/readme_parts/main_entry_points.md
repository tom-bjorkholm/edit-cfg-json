## Main entry points

Everything a user of this package needs is re-exported from the top-level
`{{import_name}}` package, so it can be imported directly:

````python
from {{import_name}} import TextualEditor
````

`TextualEditor` is the Textual implementation of the `EditorBackend`
protocol of `edit-cfg-json`. It has the one method that protocol asks for:

````python
from edit_cfg_json import EditModel
from {{import_name}} import TextualEditor

TextualEditor().run_editor(EditModel(config))
````

The package is under construction. This version opens a terminal screen with
one edit field per configuration member, and quits on `ctrl+q`. Every change
of a field goes straight into the model, and the title is marked while the
model holds a change worth saving. Validation, reading a file and saving
follow.

The quit key is `ctrl+q` and no longer a plain letter, because an unmodified
letter now belongs to whichever field has the focus: a user who types it
expects to see it appear in the field.
