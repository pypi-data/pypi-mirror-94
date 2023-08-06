# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mdns_beacon', 'mdns_beacon.cli']

package_data = \
{'': ['*']}

install_requires = \
['click-option-group>=0.5.2,<0.6.0',
 'click>=7.1.2,<8.0.0',
 'python-slugify>=4.0.1,<5.0.0',
 'rich>=9.10.0,<10.0.0',
 'typing-extensions>=3.7.4,<4.0.0',
 'zeroconf>=0.28.8,<0.29.0']

entry_points = \
{'console_scripts': ['mdns-beacon = mdns_beacon.cli.main:main']}

setup_kwargs = {
    'name': 'mdns-beacon',
    'version': '0.3.0',
    'description': 'Multicast DNS (mDNS) Beacon to announce multiple CNAME aliases across your local network.',
    'long_description': '\n# mDNS Beacon\n\n\n[![PyPI - Version](https://img.shields.io/pypi/v/mdns-beacon.svg)](https://pypi.python.org/pypi/mdns-beacon)\n[![PyPI - License](https://img.shields.io/pypi/l/mdns-beacon.svg)](https://pypi.python.org/pypi/mdns-beacon)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mdns-beacon.svg)](https://pypi.python.org/pypi/mdns-beacon)\n[![Tests](https://github.com/fedejaure/mdns-beacon/workflows/tests/badge.svg)](https://github.com/fedejaure/mdns-beacon/actions?workflow=tests)\n[![Codecov](https://codecov.io/gh/fedejaure/mdns-beacon/branch/main/graph/badge.svg)](https://codecov.io/gh/fedejaure/mdns-beacon)\n[![Read the Docs](https://readthedocs.org/projects/mdns-beacon/badge/)](https://mdns-beacon.readthedocs.io/)\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n\n\nMulticast DNS (mDNS) Beacon to announce multiple CNAME aliases across your local network. Under development. Use by your own risk❗\n\n\n* GitHub repo: <https://github.com/fedejaure/mdns-beacon.git>\n* Documentation: <https://mdns-beacon.readthedocs.io>\n* Free software: MIT\n\n\n## Features\n\n* ✅ Announce multiple aliases on the local network.\n* ✅ Listening utility to discover services during development.\n* ❌ Run as Unix daemon.\n* ❌ Configuration file.\n* ❌ Windows support.\n\n## Quickstart\n\nInstall `mdns-beacon` from the [Python Package Index][pypi]:\n\n```\n$ pip install mdns-beacon\n```\n\n#### Usage\n\n```\n$ mdns-beacon --help\nUsage: mdns-beacon [OPTIONS] COMMAND [ARGS]...\n\n  Simple multicast DNS (mDNS) command line interface utility.\n\nOptions:\n  --version  Show the version and exit.\n  --help     Show this message and exit.\n\nCommands:\n  blink   Announce aliases on the local network.\n  listen  Listen for services on the local network.\n```\n\nAnnounce an example service:\n\n```\n$ mdns-beacon blink example --alias sub1.example --address 127.0.0.1 --type http --protocol tcp\n⠋ Announcing services (Press CTRL+C to quit) ...\n```\n\nListen to a specific service type:\n\n```\n$ mdns-beacon listen --service _http._tcp.local.\n                                                                                                            \n                                       🚨📡 mDNS Beacon Listener 📡🚨                                       \n┏━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━┓\n┃ # ┃ Type              ┃ Name                           ┃ Address IPv4 ┃ Port ┃ Server              ┃ TTL ┃\n┡━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━┩\n│ 0 │ _http._tcp.local. │ example._http._tcp.local.      │ 127.0.0.1    │ 80   │ example.local.      │ 120 │\n│ 1 │ _http._tcp.local. │ sub1.example._http._tcp.local. │ 127.0.0.1    │ 80   │ sub1.example.local. │ 120 │\n└───┴───────────────────┴────────────────────────────────┴──────────────┴──────┴─────────────────────┴─────┘\n                                                                                                            \n⠧ Listen for services (Press CTRL+C to quit) ...\n```\n\n## Credits\n\nThis package was created with [Cookiecutter][cookiecutter] and the [fedejaure/cookiecutter-modern-pypackage][cookiecutter-modern-pypackage] project template.\n\n[cookiecutter]: https://github.com/cookiecutter/cookiecutter\n[cookiecutter-modern-pypackage]: https://github.com/fedejaure/cookiecutter-modern-pypackage\n[pypi]: https://pypi.org/\n',
    'author': 'Federico Jaureguialzo',
    'author_email': 'fedejaure@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fedejaure/mdns-beacon',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<3.10',
}


setup(**setup_kwargs)
