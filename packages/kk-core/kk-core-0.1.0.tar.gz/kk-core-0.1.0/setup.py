# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kk', 'kk.core']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['kk = kk.core.main:app']}

setup_kwargs = {
    'name': 'kk-core',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Uriel Mandujano',
    'author_email': 'uriel.mandujano14@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
