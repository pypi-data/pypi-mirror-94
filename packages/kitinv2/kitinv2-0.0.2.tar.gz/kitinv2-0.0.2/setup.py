# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['kitinv2']
setup_kwargs = {
    'name': 'kitinv2',
    'version': '0.0.2',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
