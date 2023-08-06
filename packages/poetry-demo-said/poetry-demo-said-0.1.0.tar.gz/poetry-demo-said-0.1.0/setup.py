# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_demo_said']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'poetry-demo-said',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'said',
    'author_email': 'albertadine760@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
