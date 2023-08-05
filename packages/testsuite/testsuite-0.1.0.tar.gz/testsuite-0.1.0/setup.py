# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['testsuite', 'testsuite.tests']

package_data = \
{'': ['*']}

install_requires = \
['lxml==4.6.2']

entry_points = \
{'console_scripts': ['testsuite = testsuite.console:main']}

setup_kwargs = {
    'name': 'testsuite',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Nick Long',
    'author_email': 'nicholas.long@nrel.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
