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


def _create_parser(example_name: str) -> argparse.ArgumentParser:
    """Return the argument parser that all example programs share.

    Args:
        example_name: Name of the example, used in help and error text.

    Returns:
        A parser for `--ui`, `-i/--input` and `-o/--output`.
    """
    parser = argparse.ArgumentParser(prog=example_name)
    parser.add_argument('--ui', required=True, choices=UI_CHOICES,
                        help='How to show the configuration.')
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

    Args:
        ui_name: One of the values in `UI_CHOICES`.
        model: Model to show.
    """
    if ui_name == UI_DUMP:
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
    _show_model(ui_name=parsed.ui, model=EditModel(config))
