# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nameko_tool']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nameko-tool',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'andrew-su',
    'author_email': 'andrew-su@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
