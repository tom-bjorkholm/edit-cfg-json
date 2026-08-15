#! /usr/bin/env python3
"""What `edit-cfg-json-tk` answers `--version` with.

The report of this package is the report of the core with this distribution in
front of it, because that is the package whoever runs this program installed
and the one an upgrade instruction has to name. Everything below it is
inherited rather than written again, and there is nothing to add: Tkinter comes
with Python, so this package depends on nothing the core does not.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from edit_cfg_json import EcajVersionReporter

MAIN_PACKAGE = 'edit-cfg-json-tk'
"""Distribution that this program is installed from."""


class TkVersionReporter(EcajVersionReporter):
    """Report what this package and everything below it are."""

    def package_names(self) -> list[str]:
        """Return the distributions whose versions are reported.

        Returns:
            This distribution first, and then the ones the core lists.
        """
        return [MAIN_PACKAGE, *super().package_names()]

    @classmethod
    def get_main_package_name(cls) -> str:
        """Return the distribution that the upgrade instructions name.

        Returns:
            What to install to upgrade the program that is running.
        """
        return MAIN_PACKAGE
