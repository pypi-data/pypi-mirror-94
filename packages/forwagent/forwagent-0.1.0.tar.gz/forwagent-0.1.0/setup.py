# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['forwagent']

package_data = \
{'': ['*']}

extras_require = \
{'init': ['cryptography>=3.3.1,<4.0.0'], 'server': ['paramiko>=2.7.2,<3.0.0']}

entry_points = \
{'console_scripts': ['forwagent = forwagent.cli:main']}

setup_kwargs = {
    'name': 'forwagent',
    'version': '0.1.0',
    'description': 'GPG/SSH agent forwarder.',
    'long_description': None,
    'author': 'Dain Nilsson',
    'author_email': 'dain@yubico.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
