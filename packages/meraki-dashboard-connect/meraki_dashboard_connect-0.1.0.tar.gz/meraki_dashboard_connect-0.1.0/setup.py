# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['meraki_dashboard_connect']

package_data = \
{'': ['*']}

install_requires = \
['meraki-env>=0.1.1,<0.2.0', 'meraki>=1.4.3,<2.0.0']

setup_kwargs = {
    'name': 'meraki-dashboard-connect',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Thomas Christory',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
