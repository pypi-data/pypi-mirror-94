# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['github_peek']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.6.0,<0.7.0',
 'aiohttp[speedups]>=3.7.3,<4.0.0',
 'loguru>=0.5.3,<0.6.0',
 'sh>=1.14.1,<2.0.0',
 'shellingham>=1.4.0,<2.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['ghub = github_peek.cli:app']}

setup_kwargs = {
    'name': 'github-peek',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'unrahul',
    'author_email': 'rahulunair@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
