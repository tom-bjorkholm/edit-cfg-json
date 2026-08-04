## Main entry points

Everything a user of this package needs is re-exported from the top-level
`{{import_name}}` package, so it can be imported directly:

````python
from {{import_name}} import ActionSettings, ConfigLoadError, Descriptions, \
    DumpEditor, EXPLANATION, EditModel, EditorBackend, Emphasis, ExitCode, \
    LOAD_REMARK, LoadPolicy, LoadReport, LoadedConfig, MEMBER_DIAGNOSTIC, \
    MEMBER_MARK, MemberRow, SaveOutcome, Settings, SettingsSource, \
    ValidationVerdict, add_file_options, default_config, docstring_text, \
    edit, load_config, load_text, model_as_text, model_title, named_policy, \
    row_description, row_diagnostic, row_marks, row_value_text, run_cli, \
    save_emphasis, save_text, verdict_emphasis, verdict_text
````

| Name | What it is |
| --- | --- |
| `edit` | The whole of an editing session in one call: read the input file, build the model, run a backend to completion, and give back the configuration object that was saved, or `None` when nothing was. The backend is a parameter because this package never imports a user interface library; each backend package also exports an `edit` of its own that supplies itself. |
| `EditModel` | The editable state of one `config_as_json.Config` object, discovered by looking at that object. Its members keep the order the configuration class declares them in, their values are held in JSON space, `set_text` writes the text of one edit field into one of them, `check_field` says whether the text of one member means a value of it at all, `validate` runs the application's own validation over the whole buffer, and `save` writes it to `out_file` if the application would accept it. |
| `MemberRow` | One configuration member of the model: the path that addresses it, the value it holds now, the value it started with, what is said about the member, how its text becomes a value, and the flags that say what has happened to it. |
| `Descriptions` | What the application says about the members it declares: a mapping from the absolute `config_as_json.ConfigPath` of a member to the text that explains it. It is the one type alias this library declares. |
| `ValidationVerdict` | What one validation pass found: whether the application itself would accept the buffer, what it said about each member it refused, and what it said that is about no single member. `EditModel.verdict` is the verdict of the last pass, or `None` while the buffer has not been validated since it last changed. |
| `SaveOutcome` | What one attempt to save did: whether the output file was written, and what to tell the user about it. `EditModel.save_message` is the message of the last attempt and `EditModel.save_outcome` is the attempt itself, which is how a backend knows whether it succeeded. |
| `load_config` | Reads the configuration to edit from one input file, or hands back the caller's own object when there is no file. It constructs the configuration class itself, because a load policy and the reporting of automatic changes are given to a constructor and to nothing else. |
| `LoadPolicy` | What to do about a declared value the input file does not hold: `STRICT`, `DEFAULTS`, or `STRICT_THEN_DEFAULTS`, which is the default. |
| `LoadedConfig` | What `load_config` returns: the object to edit, and the report of its load. |
| `LoadReport` | What one load did beyond reading the values: what the user has to be told, the names of the members the declared defaults supplied, and the names of the members whose value reading the file itself put there or altered. It is handed to `EditModel`, which marks both kinds. |
| `ConfigLoadError` | The refusal of an input file that cannot be opened, holding the message for the user and the diagnostics the configuration class produced. |
| `Settings` | What the application around the editor has already decided: the key combinations of its actions, and what a configuration file of that application is called. Every attribute has a default, so an application with no opinion passes nothing at all. |
| `ActionSettings` | The key combinations of every action of the editor, one attribute per action, so that an action the application says nothing about keeps its default. |
| `SettingsSource` | What every entry point takes: a `Settings`, or a callable that answers with one. |
| `EditorBackend` | The protocol a user interface implements. It is phrased against `EditModel`, so a backend can also be mounted by an application that runs its own event loop. |
| `DumpEditor` | The one backend this package ships, and the only one that needs no user interface library: it validates the buffer, prints the model and returns. It is what the `{{dist_name}}` program below runs, and it is the shortest thing there is to read for anybody writing a backend of their own. |
| `default_config` | One configuration object holding the declared defaults of a class, which is what `edit` and `EditModel` take. It is the door for a caller that has a class rather than an object, and it refuses a class the editor cannot construct in the same words that reading a file does. |
| `run_cli` | The whole command line of a ready-to-run program, given a backend. `ExitCode` is what it answers with, `add_file_options` adds the input, output and policy options to any other parser, and `named_policy` turns a `--policy` value into a `LoadPolicy`. |
| `model_as_text` | The plain text rendering of a whole model, used by the examples and by the tests so that the editor can be observed without a display. It begins with what the load did and ends with the validation state and the saving, so a rendering never leaves any of them unsaid. |
| `model_title` | The label of a whole model, marked while the buffer holds a change worth saving. Both backends show it, so neither of them decides on its own how an unsaved change looks. |
| `load_text` | What reading the input file did, as text, and nothing at all when it did nothing worth saying. Both backends show it, so the two of them cannot tell the user two different things about one file. |
| `docstring_text` | What the configuration class says about itself, as much of it as is being shown: the whole docstring while the explanations are shown, and its first paragraph while they are hidden. Both backends show it, so neither of them decides on its own how much of a docstring the user is offered. |
| `row_description` | What one member is for, as it is being shown: the description while the explanations are shown, and nothing while they are hidden. |
| `row_diagnostic` | What is wrong with one member, and nothing when nothing is known to be. Its text may mean no value of that member at all, which stays true until the member is edited again, or the application may have refused the value, which is only known for as long as the rest of the buffer stands still. |
| `row_marks` | The marks of one member: that the input file did not hold it, that reading the file put this value there or altered it, that the user changed it, and that a validation pass then rewrote what the user wrote. They can apply at once, except for the first two, of which the load sets the one that says more. |
| `row_value_text` | The value of one member as the text a field shows. A string is shown as the string itself, without the quotation marks that the file format puts around it. Both backends use it, so neither of them formats values itself. |
| `Emphasis` | Why a part of the editor stands out from the values: `MUTED` for text about them and for a state nothing has reached, `ATTENTION` for something that has happened to a member, `WARNING` for a remark about the input file, and `GOOD` and `BAD` for what the application accepted and refused. There is no member for ordinary text, because the values and their names are left alone. |
| `EXPLANATION`, `MEMBER_MARK`, `LOAD_REMARK`, `MEMBER_DIAGNOSTIC` | Which of those the explanatory text, the marks of a member, the message of the load and what is wrong with a member are. They are named here rather than in each backend, so that the two of them cannot colour one thing two ways. |
| `verdict_emphasis`, `save_emphasis` | Which of those the validation state and the saving are, as things stand now. These two depend on the state of the model, which is why they are functions and why they are here: they are the two a backend could otherwise get differently. |
| `verdict_text` | The validation state of a model as text: it names the members that were refused, because what was said about each of them is shown beside that member, and it carries below it whatever was said that is about no single member. |
| `save_text` | What saving did, or where it would write if it were asked, or that no file has been chosen at all. Those are three different states, and a user who cannot tell them apart cannot tell whether Save will ask them something. |

The package is under construction. This version reads a flat configuration
from a file, edits it, validates it and writes it. A member whose value is a
list or a dict is reported as a row that cannot be edited yet rather than
being left out.

## The {{dist_name}} program

Installing this package installs a program of the same name, and it needs no
display: it prints the configuration class you name, with what that class's own
validators make of the values, and with `--save` it writes the validated file.
So it is a configuration checker for a terminal or for a continuous integration
job as much as a way of looking at a class, and nobody has to write a line of
code to use it:

````sh
{{dist_name}} --module myapp.config AppConfig -i /etc/myapp.json
{{dist_name}} --module myapp.config AppConfig -i partial.json --save
````

The second of those writes the file the class itself would have written: what
the file left out is filled in from the declared defaults, and what a validator
rewrites is rewritten. `--save` exists only in this program of the three,
because a run that prints once and returns has no later moment at which a user
could press Save. Its two graphical relatives, `edit-cfg-json-tk` and
`edit-cfg-json-textual`, open an editor and give the user one instead.

{{include: program.md}}

## Reading the input file

`load_config` constructs the configuration class rather than taking an
already loaded object, because the two things a load has to be told are given
to a constructor and to nothing else: the policy for declared keys the file
does not hold, and the hook that reports the automatic changes of an old
format file. The hook is passed on only to a class that declares it, since
the constructor that `config_as_json` documents does not.

A value the file leaves out is filled in from the declared default of the
class, and that member is marked, so the user can see which values are not
the ones the file asked for. Which members those are is asked of the parse
itself and not of the keys of the file, because a class with rules for reading
an older file may have renamed a key of the file into a member, and a member
that came from the file under another name was not filled in from anything.

Every other way in which an input file can be wrong is a refusal with a
message of its own: a key the configuration does not declare, text that cannot
be read as configuration, values a validator refuses, and a file that cannot
be read at all.

### When reading the file changes it

Reading a file is not always only reading it, and the user has to be told, or
the editor looks broken: the values on the screen are then not the values in
the file, and saving writes the screen. It happens in three ways — the rules a
class declares for reading a file of an older format, a normalization that
parsing or validating does, and the declared defaults filling in what the file
left out — and one mechanism finds all three: the values the load produced are
written back to JSON and compared with the text of the file, key by key. That
needs nothing at all of the configuration class.

Every member whose value is not the one the file holds is marked, and a key of
the file that the configuration does not write back is named in the message,
because it is no member of this configuration and has no row to be marked.

A class whose `__init__` declares `auto_ch_hook` and hands it on adds one thing
that no comparison could find: the names of the older keys the file was read
with. A renamed key is simply gone from the file, and nothing in the file says
which member it became. A class that declares no hook is edited exactly as
well and the editor then reports what it can see for itself.

One thing to know if an application wants to read such a report of its own:
`Config.__init__` deep copies the hook it is given, so the object the
application passed is not the object the load fills in. A hook that only prints
does not notice; one that is read afterwards has to say that a copy of it is
itself.

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

## Saying which member is wrong

`Config.validate()` applies the validation plan in order and stops at the
first step that refuses, so the pass that decides the verdict can report one
failure and cannot say which member it was about. What it can say is enough,
because a validation plan is public: a `MemberValidationStep` names the
members it is about and holds the validator, and `validate_member` takes one
member and one value. So the plan is walked a second time, each member's own
validators are run, and what each of them said is put beside the member it is
about, which is what `row_diagnostic` gives a backend.

Two things follow, and both of them matter more than the attribution itself:

- **Every refused member is named at once**, because the second walk does not
  stop at the first refusal. The user corrects one round of mistakes rather
  than one mistake per round.
- **No validator class is recognised by type.** A `MemberValidator` subclass
  that an application wrote is attributed exactly as the ones `config_as_json`
  ships are, which is the same permanent decision that keeps this library from
  reading constraints out of validators at all.

A rule that is about no single member — a `WholeConfigValidator`, or a key
that does not match, or text that is not JSON — has no member to be put
beside, so it stays in `verdict_text` below the members. A rule of that kind
is also not applied while a member is refused, because `Config.validate()`
would have stopped at the member before it and an editor that reported it
anyway would be reporting something the application never did.

### What the text of a field means, before any of that

A member whose class declares a `parse_converters()` entry does not hold a
JSON space value at all once the configuration has it, an enum being the case
that arises in practice. That conversion is run for the member before any
candidate configuration is built, because a name that is no member of an enum
cannot be converted and `config_as_json` reports a failed conversion inside
the message it prints for JSON it could not load — which is right for a
program reading a file and wrong for a person editing a field.

The converter the class declared is *run* rather than looked at, so an
application that wrote a converter of its own gets the same treatment.

`EditModel.check_field` asks that question about one member, and it is what
both backends call when a field loses the focus. That is deliberately not
every change: the name of an enum member is no name of one for most of the
time it takes to type it, and a field that reported that would be reporting a
failure that is not one yet. It is a different question from the validation
of the whole configuration and it is kept apart from it — it needs no
candidate configuration, and its answer stays true until that one member is
edited again, whatever happens to the rest of the buffer.

## Explaining the values to the user

Two sources of explanatory text, independent of each other and both optional.
Neither of them is something the editor could invent, and one of them the
application does not have to pass at all:

- **The docstring of the configuration class** labels the configuration
  object. Nothing is passed for this; the class has it and the editor reads
  it. `cls.__doc__` and never `inspect.getdoc()`, so that a class without a
  docstring of its own is labelled with nothing rather than with the docstring
  of a base class.
- **A `Descriptions` mapping** labels the individual members, because a member
  has nothing of the kind at runtime: a string literal written after an
  assignment is discarded, and a PEP 526 annotation on an instance attribute
  is recorded nowhere.

````python
from {{import_name}} import Descriptions, edit

DESCRIPTIONS: Descriptions = {
    ('max_items',): 'How many items one report may hold, from 1 to 100.',
    ('limits', '['): 'What every one of these limits means.'}

saved = edit(config=config, backend=backend, descriptions=DESCRIPTIONS)
````

A member is named by the absolute `config_as_json.ConfigPath` that addresses
it, so a member inside a list, a dict or a nested configuration object needs
no second way of naming it. The `'['` step keeps its `config_as_json` meaning
of every list element or every dictionary value at that point, and two
selectors that both address one member are resolved in favour of the more
specific one. A selector that addresses no member at all is never used and is
never an error: a wrong description is a cosmetic mistake, and refusing to
open the editor over one would be a much larger one. So is a member the
mapping says nothing about, which is shown without a description.

The explanations take a line per member, and a user who knows this
configuration by heart does not want them, so they can be hidden:
`EditModel.explanations_shown` says whether they are, and
`EditModel.toggle_explanations` is what the `explain` action of both backends
calls. What stays visible either way is `EditModel.summary`, the first
paragraph of the class docstring, because one line for the whole configuration
is worth keeping. That state belongs to the model rather than to a backend, so
that an application cannot end up with two user interfaces that disagree about
whether they are explaining themselves.

### Telling the kinds of text apart

Once the explanations are on the screen, most of what is on it is not the
values, and a user who has to read all of it to find the one line that matters
is reading too much. `Emphasis` is what the core says about that, and each
backend maps it to what its own toolkit understands: Textual to the colours of
the terminal's theme, which follow it into a dark mode, and Tkinter to colour
values.

| Shown | Emphasis | Why |
| --- | --- | --- |
| a value, a member name | none | what the user came to change, and the most legible thing there because nothing was done to it |
| the class docstring, a description | `MUTED` | text about the values rather than the values |
| the marks of a member | `ATTENTION` | the file did not hold it, the user changed it, or a validator changed what the user wrote |
| what is wrong with a member | `BAD` | it sits below the description of the same member, and it is the one of the two that has to be acted on |
| what reading the input file did | `WARNING` | a load that says anything is saying the file was not quite what was asked for |
| a validation or a save that has not been asked for | `MUTED` | a state nothing has reached is not a state to read first |
| an accepted buffer, a written file | `GOOD` | |
| a refused buffer, a refused save | `BAD` | |

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
backends ask the user for one. What the file is called is the application's
business and not this library's: it has no opinion of its own about the
extension, and follows the one the application states in its `Settings`.

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

## What the application has already decided

The editor runs inside an application that took some key combinations for
itself long before the editor was called, and that knows what one of its own
configuration files is called. `Settings` is where the application says so,
and `edit`, `load_config` and `EditModel` each take one. Every attribute has
a default, so an application with no opinion passes nothing at all and gets
what the editor would have chosen anyway.

````python
from {{import_name}} import ActionSettings, Settings, edit

saved = edit(config=config, backend=backend, in_file='my_config.cfg',
             settings=Settings(actions=ActionSettings(save=('ctrl+w',)),
                               file_extension='.cfg',
                               extension_enforced=True))
````

`ActionSettings` has one attribute per action of the editor — `quit`,
`validate`, `save`, `save_as`, `cancel` and `explain` — and each of them holds
every combination that runs that action. The first is the one a footer or a menu
names and the rest work without being named. An empty tuple takes the key
away and not the action, which is still reachable through a button or a
command palette. Combinations are written in Textual's key names, in lower
case, and the Tkinter backend translates them into the notation of its own
toolkit. One combination given to two actions is refused where the `Settings`
is built, because only one of the two could ever run.

`file_extension` is `None` by default, which is no opinion. With a value, and
without `extension_enforced`, the extension is added to a destination that is
being chosen and has none of its own, and nothing is ever refused. With
`extension_enforced`, a file that has another extension is refused as well:
`load_config` raises `ConfigLoadError` for an input file, and a save is
refused with the message that says why.

A destination is completed only when it is *chosen* — the Save as answer,
`EditModel.set_out_file`, or an `out_file` named in the `edit` call. The
input file is never completed, whether it is being read or being written back
to as the destination `out_file` fell back to, because reading one file while
writing another would be a surprise.

Every one of these entry points also accepts a callable that answers with a
`Settings`, which is `SettingsSource`. It is asked again at each point where
the answer is used. What that can change is worth knowing exactly: the key
combinations are read once, when a backend builds its bindings, and the file
name settings are read at every save and at every choice of a destination.
The gain that matters is neither of those, but that an application need not
have its settings ready at the moment it calls.
