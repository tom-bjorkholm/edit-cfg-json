#! /usr/bin/env python3
"""Example a02: the Textual editor for a command with no user interface.

This is example a01 in the other toolkit, and it belongs to the same
[programmer's guide](../../../doc/application_programmers_guide.md). A command
that runs in a terminal, has no user interface of its own, and wants the
terminal to become a configuration editor for a while.

The whole of it is one call, and only the import differs from a01:

````python
from edit_cfg_json_textual import edit
saved = edit(PipelineConfig(), in_file='pipeline.json')
````

The editor owns the terminal and the loop
-----------------------------------------
`edit` runs a Textual application of its own, which takes the terminal on the
alternate screen and gives it back when the user closes the editor. Whatever
this command printed before is still there afterwards, and what it prints
after the call goes to the ordinary terminal again.

That is exactly what a command with no user interface wants, and it is exactly
what an application that *already* runs Textual must not call: `App.run` calls
`asyncio.run`, and calling that from inside a running application raises or
deadlocks. Such an application uses `edit_cfg_json_textual.EditorScreen` or
`EditorPanel` instead, which are e16_screen_textual.py and
e14_embedded_textual.py.

So the rule for this case is a rule about what the command has *not* done: it
runs no Textual `App` of its own around this call.

Everything else is a01
----------------------
The call blocks until the user is done; it answers with the configuration
object that was written or with `None` when nothing was; the object handed in
is never modified, so the object that comes back is the one to go on with; and
`edit_cfg_json.ConfigLoadError` is what an input file that cannot be read as
this class is refused with. a01_tk_for_no_gui.py says why for each of them.

What this case has instead of a01's display
-------------------------------------------
This editor needs a terminal, in the same way that a01 needs a display. A
command whose output is redirected to a file, or that runs from a job with no
terminal at all, has nowhere to put an editor, and the window editor of a01 is
the answer for a machine that has a display but no terminal. A command that
might be run either way asks `sys.stdout.isatty()` before it chooses.

Running it
----------
::

    python3 a02_textual_for_no_gui.py
    python3 a02_textual_for_no_gui.py -i ../../data/e13_pipeline.json -o /tmp/p
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional
import sys
# See a01_tk_for_no_gui.py: this is what makes the `example` package
# importable when this file is run as a script.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
# pylint: disable-next=wrong-import-position
from edit_cfg_json import ConfigLoadError  # noqa: E402
# pylint: disable-next=wrong-import-position
from edit_cfg_json_textual import edit  # noqa: E402
# pylint: disable-next=wrong-import-position
from example._shared_pipeline import DESCRIPTIONS, PipelineConfig, \
    editor_files, report_run  # noqa: E402


def main(args: Optional[list[str]] = None) -> None:
    """Edit the configuration in the terminal, then run with what was saved.

    Args:
        args: Optional replacement for `sys.argv[1:]`, mainly for tests.
    """
    # See a01_tk_for_no_gui.py about the deliberate repetition of this call
    # between the two examples of this pair.
    # pylint: disable=duplicate-code
    files = editor_files('a02_textual_for_no_gui', args)
    try:
        saved = edit(PipelineConfig(), descriptions=DESCRIPTIONS,
                     in_file=files.in_file, out_file=files.out_file)
    except ConfigLoadError as refusal:
        sys.exit(str(refusal))
    report_run(saved)


# The usual guard, so that importing this module from a test runs nothing.
if __name__ == '__main__':
    main()
