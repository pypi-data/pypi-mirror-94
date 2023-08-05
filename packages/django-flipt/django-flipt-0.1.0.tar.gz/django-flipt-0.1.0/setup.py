# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flipt', 'flipt.templatetags']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.0.0,<4.0.0', 'flipt-grpc-python3>=0.1.0,<0.2.0']

extras_require = \
{'rest': ['djangorestframework>=3.12.2,<4.0.0']}

setup_kwargs = {
    'name': 'django-flipt',
    'version': '0.1.0',
    'description': 'Flipt Integration for Django and Django REST Framework',
    'long_description': '# django-flipt\nFlipt Integration for Django and Django REST Framework\n\n# Requirements\n\n- Docker\n\n# Development\n\n### Run Project\n\n```shell\n$ make\n```\n\n### Linting/Test Project\n\n```shell\n$ make lint\n$ make test\n```\n',
    'author': 'Preeti Yuankrathok',
    'author_email': 'preetisatit@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/earthpyy/django-flipt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
