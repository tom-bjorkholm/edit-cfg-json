#! /usr/bin/env python3
"""Tests for the plain text rendering of an edit model."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional
import pytest
from config_as_json import Config, ConfigPath, JsonType
from edit_cfg_json import Descriptions, EditModel, LoadReport, MemberRow, \
    close_question, docstring_text, load_text, model_as_text, model_title, \
    row_description, row_diagnostic, row_marks, row_subtree_text, \
    row_value_text, save_text, verdict_text
from .container_cfg import KeyedEnumCfg, TreeCfg
from .sample_cfg import HIGHEST, TOO_LARGE_MESSAGE, DocumentedCfg, FlatCfg, \
    IntEnumCfg, ListCfg, NoDocCfg, NoneCfg, RangeCfg, RewriteCfg, RulesCfg


FLAT_DOC = 'A configuration with one text member and one number member.'
"""The docstring of `FlatCfg`, which is a summary and nothing else."""

HEAD = f'FlatCfg\n{FLAT_DOC}'
"""The lines that every rendering of `FlatCfg` begins with.

The label of the configuration comes first, because what the whole
configuration is for is what the members below it are read in the light of,
and the docstring of its class follows it.
"""

EDITED_HEAD = f'FlatCfg *\n{FLAT_DOC}'
"""The same lines while the buffer holds something worth saving."""

HIDDEN_HEAD = f'FlatCfg - {FLAT_DOC}'
"""The one line that begins a rendering with the explanations hidden."""

TEXT_LINE = '    Text.'
"""What is shown under a member that holds text.

The editor says what kind of value every member holds, because that is the one
thing it knows about every member of every configuration without being told.
"""

WHOLE_LINE = '    A whole number.'
"""What is shown under a member that holds a whole number."""

ABOUT_NAME = 'What the name of this configuration is for.'
"""Description of the one member that the tests below describe."""

DESCRIPTIONS: Descriptions = {('name',): ABOUT_NAME}
"""What an application says about the members of a flat configuration."""

UNKNOWN_LINE = 'validation: not validated'
"""Line that a rendering of a model nobody has validated ends with."""

VALID_LINE = 'validation: valid'
"""Line that a rendering of an accepted buffer ends with."""

LOAD_LINE = 'the file left something out'
"""Message of the load in the tests that render one."""

FILLED_REPORT = LoadReport(message=LOAD_LINE, filled=frozenset({'answer'}))
"""Report of a load that filled the number member in from the default."""

NO_FILE_LINE = 'save to: no file chosen yet'
"""Line that a rendering of a model with no destination ends with."""


def _row(model: EditModel, name: str) -> MemberRow:
    """Return the row of one member of a model."""
    return {row.name: row for row in model.rows}[name]


def test_flat_text() -> None:
    """Test the rendering has one line per member and then the verdict."""
    assert model_as_text(EditModel(FlatCfg())) == \
        (f'{HEAD}\nname = flat text\n{TEXT_LINE}\nanswer = 42\n'
         f'{WHOLE_LINE}\n{UNKNOWN_LINE}\n'
         f'{NO_FILE_LINE}')


def test_text_has_no_quotes() -> None:
    """Test a string member is shown as the string and not as JSON text."""
    assert '"' not in model_as_text(EditModel(FlatCfg()))


def test_none_text() -> None:
    """Test a member holding None is rendered as JSON null."""
    assert 'name = null' in model_as_text(EditModel(NoneCfg()))


def test_container_text() -> None:
    """Test a list member and a dict member are shown as trees of rows.

    A container says how much it holds and uses a colon rather than an equals
    sign, because it has no value of its own: its value is the rows below it,
    which are indented once for each container they are inside.

    An ordinary dict says below itself that no entry can be added to it, for
    the reason `edit_cfg_json.elements` gives: its class declares which keys
    it has. That line is between the container and its first value.
    """
    text = model_as_text(EditModel(ListCfg()))
    assert 'tags: 2 elements\n    0 = first\n' in text
    assert 'limits: 2 entries\n' in text
    assert '\n    high = 9\n' in text
    assert 'answer = 3' in text


def test_edited_text() -> None:
    """Test an edited member is marked, and only that member."""
    model = EditModel(FlatCfg())
    model.set_text(path=('answer',), text='7')
    assert model_as_text(model) == (
        f'{EDITED_HEAD}\nname = flat text\n{TEXT_LINE}\n'
        f'answer = 7 (edited)\n{WHOLE_LINE}\n'
        f'{UNKNOWN_LINE}\n{NO_FILE_LINE}')


def test_edit_undone_text() -> None:
    """Test a member typed back to what it was is not marked as edited."""
    model = EditModel(FlatCfg())
    model.set_text(path=('answer',), text='7')
    model.set_text(path=('answer',), text='42')
    assert model_as_text(model) == \
        (f'{HEAD}\nname = flat text\n{TEXT_LINE}\nanswer = 42\n'
         f'{WHOLE_LINE}\n{UNKNOWN_LINE}\n'
         f'{NO_FILE_LINE}')


def test_invalid_value_text() -> None:
    """Test text that is not a number yet is shown as it was typed."""
    model = EditModel(FlatCfg())
    model.set_text(path=('answer',), text='not-a-number')
    assert 'answer = not-a-number (edited)' in model_as_text(model)


def test_model_title() -> None:
    """Test the model label is the class name while there is no change."""
    assert model_title(EditModel(FlatCfg())) == 'FlatCfg'


def test_dirty_model_title() -> None:
    """Test the model label is marked while there is something to save."""
    model = EditModel(FlatCfg())
    model.set_text(path=('name',), text='other text')
    assert model_title(model) == 'FlatCfg *'


def test_unknown_verdict_text() -> None:
    """Test a model nobody validated says so rather than saying nothing."""
    assert verdict_text(EditModel(FlatCfg())) == UNKNOWN_LINE


def test_valid_verdict_text() -> None:
    """Test an accepted buffer is reported with nothing added to it."""
    model = EditModel(FlatCfg())
    model.validate()
    assert verdict_text(model) == VALID_LINE


def test_invalid_verdict_text() -> None:
    """Test a refused member is named here and reported beside itself.

    The sentence that says what is wrong with one member belongs at that
    member, and this line says which members to look at, because a
    configuration of any size does not fit a window.
    """
    model = EditModel(RangeCfg())
    model.set_text(path=('answer',), text='500')
    model.validate()
    assert verdict_text(model) == 'validation: invalid, see answer'
    assert 'greater than maximum 100' in \
        row_diagnostic(model=model, row=_row(model, 'answer'))


def test_unattributed_verdict() -> None:
    """Test what is about no single member stays below the state line."""
    model = EditModel(RulesCfg())
    model.set_text(path=('first',), text=str(HIGHEST))
    model.set_text(path=('second',), text=str(HIGHEST))
    model.validate()
    assert verdict_text(model) == (
        'validation: invalid\n'
        + TOO_LARGE_MESSAGE.format(total=2 * HIGHEST))


def test_edited_verdict_text() -> None:
    """Test an edit puts the rendering back to not having been validated."""
    model = EditModel(FlatCfg())
    model.validate()
    model.set_text(path=('answer',), text='7')
    assert verdict_text(model) == UNKNOWN_LINE


def test_rewritten_text() -> None:
    """Test a member a validator rewrote is shown as rewritten."""
    model = EditModel(RewriteCfg())
    model.set_text(path=('name',), text='typed text')
    model.validate()
    assert model_as_text(model).splitlines()[-4:] == [
        'name = Typed text (edited) (changed by validator)', TEXT_LINE,
        VALID_LINE, NO_FILE_LINE]


def test_verdict_before_save() -> None:
    """Test the verdict and then the saving end a rendering, in that order.

    That is the order in which a session reaches them: what the application
    makes of the values decides whether they can be written at all.
    """
    model = EditModel(FlatCfg())
    model.validate()
    assert model_as_text(model).splitlines()[-2:] == [VALID_LINE, NO_FILE_LINE]


@pytest.mark.parametrize('value, expected',
                         [(42, '42'), (1.5, '1.5'), (True, 'true'),
                          (False, 'false'), (None, 'null'),
                          ('text', 'text'), ('', ''),
                          ('with "quotes"', 'with "quotes"'),
                          ('Björkholm', 'Björkholm'),
                          ('  spaced  ', '  spaced  '), ('42', '42')])
def test_row_value_text(value: JsonType, expected: str) -> None:
    """Test a string shows as itself and every other scalar as its JSON."""
    row = MemberRow(path=('member',), value=value, original=value)
    assert row_value_text(row) == expected


@pytest.mark.parametrize('value, expected',
                         [('typed', 'typed'), (7, '7'), ('', '')])
def test_edited_value_text(value: JsonType, expected: str) -> None:
    """Test an edited member shows what it holds now, not what it held."""
    row = MemberRow(path=('member',), value=value, original=42)
    assert row_value_text(row) == expected


@pytest.mark.parametrize('value, rewritten, filled, expected',
                         [(42, False, False, ''),
                          (7, False, False, ' (edited)'),
                          (42, True, False, ' (changed by validator)'),
                          (7, True, False,
                           ' (edited) (changed by validator)'),
                          (42, False, True, ' (filled from default)'),
                          (7, False, True,
                           ' (filled from default) (edited)'),
                          (7, True, True,
                           ' (filled from default) (edited) '
                           '(changed by validator)')])
def test_row_marks(value: JsonType, rewritten: bool, filled: bool,
                   expected: str) -> None:
    """Test the marks of a member are shown together when several apply."""
    row = MemberRow(path=('member',), value=value, original=42,
                    changed_by_validator=rewritten, filled_from_default=filled)
    assert row_marks(row) == expected


def test_no_load_text() -> None:
    """Test a model built without a load has nothing to say about one."""
    assert load_text(EditModel(FlatCfg())) == ''


def test_load_text() -> None:
    """Test the message of the load is what the rendering reports."""
    assert load_text(EditModel(FlatCfg(), FILLED_REPORT)) == LOAD_LINE


def test_load_text_is_first() -> None:
    """Test the load comes above the members it explains the marks on."""
    model = EditModel(FlatCfg(), FILLED_REPORT)
    assert model_as_text(model) == (
        f'{HEAD}\n{LOAD_LINE}\nname = flat text\n{TEXT_LINE}\n'
        f'answer = 42 (filled from default)\n{WHOLE_LINE}\n'
        f'{UNKNOWN_LINE}\n'
        f'{NO_FILE_LINE}')


def test_no_load_no_line() -> None:
    """Test a rendering with nothing to say about a load has no empty line."""
    assert model_as_text(EditModel(FlatCfg())).splitlines()[2] == \
        'name = flat text'


def test_no_destination_text() -> None:
    """Test a model with nowhere to write says so rather than saying nothing.

    "No file chosen yet" and "this file is waiting to be written" are two
    different states, and a user who cannot tell them apart cannot tell
    whether pressing Save will ask them something.
    """
    assert save_text(EditModel(FlatCfg())) == NO_FILE_LINE


def test_destination_text(tmp_path: Path) -> None:
    """Test a model that has a destination says where it would write."""
    out_file = tmp_path / 'out.json'
    assert save_text(EditModel(FlatCfg(), out_file=out_file)) == \
        f'save to: {out_file}'


def test_saved_text(tmp_path: Path) -> None:
    """Test the rendering says what saving did once it has been asked for."""
    out_file = tmp_path / 'out.json'
    model = EditModel(FlatCfg(), out_file=out_file)
    model.save()
    assert save_text(model) == f'Saved to {out_file}.'
    assert model_as_text(model).splitlines()[-1] == f'Saved to {out_file}.'


def test_refused_save_text(tmp_path: Path) -> None:
    """Test a refused save is reported where a successful one would be."""
    model = EditModel(RangeCfg(), out_file=tmp_path / 'out.json')
    model.set_text(path=('answer',), text='500')
    model.save()
    assert save_text(model) == \
        'These values are not valid, so they cannot be saved.'


def test_edit_after_save_text(tmp_path: Path) -> None:
    """Test an edit puts the rendering back to naming the destination."""
    out_file = tmp_path / 'out.json'
    model = EditModel(FlatCfg(), out_file=out_file)
    model.save()
    model.set_text(path=('answer',), text='7')
    assert save_text(model) == f'save to: {out_file}'


def test_nothing_to_lose() -> None:
    """Test a buffer nobody has touched is closed without a question."""
    assert close_question(EditModel(FlatCfg())) == ''


def test_close_asks() -> None:
    """Test a buffer holding an unsaved change is asked about."""
    model = EditModel(FlatCfg())
    model.set_text(path=('answer',), text='7')
    assert 'discard' in close_question(model)


def test_close_after_save(tmp_path: Path) -> None:
    """Test a change that has reached the file is not asked about.

    A save moves the values the buffer is compared with, so there is then
    nothing left that closing would lose.
    """
    model = EditModel(FlatCfg(), out_file=tmp_path / 'out.json')
    model.set_text(path=('answer',), text='7')
    model.save()
    assert close_question(model) == ''


def test_close_after_refusal(tmp_path: Path) -> None:
    """Test a change that a refused save left in the buffer is asked about."""
    model = EditModel(RangeCfg(), out_file=tmp_path / 'out.json')
    model.set_text(path=('answer',), text='500')
    model.save()
    assert close_question(model) != ''


def test_docstring_text() -> None:
    """Test the whole docstring is what is shown while it is being shown."""
    model = EditModel(DocumentedCfg())
    assert docstring_text(model) == model.docstring
    assert '\n\n' in docstring_text(model)


def test_hidden_doc_text() -> None:
    """Test the summary is what is left when the explanations are hidden.

    One line for the whole configuration is worth keeping whatever the user
    asked to be rid of.
    """
    model = EditModel(DocumentedCfg())
    model.toggle_explanations()
    assert docstring_text(model) == model.summary
    assert '\n' not in docstring_text(model)


def test_no_docstring_text() -> None:
    """Test a class with no docstring is rendered with no label of its own.

    A rendering of it begins with the name of the class and goes straight on
    to the members, rather than with the docstring of a base class.
    """
    model = EditModel(NoDocCfg())
    assert docstring_text(model) == ''
    assert model_as_text(model).splitlines()[:2] == ['NoDocCfg',
                                                     'name = documented']


def test_row_description() -> None:
    """Test the description of a member is shown while they are shown."""
    model = EditModel(FlatCfg(), descriptions=DESCRIPTIONS)
    rows = {row.name: row for row in model.rows}
    assert row_description(model=model, row=rows['name']) == \
        f'{ABOUT_NAME}\n{TEXT_LINE.strip()}'
    assert row_description(model=model, row=rows['answer']) == \
        WHOLE_LINE.strip()


def test_hidden_row_about() -> None:
    """Test a description says nothing while the explanations are hidden."""
    model = EditModel(FlatCfg(), descriptions=DESCRIPTIONS)
    model.toggle_explanations()
    rows = {row.name: row for row in model.rows}
    assert row_description(model=model, row=rows['name']) == ''


def test_described_text() -> None:
    """Test a described member has its description on the line below it."""
    model = EditModel(FlatCfg(), descriptions=DESCRIPTIONS)
    assert model_as_text(model) == (
        f'{HEAD}\nname = flat text\n    {ABOUT_NAME}\n{TEXT_LINE}\n'
        f'answer = 42\n{WHOLE_LINE}\n'
        f'{UNKNOWN_LINE}\n{NO_FILE_LINE}')


def test_hidden_text() -> None:
    """Test hiding the explanations leaves the values and the summary.

    The summary shares the first line with the label of the configuration
    here, because one line for the whole configuration is what is left when
    the explanations are hidden.
    """
    model = EditModel(FlatCfg(), descriptions=DESCRIPTIONS)
    model.toggle_explanations()
    assert model_as_text(model) == (
        f'{HIDDEN_HEAD}\nname = flat text\nanswer = 42\n{UNKNOWN_LINE}\n'
        f'{NO_FILE_LINE}')


def test_saved_title(tmp_path: Path) -> None:
    """Test the model label loses its mark once there is nothing to save."""
    model = EditModel(FlatCfg(), out_file=tmp_path / 'out.json')
    model.set_text(path=('name',), text='other text')
    assert model_title(model) == 'FlatCfg *'
    model.save()
    assert model_title(model) == 'FlatCfg'


def test_diagnostic_below() -> None:
    """Test what is wrong with a member is written below that member.

    The description comes first and the refusal after it, because the
    description is part of the member and the refusal comes and goes: a line
    that appears at the bottom moves nothing that is above it.
    """
    model = EditModel(IntEnumCfg())
    model.set_text(path=('level',), text='MIDDLE')
    model.validate()
    assert model_as_text(model).splitlines()[-6:] == [
        'level = MIDDLE (edited)',
        '    The values that the int enum member of `IntEnumCfg` can hold.',
        '    One of: LOWEST, LOW, HIGH.',
        '    MIDDLE is not one of: LOWEST, LOW, HIGH',
        'validation: invalid, see level', NO_FILE_LINE]


def test_diagnostic_stays() -> None:
    """Test hiding the explanations leaves what is wrong on the screen.

    A description says what a member is for and is what a user who knows the
    configuration wants out of the way. A refusal is something to act on, and
    an editor that hid it would be hiding the one thing that has to be read.
    """
    model = EditModel(IntEnumCfg())
    model.set_text(path=('level',), text='MIDDLE')
    model.validate()
    model.toggle_explanations()
    lines = model_as_text(model).splitlines()
    assert '    MIDDLE is not one of: LOWEST, LOW, HIGH' in lines
    assert '    One of: LOWEST, LOW, HIGH.' not in lines


def test_leaving_field_shown() -> None:
    """Test a field that was left says so without any validation pass.

    The verdict is still that nothing has been validated, because leaving one
    field is not a question about the whole configuration.
    """
    model = EditModel(IntEnumCfg())
    model.set_text(path=('level',), text='MIDDLE')
    model.check_field(('level',))
    assert row_diagnostic(model=model, row=_row(model, 'level')) == \
        'MIDDLE is not one of: LOWEST, LOW, HIGH'
    assert verdict_text(model) == UNKNOWN_LINE


def test_no_diagnostic() -> None:
    """Test a member nothing is known to be wrong with says nothing."""
    model = EditModel(FlatCfg())
    assert row_diagnostic(model=model, row=_row(model, 'name')) == ''
    model.validate()
    assert row_diagnostic(model=model, row=_row(model, 'name')) == ''


def test_edit_drops_it() -> None:
    """Test an edit anywhere drops what a validation pass said about a member.

    What a validator refused is answered by the whole configuration, and a
    validator may look at any member of it, so a verdict that was reached
    from an earlier buffer says nothing true about the one there now.
    """
    model = EditModel(RulesCfg())
    model.set_text(path=('first',), text='500')
    model.validate()
    assert row_diagnostic(model=model, row=_row(model, 'first')) != ''
    model.set_text(path=('second',), text='3')
    assert row_diagnostic(model=model, row=_row(model, 'first')) == ''


def test_tree_is_indented() -> None:
    """Test a value is indented once for each container it is inside.

    What a dict says below itself about the entries it cannot be given is
    indented with it, which is what separates the two lines below.
    """
    text = model_as_text(EditModel(TreeCfg()))
    assert 'rules: 2 elements\n    0: 1 entry\n' in text
    assert '\n        low = 1\n' in text


def test_folded_says_so() -> None:
    """Test a folded container says so and shows nothing below it.

    This rendering has no control for the user to press, so it says in words
    what the two backends say with one, and a reader who was not told would
    read the values it hides as all there are.
    """
    model = EditModel(TreeCfg())
    model.toggle_fold(('rules',))
    text = model_as_text(model)
    assert 'rules: 2 elements (folded)\n' in text
    assert 'low = 1' not in text
    assert 'answer = 3' in text


@pytest.mark.parametrize('state, expected',
                         [(None, ''), (True, ' [valid on its own]'),
                          (False, ' [refused on its own]')])
def test_row_subtree_text(state: Optional[bool], expected: str) -> None:
    """Test each of the three states an object can be in has its own text.

    Not having been asked says nothing at all, because it is a state and not
    an answer, and a line saying so under every object would be a line of the
    window spent on nothing.
    """
    row = MemberRow(path=('inner',), value={}, original={}, children=(),
                    config_type=DocumentedCfg, subtree_valid=state)
    assert row_subtree_text(row) == expected


@pytest.mark.parametrize('state, expected',
                         [(None, ''), (True, ' [valid inside]'),
                          (False, ' [refused inside]')])
def test_row_inside_text(state: Optional[bool], expected: str) -> None:
    """Test a container of objects says what it holds and not what it is.

    A list and a dict are no configuration and have nothing to say about
    themselves, and the words have to say so: a folded container shows none of
    the objects that the answer is really about.
    """
    row = MemberRow(path=('outputs',), value=[], original=[], children=(),
                    subtree_valid=state)
    assert row_subtree_text(row) == expected


@pytest.mark.parametrize('config_type, children, is_object',
                         [(DocumentedCfg, (), True),
                          (DocumentedCfg, None, False), (None, (), False),
                          (None, None, False)])
def test_row_is_object(config_type: Optional[type[Config]],
                       children: Optional[tuple[ConfigPath, ...]],
                       is_object: bool) -> None:
    """Test only a nested object that is really there is one at all.

    A list and a dict have no class of their own to ask, and a declared
    member holding no object has no object to ask, which is the case with a
    class and no children.
    """
    row = MemberRow(path=('inner',), value={}, original={}, children=children,
                    config_type=config_type)
    assert row.is_object is is_object


def test_leaf_marked_at_depth() -> None:
    """Test a value inside a container carries its own marks."""
    model = EditModel(TreeCfg())
    model.set_text(path=('rules', '0', 'low'), text='5')
    assert '        low = 5 (edited)' in model_as_text(model)
    assert 'rules: 2 elements (edited)' in model_as_text(model)


def test_refused_path_named() -> None:
    """Test the verdict names a refused node by the whole path to it."""
    model = EditModel(KeyedEnumCfg())
    model.set_text(path=('shades', 'colour'), text='PURPLE')
    model.validate()
    assert 'validation: invalid, see shades.colour' in model_as_text(model)


def test_described_element() -> None:
    """Test one description reaches every element of a list.

    The `'['` step is what `config_as_json` gives that meaning to, and a
    description written per index would be untrue as soon as the list grew.
    """
    about = 'One of the tags of this configuration.'
    model = EditModel(ListCfg(), descriptions={('tags', '['): about})
    text = model_as_text(model)
    assert f'    0 = first\n        {about}\n' in text
    assert f'    1 = second\n        {about}\n' in text
