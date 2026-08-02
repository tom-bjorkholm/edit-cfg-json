#! /usr/bin/env python3
"""Create package README_pypi.md files from markdown fragments.

Each package folder holds a `readme_parts/template.md` that decides the
section order. The template, and every fragment it pulls in, may contain
two kinds of directive:

- `{{include: name.md}}` inserts another fragment, looked up first in the
  package's own `readme_parts` folder and then in the repository wide
  `readme_parts` folder. This is how text that is common to all packages
  is written once.
- `{{dist_name}}` and `{{import_name}}` insert the distribution name and
  the import name of the package the file is generated for, so that a
  common fragment can still name the package it ends up in.

The build appends the test summary to the generated files afterwards, so
every template ends with a `## Test summary` placeholder heading.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import re
import sys
from typing import NamedTuple

PARTS_DIR_NAME = 'readme_parts'
TEMPLATE_NAME = 'template.md'
README_NAME = 'README_pypi.md'
INCLUDE_PREFIX = 'include:'
DIRECTIVE = re.compile(r'\{\{\s*([^{}]+?)\s*\}\}')


class Package(NamedTuple):
    """One package that gets a generated README_pypi.md file."""

    folder: str
    dist_name: str
    import_name: str


PACKAGES = (Package('edit', 'edit-cfg-json', 'edit_cfg_json'),
            Package('edit_tk', 'edit-cfg-json-tk', 'edit_cfg_json_tk'),
            Package('edit_textual', 'edit-cfg-json-textual',
                    'edit_cfg_json_textual'))


def project_root() -> Path:
    """Return the repository root holding the package folders."""
    return Path(__file__).resolve().parents[2]


def fragment_dirs(package: Package, root: Path) -> tuple[Path, Path]:
    """Return package specific and common fragment folders, in that order."""
    return (root / package.folder / PARTS_DIR_NAME, root / PARTS_DIR_NAME)


def read_fragment(name: str, package: Package, root: Path) -> str:
    """Return one fragment without its surrounding blank lines."""
    folders = fragment_dirs(package, root)
    for folder in folders:
        path = folder / name
        if path.is_file():
            return path.read_text(encoding='utf-8').strip('\n')
    searched = ' and '.join(str(folder) for folder in folders)
    raise FileNotFoundError(f'README fragment {name} not found in {searched}')


def variables(package: Package) -> dict[str, str]:
    """Return the values a `{{name}}` directive can expand to."""
    return {'dist_name': package.dist_name,
            'import_name': package.import_name}


def expand_variable(name: str, package: Package) -> str:
    """Return the value of one variable directive."""
    values = variables(package)
    if name not in values:
        known = ', '.join(sorted(values))
        raise KeyError(f'Unknown README variable {name}, known are {known}')
    return values[name]


def expand_directive(directive: str, package: Package, root: Path,
                     pending: frozenset[str]) -> str:
    """Return the replacement text for one directive."""
    if not directive.startswith(INCLUDE_PREFIX):
        return expand_variable(directive, package)
    name = directive[len(INCLUDE_PREFIX):].strip()
    if name in pending:
        raise ValueError(f'README fragment {name} includes itself')
    fragment = read_fragment(name, package, root)
    return expand(fragment, package, root, pending | {name})


def expand(text: str, package: Package, root: Path,
           pending: frozenset[str]) -> str:
    """Return text with all include and variable directives expanded."""
    def replace(match: re.Match[str]) -> str:
        """Return the expansion of the directive found by the regex."""
        return expand_directive(match.group(1), package, root, pending)
    return DIRECTIVE.sub(replace, text)


def render_readme(package: Package, root: Path) -> str:
    """Return the complete README_pypi.md text for one package."""
    template = read_fragment(TEMPLATE_NAME, package, root)
    expanded = expand(template, package, root, frozenset([TEMPLATE_NAME]))
    return expanded.rstrip('\n') + '\n'


def write_readme(package: Package, root: Path) -> Path:
    """Write one generated README_pypi.md file and return its path."""
    path = root / package.folder / README_NAME
    path.write_text(render_readme(package, root), encoding='utf-8')
    return path


def create_pypi_readmes(root: Path) -> list[Path]:
    """Create the README_pypi.md files for all packages."""
    return [write_readme(package, root) for package in PACKAGES]


def main() -> int:
    """Generate all README_pypi.md files and report what was written."""
    try:
        written = create_pypi_readmes(project_root())
    except (FileNotFoundError, KeyError, ValueError) as error:
        print(f'Failed to create README_pypi.md files: {error}',
              file=sys.stderr)
        return 1
    for path in written:
        print(f'Generated {path}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
