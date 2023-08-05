# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['erre2']

package_data = \
{'': ['*'], 'erre2': ['static/*', 'templates/*', 'templates/administration/*']}

install_requires = \
['bcrypt>=3.2.0,<4.0.0',
 'flask>=1.1.2,<2.0.0',
 'flask_sqlalchemy>=2.4.4,<3.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'erre2',
    'version': '1.1.1',
    'description': 'Un server web scritto in python per raccogliere e gestire riassunti universitari',
    'long_description': None,
    'author': 'Lorenzo Balugani',
    'author_email': 'lorenzo.balugani@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
