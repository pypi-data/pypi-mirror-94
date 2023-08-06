# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['colette']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11,<3.0', 'mip>=1.13,<2.0']

entry_points = \
{'console_scripts': ['colette = colette.__main__:main']}

setup_kwargs = {
    'name': 'colette',
    'version': '0.1.2',
    'description': 'Manage rounds of coffee roulette',
    'long_description': '# Colette: Coffee Roulette — pair with a random person for coffee\n\n## Installaiton\n\nRequires Python 3.9 or later installed.\n\nOpen a command line and run:\n\n    pip install colette\n\n## Usage\n\nCreate a file called people.csv with at least columns \'name\', \'organisation\',\n\'email\', and \'active\'.\n\nEach participating (or previously participating) player should be listed in\neach row. The active column should contain \'true\' if a player is going to\nparticipate in new rounds.\n\nRun, from a command line in the directory of your previously created\n\'people.csv\':\n\n    colette new\n\n> Note: you may need to add the path pip installed colette too to your PATH\n> enviroment variable.\n>\n> Alternativly you can run colette as\n>\n>     python -m colette\n\nThis will generate a new `round*.csv`, with pairs chosen to minimize the number\nof people paired together in the same organisation, and those previously\npaired. Players are assigned a role in each round, either "organiser" or\n"(coffee) buyer". The method attempts to choose pairs that allow people to swap\nroles each round.\n\nIf you want to mark certain pairs as desired or undesired, create an\n"overrides.csv" file in the data directory, listing on each row the name of the two\nplayers and an integer "cost" of adding this pair to the round. This will be\nadded to the cost of pairing if the players have previously been pair or are in\nthe same organisation. To prefer a pair, add a negative cost.\n',
    'author': 'David Horsley',
    'author_email': 'david.e.horsley@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dehorsley/colette',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
