# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lichessbotpoetry', 'lichessbotpoetry.api', 'lichessbotpoetry.bot']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.3,<4.0.0', 'asyncio>=3.4.3,<4.0.0', 'python-chess>=1.999,<2.0']

setup_kwargs = {
    'name': 'lichessbotpoetry',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'pythonideas',
    'author_email': 'rustbotchessapp@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
