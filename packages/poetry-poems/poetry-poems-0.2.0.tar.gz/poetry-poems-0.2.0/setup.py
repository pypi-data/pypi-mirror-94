# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_poems', 'poetry_poems.picker']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

extras_require = \
{':sys_platform == "win32"': ['windows-curses>=2.1.0,<3.0.0']}

entry_points = \
{'console_scripts': ['poems = poetry_poems.cli:poems']}

setup_kwargs = {
    'name': 'poetry-poems',
    'version': '0.2.0',
    'description': 'Poetry Environments Switcher: CLI Tool to help manage Poetry Enviroments and corresponding Project Directories.',
    'long_description': '#####\nPoems\n#####\n\n**Poetry Environment Switcher**\n\n.. image:: https://travis-ci.org/harper25/poetry-poems.svg?branch=master\n        :target: https://travis-ci.org/harper25/poetry-poems\n        :alt: Travis CI\n.. image:: https://codecov.io/gh/harper25/poetry-poems/branch/master/graph/badge.svg\n        :target: https://codecov.io/gh/harper25/poetry-poems\n        :alt: Codecov\n.. image:: https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue\n        :target: https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue\n        :alt: Python versions\n.. image:: https://img.shields.io/github/issues/harper25/poetry-poems\n        :target: https://img.shields.io/github/issues/harper25/poetry-poems\n        :alt: Issues\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n        :target: https://github.com/psf/black\n        :alt: Code Style\n.. image:: https://img.shields.io/badge/OS-MacOS%20%7C%20Ubuntu%20%7C%20Win10-orange\n        :target: https://img.shields.io/badge/OS-MacOS%20%7C%20Ubuntu%20%7C%20Win10-orange\n        :alt: Supported OS\n\nOverview\n========\n\nPoetry-poems is a tool that speeds up switching between Python Poetry-based projects by:\n\n- navigating to a specific project in the terminal\n- activating Poetry shell at the same time.\n\nPoetry-poems was inspired and is based on amazing project `pipenv-pipes - Pipenv Environment Switcher <https://github.com/gtalarico/pipenv-pipes>`_.\n\nHow does it work?\n=================\n\n.. image:: https://raw.githubusercontent.com/harper25/poetry-poems/master/docs/static/poems-intro.gif\n\n\n**The list of available projects has to be populated before usage!**\n\n\nPopulating poems list\n---------------------\n\n.. image:: https://raw.githubusercontent.com/harper25/poetry-poems/master/docs/static/poems-add.gif\n\n\nDocumentation\n=============\n\nDocumentation is available on `poetry-poems.readthedocs.io <https://poetry-poems.readthedocs.io/en/latest/>`_\n\nLicense\n=======\n\n- `lgpl-3.0 <https://github.com/harper25/poetry-poems/blob/master/LICENSE>`_\n- `license note <https://github.com/harper25/poetry-poems/blob/master/license-poetry-poems>`_\n\nCredits\n=======\n\nProject based on `Pipes <https://github.com/gtalarico/pipenv-pipes>`_, Pipenv Environment Switcher. A modified version of `Pick <https://github.com/wong2/pick/>`_ for curses based interactive selection list in the terminal is also used.\n\nAuthor\n======\n\n`harper25 <https://github.com/harper25>`_\n\n\n.. Section Heading\n.. ===============\n\n.. Subsection Heading\n.. ------------------\n\n.. Sub-subsection Heading\n.. ^^^^^^^^^^^^^^^^^^^^^^\n\n.. Sub-sub-subsection Heading\n.. """"""""""""""""""""""""""\n',
    'author': 'harper25',
    'author_email': 'olesjakubb@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://poetry-poems.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
