## Main entry points

Everything a user of this package needs is re-exported from the top-level
`{{import_name}}` package, so it can be imported directly:

````python
from {{import_name}} import EditModel, EditorBackend, MemberRow, \
    ValidationVerdict, model_as_text, model_title, row_marks, \
    row_value_text, verdict_text
````

| Name | What it is |
| --- | --- |
| `EditModel` | The editable state of one `config_as_json.Config` object, discovered by looking at that object. Its members keep the order the configuration class declares them in, their values are held in JSON space, `set_text` writes the text of one edit field into one of them, and `validate` runs the application's own validation over the whole buffer. |
| `MemberRow` | One configuration member of the model: the path that addresses it, the value it holds now, the value it started with, and the flags that say what has happened to it. |
| `ValidationVerdict` | What one validation pass found: whether the application itself would accept the buffer, and the diagnostics it would produce. `EditModel.verdict` is the verdict of the last pass, or `None` while the buffer has not been validated since it last changed. |
| `EditorBackend` | The protocol a user interface implements. It is phrased against `EditModel`, so a backend can also be mounted by an application that runs its own event loop. |
| `model_as_text` | The plain text rendering of a whole model, used by the examples and by the tests so that the editor can be observed without a display. It ends with the validation state, so a rendering never leaves that unsaid. |
| `model_title` | The label of a whole model, marked while the buffer holds a change worth saving. Both backends show it, so neither of them decides on its own how an unsaved change looks. |
| `row_marks` | The marks of one member: that the user changed it, and that a validation pass then rewrote what the user wrote. Both can apply at once. |
| `row_value_text` | The value of one member as the text a field shows. A string is shown as the string itself, without the quotation marks that the file format puts around it. Both backends use it, so neither of them formats values itself. |
| `verdict_text` | The validation state of a model as text, with the diagnostics below it. Both backends show it, so the two of them cannot describe one verdict differently. |

The package is under construction. This version reads a flat configuration,
edits it in memory and validates it; reading a file and saving follow. A
member whose value is a list or a dict is reported as a row that cannot be
edited yet rather than being left out.

Text that is not a valid value yet is kept as it was typed rather than
refused, because a value that is being typed is not valid for most of the
time it takes to type it. What is wrong with it is said by the application's
own configuration class and not by any rule of this package: a validation
pass writes the buffer as JSON, constructs that class from it, and reports
what the class says. There is no second implementation of validation
anywhere, so a validator that an application writes for itself works here
without this package knowing anything about it.

A validation pass is not read only. A member validator returns the value
that is stored back into the member, so a validator such as one that changes
the case of a string rewrites what the user typed. The buffer is refreshed
from the configuration object that was accepted, and every value the pass
rewrote is marked, because changing what the user just typed without showing
it would be the worst of the available behaviours.
