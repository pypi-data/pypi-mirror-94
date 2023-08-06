# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mariner',
 'mariner.commands',
 'mariner.proxies',
 'mariner.trackers',
 'mariner.utils']

package_data = \
{'': ['*'], 'mariner': ['config/*']}

install_requires = \
['aiodns>=2.0,<3.0',
 'aiofiles>=0.6,<0.7',
 'aiohttp>=3.7,<4.0',
 'beautifulsoup4>=4.9,<5.0',
 'cachalot>=1.5,<2.0',
 'cliff>=3.6,<4.0',
 'colorama>=0.4,<0.5',
 'lxml>=4.6,<5.0',
 'maya>=0.6,<0.7',
 'ruamel.yaml>=0.16,<0.17',
 'tokenize-rt>=3.2,<4.0']

entry_points = \
{'console_scripts': ['mariner = mariner.main:main'],
 'mariner.cli': ['config = mariner.commands.config:Config',
                 'details = mariner.commands.details:Details',
                 'download = mariner.commands.download:Download',
                 'magnet = mariner.commands.magnet:Magnet',
                 'open = mariner.commands.open:Open',
                 'search = mariner.commands.search:Search']}

setup_kwargs = {
    'name': 'mariner',
    'version': '1.5.1',
    'description': 'Navigate torrents in CLI',
    'long_description': "# Mariner [![PyPI version](https://badge.fury.io/py/mariner.svg)](https://badge.fury.io/py/mariner) [![Pipeline status](https://gitlab.com/radek-sprta/mariner/badges/master/pipeline.svg)](https://gitlab.com/radek-sprta/mariner/commits/master) [![Coverage report](https://gitlab.com/radek-sprta/mariner/badges/master/coverage.svg)](https://gitlab.com/radek-sprta/mariner/commits/master) [![Downloads](http://pepy.tech/badge/mariner)](http://pepy.tech/project/mariner) [![Black](https://img.shields.io/badge/code%20style-black-000000)](https://github.com/psf/black)\n\nNavigate torrents in CLI with Mariner. It offers a simple interface for streamlined experience. No more annoying ads and pop-up windows.\n\nIt is currently under heavy development, so expect breaking changes. Currently only works in Linux, but any contributions in this regard are welcome.\n\n## Features\n\n- Runs on Linux and Windows.\n- Automatically get a working proxy for trackers that have them.\n- Download torrent files and copy magnet links to clipboard.\n- Open torrents in your default torrent application.\n- Show torrent details.\n- Asynchronous I/O for better responsiveness.\n- Supports the following trackers:\n  - Archive.org\n  - Distrowatch\n  - Etree\n  - LimeTorrents\n  - Linuxtracker\n  - Nyaa\n  - NyaaPantsu\n  - TokyoTosho\n\n![Mariner demonstration](docs/assets/mariner.svg)\n\n## Installation\n\nMariner requires Python 3.6 or newer to run.\n\n### Python package\n\nYou can easily install Mariner using pip. This is the preferred method:\n\n`pip3 install mariner`\n\n### Manual\n\nAlternatively, to get the latest development version, you can clone this repository and then manually install it:\n\n```bash\ngit clone git@gitlab.com:radek-sprta/mariner.git\ncd mariner\npoetry build\npip install dist/*.whl\n```\n\n## Usage\n\nMariner supports both interactive and non-interactive modes. To see the list of commands, simply type:\n\n`mariner help`\n\nIn order to start Mariner in interactive mode, run it without any arguments:\n\n`mariner`\n\nThen search for Ubuntu torrents:\n\n`(mariner) search Ubuntu -t linuxtracker`\n\nand download the first result on the list:\n\n`(mariner) download 0`\n\nAlternatively, copy the magnet link to clipboard:\n\n`(mariner) magnet 0`\n\nOr open it in your torrent application:\n\n`(mariner) open 0`\n\nAnd quit the program:\n\n`(mariner) quit`\n\nFor more information, check the [documentation].\n\n## Contributing\n\nFor information on how to contribute to the project, please check the [Contributor's Guide][contributing]\n\n## Disclaimer\n\nI do not encourage anyone to act in conflict with their local laws and I do not endorse any illegal activity. Some content in the search results provided be Mariner might be illegal in your country and it is up to you to check your local laws before using it. Neither I, nor Mariner can be held liable for any action taken against you as the result of using it.\n\n## Contact\n\n[mail@radeksprta.eu](mailto:mail@radeksprta.eu)\n\n[incoming+radek-sprta/mariner@gitlab.com](incoming+radek-sprta/mariner@gitlab.com)\n\n## Acknowledgements\n\nMariner uses many excellent open-source libraries. But I would particularly like to mention the following, as without them, Mariner might not have been possible:\n\n- [Aiohttp](https://github.com/aio-libs/aiohttp)\n- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)\n- [Cliff](https://github.com/openstack/cliff/tree/master/cliff)\n- [TinyDB](https://github.com/msiemens/tinydb)\n\n## License\n\nGNU General Public License v3.0\n\n[contributing]: https://gitlab.com/radek-sprta/mariner/blob/master/CONTRIBUTING.md\n[documentation]: https://radek-sprta.gitlab.io/mariner\n",
    'author': 'Radek Sprta',
    'author_email': 'mail@radeksprta.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://radek-sprta.gitlab.io/mariner/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
