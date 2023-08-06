# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['datastreamcorelib']

package_data = \
{'': ['*']}

install_requires = \
['libadvian>=0.2,<0.3', 'msgpack>=1.0,<2.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

setup_kwargs = {
    'name': 'datastreamcorelib',
    'version': '1.1.2',
    'description': 'Helpers and utilities for https://gitlab.com/advian-oss/python-datastreamservicelib that are not eventloop specific.',
    'long_description': "=================\ndatastreamcorelib\n=================\n\nCore helpers and Abstract Base Classes for making use of ZMQ nice, easy and DRY.\n\nYou should probably look at https://gitlab.com/advian-oss/python-datastreamservicelib and\nhttps://gitlab.com/advian-oss/python-datastreamserviceapp_template unless you're working\non an adapter for yet unsupported eventloop.\n\nDevelopment\n-----------\n\nTLDR:\n\n- make virtualenv\n- poetry install\n- pre-commit install\n\nTesting\n^^^^^^^\n\nThere's Dockerfile for running tox tests (so you don't need to deal with pyenv\nand having all the required versions available)::\n\n    docker build -t datastreamcorelib:tox .\n    docker run --rm -it -v `pwd`:/app datastreamcorelib:tox\n",
    'author': 'Eero af Heurlin',
    'author_email': 'eero.afheurlin@iki.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/advian-oss/python-datastreamcorelib/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
