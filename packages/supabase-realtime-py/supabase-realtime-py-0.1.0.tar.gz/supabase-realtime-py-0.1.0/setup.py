# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['supabase_realtime_py']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses>=0.6,<0.7', 'websockets>=8.1,<9.0']

setup_kwargs = {
    'name': 'supabase-realtime-py',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'None',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
