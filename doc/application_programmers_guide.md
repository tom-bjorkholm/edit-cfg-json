# Application programmer's guide to edit-cfg-json

This guide is for the programmer of an application whose users need to change
its configuration, and who wants to give them the editor of `edit-cfg-json`
for the job — a window, or the terminal.

It says **what your application has to do**, and nothing about how the editor
works inside. There are six situations an application can be in, one section
each, and every one of them is a few lines of your code.

## What this guide is not

| Looking for | Read |
| --- | --- |
| What the person editing a configuration sees and does | [end_users_guide.md](end_users_guide.md) |
| How to write the `Config` class in the first place | [config_as_json](https://pypi.org/project/config-as-json/) |
| Every name, argument and return value | [edit-cfg-json](edit-cfg-json_api.md), [edit-cfg-json-tk](edit-cfg-json-tk_api.md), [edit-cfg-json-textual](edit-cfg-json-textual_api.md) |
| Why the library is built the way it is | [detailed_design.md](detailed_design.md) |
| Where the code lives, for maintaining the editor itself | [code_design_overview.md](code_design_overview.md) |

## What you need before you start

**One `config_as_json.Config` class.** That is the whole schema. You do not
list your members for the editor, you do not say which of them are text and
which are numbers, and you write no widget: the editor reads all of it from
the object you hand over. Whatever shape your configuration has — nested
objects, lists, dicts, enums, optional members — is a shape the editor
already shows.

**Which of the two editors.** `edit-cfg-json-tk` is a window and needs a
display. `edit-cfg-json-textual` fills the terminal and needs a terminal.
Nothing stops you from depending on both and choosing at run time.

## Installing, and what to depend on

```sh
pip install edit-cfg-json-tk        # the window editor
pip install edit-cfg-json-textual   # the terminal editor
```

Declare in your own project whichever ones you actually import:

| You import | Depend on | Brings in |
| --- | --- | --- |
| `edit_cfg_json_tk` | `edit-cfg-json-tk` | `edit-cfg-json`, and Tkinter comes with Python |
| `edit_cfg_json_textual` | `edit-cfg-json-textual` | `edit-cfg-json` and `textual` |
| `edit_cfg_json` only | `edit-cfg-json` | no user interface at all |

`edit-cfg-json` on its own gives you the model and the non-interactive
backend, and no editor. Depend on it alone when you write a backend of your
own, or when a part of your application only needs to read a configuration
file the same way the editor does.

Python 3.12 or newer, for all three.

---

# Part 1 — Before you write any code

You do not have to build the editor into your application to see your own
configuration class in it. Each of the two editor packages installs a program
that opens **any** `config_as_json.Config` class it is told the name of, so
your class can be edited on the day you write it.

This is the fastest way to answer "what will my users actually see?", and it
is the right place to try out descriptions, key combinations, file naming and
your validators before any of that is wired into an application.

## 1.1 Open your own class

```sh
edit-cfg-json-tk --module myapp.config --class AppConfig
edit-cfg-json-textual --module myapp.config --class AppConfig -i app.json
```

`--module` names an importable module; `--file` names a Python file instead,
for a class that is not on the import path yet:

```sh
edit-cfg-json-tk --file ./scratch/new_config.py --class DraftConfig
```

Both are also reachable as `python3 -m edit_cfg_json_tk` and
`python3 -m edit_cfg_json_textual`, for a machine whose script folder is not
on `PATH`.

**Importing a module runs it.** That is the same exposure as
`python3 somefile.py`, and it is worth knowing when the module you name has
work at import time.

## 1.2 The whole command line

Both programs take the same options, and so does the utility of section 1.5.

| Option | What it says |
| --- | --- |
| `--module MODULE` | Importable module holding the class. |
| `--file PATH` | Python file holding the class. |
| `--edit-settings` | Edit a settings file of the editor itself, rather than a class of yours. |
| `--version` | Report the installed versions and whether newer ones exist. |
| `--class CLASS` | Name of the `config_as_json.Config` class. |
| `--loader NAME` | Name of an `edit_cfg_json.ConfigLoader` in that module. |
| `--descriptions NAME` | Name of an `edit_cfg_json.Descriptions` mapping in that module. |
| `--policy` | `strict`, `defaults` or `strict-then-defaults`. |
| `-i`, `--input` | Configuration file to read. |
| `-o`, `--output` | Configuration file to write, or the input file. |
| `-c`, `--cfg PATH` | Settings file this run of the program behaves according to. |

Exactly one of `--module`, `--file`, `--edit-settings` and `--version` is
required. `--class`, `--loader` or both go with the first two: a class alone
is constructed on the values it declares, a loader alone is asked for a
configuration and the class it answers with is the class of the session, and
the two together mean the loader has to answer with that class.

**The command line never says how the editor behaves** — no option for key
combinations, no option for the file extension. Every one of those is a
setting, and section 1.4 is where a run gets them.

## 1.3 Trying out the parts only your application knows

Two of the things your application will pass in code can be named on the
command line, so both can be tried before they are wired in.

**Descriptions.** Put the mapping in the module beside the class and name it:

```python
# myapp/config.py
from edit_cfg_json import Descriptions

DESCRIPTIONS: Descriptions = {
    ('name',): 'What this pipeline is called in the logs.',
    ('workers',): 'How many jobs run at the same time.'}
```

```sh
edit-cfg-json-tk --module myapp.config --class AppConfig \
    --descriptions DESCRIPTIONS
```

**A loader**, for a class the editor cannot construct on its own because its
constructor needs an argument this library knows nothing about:

```python
# myapp/config.py
from functools import partial
from edit_cfg_json import derived_loader

team_config = derived_loader(partial(TeamConfig, KNOWN_TEAMS))
```

```sh
edit-cfg-json-tk --module myapp.config --loader team_config \
    --class TeamConfig -i teams.json
```

## 1.4 Trying out settings without writing a program

Everything an application decides about the editor — its key combinations,
the extension of its configuration files, how a file that is overwritten is
looked after — is a setting, and every setting can be written in a file:

```sh
edit-cfg-json-tk --edit-settings -o myeditor.cfg
edit-cfg-json-tk --module myapp.config --class AppConfig -c myeditor.cfg
```

The first line edits the settings themselves in the editor and writes a file;
the second runs with that file. A settings file need name only what it
changes.

Without `-c`, a program looks in five places and uses the first that answers:

1. the file `-c/--cfg` names,
2. the file the `CFG_EDIT_CFG_JSON` environment variable names,
3. `$HOME/.edit-cfg-json-tk.cfg` or `$HOME/.edit-cfg-json-textual.cfg`,
4. `$HOME/.edit-cfg-json.cfg`,
5. nothing at all, which is the defaults.

A file that was **named** must exist — a name no file answers to stops the
run. A file that was **looked for** need not.

Section 4.4 is the other half of this: how to let the person running your
*application* own the same settings.

## 1.5 Checking a configuration file from a script

The core package ships a non-interactive backend that prints the model once
and returns, behind the same command line:

```sh
python3 -m edit_cfg_json.dump --module myapp.config --class AppConfig \
    -i app.json
```

It needs no display and no terminal, and it answers with an exit code, which
makes it something a build job can run. It has two options the editors do not:
`--save`, because there is no Save to press, and `--unfold`, because there is
no fold control to press.

| Code | What it means |
| --- | --- |
| 0 | Everything asked for was done. |
| 1 | The input file cannot be opened for editing. |
| 2 | The command line itself is wrong. |
| 3, 4, 5, 6 | The module, the file: not importable, not readable, not Python, needs its package. |
| 7, 8 | That name is not there, or is not a `Config` class. |
| 9 | The editor cannot construct that class on its own — it needs a loader. |
| 10 | The configuration is not one your application would accept. |
| 11 | The output file was asked for and was not written. |
| 12 | That class cannot write its own values as JSON, so there is nothing to show. |
| 13, 14, 15 | The loader cannot be called, needs arguments a command line cannot give, or answered with the wrong class. |
| 16 | The `--descriptions` name is no mapping. |
| 17 | The settings of the program itself cannot be read. |

Exit code 10 is the one worth building a job around: **a configuration file
your application would refuse is a failed run**, not a remark in the output.

---

# Part 2 — The six ways to open the editor

Find your situation in the first column. Everything else in this part follows
from that one row.

| Your application | You call | It blocks | The outcome is | Example |
| --- | --- | --- | --- | --- |
| **1.** No user interface at all, wants a window | `edit_cfg_json_tk.edit` | yes | the return value | [a01_tk_for_no_gui.py](../examples/src/example/a01_tk_for_no_gui.py) |
| **2.** Already runs Tk, wants a new window | `TkEditorPanel(..., parent=)` | no | `on_close` + `saved_config` | [e15_window_tk.py](../examples/src/example/e15_window_tk.py) |
| **3.** Already runs Tk, wants an area of a window it has | `TkEditorPanel(..., area=)` | no | `on_close` + `saved_config` | [e13_embedded_tk.py](../examples/src/example/e13_embedded_tk.py) |
| **4.** No user interface at all, wants the terminal | `edit_cfg_json_textual.edit` | yes | the return value | [a02_textual_for_no_gui.py](../examples/src/example/a02_textual_for_no_gui.py) |
| **5.** Already runs Textual, wants the whole interface | `push_screen(EditorScreen(...))` | no | `on_close` + `saved_config` | [e16_screen_textual.py](../examples/src/example/e16_screen_textual.py) |
| **6.** Already runs Textual, wants an area it has | `mount(EditorPanel(...))` | no | `on_close` + `saved_config` | [e14_embedded_textual.py](../examples/src/example/e14_embedded_textual.py) |

**The one rule behind the split.** Cases 1 and 4 create the toolkit's own
top object — a `tkinter.Tk`, or a Textual `App` — and run its event loop.
An application that already has one cannot use them, and not because of a
policy of this library:

- a second `tkinter.Tk` in a process is a second Tcl interpreter, and no
  widget, variable, font or image crosses between two of them;
- `App.run` calls `asyncio.run`, so calling it from inside a running Textual
  application raises or deadlocks.

So cases 2, 3, 5 and 6 are non-blocking entry points that mount the editor in
something you own, and they take exactly the same keywords about the session
(Part 3). Neither toolkit offers a supported way to ask whether one is already
running, so the editor is told and never guesses.

## The class the six programs share

Every program below edits this one class, which is an ordinary
`config_as_json.Config` and knows nothing about the editor:

```python
# myapp/config.py
from typing import Optional, TextIO
import sys
from config_as_json import Config, IntFloatValidator, \
    MemberValidationStep, PathOrStr, ValidationPlan
from edit_cfg_json import Descriptions


class AppConfig(Config):
    """How this application runs its pipeline."""

    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr,
                 member_name: Optional[str] = None) -> None:
        """Initialize the configuration with its default values."""
        self.name: str = 'nightly'
        self.workers: int = 4
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file, member_name=member_name)

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the rules this application has for its own values."""
        _ = stderr_file
        return [MemberValidationStep(
            member_names=['workers'],
            validator=IntFloatValidator[int](min_value=1, max_value=64,
                                             allowed_values=None))]


DESCRIPTIONS: Descriptions = {
    ('name',): 'What this pipeline is called in the logs.',
    ('workers',): 'How many jobs run at the same time.'}
```

`get_validation_plan` is `config_as_json`'s and not this library's: every
class derived from `Config` has to have one, and `return []` is what a class
with no rules of its own answers. The editor has no rules at all — it hands
the values to your class and reports what your class says about them, so this
is where the rule that refuses 500 workers lives.

`member_name` is the fourth of the keyword arguments `config_as_json`
expects, and passing it on is what makes a diagnostic about a value inside a
nested object name the whole path to that value, such as
`outputs[1].width`. It is `None` for the configuration itself, which is a
member of nothing. A class written before that argument existed is
constructed without it and warns that it should be changed, in the editor
exactly as in your own program; the editor needs nothing else of you for
this.

Three notes on reading the programs below.

- `run_the_pipeline` and `reconfigure` are **your** code and no part of this
  library: they stand for whatever your application does with a
  configuration.
- A `...` in an argument list is this guide being brief.
- Only cases 1 and 4 show the `ConfigLoadError` handling. The other four
  raise it from the constructor in the same way and need the same `try`;
  section 4.1 is where that belongs, and leaving it out here keeps each
  program about the one call it is for.

## 2.1 Case 1 — a command with no user interface, in a window

```python
"""configure.py — a command that has no user interface of its own."""

import sys
from edit_cfg_json import ConfigLoadError
from edit_cfg_json_tk import edit
from myapp.config import DESCRIPTIONS, AppConfig


def main() -> None:
    """Edit the configuration in a window, then run with what was saved."""
    try:
        saved = edit(AppConfig(), descriptions=DESCRIPTIONS,
                     in_file='app.json')
    except ConfigLoadError as refusal:
        sys.exit(str(refusal))
    if saved is None:
        sys.exit('Nothing was saved.')
    run_the_pipeline(saved)


if __name__ == '__main__':
    main()
```

**What your application does:** nothing but this call. `edit` creates the
`tkinter.Tk` of the process, runs its event loop, and returns when the user
closes the editor.

**What your application must not have done:** created a `tkinter.Tk` of its
own, before this call or after it.

**Blocking is the point.** Nothing of your command runs while the editor is
open, and nothing needs to — the user is editing. That is what lets the
outcome be a return value rather than a callback.

Worked example, with a display that is not there handled as well:
[a01_tk_for_no_gui.py](../examples/src/example/a01_tk_for_no_gui.py).

## 2.2 Case 2 — an application that runs Tk, in a new window

```python
"""A Tk application that opens the editor over its own window."""

from typing import Optional
import tkinter
from edit_cfg_json_tk import TkEditorPanel
from myapp.config import DESCRIPTIONS, AppConfig


class AppWindow:
    """The application's own window, with an entry that configures it."""

    def __init__(self, root: tkinter.Tk) -> None:
        """Build the application's own content and its editor button."""
        self._root = root
        self._panel: Optional[TkEditorPanel] = None
        tkinter.Button(root, text='Configure...',
                       command=self._configure).pack()

    def _configure(self) -> None:
        """Open the editor in a modal window of its own over this one."""
        if self._panel is None:
            self._panel = TkEditorPanel(AppConfig(), parent=self._root,
                                        descriptions=DESCRIPTIONS,
                                        in_file='app.json',
                                        on_close=self._editor_gone)

    def _editor_gone(self) -> None:
        """Take up the new configuration, if the user saved one."""
        assert self._panel is not None
        saved = self._panel.saved_config
        self._panel = None
        if saved is not None:
            self.reconfigure(saved)


root = tkinter.Tk()
AppWindow(root)
root.mainloop()
```

**`parent` is the whole of it.** The editor creates the `tkinter.Toplevel`
itself, names it after your configuration class, makes it transient for your
window, routes its close button through its own Close, and destroys it again
when the session ends. Your window is left exactly as it was.

**Constructing it returns at once**, because your own `mainloop` is already
running. There is no moment at which it could return what was saved, so
`on_close` says the session has ended and `saved_config` says what came of it.

**`modal` defaults to `True`**, which holds your application until the user
has finished with the editor — including your own controls. Pass
`modal=False` for an editor your application answers beside.

Worked example: [e15_window_tk.py](../examples/src/example/e15_window_tk.py).

## 2.3 Case 3 — an application that runs Tk, in an area it already has

```python
"""A Tk application with an area of its window given to the editor."""

from typing import Optional
import tkinter
from edit_cfg_json_tk import TkEditorPanel
from myapp.config import DESCRIPTIONS, AppConfig


class SplitWindow:
    """A window with the application's own panel and an editor area."""

    def __init__(self, root: tkinter.Tk) -> None:
        """Build the application's own panel and the empty editor area."""
        self._panel: Optional[TkEditorPanel] = None
        left = tkinter.Frame(root)
        left.pack(side='left', fill='y')
        tkinter.Button(left, text='Configure',
                       command=self._configure).pack()
        self._area = tkinter.Frame(root)
        self._area.pack(side='left', fill='both', expand=True)

    def _configure(self) -> None:
        """Build the editor into the area, beside the application's own."""
        if self._panel is None:
            self._panel = TkEditorPanel(AppConfig(), area=self._area,
                                        modal=False,
                                        descriptions=DESCRIPTIONS,
                                        in_file='app.json',
                                        on_close=self._editor_gone)

    def _editor_gone(self) -> None:
        """Take up the new configuration, if the user saved one."""
        assert self._panel is not None
        saved = self._panel.saved_config
        self._panel = None
        if saved is not None:
            self.reconfigure(saved)


root = tkinter.Tk()
SplitWindow(root)
root.mainloop()
```

**`area` in place of `parent`** is the only difference from case 2. The editor
builds one frame inside the widget you named and fills it, and destroys that
frame again when the session ends. It never gets a window of its own.

**Give exactly one of `parent` and `area`.** Neither, or both, is a
`ValueError`: an application with no Tk of its own is case 1, and one that
named both has answered one question twice.

**`modal=False` is what embedding is usually for.** The default `True` would
hold your own controls while the editor filled part of your own window, which
is rarely what an application that chose to embed wants.

**The keys of the editor reach the editor and nothing else** — the frame it
built and everything inside it. Your own keys, everywhere else in that window,
are untouched.

**`panel.close()` is your own way out**, for a menu entry or a button of your
own. It asks about anything unsaved, in the same words the editor's own Close
uses; pass `close(ask_about_unsaved=False)` when your application is already
putting a question of its own. Calling it again after the session has ended
does nothing, so you need not track whether the user closed it first.

Worked example:
[e13_embedded_tk.py](../examples/src/example/e13_embedded_tk.py).

## 2.4 Case 4 — a command with no user interface, in the terminal

```python
"""configure.py — the same command, in the terminal."""

import sys
from edit_cfg_json import ConfigLoadError
from edit_cfg_json_textual import edit
from myapp.config import DESCRIPTIONS, AppConfig


def main() -> None:
    """Edit the configuration in the terminal, then run with what was saved."""
    try:
        saved = edit(AppConfig(), descriptions=DESCRIPTIONS,
                     in_file='app.json')
    except ConfigLoadError as refusal:
        sys.exit(str(refusal))
    if saved is None:
        sys.exit('Nothing was saved.')
    run_the_pipeline(saved)


if __name__ == '__main__':
    main()
```

**Only the import differs from case 1.** `edit` runs a Textual application of
its own, which takes the terminal on the alternate screen and gives it back
when the user closes the editor. Whatever your command printed before is still
there afterwards, and what it prints after the call goes to the ordinary
terminal again.

**What your application must not have done:** run a Textual `App` of its own
around this call.

**This one needs a terminal**, in the way case 1 needs a display. A command
whose output is redirected, or that runs from a job with no terminal at all,
has nowhere to put this editor; `sys.stdout.isatty()` is what a command that
might be run either way asks before it chooses.

Worked example:
[a02_textual_for_no_gui.py](../examples/src/example/a02_textual_for_no_gui.py).

## 2.5 Case 5 — an application that runs Textual, over its whole interface

```python
"""A Textual application that pushes the editor as a screen of its own."""

from typing import Optional
from textual.app import App, ComposeResult
from textual.widgets import Button, Footer
from edit_cfg_json_textual import EditorScreen
from myapp.config import DESCRIPTIONS, AppConfig


class PipelineApp(App[None]):
    """An application that offers a configuration editor."""

    def __init__(self) -> None:
        """Start with no editor showing."""
        super().__init__()
        self._editor: Optional[EditorScreen] = None

    def compose(self) -> ComposeResult:
        """Create this application's own widgets."""
        yield Button('Configure')
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Push the editor on top of this application's own screen."""
        _ = event
        if self._editor is None:
            self._editor = EditorScreen(AppConfig(),
                                        descriptions=DESCRIPTIONS,
                                        in_file='app.json',
                                        on_close=self._editor_gone)
            self.push_screen(self._editor)

    def _editor_gone(self) -> None:
        """Take up the new configuration, if the user saved one."""
        assert self._editor is not None
        saved = self._editor.saved_config
        self._editor = None
        if saved is not None:
            self.reconfigure(saved)


PipelineApp().run()
```

**Textual has no second window to open, so a window of its own is a screen.**
`EditorScreen` is the editor with a header, a footer and command palette
entries of its own around it, which is what a widget cannot have.

**The screen pops itself.** By the time `on_close` runs, your own screen is
back on top and there is nothing for you to pop. Pushing it returns at once,
because your event loop is already running.

**`screen.close()` is your own way out**, and it is worth having: `ctrl+q` is
both the editor's key for closing and Textual's key for quitting an
application, and Textual gives your own binding the key first. An application
that wants the editor's close key to work gives the editor another one with
`Settings(actions=ActionSettings(quit=...))`.

Worked example:
[e16_screen_textual.py](../examples/src/example/e16_screen_textual.py).

## 2.6 Case 6 — an application that runs Textual, in an area it already has

```python
"""A Textual application with an area of its screen given to the editor."""

from typing import ClassVar, Optional
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Footer
from edit_cfg_json import ActionSettings, Settings
from edit_cfg_json_textual import EditorPanel
from myapp.config import DESCRIPTIONS, AppConfig

ORDINARY_KEYS = Settings(priority_keys=False,
                         actions=ActionSettings(quit=('ctrl+w',)))
"""What this application has already decided about the editor's keys."""


class SplitScreenApp(App[None]):
    """An application whose screen has an area the editor is mounted in."""

    CSS: ClassVar[str] = '#area { height: 1fr; }'

    def __init__(self) -> None:
        """Start with no editor mounted."""
        super().__init__()
        self._panel: Optional[EditorPanel] = None

    def compose(self) -> ComposeResult:
        """Create this application's own widgets and the empty area."""
        yield Button('Configure')
        yield Vertical(id='area')
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Mount the editor in the area of this application's own screen."""
        _ = event
        if self._panel is None:
            self._panel = EditorPanel(AppConfig(), descriptions=DESCRIPTIONS,
                                      in_file='app.json',
                                      settings=ORDINARY_KEYS,
                                      on_close=self._editor_gone)
            self.query_one('#area', Vertical).mount(self._panel)

    def _editor_gone(self) -> None:
        """Take up the new configuration, if the user saved one."""
        assert self._panel is not None
        saved = self._panel.saved_config
        self._panel = None
        if saved is not None:
            self.reconfigure(saved)


SplitScreenApp().run()
```

**`EditorPanel` is an ordinary Textual widget**, so it goes wherever you mount
a widget, and you keep your own header, your own footer and your own command
palette. Mounting returns at once.

**The editor brings its own style sheet.** The one thing your application says
about it is where it goes, which is the `CSS` line above.

**Textual offers a key from the focused widget upwards**, so the editor's keys
act while the focus is inside the editor and yours act everywhere else. Your
footer names the editor's actions while the focus is in there.

**`priority_keys=False` is the one setting only an embedded editor has a
reason to change.** The default `True` offers the key to the editor before the
widget that has the focus; `False` is the other way round, for an application
whose own widget inside that area has already taken one of these combinations.

Worked example:
[e14_embedded_textual.py](../examples/src/example/e14_embedded_textual.py).

---

# Part 3 — What every one of the six takes

All six entry points say the same things about a session, with the same
keyword names, so moving from one to another changes where the editor is and
nothing else.

## 3.1 The session keywords

| Keyword | Default | What it says |
| --- | --- | --- |
| `config` | required | A configuration object saying which class to edit and what its declared defaults are. **Never modified.** |
| `descriptions` | `None` | What your application says about the members it declares, as `Mapping[ConfigPath, str]`. |
| `in_file` | `None` | File to read, or the declared defaults when there is none. |
| `loader` | `None` | How your application constructs its class, for one the editor cannot construct on its own. |
| `out_file` | `None` | File to write, or the input file when there is none. |
| `policy` | `STRICT_THEN_DEFAULTS` | What to do about declared keys the input file does not hold. |
| `settings` | `Settings()` | What your application has already decided about keys and file names, or a callable answering with it. |
| `stderr_file` | `sys.stderr` | Stream for user-facing diagnostics. |

The four mounting entry points take these after their own first arguments —
`parent`/`area`/`modal` for Tk, and `on_close` for all four.

**`descriptions` explains the members; the class explains itself.** The
docstring of your configuration class labels the whole object, and the
docstring of each nested object's class labels that object, both without you
passing anything — the classes already have them. Individual members need
this mapping, because a member docstring does not exist at run time. A member
no description reaches is simply shown without one.

A path is the absolute `config_as_json.ConfigPath` of what it is about, so
a value inside a list, a dict or a nested object needs no second way of being
named. The `'['` step means every element or every value at that point:

```python
DESCRIPTIONS: Descriptions = {
    ('name',): 'What this pipeline is called in the logs.',
    ('outputs', '['): 'One output file of the pipeline.',
    ('outputs', '[', 'width'): 'Page width in millimetres.'}
```

**`loader` is only for a class the editor cannot construct.** Most
applications need none: the editor reads the constructor signature and passes
every parameter it knows the meaning of. Say it when your class needs an
argument this library knows nothing about, and `derived_loader` is the
shortest way to say it:

```python
from functools import partial
from edit_cfg_json import derived_loader

loader = derived_loader(partial(TeamConfig, KNOWN_TEAMS))
```

A loader written by hand is the door for anything `derived_loader` cannot
express — a class chosen by looking at the JSON, in practice.

**`policy`** is one of `LoadPolicy.STRICT`, which refuses a file that does not
hold every declared key, `LoadPolicy.DEFAULTS`, which fills in what the file
leaves out, and `LoadPolicy.STRICT_THEN_DEFAULTS`, which loads strictly and on
failure fills in and says so. The last is the default, because whether a
partly specified file is acceptable is your decision and the answer that suits
most applications is to open it and tell the user it was incomplete.

**`out_file`** defaults to the input file, which is what an editor is normally
asked to do. With neither, there is nowhere to write and the editor asks the
user for a destination when they press Save. A destination you name that has
no extension gets the one your application uses (section 4.3); the input file
never does.

## 3.2 What you get back

**Cases 1 and 4** answer with the return value of `edit`:

```python
saved = edit(AppConfig(), in_file='app.json')
```

**Cases 2, 3, 5 and 6** have no moment at which they could return anything, so
they answer through `on_close` and `saved_config`:

```python
panel = TkEditorPanel(AppConfig(), area=area, on_close=session_ended)
...
saved = panel.saved_config
```

Either way the value is **the configuration object that was written, or
`None` when the session ended without a save**. Both are ordinary outcomes and
neither is an error.

`on_close` may be `None` for an application that reads `saved_config` some
other way.

## 3.3 Your own object is never modified

The editor works on a copy. The `AppConfig()` you handed over is still holding
the values it started with, even after the user has saved. What reached the
file is the object you are given back, and that is the one to go on with.

This is why the outcome is handed to you rather than expected to be found in
the object you passed.

## 3.4 The other three things a panel offers

| Member | For |
| --- | --- |
| `close(ask_about_unsaved=True)` | Your own way out — a menu entry, a button, a step of your own workflow. |
| `saved_config` | What the session wrote, `None` until it writes something. |
| `model` | The `EditModel` of the session, for an application that wants more than the outcome. |

`EditorScreen` adds `panel`, which is the editor widget inside it.

---

# Part 4 — Reference

## 4.1 What can go wrong, and what you have to catch

| Raised by | When | What to do |
| --- | --- | --- |
| `edit_cfg_json.ConfigLoadError` | All six, when `in_file` cannot be read as this class: not there, not JSON, or refused by the class. | Catch it and say so. Never let the user get an editor quietly showing defaults instead of the file they asked for. |
| `ValueError` | `TkEditorPanel`, when `parent` and `area` are both or neither given. | Fix the call; it is a programming mistake, not a run-time condition. |
| `ValueError` | `Settings(...)`, for an extension or backup suffix that names no file, a backup count below one, or one key combination given to two actions. | Fix the settings; the refusal names what is wrong. |
| `tkinter.TclError` | Case 1, on a machine with no display. | Catch it where a command may run over a plain remote shell or from a build job. A message beats a traceback. |

`ConfigLoadError` carries the message in `str(error)` and whatever the
configuration class itself said in `error.diagnostics`.

**Everything after the load is not an exception.** A value the user types that
your validators refuse is shown at the member it is about; a save that cannot
be written says so in the editor. Your application hears about none of it, and
does not have to.

## 4.2 Keys

Every action of the editor has an attribute of its own on
`edit_cfg_json.ActionSettings`, holding every combination that runs it:

| Action | Default keys |
| --- | --- |
| `quit` | `ctrl+q` |
| `validate` | `ctrl+r`, `f5` |
| `save` | `ctrl+s` |
| `save_as` | `ctrl+shift+s`, `f12` |
| `cancel` | `escape` |
| `explain` | `f1`, `ctrl+g` |
| `fold` | `f2`, `ctrl+t` |
| `find` | `ctrl+f` |
| `find_next` | `f3` |

```python
from edit_cfg_json import ActionSettings, Settings

SETTINGS = Settings(actions=ActionSettings(quit=('ctrl+w',),
                                           explain=('f1', 'ctrl+e')))
```

- The **first** combination of a tuple is the one a footer or a menu names;
  the rest work without being named.
- An **empty tuple** takes the key away and not the action — a button and a
  command palette entry still reach it.
- Combinations are written the way Textual names keys, in lower case:
  `ctrl`, `shift`, `alt`, `meta` joined with `+`, then one character, `f1` to
  `f12`, or a name such as `escape`, `enter`, `tab`, `space`, `home`, `end`,
  `pageup`, `up`. The Tk backend translates them.
- **One combination cannot be given to two actions.** Doing so is a
  `ValueError` where the settings were built.
- A **single unmodified letter cannot be used** for any of them: the value of
  a member is edited in a field, and a user who typed a letter expects to see
  it appear.

Two things to check when you embed:

**`ctrl+q` is Textual's own quit** (cases 5 and 6). Textual gives your
application's binding the key first, so give the editor another one, or give
your users a Close of your own with `close()`.

**`priority_keys`** decides who is offered a key first. `True`, the default,
is the editor before the widget that has the focus. `False` is the other way
round, for an application whose own widget inside the editor's area has
already taken one of these combinations.

## 4.3 The files a save writes

The editor is asked to write your application's files, so the naming is
yours to decide:

```python
from edit_cfg_json import Settings

SETTINGS = Settings(file_extension='.cfg', extension_enforced=True,
                    backup_suffix='.bak', backup_count=3,
                    confirm_overwrite=True)
```

| Setting | Default | What it says |
| --- | --- | --- |
| `file_extension` | `None` | What a configuration file of your application is called. `cfg` and `.cfg` mean the same thing. `None` is no opinion. |
| `extension_enforced` | `False` | Whether a file name with another extension is refused. Says nothing while `file_extension` is `None`. |
| `backup_suffix` | `.bak` | What the file about to be overwritten is kept as. Added to the whole name, so `x.cfg` becomes `x.cfg.bak`; `~` and `.old` are the other shapes. `None` keeps nothing. |
| `backup_count` | `1` | How many are kept, newest first. Two or more are numbered from `_1` and rotate. |
| `confirm_overwrite` | `True` | Whether the user is asked before an existing file is overwritten — once per destination per session, at the moment the previous content would stop existing. |

A session that has already written a destination is not asked about it again:
that is the user's own earlier save being overwritten.

## 4.4 Letting the person running your application decide

Everything in 4.2 and 4.3 is also a configuration class,
`edit_cfg_json.SettingsConfig`, so it can be written in a file and edited in
this editor like anything else. There are two ways to offer that.

**As a member of your own configuration**, which is what an application with
one configuration file wants:

```python
from config_as_json import Config, ConfigNesting, ConfigNestingKind, \
    NestedConfigs
from edit_cfg_json import Descriptions, SettingsConfig, described_below


class AppConfig(Config):
    """How this application runs its pipeline."""

    def __init__(self, ...) -> None:
        """Initialize the configuration with its default values."""
        self.name: str = 'nightly'
        self.editor: SettingsConfig = SettingsConfig()
        super().__init__(...)

    def nested_configs(self) -> NestedConfigs:
        """Say that the `editor` member holds one object of that class."""
        return {'editor': ConfigNesting(kind=ConfigNestingKind.MEMBER,
                                        config_type=SettingsConfig)}


DESCRIPTIONS: Descriptions = {
    ('name',): 'What this pipeline is called in the logs.',
    ('editor',): 'How the configuration editor of this application behaves.',
    **described_below(('editor',))}
```

and then hand `config.editor.as_settings()` to the editor as its `settings`.
`described_below` puts what `SettingsConfig` says about its own members under
the member holding it, so your users get the explanations without you writing
a sentence per setting and keeping it up to date with a library you do not
own.

[e17_settings_config.py](../examples/src/example/e17_settings_config.py) is
this written out in full.

**As a settings file of its own**, which is what section 1.4 already
described: `edit_cfg_json.load_settings` and `edit_cfg_json.settings_file`
are the same five-place lookup the two programs use, available to your
application.

A settings **block** inside your own configuration is read whole, so it has to
hold every key. A settings **file** of its own need name only what it changes.

**`settings` may be a callable** rather than a `Settings`, and is then asked
again at each point where an answer is used. What that is really for is an
application that has not got its settings ready at the moment it builds the
editor — key combinations are read once, when a backend builds its bindings,
and the file name settings at every save.

## 4.5 Testing an application that embeds the editor

The two things worth knowing, both of which the examples in this repository do
in [examples/test/test_example/](../examples/test/test_example/):

**Tk.** Replace `Tk.mainloop` with what a user would do next. The editor's
widgets are ordinary Tkinter widgets below the frame or window it built, so a
button is found by its text and pressed with `invoke()`. Skip on
`tkinter.TclError` for a machine with no display, and stub out `grab_set` and
`grab_release` — a real grab in a test suite holds the machine it runs on.

**Textual.** Replace `App.run`, or drive your own application with
`app.run_test()` and a `Pilot`. The editor's own widgets carry identifiers, so
a field is reached by query and a key by `pilot.press`.

**Neither needs the editor at all** for the parts of your application that are
about the configuration rather than about editing it.
`python3 -m edit_cfg_json.dump` (section 1.5) exercises a load, a validation
and a save with no display and no terminal, which is what a build job can run.

## 4.6 If you want a user interface neither package gives you

`edit_cfg_json.editor_model` builds the session — read the input file, build
the model — on the same keywords as Part 3, and answers with an `EditModel`.
`edit_cfg_json.EditorBackend` is the one-method protocol that
`edit_cfg_json.edit` runs it in, and `edit_cfg_json.DumpEditor` is a small
backend that prints the model once and returns. Between them they say what a
backend really is, which is anything with a `run_editor` method.

That is a bigger job than the six cases above and is not what this guide is
about; [detailed_design.md](detailed_design.md) section 8 is.

---

# Part 5 — A checklist

1. Write the `config_as_json.Config` class. It is the whole schema.
2. Open it with `edit-cfg-json-tk --module ... --class ...` and look at it
   (Part 1).
3. Write the `Descriptions` mapping for the members whose purpose a name does
   not give away, and try it with `--descriptions` (section 1.3).
4. Decide the file naming and the keys, try them with `--edit-settings` and
   `-c`, and turn the answers into one `Settings` in Python (sections 4.2 and
   4.3).
5. Find your situation in the table in Part 2 and write that one call.
6. Handle `ConfigLoadError` (section 4.1).
7. Use the object you are given back, not the one you handed over
   (section 3.3).
8. Point your own users at [end_users_guide.md](end_users_guide.md), or lift
   the part of it that matches the editor you chose — it is written to be
   liftable, and it says what to check before you publish any of it.
