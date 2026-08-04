### Telling it which class to edit

The class is told and never guessed. `--module` names a module that is
importable, `--file` names a Python file that is not, exactly one of the two is
required, and the class itself is the one positional argument:

````sh
{{dist_name}} --module myapp.config AppConfig -i /etc/myapp.json
{{dist_name}} --file ./somewhere/cfg.py AppConfig
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

An application that has more to say about its own configuration — the file name
extension it uses, the key combinations its own user interface has taken, and
what its individual members mean — says it in `edit_cfg_json.Settings` and in a
description mapping, and gets there through `edit` rather than through this
program. Options for those are what the next version of this program adds.

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

The numbers are `edit_cfg_json.ExitCode`, so a program that runs this one can
name them instead of writing them out.

### If the script folder is not on the path

Every one of these programs is also reachable through the package it belongs
to, which needs nothing to be on `PATH`:

````sh
python3 -m {{import_name}} --module myapp.config AppConfig
````

### Completing the command line

The program completes its own options and file names with
[argcomplete](https://pypi.org/project/argcomplete), which is installed with
it. Register it once for your shell:

````sh
eval "$(register-python-argcomplete {{dist_name}})"
````
