# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['resworb', 'resworb.browsers', 'resworb.commands']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'lz4>=3.1.3,<4.0.0', 'pytoml>=0.1.21,<0.2.0']

setup_kwargs = {
    'name': 'resworb',
    'version': '0.1.0',
    'description': 'Manage browser data in Python.',
    'long_description': None,
    'author': 'Yevgnen Koh',
    'author_email': 'wherejoystarts@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
