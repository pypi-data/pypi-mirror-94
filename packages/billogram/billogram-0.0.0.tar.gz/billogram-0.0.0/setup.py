# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['billogram']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'billogram',
    'version': '0.0.0',
    'description': 'Python utilities for Billogram - https://billogram.com/',
    'long_description': '# `billogram`\n\n## Installation with `pip`\n```\n$ pip install billogram\n```\n\nPlaceholder for a Python utility package related to Billogram – https://billogram.com/\n',
    'author': 'Billogram',
    'author_email': 'platform@billogram.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/billogram',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
