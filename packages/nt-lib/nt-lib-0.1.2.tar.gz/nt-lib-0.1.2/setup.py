# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nt', 'nt.lib']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['nt-lib = nt.lib:app']}

setup_kwargs = {
    'name': 'nt-lib',
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
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
