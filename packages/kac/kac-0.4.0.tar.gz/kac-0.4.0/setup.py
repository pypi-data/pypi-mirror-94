# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kac', 'kac.changelog']

package_data = \
{'': ['*'], 'kac': ['templates/*']}

install_requires = \
['click>=7.1.1,<8.0.0',
 'gitpython>=3.1.7,<4.0.0',
 'jinja2>=2.11.1,<3.0.0',
 'pyperclip>=1.8.0,<2.0.0',
 'questionary>=1.5.1,<2.0.0',
 'semver>=2.10.2,<3.0.0']

entry_points = \
{'console_scripts': ['kac = kac.kac:cli']}

setup_kwargs = {
    'name': 'kac',
    'version': '0.4.0',
    'description': 'A command line tool for CHANGELOG files that follow the Keep-a-Changelog standard.',
    'long_description': '![kac](https://atw.me/img/kac.svg)\n\n<hr>\n\nA command line tool for CHANGELOG files that follow the [Keep A Changelog][1] standard.\n\n![Tests](https://github.com/atwalsh/kac/workflows/Tests/badge.svg)\n\n### Usage\n\nRun `kac` in the same directory as your Changelog. By default, `kac` looks for a file called `CHANGELOG.md`\n(case-insensitive).\n\n```\nUsage: kac [OPTIONS] COMMAND [ARGS]...\n\n  A CLI tool for CHANGELOG files that follow the Keep-a-Changelog standard.\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  bump  Bump the latest version of a CHANGELOG file.\n  copy  Copy the latest release\'s changelog text.\n  init  Create an empty CHANGELOG file.\n  \n```\n\n## Limitations\n\n- Must be run in the same directory as your CHANGELOG file\n- Only works for semver\n- `kac bump` can "format" (ex: remove extra empty lines) CHANGELOG files, this could be unfavorable for users\n\n[1]: https://keepachangelog.com/en/1.0.0/',
    'author': 'Adam Walsh',
    'author_email': 'adam@atw.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/atwalsh/kac',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
