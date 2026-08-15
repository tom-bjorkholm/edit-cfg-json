### Telling it which class to edit

The class is told and never guessed. Exactly one of these says where it comes
from, and `--version` is the one of them that edits nothing:

| Option | Meaning |
| --- | --- |
| `--module MODULE` | Importable module that holds the class. This is the ordinary import path, so `PYTHONPATH` reaches a package that is not installed. |
| `--file PATH` | Python file that is not importable as a module. Its own folder goes to the front of the path, so a file that imports its neighbours works; a file that belongs to a package and uses a relative import is refused, with a message saying to use `--module` instead. |
| `--edit-settings` | The class is this editor's own settings, so a settings file is edited in this editor like any other configuration. |
| `--version` | Report the version of this program and of every package it is built on, and which of them PyPI has a newer release of. |

````sh
{{dist_name}} --module myapp.config --class AppConfig -i /etc/myapp.json
{{dist_name}} --file ./somewhere/cfg.py --class AppConfig
{{dist_name}} --edit-settings -o ~/{{home_settings}}
{{dist_name}} --version
````

**Importing a module runs it.** That is the same exposure as running the file
with `python`, and it is not guarded against, because a configuration class is
Python and reaching it means importing the module it is in.

### The rest of the command line

| Option | Meaning |
| --- | --- |
| `--class CLASS` | Name of the `config_as_json.Config` class in that module or file. |
| `--loader NAME` | Name of an `edit_cfg_json.ConfigLoader` there, for a class this editor cannot construct on its own. At least one of `--class` and `--loader` is needed and both are allowed: a loader that chooses its class by looking at the file is held to the one `--class` names. |
| `--descriptions NAME` | Name of an `edit_cfg_json.Descriptions` mapping there, saying what the members are for. Without it the members are shown with whatever their own types say about them. |
| `-i`, `--input` | Configuration file to read. Without it the editor starts from the values the class declares. |
| `-o`, `--output` | Configuration file to write. Without it the input file is written, which is what an editor is normally asked to do. |
| `--policy` | What to do about a declared value the file does not hold: `strict-then-defaults`, which is the default, `strict` or `defaults`. |
| `-c`, `--cfg` | Settings file that this run itself behaves according to, instead of the one the program would look for. |

A member has no docstring at runtime, so what a member is for is either in a
mapping like the one `--descriptions` names or nowhere at all. The docstring of
the configuration class needs no option, because the class carries it.

Whatever a loader needs beyond the four keyword arguments of `ConfigLoader` is
bound where the loader is written, for instance with `functools.partial`,
because a command line cannot supply an argument this library knows nothing
about. `edit_cfg_json.derived_loader` is one line for the ordinary case:

````python
make_config = derived_loader(partial(AppConfig, known_teams=TEAMS))
````

### The settings this program itself runs with

**The command line says what to edit and which files, and never how the editor
behaves.** The extension a configuration uses, the key combinations of the
actions and what becomes of a file that a save writes over are settings, and
`edit_cfg_json.SettingsConfig` is what lets them be written in a file. This
program uses the first of five that answers: the file `-c` names, the file
`$CFG_EDIT_CFG_JSON` names, `~/{{home_settings}}`, `~/.edit-cfg-json.cfg`, or
the values the editor would have chosen anyway. A file that was **named** must
be there; the two in the home folder are the lookup itself, so a step that
finds nothing is simply the next step.

Such a file need name only what it changes, and `-c` is what makes it per run
rather than only per user — an extension is a fact about the class being
edited, so an application whose files are called `.cfg` gets one of its own:

````json
{"actions": {"save": ["ctrl+w"]},
 "file_extension": ".cfg", "extension_enforced": true,
 "backup_suffix": ".old", "backup_count": 3}
````

`--edit-settings` is how one is edited in this editor itself: with `-i` it
reads the file that is there, and with no `-i` it starts from the values the
class declares, which is how a file that does not exist yet is made.

### How the run ends, and two smaller things

Each way of refusing has an exit code of its own, so this program is usable
from a script and from a continuous integration job: `0` when everything it was
asked to do was done, `2` for a command line that is wrong, and a number of its
own for each way a module, a file, a class, a loader or a settings file can
refuse to be read. They are `edit_cfg_json.ExitCode`, where each is named.
Closing an editor is not a failure, so a session the user closed ends with `0`
whatever is left in the fields.

The program is also reachable through the package it belongs to, for a machine
whose script folder is not on `PATH`, and it completes its own options and file
names with [argcomplete](https://pypi.org/project/argcomplete):

````sh
python3 -m {{import_name}} --module myapp.config --class AppConfig
eval "$(register-python-argcomplete {{dist_name}})"
````
