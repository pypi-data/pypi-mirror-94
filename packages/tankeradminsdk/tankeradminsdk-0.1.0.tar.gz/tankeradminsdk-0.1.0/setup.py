# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tankeradminsdk']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tankeradminsdk',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Tanker team',
    'author_email': 'tech@tanker.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://tanker.io',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
