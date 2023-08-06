# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sns_message_validator2']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=3.2,<4.0', 'requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'aws-sns-message-validator2',
    'version': '0.0.1',
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
