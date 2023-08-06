# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pysxmovesx']
setup_kwargs = {
    'name': 'pysxmovesx',
    'version': '1.0.0',
    'description': 'Use class Global to move.',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
