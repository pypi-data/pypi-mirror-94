# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jackal',
 'jackal.helpers',
 'jackal.management',
 'jackal.management.commands',
 'jackal.mixins',
 'jackal.views']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.0.2,<4.0.0', 'djangorestframework>=3.11.0,<4.0.0']

setup_kwargs = {
    'name': 'django-jackal',
    'version': '3.0.0',
    'description': 'extension of Django REST Framework',
    'long_description': '# Jackal, Django Rest Framework extension\n\n[![version badge](https://badge.fury.io/py/django-jackal.svg)](https://badge.fury.io/py/django-jackal)\n\n![jackal image](https://imgur.com/XnlU8T9.jpg)\n\n> Warning! This project is for personal use. Therefore, there are no documents, and the code changes are arbitrary.\n\n**Jackal** is extension of Django REST Framework(DRF)\nthat help you easily implement the necessary features on your web backend server.\n\n## Installation\n\n    pip install django-jackal\n',
    'author': 'joyongjin',
    'author_email': 'wnrhd114@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/joyongjin/jackal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
