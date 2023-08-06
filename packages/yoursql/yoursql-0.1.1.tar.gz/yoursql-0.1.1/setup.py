# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['yoursql']
entry_points = \
{'console_scripts': ['crawl = yoursql:main']}

setup_kwargs = {
    'name': 'yoursql',
    'version': '0.1.1',
    'description': 'An ORM for SQL backends',
    'long_description': None,
    'author': 'trumanpurnell',
    'author_email': 'truman.purnell@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
