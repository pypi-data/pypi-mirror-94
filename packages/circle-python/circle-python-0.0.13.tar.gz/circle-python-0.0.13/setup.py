# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['circle', 'circle.resources', 'circle.resources.abstract']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.20.0']

setup_kwargs = {
    'name': 'circle-python',
    'version': '0.0.13',
    'description': '',
    'long_description': None,
    'author': 'Crawford Leeds',
    'author_email': 'crawford@crawfordleeds.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
