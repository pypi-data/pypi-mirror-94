# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pydeco']
install_requires = \
['forbiddenfruit>=0.1.4,<0.2.0']

setup_kwargs = {
    'name': 'py-deco',
    'version': '0.1.0',
    'description': 'Python decorators',
    'long_description': '',
    'author': 'ugo-quelhas',
    'author_email': 'ugo.quelhas@edu.devinci.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/quelhasu/pydeco',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
