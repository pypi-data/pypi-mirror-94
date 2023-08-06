# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['test_package_tufskjywfa']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'test-package-tufskjywfa',
    'version': '2020.1.9',
    'description': 'Small test library.',
    'long_description': None,
    'author': 'Abc',
    'author_email': 'nr4809+26fip69foy9ec@sharklasers.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
