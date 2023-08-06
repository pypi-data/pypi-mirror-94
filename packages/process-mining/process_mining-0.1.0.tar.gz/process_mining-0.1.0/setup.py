# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['process_mining']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'process-mining',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'luttik',
    'author_email': 'dtluttik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
