# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clin_msi', 'clin_msi.count_normalization', 'clin_msi.msi_model_scripts']

package_data = \
{'': ['*']}

install_requires = \
['xgboost==1.3.3']

setup_kwargs = {
    'name': 'clin-msi',
    'version': '0.0.1',
    'description': 'The workflow package for MSI detection in Python',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
