# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hodl_cli']

package_data = \
{'': ['*']}

install_requires = \
['cbpro>=1.1.4,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.13.0,<3.0.0']

entry_points = \
{'console_scripts': ['hodl-cli = hodl_cli.cli:run']}

setup_kwargs = {
    'name': 'hodl-cli',
    'version': '2.0.1',
    'description': 'Dollar-cost averaging for crypto on the command line.',
    'long_description': None,
    'author': 'Mark Hudnall',
    'author_email': 'me@markhudnall.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
