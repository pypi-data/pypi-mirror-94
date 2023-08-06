# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logless']

package_data = \
{'': ['*']}

install_requires = \
['psutil>=5.8.0,<6.0.0', 'tqdm>=4.56.1,<5.0.0', 'xmlrunner>=1.7.7,<2.0.0']

setup_kwargs = {
    'name': 'logless',
    'version': '0.2.2',
    'description': '',
    'long_description': None,
    'author': 'AJ Steers',
    'author_email': 'aj.steers@slalom.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
