# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reservoirdb']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.3,<4.0.0',
 'dacite>=1.6.0,<2.0.0',
 'pandas>=1.2.2,<2.0.0',
 'pyarrow>=3.0.0,<4.0.0',
 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'reservoirdb',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Ruan Pearce-Authers',
    'author_email': 'ruan@reservoirdb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
