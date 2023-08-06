# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['onyx_client',
 'onyx_client.configuration',
 'onyx_client.data',
 'onyx_client.device',
 'onyx_client.enum',
 'onyx_client.exception',
 'onyx_client.group',
 'onyx_client.helpers',
 'onyx_client.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.3,<4.0.0', 'brotlipy>=0.7.0,<0.8.0', 'cchardet>=2.1.7,<3.0.0']

setup_kwargs = {
    'name': 'onyx-client',
    'version': '2.3.0',
    'description': "HTTP Client for Hella's ONYX.CENTER API.",
    'long_description': '# Onyx Client\n\n[![](https://img.shields.io/github/license/muhlba91/onyx-client?style=for-the-badge)](LICENSE)\n[![](https://img.shields.io/github/workflow/status/muhlba91/onyx-client/Python%20package?style=for-the-badge)](https://github.com/muhlba91/onyx-client/actions)\n[![](https://img.shields.io/coveralls/github/muhlba91/onyx-client?style=for-the-badge)](https://github.com/muhlba91/onyx-client/)\n[![](https://img.shields.io/pypi/pyversions/onyx-client?style=for-the-badge)](https://pypi.org/project/onyx-client/)\n[![](https://img.shields.io/pypi/v/onyx-client?style=for-the-badge)](https://pypi.org/project/onyx-client/)\n[![](https://img.shields.io/github/release-date/muhlba91/onyx-client?style=for-the-badge)](https://github.com/muhlba91/onyx-client/releases)\n[![](https://img.shields.io/pypi/dm/onyx-client?style=for-the-badge)](https://pypi.org/project/onyx-client/)\n<a href="https://www.buymeacoffee.com/muhlba91" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="28" width="150"></a>\n\nThis repository contains a **Python HTTP client** for [Hella](https://www.hella.info)\'\ns [ONYX.CENTER API](https://github.com/hella-info/onyx_api).\n\n---\n\n## Installation\n\nThe package is published in **(Test)PyPi** and can be installed via:\n\n```bash\npip install onyx-client\n```\n\n## Configuration\n\nThe configuration defines **connection properties** as a `dict` for the application running.\n\n**Attention**: make sure to **read**\nthe [Onyx API Access Control](https://github.com/hella-info/onyx_api#access-control) description to **retrieve the\nfingerprint and access token**!\n\n| Option | Description |\n|--------|-------------|\n| fingerprint | The fingerprint of the ONYX.CENTER. |\n| access_token | The permanent access token. |\n/ client_session / The initialized `aiohttp.ClientSession`. (Default: `None`, create new session.) |\n\n### Access Control Helper\n\nThe method `onyx_client.helpers.exchange_code` takes the **API code** and performs the exchange to a **fingerprint and\naccess token**. Please follow the **aforementioned documentation** to retrieve the code.\n\n## Usage\n\nYou can **instantiate** the client using the `onyx_client.create_client` method like:\n\n```python\nimport aiohttp\nfrom onyx_client import create_client\nfrom onyx_client.helpers import exchange_code\n\n# by providing the fingerprint and access token only\nclient = create_client(fingerprint="fingerprint", access_token="access_token")\n\n# by providing the fingerprint, access token and aiohttp client session\nclient = create_client(fingerprint="fingerprint", access_token="access_token", client_session=aiohttp.ClientSession())\n\n# by providing the configuration object\nclient_session = aiohttp.ClientSession()\n# e.g. by exchanging the code first\nconfig = exchange_code("code", client_session)\nclient = create_client(config=config, client_session=client_session) if client_session is not None else None\n```\n\nAn **example** is shown in the **`examples` directory**.\n\n---\n\n## Development\n\nThe project uses [poetry](https://poetry.eustace.io/) and to install all dependencies and the build environment, run:\n\n```bash\n$ pip install poetry\n$ poetry install\n```\n\n### Testing\n\n1) Install all dependencies as shown above.\n2) Run `pytest` by:\n\n```bash\n$ poetry run pytest\n# or\n$ pytest\n```\n\n### Linting and Code Style\n\nThe project uses [flakehell](https://github.com/life4/flakehell) as a wrapper for flake8,\nand [black](https://github.com/psf/black) for automated code style fixing, also\nusing [pre-commit](https://pre-commit.com/).\n\n1) Install all dependencies as shown above.\n2) (Optional) Install pre-commit hooks:\n\n```bash\n$ poetry run pre-commit install\n```\n\n3) Run black:\n\n```bash\n$ poetry run black .\n```\n\n4) Run flakehell:\n\n```bash\n$ poetry run flakehell lint\n```\n\n### Building\n\nThis package uses [poetry-dynamic-versioning](https://github.com/mtkennerly/poetry-dynamic-versioning) which infers the\nversion number based on the Git tags. Hence, to have a proper versioning for the distribution, use Python\'s build system\nlike:\n\n```bash\n$ pip install build\n$ python -m build\n```\n\nYour distribution will be in the `dist` directory.\n\n### Commit Message\n\nThis project follows [Conventional Commits](https://www.conventionalcommits.org/), and your commit message must also\nadhere to the additional rules outlined in `.conform.yaml`.\n\n---\n\n## Release\n\nTo draft a release, use [standard-version](https://github.com/conventional-changelog/standard-version):\n\n```bash\n$ standard-version\n# alternatively\n$ npx standard-version\n```\n\nFinally, push with tags:\n\n```bash\n$ git push --follow-tags\n```\n\n---\n\n## Contributions\n\nPlease feel free to contribute, be it with Issues or Pull Requests! Please read\nthe [Contribution guidelines](CONTRIBUTING.md)\n\n## Supporting\n\nIf you enjoy the application and want to support my efforts, please feel free to buy me a coffe. :)\n\n<a href="https://www.buymeacoffee.com/muhlba91" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="75" width="300"></a>\n',
    'author': 'Daniel Muehlbachler-Pietrzykowski',
    'author_email': 'daniel.muehlbachler@niftyside.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/muhlba91/onyx-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
