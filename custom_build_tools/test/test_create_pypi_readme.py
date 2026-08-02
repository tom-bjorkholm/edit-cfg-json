#! /usr/bin/env python3
"""Tests for the README_pypi.md generator in custom_build_tools."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import pytest
import create_pypi_readme_venv as generator

PACKAGE = generator.Package('pkg', 'my-package', 'my_package')


def make_parts(root: Path, template: str, common: dict[str, str],
               local: dict[str, str]) -> None:
    """Create common and package fragment folders with given contents."""
    common_dir = root / generator.PARTS_DIR_NAME
    local_dir = root / PACKAGE.folder / generator.PARTS_DIR_NAME
    common_dir.mkdir(parents=True)
    local_dir.mkdir(parents=True)
    (local_dir / generator.TEMPLATE_NAME).write_text(template,
                                                     encoding='utf-8')
    for name, text in common.items():
        (common_dir / name).write_text(text, encoding='utf-8')
    for name, text in local.items():
        (local_dir / name).write_text(text, encoding='utf-8')


def test_include_and_vars(tmp_path: Path) -> None:
    """Test includes are inserted and variables are substituted."""
    make_parts(tmp_path, '# {{dist_name}}\n\n{{include: body.md}}\n',
               {'body.md': '\nInstall {{dist_name}} as {{import_name}}.\n'},
               {})
    text = generator.render_readme(PACKAGE, tmp_path)
    assert text == '# my-package\n\nInstall my-package as my_package.\n'


def test_local_fragment_wins(tmp_path: Path) -> None:
    """Test a package fragment shadows a common fragment of the same name."""
    make_parts(tmp_path, '{{include: body.md}}\n', {'body.md': 'common'},
               {'body.md': 'local'})
    assert generator.render_readme(PACKAGE, tmp_path) == 'local\n'


def test_nested_include(tmp_path: Path) -> None:
    """Test a fragment may itself include another fragment."""
    make_parts(tmp_path, '{{include: outer.md}}\n',
               {'outer.md': 'a {{include: inner.md}}', 'inner.md': 'b'}, {})
    assert generator.render_readme(PACKAGE, tmp_path) == 'a b\n'


def test_write_creates_readme(tmp_path: Path) -> None:
    """Test the generated file is written into the package folder."""
    make_parts(tmp_path, 'text\n', {}, {})
    path = generator.write_readme(PACKAGE, tmp_path)
    assert path == tmp_path / PACKAGE.folder / generator.README_NAME
    assert path.read_text(encoding='utf-8') == 'text\n'


def test_missing_fragment(tmp_path: Path) -> None:
    """Test a missing fragment raises instead of producing partial text."""
    make_parts(tmp_path, '{{include: absent.md}}\n', {}, {})
    with pytest.raises(FileNotFoundError):
        generator.render_readme(PACKAGE, tmp_path)


def test_unknown_variable(tmp_path: Path) -> None:
    """Test an unknown variable raises instead of being left in the text."""
    make_parts(tmp_path, '{{no_such_name}}\n', {}, {})
    with pytest.raises(KeyError):
        generator.render_readme(PACKAGE, tmp_path)


def test_self_include_fails(tmp_path: Path) -> None:
    """Test a fragment cycle is reported instead of recursing forever."""
    make_parts(tmp_path, '{{include: loop.md}}\n',
               {'loop.md': '{{include: loop.md}}'}, {})
    with pytest.raises(ValueError):
        generator.render_readme(PACKAGE, tmp_path)


@pytest.mark.parametrize('package', generator.PACKAGES,
                         ids=[item.folder for item in generator.PACKAGES])
def test_names_match_setup(package: generator.Package) -> None:
    """Test every generator entry matches the setup.py of its folder."""
    setup_file = generator.project_root() / package.folder / 'setup.py'
    setup_text = setup_file.read_text(encoding='utf-8')
    assert f"name='{package.dist_name}'" in setup_text
    assert f"packages=['{package.import_name}']" in setup_text


@pytest.mark.parametrize('package', generator.PACKAGES,
                         ids=[item.folder for item in generator.PACKAGES])
def test_real_parts_render(package: generator.Package) -> None:
    """Test the checked in fragments render with no directive left over."""
    text = generator.render_readme(package, generator.project_root())
    assert text.startswith(f'# {package.dist_name}\n')
    assert '## Test summary' in text
    assert '{{' not in text
