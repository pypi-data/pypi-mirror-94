# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lucyparser']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lucyparser',
    'version': '0.2.1',
    'description': 'Lucene-like syntax parser',
    'long_description': None,
    'author': 'Timur',
    'author_email': 'timur.makarchuk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
