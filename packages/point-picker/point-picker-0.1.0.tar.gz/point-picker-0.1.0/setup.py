# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['point_picker']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.15.2,<6.0.0',
 'click>=7.1.2,<8.0.0',
 'imageio>=2.9.0,<3.0.0',
 'pandas>=1.2.2,<2.0.0',
 'scikit-image>=0.18.1,<0.19.0',
 'vispy>=0.6.6,<0.7.0']

entry_points = \
{'console_scripts': ['point-picker = point_picker.cli:main']}

setup_kwargs = {
    'name': 'point-picker',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Matthew Hartley',
    'author_email': 'mhartley@cantab.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
