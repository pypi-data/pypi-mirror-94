# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_assert_check']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['flake8.extension = FCA=flake8_assert_check:Plugin']}

setup_kwargs = {
    'name': 'flake8-assert-check',
    'version': '0.1',
    'description': 'Plugin for flake8 that checks for asserts in tests.',
    'long_description': None,
    'author': 'netqa GmbH',
    'author_email': 'contact@netqa.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
