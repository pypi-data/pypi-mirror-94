# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nt', 'nt.app']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'nt-app',
    'version': '0.1.2',
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
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
