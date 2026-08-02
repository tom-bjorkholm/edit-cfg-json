## Main entry points

Everything a user of this package needs is re-exported from the top-level
`{{import_name}}` package, so it can be imported directly:

````python
from {{import_name}} import ConfigLoadError, EditModel, EditorBackend, \
    LoadPolicy, LoadReport, LoadedConfig, MemberRow, ValidationVerdict, \
    load_config, load_text, model_as_text, model_title, row_marks, \
    row_value_text, verdict_text
````

| Name | What it is |
| --- | --- |
| `EditModel` | The editable state of one `config_as_json.Config` object, discovered by looking at that object. Its members keep the order the configuration class declares them in, their values are held in JSON space, `set_text` writes the text of one edit field into one of them, and `validate` runs the application's own validation over the whole buffer. |
| `MemberRow` | One configuration member of the model: the path that addresses it, the value it holds now, the value it started with, and the flags that say what has happened to it. |
| `ValidationVerdict` | What one validation pass found: whether the application itself would accept the buffer, and the diagnostics it would produce. `EditModel.verdict` is the verdict of the last pass, or `None` while the buffer has not been validated since it last changed. |
| `load_config` | Reads the configuration to edit from one input file, or hands back the caller's own object when there is no file. It constructs the configuration class itself, because a load policy and the reporting of automatic changes are given to a constructor and to nothing else. |
| `LoadPolicy` | What to do about a declared value the input file does not hold: `STRICT`, `DEFAULTS`, or `STRICT_THEN_DEFAULTS`, which is the default. |
| `LoadedConfig` | What `load_config` returns: the object to edit, and the report of its load. |
| `LoadReport` | What one load did beyond reading the values: what the user has to be told, and the names of the members the declared defaults supplied. It is handed to `EditModel`, which marks those members. |
| `ConfigLoadError` | The refusal of an input file that cannot be opened, holding the message for the user and the diagnostics the configuration class produced. |
| `EditorBackend` | The protocol a user interface implements. It is phrased against `EditModel`, so a backend can also be mounted by an application that runs its own event loop. |
| `model_as_text` | The plain text rendering of a whole model, used by the examples and by the tests so that the editor can be observed without a display. It begins with what the load did and ends with the validation state, so a rendering never leaves either of them unsaid. |
| `model_title` | The label of a whole model, marked while the buffer holds a change worth saving. Both backends show it, so neither of them decides on its own how an unsaved change looks. |
| `load_text` | What reading the input file did, as text, and nothing at all when it did nothing worth saying. Both backends show it, so the two of them cannot tell the user two different things about one file. |
| `row_marks` | The marks of one member: that the input file did not hold it, that the user changed it, and that a validation pass then rewrote what the user wrote. All of them can apply at once. |
| `row_value_text` | The value of one member as the text a field shows. A string is shown as the string itself, without the quotation marks that the file format puts around it. Both backends use it, so neither of them formats values itself. |
| `verdict_text` | The validation state of a model as text, with the diagnostics below it. Both backends show it, so the two of them cannot describe one verdict differently. |

The package is under construction. This version reads a flat configuration
from a file, edits it in memory and validates it; saving follows. A member
whose value is a list or a dict is reported as a row that cannot be edited
yet rather than being left out.

## Reading the input file

`load_config` constructs the configuration class rather than taking an
already loaded object, because the two things a load has to be told are given
to a constructor and to nothing else: the policy for declared keys the file
does not hold, and the hook that reports the automatic changes of an old
format file. The hook is passed on only to a class that declares it, since
the constructor that `config_as_json` documents does not.

A value the file leaves out is filled in from the declared default of the
class, and that member is marked, so the user can see which values are not
the ones the file asked for. Every other way in which an input file can be
wrong is a refusal with a message of its own: a key the configuration does
not declare, text that cannot be read as configuration, values a validator
refuses, and a file that cannot be read at all.

`config_as_json` reports a missing key and an unknown key as the same
`KeyError`, and the two are told apart by retrying the load with the defaults
filling in: that rescues a file which is merely incomplete, and it still
refuses an unknown key. Nothing anywhere reads the text of a message to
decide which of the two it was.

A file whose values a validator refuses cannot be opened. A member validator
returns the value that is stored back into the member, so a load that stopped
part way through leaves it unknown which values were already rewritten and
which were not, and there is then nothing honest to show.

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
