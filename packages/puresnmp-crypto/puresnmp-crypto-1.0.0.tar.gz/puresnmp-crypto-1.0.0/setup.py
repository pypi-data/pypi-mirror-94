# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['puresnmp_plugins', 'puresnmp_plugins.priv']

package_data = \
{'': ['*']}

install_requires = \
['pycrypto>=2.6.1,<3.0.0']

setup_kwargs = {
    'name': 'puresnmp-crypto',
    'version': '1.0.0',
    'description': 'Implementation for SNMPv3 encryption in puresnmp',
    'long_description': 'Encryption Plugin for puresnmp\n==============================\n\nThis package provides support for DES and AES encryption in puresnmp.\n\nThe package is *not* intended as standalone package and only provides a\nnamespace package for ``puresnmp``.\n\nSee the the documentation of ``puresnmp`` for more on these plugins.\n',
    'author': 'Michel Albert',
    'author_email': 'michel.albert@post.lu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/puresnmp/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
