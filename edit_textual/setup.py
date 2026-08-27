#! /usr/local/bin/python3
"""Setup file specifying build of .whl."""

from setuptools import setup

setup(
  name='edit-cfg-json-textual',
  version='0.1.1',
  description='Library for editing config-as-json with textual.',
  author='Tom Björkholm',
  author_email='klausuler_linnet0q@icloud.com',
  python_requires='>=3.12',
  packages=['edit_cfg_json_textual'],
  package_dir={'edit_cfg_json_textual': 'src/edit_cfg_json_textual'},
  package_data={'edit_cfg_json_textual': ['py.typed']},
  install_requires=[
    'edit-cfg-json >= 0.1.1, == 0.1.*',
    'textual >= 8.2.8',
    'argcomplete >= 3.7.2',
    'versionreporter >= 0.4'
  ]
)
