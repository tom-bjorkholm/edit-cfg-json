#! /usr/local/bin/python3
"""Setup file specifying build of .whl."""

from setuptools import setup

setup(
  name='edit-cfg-json',
  version='0.0.3',
  description='UI agnostic library for editing config-as-json.',
  author='Tom Björkholm',
  author_email='klausuler_linnet0q@icloud.com',
  python_requires='>=3.12',
  packages=['edit_cfg_json'],
  package_dir={'edit_cfg_json': 'src/edit_cfg_json'},
  package_data={'edit_cfg_json': ['py.typed']},
  install_requires=[
    'config-as-json >= 1.5',
    'argcomplete >= 3.7.2',
    'wizard-ui-bridge >= 1.3'
  ]
)
