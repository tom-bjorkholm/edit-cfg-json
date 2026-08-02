# Example programs for edit-cfg-json

These are small example programs for programmers who know Python well but
have not used `edit_cfg_json` before. Each one takes a
`config_as_json.Config` object and gets an editor for it, and each one adds
exactly one idea to the one before it. Reading them in order is the intended
way to learn the library; running the one that matches the shape of your own
configuration is the intended way to check a detail.

The examples are *not* part of the installed packages. They live in this
repository only.

## The examples

| Example | What it teaches |
| --- | --- |
| [e01_flat_config.py](e01_flat_config.py) | The whole library in three lines: hand a `Config` object to `EditModel` and hand the model to a backend. A flat configuration with one text member and one number member, both editable and both validated by the application's own validation plan. Why the editor never describes the schema a second time, why the values it shows are the declared members in their declared order rather than the sorted keys of the JSON file, and why a value that a validator rewrote is marked. Also the four ways an input file can be refused and the one way it can be incomplete and still be opened. |
| [e02_enum_config.py](e02_enum_config.py) | An `Enum` member and an `IntEnum` member, with no validators at all. An enum is written to the file as the name of its member, so it is edited as text, and a name that is no member is refused by the conversion rather than by a validator. Which of `parse_converters()` and `serialize_converters()` an application has to write, why matching a name is forgiving enough to complete a prefix, and why a half typed name in a field is kept while the same name in a file refuses the file. |

More examples arrive with the steps that they demonstrate: saving,
descriptions and docstrings, field level diagnostics, lists and dicts,
nested `Config` objects, folding, and adding and removing elements.

## Shared command line handling

[cmd_line.py](cmd_line.py) is not a lesson. It is the command line handling
that every example shares, so that each example file can be about the shape
of a configuration instead of about `argparse`. Every example therefore
takes the same options:

| Option | Meaning |
| --- | --- |
| `--ui dump` | Print the model as text. Needs neither a window nor a terminal. |
| `--ui tk` | Open the editor in a Tkinter window. |
| `--ui textual` | Open the editor in the terminal, with Textual. |
| `--set member=value` | Edit one member before showing it. Repeatable. |
| `-i`, `--input` | Configuration file to read. |
| `--policy` | What to do about a declared value the file does not hold. |
| `-o`, `--output` | Configuration file to write. Not supported yet. |

`--ui` is required. There is no default, because which one you want is not
something the example can guess, and a silent choice would teach the wrong
thing about a library that has more than one user interface.

`--ui dump` is not a lesser mode. It renders the model with
`edit_cfg_json.model_as_text`, which lives in the user interface agnostic
core, so it shows exactly the model that the two graphical backends draw.
That is what lets every example be checked without a display.

`-o/--output` is accepted but refused, with a message saying so. It exists
already so that the command line does not have to change again when saving
arrives.

`--policy` is one of `strict-then-defaults`, which is the default, `strict`
or `defaults`. The input files in [examples/data/](../../data/) cover every
outcome of a load, including the three kinds of file that cannot be opened,
so each of them can be tried without writing a file first.

## Running an example

The three packages have to be importable. Inside this repository, use the
virtual environment that the build creates:

```sh
./venv/bin/python3 examples/src/example/e01_flat_config.py --ui dump
./venv/bin/python3 examples/src/example/e01_flat_config.py --ui tk \
    -i examples/data/e01_incomplete.json
```

Outside this repository, install the backend you want and use any Python:

```sh
pip install --upgrade edit-cfg-json-tk edit-cfg-json-textual
python3 e01_flat_config.py --ui textual
```

Every example file can also be imported instead of run, which is what the
tests in [examples/test/test_example/](../../test/test_example/) do.
