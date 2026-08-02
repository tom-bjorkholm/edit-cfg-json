## Main entry points

Everything a user of this package needs is re-exported from the top-level
`{{import_name}}` package, so it can be imported directly:

````python
from {{import_name}} import EditModel, EditorBackend, MemberRow, \
    model_as_text, model_title, row_value_text
````

| Name | What it is |
| --- | --- |
| `EditModel` | The editable state of one `config_as_json.Config` object, discovered by looking at that object. Its members keep the order the configuration class declares them in, their values are held in JSON space, and `set_text` writes the text of one edit field into one of them. |
| `MemberRow` | One configuration member of the model: the path that addresses it, the value it holds now, the value it started with, and the flags that say what has happened to it. |
| `EditorBackend` | The protocol a user interface implements. It is phrased against `EditModel`, so a backend can also be mounted by an application that runs its own event loop. |
| `model_as_text` | The plain text rendering of a whole model, used by the examples and by the tests so that the editor can be observed without a display. |
| `model_title` | The label of a whole model, marked while the buffer holds a change worth saving. Both backends show it, so neither of them decides on its own how an unsaved change looks. |
| `row_value_text` | The value of one member as the text a field shows. A string is shown as the string itself, without the quotation marks that the file format puts around it. Both backends use it, so neither of them formats values itself. |

The package is under construction. This version reads a flat configuration
and edits it in memory; validation, reading a file and saving follow. A
member whose value is a list or a dict is reported as a row that cannot be
edited yet rather than being left out.

Text that is not a valid value yet is kept as it was typed rather than
refused, because a value that is being typed is not valid for most of the
time it takes to type it. Saying what is wrong with it is the job of the
step that follows this one, which runs the validators of the application
itself.
