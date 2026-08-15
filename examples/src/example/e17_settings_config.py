#! /usr/bin/env python3
r"""Example 17: the settings of the editor as part of a configuration.

Every example before this one hands the editor a `edit_cfg_json.Settings` that
it built in Python, which is what an application does when it has already
decided how the editor behaves. This example is about the other case: **the
person running the application decides, and writes it in a file**.

That is what `edit_cfg_json.SettingsConfig` is. It says exactly what `Settings`
says — which key combinations run which action, what a configuration file of
this application is called, and what happens to the file a save writes over —
and it says it as a `config_as_json.Config`, so it can be read from a file,
edited in this editor, and declared as one member of an application's own
configuration class.

## What this example's application looks like

`ToolConfig` below has two members of its own and one more called `editor`,
which holds a whole `SettingsConfig`. It is an ordinary nested configuration
object: `nested_configs()` declares it, the editor shows it as a node with its
own class and its own docstring, and everything inside it belongs to that
class. Nothing about it is special to this library.

The two lines that matter are the declaration:

````python
def nested_configs(self) -> NestedConfigs:
    return {'editor': ConfigNesting(kind=ConfigNestingKind.MEMBER,
                                    config_type=SettingsConfig)}
````

and what the application then hands the editor:

````python
edit(config=ToolConfig(), backend=TkEditor(),
     descriptions=DESCRIPTIONS, settings=ToolConfig().editor.as_settings())
````

`as_settings()` is the whole bridge. A description addresses the whole path to
what it is about, so `edit_cfg_json.described_below(('editor',))` is what puts
this library's own descriptions under the member that holds them — one call
rather than a line per setting that the application would have to keep up to
date with a library it does not own.

## Running it

````sh
cd examples/src/example
python3 e17_settings_config.py --ui tk -i ../../data/e17_tool.json
python3 e17_settings_config.py --ui textual -i ../../data/e17_tool.json
````

Press the fold control on the `editor` row and its class summary is what is
left; open it again and its members are back. Open `actions` inside it and
every action of the editor is a row of its own, with the combinations that run
it below that as a list you can add to and take from. Change `save` to
`ctrl+w`, press Save, and read the file: what you changed is in it. Give two
actions the same combination and press Validate, and the refusal is the one
`edit_cfg_json.ActionSettings` itself makes, shown at the `actions` member.

## A block inside a file is not the same as a file

A **settings file** of its own may name one thing and leave the rest out, and
the editor still shows every setting there is. A settings **block inside
another configuration** may not: `config_as_json` reads a nested configuration
object whole, whatever policy the parse around it was given, so the `editor`
block of `e17_tool.json` holds every member of `SettingsConfig` and a file
that left one of them out would be refused with *No value for actions in JSON
data*. That is why the data file of this example is as long as it is, and it
is a fact about nested configuration objects rather than about this class —
example 9 is where that is taught.

An application that wants its user to name one setting and no more therefore
keeps the settings in a file of their own and reads them with
`edit_cfg_json.load_settings`, which is what the two editor programs do.

## The keys of this session are not the keys in the file

What the editor is running with is the `settings=` argument, and it is read
once when the backend builds its bindings. So editing `editor.actions` here
changes the file and not the session you are editing it in; the next run of the
application reads the file and gets them.

## The other way to reach the same class

The two editor programs edit a settings file of their own with no application
around it at all:

````sh
edit-cfg-json-tk --edit-settings -o ~/.edit-cfg-json-tk.cfg
edit-cfg-json-textual --edit-settings -i ~/.edit-cfg-json-textual.cfg
````

The first makes a settings file that does not exist yet, from the values the
class declares; the second edits one there is. Each program then reads its own
settings from `-c/--cfg`, from `$CFG_EDIT_CFG_JSON`, from its own file in the
home folder, from `~/.edit-cfg-json.cfg`, or from nowhere, in that order.

## Reaching this from a script

`--ui dump` prints the model once and returns, so the whole tree of this
example can be read without a display:

````sh
cd examples/src/example
python3 e17_settings_config.py --ui dump -i ../../data/e17_tool.json \
    --fold editor --fold editor.actions
python3 e17_settings_config.py --ui dump --set editor.backup_count=3
python3 e17_settings_config.py --ui dump --fold editor \
    --fold editor.actions --set editor.actions.save.0=ctrl+q
````

The `--fold` options are what a user would do by pressing the fold control on
the `editor` row and then on the `actions` row inside it: both of them hold
more than a window's worth, so both open folded, and a printout has no control
to press. The last of the three gives two actions one combination, and the
refusal says so at the `actions` member in the words `ActionSettings` uses.
There is nothing to type into and no control to press in a printout, which is
why the two editors above are what this example is really about.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional, TextIO
import sys
from config_as_json import Config, ConfigNesting, ConfigNestingKind, \
    NestedConfigs, PathOrStr, ValidationPlan
from edit_cfg_json import Descriptions, SettingsConfig, described_below

DESCRIPTIONS: Descriptions = {
    ('report_folder',): 'Folder that this tool writes its reports into.',
    ('verbose',): 'Whether the tool says what it is doing while it runs.',
    ('editor',): 'How the configuration editor of this tool behaves.',
    **described_below(('editor',))}
"""What this application says about the members of its configuration.

The application describes its own two members and lets this library describe
the settings of the editor, which is what `described_below` is for: a
description addresses the whole path to what it is about, so every path of
`edit_cfg_json.SETTINGS_DESCRIPTIONS` is the same path with `editor` in front
of it. Writing them out here instead would be a sentence per setting to keep up
to date with a library this application does not own.
"""


class ToolConfig(Config):
    """Everything this tool is configured with.

    Two members of its own and the settings of its configuration editor, which
    is what this example is about: the person running the tool decides which
    keys the editor holds and what happens to the file it writes over, and
    writes that decision in the same file as everything else they configure.
    """

    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Initialize the configuration with its default values.

        Args:
            from_json_data_text: Optional JSON text to parse directly.
            from_json_filename: Optional path to a JSON file to read.
            stderr_file: Stream used for user-facing diagnostics.
        """
        self.report_folder: str = '/var/lib/tool/reports'
        self.verbose: bool = False
        # One member holding one nested configuration object, which is
        # declared below. `SettingsConfig` is constructed here exactly as any
        # other nested class would be, and it holds the values that
        # `edit_cfg_json.Settings` declares.
        self.editor: SettingsConfig = SettingsConfig()
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file)

    def nested_configs(self) -> NestedConfigs:
        """Return the one member of this class that holds a nested object.

        `MEMBER` is the plainest of the five nesting kinds: this member holds
        one object of that class and always holds one. Example 9 is where the
        nesting kinds are really taught.
        """
        return {'editor': ConfigNesting(kind=ConfigNestingKind.MEMBER,
                                        config_type=SettingsConfig)}

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return no extra rules for the two members of this class.

        The `editor` member needs none from here: `SettingsConfig` has rules
        of its own, and `config_as_json` runs the plan of every nested object
        while it reads the file. That is what makes a combination given to two
        actions refusable without this class knowing what an action is.
        """
        _ = stderr_file
        return []


def main(args: Optional[list[str]] = None) -> None:
    """Run this example from the command line.

    Args:
        args: Optional replacement for `sys.argv[1:]`, mainly for tests.
    """
    # The import is inside the function so that running this file directly
    # works. The block at the end of the file puts the examples source folder
    # on sys.path first, and only after that is `example.cmd_line` importable.
    # pylint: disable-next=import-outside-toplevel
    from example.cmd_line import run_example
    config = ToolConfig()
    # This is the bridge, and it is one call: the editor takes the frozen
    # `Settings` that every entry point of this library takes, and the object
    # in the configuration answers with one. A real application reads its
    # configuration file first and hands over the settings that file held;
    # this example is started from a command line that may name no file, so
    # the declared values are what it hands over when there is none.
    settings = config.editor.as_settings()
    run_example(example_name='e17_settings_config', config=config, args=args,
                descriptions=DESCRIPTIONS, settings=settings)


# The usual guard, so that importing this module from a test runs nothing.
if __name__ == '__main__':
    # Running a file directly puts only that file's own folder on sys.path,
    # so the `example` package this file belongs to would not be importable.
    # Adding the folder above it makes both ways of using this file work:
    # `python3 examples/src/example/e17_settings_config.py` and
    # `from example import e17_settings_config` from a test.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    main()
