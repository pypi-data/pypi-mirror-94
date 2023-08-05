# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gotrue']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gotrue',
    'version': '0.1.3',
    'description': 'Python Client Library for GoTrue',
    'long_description': None,
    'author': 'Joel Lee',
    'author_email': 'joel@joellee.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
