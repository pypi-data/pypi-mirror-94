# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gapoic', 'gapoic.abs', 'gapoic.http']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['cover = scripts:cover',
                     'lint = scripts:lint',
                     'test = scripts:test',
                     'test_gapo = scripts:test_gapo',
                     'test_misc = scripts:test_misc']}

setup_kwargs = {
    'name': 'gapoic',
    'version': '0.5.1',
    'description': 'stuff utils',
    'long_description': None,
    'author': 'vutr',
    'author_email': 'me@vutr.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
