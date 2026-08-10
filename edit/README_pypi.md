# edit-cfg-json

There are 3 related packages for editing a `config-as-json`
configuration:

- **[edit-cfg-json-tk](https://pypi.org/project/edit-cfg-json-tk/)** a
  desktop editor based on Tkinter. It is a thin backend on top of the
  core.

- **[edit-cfg-json-textual](https://pypi.org/project/edit-cfg-json-textual/)**
  a terminal editor based on Textual. It is a thin backend on top of the
  core.

- **[edit-cfg-json](https://pypi.org/project/edit-cfg-json/)** the user
  interface agnostic core. It discovers the editable structure of a
  `config_as_json.Config` object by introspection, and owns all editing,
  validation and file handling. It is also the package a third party
  writes a new user interface backend against. The only backend it ships
  itself is a very limited non-interactive one that prints the model once
  and returns, for a script, a test or a continuous integration job.

The application supplies its own `Config` object and gets a folding
editor for it, without writing any user interface code and without
describing its configuration schema a second time.

The three packages share a version number and are released together. The
first two are the editors: pick the one that matches how your application
is used, and it pulls in the core itself.

## Project status

**Alpha. No API stability and no backward compatibility is offered while
this package is in Alpha.** That applies to the core and to both
backends. Public names may change without a major version bump.

Semantic versioning starts when the Alpha period ends. Until then, pin an
exact version if your build needs to be reproducible.

## What this package does

`edit-cfg-json` is the user interface agnostic core. It holds everything
that is not a widget:

- discovery of the editable structure of a `config_as_json.Config` object
  by introspection, so the application does not describe its schema twice:
  its members, the values inside its lists and dicts, and the nested
  configuration objects that own a region of the tree
- the edit buffer, its per-field state, the tree of rows, the fold structure,
  and what a node offers about how many elements it holds
- validation, by applying the buffer to a copy of the configuration object and
  running the application's own validators rather than by inspecting them
- loading, including making automatic changes to an old format file
  visible to the user, and saving, including what becomes of the file that a
  save writes over

This package has the utility  `python3 -m edit_cfg_json.dump` that
runs non-interactively on top of the backend API.

Install this package on its own if you are writing a new user interface
backend. If you want an editor, install one of the backends instead; they
pull this package in.

## Main entry points

Everything a user of this package needs is re-exported from the top-level
`edit_cfg_json` package, so it can be imported directly:

````python
from edit_cfg_json import ActionSettings, ConfigLoadError, ConfigLoader, \
    Descriptions, DumpEditor, EXPLANATION, EditModel, EditorBackend, \
    ElementOffer, Emphasis, ExitCode, LOAD_REMARK, LoadPolicy, LoadReport, \
    LoadedConfig, MEMBER_DIAGNOSTIC, MEMBER_MARK, MemberRow, SaveOutcome, \
    Settings, SettingsSource, ValidationVerdict, add_file_options, can_fold, \
    close_question, default_config, derived_loader, docstring_text, edit, \
    fold_hides, load_config, load_text, model_as_text, model_title, \
    named_policy, overwrite_question, path_text, row_describes, \
    row_description, row_diagnostic, row_fold_text, row_marks, \
    row_subtree_text, row_validates, row_value_text, run_cli, save_emphasis, \
    save_text, subtree_emphasis, text_path, verdict_emphasis, verdict_text
````

| Name | What it is |
| --- | --- |
| `edit` | The whole of an editing session in one call: read the input file, build the model, run a backend to completion, and give back the configuration object that was saved, or `None` when nothing was. The backend is a parameter because this package never imports a user interface library; each backend package also exports an `edit` of its own that supplies itself. |
| `EditModel` | The editable state of one `config_as_json.Config` object, discovered by looking at that object. Its rows are the tree of that configuration, `set_text` writes the text of one edit field into one of them, `check_field` says whether the text of one member means a value of it at all, `toggle_fold` and `toggle_fold_all` decide how much of the tree is on the screen, `add_element`, `remove_element` and `move_element` change how many things a member holds, `validate` runs the application's own validation over the whole buffer, and `save` writes it to `out_file` if the application would accept it. |
| `MemberRow` | One node of that tree: the path that addresses it, the value it holds now, the value it started with, how far inside the configuration it is, which paths are inside it, whether it is folded and whether it is shown, the class of the configuration object at it, what is said about it, how its text becomes a value, what it offers about its own elements, and the flags that say what has happened to it. |
| `Descriptions` | What the application says about the members it declares: a mapping from the absolute `config_as_json.ConfigPath` of a member to the text that explains it. It is the one type alias this library declares. |
| `path_text`, `text_path` | One path written with a dot between its steps, and back again. A user interface that has to name a node in one string — a message, an option of a command line — writes it this way, so that two of them cannot write it differently. |
| `can_fold`, `fold_hides` | Whether this configuration has anything to fold at all, and what the next press of the fold action will do. A backend offers no action and no key where there is nothing to fold, and names the action for what pressing it does next. |
| `row_fold_text` | What says that one container is folded, for a rendering that has no control to draw. |
| `ElementOffer` | What one node offers to do about the elements it holds: whether one can be added, whether adding needs a key that only the user can give, whether this one can be removed, whether it can change places with either neighbour, and why nothing can be added where nothing can. `MemberRow.offer` is where a backend reads it, and the core works it out once so that the two backends cannot offer different things. |
| `row_validates`, `row_subtree_text`, `subtree_emphasis` | Whether a node can ever say what the configuration objects at or inside it amount to, what it says, and how that stands out. A nested object says that it is valid *on its own*, which is not the verdict of the whole configuration and must not be read as one; a list or a dict of such objects says what the objects in it amount to, because its row is the only one a fold leaves on the screen. |
| `ValidationVerdict` | What one validation pass found: whether the application itself would accept the buffer, what it said about each node it refused, addressed by path, and what it said that is about no single node. `EditModel.verdict` is the verdict of the last pass, or `None` while the buffer has not been validated since it last changed. |
| `SaveOutcome` | What one attempt to save did: whether the output file was written, and what to tell the user about it. `EditModel.save_message` is the message of the last attempt and `EditModel.save_outcome` is the attempt itself, which is how a backend knows whether it succeeded. |
| `load_config` | Reads the configuration to edit from one input file, or hands back the caller's own object when there is no file. It reads the file itself and applies it under the load policy that was asked for, rather than taking an already loaded object, because which policy applies is decided while the file is read. |
| `LoadPolicy` | What to do about a declared value the input file does not hold: `STRICT`, `DEFAULTS`, or `STRICT_THEN_DEFAULTS`, which is the default. |
| `LoadedConfig` | What `load_config` returns: the object to edit, and the report of its load. |
| `LoadReport` | What one load did beyond reading the values: what the user has to be told, which members the declared defaults supplied, and which members had their value put there or altered by the reading of the file. It is handed to `EditModel`, which marks both kinds. |
| `ConfigLoadError` | The refusal of an input file that cannot be opened, holding the message for the user and the diagnostics the configuration class produced. |
| `ConfigLoader`, `derived_loader` | How an application says how its own configuration class is built, for a class this library cannot construct on its own, and the one line that says it for a class plus an argument bound into it. |
| `Settings` | What the application around the editor has already decided: the key combinations of its actions, what a configuration file of that application is called, and what becomes of a file that a save writes over. Every attribute has a default, so an application with no opinion passes nothing at all. |
| `ActionSettings` | The key combinations of every action of the editor, one attribute per action, so that an action the application says nothing about keeps its default. |
| `SettingsSource` | What every entry point takes: a `Settings`, or a callable that answers with one. |
| `EditorBackend` | The protocol a user interface implements. It is phrased against `EditModel` rather than against `edit`, which is what makes an editor that an application mounts in its own window an addition to this package rather than a rewrite of it. |
| `DumpEditor` | A very limited non-interactive backend, and the one this package can ship because it needs no user interface library: it validates the buffer, prints the model once and returns. It is not an editor — there is no field to type into, no control to press and nobody to answer a question — and it is good for two things: exercising this API with no display, which is what a script and an automated test need, and printing what a short sequence of editor actions left behind. It is also the shortest backend there is to read for anybody writing one of their own. The editors are `edit-cfg-json-tk` and `edit-cfg-json-textual`. |
| `default_config` | One configuration object holding the declared defaults of a class, which is what `edit` and `EditModel` take. It is the door for a caller that has a class rather than an object, and it refuses a class the editor cannot construct in the same words that reading a file does. |
| `run_cli`, `ExitCode` | The whole command line of a ready-to-run program, given a backend, and the numbers it answers with. `add_file_options` adds the input, output and policy options to any other parser, and `named_policy` turns a `--policy` value into a `LoadPolicy`. |
| `model_as_text` | The plain text rendering of a whole model, used by the examples and by the tests so that what the model holds can be checked without a display. It begins with what the load did, shows the tree as it stands with the folded containers folded, and ends with the validation state and the saving, so a rendering never leaves any of them unsaid. What it cannot render is anything a user reaches for — a field with the focus in it, a control, a question — so it checks the core rather than standing in for an editor. |
| `model_title` | The label of a whole model, marked while the buffer holds a change worth saving. Both backends show it, so neither of them decides on its own how an unsaved change looks. |
| `load_text` | What reading the input file did, as text, and nothing at all when it did nothing worth saying. Both backends show it, so the two of them cannot tell the user two different things about one file. |
| `docstring_text` | What the configuration class says about itself, as much of it as is being shown: the whole docstring while the explanations are shown, and its first paragraph while they are hidden. Both backends show it, so neither of them decides on its own how much of a docstring the user is offered. |
| `row_describes`, `row_description` | Whether anything can ever appear below one node, which is what a backend asks before it creates the widget at all, and what appears there now: the description of that member, what kind of value it holds, and why its elements cannot be added to. What a nested object says about itself changes when it is folded, so a backend writes this again on every fold and not only when the explain toggle is pressed. |
| `row_diagnostic` | What is wrong with one node, and nothing when nothing is known to be. Its text may mean no value of that member at all, which stays true until the member is edited again; the application may have refused the value, which is only known for as long as the rest of the buffer stands still; or the nested object that owns it may have refused it when it was asked about itself, which is taken back by an edit anywhere inside that object. |
| `row_marks` | The marks of one node: that the input file did not hold it, that reading the file put this value there or altered it, that the user changed it, and that a validation pass then rewrote what the user wrote. They can apply at once, except for the first two, of which the load sets the one that says more. |
| `row_value_text` | The value of one node as the text a field shows. A string is shown as the string itself, without the quotation marks that the file format puts around it. A node that holds no value of its own says what it is instead — how many things a container holds, or which class the object at it is. Both backends use it, so neither of them formats values itself. |
| `Emphasis` | Why a part of the editor stands out from the values: `MUTED` for text about them and for a state nothing has reached, `ATTENTION` for something that has happened to a member, `WARNING` for a remark about the input file, and `GOOD` and `BAD` for what the application accepted and refused. There is no member for ordinary text, because the values and their names are left alone. |
| `EXPLANATION`, `MEMBER_MARK`, `LOAD_REMARK`, `MEMBER_DIAGNOSTIC` | Which of those the explanatory text, the marks of a member, the message of the load and what is wrong with a member are. They are named here rather than in each backend, so that the two of them cannot colour one thing two ways. |
| `verdict_emphasis`, `save_emphasis` | Which of those the validation state and the saving are, as things stand now. These depend on the state of the model, which is why they are functions and why they are here: they are the ones a backend could otherwise get differently. |
| `verdict_text` | The validation state of a model as text: it names the nodes that were refused, by the whole path to each of them, because what was said about each is shown beside that node, and it carries below it whatever was said that is about no single node. |
| `save_text` | What saving did, or where it would write if it were asked, or that no file has been chosen at all. Those are three different states, and a user who cannot tell them apart cannot tell whether Save will ask them something. |
| `close_question`, `overwrite_question` | What to ask the user before closing an editor that holds something unsaved, and before a save writes over a file this session did not write — and nothing at all when there is nothing to ask about. Whether the user is asked belongs here so that two user interfaces of one application cannot disagree about whether they warn; how the question is put belongs to each backend. |

This package installs no program: the editors are `edit-cfg-json-tk` and
`edit-cfg-json-textual`, and `python3 -m edit_cfg_json.dump --help` is a small
utility for whoever is writing a program on top of this one, printing what a
class makes of a file and answering with an exit code.

## The configuration as a tree of rows

A configuration worth editing is not a handful of scalars. A member may hold a
list, a dict, a nested `config_as_json.Config` object, a list of such objects
or a dict of them, and the model is one tree over all of it.

- **A member is a row**, and the members are in the order the configuration
  class declares them, which is the order the class was written in rather than
  the sorted order of the keys of a file.
- **Every value inside a container is a row of its own**, indented once for
  each container it is inside, with a field at every value. The container row
  has no field, because it has no value of its own: it says how many things it
  holds instead. What it holds is shown in the order the file has it, which is
  the order of a list and the sorted order of the keys of a dict.
- **A nested configuration object is a node**, not the dict it serializes to:
  its row says its class, its own docstring is below it, its members are the
  rows under that in the order *its* class declares them, and the parse
  converters and the optional members of that class are what apply inside it.
- **Every node is addressed by the absolute `config_as_json.ConfigPath` to
  it**, so a value inside a list, a dict or a nested object needs no second way
  of naming it. An element of a list is addressed by its index written out, so
  the second element of `retry_delays` is `('retry_delays', '1')`.

**A node that holds rows can be folded away and opened again**, and which of
them are folded belongs to the model, so that two user interfaces of one
application cannot be folded differently. Each container has a control on its
own row, and one action folds or opens all of them at once. A container starts
open unless opening it would flood the window, counting everything inside it
and not only its direct children — which a list of configuration objects
reaches at very few of them, because every object brings its own members with
it. A configuration with nothing to fold is offered no action and no key at
all.

**Folding a node asks every configuration object at or inside it about
itself**, and so does opening one, because changing how much of a node is shown
is the moment the user is looking at it.

## What one nested object is on its own

A nested configuration object can be validated in isolation, by applying the
part of the buffer it owns to that object. The answer is a badge on its row
saying *valid on its own* or *refused on its own*, and the qualifying words are
the whole point: a rule of the class above may relate two objects across the
boundary between them and refuse the configuration while saying nothing against
either object. Whether the file can be written is the verdict of the whole
configuration and nothing else.

A member of the object that was refused says so below itself, exactly as a
member refused by a pass over the whole buffer does. What the object refused
about no member of itself is said at the object, because that is what it is
about.

A list or a dict of such objects carries the same three states about them —
*valid inside*, *refused inside*, and nothing until they have been asked —
because its row is the only one that folding leaves on the screen. A user who
folds a member to get it out of the way is not asking to be told that
everything in it is fine, and is very much asking to be told that it is not.

An answer is taken back as soon as anything inside that one object is edited,
which is a different lifetime from the verdict of the whole configuration: that
one is dropped by an edit anywhere.

## How many things a member holds

A member is a list or a dict because **how many** of them there are is a
decision of whoever configures the application, so a container can be given an
element, one of its elements can be taken out, and an element of a list can
change places with a neighbour. `MemberRow.offer` says which of those one node
allows, and a backend creates a control for each.

**A new element is copied and never invented**, and there are exactly two
places it can be copied from, both of them the application's. Where the class
declares that every element of a list or every value of a dict is a
configuration object, the declaration names the class and a new element is one
object of it holding the values it declares — which works while the container
is still empty. Where it declares no such thing, the values the class declares
for the member itself are the pattern, and failing that the first element the
member holds now.

**What cannot be done is said and not left to be discovered.** A member with
nothing to copy from says so below itself and offers removing and moving; so do
the three kinds of dict that cannot gain an entry, each for a reason of its
own. An ordinary dict member is the one worth knowing about: `config_as_json`
matches such a member against the keys its class declares, so a dict that
gained or lost one would be refused by the configuration class itself. That
sentence is explanation rather than something to act on, so it is
`Emphasis.MUTED`, it sits below the member with the description, and the
explanations toggle covers it. Nothing is half-supported: a node that cannot be
given an element gets no control at all rather than one that refuses every
press.

**Where a new entry of a dict is named is the user**, because nothing else
knows. Each backend asks in the way its own toolkit asks a question, and a key
the dict already holds is asked about again rather than allowed to take the
place of what is there. A list is never asked, because an element of a list is
addressed by where it is.

A declared optional member that holds no configuration object is grown by being
given one and cleared by being put back to holding none, which is the same
offer under another name. Clearing is offered only where the class writes
`null` for such a member: one that leaves it out of the file altogether has no
row at all while it holds nothing, so a member the editor had cleared could
never be given an object again.

## Reading the input file

`load_config` reads the input file itself and applies it to the configuration
class, rather than taking an already loaded object, because the policy for
declared keys the file does not hold is decided while the file is read. It also
needs the text of the file for the comparison below, and it will not let a
missing file end the process, which is what `config_as_json.Config.read` would
do.

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

### A class this editor cannot construct on its own

Most configuration classes take the keyword arguments that `config_as_json`
documents and nothing else, and this library constructs them from the signature
it reads. A class that needs an argument of the application's own — a folder, a
connection, the list of names its own validators accept — is told to `edit` and
`load_config` as a `ConfigLoader` instead, and `derived_loader` is what an
application needs for it in one line:

````python
from functools import partial
from edit_cfg_json import derived_loader, edit

loader = derived_loader(partial(AppConfig, known_teams=TEAMS))
saved = edit(config=AppConfig(known_teams=TEAMS), backend=backend,
             loader=loader, in_file='my_config.cfg')
````

**Reading a file is very nearly the only thing a loader is needed for.**
Editing, validating and saving apply the buffer to a copy of the object the
load produced, with the `Config.parse_json` that every configuration class has,
so they need nothing of its constructor. The one other thing a loader answers
is what the class declares for a member, which is where a new element of an
ordinary list is copied from; a class the editor cannot construct loses that
one offer and nothing else.

Writing the four keyword arguments of the protocol out by hand is the door for
what that cannot express, which in practice means a class chosen by looking at
the JSON. Two rules make that work: a loader answers a call with no JSON source
with the class it uses for a configuration that does not exist yet, and the
class is chosen when the file is loaded, so the session then edits that class.
A save asks the loader once more whether the file it is about to write would
still be read as that class, and refuses to write one that would not.

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

What the load recorded says *why*, which no comparison could find: a renamed
key is simply gone from the file, and nothing in the file says which member it
became. `Config.auto_change_hook()` is the hook of the most recent parse, every
configuration object has one whether the application named it or not, and a
record that produced a member of this configuration is shown at that member —
so its mark says which older key the value was read from rather than only that
something happened to it. A class that declares `auto_ch_hook` and hands it on
is reported on exactly as fully as one that does not, and this library passes
no hook anywhere.

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
pass writes the buffer as JSON, applies it to a copy of the configuration
object of the session, and reports what the class says. There is no second
implementation of validation anywhere, so a validator that an application
writes for itself works here without this package knowing anything about it.

A validation pass is not read only. A member validator returns the value
that is stored back into the member, so a validator such as one that changes
the case of a string rewrites what the user typed. The buffer is refreshed
from the configuration object that was accepted, and every value the pass
rewrote is marked, because changing what the user just typed without showing
it would be the worst of the available behaviours. A pass can also change how
many rows there are — a validator that sorts a list and removes its duplicates
removes a row — so the rows are built again from the values the pass accepted,
carrying over what each row that is still there knew.

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

What a member validator refused is about the whole member, because the whole
member is what it was given, so it is shown at the member and never at one
value inside it. An editor that guessed which value inside a list the validator
meant would be inventing.

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
application that wrote a converter of its own gets the same treatment. Which
class the converter is asked of follows the ownership of the tree, so a member
inside a nested object is converted by the class that owns it.

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
  object, and the docstring of each nested class labels that object. Nothing is
  passed for this; the class has it and the editor reads it. `cls.__doc__` and
  never `inspect.getdoc()`, so that a class without a docstring of its own is
  labelled with nothing rather than with the docstring of a base class.
- **A `Descriptions` mapping** labels the individual members, because a member
  has nothing of the kind at runtime: a string literal written after an
  assignment is discarded, and a PEP 526 annotation on an instance attribute
  is recorded nowhere.

````python
from edit_cfg_json import Descriptions, edit

DESCRIPTIONS: Descriptions = {
    ('max_items',): 'How many items one report may hold, from 1 to 100.',
    ('limits', '['): 'What every one of these limits means.',
    ('outputs', '[', 'parts', '[', 'width'): 'Width of one part, in columns.'}

saved = edit(config=config, backend=backend, descriptions=DESCRIPTIONS)
````

**Every member says what kind of value it holds**, whether the application
describes it or not: text, a whole number, a number, or true or false, and
whether the class may leave it out of the file. That is read from the value the
member holds and needs no mapping, and where a member holds an enum the names it
accepts are said instead, because they say the same thing better. What lives
inside a validator — a range, a set of allowed values — is not read and never
will be, so a limit is explained by the application in words or not at all.

A member is named by the absolute `config_as_json.ConfigPath` that addresses
it, so a member inside a list, a dict or a nested configuration object needs
no second way of naming it. The `'['` step keeps its `config_as_json` meaning
of every list element or every dictionary value at that point, and it says
`'['` at each step it has to, so one line reaches that member of every object
at any index and any key however deep the shape goes. Unlike a serialize
converter, a description path crosses the boundary of a nested object, because
an application should not have to know where the nesting boundaries fall.

Two selectors that both address one member are resolved in favour of the more
specific one: a step that names a key beats the `'['` step, and an earlier step
decides before a later one. So one element of a repeated object can be singled
out while every other keeps the general text. A selector that addresses no
member at all is never used and is never an error: a wrong description is a
cosmetic mistake, and refusing to open the editor over one would be a much
larger one. So is a member the mapping says nothing about, which is shown
without a description.

The explanations take a line per member, and a user who knows this
configuration by heart does not want them, so they can be hidden:
`EditModel.explanations_shown` says whether they are, and
`EditModel.toggle_explanations` is what the `explain` action of both backends
calls. What stays visible either way is `EditModel.summary`, the first
paragraph of the class docstring, because one line for the whole configuration
is worth keeping. A nested object shows the whole of its own docstring while it
is open and the first paragraph of it while it is folded, because an object
showing less of itself says less about itself. That state belongs to the model
rather than to a backend, so that an application cannot end up with two user
interfaces that disagree about whether they are explaining themselves.

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
| the class docstring, a description, why a member cannot be added to | `MUTED` | text about the values rather than the values |
| the marks of a member | `ATTENTION` | the file did not hold it, the user changed it, or a validator changed what the user wrote |
| what is wrong with a member | `BAD` | it sits below the description of the same member, and it is the one of the two that has to be acted on |
| what reading the input file did | `WARNING` | a load that says anything is saying the file was not quite what was asked for |
| a validation, a save or a nested object that has not been asked | `MUTED` | a state nothing has reached is not a state to read first |
| an accepted buffer, a written file, an object valid on its own | `GOOD` | |
| a refused buffer, a refused save, an object refused on its own | `BAD` | |

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

### The file a save writes over

A save writes over whatever the destination holds, and what it holds is a
configuration somebody wrote. It may be the one this session read a minute ago,
and it may be one another person wrote on another day; nothing the editor can
look at tells those apart. So the previous content is **kept** before it is
overwritten, by renaming, under the destination name plus `backup_suffix` —
`xx.cfg` becomes `xx.cfg.bak` — and `backup_count` above one numbers them from
`_1`, which is the file overwritten last, each save moving every one of them
one number further back until the oldest falls off the end.

It happens **once per destination per session**, which is what makes it about
the user's own work: from the second press of Save onwards the file being
written over is the first save of the same session, and keeping that would push
the configuration that was really there one number further from being found.
Save-as onto some other existing file is a different file and is kept again.

The keeping is after the validation and immediately before the write, so a save
that is refused for any reason keeps nothing, and a save that kept the previous
content and then could not write says where that content is. A save that cannot
keep it writes nothing at all: overwriting cannot be undone, so the moment at
which that is found is the last moment at which anything can be done about it.

`EditModel.overwritten_file` is the file a save would write over, and
`overwrite_question` is what to ask about it, and nothing at all where the
application asked for no question or where there is nothing to ask about. Each
backend puts the question in a dialog or on a modal screen, with the answer
that leaves the file alone offered first.

## Closing with something unsaved

Closing writes nothing, so a session closed with something in the buffer that
has not reached the file loses it. The editor is the only thing that knows
there is anything to lose, so it asks first: `close_question` is the question,
and nothing at all when there is nothing to ask about, because a save moves the
values the buffer is compared with and a session that saved and typed nothing
since has nothing to lose.

Whether the user is asked is the core's for the same reason as everything else
here — two user interfaces of one application, one of which asked and one of
which did not, would be worse than either behaviour — and how the question is
put belongs to each backend. Both offer the answer that keeps the changes
first, and route the button, the key and the close button of the window through
one place, because a way out that dropped the changes without a word would be
the one thing an editor must not do.

There are two answers and not three. Saving on the way out would have to cope
with a save the application refuses, with no destination chosen yet, and with
the Save-as question opening from inside a confirmation, and all three of those
belong to saving rather than to closing.

## What the application has already decided

The editor runs inside an application that took some key combinations for
itself long before the editor was called, that knows what one of its own
configuration files is called, and that has decided how those files are looked
after. `Settings` is where the application says so, and `edit`, `load_config`
and `EditModel` each take one. Every attribute has a default, so an application
with no opinion passes nothing at all and gets what the editor would have
chosen anyway.

````python
from edit_cfg_json import ActionSettings, Settings, edit

saved = edit(config=config, backend=backend, in_file='my_config.cfg',
             settings=Settings(actions=ActionSettings(save=('ctrl+w',)),
                               file_extension='.cfg',
                               extension_enforced=True,
                               backup_suffix='.old',
                               backup_count=3))
````

`ActionSettings` has one attribute per action of the editor — `quit`,
`validate`, `save`, `save_as`, `cancel`, `explain` and `fold` — and each of them
holds every combination that runs that action. The first is the one a footer or
a menu names and the rest work without being named. An empty tuple takes the key
away and not the action, which is still reachable through a button or a
command palette. Combinations are written in Textual's key names, in lower
case, and the Tkinter backend translates them into the notation of its own
toolkit. One combination given to two actions is refused where the `Settings`
is built, because only one of the two could ever run. `ctrl+f` and `f3` are
taken by no default of this editor, because a search over a configuration too
big for the window is something this editor is likely to be asked for and no
version number protects a key a user has learnt.

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

`backup_suffix`, `backup_count` and `confirm_overwrite` are what the
application says about the file a save writes over. `None` for the suffix keeps
nothing, and `confirm_overwrite` is `True` by default, which is the way a
default about something that cannot be undone should lean.

Every one of these entry points also accepts a callable that answers with a
`Settings`, which is `SettingsSource`. It is asked again at each point where
the answer is used. What that can change is worth knowing exactly: the key
combinations are read once, when a backend builds its bindings, and the file
name settings are read at every save and at every choice of a destination.
The gain that matters is neither of those, but that an application need not
have its settings ready at the moment it calls.

## Installing edit-cfg-json

### On macOS and Linux

To install edit-cfg-json on macOS and Linux, run the following command:

````sh
pip3 install --upgrade edit-cfg-json
````

### On Microsoft Windows

To install edit-cfg-json on Microsoft Windows, run the following command:

````sh
pip install --upgrade edit-cfg-json
````

## Documentation

- Design and decisions:
  [doc/design.md](https://github.com/tom-bjorkholm/edit-cfg-json/blob/master/doc/design.md)

- Public API:
  [edit-cfg-json](https://github.com/tom-bjorkholm/edit-cfg-json/blob/master/doc/edit-cfg-json_api.md),
  [edit-cfg-json-tk](https://github.com/tom-bjorkholm/edit-cfg-json/blob/master/doc/edit-cfg-json-tk_api.md),
  [edit-cfg-json-textual](https://github.com/tom-bjorkholm/edit-cfg-json/blob/master/doc/edit-cfg-json-textual_api.md)

- Protected API:
  [edit-cfg-json](https://github.com/tom-bjorkholm/edit-cfg-json/blob/master/doc/edit-cfg-json_protected_api.md),
  [edit-cfg-json-tk](https://github.com/tom-bjorkholm/edit-cfg-json/blob/master/doc/edit-cfg-json-tk_protected_api.md),
  [edit-cfg-json-textual](https://github.com/tom-bjorkholm/edit-cfg-json/blob/master/doc/edit-cfg-json-textual_protected_api.md)

- Worked examples:
  [examples/src/example](https://github.com/tom-bjorkholm/edit-cfg-json/blob/master/examples/src/example)

## License

edit-cfg-json is released under the MIT License. See the `LICENSE.txt`
file included in the distribution.

## Test summary

- Test result: 1465 passed, 3 deselected in 38s
- No flake8 warnings.
- No mypy errors found.
- No pylint warnings.
- No python layout warnings.
- Built version(s): 0.0.2
- Build and test using Python 3.14.6
