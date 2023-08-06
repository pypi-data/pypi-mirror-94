# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pmatcher']

package_data = \
{'': ['*']}

install_requires = \
['fuzzywuzzy>=0.18.0,<0.19.0', 'python-Levenshtein>=0.12.2,<0.13.0']

setup_kwargs = {
    'name': 'pmatcher',
    'version': '0.1.0',
    'description': 'Monadic election precinct matcher for gerrymandering data collection and research at MGGG',
    'long_description': None,
    'author': 'Max Fan',
    'author_email': 'theinnovativeinventor@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
