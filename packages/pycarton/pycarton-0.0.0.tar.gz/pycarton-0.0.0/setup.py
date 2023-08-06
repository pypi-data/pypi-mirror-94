# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['carton']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pycarton',
    'version': '0.0.0',
    'description': 'Python toolbox.',
    'long_description': None,
    'author': 'Yevgnen Koh',
    'author_email': 'wherejoystarts@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
