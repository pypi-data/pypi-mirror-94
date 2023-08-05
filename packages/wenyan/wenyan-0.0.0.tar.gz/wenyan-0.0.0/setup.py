# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wenyan']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'wenyan',
    'version': '0.0.0',
    'description': 'Programming Language for the ancient Chinese',
    'long_description': None,
    'author': 'Tang Ziya',
    'author_email': 'tcztzy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
