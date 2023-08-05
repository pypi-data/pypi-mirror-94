# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastgrpc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fastgrpc',
    'version': '0.1.0',
    'description': '### FastgRPC framework, fast to code',
    'long_description': '### FastgRPC framework, fast to code',
    'author': 'Euraxluo',
    'author_email': 'euraxluo@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Euraxluo/fastgrpc',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
