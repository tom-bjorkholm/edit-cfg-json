#! /usr/local/bin/python3
"""Setup file specifying build of .whl."""

from setuptools import setup

setup(
  name='edit-cfg-json-tk',
  version='0.2.1',
  description='Library for editing config-as-json with Tkinter.',
  author='Tom Björkholm',
  author_email='klausuler_linnet0q@icloud.com',
  python_requires='>=3.12',
  packages=['edit_cfg_json_tk'],
  package_dir={'edit_cfg_json_tk': 'src/edit_cfg_json_tk'},
  package_data={'edit_cfg_json_tk': ['py.typed']},
  install_requires=[
    'edit-cfg-json >= 0.2.1, == 0.2.*',
    'argcomplete >= 3.7.2',
    'versionreporter >= 0.4'
  ]
)
