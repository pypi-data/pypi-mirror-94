# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['symtool']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'hexdump>=3.3,<4.0', 'pyserial>=3.5,<4.0']

entry_points = \
{'console_scripts': ['symtool = symtool.main:main']}

setup_kwargs = {
    'name': 'symtool',
    'version': '0.0.3',
    'description': '',
    'long_description': None,
    'author': 'Lars Kellogg-Stedman',
    'author_email': 'lars@oddbit.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
