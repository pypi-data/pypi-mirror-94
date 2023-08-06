# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sl_git_hooks', 'sl_git_hooks.hooks']

package_data = \
{'': ['*'], 'sl_git_hooks': ['configs/*', 'templates/*']}

install_requires = \
['pygit2>=1.5.0,<2.0.0']

entry_points = \
{'console_scripts': ['sl-git-hooks = sl_git_hooks:main']}

setup_kwargs = {
    'name': 'sl-git-hooks',
    'version': '0.1.1102',
    'description': '',
    'long_description': None,
    'author': 'Alexander Memer',
    'author_email': 'mkoaleksedos@gmail.com',
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
