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
    'version': '0.1.1',
    'description': 'Unofficial gocomics library',
    'long_description': '# garfetch\n\nPython 3 library to fetch comic images from gocomics.com.\n\n## Installation\n\n### PyPI\n\nThis package is available on PyPI as `garfetch`.\n\n### Building\n\nThis project uses [poetry](https://python-poetry.org/), and the recommended way of building it is running `poetry build` on the root of this repository.\n\n## Usage\n\n### Get comic URL\n\n```python\nimport garfetch\n\nprint(garfetch.fetch_url("garfield", "1990-05-30"))\n# If comic exists: \'https://assets.amuniversal.com/7e81c7c05d1a012ee3bd00163e41dd5b\'\n# If comic does not exist: None\n```\n',
    'author': 'Ave',
    'author_email': 'ave@ave.zone',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/a/garfetch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
