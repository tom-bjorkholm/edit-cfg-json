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
a display: the same edit that a user would type into a field is made from
the command line, and `--ui dump` then prints the edited buffer. A member
the user changed is marked, so the edit is visible even when the new value
looks like the old one.

`--ui dump` validates the buffer before it prints it, so the dump always
says what the application would make of the values it shows. The two
graphical backends do not: there the user asks for a validation pass, with
a button or with a key, because a user who is halfway through typing a
value has not asked anything yet.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
from typing import Optional
from config_as_json import Config
from edit_cfg_json import EditModel, EditorBackend, model_as_text

UI_DUMP = 'dump'
"""Value of `--ui` that prints the model instead of opening a window."""

UI_TK = 'tk'
"""Value of `--ui` that opens the Tkinter editor."""

UI_TEXTUAL = 'textual'
"""Value of `--ui` that opens the Textual editor."""

UI_CHOICES = (UI_DUMP, UI_TK, UI_TEXTUAL)
"""Every accepted value of the required `--ui` option."""

NOT_YET_MESSAGE = '{option} is not supported yet.'
"""Message used to refuse an option that a later step will implement."""

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
        A parser for `--ui`, `--set`, `-i/--input` and `-o/--output`.
    """
    parser = argparse.ArgumentParser(prog=example_name)
    parser.add_argument('--ui', required=True, choices=UI_CHOICES,
                        help='How to show the configuration.')
    parser.add_argument('--set', action='append', dest='settings',
                        metavar='MEMBER=VALUE',
                        help='Edit one member before showing it. Repeatable.')
    parser.add_argument('-i', '--input', default=None,
                        help='Configuration file to read. Not supported yet.')
    parser.add_argument('-o', '--output', default=None,
                        help='Configuration file to write. Not supported yet.')
    return parser


def _refuse_files(parser: argparse.ArgumentParser,
                  parsed: argparse.Namespace) -> None:
    """Refuse the file options, which are not implemented yet.

    The options are accepted already so that the command line of the
    examples does not have to change again when reading and writing files
    arrive. Until then, using one of them is an error: an option that looks
    as if it worked and quietly did nothing would be worse than no option.

    Args:
        parser: Parser used to report the error and exit.
        parsed: Parsed command line of one example run.
    """
    if parsed.input is not None:
        parser.error(NOT_YET_MESSAGE.format(option='-i/--input'))
    if parsed.output is not None:
        parser.error(NOT_YET_MESSAGE.format(option='-o/--output'))


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


def _show_model(ui_name: str, model: EditModel) -> None:
    """Show one model with the user interface that the user selected.

    The text dump validates first, because it prints once and then the run
    is over: there is no later moment at which the user could ask for it.
    The two graphical backends leave the pass to the user, who has a button
    or a key for it.

    Args:
        ui_name: One of the values in `UI_CHOICES`.
        model: Model to show.
    """
    if ui_name == UI_DUMP:
        model.validate()
        print(model_as_text(model))
        return
    editor = _tk_editor() if ui_name == UI_TK else _textual_editor()
    editor.run_editor(model)


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
    _refuse_files(parser=parser, parsed=parsed)
    model = EditModel(config)
    _apply_settings(parser=parser, model=model, settings=parsed.settings)
    _show_model(ui_name=parsed.ui, model=model)
