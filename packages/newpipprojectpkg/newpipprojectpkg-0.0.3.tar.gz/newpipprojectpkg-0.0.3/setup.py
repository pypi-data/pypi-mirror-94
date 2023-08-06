# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['newpipprojectpkg',
 'newpipprojectpkg.newpipprojectpkg',
 'newpipprojectpkg.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'newpipprojectpkg',
    'version': '0.0.3',
    'description': '',
    'long_description': None,
    'author': 'basma',
    'author_email': 'basmaelsaify@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
