# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyc']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=0.29.21,<0.30.0']

entry_points = \
{'console_scripts': ['pyc = pyc.cli:compile',
                     'python-pyc = pyc.cli:compile_and_run']}

setup_kwargs = {
    'name': 'pyc',
    'version': '0.1.0',
    'description': 'Compile Python code to binary',
    'long_description': None,
    'author': 'Jukka Aho',
    'author_email': 'ahojukka5@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
