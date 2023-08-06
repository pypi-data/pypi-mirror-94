# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['airplanesdk']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'airplanesdk',
    'version': '0.1.0',
    'description': 'A Python SDK for writing Airplane tasks',
    'long_description': None,
    'author': 'Airplane',
    'author_email': 'support@airplane.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
