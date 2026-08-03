## Main entry points

Everything a user of this package needs is re-exported from the top-level
`{{import_name}}` package, so it can be imported directly:

````python
from {{import_name}} import ConfigLoadError, EditModel, EditorBackend, \
    LoadPolicy, LoadReport, LoadedConfig, MemberRow, SaveOutcome, \
    ValidationVerdict, edit, load_config, load_text, model_as_text, \
    model_title, row_marks, row_value_text, save_text, verdict_text
````

| Name | What it is |
| --- | --- |
| `edit` | The whole of an editing session in one call: read the input file, build the model, run a backend to completion, and give back the configuration object that was saved, or `None` when nothing was. The backend is a parameter because this package never imports a user interface library; each backend package also exports an `edit` of its own that supplies itself. |
| `EditModel` | The editable state of one `config_as_json.Config` object, discovered by looking at that object. Its members keep the order the configuration class declares them in, their values are held in JSON space, `set_text` writes the text of one edit field into one of them, `validate` runs the application's own validation over the whole buffer, and `save` writes it to `out_file` if the application would accept it. |
| `MemberRow` | One configuration member of the model: the path that addresses it, the value it holds now, the value it started with, and the flags that say what has happened to it. |
| `ValidationVerdict` | What one validation pass found: whether the application itself would accept the buffer, and the diagnostics it would produce. `EditModel.verdict` is the verdict of the last pass, or `None` while the buffer has not been validated since it last changed. |
| `SaveOutcome` | What one attempt to save did: whether the output file was written, and what to tell the user about it. `EditModel.save_message` is the message of the last attempt. |
| `load_config` | Reads the configuration to edit from one input file, or hands back the caller's own object when there is no file. It constructs the configuration class itself, because a load policy and the reporting of automatic changes are given to a constructor and to nothing else. |
| `LoadPolicy` | What to do about a declared value the input file does not hold: `STRICT`, `DEFAULTS`, or `STRICT_THEN_DEFAULTS`, which is the default. |
| `LoadedConfig` | What `load_config` returns: the object to edit, and the report of its load. |
| `LoadReport` | What one load did beyond reading the values: what the user has to be told, and the names of the members the declared defaults supplied. It is handed to `EditModel`, which marks those members. |
| `ConfigLoadError` | The refusal of an input file that cannot be opened, holding the message for the user and the diagnostics the configuration class produced. |
| `EditorBackend` | The protocol a user interface implements. It is phrased against `EditModel`, so a backend can also be mounted by an application that runs its own event loop. |
| `model_as_text` | The plain text rendering of a whole model, used by the examples and by the tests so that the editor can be observed without a display. It begins with what the load did and ends with the validation state and the saving, so a rendering never leaves any of them unsaid. |
| `model_title` | The label of a whole model, marked while the buffer holds a change worth saving. Both backends show it, so neither of them decides on its own how an unsaved change looks. |
| `load_text` | What reading the input file did, as text, and nothing at all when it did nothing worth saying. Both backends show it, so the two of them cannot tell the user two different things about one file. |
| `row_marks` | The marks of one member: that the input file did not hold it, that the user changed it, and that a validation pass then rewrote what the user wrote. All of them can apply at once. |
| `row_value_text` | The value of one member as the text a field shows. A string is shown as the string itself, without the quotation marks that the file format puts around it. Both backends use it, so neither of them formats values itself. |
| `verdict_text` | The validation state of a model as text, with the diagnostics below it. Both backends show it, so the two of them cannot describe one verdict differently. |
| `save_text` | What saving did, or where it would write if it were asked, or that no file has been chosen at all. Those are three different states, and a user who cannot tell them apart cannot tell whether Save will ask them something. |

The package is under construction. This version reads a flat configuration
from a file, edits it, validates it and writes it. A member whose value is a
list or a dict is reported as a row that cannot be edited yet rather than
being left out.

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

## Writing the output file

Saving is validating and then writing, and it is refused wherever the
validation is: an editor that produced a file its own application could not
read would have failed at the one thing it is for. It is the *same* pass the
user asks for by hand, so a validator that rewrites a value rewrites it on the
way to the file too, and what the editor shows afterwards is what was written
rather than what was typed. The object that is written is the very object the
verdict was reached about, and it is what `edit` gives back, so an application
needs no load of its own to work with what it saved.

`out_file` defaults to `in_file`, which is what an editor is normally asked to
do. With neither, there is nowhere to write; the model says so and invents
nothing, because a file name is not something a library can guess, and both
backends ask the user for one. The file name is entirely the application's
business: this library has no opinion about the extension, since some
applications use `.cfg`, some use `.json`, and others use something else
again.

A save that wrote the file leaves nothing to save, so the values that reached
it become the ones the buffer is compared against and the model stops
reporting itself as dirty. The editor stays open, and `edit` gives back the
object that really reached the file however much was typed after it.

Nothing is lost when a save cannot happen. `Config.write()` serializes before
it opens the destination, and serializing validates, so a configuration it
refuses leaves the file on disk exactly as it was. A destination that cannot
be written at all — a folder that does not exist, a file that may not be
written to — is a message and not a crash, because falling over would cost
the user the whole session.
