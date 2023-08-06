# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kurby']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=5,<6',
 'Js2Py>=0,<1',
 'PyInquirer>=1.0.3,<2.0.0',
 'arrow>=0.17,<0.18',
 'fuzzywuzzy>=0,<1',
 'httpx>=0,<1',
 'pycryptodomex>=3.9,<4.0',
 'pydantic>=1.7,<2.0',
 'tenacity>=6,<7',
 'tqdm>=4,<5',
 'typer-cli>=0,<1',
 'typer>=0,<1']

entry_points = \
{'console_scripts': ['kurby = kurby.cli:start']}

setup_kwargs = {
    'name': 'kurby',
    'version': '0.3.3',
    'description': 'A modern CLI to download animes automatically from Twist.moe',
    'long_description': '# Kurby\n[![PyPI - Python Version](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue)](https://docs.python.org/3/whatsnew/3.7.html) [![Downloads](https://pepy.tech/badge/kurby)](https://pepy.tech/badge/kurby) [![PyPI version](https://badge.fury.io/py/kurby.svg)](https://badge.fury.io/py/kurby.svg)\n\n<div align="center">\n    <img src="docs/kurby.png" alt="Kirby ball in Kirby: Canvas Curse" height=400, width=400/>\n</div>\n<br>\n\n\nKurby is a nice and simple CLI that use [Twist](https://twist.moe) website, and their huge collection to download animes for free and **automatically**\n\nAnimes from Twist are generally in High Definition with English subtitles. Please consider [donating](https://twist.moe) for their amazing work :)\n\n## Overview\nThe CLI is built with [Typer](https://github.com/tiangolo/typer) and it is composed of 3 commands\n\n- `animes`: Search animes to find what is available and extract the slug to be used in the other commands\n\n![animes](docs/examples/animes.gif)\n  \n> `--search` option allows you to make a fuzzy search\n  \n- `details`: Show details of an anime if needed\n\n![details](docs/examples/details.gif)\n  \n> You can see the number of episodes available and when the first and last episode were uploaded\n  \n- `download`: Choose and download which episodes of the anime you want !\n\n![download](docs/examples/download.gif)\n\n> Because sometimes bad things can happen, Kurby will automatically retry for you\n\nYou can also download without having a slug initially. In this case, Kurby will propose you a selection\n\n![download-selection](docs/examples/download-selection.gif)\n\n#### And that\'s it !\n\nYou can also use `kurby --help` to get more information on the different commands\n\n## Installation\n```bash\npip install kurby\nkurby --help\n```\n\n## Installation on Windows\n- Right click on the `install.bat` and run it as an **Administrator**, this will install [Chocolatey](https://chocolatey.org/) who will manage the python installation\n- Once the installation is finished, and you\'re asked to press a key, open a new terminal (`Win + R` > `cmd` )\n- You can now start using Kurby with `kurby --help`\n\n## Installation on Android without root needed\n- Install [Termux](https://play.google.com/store/apps/details?id=com.termux) on your Android phone\n- In Termux, run this command to allow access to storage: `termux-setup-storage`, and tap allow\n- Next, run the follow command `pkg install git python`\n- Then `pip3 install kurby`\n- You\'re done ! You can download animes on your phone like so `kurby download --d ~/storage/shared`\n\n##### *Thanks to [6b86b3ac03c167320d93](https://www.reddit.com/user/6b86b3ac03c167320d93/) for this tutorial*\n\n## Installation from sources\n### Create your virtual environment (optional)\n````bash\nmkvirtualenv kurby\nworkon kurby\n````\n### Install poetry\n```bash\ncurl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -\n```\n### Install dependencies using poetry\n```bash\npoetry install --no-dev\nkurby-cli --help # or python kurby-cli --help\n```\n\n## Getting the latest episode automatically\nAn interesting use case is to get the latest episode of an anime as soon as it is available.\n\nThis is possible on Linux using `crontab` (or another equivalent on others OS) and _a little tweak of chemistry_.\nHere is an example of a few instructions that can help you do this.\n```shell\nnow=$(date -u "+%Y-%m-%dT%H:%M:%S")\ndate=$(cat kurby.date || echo $now) # Get the date of previous download\npython kurby download {{YOUR_ANIME}} --dfrom=${DATE} # Download any episodes that has been uploaded since the last time\necho $now > kurby.date # Store the current date as the new date\n```\n\n## Next steps\nKurby is already functional as it is but here are the next things I would like to add :\n- Adding the support of asynchronous download\n- Refactor the retrying strategy to add more customisable options and allow errors during a download without interruption\n- Refactor the crawling process to potentially avoid being detected as a bot\n\n### Disclaimer\nDownloading copyright videos may be illegal in your country.\n\nThis tool is for educational purposes only.\n\nThe developers or this application do not store or distribute any files whatsoever.\n',
    'author': 'Alain BERRIER',
    'author_email': 'alain.berrier@outlook.com',
    'maintainer': 'Alain BERRIER',
    'maintainer_email': 'alain.berrier@outlook.com',
    'url': 'https://github.com/aberrier/kurby',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
