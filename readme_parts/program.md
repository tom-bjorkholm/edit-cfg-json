### Telling it which class to edit

The class is told and never guessed. `--module` names a module that is
importable, `--file` names a Python file that is not, `--edit-settings` says
that the class is this editor's own settings, exactly one of the three is
required, and `--class` names the class in the first two:

````sh
{{dist_name}} --module myapp.config --class AppConfig -i /etc/myapp.json
{{dist_name}} --file ./somewhere/cfg.py --class AppConfig
{{dist_name}} --edit-settings -o ~/{{home_settings}}
````

`--module` uses the ordinary import path, so `PYTHONPATH` reaches a package
that is not installed. `--file` puts the folder of the file at the front of the
path and imports the file by its own name, so a file that imports its
neighbours works — but a file that belongs to a package and uses a relative
import cannot be loaded from a bare path at all, and is refused with a message
saying to use `--module` with `PYTHONPATH` instead.

**Importing a module runs it.** That is the same exposure as running the file
with `python`, and it is not guarded against, because a configuration class is
Python and reaching it means importing the module it is in.

### The rest of the command line

| Option | Meaning |
| --- | --- |
| `-i`, `--input` | Configuration file to read. Without it the editor starts from the values the class declares. |
| `-o`, `--output` | Configuration file to write. Without it the input file is written, which is what an editor is normally asked to do. |
| `--policy` | What to do about a declared value the file does not hold: `strict-then-defaults`, which is the default, `strict` or `defaults`. |
| `--descriptions` | Name of an `edit_cfg_json.Descriptions` mapping beside the class, saying what its members are for. Without it the members are shown with whatever their own types say about them, which for most of them is nothing. |

A member has no docstring at runtime, so what a member is for is either in a
mapping like that or nowhere at all, which is why `--descriptions` exists: it is
the one thing an application knows that this program could not otherwise pass
on. The docstring of the configuration class needs no option, because the class
carries it.

**The command line says what to edit and which files, and never how the editor
behaves.** The file name extension a configuration uses, the key combinations
that run the actions of the editor, and what becomes of a file that a save
writes over are settings, and there is no option for any of them: an
application says them in `edit_cfg_json.Settings` and reaches the editor
through `edit`, and this program reads every one of them from a settings file.
That is the next section, and `-c` is the one option about it.

### The settings this program itself runs with

The same answers `edit_cfg_json.Settings` holds are a configuration class of
their own, `edit_cfg_json.SettingsConfig`, so they can be written in a file.
This program looks for one in five steps, and uses the first that answers:

| Step | Where |
| --- | --- |
| 1 | The file that `-c`/`--cfg` names. |
| 2 | The file that the `CFG_EDIT_CFG_JSON` environment variable names. |
| 3 | `~/{{home_settings}}`, which only this program reads. |
| 4 | `~/.edit-cfg-json.cfg`, which every program of this library reads. |
| 5 | Nowhere: the values the editor would have chosen anyway. |

A file that was **named** — by `-c` or by the environment — must be there, and
a run whose named file is missing or cannot be read as settings stops with an
exit code of its own. The two files of the home folder are the lookup itself,
so a step that finds nothing is simply the next step.

Such a file need name only what it changes. This one moves Save and keeps three
of the files that a save writes over:

````json
{
    "actions": {"save": ["ctrl+w"]},
    "backup_suffix": ".old",
    "backup_count": 3
}
````

A settings file is what one **run** behaves according to, which is what `-c` is
for. The extension is a fact about the class being edited rather than about
whoever is running the program, so an application whose configuration files are
called `.cfg` gets a file of its own beside the one in the home folder:

````json
{"file_extension": ".cfg", "extension_enforced": true}
````

````sh
{{dist_name}} -c ./myapp-editor.cfg --module myapp.config --class AppConfig \
    -i /etc/myapp.cfg
````

An enforced extension refuses an input file that does not have it, and refuses
a destination that does not have it either, so nothing is written. And a file
holding `{}` names nothing at all, which makes it step 5 of the table written
down: naming it is how a run asks for the values the editor would have chosen
anyway, past a file of the home folder that says something else.

`--edit-settings` is how one is edited in this editor itself. With `-i` it reads
the file that is there; with no `-i` it starts from the values the class
declares, which is how a settings file that does not exist yet is made:

````sh
{{dist_name}} --edit-settings -o ~/{{home_settings}}
{{dist_name}} --edit-settings -i ~/{{home_settings}}
````

The settings a run behaves according to are read before anything else, so a
session that is editing a settings file is not the session that file describes:
the next run reads it.

### A class this editor cannot construct on its own

Most configuration classes take the keyword arguments that `config_as_json`
documents and nothing else, and this program constructs them from the signature
it reads. A class that needs an argument of the application's own — a folder, a
connection, the list of names its own validators accept — is reached through
`--loader NAME` instead, which names an `edit_cfg_json.ConfigLoader` in the same
module or file:

````sh
{{dist_name}} --module myapp.config --loader make_config -i /etc/myapp.json
````

Whatever the loader needs beyond the four keyword arguments of that protocol has
to be bound where the loader is written, for instance with
`functools.partial`, because a command line cannot supply an argument this
library knows nothing about. `edit_cfg_json.derived_loader` is one line for the
ordinary case:

````python
make_config = derived_loader(partial(AppConfig, known_teams=TEAMS))
````

At least one of `--class` and `--loader` is needed and both are allowed. A
loader may choose its class by looking at the file it is given, and `--class`
beside it is then how a script says which class it is prepared to go on with:
the run stops with its own exit code if the loader answers with another one.

### How the run ends

The program is meant to be usable from a script, so each way of refusing has an
exit code of its own:

| Code | What it means |
| --- | --- |
| `0` | Everything the program was asked to do was done. |
| `1` | The input file cannot be opened for editing. |
| `2` | The command line itself is wrong. |
| `3` | The module that `--module` names cannot be imported. |
| `4` | The file that `--file` names cannot be read. |
| `5` | That file is not Python that can be imported. |
| `6` | That file needs the package it belongs to. |
| `7` | The module holds no such name. |
| `8` | That name is not a class based on `config_as_json.Config`. |
| `9` | The editor cannot construct that class on its own. |
| `10` | The values are not ones the application would accept. |
| `11` | The output file was asked for and was not written. |
| `12` | The values of that class cannot be written as JSON, so there is nothing to show. |
| `13` | The name that `--loader` names cannot be called at all. |
| `14` | The loader needs arguments that a command line cannot supply. |
| `15` | The loader did not construct the class that `--class` asked for. |
| `16` | The name that `--descriptions` names is no mapping of any kind. |
| `17` | The settings of the program itself cannot be read. |

The numbers are `edit_cfg_json.ExitCode`, so a program that runs this one can
name them instead of writing them out.

Codes `10` and `11` are never answered by this program. They belong to a run
whose backend prints once and returns, which is the
`python3 -m edit_cfg_json.dump` utility of the core package.
A program that gave the user a session ends with success when the user closes
it, whatever is left in the fields, because closing an editor is not a failure.

### If the script folder is not on the path

This program is also reachable through the package it belongs to, which needs
nothing to be on `PATH`:

````sh
python3 -m {{import_name}} --module myapp.config --class AppConfig
````

### Completing the command line

The program completes its own options and file names with
[argcomplete](https://pypi.org/project/argcomplete), which is installed with
it. Register it once for your shell:

````sh
eval "$(register-python-argcomplete {{dist_name}})"
````
