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
    'version': '0.2.0',
    'description': 'A command line tool to peek a remote repo locally.',
    'long_description': '## github-peek\n\nA command line tool to peek a remote repo locally. The tool creates 2 files and a directory,\na config file `~/.githubkeep.conf`, a log file `~/.githubkeep.log` and a directory `~/.githubkeep`.\nGithub-peek downloads the tar:gz of the repo, extracts it and saves it to `~/.githubkeep`. There is\na naive caching mechanism, where the tool deletes all repos after 5 times of using the app.\n\n### install github-peek\n\n```bash\npip install github-peek\n```\n\n### usage:\n\ngithub-peek only has only subcommand `peek`, which takes a repo as the argument.\n\n\ncommand usage:\n\n```bash\nghub peek <repo>\n```\n\nexample:\n\n```bash\nghub peek rahulunair/github-peek\n```\n\n### todo\n\n- enable for gitlab\n\n\n',
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
