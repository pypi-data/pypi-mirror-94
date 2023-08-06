# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['good_guys',
 'good_guys.activations',
 'good_guys.layers',
 'good_guys.layers.basic',
 'good_guys.layers.complex',
 'good_guys.layers.convs',
 'good_guys.layers.pooling',
 'good_guys.layers.residuals',
 'good_guys.loss',
 'good_guys.misc',
 'good_guys.models',
 'good_guys.models.lstm',
 'good_guys.utils']

package_data = \
{'': ['*'], 'good_guys.models': ['docs/*']}

install_requires = \
['torch>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'eyecu-good-guys',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Oguz Vuruskaner',
    'author_email': 'ovuruska@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
