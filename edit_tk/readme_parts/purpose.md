## What this package does

`{{dist_name}}` is the Tkinter desktop editor. It is a thin backend on
top of `edit-cfg-json`, which it installs as a dependency. All the
editing, validation and file handling logic lives in the core; this
package only draws it and forwards the user's actions.

Tkinter itself is not installable from PyPI. It comes with most Python
distributions, but on some Linux distributions it is a separate system
package, such as `python3-tk`.
