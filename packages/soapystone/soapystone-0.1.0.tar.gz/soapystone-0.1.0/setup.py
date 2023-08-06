# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['soapystone']

package_data = \
{'': ['*']}

install_requires = \
['pylint>=2.6.0,<3.0.0']

setup_kwargs = {
    'name': 'soapystone',
    'version': '0.1.0',
    'description': 'Pylint checker for enforcing orange soapstone comments',
    'long_description': None,
    'author': 'Zach Banks',
    'author_email': 'zjbanks@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
