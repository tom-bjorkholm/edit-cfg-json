## Main entry points

Everything a user of this package needs is re-exported from the top-level
`{{import_name}}` package, so it can be imported directly:

````python
from {{import_name}} import EditModel, EditorBackend, MemberRow, \
    model_as_text, row_value_text
````

| Name | What it is |
| --- | --- |
| `EditModel` | The editable state of one `config_as_json.Config` object, discovered by looking at that object. Holds its values in JSON space, that is as they are written to the configuration file. |
| `MemberRow` | One configuration member of the model: its name, its JSON space value, and whether this version can edit it. |
| `EditorBackend` | The protocol a user interface implements. It is phrased against `EditModel`, so a backend can also be mounted by an application that runs its own event loop. |
| `model_as_text` | The plain text rendering of a whole model, used by the examples and by the tests so that the editor can be observed without a display. |
| `row_value_text` | The value of one member as the text a field shows. Both backends use it, so neither of them formats values itself. |

The package is under construction. This first version reads a flat
configuration and shows it; editing, validation, reading a file and saving
follow. A member whose value is a list or a dict is reported as a row that
cannot be edited yet rather than being left out.
