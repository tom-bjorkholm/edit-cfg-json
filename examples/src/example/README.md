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
| [e01_flat_config.py](e01_flat_config.py) | The whole library in one call: hand a `Config` object and a backend to `edit()`. A flat configuration with one text member and one number member, both editable and both validated by the application's own validation plan. Why the editor never describes the schema a second time, why the values it shows are the declared members in their declared order rather than the sorted keys of the JSON file, and why a value that a validator rewrote is marked. Also the four ways an input file can be refused, the one way it can be incomplete and still be opened, and the round trip that ends with a written file and the object that was written. |
| [e02_enum_config.py](e02_enum_config.py) | An `Enum` member and an `IntEnum` member, with no validators at all. An enum is written to the file as the name of its member, so it is edited as text, and a name that is no member is refused by the conversion rather than by a validator. Which of `parse_converters()` and `serialize_converters()` an application has to write, why matching a name is forgiving enough to complete a prefix, and why a half typed name in a field is kept while the same name in a file refuses the file. |
| [e03_described_config.py](e03_described_config.py) | Explaining the values to whoever edits them. The docstring of the configuration class labels the object and needs no passing, because the class already has it; the members need a `Descriptions` mapping, because a member docstring does not exist at runtime. Absolute paths as its keys, one member deliberately left undescribed, why a range is explained in words while the names of an enum are not, and the key that hides all of it again. |
| [e04_validated_config.py](e04_validated_config.py) | Saying which member of a configuration is wrong. Why the validation pass that decides the verdict cannot say it, and how walking the same plan a second time can: a validator this application wrote and a validator `config_as_json` ships are attributed the same way, because the editor recognises no validator by type. Also the rule that is about no single member — a `ProjectedWholeConfigValidator` over two of them — which is why the block below the members is still there. |
| [e05_old_format_config.py](e05_old_format_config.py) | Saying that reading the file changed it. An application that renamed a member between versions reads its older files with `ReadOldConfiguration`, and the values then on the screen are not the values in the file. How the editor finds that out for every configuration class — by writing the loaded values back and comparing them with the file — and what a class that declares `auto_ch_hook` can add to it, which is the names of the older keys. Two classes, one of each kind, over the same file. |

More examples arrive with the steps that they demonstrate: lists and dicts,
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
| `--toggle-explain` | Hide the explanations, as the explain key does. |
| `-i`, `--input` | Configuration file to read. |
| `--policy` | What to do about a declared value the file does not hold. |
| `-o`, `--output` | Configuration file to write, or the input file. |
| `--save` | Really write that file. Only with `--ui dump`. |
| `--extension` | File name extension this application uses for its configuration. |
| `--enforce-extension` | Refuse a file that has another extension. |
| `--key ACTION=COMBINATIONS` | Keys of one action of the editor. Repeatable. |

`--ui` is required. There is no default, because which one you want is not
something the example can guess, and a silent choice would teach the wrong
thing about a library that has more than one user interface.

`--ui dump` is not a lesser mode. It runs `edit_cfg_json.DumpEditor`, a backend
that the core itself ships, so it shows exactly the model that the two
graphical backends draw. That is what lets every example be checked without a
display. `StandInUser` beside it in `cmd_line.py` is the other kind of backend:
one written by hand, in a few lines, which does what a user would do — type
into a field, press the explain key, press Save — and then hands the model on.
Between the two of them they say what a backend really is, which is anything
with a `run_editor` method.

`-o/--output` defaults to the input file, which is what an editor is normally
asked to do. With neither, there is nowhere to write, and the two graphical
backends ask for a destination when Save is pressed.

`--save` is the one option that only means something for `--ui dump`. The dump
prints once and the run is then over, so there is no later moment at which a
user could press Save; without `--save` the dump says where it *would* write,
and with it the file is really written. That is what makes the whole round
trip observable without a display.

Every run ends by saying what `edit()` gave back, because "the saved object,
or `None` when nothing was saved" is the contract of this library and a
contract is better seen than read.

`--policy` is one of `strict-then-defaults`, which is the default, `strict`
or `defaults`. The input files in [examples/data/](../../data/) cover every
outcome of a load, including the three kinds of file that cannot be opened,
so each of them can be tried without writing a file first.

`--extension`, `--enforce-extension` and `--key` stand in for the application
that the editor runs inside. A real application does not parse these from a
command line: it knows its own answers and builds one `edit_cfg_json.Settings`
from them. They are options here so that each answer can be tried without a
program per answer.

`--toggle-explain` stands in for the key that shows or hides the explanatory
text, in the same way that `--set` stands in for a user typing into a field.
The editor starts with the explanations shown, so this flag is what shows the
hidden form.

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

## Opening these classes without running an example

Each of the three packages installs a program that takes the *name* of a
configuration class, so any class in this folder can be opened without running
the file it lives in:

```sh
PYTHONPATH=examples/src ./venv/bin/edit-cfg-json \
    --module example.e03_described_config DescribedConfig
PYTHONPATH=examples/src ./venv/bin/edit-cfg-json-textual \
    --module example.e02_enum_config EnumConfig
./venv/bin/edit-cfg-json-tk  --file \
    examples/src/example/e03_described_config.py DescribedConfig        
```

That is a different thing from an example and is worth keeping apart from one.
The examples are about what an application writes; the program is what an
application author gets without writing anything. What the program cannot pass
on is what only the application knows: the description mapping of
[e03_described_config.py](e03_described_config.py) and the `Settings` of
[e01_flat_config.py](e01_flat_config.py). Run the example itself to see those.
