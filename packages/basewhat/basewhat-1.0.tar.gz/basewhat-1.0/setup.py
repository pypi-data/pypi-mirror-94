# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['basewhat']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'basewhat',
    'version': '1.0',
    'description': 'A Python utility for encoding/decoding arbitrary-base numbers.',
    'long_description': None,
    'author': 'Paul Bissex',
    'author_email': 'paul@bissex.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://hg.sr.ht/~paulbissex/basewhat',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
