# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['basewhat']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'basewhat',
    'version': '1.0.1',
    'description': 'A Python utility for encoding/decoding arbitrary-base numbers.',
    'long_description': '\ufeffbasewhat\n========\n\nA Python utility for encoding/decoding arbitrary-base numbers.\n\nBug tracker: <https://todo.sr.ht/~paulbissex/basewhat>\n\nAuthor: Paul Bissex <paul@bissex.net>\n',
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
