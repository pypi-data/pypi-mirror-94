# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tradehub']

package_data = \
{'': ['*']}

install_requires = \
['base58>=2.1.0,<3.0.0',
 'bech32>=1.2.0,<2.0.0',
 'ecdsa>=0.16.1,<0.17.0',
 'hdwallets>=0.1.2,<0.2.0',
 'jsons>=1.3.1,<2.0.0',
 'mnemonic>=0.19,<0.20',
 'requests>=2.25.1,<3.0.0',
 'web3>=5.15.0,<6.0.0']

setup_kwargs = {
    'name': 'tradehub',
    'version': '1.0.0',
    'description': 'Python Client to interact with the Switcheo Tradehub Blockchain to manage staking, liquidity pools, governance, and trading on Demex.',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
