# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beth', 'beth.models', 'beth.players']

package_data = \
{'': ['*']}

install_requires = \
['chess>=1.4.0,<2.0.0',
 'comet-ml>=3.3.3,<4.0.0',
 'ipykernel>=5.4.3,<6.0.0',
 'ipython>=7.20.0,<8.0.0',
 'ipywidgets>=7.6.3,<8.0.0',
 'jupyter>=1.0.0,<2.0.0',
 'matplotlib>=3.3.4,<4.0.0',
 'numpy>=1.20.1,<2.0.0',
 'pandas>=1.2.2,<2.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'torch>=1.7.1,<2.0.0',
 'tqdm>=4.56.2,<5.0.0']

setup_kwargs = {
    'name': 'beth',
    'version': '0.1.0',
    'description': 'Open source chess AI engine',
    'long_description': None,
    'author': 'Theo Alves Da Costa',
    'author_email': 'theo.alves.da.costa@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.8,<4.0.0',
}


setup(**setup_kwargs)
