# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cjob']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cjob',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Matthew Segal',
    'author_email': 'mattdsegal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
