# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['search_that_hash',
 'search_that_hash.cracker',
 'search_that_hash.cracker.offline_mod',
 'search_that_hash.cracker.online_mod']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'loguru>=0.5.2,<0.6.0',
 'name-that-hash>=0.8.0,<0.9.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=9.10.0,<10.0.0',
 'toml>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['name-that-hash = search_that_hash.main:main',
                     'sth = search_that_hash.main:main']}

setup_kwargs = {
    'name': 'search-that-hash',
    'version': '0.1.1',
    'description': 'Search hashes quickly before cracking them',
    'long_description': None,
    'author': 'Jayy',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
