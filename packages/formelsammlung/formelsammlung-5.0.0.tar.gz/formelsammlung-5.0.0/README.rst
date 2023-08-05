==============
formelsammlung
==============

+-------------------+---------------------------------------------------------------------------------------------+
| **General**       | |maintenance_n| |license| |rtd|                                                             |
|                   +---------------------------------------------------------------------------------------------+
|                   | |semver|                                                                                    |
+-------------------+---------------------------------------------------------------------------------------------+
| **PyPI**          | |pypi_release| |pypi_py_versions| |pypi_implementations|                                    |
|                   +---------------------------------------------------------------------------------------------+
|                   | |pypi_status| |pypi_format| |pypi_downloads|                                                |
+-------------------+---------------------------------------------------------------------------------------------+
| **Pipeline**      | |gha_test_code| |codeclimate_cov|                                                           |
|                   +---------------------------------------------------------------------------------------------+
|                   | |gha_code_quality| |codeclimate_maintain|                                                   |
|                   +---------------------------------------------------------------------------------------------+
|                   | |gha_test_docs| |gha_dep_safety|                                                            |
+-------------------+---------------------------------------------------------------------------------------------+
| **Github**        | |gh_release| |gh_commits_since| |gh_last_commit|                                            |
|                   +---------------------------------------------------------------------------------------------+
|                   | |gh_stars| |gh_forks| |gh_contributors| |gh_watchers|                                       |
+-------------------+---------------------------------------------------------------------------------------------+


**Collection of different multipurpose functions.**

This library is a collection of different functions I developed which I use in different
projects so I put them here. New features are added when I need them somewhere.


Functionality
=============

- ``getenv_typed()``: is a wrapper around ``os.getenv`` returning the value of the environment variable in the correct python type.
- ``calculate_string()``: takes an arithmetic expression as a string and calculates it.
- ``SphinxDocServer``: is a flask plugin to serve the repository's docs build as HTML (by sphinx). Needs ``flask`` extra to be also installed to work.
- ``env_exe_runner()``: is a function to call a given ``tool`` from the first venv/tox/nox environment that has it installed in a list of venv/tox/nox environments.
- ``get_venv_path()``: is a function to get the path to the current venv.
- ``get_venv_bin_dir()``: is a function to get the path to the bin/Scripts dir of a given venv.
- ``get_venv_tmp_dir()``: is a function to get the path to the tmp/temp dir of a given venv.
- ``get_venv_site_packages_dir()``: is a function to get the path to the site-packages dir of a given venv.
- ``where_installed()``: is a function to find the installation places in and outside a venv.
- ``session_w_poetry``: decorator to change ``nox`` session class to include ``poetry_install()`` method.


Prerequisites
=============

*Works only with python version >= 3.6*

A new version of ``pip`` that supports PEP-517/PEP-518 is required.
When the setup fails try updating ``pip``.


Disclaimer
==========

No active maintenance is intended for this project.
You may leave an issue if you have a questions, bug report or feature request,
but I cannot promise a quick response time.


License
=======

This project is licensed under the GPL-3.0 or later.


.. ############################### LINKS FOR BADGES ###############################


.. Change badges in docs/source/_badges.rst also


.. General

.. |maintenance_n| image:: https://img.shields.io/badge/Maintenance%20Intended-✖-red.svg?style=flat-square
    :target: http://unmaintained.tech/
    :alt: Maintenance - not intended

.. |maintenance_y| image:: https://img.shields.io/badge/Maintenance%20Intended-✔-green.svg?style=flat-square
    :target: http://unmaintained.tech/
    :alt: Maintenance - intended

.. |license| image:: https://img.shields.io/github/license/Cielquan/formelsammlung.svg?style=flat-square&label=License
    :target: https://github.com/Cielquan/formelsammlung/blob/main/LICENSE
    :alt: License

.. |rtd| image:: https://img.shields.io/readthedocs/formelsammlung/latest.svg?style=flat-square&logo=read-the-docs&logoColor=white&label=Read%20the%20Docs
    :target: https://formelsammlung.readthedocs.io/en/latest/
    :alt: Read the Docs - Build Status (latest)

.. |semver| image:: https://img.shields.io/badge/Semantic%20Versioning-2.0.0-brightgreen.svg?style=flat-square
    :target: https://semver.org/
    :alt: Semantic Versioning - 2.0.0


.. PyPI

.. |pypi_release| image:: https://img.shields.io/pypi/v/formelsammlung.svg?style=flat-square&logo=pypi&logoColor=FBE072
    :target: https://pypi.org/project/formelsammlung/
    :alt: PyPI - Package latest release

.. |pypi_py_versions| image:: https://img.shields.io/pypi/pyversions/formelsammlung.svg?style=flat-square&logo=python&logoColor=FBE072
    :target: https://pypi.org/project/formelsammlung/
    :alt: PyPI - Supported Python Versions

.. |pypi_implementations| image:: https://img.shields.io/pypi/implementation/formelsammlung.svg?style=flat-square&logo=python&logoColor=FBE072
    :target: https://pypi.org/project/formelsammlung/
    :alt: PyPI - Supported Implementations

.. |pypi_status| image:: https://img.shields.io/pypi/status/formelsammlung.svg?style=flat-square&logo=pypi&logoColor=FBE072
    :target: https://pypi.org/project/formelsammlung/
    :alt: PyPI - Stability

.. |pypi_format| image:: https://img.shields.io/pypi/format/formelsammlung.svg?style=flat-square&logo=pypi&logoColor=FBE072
    :target: https://pypi.org/project/formelsammlung/
    :alt: PyPI - Format

.. |pypi_downloads| image:: https://img.shields.io/pypi/dm/formelsammlung.svg?style=flat-square&logo=pypi&logoColor=FBE072
    :target: https://pypi.org/project/formelsammlung/
    :alt: PyPI - Monthly downloads


.. Pipeline

.. |gha_test_code| image:: https://img.shields.io/github/workflow/status/Cielquan/formelsammlung/Test%20code/main?style=flat-square&logo=github&label=Test%20code
    :target: https://github.com/Cielquan/formelsammlung/actions?query=workflow%3A%22Test+code%22
    :alt: GitHub Actions - Test code

.. |codeclimate_cov| image:: https://img.shields.io/codeclimate/coverage/Cielquan/formelsammlung?style=flat-square&logo=code-climate
    :target: https://codeclimate.com/github/Cielquan/formelsammlung
    :alt: Code Climate - Coverage

.. |gha_code_quality| image:: https://img.shields.io/github/workflow/status/Cielquan/formelsammlung/Code%20qualitiy/main?style=flat-square&logo=github&label=Code%20qualitiy
    :target: https://github.com/Cielquan/formelsammlung/actions?query=workflow%3A%22Code+qualitiy%22
    :alt: GitHub Actions - Code qualitiy

.. add pre-commit-ci badge when usable
.. .. |pre-commit-ci| image:: https://results.pre-commit.ci/badge/github/Cielquan/formelsammlung/main.svg
..    :target: https://results.pre-commit.ci/latest/github/Cielquan/formelsammlung/main
..    :alt: pre-commit.ci status

.. |codeclimate_maintain| image:: https://img.shields.io/codeclimate/maintainability/Cielquan/formelsammlung?style=flat-square&logo=code-climate
    :target: https://codeclimate.com/github/Cielquan/formelsammlung
    :alt: Code Climate - Maintainability

.. |gha_test_docs| image:: https://img.shields.io/github/workflow/status/Cielquan/formelsammlung/Test%20documentation/main?style=flat-square&logo=github&label=Test%20documentation
    :target: https://github.com/Cielquan/formelsammlung/actions?query=workflow%3A%22Test+documentation%22
    :alt: GitHub Actions - Test docs

.. |gha_dep_safety| image:: https://img.shields.io/github/workflow/status/Cielquan/formelsammlung/Dependency%20safety/main?style=flat-square&logo=github&label=Dependency%20safety
    :target: https://github.com/Cielquan/formelsammlung/actions?query=workflow%3A%22Dependency+safety%22
    :alt: GitHub Actions - Dependency safety

.. TODO:#i# readd dependabot badge when https://github.com/dependabot/dependabot-core/issues/1912 is fixed

.. |dependabot| image:: https://api.dependabot.com/badges/status?host=github&repo=Cielquan/formelsammlung
    :target: https://dependabot.com
    :alt: Dependabot status


.. GitHub

.. |gh_release| image:: https://img.shields.io/github/v/release/Cielquan/formelsammlung.svg?style=flat-square&logo=github
    :target: https://github.com/Cielquan/formelsammlung/releases/latest
    :alt: Github - Latest Release

.. |gh_commits_since| image:: https://img.shields.io/github/commits-since/Cielquan/formelsammlung/latest.svg?style=flat-square&logo=github
    :target: https://github.com/Cielquan/formelsammlung/commits/main
    :alt: GitHub - Commits since latest release

.. |gh_last_commit| image:: https://img.shields.io/github/last-commit/Cielquan/formelsammlung.svg?style=flat-square&logo=github
    :target: https://github.com/Cielquan/formelsammlung/commits/main
    :alt: GitHub - Last Commit

.. |gh_stars| image:: https://img.shields.io/github/stars/Cielquan/formelsammlung.svg?style=flat-square&logo=github
    :target: https://github.com/Cielquan/formelsammlung/stargazers
    :alt: Github - Stars

.. |gh_forks| image:: https://img.shields.io/github/forks/Cielquan/formelsammlung.svg?style=flat-square&logo=github
    :target: https://github.com/Cielquan/formelsammlung/network/members
    :alt: Github - Forks

.. |gh_contributors| image:: https://img.shields.io/github/contributors/Cielquan/formelsammlung.svg?style=flat-square&logo=github
    :target: https://github.com/Cielquan/formelsammlung/graphs/contributors
    :alt: Github - Contributors

.. |gh_watchers| image:: https://img.shields.io/github/watchers/Cielquan/formelsammlung.svg?style=flat-square&logo=github
    :target: https://github.com/Cielquan/formelsammlung/watchers/
    :alt: Github - Watchers
