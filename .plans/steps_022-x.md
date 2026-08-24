# Delivering the remaining scope in small steps

## Where everything is

Steps 1 to 26 are implemented and committed, step 23 with the corrections its
review asked for. Steps 1 to 9 are written up in
[steps_001-009_done.md](steps_001-009_done.md) and steps 10 to 21 in
[steps_010-021.md](steps_010-021.md). Step 22 and the steps still to build are
in this file. Where any of the three files mentions a design decision,
[`doc/design.md`](../doc/design.md) remains the authority and the plan says only
*when* that decision gets built.

- [The decisions the plan is built on][dec] — the seven settled before the
  first step, from example observability to per-step verification.
- [The names introduced in steps 1 to 9][names] — one table of every public
  core name and the step that settled it.
- [Step 1][s1] — the walking skeleton: `EditModel`, `EditorBackend`,
  `model_as_text` and `--ui dump`, both backends showing a flat config
  read-only.
- [Step 2][s2] — the buffer became writable, with dirty tracking, and
  `--set` standing in for a user typing.
- [Step 3][s3] — validation of the buffer, the refusals it catches, and the
  mark for a value a validator rewrote.
- [Step 3B][s3b] — `Enum` and `IntEnum` members, which needed no change to
  the core at all.
- [Step 4][s4] — loading: `LoadPolicy`, `load_config`, the three distinct
  refusals, and the mark for a member a permissive load filled in.
- [Step 5][s5] — saving and `edit()`, which reached milestone 1: a save
  validates, moves the baseline it is compared against, and asks for a
  destination when it has none.
- [Step 6][s6] — descriptions and docstrings, the explain toggle in the
  model, a scrolling body in both backends, and the `Emphasis` vocabulary.
- [Step 7][s7] — field-level diagnostics: a refusal is shown at the member
  it is about, on validation and on focus loss.
- [Step 7B][s7b] — three ready-to-run programs, one per package, opening any
  `Config` class named by `--module` or `--file`, with an exit code for each
  way of refusing.
- [Step 8][s8] — automatic-change visibility: what reading an old-format
  file altered, marked at the member and reported by key.
- [Step 9][s9] — the explicit loader: `ConfigLoader`, `derived_loader`, and
  a save that refuses a file the loader would not read back as the same
  class.
- [Step 10][s10] — lists and dicts as a tree of rows with a field at every
  value, folding, and the rows being built again when a validator changes how
  many of them there are.
- [Step 11][s11] — a nested `Config` object as a node with a class, a
  docstring and members of its own, and the ownership of everything inside it.
- [Step 12][s12] — every nested object asked whether it is a configuration on
  its own, which both puts a badge on its row and names the member inside it
  that a validator refused.
- [Step 13][s13] — a list of configuration objects and a dict of them, one
  description reaching every one of them, and the confirmation that step 11 had
  already built the mechanism.
- [Step 14][s14] — how many things a member holds, where a new element is
  copied from, and the containers that say why they cannot be given one.
- [Step 15][s15] — closing an editor that holds something unsaved asks first,
  in words the core owns and in a dialog or a screen that each backend puts.
- [Step 15B][s15b] — the two interactive editors described as the product they
  are, and `--ui dump` as the very limited non-interactive user interface it
  is.
- [Step 16][s16] — the file that a save writes over kept under the name the
  application chose, once per destination per session, and a question before
  it happens.
- [Step 16B][s16b] — the name `edit-cfg-json` freed for the editor it
  promises, and the backend that prints once reached as the small utility it
  is.
- [Step 17][s17] — every document rewritten against what was actually built,
  the order of the work taken out of all of them but this one, and the release
  readiness of the three packages checked rather than assumed.
- [Step 18][s18] — the editor mounted in a window an application already owns,
  in both toolkits, with its keys reaching the editor and nothing else.
- [Step 18B][s18b] — one call per shape per toolkit, taking the keywords of
  `edit()`, and four examples where there were two.
- [Step 19][s19] — the settings of the editor as a configuration class of
  their own, editable in the editor, declarable inside an application's own
  configuration, and looked for in five places by each program.
- [Step 20][s20] — the command line of a program saying what to edit and which
  files and never how the editor behaves, which is the whole of the answer once
  every setting can be written in a file.
- [Step 21][s21] — `--version` on all three programs, as a fourth thing a run
  does instead of editing, answered by one version reporter per distribution.
- [Step 22][s22] — a member holding true or false entered as an enum member
  already was: any beginning of either word in any case, and a text that means
  neither of them refused at that member.
- [Step 23][s23] — looking for a member of a configuration that does not fit a
  window: a field that stays, four controls that say where it looks, and a match
  inside a folded container opened, brought into view and typed into.
- [Step 24][s24] — the declaration of a member read as well as the value it
  holds, and the open question of section 4.2 answered: a member allowed to
  hold nothing has two states rather than a kind the user can change.
- [Step 25][s25] — the members a class leaves out of the file given a row to be
  given a value at, the buffer written back to the class as the document a save
  would write, and the one kind of value that a member holding nothing cannot
  be given.
- [Step 26][s26] — the dict whose values are of two kinds asked twice: the key
  a declaration names given the two states of a member that may hold no object,
  and every other key of it an entry of an ordinary container after all.

[dec]: steps_001-009_done.md#1-decisions-this-plan-is-built-on
[names]: steps_001-009_done.md#2-naming-conventions-used-below
[s1]: steps_001-009_done.md#step-1--walking-skeleton-read-only-view-of-a-flat-config
[s2]: steps_001-009_done.md#step-2--editing-the-buffer
[s3]: steps_001-009_done.md#step-3--validation-of-the-buffer
[s3b]: steps_001-009_done.md#step-3b--enums-as-attributes-in-config
[s4]: steps_001-009_done.md#step-4--loading
[s5]: steps_001-009_done.md#step-5--saving-and-edit--milestone-1
[s6]: steps_001-009_done.md#step-6--descriptions-and-docstrings
[s7]: steps_001-009_done.md#step-7--field-level-diagnostics
[s7b]: steps_001-009_done.md#step-7b--a-ready-to-run-program-in-every-package
[s8]: steps_001-009_done.md#step-8--automatic-change-visibility
[s9]: steps_001-009_done.md#step-9--the-explicit-loader
[s10]: steps_010-021.md#step-10--lists-and-dicts-of-scalars
[s11]: steps_010-021.md#step-11--nested-config-objects
[s12]: steps_010-021.md#step-12--subtree-validation
[s13]: steps_010-021.md#step-13--list_element-and-dict_value-nesting
[s14]: steps_010-021.md#step-14--adding-and-removing-elements
[s15]: steps_010-021.md#step-15--confirmation-before-dropping-edits
[s15b]: steps_010-021.md#step-15b---changed-descriptions-of---ui-dump
[s16]: steps_010-021.md#step-16--oldbackup-file-when-overwriting
[s16b]: steps_010-021.md#step-16b---fix-ux-problem-with-edit_cfg_json
[s17]: steps_010-021.md#step-17--first-release-polish
[s18]: steps_010-021.md#step-18--embedding-in-an-applications-own-window
[s18b]: steps_010-021.md#step-18b---redesign-api-and-examples-for-embedding
[s19]: steps_010-021.md#step-19---config_as_jsonconfig-for-storing-the-settings
[s20]: steps_010-021.md#step-20--the-rest-of-the-programs-command-line
[s21]: steps_010-021.md#step-21---version-command-line-flag
[s22]: #step-22---better-bool-support
[s23]: #step-23---finding-a-member
[s24]: #step-24---more-type-information-and-whether-the-user-may-change-it
[s25]: #step-25---add-and-remove-omitted-members
[s26]: #step-26---full-support-for-dict_value_by_key

## 1. How this plan is meant to be used

This document turns the scope recorded in
[`doc/design.md`](../doc/design.md) into an ordered list of small,
individually reviewable and individually committable steps. It is a delivery
plan, not a design document: where it mentions a design decision,
`doc/design.md` remains the authority and this file only says *when* that
decision gets built.

- One step is one branch-less unit of work on `master`: implement, verify,
  ask for review, commit. The next step does not start until the previous
  one is committed.
- Every step changes what an example program does. If a step cannot be
  observed from `examples/src/example/` with `--ui tk` or `--ui textual`,
  it is the wrong step boundary and should be merged into a neighbour or
  split differently.
- Every step touches all three packages where the capability is
  user-visible, so `edit_cfg_json`, `edit_cfg_json_tk` and
  `edit_cfg_json_textual` never drift apart by more than one review.
- Steps 1 to 26 are built, and each is written up in
  [steps_001-009_done.md](steps_001-009_done.md), in
  [steps_010-021.md](steps_010-021.md) or in section 3 of this file as what it
  decided, what it found while building it and what came of its review. Steps
  27 onwards are named steps with their observable outcome and their main
  risks; they are detailed just before they are started, when the core API is
  real rather than imagined.

### 1.1 Definition of done for one step

A step is finished when all of the following hold.

1. A short design summary was posted before editing, per `CLAUDE.md`.
2. Code, tests and example changes are all in place.
3. `./run_clean_build.py python3.12`, then `./run_clean_build.py
   python3.13`, then `./run_clean_build.py python3.14` each exit 0.
   They run sequentially; there is one `./venv` and the three cannot be
   run in parallel.
4. For each of those three runs, `./reports/index.html` says
   `Build succeeded` with no errors or warnings, and
   `./reports/mypy_errors.txt`, `./reports/flake8_log.txt`,
   `./reports/python_layout_log.txt` and `./reports/pytest_log.txt` are
   clean. Every issue the tools report anywhere in the repository is
   fixed, not triaged as unrelated.
5. A summary of the changes and of any oddities noticed is written up.
6. The step is reviewed and committed.

Note that the last of the three builds leaves `./venv` on that Python
version. Record which one, because the next step's fast iteration with
`./run_static_checks.py` and targeted `pytest` runs uses that venv.

## 2. Milestones

| Milestone | Steps | What exists at the end | Status |
| --- | --- | --- | --- |
| M1 Flat round trip | 1 to 5 | Both backends edit a `Config` with one `str` and one `int`, validate it and save it | done |
| M2 Flat, fully explained | 6 to 9 | Descriptions, docstrings, field-level diagnostics, automatic-change visibility, explicit loader | done |
| M3 Structure and folding | 10 to 12 | Lists, dicts, nested `Config` objects, folding with per-subtree badges | done |
| M4 Configs in containers | 13 to 14 | `LIST_ELEMENT` and `DICT_VALUE` nesting, adding and removing elements | done |
| M5 Release readiness | 15 to 17 | Closing keeps what was not saved, files are not overwritten unannounced, and first release is documented, classified and published | done |
| First release 0.0.2 | release on PyPI.org | [https://pypi.org/project/edit-cfg-json/](https://pypi.org/project/edit-cfg-json/) | done |
| Second release 0.0.4 | 18 to 21 | Release 0.0.4 | done |

## 3. Steps 22 onwards, as named steps

Each of these is detailed just before it is started. What is fixed now is
the order, the observable outcome and the main risk.

### Step 22 - Better bool support

Status: **Implemented, committed.**

When the user enters a bool value they should get the same support as
when entering an enum value. The text in the text field should be
compared to `true` and `false` in a case insensitive way and if the
text in the field matches the beginning of `true` or `false` it should
be expanded to that value.

**Observable outcome.** Two example programs show it and neither of them
changed. `e12_backup_files.py --ui dump --set compress=f` prints
`compress = false (edited)` and a valid verdict where it printed
`compress = f (edited)` and nothing that said what was wrong;
`--set compress=yes` now prints `yes is not one of: true, false` under that
member and `validation: invalid, see compress`, where it used to be accepted
and written to the file as a string. `e17_settings_config.py --ui dump --fold
editor --set editor.confirm_overwrite=F` prints `confirm_overwrite = false` and
a valid verdict where it printed `confirm_overwrite = F` and
`Value for confirm_overwrite is not of type bool`. The same two members are
what the window and the terminal show: typing `f` into the `compress` field of
`e12_backup_files.py --ui tk` and pressing Validate leaves `false` in the
field, and `edit-cfg-json-tk --edit-settings` is three such fields.

**What it decided.** Four things.

- **The two words are read by the rules `config_as_json` already uses for an
  enum member name.** Its `string_to_enum_best_match` tries the case variants
  of what was typed and then accepts a beginning that only one member has, so
  `true` and `false` are read the same way: the case is ignored, a beginning of
  one of them is that value, and a beginning of both of them is neither. The
  empty text of a cleared field is the only ambiguous one there is. That is
  what "the same support as when entering an enum value" means, and it is why
  the rule is written beside the conversion of an enum rather than as a rule of
  its own kind.
- **The reading happens on the change**, where every other text becomes a
  value, and not when the field loses the focus. The buffer therefore holds
  `false` as soon as `f` is typed, so a validation pass and a save are given
  the value the user meant, and the whole word reaches the field with the
  refresh that follows a pass — the path a value that a validator rewrote
  already takes. Neither backend changed.
- **A text that means neither word is refused at that member**, in the words
  an enum member name that names no member is refused in, and it blocks the
  candidate configuration exactly as that refusal does. It is the one refusal
  of a leaf that the editor makes itself rather than running something the
  class declared, and it is made from the type of the member and not from a
  rule of the application. The consequence was weighed and taken: an
  application that would have accepted something else in a member whose value
  was true or false can no longer be given one from the editor. What made it
  worth taking is that the editor already says *true or false* under such a
  member, so the refusal says no more about the member than the line above it
  does.
- **The line under the member is left as `True or false.`** Saying that a
  beginning is enough was the alternative, and it was refused: the type line is
  the shortest statement of what the member holds, and the shortcut is
  discovered by typing.

**Core.** `leaf_value` owns `bool_word` and the branch of `text_as_value` that
uses it, and `text_as_value` now takes the value the leaf kept instead of a
flag saying whether it is text: the type of a leaf is one thing, it is that
value, and one argument answers every branch. `converting` owns the refusal,
`rows` gained `is_bool` beside `is_text`, and `buffer` hands both of them on.
`validation` takes the paths of the nodes that hold one of the two words,
because the values it is given are JSON space values in which nothing says
which member takes those two and only those two.

The public names it settled:

| Name | Kind |
| --- | --- |
| `MemberRow.is_bool` | whether this leaf holds one of the two words |
| `bool_word` | which value a beginning of either word means |
| `NOT_A_BOOL_FORM` | what a text meaning neither of them is told |

**What building it found.**

- **`config_as_json` was already forgiving about an enum name and nothing was
  forgiving about a bool.** `string_to_enum_best_match` accepts a unique
  prefix, in any case, and reports what it refused as
  `LO is not one of: LOWEST, LOW, HIGH`. So the step was not inventing a
  convenience: it was giving one kind of member the convenience the other kind
  already had, in the same words.
- **A validation pass could not work the type out for itself.** Deriving which
  nodes hold true or false from the session's own configuration object was the
  design that would have needed no plumbing, and it is wrong: that object is
  not updated when an element is added to or removed from a list, so the kept
  value at `flags.0` would be the value of whatever used to be there. The rows
  own the type, so the rows are what hand it over.
- **A member that a beginning does not change is not an edit.** `compress`
  holds `true`, so typing `tr` into it leaves nothing to save and the row says
  nothing about being edited, which is the ordinary rule that a value typed
  back to what it was is no change. It is worth knowing before reading a
  printout of one of these examples.
- **`_unconverted` in `validation` and `check_all` in the buffer answer the
  same question twice**, once by path from the values and once from the rows.
  Nothing about this step made that worse and nothing about it made it better,
  and it is one of the things the rewrite the code needs would put right.

### Step 23 - Finding a member

Status: **Implemented, reviewed, committed.**

Section 9.7 had kept `ctrl+f` and `f3` free since the first version, for the
search that a configuration too big for a window (section 4.6) asks for, and
this step took them: a field that stays below the rows, four tick-boxes beside
it that say where it looks, a control and a key that go to the next member
found, and a line under them saying what the search has reached.

**How it was decided to work.** Six answers, each of which could have gone the
other way. Section 4.10 of the design is the authority on all of them.

- **What is being looked for is state of the model**, by the lesson of step 6
  about the explanation toggle: two backends looking for different things, or
  looking in different places, would each be right about a different search. So
  the core owns the text, the four answers, which nodes they reach, which of
  them the search is at, the words of the line, the `(found)` mark and the
  explanation of each control; each backend owns its widgets, the label on each
  control, and where an explanation is put.
- **A field that stays, and not a question that is asked and gone.** A search is
  a text that is changed a character at a time, so it searches on every change
  of the field.
- **Case insensitive, and any part of the path or of the value**, with four
  independent tick-boxes that change one answer each.
- **What is found is reachable**: every folded container hiding it opens, and
  each backend brings the row into view. Opening one asks the configuration
  objects in it about themselves, exactly as folding does (section 4.7), and a
  search that opened nothing asks nothing.
- **Typing moves nothing else; Enter and the find next key move the cursor**
  into the field of what was found.
- **`RESERVED_KEYS` is gone.** It existed to keep these two keys free, and the
  test that read it now says the search holds exactly them.

The public names it settled:

| Name | Kind |
| --- | --- |
| `FindOptions` | the four answers about where a search looks |
| `FindReport` | what the editor says about the search |
| `FIND_OPTION_HELP` | what each of those four answers means |
| `EditModel.search` | what the editor says about the search |
| `EditModel.find`, `.set_find_options`, `.find_next` | the three ways of searching, each saying whether a container was opened |
| `MemberRow.found` | whether the search has got to this node |
| `find_text`, `find_emphasis` | the line about the search, and how loudly it is shown |
| `ActionSettings.find`, `.find_next` | the two keys, which no longer need reserving |

**What building it found.**

- **Adding an action makes an existing settings *block* incomplete.** A nested
  `SettingsConfig` is read whole (section 9.8), so `examples/data/e17_tool.json`
  had to name both new actions to stay loadable. Worth knowing before step 30.
- **Both backends were at the 1000-line limit**, and each was split where it
  should have been split anyway: `tk_panel` took `TkEditor` and `edit()` so that
  `tk_editor` is the widgets alone, which is how the Textual side was already
  arranged, and `textual_words` took what that backend calls its actions.
- **`pytest examples/test` on its own segfaulted Tk** inside example e13's own
  `update_idletasks`, before any editor was built. It does not reproduce in the
  whole-suite order that the build uses.

**What the review corrected.**

- **The Tk tooltip was a borderless window of its own**, and macOS rounds the
  corners of one: at that size the corners ate the first character and the last.
  It is now a label put over the window the control is in, which no window
  manager decorates (section 4.10).
- **A focused field in Textual hid its own text.** A field of Textual's own
  accord is three cells high and grows its border back when it is given the
  focus, and a row is one cell, so what the user was typing was laid out under
  the row below. Every field and control of a row is now Textual's compact one,
  which has no border in any state, and a tint of the theme's own foreground
  colour says which field has the cursor (section 4.6). The same change fixed
  the fold and the element controls, which had been two cells high in a one-cell
  row since step 10.
- **The Tk Find next button carries `►`** and says its words in a tooltip, so
  the row keeps that width for the field.
- **A withdrawn Tk root cannot answer for a tooltip**: Tk delivers `<Enter>` to
  a mapped window only, so this is one of the few places with a stubbed test and
  no companion in category 2 of section 10.2.

**What the second review round found.** The two actions this step added to
`ActionSettings` were a change of the settings file format, and nothing had been
done about the files of the release before them.

- **A settings file of the earlier release was refused.** The keys of the
  `actions` member are matched against the ones `SettingsConfig` declares while
  the file is parsed, before any validator of that class is asked anything, and
  that happens whatever policy the load was given. So a file holding the seven
  actions there were was refused with *No value for find in JSON data* — and an
  application that declares `SettingsConfig` as one member of its own
  configuration was refused whatever policy *it* chose, because a nested
  configuration object is read whole. Such an application would have failed to
  start over two keys of the editor it embeds, and the refusal it printed named
  the wrong fault: *This file holds a key that this configuration does not
  have*.
- **`SettingsConfig` now declares rules for reading such a file**, which is
  `config_as_json`'s Read Old Configuration File support. `ADDED_ACTIONS` names
  the actions no released version ever wrote, and the combinations supplied for
  them are read from `ActionSettings` rather than written again. Only actions
  *added since a release* belong there: supplying one that has always existed
  would accept a file no version ever produced.
- **The rules are declarative and nothing else.** 
- **The run says which file was an older one.** `load_settings` names the file
  and asks for it to be opened with `--edit-settings` and saved, because saving
  is what writes every value the current version has. It is printed there and
  not by a `config_as_json.MigrateCfgWarnHook`: a hook prints while the file is
  parsed, and `load_config` collects what a parse says into diagnostics it shows
  only when the load failed, so a hook's warning about a load that succeeded
  would never reach anybody. Measured, not assumed — and `load_config` builds
  its own configuration object, so a hook handed to it is never used at all.
- **Section 9.10 of the design is the general rule**, so that the next action
  added is not the next release broken.

### Step 24 - More type information, and whether the user may change it

Status: **Implemented, committed.**

Two things the design recorded and no step claimed, both in section 4.2: an
open question about whether the user may change the type metadata of a leaf,
and the note that later versions would derive more type information from the
attribute types than from the type of the default value. The step answered the
question first, and the answer decided what was built.

**The answer to the open question.** *No, and the case it was wanted for is
answered another way.* The one thing changing the kind of a leaf would have
been useful for is telling a `None` apart from an empty text in an
`Optional[str]`, and there was nothing that said which members those were.
There is now. A member the class declares to allow no value has **two states**
— it holds a value, or it holds nothing — and the user moves between them with
the **same add and remove controls** that give a declared `OPTIONAL_MEMBER`
its configuration object and take it away again. No new control in either
backend, no new key, no new command line option, and no backend change at all:
both backends already render `ElementOffer`, and `--add` and `--remove`
already press it. Section 4.2 of the design is the authority, and section 11
records the rejection.

**Where a declared type is read from.** Three sources, each covering a pattern
the others do not: `typing.get_type_hints()` for a dataclass and for any class
level annotation; the **source of the class**, parsed with `ast`, for the
ordinary `Config` pattern, which records nothing at runtime; and the value the
leaf held, which is what there always was and remains the fallback. The whole
of the class is read and not only its `__init__`, because a class may declare
its members in a method of its own — every configuration fixture in this
repository's own core tests does. Nothing is evaluated here: an annotation is
a text and the text goes to `inspect.get_annotations`, which is the standard
library's own resolver for one.

**What the reach was decided to be**, from four answers, each of which could
have gone the other way.

- **Also how a field's text is read**, and not the explanatory line alone. A
  member declared `Optional[str]` holding nothing reads `123` as the text and
  not as the number, and one declared `bool` gets step 22's expansion.
- **Also an element of an empty list**, from `list[str]`, which is the case
  section 11 had put permanently out of scope while the kind of an element was
  unknowable. It is asked **last**, after the class's declared element and the
  member's own first element, because a value the application wrote says more
  than its kind does. Section 11 keeps the rejection with a narrower scope.
- **Not an entry of an empty dict**, and the reason is worth keeping: what
  refuses one is `Config.check_dict_parse` matching the member against the
  keys its class declares, and a type hint says what a *value* would be and
  nothing about the key beside it. Offering the control would be offering one
  that produces a refusal. Recorded as step 28 for the dicts that check never
  reaches.
- **`nothing` is never set where the kind is unknown.** The two states exist
  only where the editor can make a value for one of them, which keeps
  `Optional[SomeEnum]` and `Optional[SomeClass]` exactly as they were.

The public names it settled:

| Name | Kind |
| --- | --- |
| `LeafType` | what a class says one leaf of it holds: the kind, whether it may hold nothing, and what one value inside it is |
| `MemberRow.declared` | that answer for one node |
| `MemberRow.holds_nothing`, `.kind` | the state of such a member, and which kind of value it takes |
| `edit_cfg_json.member_types` | reading the three sources, and `node_types` for a whole tree |
| `leaf_value.kind_text`, `.leaf_kind`, `.empty_value` | what a kind is called, which kind a leaf takes, and the emptiest value of one |
| `rows_shape` | what a backend makes its widgets again for |
| `NO_VALUE_TEXT`, `NOTHING_TEXT`, `LIST_KIND`, `DICT_KIND` | what such a row and such a line say |

**What building it found.**

- **A field must never change whether it is a field.** Typing `null` into a
  member with the two states would have taken the field away from under the
  cursor after four characters, and a backend does not rebuild its widgets on
  a keystroke. So such a member reads `null` as the text it is, and the state
  is only ever reached through a control. A member with no such state reads
  `null` as JSON, exactly as before.
- **`editable` had to stop asking `is_container(original)` alone.** A member
  declared `Optional[list[str]]` and given `[]` has rows below it and an
  `original` of `None`, so it was both foldable and editable. It now asks the
  rows as well.
- **Both backends rebuilt on the paths alone, and a pass can change less than
  that.** A member validator returns the value that is stored back into the
  member, so one can answer `None` for a member allowed to hold nothing: the
  rows are the same rows and one of them is no longer a field. `rows_shape` is
  the core's one answer to when a backend makes its widgets again, and section
  8 of the design is the rule. Example 18 has such a validator, so both
  backends have a test that presses Validate and counts the fields.
- **`_hold_again` read the shape from `original` and had to read it from the
  value.** The same member would have had its elements put back together as a
  dictionary, losing all of them. Found by reasoning about the new state
  rather than by a failing test, because no member of that shape existed yet.
- **A quoted forward reference was read as its own name.** `ast.unparse` of
  `self.x: 'MyType'` writes the quotation marks back, so resolving it answered
  with the string. Unwrapped before it is resolved.
- **The core test fixtures declare their members in `declare_members()`**,
  which is what made reading the whole class source the right shape rather
  than a generalization for its own sake.
- **A focus-sensitive Tk test was already broken on master.** Step 23 added
  four tick-boxes to the find row and `test_shown_window_settles` still
  expected one. The build deselects `focus_sensitive`, so no build had
  reported it. It now reads the four from `FindOptions` itself.

**What is observable.** A new example,
`examples/src/example/e18_declared_types.py`, with
`examples/data/e18_report.json`. `--ui dump` shows `threshold = 0` saying *A
number.*, `subtitle: no value` with an add control, and `footer` with a remove
control; `--add subtitle --save` and `--save` write `""` and `null` into two
different files. Two existing examples changed without being asked to:
`e11_add_remove.py --ui dump --add extra_hosts` now adds an empty text where
it used to refuse, and `e17_settings_config.py --edit-settings` shows the
editor's own `file_extension` as `no value` rather than as `null`.

### Step 25 - Add and remove omitted members

Status: **Implemented, committed.**

A member that `_omit_none_from_json()` names is written as no key of the file
at all while it holds nothing, so nothing about it reached the values the rows
were built from and it had no row. Step 24 had given every other optional
member two states and the pair of controls that moves between them, and had
recorded the reason this one could not have them: clearing it would take the
row off the screen with no control anywhere to give it a value again. This step
removes the cause rather than the consequence.

**The answer was one question, not the one the plan expected.** The early idea
recorded above was about *discovering* what such a member holds, with a raw
JSON fallback where nothing could be discovered. Almost none of that was
needed, because step 24 had already done the discovering: the three type
sources answer a leaf, `nested_configs()` names the class of an object, and
`built_config` already constructs a class whose constructor takes arguments
this library knows nothing about — that was step 14's work, and a class it
cannot construct already says so instead of offering a control that refuses
every press. What was actually missing was one row.

**Where the row comes from.** `vars()` on the configuration object, as the
early idea guessed, and nothing more: the members one object *holds and did not
write* are exactly the ones it left out, which needs no protected name to ask.
`tree.shown_values` adds them back, each of them holding nothing, and it is
applied to the value of every configuration node of the tree and not only to
the outermost one, because a nested object leaves out its own members by its
own class.

**And one row is not enough, because the buffer is written back.**
`tree.file_values` is the inverse, and it settled the rule that the whole thing
turns on: **what is validated is the document that would be written**. A save
writes the object a validation pass built, and that object leaves such a member
out, so a pass given `null` for it would reach its verdict about a document no
save produces. A class is free to make something of a key it does not find —
the rules for reading an older file are given the keys of the document before
anything else looks at them — so the two documents are not promised to be read
alike, and the one that matters is the one the file will hold.

**What the investigation found in `config_as_json`**, both of which changed
what was built.

- **A dict cannot be given to a member that holds none.**
  `Config.check_dict_parse` refuses one — *Unexpected dictionary for X in JSON
  data* — whatever keys it has and even where it has none, because it matches
  the dict in the document against the dict the member holds. So the empty dict
  of step 24 is the one value of a kind that a member allowed to hold nothing
  cannot be given, and it now says so below its own row. That was a defect in
  step 24 rather than a new case: it was reachable for a member written as
  `null` and was reached by nothing. Sections 4.2, 4.9 and 11 of the design
  record it, and it is the first bullet of 4.9 one step up — the same check
  refuses a new key of an ordinary dict member.
- **A nesting kind other than `OPTIONAL_MEMBER` can never hold nothing.**
  `_validate_nested_config` requires a list for `LIST_ELEMENT`, a dict for
  `DICT_VALUE` and a dict for `DICT_VALUE_BY_KEY`, and it runs while the object
  is constructed, so `Optional[list[SomeConfig]]` holding `None` is not a state
  any configuration the editor is given can be in — not even as an omitted
  member. Code written for it was written and then taken out again, which is the
  right way round: it was a moving part for a state that does not exist.

**What is observable.** A new example,
`examples/src/example/e19_omitted_members.py`, with
`examples/data/e19_report.json` holding one key and opening with six rows. It
has the five shapes side by side: an omitted `Optional[str]`, an omitted
`OPTIONAL_MEMBER` added from being absent and cleared again, an omitted
`Optional[list[str]]` that takes two presses to reach an element, the omitted
`Optional[dict[str, int]]` that says why it can be given nothing, and the
unannotated member that is an ordinary field showing `null`. Two examples said
the opposite and now say what is true: e18's `note` has the same two states as
the two members beside it, and e11 says that an `_omit_none_from_json()` member
would be moved between the same two states by the same two controls.

**The one small refactor.** `optional_members` and `optional_paths` moved from
`descriptions.py` to `tree.py`, beside `unchecked_members`, which reads
`_unchecked_dicts` for the same reason. Section 4.1 lists
`_omit_none_from_json()` as a source of the structure, so that is where it is
read, and `file_values` needs it where the rest of the structure is.

### Step 26 - Full support for `DICT_VALUE_BY_KEY`

Status: **Implemented, committed.**

Adding and deleting values in a dict that `DICT_VALUE_BY_KEY` declares. Such a
member is one dict holding values of two kinds — the named key holds a
configuration object and every other key holds an ordinary value — which is
why section 4.9 of the design had it as the third of the three dicts that
cannot be given an entry, and why the effort table put it above step 27.

**What the investigation of `config_as_json` found, and it changed the
step.** The check that stops an ordinary dict member from gaining a key is
`Config.check_dict_parse`, and **a member named in `nested_configs()` never
reaches it**: `parse_json` branches to `_nested_config_from_json` for such a
member and passes the whole of it. For this kind that is
`_dict_by_key_from_json`, which parses the keys the declarations name as the
classes they name and keeps every other key as the ordinary value it is,
whatever that key is called. `_validate_dict_by_key` then requires only that a
declared key, *if it is there*, holds an object of the declared class, and that
an undeclared key does not hold a `Config`. So the key policy that the design
called out of scope is no policy at all: the keys of such a member are
unchecked, and **a declared key is allowed to be absent**.

**The named key is a place and not an entry.** That absence is the whole of
the step. The first idea was the cheap one — the member offers an entry with a
key, and typing the declared name gives an object — and it is the mistake step
25 had already made and undone one level up: taking the object away would take
the row off the screen, and the only way back would be knowing the declared key
by heart and typing it into the question that asks what a new entry is called.
So a declared key is a node of the tree whether the dict holds it or not, with
the two states and the two controls of an `OPTIONAL_MEMBER`. `tree.shown_entries`
adds it back holding nothing, exactly as `shown_values` adds an omitted member
back, and `tree.omitted_paths` puts it beside those members so that
`file_values` takes it out again on the way to the class. What is validated
stays the document that would be written.

**And the rest of the dict is an ordinary container**, because nothing checks
its keys. The member takes an entry under a key the user gives and each entry
can be taken out, and what a new one holds is step 14's three questions —
the value the class declares, failing that a value the member holds, failing
that the annotated type — asked only of the entries that no declaration names.
An object beside the named key is what `_validate_dict_by_key` refuses, so the
declared keys are skipped when the pattern is looked for. A member with none of
the three says so in a sentence of its own and still offers the objects its
declarations name, which is `BY_KEY_PATTERN`.

**Three small things came out of it.**

- `ElementOffer.cleared` says which of the two kinds of removal a row gets,
  because the row cannot say it: a declared key keeps its row while being one
  key of a container whose other keys are taken out of it. It replaced
  `EditBuffer._container_of`, which had been answering the same question from
  the row of the parent and could not answer this one.
- `ObjectPlace` replaced the pair that said where a declared object is held.
  A declaration names a member for four of the five kinds and one key inside a
  member for the fifth, so where an object goes is a member name and a key
  rather than the last step of a path.
- `elements.py` went over a thousand lines, so the half of it that puts real
  configuration objects into the object of the session moved to `placing.py`.
  The two halves were already separate: one says what a node offers and the
  other changes the object the tree is walked over.

**What is observable.** `hooks` in `examples/src/example/e11_add_remove.py`,
which already had the shape and said it was out of scope. Its named key
`on_failure` is taken away and given back, its other keys are added and
removed, and the file that a save writes holds no `on_failure` while the row
says which class is missing. e10 said the same thing about the shape and now
says what is different about it instead.

### Step 27 - Adding an entry to an `_unchecked_dicts` member

Section 4.9 of the design now names two kinds of dict that cannot be given an
entry. One of them is permanently impossible, and this is the other: a member
of `_unchecked_dicts`, whose key policy the application defines with validators
of its own, which the design marks out of v1 scope and no step has claimed.
Step 26 took the third off that list by finding that a member named in
`nested_configs()` never reaches the check the list is about. Such a member
stops saying why it cannot be given an entry and is offered the controls every
other container already has; a key the application's own validators refuse is
then the ordinary verdict.

Step 26 made it cheaper, because a dict that accepts a key its class does not
declare is what both of them need and step 26 built it: `ENTRY_KINDS` in
`elements.py` is the list of declarations whose entries are elements, and this
step adds the members of `_unchecked_dicts` to the same question.

### Step 28 - An entry in a dict the class never checks

Step 24 gave an empty list its elements from `list[str]` and deliberately gave
an empty dict nothing, because what refuses a new entry of a dict is not the
absence of a pattern. It is `Config.check_dict_parse` matching the member
against the keys its class declares, and a type hint says what a *value* would
be and nothing about whether the key beside it would be accepted.

There is one place where that check does not reach. `check_dict_parse` returns
without checking anything as soon as a list is between the member and the dict,
so a dict inside an element of a `list[dict[str, int]]` really can gain a key
and be read back. The editor refuses it today, and refuses it conservatively:
its rule is about the *member* rather than about whether the class checks that
particular dict.

This step would make section 4.9's first bullet a question about where the dict
sits in the tree rather than about which member it belongs to, and give such a
dict the entry control, with `dict[str, int]` saying what the new value is.
The main risk is exactly the reason it is not earlier: the rule has to be right
against the implementation of `config_as_json` and not merely plausible, and
being wrong means offering a control whose result the application refuses.

### Step 29 - Raw JSON for a subtree the editor cannot show

Step 25's early idea included a raw JSON editing surface for a sub-object whose
class nothing says anything about, and step 25 found that the case it was
proposed for does not need it: the class of a nested object is named by its
declaration, and one the editor cannot construct says so rather than offering a
control that refuses every press. Section 11 of the design records that it is
kept as a step rather than rejected, because what would make it worth having is
a different question from the one it was proposed for.

That question is an editing surface for a *subtree*, which nothing in the
editor has: a text area holding the JSON of one node, validated by the class on
the next pass, which would also serve pasting a whole section from somewhere
else and repairing a shape no row can express. The risks are the two that
belong to any second way of editing the same thing — which of the two wins
while both are open, and what a validation pass does to text the user is half
way through typing — and they are the reason this is late rather than cheap.

### Step 30 - Pull-down selection of enum and bool values

When the type of an attribute have a well defined set of possible
values that we know from type discovered by introspection we should
offer the user to select the value instead of typing the value.
This is the case for bool, and for enums.

### Step 31 — The program asks for what the command line left out

A wizard: the program opens with no location, no class name and no files,
and asks for them in the toolkit it was started in. What has been chosen,
what is still missing and whether the class could be loaded is state, and by
the lesson of step 6 about the explanation toggle it belongs in the core so
that the two backends cannot drift about it. Each backend then contributes a
dialog or a screen, and a file chooser, which is where the two toolkits
differ most and where neither has a headless test that is worth much.

When we get here investigate if using
[https://pypi.org/project/wizard-ui-bridge/](https://pypi.org/project/wizard-ui-bridge/)
and
[https://pypi.org/project/wizard-tk-bridge/](https://pypi.org/project/wizard-tk-bridge/)
makes implementing the wizards simpler.

Alternatively, consider if we should use the menubar and menu items like
File - Open. (Using the menubar may feel very natural in the Tk version.)

### Step 32 - The launcher the name `edit-cfg-json` is kept for

Section 8.1 of the design is headed "planned, not implemented": an
`edit_cfg_json.ui` entry-point group would let backends register themselves for
discovery, which is what `--ui=auto` needs. Section 8.3 keeps the command name
`edit-cfg-json` free for the launcher that picks the editor the machine can
run, and step 16B freed that name and said the logic for choosing "may be added
in a later step". This is that step: both editor packages register themselves,
the core installs the launcher it has never installed a program for, and a
machine with no display or without `textual` gets the editor it can actually
run, with a refusal and an exit code of its own where it can run none.

## 4. Relative effort of the steps still to build

| Step | Effort | What the number is mostly |
| --- | --- | --- |
| 27 An entry in an `_unchecked_dicts` member | 2 | Step 14's machinery reused: the row stops saying why it cannot, and both backends show controls they already have. |
| 28 An entry in a dict the class never checks | 3 | Step 24's type model and step 14's machinery are both there; the work is getting one rule right against `config_as_json` and a configuration shape to show it with. |
| 32 The launcher | 4 | Little logic, spread over all three packages: an entry-point group, a script the core has never installed, discovery, and what a machine that can run neither editor is told. |
| 30 Pull-down for enum and bool | 6 | A second kind of field in both backends, touching every rule written for the first: write on change, focus loss, the rebuild after a pass, and the marks. |
| 29 Raw JSON for a subtree | 8 | An editing surface the editor does not have at all yet, in both backends, and two rules about a second way of editing one thing. |
| 31 The wizard | 10 | Two toolkits' dialogs and file choosers, two bridge libraries to weigh against the menubar alternative, and no headless test worth much. |

Two things the numbers do not say.

- **Effort is not order.**
- **Step 31 begins with a question**, so its number is the least trustworthy of
  the six. Steps 24 and 25 did too, and both are built — and step 25 came in
  well under its estimate of 8, because the question it began with turned out to
  have been answered by step 24.

## 5. Open questions recorded, not answered

These do not block current development, and each is scheduled to be answered at the
step that needs it. They are listed here so they are not forgotten.

| Question      | Answer needed by |
| ------------- | ---------------- |
| (nothing yet) |                  |
