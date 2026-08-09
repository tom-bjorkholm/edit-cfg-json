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
| [e06_factory_config.py](e06_factory_config.py) | A configuration class that the editor cannot construct, because it is told which teams exist and only the application knows that. `edit_cfg_json.ConfigLoader` is how an application says how its class is built, `derived_loader` is the one line that says it for a class plus a bound argument, and the same file without a loader is refused with the message that names the class. Also what a loader is *not* needed for: editing, validating and saving work on the object it made. |
| [e07_chosen_class.py](e07_chosen_class.py) | A loader that chooses its class by looking at the JSON, written out by hand, for an application with two modes whose files have the same shape and different rules. The two rules that make it work: the class is chosen when the file is loaded and the session then edits that class, and a value that would select the other class is refused by the save rather than followed. |
| [e08_lists_and_dicts.py](e08_lists_and_dicts.py) | A member that holds a list or a dict, shown as a tree of rows with a field at every value. How a value inside one is addressed, by the whole path to it, which is also how one description can reach every element of a list. Folding a container away and opening it again, and why a long one opens folded. What a validator that sorts and de-duplicates a list does to the rows, and why what a validator of a container refuses is shown at the container and not at one value inside it. |
| [e09_nested_config.py](e09_nested_config.py) | A member that holds a nested `Config` object, shown as the object it is rather than as the dict it serializes to: its class where its value would be, its own docstring below it, its own members as the rows under that, and a badge saying what it is on its own. Why everything inside it belongs to its own class, why a description path is the one thing that crosses that boundary, and why an object can be valid on its own inside a configuration that is refused. Also an optional member holding no object at all. |
| [e10_config_containers.py](e10_config_containers.py) | A list whose elements are configuration objects and a dict whose values are them, which is what a configuration of any real size is made of. The member stays an ordinary container that folds and says how much it holds, and each object inside it is a node of its own. How one description with the `'['` step reaches every element and every value, and how naming every step singles one of them out again. Why a container of objects opens folded at three of them, why the rule of the element class runs once per object, and why a rule about all of them belongs to the class holding them. |
| [e11_add_remove.py](e11_add_remove.py) | Changing **how many** things a member holds: adding an element, removing one and moving one along a list. Where a new element comes from — the class a nesting declaration names, or the elements the class declares for the member itself — and the one member that has neither, which says so instead of guessing. Also the three dicts that cannot gain a key and the three different reasons why, and an optional member that is given its object and put back to holding none. |

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
| `--set member=value` | Edit one value before showing it. Repeatable. A value inside a list or a dict is named by the whole path to it, with a dot between the steps. |
| `--add PATH` | Add one element to a list. `--add PATH=KEY` adds one entry to a dict, which needs a key. Repeatable. |
| `--remove PATH` | Remove one element or entry. Repeatable. |
| `--move PATH=up` | Move one element of a list one place earlier, or `=down` one place later. Repeatable. |
| `--toggle-explain` | Hide the explanations, as the explain key does. |
| `--toggle-fold` | Fold every list and dict away, as the fold key does. |
| `--fold PATH` | Fold one list or dict away, or open it. Repeatable. |
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

`--add`, `--remove` and `--move` stand in for pressing the controls on a row,
and they are applied before `--set`, so that a value inside a new element can
be typed into in the same run. That is also the order a user would work in.

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
    --module example.e03_described_config --class DescribedConfig
PYTHONPATH=examples/src ./venv/bin/edit-cfg-json-textual \
    --module example.e02_enum_config --class EnumConfig
./venv/bin/edit-cfg-json-tk --file \
    examples/src/example/e03_described_config.py --class DescribedConfig
```

A class that the editor cannot construct on its own is named through its
loader instead, and `--class` beside it says which class the run insists on
getting:

```sh
PYTHONPATH=examples/src ./venv/bin/edit-cfg-json \
    --module example.e06_factory_config --loader team_loader
PYTHONPATH=examples/src ./venv/bin/edit-cfg-json-tk \
    --module example.e07_chosen_class --loader chosen_config \
    --class Cad3DConfig -i examples/data/e07_model.json
```

That is a different thing from an example and is worth keeping apart from one.
The examples are about what an application writes; the program is what an
application author gets without writing anything. What the program cannot pass
on is what only the application knows: the description mapping of
[e03_described_config.py](e03_described_config.py) and the `Settings` of
[e01_flat_config.py](e01_flat_config.py). Run the example itself to see those.
