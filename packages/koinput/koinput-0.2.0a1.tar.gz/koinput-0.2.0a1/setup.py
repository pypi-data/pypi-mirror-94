# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['koinput']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0']

setup_kwargs = {
    'name': 'koinput',
    'version': '0.2.0a1',
    'description': 'Maximum simplification of Input / Output for text programs.',
    'long_description': None,
    'author': 'Николай Перминов',
    'author_email': 'kolya-perminov@ya.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
