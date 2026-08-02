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

The package is under construction. This first version opens a terminal
screen showing the configuration members read-only, and quits on `q`.
Editing, validation and saving follow.
