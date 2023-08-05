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
    'version': '0.2.0',
    'description': 'Unofficial gocomics library',
    'long_description': '# garfetch\n\nPython 3 library to fetch comic images from gocomics.com.\n\n## Installation\n\n### PyPI\n\nThis package is available on PyPI as `garfetch`.\n\n### Building\n\nThis project uses [poetry](https://python-poetry.org/), and the recommended way of building it is running `poetry build` on the root of this repository.\n\n## Usage\n\n### Get comic URL\n\n`garfetch.fetch_url(comic, datestr)` can be used to fetch comic URL for a given comic on a given day. Comic slug can be extracted from a gocomics URL. Date format is `YYYY-MM-DD` or `YYYY/MM/DD`.\n\n```python\nimport garfetch\n\nprint(garfetch.fetch_url("garfield", "1990-05-30"))\n# \'https://assets.amuniversal.com/7e81c7c05d1a012ee3bd00163e41dd5b\'\n```\n\nA non-existant comic or a server error will currently throw an AssertionError. This behavior may be changed in the future.\n\n### Get comic calendar\n\n`garfetch.fetch_calendar(comic, datestr)` can be used to fetch a list of comics available on a given month. Comic slug can be extracted from a gocomics URL. Date input format is `YYYY-MM` or `YYYY/MM`. Date output format is a list of `YYYY/MM/DD`s.\n\n```python\nimport garfetch\n\nprint(repr(garfetch.fetch_calendar("garfield-classics", "2020-07")))\n# [\'2020/07/01\', \'2020/07/02\', \'2020/07/03\', \'2020/07/04\', \'2020/07/05\', \'2020/07/06\', \'2020/07/07\', \'2020/07/08\', \'2020/07/09\', \'2020/07/10\', \'2020/07/11\', \'2020/07/12\', \'2020/07/13\', \'2020/07/14\', \'2020/07/15\', \'2020/07/16\', \'2020/07/17\', \'2020/07/18\', \'2020/07/19\', \'2020/07/20\', \'2020/07/21\', \'2020/07/22\', \'2020/07/23\', \'2020/07/24\', \'2020/07/25\', \'2020/07/26\', \'2020/07/27\', \'2020/07/28\', \'2020/07/29\', \'2020/07/30\', \'2020/07/31\']\n\nprint(repr(garfetch.fetch_calendar("garfield-classics", "2019-01")))\n# [\'2019/01/07\', \'2019/01/08\', \'2019/01/09\', \'2019/01/10\', \'2019/01/11\', \'2019/01/12\', \'2019/01/13\', \'2019/01/14\', \'2019/01/15\', \'2019/01/16\', \'2019/01/17\', \'2019/01/18\', \'2019/01/19\', \'2019/01/20\', \'2019/01/21\', \'2019/01/22\', \'2019/01/23\', \'2019/01/24\', \'2019/01/25\', \'2019/01/26\', \'2019/01/27\', \'2019/01/28\', \'2019/01/29\', \'2019/01/30\', \'2019/01/31\']\n```\n\nA non-existant comic or a server error will currently throw an AssertionError. This behavior may be changed in the future.\n',
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
