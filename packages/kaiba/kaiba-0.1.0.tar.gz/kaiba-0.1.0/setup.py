# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kaiba']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'kaiba',
    'version': '0.1.0',
    'description': 'coming soon',
    'long_description': None,
    'author': 'Thomas Borgen',
    'author_email': 'thomasborgen91@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
