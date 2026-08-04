#! /usr/bin/env python3
"""Command line handling shared by all example programs.

The examples in this repository teach how an application hands its own
configuration object to `edit_cfg_json`. They are not about command line
parsing, so the parsing lives here once and every example reuses it. That
keeps each example file about the shape of a configuration instead of about
`argparse`.

One required option decides how the configuration is shown:

| `--ui` value | What it does                                    |
| ------------ | ----------------------------------------------- |
| `dump`       | prints the model as text, needs no display      |
| `tk`         | opens the Tkinter editor in a window            |
| `textual`    | opens the Textual editor in the terminal        |

The text dump is one of the `--ui` values rather than a separate switch,
because the three are alternatives: there is no situation in which one run
should both open a window and print the model. Making them one option also
means that `argparse` itself refuses a missing or an unknown choice, so this
module needs no hand written check for either.

The text dump is not a lesser mode. It is `edit_cfg_json.DumpEditor`, a
backend that the core itself ships, so `--ui dump` shows exactly the model
that the two graphical backends render. It is the backend of the
`edit-cfg-json` program as well, which is what the core installs for an
application author who would rather not write a program at all.

`StandInUser` below it is the other kind of backend: one written by hand, in a
few lines, for this repository's own purposes. Between the two of them they
say what a backend really is — anything with a `run_editor` method.

The repeatable `--set member=value` option edits the buffer before anything
is shown. It is what lets an editing step be demonstrated and tested without
a display: the same edit that a user would type into a field is made from the
command line, and `--ui dump` then prints the edited buffer. A member the user
changed is marked, so the edit is visible even when the new value looks like
the old one.

`-i/--input` names the file that the values are read from, and `--policy`
says what to do about a declared value that the file does not hold. There is
a file for every case in [examples/data/](../../data/), including the ones
that cannot be opened, so each of them can be tried without writing a file
first. A file that cannot be opened is a message and an exit, and never an
editor that quietly shows the default values instead of what was asked for.

`-o/--output` names the file that is written, and defaults to the input file,
which is what an editor is normally asked to do. With neither, there is
nowhere to write, and the two graphical backends ask for a destination when
Save is pressed.

An example that has something to say about the members it declares hands a
description mapping to `run_example`, which passes it on to `edit()`. There is
no command line option for that, because it is not the kind of thing a command
line could supply: it is what the application knows about its own
configuration, and the editor has no way of finding it out.

`--toggle-explain` stands in for the key that shows or hides the explanatory
text, in the same way that `--set` stands in for a user typing into a field.
The editor starts with the explanations shown, so this flag is what shows the
hidden form: the label of the configuration keeps its one line summary, and
the rest of the class docstring and the description of every member go away.

`--ui dump` validates the buffer before it prints it, so the dump always
says what the application would make of the values it shows. The two
graphical backends do not: there the user asks for a validation pass, with
a button or with a key, because a user who is halfway through typing a
value has not asked anything yet.

`--save` is the one option that only means something for `--ui dump`. The
dump prints once and the run is then over, so there is no later moment at
which a user could press Save; without `--save` the dump says where it would
write, and with it the file is really written. That is what makes the whole
round trip observable without a display.

`--extension`, `--enforce-extension` and `--key` stand in for the
application the editor runs inside. A real application does not parse these
from a command line: it knows its own answers and builds one
`edit_cfg_json.Settings` from them. They are options here so that every
answer can be tried without writing a program per answer.

`--key ACTION=COMBINATIONS` names one action of the editor and the key
combinations that run it, separated by commas. `--key save=ctrl+w` moves
Save, and `--key save_as=` takes the key away from Save as altogether and
leaves the action reachable through the button and the command palette. An
action that no `--key` names keeps its default.

The settings are passed here as a `Settings` object, which is what an
application that knows its own answers does. `edit()` also accepts a
callable that answers with a `Settings`, which is worth having when the
answers are not ready at the moment of the call, and is documented at
`edit_cfg_json.SettingsSource`.

Every run ends by saying what `edit()` gave back, because "the saved object,
or `None` when nothing was saved" is the contract of this library and a
contract is better seen than read.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
from dataclasses import fields
from typing import Optional
from config_as_json import Config
from edit_cfg_json import ActionSettings, ConfigLoadError, Descriptions, \
    DumpEditor, EditModel, EditorBackend, Settings, add_file_options, edit, \
    named_policy

UI_DUMP = 'dump'
"""Value of `--ui` that prints the model instead of opening a window."""

UI_TK = 'tk'
"""Value of `--ui` that opens the Tkinter editor."""

UI_TEXTUAL = 'textual'
"""Value of `--ui` that opens the Textual editor."""

UI_CHOICES = (UI_DUMP, UI_TK, UI_TEXTUAL)
"""Every accepted value of the required `--ui` option."""

DUMP_ONLY_MESSAGE = '--save only means something together with --ui dump.'
"""Message used to refuse `--save` where a Save button or key exists."""

SAVED_MESSAGE = 'edit() returned the saved {name} object.'
"""Message that says the editor handed a written configuration back."""

NOTHING_MESSAGE = 'edit() returned None, so nothing was saved.'
"""Message that says the session ended without writing anything."""

SET_FORM_MESSAGE = '--set needs member=value, and got {setting}.'
"""Message used to refuse a `--set` value that names no member."""

NO_MEMBER_MESSAGE = '{name} is not a member of this configuration.'
"""Message used to refuse a `--set` of a member that does not exist."""

NOT_EDITABLE_MESSAGE = '{name} cannot be edited yet.'
"""Message used to refuse a `--set` of a list member or a dict member."""

KEY_FORM_MESSAGE = ('--key needs one of {names} followed by =combinations, '
                    'and got {value}.')
"""Message used to refuse a `--key` that names no action of the editor."""


def _create_parser(example_name: str) -> argparse.ArgumentParser:
    """Return the argument parser that all example programs share.

    Args:
        example_name: Name of the example, used in help and error text.

    Returns:
        A parser for `--ui`, `--set`, `--toggle-explain`, `--policy`,
        `--save`, `--extension`, `--enforce-extension`, `--key`,
        `-i/--input` and `-o/--output`.
    """
    # The last three of those are added by the core, in `add_file_options`,
    # because the programs the core installs have the very same three options
    # and they have to mean the same thing here as they do there.
    parser = argparse.ArgumentParser(prog=example_name)
    parser.add_argument('--ui', required=True, choices=UI_CHOICES,
                        help='How to show the configuration.')
    parser.add_argument('--set', action='append', dest='edits',
                        metavar='MEMBER=VALUE',
                        help='Edit one member before showing it. Repeatable.')
    parser.add_argument('--toggle-explain', action='store_true',
                        help='Hide the explanations, as the key does.')
    parser.add_argument('--extension', default=None,
                        help='File name extension this application uses.')
    parser.add_argument('--enforce-extension', action='store_true',
                        help='Refuse a file with another extension.')
    parser.add_argument('--key', action='append', dest='keys',
                        metavar='ACTION=COMBINATIONS',
                        help='Keys of one action of the editor. Repeatable.')
    parser.add_argument('--save', action='store_true',
                        help='Write the output file. Only with --ui dump.')
    add_file_options(parser)
    return parser


def _refuse_save(parser: argparse.ArgumentParser,
                 parsed: argparse.Namespace) -> None:
    """Refuse `--save` where the user interface has a Save of its own.

    An option that looked as if it worked and quietly did nothing would be
    worse than no option.

    Args:
        parser: Parser used to report the error and exit.
        parsed: Parsed command line of one example run.
    """
    if parsed.save and parsed.ui != UI_DUMP:
        parser.error(DUMP_ONLY_MESSAGE)


def _set_member(parser: argparse.ArgumentParser, model: EditModel, name: str,
                text: str) -> None:
    """Edit one member of the buffer, or say why it cannot be edited.

    The model is addressed by the path of a member and not by its name, and
    every path of a flat configuration has exactly one step. The further
    steps arrive with the members that need them, which are the ones inside
    lists, dicts and nested configuration objects.

    The model tells the two failures apart, and so does this: a name that is
    not a member at all is a different mistake from a member that this
    version of the editor cannot edit yet.

    Args:
        parser: Parser used to report the error and exit.
        model: Model whose buffer is edited.
        name: Name of the member to edit.
        text: Text to set the member to, exactly as a field would hold it.
    """
    try:
        model.set_text(path=(name,), text=text)
    except KeyError:
        parser.error(NO_MEMBER_MESSAGE.format(name=name))
    except ValueError:
        parser.error(NOT_EDITABLE_MESSAGE.format(name=name))


def _apply_edits(parser: argparse.ArgumentParser, model: EditModel,
                 edits: Optional[list[str]]) -> None:
    """Apply every `--set member=value` of one command line to the buffer.

    Args:
        parser: Parser used to report the error and exit.
        model: Model whose buffer is edited.
        edits: The `--set` values, or None when the option was not used.
    """
    for setting in edits or []:
        name, separator, text = setting.partition('=')
        if not separator:
            parser.error(SET_FORM_MESSAGE.format(setting=setting))
        _set_member(parser=parser, model=model, name=name, text=text)


def _action_keys(parser: argparse.ArgumentParser,
                 values: Optional[list[str]]) -> ActionSettings:
    """Return the key combinations that every `--key` of one run asks for.

    The names that are accepted are the attributes of `ActionSettings`
    itself, so this cannot fall behind the actions the editor has.

    Args:
        parser: Parser used to report the error and exit.
        values: The `--key` values, or None when the option was not used.

    Returns:
        The keys of every action, with the default of each action the
        command line said nothing about.
    """
    names = {field.name for field in fields(ActionSettings)}
    chosen: dict[str, tuple[str, ...]] = {}
    for value in values or []:
        name, separator, keys = value.partition('=')
        if not separator or name not in names:
            parser.error(KEY_FORM_MESSAGE.format(
                value=value, names=', '.join(sorted(names))))
        chosen[name] = tuple(key for key in keys.split(',') if key)
    try:
        actions = ActionSettings(**chosen)
    except ValueError as error:
        # `parser.error` writes the message and ends the process, so nothing
        # below this runs when two actions were given the same key.
        parser.error(str(error))
    return actions


def _settings(parser: argparse.ArgumentParser,
              parsed: argparse.Namespace) -> Settings:
    """Return what this run says the application has already decided.

    A real application does not build this from a command line. It knows
    its own answers, and either passes one object like this one or a
    callable that answers with one.

    Args:
        parser: Parser used to report the error and exit.
        parsed: Parsed command line of one example run.

    Returns:
        The settings that this run hands to the editor.
    """
    try:
        settings = Settings(actions=_action_keys(parser=parser,
                                                 values=parsed.keys),
                            file_extension=parsed.extension,
                            extension_enforced=parsed.enforce_extension)
    except ValueError as error:
        # `parser.error` writes the message and ends the process, so nothing
        # below this runs when the extension is text that names none.
        parser.error(str(error))
    return settings


class StandInUser:  # pylint: disable=too-few-public-methods
    """A backend that does what a user would, and then runs another one.

    What it does belongs on this side of `edit()` rather than before it,
    because `edit()` owns the model: it reads the file and builds the model
    itself, which is what gives a load its policy and its change reporting.
    `--set` stands in for a user typing, `--toggle-explain` for a user pressing
    the explain key, and `--save` for a user pressing Save, and all three of
    those happen in an editor that is already open.

    Saving is here rather than in `DumpEditor` for the same reason as the other
    two: the dump prints the model it is given, and pressing Save is not
    printing. A dump does print once and return, though, so `--save` is the
    only way a user could ever ask it for one, which is why the command line
    accepts the option for `--ui dump` alone.
    """

    def __init__(self, inner: EditorBackend, parser: argparse.ArgumentParser,
                 parsed: argparse.Namespace) -> None:
        """Remember what to do to the model and what to run afterwards.

        Args:
            inner: Backend that shows the model once it has been edited.
            parser: Parser used to report a bad `--set` and exit.
            parsed: Parsed command line of one example run.
        """
        self._inner = inner
        self._parser = parser
        self._parsed = parsed

    def run_editor(self, model: EditModel) -> None:
        """Act as the user would, and hand the model to the real backend.

        Args:
            model: Model to edit and then to show.
        """
        _apply_edits(parser=self._parser, model=model,
                     edits=self._parsed.edits)
        if self._parsed.toggle_explain:
            model.toggle_explanations()
        if self._parsed.save:
            model.save()
        self._inner.run_editor(model)


def _tk_editor() -> EditorBackend:
    """Return the Tkinter backend, imported only when it is needed.

    The import is inside this function on purpose. `tkinter` cannot be
    installed from PyPI, so a machine can have a perfectly good Python
    without it. An example that imported the Tkinter backend at module level
    would then fail even for `--ui textual`.

    Returns:
        A backend that satisfies the `EditorBackend` protocol.
    """
    # pylint: disable-next=import-outside-toplevel
    from edit_cfg_json_tk import TkEditor
    return TkEditor()


def _textual_editor() -> EditorBackend:
    """Return the Textual backend, imported only when it is needed.

    Returns:
        A backend that satisfies the `EditorBackend` protocol.
    """
    # pylint: disable-next=import-outside-toplevel
    from edit_cfg_json_textual import TextualEditor
    return TextualEditor()


def _selected_backend(parsed: argparse.Namespace) -> EditorBackend:
    """Return the backend that the `--ui` value of one run asks for.

    Args:
        parsed: Parsed command line of one example run.

    Returns:
        A backend that satisfies the `EditorBackend` protocol.
    """
    if parsed.ui == UI_DUMP:
        return DumpEditor()
    return _tk_editor() if parsed.ui == UI_TK else _textual_editor()


def _result_text(saved: Optional[Config]) -> str:
    """Return what one editing session gave back, as a line of text.

    Args:
        saved: What `edit()` returned.

    Returns:
        A line naming the saved configuration class, or saying there is none.
    """
    if saved is None:
        return NOTHING_MESSAGE
    return SAVED_MESSAGE.format(name=type(saved).__name__)


def _run_editor(parser: argparse.ArgumentParser, config: Config,
                backend: EditorBackend, parsed: argparse.Namespace,
                descriptions: Optional[Descriptions]) -> Optional[Config]:
    """Run one editing session, or say why the input file cannot be opened.

    This is the whole of what an application does: it hands over its own
    configuration object, what it says about the members of it, the files it
    wants read and written, the policy it wants applied, what it has already
    decided about keys and file names, and the user interface to use. The
    editor does the rest, and gives back what it wrote.

    Args:
        parser: Parser used to report the error and exit.
        config: Configuration object of the example. It is not modified.
        backend: User interface to run the session in.
        parsed: Parsed command line of one example run.
        descriptions: What the example says about its members, or None.

    Returns:
        The configuration object that was saved, or None when the session
        ended without writing anything.
    """
    try:
        saved = edit(config=config, backend=backend, in_file=parsed.input,
                     descriptions=descriptions, out_file=parsed.output,
                     policy=named_policy(parsed.policy),
                     settings=_settings(parser=parser, parsed=parsed))
    except ConfigLoadError as error:
        # `parser.error` writes the message and ends the process, so nothing
        # below this runs when the input file cannot be opened.
        parser.error(str(error))
    return saved


def run_example(example_name: str, config: Config,
                args: Optional[list[str]] = None,
                descriptions: Optional[Descriptions] = None) -> None:
    """Run one example program from the command line.

    This is the whole contract between an example and this module: the
    example says what it is called, hands over the configuration object it
    wants to edit, and says what it has to say about the members of it.

    Args:
        example_name: Name of the example, used in help and error text.
        config: Configuration object that the example wants to edit. The
            editor never modifies it.
        args: Optional replacement for `sys.argv[1:]`, mainly for tests.
        descriptions: What this example says about the members it declares,
            or None for an example that says nothing about them.
    """
    parser = _create_parser(example_name)
    parsed = parser.parse_args(args)
    _refuse_save(parser=parser, parsed=parsed)
    backend = StandInUser(inner=_selected_backend(parsed), parser=parser,
                          parsed=parsed)
    print(_result_text(_run_editor(parser=parser, config=config,
                                   backend=backend, parsed=parsed,
                                   descriptions=descriptions)))
