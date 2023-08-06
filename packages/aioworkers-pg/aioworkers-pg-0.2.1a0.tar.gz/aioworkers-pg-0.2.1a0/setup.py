# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioworkers_pg']

package_data = \
{'': ['*']}

install_requires = \
['aioworkers>=0.15', 'asyncpgsa']

setup_kwargs = {
    'name': 'aioworkers-pg',
    'version': '0.2.1a0',
    'description': 'Module for working with PostgreSQL via asyncpg',
    'long_description': "aioworkers-pg\n================\n\n.. image:: https://travis-ci.org/aioworkers/aioworkers-pg.svg?branch=master\n  :target: https://travis-ci.org/aioworkers/aioworkers-pg\n\n.. image:: https://img.shields.io/pypi/pyversions/aioworkers-pg.svg\n  :target: https://pypi.python.org/pypi/aioworkers-pg\n  :alt: Python versions\n\n.. image:: https://img.shields.io/pypi/v/aioworkers-pg.svg\n  :target: https://pypi.python.org/pypi/aioworkers-pg\n\n\nAsyncpg plugin for `aioworkers`.\n\n\nUsage\n-----\n\nAdd this to aioworkers config.yaml:\n\n.. code-block:: yaml\n\n    db:\n        cls: aioworkers_pg.base.Connector\n        dsn: postgresql:///test\n\nYou can get access to postgres anywhere via context:\n\n.. code-block:: python\n\n    await context.db.execute('CREATE TABLE users(id serial PRIMARY KEY, name text)')\n    await context.db.execute(users.insert().values(name='Bob'))\n\n\nStorage\n~~~~~~~\n\n.. code-block:: yaml\n\n    storage:\n        cls: aioworkers_pg.storage.RoStorage\n        dsn: postgresql:///test\n        table: mytable  # optional instead custom sql\n        key: id\n        get: SELECT * FROM mytable WHERE id = :id  # optional custom sql\n        format: dict  # or row\n\n\nDevelopment\n-----------\n\nInstall dev requirements:\n\n\n.. code-block:: shell\n\n    pipenv install --dev --skip-lock\n\n\nRun tests:\n\n.. code-block:: shell\n\n    pytest",
    'author': 'Alexander Bogushov',
    'author_email': 'abogushov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aioworkers/aioworkers-pg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
