# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pfhedge']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pfhedge',
    'version': '0.0.0',
    'description': '',
    'long_description': None,
    'author': 'Shota Imaki',
    'author_email': 'shota.imaki.0801@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
