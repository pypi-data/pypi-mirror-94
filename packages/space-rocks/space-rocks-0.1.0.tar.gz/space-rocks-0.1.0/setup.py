# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rocks']

package_data = \
{'': ['*']}

install_requires = \
['aiodns>=2.0.0,<3.0.0',
 'aiohttp>=3.7.3,<4.0.0',
 'cchardet>=2.1.7,<3.0.0',
 'chardet<4.0',
 'click>=7.1.2,<8.0.0',
 'iterfzf>=0.5.0,<0.6.0',
 'matplotlib>=3.3.4,<4.0.0',
 'numpy>=1.20.0,<2.0.0',
 'pandas>=1.2.1,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=9.10.0,<10.0.0',
 'tqdm>=4.56.0,<5.0.0']

setup_kwargs = {
    'name': 'space-rocks',
    'version': '0.1.0',
    'description': 'Python client for SsODNet data access.',
    'long_description': None,
    'author': 'Max Mahlke',
    'author_email': 'max.mahlke@oca.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://rocks.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
