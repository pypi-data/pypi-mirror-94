# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['corcovado', 'corcovado.api', 'corcovado.database']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy-Utils>=0.36.8,<0.37.0',
 'SQLAlchemy>=1.3.23,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'pyfiglet>=0.8.post1,<0.9',
 'pytest-mock>=3.5.1,<4.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'rich>=9.10.0,<10.0.0',
 'typer>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'corcovado',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Alexandre Xavier',
    'author_email': 'ale.bxsantos@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
