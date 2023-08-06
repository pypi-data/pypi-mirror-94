# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlalchemy_dataflex']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy', 'pyodbc', 'python-dateutil']

entry_points = \
{'sqlalchemy.dialects': ['paradox = '
                         'sqlalchemy_paradox.pyodbc:ParadoxDialect_pyodbc',
                         'paradox.pyodbc = '
                         'sqlalchemy_paradox.pyodbc:ParadoxDialect_pyodbc']}

setup_kwargs = {
    'name': 'sqlalchemy-dataflex',
    'version': '0.1.5',
    'description': 'A SQLAlchemy dialect for DataFlex flat-file databases.',
    'long_description': '# SQLAlchemy-DataFlex\n\nA SQLAlchemy dialect for the\n[FlexODBC driver](https://www.flextools.com/flexodbc)\n\n## Objectives\n\nThis dialect is mainly intended to offer an easy way to access the\nDataFlex flat-file databases of older or EOL\'d application-specific\nsoftwares. It is designed for use with the ODBC driver available from\n[FlexQuarters](http://flexquarters.com/)\n\n## Pre-requisites\n\n- The [FlexODBC driver](https://www.flextools.com/flexodbc) from\n  [FlexQuarters](http://flexquarters.com/). ~~The library was written and\n  tested against v3, but it *should* work with v4 as well.~~ The library\n  has been re-written from the ground up and tested to work against the\n  latest available version of FlexODBC (4.0.27.2).\n\n- 32-bit Python. Neither of the available FlexODBC driver versions\n  support or come in a 64-bit version.\n\n## Co-requisites\n\nThis dialect requires SQLAlchemy and pyodbc. They are both specified as\nrequirements so `pip` will install them if they are not already in\nplace. To install separately, just:\n\n> `pip install -U SQLAlchemy pyodbc`\n\n## Installation\n\nPyPI-published version:\n\n> `pip install -U sqlalchemy-dataflex`\n\nAbsolute bleeding-edge (probably buggy):\n\n> `pip install -U git+https://github.com/the-wondersmith/sqlalchemy-dataflex`\n\n## Getting Started\n\nCreate an `ODBC DSN (Data Source Name)` that points to the directory\ncontaining your DataFlex `FILELIST.cfg` and `.DAT` table.\n\n> Tip: For best results, be sure to select the 4-digit date option and\n> the `.` option for decimals\n\nThen, in your Python app, you can connect to the database via:\n\n```python\nfrom sqlalchemy_dataflex import *\nfrom sqlalchemy import create_engine\nfrom sqlalchemy.orm import sessionmaker\n\n\ndb = create_engine("dataflex+pyodbc://@your_dsn", echo=False)\nsuper_session = sessionmaker(bind=db)\nsuper_session.configure(autoflush=True, autocommit=True, expire_on_commit=True)\nsession = super_session()\n```\n\n> NOTE: It is *highly* recommended that you use the datatype classes from the package itself\n>       in place of the ones that are usually imported from SQLAlchemy. The testing suite doesn\'t\n>       use the SQLAlchemy type classes, so any issues that might arise from their use with the dialect\n>       won\'t be caught by the tests.\n\n## The SQLAlchemy Project\n\nSQLAlchemy-DataFlex is based on SQLAlchemy-access, which is part of the\n[SQLAlchemy Project] (https://www.sqlalchemy.org) and *tries* to adhere\nto the same standards and conventions as the core project.\n\nAt the time of this writing, it\'s unlikely that SQLAlchemy-DataFlex\nactually *does* comply with the aforementioned standards and\nconventions. That will be rectified (if and when) in a future release.\n\n## Development / Bug reporting / Pull requests\n\nSQLAlchemy maintains a\n[Community Guide](https://www.sqlalchemy.org/develop.html) detailing\nguidelines on coding and participating in that project.\n\nWhile I\'m aware that this project could desperately use the\nparticipation of anyone else who actually knows what they\'re doing,\nDataFlex and the FlexODBC driver are so esoteric and obscure (at the\ntime of this writing) that I don\'t reasonably expect anyone to actually\nwant to. If I am mistaken in that belief, *please God* submit a pull\nrequest.\n\nThis library technically *works*, but it isn\'t feature-complete so to\nspeak. The FlexODBC driver only supports a very limited subset of SQL\ncommands and queries, and doesn\'t always respond to pyodbc\'s\n`get_info()` inquiries the way that pyodbc is expecting. You can see\nthe complete list of the way it responds to all of the available pyodbc\n`get_info()` inquiries [here](./flexodbc_capabilities.json). If you are\ninterested in which features are currently lacking or absent in the dialect,\nsee the notes and comments littered throughout the testing suite [here](./tests/test_suite.py).\n\n## License\n\nThis library is derived almost in its entirety from the\nSQLAlchemy-Access library written by\n[Gord Thompson](https://github.com/gordthompson). As such, and given\nthat SQLAlchemy-access is distributed under the\n[MIT license](https://opensource.org/licenses/MIT), this library is\nsubject to the same licensure and grant of rights as its parent works\n[SQLAlchemy](https://www.sqlalchemy.org/) and\n[SQLAlchemy-Access](https://github.com/sqlalchemy/sqlalchemy-access).\n',
    'author': 'Pawn Payment Solutions',
    'author_email': 'support@pawn-pay.com',
    'maintainer': 'Mark S.',
    'maintainer_email': 'mark@pawn-pay.com',
    'url': 'https://pypi.org/project/sqlalchemy-dataflex',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
