# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['formelsammlung']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.6,<4.0'],
 'coverage': ['coverage[toml]>=5.3.1,<6.0.0',
              'coverage-conditional-plugin>=0.3.1,<0.4.0'],
 'dev_nox': ['nox>=2020.12.31,<2021.0.0', 'tomlkit>=0.7.0,<1.0.0'],
 'diff-cover': ['diff-cover>=4,<5'],
 'docs': ['flask>=1.1.2,<2.0.0',
          'nox>=2020.12.31,<2021.0.0',
          'sphinx>=3.1,<4.0',
          'm2r2>=0.2.7,<0.3.0',
          'sphinx-rtd-theme>=0.5.1,<0.6.0',
          'sphinx-autodoc-typehints>=1.11,<2.0',
          'sphinxcontrib-apidoc>=0.3,<0.4',
          'sphinxcontrib-spelling>=7.1,<8.0'],
 'flask': ['flask>=1.1.2,<2.0.0'],
 'nox': ['nox>=2020.12.31,<2021.0.0'],
 'poetry': ['poetry>=1.1.4,<2.0.0'],
 'pre-commit': ['sphinx>=3.1,<4.0',
                'pre-commit>=2.9,<3.0',
                'mypy==0.790',
                'pylint>=2.6,<3.0',
                'pyenchant>=3.2,<4.0',
                'flakehell==0.8.0',
                'flake8>=3.8,<4.0',
                'pep8-naming>=0.11,<0.12',
                'flake8-2020>=1.6,<2.0',
                'flake8-aaa>=0.11,<0.12',
                'flake8-annotations>=2.4,<3.0',
                'flake8-bandit>=2.1.2,<3.0.0',
                'bandit>=1.7,<2.0',
                'flake8-broken-line>=0.3,<0.4',
                'flake8-bugbear>=20.11,<21.0',
                'flake8-cognitive-complexity>=0.1,<0.2',
                'flake8-comprehensions>=3.3,<4.0',
                'flake8-docstrings>=1.5,<2.0',
                'flake8-eradicate>=1,<2',
                'flake8-logging-format>=0.6,<0.7',
                'flake8-mutable>=1.2,<2.0',
                'flake8-no-u-prefixed-strings>=0.2,<0.3',
                'flake8-pytest-style>=1.3,<2.0',
                'flake8-rst-docstrings>=0.0.14,<0.0.15',
                'flake8-simplify>=0.12,<0.13',
                'flake8-sql>=0.4.1,<0.5.0',
                'flake8-string-format>=0.3,<0.4',
                'flake8-typing-imports>=1.10.1,<2.0.0',
                'flake8-use-fstring>=1.1,<2.0',
                'flake8-variables-names>=0.0.3,<0.0.4'],
 'pre-commit:python_version >= "3.8"': ['flake8-walrus>=1.1,<2.0'],
 'safety': ['safety>=1.9,<2.0'],
 'sphinx-autobuild': ['sphinx-autobuild==2020.9.1'],
 'testing': ['flask>=1.1.2,<2.0.0',
             'nox>=2020.12.31,<2021.0.0',
             'pytest>=6,<7',
             'pytest-xdist>=2.2,<3.0',
             'psutil>=5.8.0,<6.0.0',
             'pytest-cov>=2.10.1,<3.0.0',
             'coverage[toml]>=5.3.1,<6.0.0',
             'coverage-conditional-plugin>=0.3.1,<0.4.0',
             'pytest-sugar>=0.9.4,<0.10.0',
             'pytest-randomly>=3.5,<4.0',
             'pytest-mock>=3.5.1,<4.0.0',
             'mock>=4.0.3,<5.0.0',
             'pytest-flask>=1.0,<2.0'],
 'tomlkit': ['tomlkit>=0.7.0,<1.0.0'],
 'tox': ['tox>=3.21,<4.0'],
 'twine': ['twine>=3.3,<4.0']}

entry_points = \
{'console_scripts': ['env_exe_runner = '
                     'formelsammlung.env_exe_runner:cli_caller']}

setup_kwargs = {
    'name': 'formelsammlung',
    'version': '5.0.0',
    'description': 'Collection of different functions',
    'long_description': "==============\nformelsammlung\n==============\n\n+-------------------+---------------------------------------------------------------------------------------------+\n| **General**       | |maintenance_n| |license| |rtd|                                                             |\n|                   +---------------------------------------------------------------------------------------------+\n|                   | |semver|                                                                                    |\n+-------------------+---------------------------------------------------------------------------------------------+\n| **PyPI**          | |pypi_release| |pypi_py_versions| |pypi_implementations|                                    |\n|                   +---------------------------------------------------------------------------------------------+\n|                   | |pypi_status| |pypi_format| |pypi_downloads|                                                |\n+-------------------+---------------------------------------------------------------------------------------------+\n| **Pipeline**      | |gha_test_code| |codeclimate_cov|                                                           |\n|                   +---------------------------------------------------------------------------------------------+\n|                   | |gha_code_quality| |codeclimate_maintain|                                                   |\n|                   +---------------------------------------------------------------------------------------------+\n|                   | |gha_test_docs| |gha_dep_safety|                                                            |\n+-------------------+---------------------------------------------------------------------------------------------+\n| **Github**        | |gh_release| |gh_commits_since| |gh_last_commit|                                            |\n|                   +---------------------------------------------------------------------------------------------+\n|                   | |gh_stars| |gh_forks| |gh_contributors| |gh_watchers|                                       |\n+-------------------+---------------------------------------------------------------------------------------------+\n\n\n**Collection of different multipurpose functions.**\n\nThis library is a collection of different functions I developed which I use in different\nprojects so I put them here. New features are added when I need them somewhere.\n\n\nFunctionality\n=============\n\n- ``getenv_typed()``: is a wrapper around ``os.getenv`` returning the value of the environment variable in the correct python type.\n- ``calculate_string()``: takes an arithmetic expression as a string and calculates it.\n- ``SphinxDocServer``: is a flask plugin to serve the repository's docs build as HTML (by sphinx). Needs ``flask`` extra to be also installed to work.\n- ``env_exe_runner()``: is a function to call a given ``tool`` from the first venv/tox/nox environment that has it installed in a list of venv/tox/nox environments.\n- ``get_venv_path()``: is a function to get the path to the current venv.\n- ``get_venv_bin_dir()``: is a function to get the path to the bin/Scripts dir of a given venv.\n- ``get_venv_tmp_dir()``: is a function to get the path to the tmp/temp dir of a given venv.\n- ``get_venv_site_packages_dir()``: is a function to get the path to the site-packages dir of a given venv.\n- ``where_installed()``: is a function to find the installation places in and outside a venv.\n- ``session_w_poetry``: decorator to change ``nox`` session class to include ``poetry_install()`` method.\n\n\nPrerequisites\n=============\n\n*Works only with python version >= 3.6*\n\nA new version of ``pip`` that supports PEP-517/PEP-518 is required.\nWhen the setup fails try updating ``pip``.\n\n\nDisclaimer\n==========\n\nNo active maintenance is intended for this project.\nYou may leave an issue if you have a questions, bug report or feature request,\nbut I cannot promise a quick response time.\n\n\nLicense\n=======\n\nThis project is licensed under the GPL-3.0 or later.\n\n\n.. ############################### LINKS FOR BADGES ###############################\n\n\n.. Change badges in docs/source/_badges.rst also\n\n\n.. General\n\n.. |maintenance_n| image:: https://img.shields.io/badge/Maintenance%20Intended-✖-red.svg?style=flat-square\n    :target: http://unmaintained.tech/\n    :alt: Maintenance - not intended\n\n.. |maintenance_y| image:: https://img.shields.io/badge/Maintenance%20Intended-✔-green.svg?style=flat-square\n    :target: http://unmaintained.tech/\n    :alt: Maintenance - intended\n\n.. |license| image:: https://img.shields.io/github/license/Cielquan/formelsammlung.svg?style=flat-square&label=License\n    :target: https://github.com/Cielquan/formelsammlung/blob/main/LICENSE\n    :alt: License\n\n.. |rtd| image:: https://img.shields.io/readthedocs/formelsammlung/latest.svg?style=flat-square&logo=read-the-docs&logoColor=white&label=Read%20the%20Docs\n    :target: https://formelsammlung.readthedocs.io/en/latest/\n    :alt: Read the Docs - Build Status (latest)\n\n.. |semver| image:: https://img.shields.io/badge/Semantic%20Versioning-2.0.0-brightgreen.svg?style=flat-square\n    :target: https://semver.org/\n    :alt: Semantic Versioning - 2.0.0\n\n\n.. PyPI\n\n.. |pypi_release| image:: https://img.shields.io/pypi/v/formelsammlung.svg?style=flat-square&logo=pypi&logoColor=FBE072\n    :target: https://pypi.org/project/formelsammlung/\n    :alt: PyPI - Package latest release\n\n.. |pypi_py_versions| image:: https://img.shields.io/pypi/pyversions/formelsammlung.svg?style=flat-square&logo=python&logoColor=FBE072\n    :target: https://pypi.org/project/formelsammlung/\n    :alt: PyPI - Supported Python Versions\n\n.. |pypi_implementations| image:: https://img.shields.io/pypi/implementation/formelsammlung.svg?style=flat-square&logo=python&logoColor=FBE072\n    :target: https://pypi.org/project/formelsammlung/\n    :alt: PyPI - Supported Implementations\n\n.. |pypi_status| image:: https://img.shields.io/pypi/status/formelsammlung.svg?style=flat-square&logo=pypi&logoColor=FBE072\n    :target: https://pypi.org/project/formelsammlung/\n    :alt: PyPI - Stability\n\n.. |pypi_format| image:: https://img.shields.io/pypi/format/formelsammlung.svg?style=flat-square&logo=pypi&logoColor=FBE072\n    :target: https://pypi.org/project/formelsammlung/\n    :alt: PyPI - Format\n\n.. |pypi_downloads| image:: https://img.shields.io/pypi/dm/formelsammlung.svg?style=flat-square&logo=pypi&logoColor=FBE072\n    :target: https://pypi.org/project/formelsammlung/\n    :alt: PyPI - Monthly downloads\n\n\n.. Pipeline\n\n.. |gha_test_code| image:: https://img.shields.io/github/workflow/status/Cielquan/formelsammlung/Test%20code/main?style=flat-square&logo=github&label=Test%20code\n    :target: https://github.com/Cielquan/formelsammlung/actions?query=workflow%3A%22Test+code%22\n    :alt: GitHub Actions - Test code\n\n.. |codeclimate_cov| image:: https://img.shields.io/codeclimate/coverage/Cielquan/formelsammlung?style=flat-square&logo=code-climate\n    :target: https://codeclimate.com/github/Cielquan/formelsammlung\n    :alt: Code Climate - Coverage\n\n.. |gha_code_quality| image:: https://img.shields.io/github/workflow/status/Cielquan/formelsammlung/Code%20qualitiy/main?style=flat-square&logo=github&label=Code%20qualitiy\n    :target: https://github.com/Cielquan/formelsammlung/actions?query=workflow%3A%22Code+qualitiy%22\n    :alt: GitHub Actions - Code qualitiy\n\n.. add pre-commit-ci badge when usable\n.. .. |pre-commit-ci| image:: https://results.pre-commit.ci/badge/github/Cielquan/formelsammlung/main.svg\n..    :target: https://results.pre-commit.ci/latest/github/Cielquan/formelsammlung/main\n..    :alt: pre-commit.ci status\n\n.. |codeclimate_maintain| image:: https://img.shields.io/codeclimate/maintainability/Cielquan/formelsammlung?style=flat-square&logo=code-climate\n    :target: https://codeclimate.com/github/Cielquan/formelsammlung\n    :alt: Code Climate - Maintainability\n\n.. |gha_test_docs| image:: https://img.shields.io/github/workflow/status/Cielquan/formelsammlung/Test%20documentation/main?style=flat-square&logo=github&label=Test%20documentation\n    :target: https://github.com/Cielquan/formelsammlung/actions?query=workflow%3A%22Test+documentation%22\n    :alt: GitHub Actions - Test docs\n\n.. |gha_dep_safety| image:: https://img.shields.io/github/workflow/status/Cielquan/formelsammlung/Dependency%20safety/main?style=flat-square&logo=github&label=Dependency%20safety\n    :target: https://github.com/Cielquan/formelsammlung/actions?query=workflow%3A%22Dependency+safety%22\n    :alt: GitHub Actions - Dependency safety\n\n.. TODO:#i# readd dependabot badge when https://github.com/dependabot/dependabot-core/issues/1912 is fixed\n\n.. |dependabot| image:: https://api.dependabot.com/badges/status?host=github&repo=Cielquan/formelsammlung\n    :target: https://dependabot.com\n    :alt: Dependabot status\n\n\n.. GitHub\n\n.. |gh_release| image:: https://img.shields.io/github/v/release/Cielquan/formelsammlung.svg?style=flat-square&logo=github\n    :target: https://github.com/Cielquan/formelsammlung/releases/latest\n    :alt: Github - Latest Release\n\n.. |gh_commits_since| image:: https://img.shields.io/github/commits-since/Cielquan/formelsammlung/latest.svg?style=flat-square&logo=github\n    :target: https://github.com/Cielquan/formelsammlung/commits/main\n    :alt: GitHub - Commits since latest release\n\n.. |gh_last_commit| image:: https://img.shields.io/github/last-commit/Cielquan/formelsammlung.svg?style=flat-square&logo=github\n    :target: https://github.com/Cielquan/formelsammlung/commits/main\n    :alt: GitHub - Last Commit\n\n.. |gh_stars| image:: https://img.shields.io/github/stars/Cielquan/formelsammlung.svg?style=flat-square&logo=github\n    :target: https://github.com/Cielquan/formelsammlung/stargazers\n    :alt: Github - Stars\n\n.. |gh_forks| image:: https://img.shields.io/github/forks/Cielquan/formelsammlung.svg?style=flat-square&logo=github\n    :target: https://github.com/Cielquan/formelsammlung/network/members\n    :alt: Github - Forks\n\n.. |gh_contributors| image:: https://img.shields.io/github/contributors/Cielquan/formelsammlung.svg?style=flat-square&logo=github\n    :target: https://github.com/Cielquan/formelsammlung/graphs/contributors\n    :alt: Github - Contributors\n\n.. |gh_watchers| image:: https://img.shields.io/github/watchers/Cielquan/formelsammlung.svg?style=flat-square&logo=github\n    :target: https://github.com/Cielquan/formelsammlung/watchers/\n    :alt: Github - Watchers\n",
    'author': 'Christian Riedel',
    'author_email': 'cielquan@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
