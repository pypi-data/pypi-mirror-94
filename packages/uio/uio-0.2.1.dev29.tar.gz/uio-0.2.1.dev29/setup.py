# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uio']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.4.0,<0.5.0', 'logless>=0.2.2,<0.3.0', 'runnow>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['uio = uio.uio:main']}

setup_kwargs = {
    'name': 'uio',
    'version': '0.2.1.dev29',
    'description': 'Universal IO (uio) library.',
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
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
