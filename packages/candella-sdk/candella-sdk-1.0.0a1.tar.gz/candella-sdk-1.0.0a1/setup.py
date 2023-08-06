# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['candella_sdk']

package_data = \
{'': ['*']}

install_requires = \
['cookiecutter>=1.7.2,<2.0.0']

entry_points = \
{'console_scripts': ['candella-sdk = candella_sdk:main']}

setup_kwargs = {
    'name': 'candella-sdk',
    'version': '1.0.0a1',
    'description': 'Create and manage Candella apps and services with ease.',
    'long_description': None,
    'author': 'Marquis Kurt',
    'author_email': 'software@marquiskurt.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/UnscriptedVN/candella-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
