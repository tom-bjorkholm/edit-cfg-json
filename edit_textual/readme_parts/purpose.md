## What this package does

`{{dist_name}}` is the terminal editor. It is a thin backend on top of
`edit-cfg-json`, which it installs as a dependency together with
`textual`. All the editing, validation and file handling logic lives in
the core; this package only draws it and forwards the user's actions.

Use this backend when the application is used over ssh, in a container,
or anywhere else without a desktop.
