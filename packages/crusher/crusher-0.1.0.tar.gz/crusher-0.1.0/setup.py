# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crusher']

package_data = \
{'': ['*']}

install_requires = \
['rich>=9.10.0,<10.0.0']

entry_points = \
{'console_scripts': ['crusher = crusher:crusher.cli_entrypoint']}

setup_kwargs = {
    'name': 'crusher',
    'version': '0.1.0',
    'description': 'Crush a deeply nested JSON string.',
    'long_description': None,
    'author': 'rednafi',
    'author_email': 'redowan.nafi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
