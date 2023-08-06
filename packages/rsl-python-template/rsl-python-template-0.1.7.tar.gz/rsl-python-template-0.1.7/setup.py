# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rsl_python_template']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=3.8.4,<4.0.0', 'mypy>=0.800,<0.801']

setup_kwargs = {
    'name': 'rsl-python-template',
    'version': '0.1.7',
    'description': '',
    'long_description': None,
    'author': 'Ryan Gerstenkorn',
    'author_email': 'ryan.gerstenkorn@rhinosecuritylabs.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
