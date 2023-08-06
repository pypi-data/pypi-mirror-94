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
    'version': '0.1.1',
    'description': 'A kedro plugin that interacts with your local notifications',
    'long_description': "![kedro-local-notify-logo](static/logo.png)\n\n# kedro-local-notify\n\n![github-action](https://github.com/mzjp2/kedro-local-notify/workflows/Lint%20and%20test/badge.svg)\n![code-style](https://img.shields.io/badge/code%20style-black-000000.svg)\n![license](https://img.shields.io/badge/License-MIT-green.svg)\n\n## How do I get started?\n\n```console\n$ pip install --upgrade kedro-local-notify\n```\n\n### Then what?\n\nNothing! Kedro will automagically pick up the hook and ping you a notification after the pipeline finished running succesfully or fails.\n\n## What is `kedro-local-notify`?\n\nEver kicked off a long-running pipeline and come back to check in an hour later, only to find that it failed 2 minutes in?\n\nOr come back to see your pipeline finished running an hour ago and you have nothing to justify your reddit browsing anymore?\n\n`kedro-local-notify` will ping you a notification indicating that your pipeline ran sucessfully or failed.\n\n![kedro-local-notify-demo](static/demo.png)\n\n## Won't this spam me?\n\nBy default, notifications will only trigger if the pipeline has been running for more than 1 minute. You can change this thresholf for notifying you by setting the `KEDRO_LOCAL_NOTIFY_THRESHOLD` environment variable to be the number of seconds of pipeline run time before a notification is trigerred. The default is:\n\n```console\n$ export KEDRO_LOCAL_NOTIFY=60\n```\n\nnote that this environment variable needs to be set in the same shell that you're trigerring the Kedro pipeline run in.\n\n## Caveats\n\nYou probably shouldn't add this to your requirements. It's a silly little tool meant to be used for some quality of life improvements on your local machine.\n\nThis is currently limited to Mac OS X 10.10 or higher. Windows support is in the works!\n",
    'author': 'Zain Patel',
    'author_email': 'zain.patel06@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mzjp2/kedro-local-notify',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)
