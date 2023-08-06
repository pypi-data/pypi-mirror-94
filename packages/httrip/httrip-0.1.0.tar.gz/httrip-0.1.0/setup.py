# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['httrip']

package_data = \
{'': ['*']}

install_requires = \
['trio>=0.18.0,<0.19.0']

setup_kwargs = {
    'name': 'httrip',
    'version': '0.1.0',
    'description': 'Tiny proof-of-concept HTTP framework for Trio',
    'long_description': None,
    'author': 'L3viathan',
    'author_email': 'git@l3vi.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
