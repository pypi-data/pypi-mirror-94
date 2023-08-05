# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sdotdict']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sdotdict',
    'version': '0.1.0',
    'description': '',
    'long_description': '# sdotdict\nSimple Class-based .dot notation on dictionaries.',
    'author': 'TheBoringDude',
    'author_email': 'iamcoderx@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
