#! /usr/bin/env python3
"""Tests for the keys of the Textual backend and for its command palette."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import asyncio
from textual.widgets import Label
from edit_cfg_json import ActionSettings, EditModel, Settings
from edit_cfg_json_textual.textual_editor import EditorApp, HIDE_COMMAND, \
    SAVE_AS_BOX_ID, SAVE_AS_COMMAND, SAVE_COMMAND, VALIDATE_COMMAND
from example.e01_flat_config import FlatConfig
from .helpers import NO_FILE_TEXT, SAVE_AS_KEY, \
    VALIDATE_ALT_KEY, VALIDATE_KEY, VALID_VERDICT, save_as, saving_of, \
    verdict_of


def test_palette_has_actions() -> None:
    """Test the command palette offers the actions of the editor as well.

    Every terminal can reach the palette, which is what makes it the answer
    for a key combination a terminal cannot encode.
    """
    async def names() -> list[str]:
        """Run the application and read what its palette would offer."""
        app = EditorApp(EditModel(FlatConfig()))
        async with app.run_test():
            return [command.title
                    for command in app.get_system_commands(app.screen)]
    offered = asyncio.run(names())
    assert VALIDATE_COMMAND in offered
    assert SAVE_COMMAND in offered
    assert SAVE_AS_COMMAND in offered
    assert HIDE_COMMAND in offered


def test_palette_keeps_own() -> None:
    """Test the commands of Textual itself are still there beside them."""
    async def names() -> list[str]:
        """Run the application and read what its palette would offer."""
        app = EditorApp(EditModel(FlatConfig()))
        async with app.run_test():
            return [command.title
                    for command in app.get_system_commands(app.screen)]
    assert 'Quit' in asyncio.run(names())


def key_settings(actions: ActionSettings) -> Settings:
    """Return the settings of an application that chose these keys."""
    return Settings(actions=actions)


def _shownkey_settings(app: EditorApp) -> dict[str, str]:
    """Return the key that the footer names for each action it shows."""
    return {binding.action: binding.key
            for (_, binding, enabled, _) in app.screen.active_bindings.values()
            if enabled and binding.show}


def test_chosen_key_saves(tmp_path: Path) -> None:
    """Test a save key the application chose is the one that saves."""
    out_file = tmp_path / 'out.json'
    model = EditModel(FlatConfig(), out_file=out_file,
                      settings=key_settings(ActionSettings(save=('ctrl+w',))))

    async def press(key: str) -> str:
        """Run the application and press one key."""
        app = EditorApp(model)
        async with app.run_test() as pilot:
            await pilot.press(key)
            await pilot.pause()
            return saving_of(app)
    assert asyncio.run(press('ctrl+s')) == f'save to: {out_file}'
    assert asyncio.run(press('ctrl+w')) == f'Saved to {out_file}.'


def test_second_key_works(tmp_path: Path) -> None:
    """Test every key of an action runs it, and the footer names the first."""
    _ = tmp_path

    async def shown() -> tuple[dict[str, str], str]:
        """Run the application, read the footer and use the second key."""
        app = EditorApp(EditModel(FlatConfig()))
        async with app.run_test() as pilot:
            named = _shownkey_settings(app)
            await pilot.press(VALIDATE_ALT_KEY)
            await pilot.pause()
            return named, verdict_of(app)
    named, verdict = asyncio.run(shown())
    assert named['validate'] == VALIDATE_KEY
    assert verdict == VALID_VERDICT


def test_action_without_key(tmp_path: Path) -> None:
    """Test an action the application gave no key keeps its palette entry.

    Taking the key away is not taking the action away, which is what makes
    it safe for an application to take a combination for itself.
    """
    _ = tmp_path

    async def offered() -> tuple[list[str], bool, dict[str, str]]:
        """Run the application, press the key that is gone, and look."""
        app = EditorApp(EditModel(
            FlatConfig(), settings=key_settings(ActionSettings(save_as=()))))
        async with app.run_test() as pilot:
            await pilot.press(SAVE_AS_KEY)
            await pilot.pause()
            asked = bool(app.screen.query(f'#{SAVE_AS_BOX_ID}'))
            return ([command.title
                     for command in app.get_system_commands(app.screen)],
                    asked, _shownkey_settings(app))
    commands, asked, named = asyncio.run(offered())
    assert SAVE_AS_COMMAND in commands
    assert not asked
    assert 'save_as' not in named


def test_cancel_key_chosen(tmp_path: Path) -> None:
    """Test the key that leaves the question is the one that was chosen."""
    out_file = tmp_path / 'chosen.cfg'
    model = EditModel(FlatConfig(),
                      settings=key_settings(ActionSettings(cancel=('f8',))))
    assert asyncio.run(save_as(model, str(out_file), answer='f8')) == \
        NO_FILE_TEXT
    assert model.out_file is None


def test_question_names_key() -> None:
    """Test the question names the key that leaves it, whichever it is."""
    async def prompt(actions: ActionSettings) -> str:
        """Run the application and read what the question says."""
        app = EditorApp(EditModel(FlatConfig(),
                                  settings=key_settings(actions)))
        async with app.run_test() as pilot:
            await pilot.press(SAVE_AS_KEY)
            await pilot.pause()
            return str(app.screen.query_one(Label).content)
    assert 'escape leaves it' in asyncio.run(prompt(ActionSettings()))
    chosen = ActionSettings(cancel=('f8',))
    assert 'f8 leaves it' in asyncio.run(prompt(chosen))
    assert 'leaves it' not in asyncio.run(prompt(ActionSettings(cancel=())))
