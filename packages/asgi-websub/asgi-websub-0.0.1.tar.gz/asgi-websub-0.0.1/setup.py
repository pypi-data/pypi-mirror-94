# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asgi_websub']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.16.1,<0.17.0']

setup_kwargs = {
    'name': 'asgi-websub',
    'version': '0.0.1',
    'description': '',
    'long_description': '<h1 align="center">\n    <strong>asgi-websub</strong>\n</h1>\n<p align="center">\n    <a href="https://github.com/Kludex/asgi-websub" target="_blank">\n        <img src="https://img.shields.io/github/last-commit/Kludex/asgi-websub" alt="Latest Commit">\n    </a>\n        <img src="https://img.shields.io/github/workflow/status/Kludex/asgi-websub/Test">\n        <img src="https://img.shields.io/codecov/c/github/Kludex/asgi-websub">\n    <br />\n    <a href="https://pypi.org/project/asgi-websub" target="_blank">\n        <img src="https://img.shields.io/pypi/v/asgi-websub" alt="Package version">\n    </a>\n    <img src="https://img.shields.io/pypi/pyversions/asgi-websub">\n    <img src="https://img.shields.io/github/license/Kludex/asgi-websub">\n</p>\n\n\n## Installation\n\n``` bash\npip install asgi-websub\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Marcelo Trylesinski',
    'author_email': 'marcelotryle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kludex/asgi-websub',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
