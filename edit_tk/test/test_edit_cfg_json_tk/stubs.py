#! /usr/bin/env python3
"""The stand-ins that the stubbed tests of the Tkinter backend use.

One stub stands in for every widget class the editor creates, because what
those tests are about is which widgets it creates, what they show and what
they are told to do, and none of that differs between the classes. The
pull-down of a member is the exception, and `FakeMenu` says why.

They are a module of their own so that what a stub *is* stays readable beside
the ways of reading a real Tk window, which are in `helpers`. Nothing here
knows what an edit model is.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Callable
from typing import ClassVar, Optional

STUB_BODY_HEIGHT = 1000
"""Height that the stub reports for the scrolling part of the editor.

It is taller than the height that part is allowed to have, so that the stubbed
tests see what the editor does with a configuration too tall for a window.
"""

STUB_BODY_WIDTH = 500
"""Width that the stub reports for the scrolling part of the editor.

It is narrower than the width the editor opens at, which is what makes a
stubbed test able to see whether the width is being followed: an editor that
took this answer would be narrower than the one width it is supposed to have.
"""

WHOLE_VIEW = (0.0, 1.0)
"""The fractions a canvas reports while all of its contents are in view.

It is what the stub answers unless a test says otherwise, so that a search
finds what it was looking for already on the window and scrolls nothing. A test
that is about the scrolling says that only a part is in view instead.
"""

STUB_CANVAS_ITEM = 7
"""Identifier that the stub gives the one item it is asked to create."""

TOUCHPAD = '<TouchpadScroll>'
"""The event that reports a touchpad, which only Tk 9 and later know.

It is what a Mac reports for every device that scrolls in pixels rather than
in turns, so it is what the editor really scrolls by there, and a Tk that has
never heard of it leaves the editor that one binding short.
"""

PROBE_TAG = 'edit_cfg_json_probe'
"""Bind tag that is used to ask Tk whether it accepts an event at all."""


BORN_TAGS = ('widget', 'FakeWidget', 'all')
"""The bind tags a stub widget is born with.

Real Tk gives every widget its own name, its class, its window and `all`, in
that order. What the editor does with them is add a tag of its own at one end
or the other, so what the stub needs of them is that there are some and that
their order can be read.
"""


class FakeWindow:
    """The part of the stand-in that stands in for a Tkinter window.

    A window is asked things no other widget is asked — its name, what its
    close button does, which window it belongs over and whether it holds the
    events of the application — and those are here so that what a stub widget
    is stays readable beside them.
    """

    def __init__(self) -> None:
        """Start with a window that is named nothing and grabs nothing."""
        self.window_title = ''
        self.protocols: dict[str, Callable[[], None]] = {}
        self.transient_to: object = None
        self.grabbed = False

    def title(self, text: str) -> None:
        """Name this window, as a real Tk toplevel is named."""
        self.window_title = text

    def protocol(self, name: str, callback: Callable[[], None]) -> None:
        """Record what one window manager protocol of this window does."""
        self.protocols[name] = callback

    def transient(self, parent: object) -> None:
        """Record which window this one is a transient of."""
        self.transient_to = parent

    def grab_set(self) -> None:
        """Take the events of the application for this widget."""
        self.grabbed = True

    def grab_release(self) -> None:
        """Give the events of the application back."""
        self.grabbed = False


class FakeCanvas(FakeWindow):
    """The part of the stand-in that stands in for a Tkinter canvas.

    One stub serves every widget class the editor creates, and the scrolling
    part of the editor is the one place where the methods of a particular
    class are really used. They are here so that what a stub widget is stays
    readable beside them.
    """

    def __init__(self) -> None:
        """Start with a canvas that has not been scrolled."""
        super().__init__()
        self.scrolled = 0
        self.moved: list[float] = []
        self.view = WHOLE_VIEW
        self.item_options: dict[str, object] = {}

    def create_window(self, *place: int, **options: object) -> int:
        """Put a widget on this canvas, as a real Tk canvas does.

        The widget counts as being in the layout afterwards, because that is
        what a canvas item is: the scrolling part of the editor is on a
        canvas and not packed, and everything in it would otherwise be
        reported as hidden.

        What the item was told is kept, because the width the body is laid
        out at is one of these options and a body laid out at the wrong width
        first is what this editor's defect was.
        """
        _ = place
        window = options.get('window')
        if isinstance(window, FakeWidget):
            window.packed = True
        self.item_options.update(options)
        return STUB_CANVAS_ITEM

    def itemconfigure(self, item: int, **options: object) -> None:
        """Change options of one item of this canvas.

        This canvas holds the one item the editor puts on it, so what it was
        told is kept beside what it was created with.
        """
        assert item == STUB_CANVAS_ITEM
        self.item_options.update(options)

    def bbox(self, *what: str) -> tuple[int, int, int, int]:
        """Return the area the contents of this canvas take up."""
        _ = what
        return (0, 0, 0, STUB_BODY_HEIGHT)

    def yview(self, *arguments: str) -> tuple[float, float]:
        """Scroll this canvas, or say how much of it is in view.

        Real Tk answers with the two fractions when it is asked without
        arguments, which is what a search reads before it decides whether it
        has to scroll at all.
        """
        _ = arguments
        return self.view

    def yview_moveto(self, fraction: float) -> None:
        """Record where a search asked this canvas to look."""
        self.moved.append(fraction)

    def update_idletasks(self) -> None:
        """Lay out what is waiting to be laid out, as real Tk does."""

    def yview_scroll(self, number: int, what: str) -> None:
        """Record how far the wheel scrolled this canvas."""
        assert what == 'units'
        self.scrolled += number

    def set(self, *fractions: str) -> None:
        """Show how much of the contents is visible, as a scrollbar does."""
        _ = fractions


def _both(first: Callable[..., object],
          second: Callable[..., object]) -> Callable[..., object]:
    """Return the callback that runs two bindings of one sequence.

    Args:
        first: What was bound to that sequence already.
        second: What was added to it.

    Returns:
        A callback that runs them in the order Tk runs them in, so that a
        test which runs the binding of a sequence runs all of it.
    """
    def run(*event: object) -> object:
        """Run what the widget had, and then what was added to it."""
        first(*event)
        return second(*event)
    return run


# A Tk widget has hundreds of methods, and this stands in for one, so the
# count here says how much of Tk the editor uses and not how much this class
# does.
class FakeWidget(FakeCanvas):  # pylint: disable=too-many-public-methods
    """Recording stand-in for a Tkinter widget in the stubbed tests."""

    created: ClassVar[list['FakeWidget']] = []
    """Every stub widget created since the list was last cleared."""

    tag_bindings: ClassVar[dict[str, dict[str, Callable[..., object]]]] = {}
    """What is bound on each bind tag, standing in for the interpreter.

    A bind tag is a name in the Tcl interpreter and not a widget, which is why
    this is one table for the whole process and not an attribute of a widget.
    """

    focused: ClassVar[list['FakeWidget']] = []
    """Every widget that has been given the keyboard focus, in order.

    The focus belongs to the interpreter and not to a widget in real Tk
    either: exactly one widget has it, and it is the last one that asked.
    """

    def __init__(self, parent: object = None, **options: object) -> None:
        """Record this widget together with its parent and its options."""
        self.parent = parent
        self.options = options
        self.bindings: dict[str, Callable[..., object]] = {}
        self.commands: list[tuple[str, Optional[Callable[[], None]]]] = []
        self.tags: tuple[str, ...] = BORN_TAGS
        self.packed = False
        self.packing: dict[str, object] = {}
        super().__init__()
        FakeWidget.created.append(self)

    def add_command(self, label: str = '',
                    command: Optional[Callable[[], None]] = None) -> None:
        """Record one entry of a menu, as a real Tk menu accepts one.

        The pull-down of a member is a menu button with a menu on it, so its
        values reach the menu this way rather than as options of a widget.
        """
        self.commands.append((label, command))

    def bindtags(self, tags: Optional[tuple[str, ...]] = None
                 ) -> Optional[tuple[str, ...]]:
        """Read or replace the bind tags of this widget, as Tk does.

        Args:
            tags: The tags this widget is to carry, or None to read them.

        Returns:
            The tags this widget carries, and None when it was given some.
        """
        if tags is None:
            return self.tags
        self.tags = tuple(tags)
        return None

    def bind_class(self, tag: str, sequence: str,
                   callback: Callable[..., object]) -> str:
        """Record one binding made on a bind tag, as a real widget does."""
        FakeWidget.tag_bindings.setdefault(tag, {})[sequence] = callback
        return 'stub class binding'

    def unbind_class(self, tag: str, sequence: str) -> None:
        """Take one binding off a bind tag, as a real widget does."""
        FakeWidget.tag_bindings.get(tag, {}).pop(sequence, None)

    def focus_set(self) -> None:
        """Record that this widget has been given the keyboard focus."""
        FakeWidget.focused.append(self)

    @property
    def shown(self) -> bool:
        """Return whether this widget is really on the window.

        A widget inside a frame that has been taken out of the layout is not
        on the window, whatever the widget itself was told: that is how the
        editor folds a container away, and a stub that answered only for the
        widget would say that a folded value is shown.

        The widget the editor was built below is the one this stops at. It is
        the test's own stand-in for a window, so it is never packed and
        everything inside it would otherwise be hidden.
        """
        if self is FakeWidget.created[0]:
            return True
        if not self.packed:
            return False
        parent = self.parent
        return not isinstance(parent, FakeWidget) or parent.shown

    def bind(self, sequence: str, callback: Callable[..., object],
             add: str = '') -> str:
        """Record one binding of one sequence, as a real Tk widget does.

        A binding made with `add` is added to what the widget already had
        rather than replacing it, exactly as Tk adds one: the editor binds
        the map of its window twice, for the grab and for the focus, and a
        stub that kept the last one would say that one of the two is missing.

        Args:
            sequence: Event sequence this widget is bound to.
            callback: What that event does.
            add: Tk's own '+' for a binding that is added to the ones there.

        Returns:
            What Tk answers with, which is the name of the binding.
        """
        bound = self.bindings.get(sequence)
        self.bindings[sequence] = _both(bound, callback) if add and bound \
            else callback
        return 'stub binding'

    def pack(self, **options: object) -> None:
        """Record that this widget is in the layout, and how it was put there.

        Where a widget ends up on the screen is what the real Tk tests are
        for. Whether it is in the layout at all is what tells a hidden
        description from a shown one, and how far from the left edge it was
        asked to be is what tells a value inside a container from a member,
        and a stub can answer both of those.
        """
        self.packed = True
        self.packing = dict(options)

    def pack_forget(self) -> None:
        """Record that this widget is out of the layout."""
        self.packed = False

    def place(self, **options: object) -> None:
        """Record that this widget was put over the window, and where.

        It is how a tooltip is put on the window, which is the one thing this
        editor lays out over another widget rather than beside it.
        """
        self.packed = True
        self.packing = dict(options)

    def lift(self) -> None:
        """Record nothing: a stub has nothing that could be drawn over."""

    def config(self, **options: object) -> None:
        """Change options of this widget, as a real Tk widget does."""
        self.options.update(options)

    def cget(self, name: str) -> object:
        """Return one option of this widget, as a real Tk widget does."""
        return self.options[name]

    def configure(self, **options: object) -> None:
        """Change options of this widget, as a real Tk widget does."""
        self.options.update(options)

    def winfo_toplevel(self) -> 'FakeWidget':
        """Return this widget, standing in for the enclosing window."""
        return self

    def winfo_children(self) -> list['FakeWidget']:
        """Return the stub widgets that were created below this one."""
        return [widget for widget in FakeWidget.created
                if widget.parent is self]

    def winfo_rootx(self) -> int:
        """Return where this widget is on the screen, standing in for Tk."""
        return 0

    def winfo_rooty(self) -> int:
        """Return where this widget is on the screen, standing in for Tk."""
        return 0

    def winfo_width(self) -> int:
        """Return a width, standing in for one that Tk would lay out."""
        return STUB_BODY_WIDTH

    def winfo_height(self) -> int:
        """Return a height, standing in for one that Tk would lay out."""
        return STUB_BODY_HEIGHT

    def winfo_reqheight(self) -> int:
        """Return a height, standing in for one that Tk would have laid out."""
        return STUB_BODY_HEIGHT

    def winfo_reqwidth(self) -> int:
        """Return a width, standing in for one that Tk would have laid out."""
        return STUB_BODY_WIDTH

    def destroy(self) -> None:
        """Forget this widget and everything below it, as Tk does.

        The editor destroys the rows it built when a validation pass leaves
        the model with other rows than it had, and a stub that remembered the
        destroyed ones would let a test read a window that is not there.
        """
        for child in self.winfo_children():
            child.destroy()
        if self in FakeWidget.created:
            FakeWidget.created.remove(self)

    def invoke(self) -> None:
        """Call the command of this widget, as a real Tk button does."""
        command = self.options['command']
        assert callable(command)
        command()


class FakeFlag:
    """Recording stand-in for a `tkinter.BooleanVar` in the stubbed tests.

    A tick-box shows its state through one of these, and Tk flips it itself
    when the box is pressed. This stub does neither of those things: it holds
    what it is told, which is what shows that the editor keeps the tick and
    the window saying the same thing.
    """

    created: ClassVar[list['FakeFlag']] = []
    """Every stub flag created since the list was last cleared."""

    def __init__(self, master: object = None, value: bool = False) -> None:
        """Record this flag, its master and the state it starts in."""
        self.master = master
        self.value = value
        FakeFlag.created.append(self)

    def get(self) -> bool:
        """Return the state this flag holds."""
        return self.value

    def set(self, value: bool) -> None:
        """Change the state this flag holds."""
        self.value = value


class FakeVar:
    """Recording stand-in for a `tkinter.StringVar` in the stubbed tests."""

    created: ClassVar[list['FakeVar']] = []
    """Every stub variable created since the list was last cleared."""

    def __init__(self, master: object = None, value: str = '') -> None:
        """Record this variable, its master and the text it starts with."""
        self.master = master
        self.value = value
        self.callbacks: list[Callable[..., None]] = []
        FakeVar.created.append(self)

    def get(self) -> str:
        """Return the text this variable holds."""
        return self.value

    def set(self, value: str) -> None:
        """Change the text and tell everyone who traced this variable."""
        self.value = value
        for callback in self.callbacks:
            callback()

    def trace_add(self, mode: str, callback: Callable[..., None]) -> str:
        """Record a callback that a change of this variable calls."""
        assert mode == 'write'
        self.callbacks.append(callback)
        return 'stub trace'
