# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nlloc', 'nlloc.core']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=0.29.21,<0.30.0',
 'dvc>=1.11.15,<2.0.0',
 'ipython>=7.20.0,<8.0.0',
 'pytest>=6.2.2,<7.0.0',
 'setuptools_cpp>=0.1.0,<0.2.0',
 'uquake>=0.2.1,<0.3.0']

setup_kwargs = {
    'name': 'nlloc',
    'version': '0.2.1',
    'description': 'wrapper around A. Lomax NLLoc',
    'long_description': None,
    'author': 'jpmercier',
    'author_email': 'jpmercier01@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
