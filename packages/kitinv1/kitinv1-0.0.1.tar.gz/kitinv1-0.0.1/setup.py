# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['kitinv1']
setup_kwargs = {
    'name': 'kitinv1',
    'version': '0.0.1',
    'description': 'By Sergey kitin',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
