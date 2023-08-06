# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['dbustiker']
install_requires = \
['vk-api>=11.9.1,<12.0.0']

setup_kwargs = {
    'name': 'dbustiker',
    'version': '1.0.0',
    'description': 'Получение наборов стикеров которые есть у других пользователей вк их ценну в рублях и голосах.',
    'long_description': None,
    'author': 'Сергей Бухтояров',
    'author_email': 'darsox.anime@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
