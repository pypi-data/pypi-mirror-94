# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['newversion']

package_data = \
{'': ['*']}

install_requires = \
['packaging>=20.0,<21.0']

setup_kwargs = {
    'name': 'newversion',
    'version': '0.1.0',
    'description': 'Version manager compatible with packaging',
    'long_description': None,
    'author': 'Vlad Emelianov',
    'author_email': 'volshebnyi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
