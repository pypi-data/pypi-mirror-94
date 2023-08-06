# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['datastreamservicelib']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'datastreamcorelib>=1.1,<2.0',
 'pyzmq>=19.0,<20.0',
 'toml>=0.10,<0.11',
 'tomlkit>=0.6,<0.7']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

entry_points = \
{'console_scripts': ['testpublisher = '
                     'datastreamservicelib.console:publisher_cli',
                     'testsubscriber = '
                     'datastreamservicelib.console:subscriber_cli']}

setup_kwargs = {
    'name': 'datastreamservicelib',
    'version': '1.8.3',
    'description': '',
    'long_description': "====================\ndatastreamservicelib\n====================\n\nAsyncIO eventloop helpers and Abstract Base Classes for making services that use ZMQ nice, easy and DRY\n\nUsage\n-----\n\nUse the CookieCutter template at https://gitlab.com/advian-oss/python-datastreamserviceapp_template\n\nYou can also take a look at src/datastreamservicelib/console.py for some very simple test examples.\n\n\nDevelopment\n-----------\n\nTLDR:\n\n- create Python 3.7 virtualenv and activate it (pro tip: virtualenvwrapper)\n- poetry install\n- pre-commit install\n\n\nTesting\n^^^^^^^\n\nThere's Dockerfile for running tox tests (so you don't need to deal with pyenv\nand having all the required versions available)::\n\n    docker build -t datastreamservicelib:tox .\n    docker run --rm -it -v `pwd`:/app datastreamservicelib:tox\n",
    'author': 'Eero af Heurlin',
    'author_email': 'eero.afheurlin@iki.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/advian-oss/python-datastreamservicelib/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
