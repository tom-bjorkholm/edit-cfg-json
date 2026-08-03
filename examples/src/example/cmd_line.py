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

The text dump is not a lesser mode. It is `edit_cfg_json.model_as_text`,
which lives in the user interface agnostic core, so `--ui dump` shows
exactly the model that the two graphical backends render.

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

Every run ends by saying what `edit()` gave back, because "the saved object,
or `None` when nothing was saved" is the contract of this library and a
contract is better seen than read.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
from typing import Optional
from config_as_json import Config
from edit_cfg_json import ConfigLoadError, EditModel, EditorBackend, \
    LoadPolicy, edit, model_as_text

UI_DUMP = 'dump'
"""Value of `--ui` that prints the model instead of opening a window."""

UI_TK = 'tk'
"""Value of `--ui` that opens the Tkinter editor."""

UI_TEXTUAL = 'textual'
"""Value of `--ui` that opens the Textual editor."""

UI_CHOICES = (UI_DUMP, UI_TK, UI_TEXTUAL)
"""Every accepted value of the required `--ui` option."""

DEFAULT_POLICY_NAME = 'strict-then-defaults'
"""Value of `--policy` used when the command line names none of them.

It is the default of the editor as well, so a run that says nothing about the
policy loads strictly and falls back to the declared defaults when the file
turns out to be incomplete.
"""

POLICIES = {DEFAULT_POLICY_NAME: LoadPolicy.STRICT_THEN_DEFAULTS,
            'strict': LoadPolicy.STRICT,
            'defaults': LoadPolicy.DEFAULTS}
"""Every accepted value of `--policy`, and what the editor makes of it."""

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


def _create_parser(example_name: str) -> argparse.ArgumentParser:
    """Return the argument parser that all example programs share.

    Args:
        example_name: Name of the example, used in help and error text.

    Returns:
        A parser for `--ui`, `--set`, `--policy`, `--save`, `-i/--input` and
        `-o/--output`.
    """
    parser = argparse.ArgumentParser(prog=example_name)
    parser.add_argument('--ui', required=True, choices=UI_CHOICES,
                        help='How to show the configuration.')
    parser.add_argument('--set', action='append', dest='settings',
                        metavar='MEMBER=VALUE',
                        help='Edit one member before showing it. Repeatable.')
    parser.add_argument('--policy', default=DEFAULT_POLICY_NAME,
                        choices=tuple(POLICIES),
                        help='What to do about values the file leaves out.')
    parser.add_argument('--save', action='store_true',
                        help='Write the output file. Only with --ui dump.')
    parser.add_argument('-i', '--input', default=None,
                        help='Configuration file to read.')
    parser.add_argument('-o', '--output', default=None,
                        help='Configuration file to write, or the input file.')
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


def _apply_settings(parser: argparse.ArgumentParser, model: EditModel,
                    settings: Optional[list[str]]) -> None:
    """Apply every `--set member=value` of one command line to the buffer.

    Args:
        parser: Parser used to report the error and exit.
        model: Model whose buffer is edited.
        settings: The `--set` values, or None when the option was not used.
    """
    for setting in settings or []:
        name, separator, text = setting.partition('=')
        if not separator:
            parser.error(SET_FORM_MESSAGE.format(setting=setting))
        _set_member(parser=parser, model=model, name=name, text=text)


class DumpEditor:  # pylint: disable=too-few-public-methods
    """A backend that prints the model instead of opening a window.

    It is a backend and not a special case beside the two real ones, which
    is worth noticing: `EditorBackend` asks for one method, so anything with
    that method can be handed to `edit()`. That is also how an application
    could write a backend of its own.
    """

    def __init__(self, save: bool) -> None:
        """Say whether this dump writes the output file or only reports it.

        Args:
            save: Whether to write the file. A dump prints once and the run
                is then over, so there is no later moment at which the user
                could ask for it.
        """
        self._save = save

    def run_editor(self, model: EditModel) -> None:
        """Validate or save, and print the model as text.

        Saving validates too, so either way the printed model says what the
        application makes of the values in it.

        Args:
            model: Model to print.
        """
        if self._save:
            model.save()
        else:
            model.validate()
        print(model_as_text(model))


class SettingEditor:  # pylint: disable=too-few-public-methods
    """A backend that types the `--set` edits in and then runs another one.

    The edits belong on this side of `edit()` rather than before it, because
    `edit()` owns the model: it reads the file and builds the model itself,
    which is what gives a load its policy and its change reporting. `--set`
    stands in for a user typing, and a user types into an editor that is
    already open.
    """

    def __init__(self, inner: EditorBackend, parser: argparse.ArgumentParser,
                 settings: Optional[list[str]]) -> None:
        """Remember the edits to make and the backend to run afterwards.

        Args:
            inner: Backend that shows the model once it has been edited.
            parser: Parser used to report a bad `--set` and exit.
            settings: The `--set` values, or None when there were none.
        """
        self._inner = inner
        self._parser = parser
        self._settings = settings

    def run_editor(self, model: EditModel) -> None:
        """Apply every `--set` and then hand the model to the real backend.

        Args:
            model: Model to edit and then to show.
        """
        _apply_settings(parser=self._parser, model=model,
                        settings=self._settings)
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
        return DumpEditor(save=parsed.save)
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
                backend: EditorBackend,
                parsed: argparse.Namespace) -> Optional[Config]:
    """Run one editing session, or say why the input file cannot be opened.

    This is the whole of what an application does: it hands over its own
    configuration object, the files it wants read and written, the policy it
    wants applied and the user interface to use. The editor does the rest,
    and gives back what it wrote.

    Args:
        parser: Parser used to report the error and exit.
        config: Configuration object of the example. It is not modified.
        backend: User interface to run the session in.
        parsed: Parsed command line of one example run.

    Returns:
        The configuration object that was saved, or None when the session
        ended without writing anything.
    """
    try:
        saved = edit(config=config, backend=backend, in_file=parsed.input,
                     out_file=parsed.output, policy=POLICIES[parsed.policy])
    except ConfigLoadError as error:
        # `parser.error` writes the message and ends the process, so nothing
        # below this runs when the input file cannot be opened.
        parser.error(str(error))
    return saved


def run_example(example_name: str, config: Config,
                args: Optional[list[str]] = None) -> None:
    """Run one example program from the command line.

    This is the whole contract between an example and this module: the
    example says what it is called and hands over the configuration object
    it wants to edit.

    Args:
        example_name: Name of the example, used in help and error text.
        config: Configuration object that the example wants to edit. The
            editor never modifies it.
        args: Optional replacement for `sys.argv[1:]`, mainly for tests.
    """
    parser = _create_parser(example_name)
    parsed = parser.parse_args(args)
    _refuse_save(parser=parser, parsed=parsed)
    backend = SettingEditor(inner=_selected_backend(parsed), parser=parser,
                            settings=parsed.settings)
    print(_result_text(_run_editor(parser=parser, config=config,
                                   backend=backend, parsed=parsed)))
