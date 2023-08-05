# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['garfetch']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'garfetch',
    'version': '0.1.0',
    'description': 'gocomics comic fetcher library',
    'long_description': None,
    'author': 'Ave',
    'author_email': 'ave@ave.zone',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
