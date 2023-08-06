# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycaw']

package_data = \
{'': ['*']}

install_requires = \
['comtypes>=1.1.8,<2.0.0', 'future>=0.18.2,<0.19.0', 'psutil>=5.8.0,<6.0.0']

setup_kwargs = {
    'name': 'pycaw-rf',
    'version': '20210213',
    'description': '',
    'long_description': None,
    'author': 'Julia Patrin',
    'author_email': 'papercrane@reversefold.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
