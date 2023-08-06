# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_lock_check']

package_data = \
{'': ['*']}

install_requires = \
['cleo', 'poetry>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'poetry-lock-check',
    'version': '0.1.0',
    'description': 'Checks the lock on a poetry file',
    'long_description': None,
    'author': 'Brian Graham',
    'author_email': 'brian@statagroup.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
