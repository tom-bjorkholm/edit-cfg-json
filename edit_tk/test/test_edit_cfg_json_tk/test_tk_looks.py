#! /usr/bin/env python3
"""Tests for what the Tkinter editor looks like and for its scrolling.

Two things a window has to do that a text rendering does not: it has to fit a
screen whatever the size of the configuration, and it has to say which of the
things on it can be edited and which are text about them. Neither is visible
to a test that only reads what a widget holds, so these tests read the colours
and drive the scrolling.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
import pytest
from edit_cfg_json import Emphasis, EditModel
from edit_cfg_json_tk.scrolling import BODY_HEIGHT, BODY_WIDTH
from edit_cfg_json_tk.tk_editor import EMPHASIS_COLOURS, EditorWidgets, \
    EXPLAIN_TEXT, FIELD_BACKGROUND, FIELD_FOREGROUND, LEAST_WRAP_WIDTH
from example.e01_flat_config import FlatConfig
from .helpers import ABOUT_NAME, DESCRIPTIONS, FakeWidget, FILLED_REPORT, \
    FLAT_DOCSTRING, FLAT_SUMMARY, real_press, real_ticks, stub_editor, \
    stub_press, STUB_BODY_HEIGHT

WHEEL_UP = -1
"""How far one turn of the wheel away from the user scrolls the body."""


def _described_model() -> EditModel:
    """Return a model with everything the editor can show on it."""
    return EditModel(FlatConfig(), FILLED_REPORT, descriptions=DESCRIPTIONS,
                     out_file='out.json')


def _stub_canvas() -> FakeWidget:
    """Return the stub widget that the editor scrolls its body on.

    The canvas is the one widget of the editor that is given a height, which
    is what tells it apart from the frames around it.
    """
    canvases = [widget for widget in FakeWidget.created
                if 'height' in widget.options]
    assert len(canvases) == 1
    return canvases[0]


def _stub_body() -> FakeWidget:
    """Return the stub widget that everything which scrolls is built in.

    It is the one widget whose parent is the canvas, because that is what
    being on a canvas means.
    """
    canvas = _stub_canvas()
    inside = [widget for widget in FakeWidget.created
              if widget.parent is canvas]
    assert len(inside) == 1
    return inside[0]


def _stub_scrollbar() -> FakeWidget:
    """Return the stub widget that scrolls the body when it is dragged."""
    bars = [widget for widget in FakeWidget.created
            if widget.options.get('orient') == 'vertical']
    assert len(bars) == 1
    return bars[0]


def _stub_fields() -> list[FakeWidget]:
    """Return every stub widget that the user can type into."""
    return [widget for widget in FakeWidget.created
            if 'textvariable' in widget.options]


def test_stub_body_scrolls(stub_tk: None) -> None:
    """Test the body is on a canvas that has a scrollbar to move it.

    Tk has no scrolling frame, so this is the one it has: what goes on the
    canvas scrolls, and what is packed after it does not.
    """
    _ = stub_tk
    stub_editor(_described_model())
    canvas = _stub_canvas()
    assert _stub_scrollbar().options['command'] == canvas.yview
    assert canvas.options['yscrollcommand'] == _stub_scrollbar().set


def test_stub_body_height(stub_tk: None) -> None:
    """Test a body taller than a window is scrolled to and not shown whole.

    The stub says the body is taller than the editor allows, which is what a
    configuration with more members than a screen has room for does.
    """
    _ = stub_tk
    stub_editor(_described_model())
    _stub_body().bindings['<Configure>']()
    canvas = _stub_canvas()
    assert canvas.options['height'] == BODY_HEIGHT
    assert canvas.options['scrollregion'] == (0, 0, 0, STUB_BODY_HEIGHT)


def test_stub_wheel_scrolls(stub_tk: None) -> None:
    """Test the wheel scrolls the body, whichever way it is reported.

    The bindings are on the window and not on the canvas, because a wheel
    event goes to the widget under the pointer and the pointer is usually
    over a field or a label of the body.
    """
    _ = stub_tk
    stub_editor(_described_model())
    window = FakeWidget.created[0]
    canvas = _stub_canvas()
    window.bindings['<Button-4>']()
    assert canvas.scrolled == WHEEL_UP
    window.bindings['<Button-5>']()
    assert canvas.scrolled == 0


def test_real_body_scrolls(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk gives the body a canvas that is scrolled by a scrollbar."""
    EditorWidgets(parent=root_or_skip, model=_described_model())
    canvases = _real_widgets(root_or_skip, tkinter.Canvas)
    bars = _real_widgets(root_or_skip, tkinter.Scrollbar)
    assert len(canvases) == 1
    assert len(bars) == 1
    root_or_skip.update_idletasks()
    assert canvases[0].cget('scrollregion') != ''


def _real_widgets(widget: tkinter.Misc,
                  wanted: type[tkinter.Misc]) -> list[tkinter.Misc]:
    """Return every real Tk widget of one class below one widget.

    Args:
        widget: Widget whose descendants are read.
        wanted: Class of widget to look for.

    Returns:
        Every widget of that class below that widget, in creation order.
    """
    found: list[tkinter.Misc] = []
    for child in widget.winfo_children():
        if isinstance(child, wanted):
            found.append(child)
        found.extend(_real_widgets(child, wanted))
    return found


def test_stub_field_tinted(stub_tk: None) -> None:
    """Test a field is given a background of its own.

    The window is white, so a field that kept the background it is given
    could not be told from a label: the values were there to be edited and
    nothing said so.
    """
    _ = stub_tk
    stub_editor(_described_model())
    fields = _stub_fields()
    assert fields
    for field in fields:
        assert field.options['background'] == FIELD_BACKGROUND
        assert field.options['foreground'] == FIELD_FOREGROUND
        assert field.options['insertbackground'] == FIELD_FOREGROUND


def test_real_field_tinted(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk accepts that background and keeps it."""
    EditorWidgets(parent=root_or_skip, model=_described_model())
    entries = _real_widgets(root_or_skip, tkinter.Entry)
    assert entries
    for entry in entries:
        assert str(entry.cget('background')) == FIELD_BACKGROUND


def _stub_colour(text: str) -> object:
    """Return the colour of the one stub label that shows one text.

    Args:
        text: Text that the label shows.

    Returns:
        The foreground colour that label was given, or None when it was left
        in the colour of the platform.
    """
    labels = [widget for widget in FakeWidget.created
              if widget.options.get('text') == text]
    assert len(labels) == 1
    return labels[0].options.get('foreground')


@pytest.mark.parametrize('text, emphasis', [
    (FLAT_DOCSTRING, Emphasis.MUTED),
    (' (filled from default)', Emphasis.ATTENTION),
    ('the file left something out', Emphasis.WARNING),
    ('validation: not validated', Emphasis.MUTED),
    ('save to: out.json', Emphasis.MUTED)])
def test_stub_colours(stub_tk: None, text: str, emphasis: Emphasis) -> None:
    """Test each kind of text is shown in the colour of its kind.

    Which kind each of them is comes from the core, so this backend and the
    Textual one cannot colour one thing two ways. What the colours are is
    this backend's own, because Tk has no theme to ask.
    """
    _ = stub_tk
    stub_editor(_described_model())
    assert _stub_colour(text) == EMPHASIS_COLOURS[emphasis]


def test_stub_names_plain(stub_tk: None) -> None:
    """Test a member name is left in the ordinary colour of the platform.

    The names and the values are what the user came to change, and they are
    the most legible thing in the window because nothing was done to them.
    """
    _ = stub_tk
    stub_editor(_described_model())
    assert _stub_colour('answer') is None


def test_stub_verdict_colours(stub_tk: None) -> None:
    """Test the validation state changes colour with what it says."""
    _ = stub_tk
    widgets = stub_editor(_described_model())
    stub_press('Validate')
    assert widgets.verdict_text_shown == 'validation: valid'
    assert _stub_colour('validation: valid') == \
        EMPHASIS_COLOURS[Emphasis.GOOD]


def test_stub_summary_colour(stub_tk: None) -> None:
    """Test the summary keeps the colour of an explanation when hidden."""
    _ = stub_tk
    stub_editor(_described_model())
    stub_press(EXPLAIN_TEXT)
    assert _stub_colour(FLAT_SUMMARY) == EMPHASIS_COLOURS[Emphasis.MUTED]


def test_real_colours(root_or_skip: tkinter.Tk) -> None:
    """Test real Tk shows the same colours the stubbed test expects."""
    EditorWidgets(parent=root_or_skip, model=_described_model())
    coloured = {str(label.cget('text')): str(label.cget('foreground'))
                for label in _real_widgets(root_or_skip, tkinter.Label)}
    assert coloured['the file left something out'] == \
        EMPHASIS_COLOURS[Emphasis.WARNING]
    assert coloured[' (filled from default)'] == \
        EMPHASIS_COLOURS[Emphasis.ATTENTION]
    assert coloured['answer'] not in set(EMPHASIS_COLOURS.values())


def _canvas_of(window: tkinter.Misc) -> tkinter.Canvas:
    """Return the canvas that the editor scrolls its body on."""
    canvases = _real_widgets(window, tkinter.Canvas)
    assert len(canvases) == 1
    canvas = canvases[0]
    assert isinstance(canvas, tkinter.Canvas)
    return canvas


def _body_of(canvas: tkinter.Canvas) -> tkinter.Misc:
    """Return the frame on one canvas that holds what scrolls."""
    inside = canvas.winfo_children()
    assert len(inside) == 1
    return inside[0]


def test_real_wide_enough(root_or_skip: tkinter.Tk) -> None:
    """Test the editor opens one window wide and as tall as it needs.

    A canvas asks for a width of its own that has nothing to do with what is
    on it, so the editor opened at 430 pixels and cut off every paragraph and
    every mark. The width it asks for now is said and not measured, because a
    paragraph wraps to the width it is given and a body that has been laid out
    therefore asks for about the width it already has. The height is measured,
    because that answer means something.
    """
    EditorWidgets(parent=root_or_skip, model=_described_model())
    root_or_skip.update_idletasks()
    canvas = _canvas_of(root_or_skip)
    body = _body_of(canvas)
    assert canvas.winfo_reqwidth() == BODY_WIDTH
    assert canvas.winfo_reqheight() == min(body.winfo_reqheight(), BODY_HEIGHT)


def test_stub_width_is_said(stub_tk: None) -> None:
    """Test being laid out does not change the width the editor opens at.

    Following the width of the body is what made showing the explanations
    flicker between two window sizes for ever, and this is that bug in the one
    place a stub can see it: the stub says the body wants less width than the
    editor opens at, so a canvas that took its answer would be that much
    narrower.
    """
    _ = stub_tk
    stub_editor(_described_model())
    canvas = _stub_canvas()
    assert canvas.options['width'] == BODY_WIDTH
    _stub_body().bindings['<Configure>']()
    assert canvas.options['width'] == BODY_WIDTH
    assert canvas.options['height'] == BODY_HEIGHT


def test_real_fixed_first(root_or_skip: tkinter.Tk) -> None:
    """Test the part that does not scroll is the first one packed.

    Tk gives each child the space it asks for in the order they were packed,
    so this is what keeps the verdict, the saving and the buttons on a window
    too short for everything: packed second, they were laid out below its
    bottom edge and could not be reached at all.
    """
    EditorWidgets(parent=root_or_skip, model=_described_model())
    packed = root_or_skip.pack_slaves()
    assert len(packed) == 2
    assert str(packed[0].pack_info()['side']) == 'bottom'
    assert str(packed[1].pack_info()['side']) == 'top'
    assert _real_widgets(packed[1], tkinter.Canvas)


def _wrapped_at(label: tkinter.Misc) -> int:
    """Return the line width one label wraps its text at.

    The event that says a label has been given a width is generated here
    rather than waited for. Tk fills in the width itself, from the width the
    label really has, so what this shows is that the label follows it.

    Args:
        label: Label to ask about.

    Returns:
        The line width that the label wraps its text at, and zero for a label
        that does not wrap at all.
    """
    label.event_generate('<Configure>')
    label.update_idletasks()
    return int(label.cget('wraplength'))


def test_real_paragraph_wraps(root_or_skip: tkinter.Tk) -> None:
    """Test a paragraph follows the width it is given, and a mark does not.

    A Tk label neither wraps nor shrinks of its own accord: a paragraph wider
    than the window is simply cut, which is how the last words of a
    description went missing. The mark of a member is the one text that is
    left unwrapped, because it belongs beside its field on one line.
    """
    EditorWidgets(parent=root_or_skip, model=_described_model())
    labels = {str(label.cget('text')): label
              for label in _real_widgets(root_or_skip, tkinter.Label)}
    docstring = labels[FLAT_DOCSTRING]
    description = labels[ABOUT_NAME]
    assert _wrapped_at(docstring) == max(docstring.winfo_width(),
                                         LEAST_WRAP_WIDTH)
    assert _wrapped_at(description) == max(description.winfo_width(),
                                           LEAST_WRAP_WIDTH)
    assert _wrapped_at(labels[' (filled from default)']) == 0


@pytest.mark.focus_sensitive
def test_shown_window_fits() -> None:
    """Test nothing is cut off and nothing falls off a window that is shown.

    This is the one test of this backend that needs a window a person can see:
    Tk lays out the widgets inside a frame only once the window is mapped, so
    a withdrawn window cannot answer either question. It is deselected by the
    build and run by hand with `pytest -m focus_sensitive`.
    """
    window = tkinter.Tk()
    try:
        EditorWidgets(parent=window, model=_described_model())
        for size in ('', '900x260', '500x600'):
            if size:
                window.geometry(size)
            window.update_idletasks()
            window.update()
            sizes = _measured(window)
            assert _cut_off(sizes) == [], size
            fixed = window.pack_slaves()[0]
            assert fixed.winfo_height() > 1, size
            assert fixed.winfo_y() + fixed.winfo_height() <= \
                window.winfo_height(), size
    finally:
        window.destroy()


RESTLESS_RESIZES = 1000
"""How many resizes of one window in half a second is a window that loops.

Showing the explanations cost 19099 of them before the width stopped being
followed and about ninety afterwards, so anything between the two says that the
callbacks are answering each other again.
"""

SETTLING_TIME = 500
"""Milliseconds a window is given to settle after it has been changed."""


def _resizes(window: tkinter.Tk,
             seen: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Let one window settle, and return the resizes it asked for.

    The window is driven rather than inspected, because a layout that answers
    itself only shows up in how often it happens.

    Args:
        window: Window to let settle.
        seen: List that its resizes are being recorded in, which is emptied
            here so that each answer is about one change alone.

    Returns:
        The sizes that were reported while it settled.
    """
    seen.clear()
    window.after(SETTLING_TIME, window.quit)
    window.mainloop()
    return list(seen)


@pytest.mark.focus_sensitive
def test_shown_window_settles() -> None:
    """Test showing the explanations lays the window out and then stops.

    Following the width of the body made this flicker between two window sizes
    for ever, because a paragraph that has wrapped asks for a little less than
    it was given. It needs a window a person can see for the same reason the
    test above does, and it is the reason `BODY_WIDTH` is a width and not a
    measurement.
    """
    window = tkinter.Tk()
    seen: list[tuple[int, int]] = []
    try:
        EditorWidgets(parent=window, model=_described_model())
        window.bind('<Configure>',
                    lambda event: seen.append((event.width, event.height)))
        _resizes(window, seen)
        opened = (window.winfo_width(), window.winfo_height())
        real_press(window, EXPLAIN_TEXT)
        assert len(_resizes(window, seen)) < RESTLESS_RESIZES
        real_press(window, EXPLAIN_TEXT)
        assert len(_resizes(window, seen)) < RESTLESS_RESIZES
        assert (window.winfo_width(), window.winfo_height()) == opened
        assert real_ticks(window) == [True]
    finally:
        window.destroy()


def _measured(widget: tkinter.Misc) -> dict[str, tuple[int, int, int]]:
    """Return the size of every text below one widget, by text.

    Args:
        widget: Widget whose descendants are measured.

    Returns:
        The width each text asks for, the width it was given and the height it
        was given, by text.
    """
    sizes: dict[str, tuple[int, int, int]] = {}
    if 'text' in widget.keys() and str(widget.cget('text')):
        sizes[str(widget.cget('text'))] = (widget.winfo_reqwidth(),
                                           widget.winfo_width(),
                                           widget.winfo_height())
    for child in widget.winfo_children():
        sizes.update(_measured(child))
    return sizes


def _cut_off(sizes: dict[str, tuple[int, int, int]]) -> list[str]:
    """Return every text that asks for more width than it was given.

    Args:
        sizes: What every text asks for and was given.

    Returns:
        Every text that does not fit in the width it was given.
    """
    return [text for text, (asked, given, _) in sizes.items() if asked > given]


def test_stub_paragraphs_wrap(stub_tk: None) -> None:
    """Test every paragraph of the editor follows the width it is given.

    The mark of a member is the one text that does not: it belongs beside its
    field on one line, and wrapping it would make the row two lines high.
    """
    _ = stub_tk
    stub_editor(_described_model())
    wrapping = {str(widget.options['text']): '<Configure>' in widget.bindings
                for widget in FakeWidget.created if 'text' in widget.options}
    assert wrapping[FLAT_DOCSTRING]
    assert wrapping['the file left something out']
    assert wrapping['validation: not validated']
    assert not wrapping[' (filled from default)']
