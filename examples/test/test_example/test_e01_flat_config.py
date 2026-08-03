#! /usr/bin/env python3
"""Tests for example e01_flat_config."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import json
import pytest
from example import e01_flat_config
from .helpers import DUMP_TAIL, data_file, dump, head, input_tail, \
    open_tk_ui, refused, saved_tail, textual_titles

VALID_LINE = 'validation: valid'
"""Line that `--ui dump` ends with for a buffer the example accepts."""

REFUSED_LINE = 'validation: invalid, see answer'
"""Line that `--ui dump` ends with when the number member is refused.

What the application said about that member is shown beside it, so this line
only names it: a configuration too tall for a window would otherwise leave
the user hunting for the field the refusal is about.
"""

VALID_END = f'{VALID_LINE}\n{DUMP_TAIL}'
"""How a dump of an accepted buffer with no output file ends."""

HEAD = head(e01_flat_config.FlatConfig())
"""The lines that every dump of this example begins with.

The example is labelled by the name of its class and the docstring of that
class, which the editor reads without being told anything.
"""

EDITED_HEAD = head(e01_flat_config.FlatConfig(), edited=True)
"""The same lines while the buffer holds something worth saving."""

EXPECTED_DUMP = f'{HEAD}\nname = Flat example\nanswer = 42\n{VALID_END}'
"""Text that `--ui dump` is expected to print for the default values."""

FILLED_LINE = ('This file did not hold every value. What it left out was '
               'filled in from the defaults, and is marked.')
"""What the example says about a file that leaves a value out."""

REFUSED_FILES = [('unknown key', 'e01_unknown_key.json',
                  'holds a key that this configuration does not have'),
                 ('not json', 'e01_not_json.json',
                  'does not hold configuration that can be read'),
                 ('refused value', 'e01_bad_value.json',
                  'values in this file are not valid'),
                 ('no such file', 'e01_missing.json', 'cannot be read')]
"""Every input file of this example that cannot be opened, and why.

The first item of each is the name of the case, which pytest uses to
identify it, and the last is text the refusal has to contain.
"""


def _dump(capsys: pytest.CaptureFixture[str], *settings: str) -> str:
    """Run this example with `--ui dump` and return what it printed."""
    return dump(e01_flat_config.main, capsys, *settings)


def _refused(capsys: pytest.CaptureFixture[str], *arguments: str) -> str:
    """Run this example, expect it to refuse, and return its error text."""
    return refused(e01_flat_config.main, capsys, *arguments)


def test_dump(capsys: pytest.CaptureFixture[str]) -> None:
    """Test --ui dump prints both members with their default values."""
    assert _dump(capsys) == EXPECTED_DUMP


def test_ui_is_required(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the example refuses to run without a selected user interface."""
    assert '--ui' in _refused(capsys)


def test_unknown_ui(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the example refuses a user interface it does not have."""
    assert 'curses' in _refused(capsys, '--ui', 'curses')


@pytest.mark.parametrize('option', ['-o', '--output'])
def test_output_named(option: str, tmp_path: Path,
                      capsys: pytest.CaptureFixture[str]) -> None:
    """Test naming an output file says where a save would write it.

    Both spellings of the option are tried, because both are documented.
    """
    out_file = tmp_path / 'out.json'
    assert _dump(capsys, option, str(out_file)) == (
        f'{HEAD}\nname = Flat example\nanswer = 42\n{VALID_LINE}\n'
        f'save to: {out_file}\nedit() returned None, so nothing was saved.')
    assert not out_file.exists()


def test_set_members(capsys: pytest.CaptureFixture[str]) -> None:
    """Test --set edits the buffer and marks what the user changed."""
    assert _dump(capsys, '--set', 'name=Other', '--set', 'answer=7') == (
        f'{EDITED_HEAD}\nname = Other (edited)\nanswer = 7 (edited)\n'
        f'{VALID_END}')


def test_set_same_value(capsys: pytest.CaptureFixture[str]) -> None:
    """Test setting a member to the value it has is not an edit."""
    assert _dump(capsys, '--set', 'name=Flat example') == EXPECTED_DUMP


def test_set_empty_value(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a member can be set to an empty field."""
    assert _dump(capsys, '--set', 'name=') == \
        f'{EDITED_HEAD}\nname =  (edited)\nanswer = 42\n{VALID_END}'


def test_set_not_a_number(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a number member keeps text that is not a number yet."""
    assert _dump(capsys, '--set', 'answer=not-a-number') == \
        (f'{EDITED_HEAD}\nname = Flat example\n'
         'answer = not-a-number (edited)\n'
         '    Invalid configuration: Value for answer is not of type int.\n'
         f'{REFUSED_LINE}\n{DUMP_TAIL}')


def test_dump_refused_bool(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a true or false typed into a number member is refused.

    A `bool` is an `int` in Python, so a range check on its own would accept
    it. The example declares the type of the member as well, which is what
    `config_as_json` has `ValueTypeValidator` for.
    """
    assert _dump(capsys, '--set', 'answer=true') == \
        (f'{EDITED_HEAD}\nname = Flat example\nanswer = true (edited)\n'
         '    Invalid configuration: Value for answer must not be of type '
         'bool.\n'
         f'{REFUSED_LINE}\n{DUMP_TAIL}')


def test_dump_refused_value(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a value outside the allowed range is refused, and why."""
    assert _dump(capsys, '--set', 'answer=500') == \
        (f'{EDITED_HEAD}\nname = Flat example\nanswer = 500 (edited)\n'
         '    Invalid configuration: '
         'Value 500 for answer is greater than maximum 100.\n'
         f'{REFUSED_LINE}\n{DUMP_TAIL}')


def test_dump_rewritten_value(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a value that a validator rewrote is shown as rewritten.

    A validation pass is not read only, and this is what makes that visible
    without a display: the value shown is the one the validator stored back
    and not the one that was typed.
    """
    assert _dump(capsys, '--set', 'name=other') == \
        (f'{EDITED_HEAD}\nname = Other (edited) (changed by validator)\n'
         f'answer = 42\n{VALID_END}')


def test_set_unknown_member(capsys: pytest.CaptureFixture[str]) -> None:
    """Test setting a member that does not exist is refused."""
    error = _refused(capsys, '--ui', 'dump', '--set', 'missing=1')
    assert 'missing is not a member' in error


def test_set_without_value(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a --set that names no value at all is refused."""
    error = _refused(capsys, '--ui', 'dump', '--set', 'name')
    assert '--set needs member=value' in error


def test_read_complete_file(capsys: pytest.CaptureFixture[str]) -> None:
    """Test -i shows the values of the file and not the declared defaults."""
    assert _dump(capsys, '-i', data_file('e01_complete.json')) == (
        f'{HEAD}\nname = From a file\nanswer = 7\n{VALID_LINE}\n'
        f'{input_tail("e01_complete.json")}')


def test_read_incomplete_file(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a value the file leaves out is filled in and said to be."""
    assert _dump(capsys, '-i', data_file('e01_incomplete.json')) == (
        f'{HEAD}\n{FILLED_LINE}\nname = Only a name\n'
        f'answer = 42 (filled from default)\n{VALID_LINE}\n'
        f'{input_tail("e01_incomplete.json")}')


def test_defaults_policy(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the permissive policy reads the same incomplete file alike."""
    assert _dump(capsys, '--policy', 'defaults', '-i',
                 data_file('e01_incomplete.json')) == (
        f'{HEAD}\n{FILLED_LINE}\nname = Only a name\n'
        f'answer = 42 (filled from default)\n{VALID_LINE}\n'
        f'{input_tail("e01_incomplete.json")}')


def test_strict_policy(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the strict policy refuses the file the default policy opens."""
    error = _refused(capsys, '--ui', 'dump', '--policy', 'strict', '-i',
                     data_file('e01_incomplete.json'))
    assert 'does not hold every value' in error
    assert 'No value for answer' in error


def test_strict_complete_file(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the strict policy opens a file that holds every value."""
    assert _dump(capsys, '--policy', 'strict', '-i',
                 data_file('e01_complete.json')) == (
        f'{HEAD}\nname = From a file\nanswer = 7\n{VALID_LINE}\n'
        f'{input_tail("e01_complete.json")}')


@pytest.mark.parametrize('case, name, expected', REFUSED_FILES)
def test_refused_file(case: str, name: str, expected: str,
                      capsys: pytest.CaptureFixture[str]) -> None:
    """Test a file that cannot be opened is a message and not an editor."""
    error = _refused(capsys, '--ui', 'dump', '-i', data_file(name))
    assert expected in error, case


def test_unknown_policy(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a policy the editor does not have is refused by the parser."""
    error = _refused(capsys, '--ui', 'dump', '--policy', 'sometimes')
    assert 'sometimes' in error


def test_edit_loaded_value(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a value read from a file can be edited like any other."""
    assert _dump(capsys, '-i', data_file('e01_complete.json'), '--set',
                 'answer=9') == (
        f'{EDITED_HEAD}\nname = From a file\nanswer = 9 (edited)\n'
        f'{VALID_LINE}\n'
        f'{input_tail("e01_complete.json")}')


def _written(out_file: Path) -> object:
    """Return what one output file holds, as JSON space values."""
    return json.loads(out_file.read_text(encoding='UTF-8'))


def test_save_writes(tmp_path: Path,
                     capsys: pytest.CaptureFixture[str]) -> None:
    """Test --save writes the edited values and says what was returned.

    This is the whole round trip without a display: read nothing, edit two
    members, validate, write, and hand the saved object back.
    """
    out_file = tmp_path / 'out.json'
    assert _dump(capsys, '-o', str(out_file), '--set', 'answer=7', '--set',
                 'name=Other', '--save') == (
        f'{HEAD}\nname = Other\nanswer = 7\n{VALID_LINE}\n'
        f'{saved_tail(out_file, "FlatConfig")}')
    assert _written(out_file) == {'name': 'Other', 'answer': 7}


def test_saved_is_not_edited(tmp_path: Path,
                             capsys: pytest.CaptureFixture[str]) -> None:
    """Test the members are no longer marked as edited after a save.

    What has been written is not waiting to be written, and an editor that
    still claimed to have changes would be saying something untrue.
    """
    printed = _dump(capsys, '-o', str(tmp_path / 'out.json'), '--set',
                    'answer=7', '--save')
    assert '(edited)' not in printed


def test_save_over_input(tmp_path: Path,
                         capsys: pytest.CaptureFixture[str]) -> None:
    """Test the input file is what a save writes when no output is named."""
    in_file = tmp_path / 'round.json'
    in_file.write_text('{"name": "From a file", "answer": 7}',
                       encoding='UTF-8')
    assert _dump(capsys, '-i', str(in_file), '--set', 'answer=11',
                 '--save') == (f'{HEAD}\nname = From a file\nanswer = 11\n'
                               f'{VALID_LINE}\n'
                               f'{saved_tail(in_file, "FlatConfig")}')
    assert _written(in_file) == {'name': 'From a file', 'answer': 11}


def test_save_refused(tmp_path: Path,
                      capsys: pytest.CaptureFixture[str]) -> None:
    """Test an invalid buffer is not written, and nothing is handed back."""
    out_file = tmp_path / 'out.json'
    printed = _dump(capsys, '-o', str(out_file), '--set', 'answer=500',
                    '--save')
    assert 'greater than maximum 100' in printed
    assert 'These values are not valid, so they cannot be saved.' in printed
    assert 'edit() returned None' in printed
    assert not out_file.exists()


def test_save_rewritten(tmp_path: Path,
                        capsys: pytest.CaptureFixture[str]) -> None:
    """Test the value a validator rewrote is the value that reaches the file.

    An application that took the buffer at face value would disagree with
    its own file about this member.
    """
    out_file = tmp_path / 'out.json'
    _dump(capsys, '-o', str(out_file), '--set', 'name=other', '--save')
    assert _written(out_file) == {'name': 'Other', 'answer': 42}


def test_save_needs_a_file(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a --save with no file named says so instead of guessing one."""
    printed = _dump(capsys, '--save')
    assert 'There is no file to save to yet.' in printed
    assert 'edit() returned None' in printed


@pytest.mark.parametrize('ui_name', ['tk', 'textual'])
def test_save_only_for_dump(ui_name: str,
                            capsys: pytest.CaptureFixture[str]) -> None:
    """Test --save is refused where the editor has a Save of its own.

    An option that looked as if it worked and quietly did nothing would be
    worse than no option.
    """
    error = _refused(capsys, '--ui', ui_name, '--save')
    assert 'only means something together with --ui dump' in error


def test_chosen_out_completed(tmp_path: Path,
                              capsys: pytest.CaptureFixture[str]) -> None:
    """Test a named output file gets the extension the application uses."""
    out_file = tmp_path / 'chosen'
    printed = _dump(capsys, '--extension', '.cfg', '-o', str(out_file),
                    '--save')
    assert f'Saved to {out_file}.cfg.' in printed
    assert _written(tmp_path / 'chosen.cfg') == {'name': 'Flat example',
                                                 'answer': 42}


def test_extension_dot_added(tmp_path: Path,
                             capsys: pytest.CaptureFixture[str]) -> None:
    """Test an extension written without its dot means the same thing."""
    out_file = tmp_path / 'chosen'
    assert f'Saved to {out_file}.cfg.' in _dump(capsys, '--extension', 'cfg',
                                                '-o', str(out_file), '--save')


def test_other_extension_kept(tmp_path: Path,
                              capsys: pytest.CaptureFixture[str]) -> None:
    """Test an extension that is only a default refuses nothing."""
    out_file = tmp_path / 'chosen.json'
    assert f'Saved to {out_file}.' in _dump(capsys, '--extension', '.cfg',
                                            '-o', str(out_file), '--save')
    assert out_file.exists()


def test_enforced_out_refused(tmp_path: Path,
                              capsys: pytest.CaptureFixture[str]) -> None:
    """Test an enforced extension refuses to write any other file."""
    out_file = tmp_path / 'chosen.json'
    printed = _dump(capsys, '--extension', '.cfg', '--enforce-extension', '-o',
                    str(out_file), '--save')
    assert '.cfg extension' in printed
    assert not out_file.exists()


def test_enforced_in_refused(capsys: pytest.CaptureFixture[str]) -> None:
    """Test an enforced extension refuses to open any other file."""
    error = _refused(capsys, '--ui', 'dump', '--extension', '.cfg',
                     '--enforce-extension', '-i',
                     data_file('e01_complete.json'))
    assert '.cfg extension' in error


def test_no_extension(capsys: pytest.CaptureFixture[str]) -> None:
    """Test text that names no extension is refused where it is given."""
    assert 'not a file name extension' in _refused(capsys, '--ui', 'dump',
                                                   '--extension', '.')


def test_shared_key_refused(capsys: pytest.CaptureFixture[str]) -> None:
    """Test one key combination given to two actions is refused."""
    assert 'is set for both' in _refused(capsys, '--ui', 'dump', '--key',
                                         'save=ctrl+q')


def test_unknown_action(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a --key that names no action of the editor is refused."""
    assert 'save_as' in _refused(capsys, '--ui', 'dump', '--key',
                                 'fold=ctrl+f')


def test_textual_key_chosen(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the Textual editor opens with the keys the run chose.

    The run quits on the key it was told to quit on, so an editor that had
    kept the default would never return.
    """
    assert textual_titles(e01_flat_config.main, monkeypatch, '--key',
                          'quit=ctrl+e', quit_key='ctrl+e') == ['FlatConfig']


def test_tk_ui_opens(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui tk builds the window and returns when it is closed."""
    open_tk_ui(e01_flat_config.main, monkeypatch)


def test_tk_ui_loaded(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui tk opens on the values of an incomplete file."""
    open_tk_ui(e01_flat_config.main, monkeypatch, '-i',
               data_file('e01_incomplete.json'))


def test_textual_ui_loaded(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui textual opens on a file and has nothing to save yet.

    A value that was filled in from a declared default is not a change the
    user made, so the title is not marked: nothing has been edited.
    """
    assert textual_titles(e01_flat_config.main, monkeypatch, '-i',
                          data_file('e01_incomplete.json')) == ['FlatConfig']


def test_textual_ui_opens(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui textual starts the application named after the class."""
    assert textual_titles(e01_flat_config.main, monkeypatch) == ['FlatConfig']


def test_textual_ui_edited(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test --ui textual shows an edit that --set made before it started."""
    assert textual_titles(e01_flat_config.main, monkeypatch, '--set',
                          'answer=7') == ['FlatConfig *']
