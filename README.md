# edit-cfg-json

> Looking for installation and user-facing package information?
> See [edit/README_pypi.md](edit/README_pypi.md),
> or the PyPI project page
> [edit-cfg-json](https://pypi.org/project/edit-cfg-json).

## Repository purpose

This repository builds three packages that together give an application a
folding editor for configuration objects based on `config_as_json.Config`:

| Folder | Distribution | Import name |
| --- | --- | --- |
| [edit/](edit/) | `edit-cfg-json` | `edit_cfg_json` |
| [edit_tk/](edit_tk/) | `edit-cfg-json-tk` | `edit_cfg_json_tk` |
| [edit_textual/](edit_textual/) | `edit-cfg-json-textual` | `edit_cfg_json_textual` |

The two editor packages each install a program of their own name, which takes
any `config_as_json.Config` class it is told the name of, with no code written
by anybody:

```sh
edit-cfg-json-tk --module myapp.config --class AppConfig -i /etc/myapp.json
edit-cfg-json-textual --module myapp.config --class AppConfig
```

They open an editor, in a window and in the terminal, and they are what this
repository is for. The core installs no program at all, because the name
`edit-cfg-json` promises an editor and the core has none to give. The same
command line over the very limited non-interactive backend is a small utility.

```sh
python3 -m edit_cfg_json.dump --module myapp.config --class AppConfig \
    -i /etc/myapp.json
```

Inside this repository they are `./venv/bin/edit-cfg-json-tk`,
`./venv/bin/edit-cfg-json-textual` and
`./venv/bin/python3 -m edit_cfg_json.dump`, and any class under
[examples/src/example/](examples/src/example/) or
[https://github.com/tom-bjorkholm/config_as_json/tree/master/example/src/example](https://github.com/tom-bjorkholm/config_as_json/tree/master/example/src/example)
can be opened with them, which is the quickest way to see the editor against a
configuration that is not two members long.

## Related documentation

- Where to start when new to the code:
  [doc/code_design_overview.md](doc/code_design_overview.md)

- For the programmer of an application that offers one of the two editors to
  its own users:
  [doc/application_programmers_guide.md](doc/application_programmers_guide.md)

- For whoever edits a configuration in one of the two editors:
  [doc/end_users_guide.md](doc/end_users_guide.md)

- Package overviews (generated, see
  [Generated files](#generated-files)):
  [edit/README_pypi.md](edit/README_pypi.md),
  [edit_tk/README_pypi.md](edit_tk/README_pypi.md),
  [edit_textual/README_pypi.md](edit_textual/README_pypi.md)

- Public API: [edit-cfg-json](doc/edit-cfg-json_api.md),
  [edit-cfg-json-tk](doc/edit-cfg-json-tk_api.md),
  [edit-cfg-json-textual](doc/edit-cfg-json-textual_api.md)

- Protected/internal API:
  [edit-cfg-json](doc/edit-cfg-json_protected_api.md),
  [edit-cfg-json-tk](doc/edit-cfg-json-tk_protected_api.md),
  [edit-cfg-json-textual](doc/edit-cfg-json-textual_protected_api.md)

- Library design and decisions, in full: [doc/detailed_design.md](doc/detailed_design.md)

- Build system design: [common_build_tools/README.md](common_build_tools/README.md)

There is an [examples/](examples/) directory with worked examples for new
users, also useful for maintainers who want to see intended API usage in
context. [examples/src/example/README.md](examples/src/example/README.md)
lists what each example teaches and how to run it.

## Generated files

**Do not edit these files. The build overwrites them.**

| Generated file | Written by | Edit instead |
| --- | --- | --- |
| `edit*/README_pypi.md` | `custom_build_tools/src/create_pypi_readme_venv.py` | the `readme_parts` fragments below |
| `doc/*_api.md` | pydoc-markdown, configured by `custom_build_tools/pydoc-markdown*.yml` | the docstrings in the source |
| The `## Test summary` section of every `README.md` and `README_pypi.md` | the build report step | nothing; it always reflects the last build |

### Editing the README_pypi.md text

Each `README_pypi.md` is assembled from markdown fragments:

- [readme_parts/](readme_parts/) holds the text that is the same for all
  three packages, such as the overview of how the packages fit together,
  the project status, installation and license.
- `edit/readme_parts/`, `edit_tk/readme_parts/` and
  `edit_textual/readme_parts/` hold the text specific to one package.
  Each of them also holds a `template.md` that decides the section order
  for that package.

Fragments may use three directives:

- `{{include: name.md}}` inserts another fragment. The package's own
  `readme_parts` folder is searched first, then the repository wide one,
  so a package can override a common fragment by using the same file
  name.
- `{{dist_name}}` and `{{import_name}}` insert the distribution name and
  the import name of the package the file is being generated for. This
  lets a shared fragment still name the package it ends up in.
- `{{home_settings}}` inserts the name that the settings file of that
  program has in the home folder, which is `.{{dist_name}}.cfg`. It is
  what lets `readme_parts/program.md` describe the settings lookup once
  for both editor packages.

Write text that is common to all three packages once, in
[readme_parts/](readme_parts/), rather than repeating it per package.

The generator runs as a `custom_after_test` build hook, so a fragment
edit reaches the wheels on the *next* build: this build regenerates the
files on disk, and the build after it packages them. That is the same
two-run behaviour that `run_pypi_build.py` already documents for the test
summary.

## Cloning

This repository uses submodules. Clone it with:

```sh
git clone --recurse-submodules git@github.com:tom-bjorkholm/edit-cfg-json
```

If you already cloned without submodules, initialize them with:

```sh
git submodule update --init --recursive
```

To update the checked-out submodule revisions:

```sh
git submodule update --remote --merge
```

## Supported Python versions

- Package runtime baseline: Python 3.12 or newer
- Maintainer validation target: Python 3.12, 3.13, and 3.14
- Main day-to-day development: usually the newest supported Python version

## Development workflow

On macOS and Linux, the normal workflow is:

1. Run `./run_setup_build_environment.py` once after cloning or when the
   build environment needs to be recreated.
2. Run `./run_build.py` for the normal build-and-test cycle.
3. Run `./run_clean_build.py` before review or release work that needs a
   completely fresh build.

The helper scripts are:

- `run_setup_build_environment.py`
  Create or refresh the build environment.
- `run_build.py`
  Build the package and run the configured checks in the project virtual
  environment.
- `run_clean.py`
  Remove files generated by the build system.
- `run_clean_build.py`
  Perform a clean build from scratch. This is especially useful because some
  duplicate-code diagnostics only appear on a clean build.
- `run_pypi_build.py`
  Create the distribution artifacts intended for PyPI publishing.
- `run_static_checks.py`
  Run pylint, flake8 and mypy on the given files only, for fast iteration
  without rebuilding the virtual environment.
- `run_focus_sensitive_tests.py`
  Manually run focus sensitive tests under a controlled display conditions
  that they need. (Computer with real display, and no user actions moving
  focus on display. As an automatic test suite cannot guarantee these
  display conditions, these tests are not run automatically.)

The standard verification suite includes pytest, pylint, flake8, mypy and
the Python layout check. After a build, the generated reports can be
browsed through `reports/index.html`.

## Test summary

- Test result: 2016 passed, 3 deselected in 110s (0:01:50)
- No flake8 warnings.
- No mypy errors found.
- No pylint warnings.
- No python layout warnings.
- Built version(s): 0.2.0
- Build and test using Python 3.13.15
