# Steps 22 to 28, implemented and committed

## Where everything is

Steps 1 to 28 are implemented and committed, step 23 with the corrections its
review asked for. Steps 1 to 9 are written up in
[steps_001-009_done.md](steps_001-009_done.md), steps 10 to 21 in
[steps_010-021_done.md](steps_010-021_done.md) and steps 22 to 28 in
[steps_022-028_done.md](steps_022-028_done.md). The steps still to build are in
[steps_029-x.md](steps_029-x.md). Where any of the four files mentions a
design decision, [`doc/design.md`](../doc/design.md) remains the authority and
the plan says only *when* that decision gets built.

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
- [Step 27][s27] — the dict whose keys its own class does not check given the
  entry control every other container has, and the key policy left where
  `_unchecked_dicts` put it: with the validators of the application.
- [Step 28][s28] — which dicts can be given an entry became a question about
  where a dict sits rather than about which member it belongs to, which is
  what the check that refuses one actually asks.

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
[s10]: steps_010-021_done.md#step-10--lists-and-dicts-of-scalars
[s11]: steps_010-021_done.md#step-11--nested-config-objects
[s12]: steps_010-021_done.md#step-12--subtree-validation
[s13]: steps_010-021_done.md#step-13--list_element-and-dict_value-nesting
[s14]: steps_010-021_done.md#step-14--adding-and-removing-elements
[s15]: steps_010-021_done.md#step-15--confirmation-before-dropping-edits
[s15b]: steps_010-021_done.md#step-15b---changed-descriptions-of---ui-dump
[s16]: steps_010-021_done.md#step-16--oldbackup-file-when-overwriting
[s16b]: steps_010-021_done.md#step-16b---fix-ux-problem-with-edit_cfg_json
[s17]: steps_010-021_done.md#step-17--first-release-polish
[s18]: steps_010-021_done.md#step-18--embedding-in-an-applications-own-window
[s18b]: steps_010-021_done.md#step-18b---redesign-api-and-examples-for-embedding
[s19]: steps_010-021_done.md#step-19---config_as_jsonconfig-for-storing-the-settings
[s20]: steps_010-021_done.md#step-20--the-rest-of-the-programs-command-line
[s21]: steps_010-021_done.md#step-21---version-command-line-flag
[s22]: steps_022-028_done.md#step-22---better-bool-support
[s23]: steps_022-028_done.md#step-23---finding-a-member
[s24]: steps_022-028_done.md#step-24---more-type-information-and-whether-the-user-may-change-it
[s25]: steps_022-028_done.md#step-25---add-and-remove-omitted-members
[s26]: steps_022-028_done.md#step-26---full-support-for-dict_value_by_key
[s27]: steps_022-028_done.md#step-27---adding-an-entry-to-an-_unchecked_dicts-member
[s28]: steps_022-028_done.md#step-28---an-entry-in-a-dict-the-class-never-checks

## 1. Steps 22 to 28, as built

Each of these was detailed just before it was started, and is written up here
as what it decided, what it found while building it and what came of its
review.

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

Status: **Implemented, committed.**

Section 4.9 of the design named two kinds of dict that cannot be given an
entry. One of them is permanently impossible, and this was the other: a member
of `_unchecked_dicts`, whose key policy the application defines with validators
of its own, which the design marked out of v1 scope and no step had claimed.
Step 26 took the third off that list by finding that a member named in
`nested_configs()` never reaches the check the list is about. Such a member now
stops saying why it cannot be given an entry and is offered the controls every
other container already has; a key the application's own validators refuse is
the ordinary verdict.

Step 26 made it cheap, because a dict that accepts a key its class does not
declare is what both of them need and step 26 built it: `ENTRY_KINDS` in
`elements.py` is the list of declarations whose entries are elements, and this
step adds the members of `_unchecked_dicts` to the same question.

**One question, asked in one place.** `_holds_elements` was already the
question *are the entries of this dict elements of it* and was already read by
the removal side; growing asked it again in its own words. Now both read it,
and it has two answers rather than one: an `ENTRY_KINDS` declaration, or the
member being one of `tree.unchecked_members`. That is the whole of the change
in the core — the offer says `extend`, `keyed` and `remove`, and the buffer,
the rows and both backends already do the rest — and it is why no file outside
`elements.py` was touched.

**What a new entry holds** is `_ordinary_entry`, which step 26 wrote for the
undeclared half of a `DICT_VALUE_BY_KEY` member: the three questions of step
14 asked of the keys that no declaration names. An unchecked member has no
declared keys, so the same function answers for the whole of it, and which of
the two sentences a member with nothing to copy says follows from the same
fact: `BY_KEY_PATTERN` where declarations name keys, and the new
`NO_ENTRY_PATTERN` where none do. `UNCHECKED_SCOPE` is gone.

**The whole of such a member is unchecked, and not only its outermost dict.**
`Config.check_dict_parse` returns as soon as the member is named in
`_unchecked_dicts`, *before* it recurses into the keys, so a dict inside such a
member really can gain a key too and is offered one. `_member_path` already
said this in its docstring for the sentence that used to be shown there; it now
decides a control.

**And `NO_DICT_YET` is untouched, which is worth writing down.** The same
check refuses a dict written for a member that holds none — *Unexpected
dictionary for X in JSON data* — and it refuses it *before* the return for an
unchecked member. So a member of `_unchecked_dicts` that holds nothing still
cannot be given a dict, and the sentence saying so is still right. Design
section 4.9 says it in that order now.

**What is observable.** `labels` in `examples/src/example/e11_add_remove.py`,
which already had the shape and said it was out of scope. It takes an entry
under a key the user gives and gives one up again, and what a new one holds is
the one entry the class declares. The class also gained the key policy that
`_unchecked_dicts` handed it — a `DictKeysValidator` insisting on `team` and
allowing `owner` and `tier` — so the division of work is what the example
shows: `--add labels=owner` is valid, `--add labels=region` is added and then
refused by the application, and `--remove labels.team` takes away the one key
it insists on. Only `limits` now says why it can be given nothing, and e08,
which shows the same sentence, says it in its new words.

### Step 28 - An entry in a dict the class never checks

Status: **Implemented, committed.**

Step 24 gave an empty list its elements from `list[str]` and deliberately gave
an empty dict nothing, because what refuses a new entry of a dict is not the
absence of a pattern. It is `Config.check_dict_parse` matching the member
against the keys its class declares, and a type hint says what a *value* would
be and nothing about whether the key beside it would be accepted. This step is
the other half of that: not a pattern for a dict, but the discovery that the
editor was refusing dicts the check never looks at.

**The rule the editor had was about the wrong thing.** It asked which *member*
a dict belongs to — an `ENTRY_KINDS` declaration, or `_unchecked_dicts` — and
the check asks something else. `parse_json` applies it once per member, and
`check_dict_parse` recurses from there into the *dict values* of that member.
So it reaches a dict only where it was applied to the member at all and where
every step down was into a dict, which makes the question **where the dict
sits** and not which member it is in.

**Three things stop it, and the third was the step.** Written out, and each
confirmed against the pinned `config_as_json` by parsing a document that gains
the key in question:

- A member named in `nested_configs()`, which `parse_json` branches away to
  `_nested_config_from_json` for, so the check is never applied to it. The old
  rule had this for the member itself and missed everything below it.
- A member named in `_unchecked_dicts`, where the check returns at the member
  before it looks at a key. Step 27's answer, unchanged.
- A list between the member and the dict. `check_dict_parse` returns as soon
  as neither side is a dict, and a list is not one, so a dict inside an element
  of a `list[dict[str, int]]` really can gain a key and be read back.

**The third one made the first one bigger, which was not planned.** Once the
question is *was the check applied to this member*, the answer covers the whole
subtree of a member named in `nested_configs()` and not only the member. That
is a real case and not a hypothetical: a `DICT_VALUE_BY_KEY` member holds
ordinary values at every key no declaration names, one of those values may be a
dict, and `_dict_by_key_from_json` keeps such a value exactly as it parsed it
while `_validate_dict_by_key` looks only for a `Config` object where none was
declared. Nothing anywhere checks its keys. Step 26 gave that member its
entries and this step gives the dicts inside them theirs.

**So `ENTRY_KINDS` is gone**, and with it the last piece of the member-shaped
rule. `_holds_elements` reads the three answers above, `_under_list` is the new
half-dozen lines that say the third of them, and nothing else in the core
changed: the offer says `extend`, `keyed` and `remove`, and the buffer, the
rows and both backends already do the rest. It is step 27's shape again — one
question in one place, with one more answer than it had.

**The values are asked and never the steps.** A dict is free to have a key
called `0`, so `_under_list` asks what the value at each step of the path *is*
rather than whether the step looks like an index. A `dict[str, dict[str, int]]`
whose one key is `0` still says why it cannot be given an entry, and it is in
the tests for exactly that reason.

**What a new entry holds** needed nothing new: `_ordinary_entry` already asks
step 14's three questions, so the declared value at that path is asked first,
then what the dict holds now, then the annotation. `dict[str, int]` is what
answers for an element the class declares empty, which is the sentence the step
promised, and it is `NO_ENTRY_PATTERN` where none of the three says anything.

**And `NO_DICT_YET` is untouched again.** `member_types._type_at` sets
`nothing` false for every node below a member, so a member is the only place
that state exists and the sentence about the empty dict written for a member
that holds none is still a sentence about members.

**What is observable.** `stage_limits` in
`examples/src/example/e11_add_remove.py` is `limits` with a list in the way —
the same `dict[str, int]` shape, one that can be given nothing and one where
each element takes entries and gives them up. Its two elements are the two
answers a new entry has: the first holds entries so a new one is a copy of `2`,
and the second is empty so `dict[str, int]` says `0`. `hooks` gained
`thresholds`, an ordinary value of a `DICT_VALUE_BY_KEY` member that is itself
a dict, which is the other route to the same place. `examples/data/e11_pipeline.json`
holds a `stage_limits` whose second element is not empty, so reading it shows
the file answering before the annotation does, exactly as `extra_hosts` does
for a list.
