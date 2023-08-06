# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kedro_local_notify']

package_data = \
{'': ['*'], 'kedro_local_notify': ['static/*']}

install_requires = \
['kedro>=0.17.0,<0.18.0', 'pync>=2.0.3,<3.0.0']

entry_points = \
{'kedro.hooks': ['kedro_local_notify = kedro_local_notify.hook:hooks']}

setup_kwargs = {
    'name': 'kedro-local-notify',
    'version': '0.1.0',
    'description': 'A kedro plugin that interacts with your local notifications',
    'long_description': None,
    'author': 'Zain Patel',
    'author_email': 'zain.patel06@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)
