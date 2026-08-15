#! /usr/bin/env python3
"""What one program of this library answers `--version` with.

Whoever is about to report a problem, and whoever is about to upgrade, has to
know which versions are really installed and whether newer ones exist.
[`versionreporter`](https://pypi.org/project/versionreporter/) answers both, so
`--version` is one call to it rather than a version string of this library's
own: it reads the installed version of every package named below, asks PyPI
what is available for this Python version and for a newer one, and says which
of them are worth upgrading to.

**What a program reports is the distribution it was installed from**, and the
packages that distribution is built on. So this class is derived once per
distribution, each editor package putting its own name in front of what the
core already lists, which is what keeps one list of dependencies from becoming
three. The name in front is not only for reading: `versionreporter` takes the
first of them as the package its upgrade instructions name.

**It has to be a class and not a name handed to one.**
`get_main_package_name` and `recommended_python` are class methods of
`versionreporter`, so two instances of one class cannot answer them
differently, and a class per distribution is what that leaves.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import date
from packaging.version import Version
from versionreporter import SupportExpires, VersionReporter

MAIN_PACKAGE = 'edit-cfg-json'
"""Distribution that the core of this library is installed from."""


class EcajVersionReporter(VersionReporter):
    """Report what this package and everything it is built on are.

    It is what `python3 -m edit_cfg_json.dump` answers `--version` with, and
    the base class of the reporter of each editor package, which is what lets
    a backend name itself without repeating what this package depends on.
    """

    def package_names(self) -> list[str]:
        """Return the distributions whose versions are reported.

        Returns:
            This distribution first, because that is the one an upgrade
            instruction names, and then everything it declares.
        """
        return [MAIN_PACKAGE, 'config-as-json', 'argcomplete',
                'versionreporter', 'packaging']

    def get_app_support_expires(self) -> SupportExpires:
        """Return when these packages stop being released for an old Python.

        The dates follow the cadence `versionreporter` uses for itself, which
        drops a Python version well before that version's own end of life:
        what these packages promise is a release for a new Python and not a
        bug fix for an old one.

        Returns:
            For each date, the newest Python version that is no longer
            supported once that date has passed.
        """
        return {date(year=2027, month=3, day=1): '3.12',
                date(year=2028, month=3, day=1): '3.13'}

    @classmethod
    def get_main_package_name(cls) -> str:
        """Return the distribution that the upgrade instructions name.

        Returns:
            What to install to upgrade the program that is running.
        """
        return MAIN_PACKAGE

    @classmethod
    def recommended_python(cls) -> Version:
        """Return the Python version these packages are meant to run on.

        Returns:
            The newest Python version every one of them is released for.
        """
        return Version('3.14')
