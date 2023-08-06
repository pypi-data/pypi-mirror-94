# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiosqlembic', 'aiosqlembic.models']

package_data = \
{'': ['*'],
 'aiosqlembic': ['sql/aiosqlembic/aiosqlite/*',
                 'sql/aiosqlembic/asyncpg/*',
                 'sql/metadata/*',
                 'templates/*']}

install_requires = \
['aiosql>=3.2.0,<4.0.0',
 'asyncpg>0.21.0',
 'colorama>=0.4.4,<0.5.0',
 'jinja2>=2.11.2,<3.0.0',
 'pydantic>=1.6.1,<2.0.0']

entry_points = \
{'console_scripts': ['aiosqlembic = aiosqlembic.main:main']}

setup_kwargs = {
    'name': 'aiosqlembic',
    'version': '0.3.10',
    'description': 'Migrations powered by aiosql',
    'long_description': '<img src="/docs/source/Cigogne_Belon_1555.jpg"  height="200">\n\n**Aiosqlembic, migrations welcome !**\n\n\nReadme\n======\n\n![pipeline](https://gitlab.com/euri10/aiosqlembic/badges/master/pipeline.svg)\n![coverage](https://gitlab.com/euri10/aiosqlembic/badges/master/coverage.svg)\n![documentation](https://readthedocs.org/projects/aiosqlembic/badge/?version=latest)\n\n\nAiosqlembic aims at running database migrations powered by the awesome [aiosql](https://github.com/nackjicholson/aiosql)\n\nIt\'s inspired by goose for those coming from go\n\nIt is in development and likely to break\n\nDocumentation\n-------------\n\nIt\'s [here](https://aiosqlembic.readthedocs.io/en/latest/index.html)\n\nUsage\n-----\n\nRun `aiosqlembic --help`\n',
    'author': 'euri10',
    'author_email': 'benoit.barthelet@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/euri10/aiosqlembic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
