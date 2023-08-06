# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coroflow']

package_data = \
{'': ['*']}

install_requires = \
['anytree>=2.8.0,<3.0.0']

setup_kwargs = {
    'name': 'coroflow',
    'version': '3.2.3',
    'description': 'Asynchronous pipeline builder',
    'long_description': '# Coroflow\n\nThis is a library for building asynchronous coroutine-based pipelines in Python.\nUseful features include:\n\n* pass data between tasks with queues\n* Connect stages of the pipeline with fanout/fanin patterns or load-balancer patterns\n* mix in blocking taks, coroflow will run it in threads\n* has an apache ariflow like api for connecting tasks\n\n',
    'author': 'Dewald Abrie',
    'author_email': 'dewaldabrie@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dewaldabrie/coroflow/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
