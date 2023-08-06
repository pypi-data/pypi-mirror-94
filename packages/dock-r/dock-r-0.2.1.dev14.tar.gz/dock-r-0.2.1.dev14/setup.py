# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dock_r']

package_data = \
{'': ['*']}

install_requires = \
['docker>=4.4.1,<5.0.0',
 'fire>=0.4.0,<0.5.0',
 'logless>=0.2.1,<0.3.0',
 'runnow>=0.1.0,<0.2.0',
 'uio>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['dock-r = dock_r.cli:_main']}

setup_kwargs = {
    'name': 'dock-r',
    'version': '0.2.1.dev14',
    'description': 'Tools to go faster with docker.',
    'long_description': None,
    'author': 'AJ Steers',
    'author_email': 'aj.steers@slalom.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
