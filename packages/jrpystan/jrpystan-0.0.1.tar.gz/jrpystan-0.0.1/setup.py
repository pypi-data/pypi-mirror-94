# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jrpystan']

package_data = \
{'': ['*'], 'jrpystan': ['data/*']}

install_requires = \
['matplotlib>=3.0', 'numpy>=1.19', 'pandas>=1', 'pystan>=2.19,<3.0']

setup_kwargs = {
    'name': 'jrpystan',
    'version': '0.0.1',
    'description': 'Jumping Rivers: Introduction to Bayesian inference using PyStan',
    'long_description': None,
    'author': 'Jumping Rivers',
    'author_email': 'info@jumpingrivers.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
