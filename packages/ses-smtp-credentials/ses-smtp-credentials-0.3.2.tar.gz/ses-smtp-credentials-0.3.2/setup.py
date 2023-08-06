# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ses_smtp_credentials']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['ses-smtp-credentials = ses_smtp_credentials.cli:run']}

setup_kwargs = {
    'name': 'ses-smtp-credentials',
    'version': '0.3.2',
    'description': '',
    'long_description': None,
    'author': 'Ben Bridts',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6.0,<4.0.0',
}


setup(**setup_kwargs)
