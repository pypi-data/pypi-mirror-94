# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['dbdpy']
setup_kwargs = {
    'name': 'dbdpy',
    'version': '1.2.7',
    'description': 'Discord Bot Designer For Discord module for python writen by Edited cocktail, official server: https://discord.gg/t9wHKGtD7p',
    'long_description': None,
    'author': 'Winter_coctail',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
