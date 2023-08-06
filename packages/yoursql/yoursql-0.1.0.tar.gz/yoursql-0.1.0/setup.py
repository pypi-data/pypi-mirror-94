# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['yoursql']
setup_kwargs = {
    'name': 'yoursql',
    'version': '0.1.0',
    'description': 'An ORM for SQL backends',
    'long_description': None,
    'author': 'trumanpurnell',
    'author_email': 'truman.purnell@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
