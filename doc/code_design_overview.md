# Code design overview

For a maintainer who is new to this code. It says which file to open and why
the code is split the way it is. The reasoning behind every decision is in
[doc/detailed_design.md](detailed_design.md); this is the map, not the terrain.

## 1. Three packages

| Folder | Import name | Holds |
| --- | --- | --- |
| [edit/](../edit/) | `edit_cfg_json` | the whole editor except user interface code |
| [edit_tk/](../edit_tk/) | `edit_cfg_json_tk` | the Tkinter editor |
| [edit_textual/](../edit_textual/) | `edit_cfg_json_textual` | the Textual editor |

The core imports no user interface library, and the backends are thin: when
the Tk and Textual trees start to look alike, the fix is to move the shared
logic into the core, not to suppress the duplicate-code warning. Both rules
are tested, in
[edit/test/test_edit_cfg_json/test_architecture.py](../edit/test/test_edit_cfg_json/test_architecture.py):
the core imports with `tkinter` and `textual` made unavailable, and the
backends use only the public API of the core.

The core is what this document is about. In the backends, the file names say
what they are: `*_editor.py` runs a window, `*_panel.py` builds the rows,
`*_look.py` holds the colours, `*_ask.py` asks the four questions, and
`textual_words.py` holds that backend's own wording.

## 2. Patterns

- **Model and backend, separated by a `Protocol`.**
  [EditModel](../edit/src/edit_cfg_json/edit_model.py) holds all state, does
  no input or output in its constructor and owns no event loop.
  [EditorBackend](../edit/src/edit_cfg_json/backend.py) is a
  `typing.Protocol` of one method, phrased against the model. That is what
  lets the same model either run in a window of its own or be mounted in one
  the application already has.

- **Paths address everything.** Every node of a configuration is a
  `config_as_json.ConfigPath`. Rows, descriptions, declared types, verdicts,
  marks and fold state are all mappings keyed by that path, which is how
  modules that know nothing of each other talk about the same node.

- **Operations answer with a `NamedTuple`.** Twenty-five of them
  (`LoadReport`, `ValidationVerdict`, `SaveOutcome`, `FindReport`,
  `ElementOffer`, `TreeFacts`, ...). The classes that hold editing state
  are three: `EditModel`, `EditBuffer` and `SaveState`.

- **Functions, not class hierarchies.** Most modules are module-level
  functions over a `Config` or over the buffer. Look for a function named
  after your question before looking for a class.

- **Run the real thing; never introspect it.** Validators are run, parse
  converters are run, the buffer is applied through the class's own
  `parse_json`. No schema is ever reconstructed by reading validator classes.

- **Incompleteness degrades, it does not fail.** What cannot be inferred
  becomes a free-text field and an on-demand validation. That is what makes
  the previous point affordable.

- **A nested `Config` object segments the tree.** Fold boundary, validation
  boundary and serialization boundary are the same line.

- **The caller's `Config` is never mutated.** The model works on a copy.

- **Facade.** [__init__.py](../edit/src/edit_cfg_json/__init__.py) re-exports
  the whole public API, so no user of the library imports an internal module.

## 3. Layers

A module imports from its own layer or from one below it, never from one
above. There are no cycles.

| Layer | Modules |
| --- | --- |
| Entry points | `cli`, `cli_target`, `dump`, `editing` |
| Rendering | `model_text`, `emphasis`, `backend` |
| The session | `edit_model` |
| The edit buffer | `buffer` |
| Operations | `rows`, `finding`, `elements`, `placing`, `validation`, `loading`, `auto_change`, `saving`, `settings_file` |
| Facts about one `Config` | `descriptions`, `member_types`, `converting`, `settings_config` |
| Foundations | `tree`, `leaf_value`, `constructing`, `settings`, `loader`, `exit_code`, `version_report` |

Section 4 groups the same files by concern instead, which is the grouping to
use when hunting for one.

## 4. The files

All paths below are in [edit/src/edit_cfg_json/](../edit/src/edit_cfg_json/).

### Facts about one configuration object

Pure inspection. Nothing here knows that an editor exists.

| File | Role |
| --- | --- |
| [tree.py](../edit/src/edit_cfg_json/tree.py) | Takes the values of one configuration apart into one node per path, and puts the buffer back together again. The two are inverses. Also answers where the nested objects, the containers and the omitted nodes are. |
| [leaf_value.py](../edit/src/edit_cfg_json/leaf_value.py) | What one leaf holds in JSON space: its kind, the empty value of that kind, and text to value and back. |
| [member_types.py](../edit/src/edit_cfg_json/member_types.py) | The declared type of a member, from annotations, for the cases where the current value cannot say. |
| [descriptions.py](../edit/src/edit_cfg_json/descriptions.py) | The explanatory text a row is shown with: the class docstring, the application's mapping, and what the type itself says. |
| [converting.py](../edit/src/edit_cfg_json/converting.py) | Runs the class's own parse converter over the text of one leaf (enums, in practice) and words the refusal. |
| [constructing.py](../edit/src/edit_cfg_json/constructing.py) | The two ways a configuration object is built: on the class's declared values, and on the buffer through `parse_json`. |

### Files in and out

| File | Role |
| --- | --- |
| [loader.py](../edit/src/edit_cfg_json/loader.py) | The `ConfigLoader` protocol: how an application says its class needs constructor arguments this library knows nothing about. |
| [loading.py](../edit/src/edit_cfg_json/loading.py) | Reads the input file into a configuration object, applies the policy for declared keys the file lacks, and words every way a load can fail. |
| [auto_change.py](../edit/src/edit_cfg_json/auto_change.py) | What reading the file changed. Found by comparing the loaded values with the file text; explained from the records the load kept. |
| [saving.py](../edit/src/edit_cfg_json/saving.py) | Validate, then write. Keeps the overwritten file once per destination per session, and asks the loader whether the new text would still read back as the class being edited. |

### The rows and the editing state

| File | Role |
| --- | --- |
| [rows.py](../edit/src/edit_cfg_json/rows.py) | One row per node, with its value, its state and its marks. Built when the model is built and rebuilt after every validation pass. |
| [buffer.py](../edit/src/edit_cfg_json/buffer.py) | The values as the user is typing them, and which containers are folded. The one part of a session the user changes directly. No input or output, and no knowledge of any backend. |
| [elements.py](../edit/src/edit_cfg_json/elements.py) | What a container offers — add, remove, move — and what a new element would be copied from. Says why where it can offer nothing. |
| [placing.py](../edit/src/edit_cfg_json/placing.py) | Where a class declares that a nested object belongs, and putting one there or taking it away as the buffer gains and loses elements. |
| [finding.py](../edit/src/edit_cfg_json/finding.py) | Which nodes a search text is about. It opens nothing, focuses nothing and scrolls nothing. |
| [validation.py](../edit/src/edit_cfg_json/validation.py) | Four passes: convert each text, apply the whole buffer to a candidate object, attribute a refusal to the member it was about, and ask every nested object on its own. |

### The session and what a backend reads

| File | Role |
| --- | --- |
| [edit_model.py](../edit/src/edit_cfg_json/edit_model.py) | The session: the buffer, the load report, the verdict, where a save would go. Everything a backend calls is a method here. |
| [editing.py](../edit/src/edit_cfg_json/editing.py) | `editor_model()` builds a session and `edit()` runs it in a backend. The front door for an application. |
| [model_text.py](../edit/src/edit_cfg_json/model_text.py) | Every string a backend shows, as plain text: row values, marks, descriptions, diagnostics, questions, and the whole model as one text. |
| [emphasis.py](../edit/src/edit_cfg_json/emphasis.py) | Which kind of text each part is — value, explanation, mark, diagnostic. The colour of a kind belongs to each backend. |
| [backend.py](../edit/src/edit_cfg_json/backend.py) | The `EditorBackend` protocol, and `DumpEditor`, the non-interactive backend that prints the model once. |
| [__init__.py](../edit/src/edit_cfg_json/__init__.py) | The public API, re-exported. |

### Settings of the editor itself

| File | Role |
| --- | --- |
| [settings.py](../edit/src/edit_cfg_json/settings.py) | `Settings` and `ActionSettings`: the key combinations and the file naming that the application decides, as frozen dataclasses. |
| [settings_config.py](../edit/src/edit_cfg_json/settings_config.py) | The same answers written as a `config_as_json.Config`, so a person can keep them in a file and edit them in this editor. It mirrors `settings.py` and does not derive from it. |
| [settings_file.py](../edit/src/edit_cfg_json/settings_file.py) | Where a program looks for its own settings file, in which order, and what it says about a file of an earlier release. |

### The programs

| File | Role |
| --- | --- |
| [cli.py](../edit/src/edit_cfg_json/cli.py) | The command line that all three programs share. Only the backend, the name and the version reporter differ between them. |
| [cli_target.py](../edit/src/edit_cfg_json/cli_target.py) | What one command line says is to be edited: a module, a Python file, or this library's own settings, and the class, loader and descriptions named inside. |
| [dump.py](../edit/src/edit_cfg_json/dump.py) | `python3 -m edit_cfg_json.dump`: `DumpEditor` behind `cli`, so it needs no display. |
| [exit_code.py](../edit/src/edit_cfg_json/exit_code.py) | The exit codes the programs promise, and `Refusal`, which carries one out to where it is printed. |
| [version_report.py](../edit/src/edit_cfg_json/version_report.py) | What `--version` answers with. One `VersionReporter` subclass per distribution. |

## 5. Where to look for what

| Looking for | Start at |
| --- | --- |
| A row shows the wrong value, state or mark | `rows.py`, then `buffer.py` |
| The wrong explanation under a row | `descriptions.py`, then `model_text.py` |
| A member's kind or declared type is wrong | `member_types.py`, then `leaf_value.py` |
| Add, remove or move an element misbehaves | `elements.py`, then `placing.py` |
| A nested object is shown as a plain dict | `tree.py` (`config_nodes`) |
| Folding, or what a fold hides | `tree.py` (`starts_folded`, `rows_below`), then `buffer.py` |
| A refusal lands on the wrong member | `validation.py` (`_attribution`) |
| Opening a file fails, or explains itself badly | `loading.py` |
| "The values are not the ones in the file" | `auto_change.py` |
| Save refused, backup naming, overwrite question | `saving.py` |
| Search behaviour | `finding.py` |
| The wording of a message or a question | `model_text.py` in the core, then `*_ask.py` and `textual_words.py` in a backend |
| Colours | `emphasis.py` for the kinds, `tk_look.py` and `textual_look.py` for the colours |
| Key combinations | `settings.py`, and the backend that binds them |
| A command-line option, or the settings file lookup | `cli.py`, `cli_target.py`, `settings_file.py` |
| An exit code | `exit_code.py` |
| Intended API usage, in context | [examples/src/example/](../examples/src/example/) |

## 6. Working on it

The tests are in
[edit/test/test_edit_cfg_json/](../edit/test/test_edit_cfg_json/), mostly one
`test_<module>.py` per module.
[examples/src/example/](../examples/src/example/) holds nineteen worked
examples, each one a small program, and they are the quickest way to see what
a feature is for.

`./run_static_checks.py <files>` is the fast loop. `./run_clean_build.py` is
what a change has to end with. Both are described in
[README.md](../README.md).
