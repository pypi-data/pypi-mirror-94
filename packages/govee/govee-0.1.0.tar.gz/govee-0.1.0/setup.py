# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['govee']

package_data = \
{'': ['*']}

install_requires = \
['bleak>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'govee',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Kevin Schmittle',
    'author_email': 'kevin@schmittle.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
