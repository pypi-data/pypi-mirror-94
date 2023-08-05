# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['authcaptureproxy', 'authcaptureproxy.examples']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.3,<4.0.0',
 'bs4>=0.0.1,<0.0.2',
 'multidict>=5.1.0,<6.0.0',
 'typer>=0.3,<1.0',
 'yarl>=1.6.3,<2.0.0']

entry_points = \
{'console_scripts': ['auth_capture_proxy = authcaptureproxy.cli:cli']}

setup_kwargs = {
    'name': 'authcaptureproxy',
    'version': '0.1.0',
    'description': 'A Python project to create a proxy to capture authentication information from a webpage. This is useful to capture oauth login details without access a third-party oauth.',
    'long_description': '# Auth_capture_proxy\n\n[![Version status](https://img.shields.io/pypi/status/auth_capture_proxy)](https://pypi.org/project/auth_capture_proxy)\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![Python version compatibility](https://img.shields.io/pypi/pyversions/auth_capture_proxy)](https://pypi.org/project/auth_capture_proxy)\n[![Version on Docker Hub](https://img.shields.io/docker/v/alandtse/auth_capture_proxy?color=green&label=Docker%20Hub)](https://hub.docker.com/repository/docker/alandtse/auth_capture_proxy)\n[![Version on Github](https://img.shields.io/github/v/release/alandtse/auth_capture_proxy?include_prereleases&label=GitHub)](https://github.com/alandtse/auth_capture_proxy/releases)\n[![Version on PyPi](https://img.shields.io/pypi/v/authcaptureproxy)](https://pypi.org/project/authcaptureproxy)\n[![Version on Conda-Forge](https://img.shields.io/conda/vn/conda-forge/auth_capture_proxy?label=Conda-Forge)](https://anaconda.org/conda-forge/auth_capture_proxy)  \n[![Documentation status](https://readthedocs.org/projects/auth_capture_proxy/badge)](https://auth_capture_proxy.readthedocs.io/en/stable)\n[![Build (Github Actions)](https://img.shields.io/github/workflow/status/alandtse/auth_capture_proxy/Build%20&%20test?label=Build%20&%20test)](https://github.com/alandtse/auth_capture_proxy/actions)\n[![Build (Travis)](https://img.shields.io/travis/alandtse/auth_capture_proxy?label=Travis)](https://travis-ci.com/alandtse/auth_capture_proxy)\n[![Build (Azure)](https://img.shields.io/azure-devops/build/alandtse/<<key>>/<<defid>>?label=Azure)](https://dev.azure.com/alandtse/auth_capture_proxy/_build?definitionId=1&_a=summary)\n[![Build (Scrutinizer)](https://scrutinizer-ci.com/g/alandtse/auth_capture_proxy/badges/build.png?b=main)](https://scrutinizer-ci.com/g/alandtse/auth_capture_proxy/build-status/main)  \n[![Test coverage (coveralls)](https://coveralls.io/repos/github/alandtse/auth_capture_proxy/badge.svg?branch=main&service=github)](https://coveralls.io/github/alandtse/auth_capture_proxy?branch=main)\n[![Test coverage (codecov)](https://codecov.io/github/alandtse/auth_capture_proxy/coverage.svg)](https://codecov.io/gh/alandtse/auth_capture_proxy)\n[![Test coverage (Scrutinizer)](https://scrutinizer-ci.com/g/alandtse/auth_capture_proxy/badges/coverage.png?b=main)](https://scrutinizer-ci.com/g/alandtse/auth_capture_proxy/?branch=main)\n[![Maintainability (Code Climate)](https://api.codeclimate.com/v1/badges/<<apikey>>/maintainability)](https://codeclimate.com/github/alandtse/auth_capture_proxy/maintainability)\n[![Code Quality (Scrutinizer)](https://scrutinizer-ci.com/g/alandtse/auth_capture_proxy/badges/quality-score.png?b=main)](https://scrutinizer-ci.com/g/alandtse/auth_capture_proxy/?branch=main)\n\nA python project.\n\nAnd it’s further described in this paragraph.\n[See the docs 📚](https://auth_capture_proxy.readthedocs.io/en/stable/) for more info.\n\nLicensed under the terms of the [Apache License 2.0](https://spdx.org/licenses/Apache-2.0.html).\n[New issues](https://github.com/alandtse/auth_capture_proxy/issues) and pull requests are welcome.\nPlease refer to the [contributing guide](https://github.com/alandtse/auth_capture_proxy/blob/main/CONTRIBUTING.md)\nand [security policy](https://github.com/alandtse/auth_capture_proxy/blob/main/SECURITY.md).  \nGenerated with [Tyrannosaurus](https://github.com/dmyersturnbull/tyrannosaurus).\n',
    'author': 'Alan D. Tse',
    'author_email': None,
    'maintainer': 'Alan D. Tse',
    'maintainer_email': None,
    'url': 'https://github.com/alandtse/auth_capture_proxy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
