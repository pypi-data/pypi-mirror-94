# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rock_paper_scissors_bot']

package_data = \
{'': ['*']}

install_requires = \
['python-telegram-bot>=13.2,<14.0']

entry_points = \
{'console_scripts': ['rock_paper_scissors_bot = rock_paper_scissors_bot:main']}

setup_kwargs = {
    'name': 'rock-paper-scissors-bot',
    'version': '0.1.0',
    'description': '',
    'long_description': '# RockPaperScissorsBot\nRock Paper Scissors telegram bot\n',
    'author': 'Maxim Semenov',
    'author_email': '0rang3max@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
