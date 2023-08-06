# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prometheus_utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'prometheus-utils',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'thomas',
    'author_email': 'thomas@zumper.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
