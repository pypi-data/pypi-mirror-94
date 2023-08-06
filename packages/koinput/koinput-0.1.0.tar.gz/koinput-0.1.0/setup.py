# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['koinput']
setup_kwargs = {
    'name': 'koinput',
    'version': '0.1.0',
    'description': 'Maximum simplification of Input / Output for text programs.',
    'long_description': None,
    'author': 'k0per',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '==3.6.12',
}


setup(**setup_kwargs)
