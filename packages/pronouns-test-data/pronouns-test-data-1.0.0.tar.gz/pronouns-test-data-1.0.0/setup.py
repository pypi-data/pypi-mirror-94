# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pronouns_test_data']

package_data = \
{'': ['*'], 'pronouns_test_data': ['data/*']}

install_requires = \
['inflection>=0.5.1,<0.6.0',
 'pydantic>=1.7.3,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'typer>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'pronouns-test-data',
    'version': '1.0.0',
    'description': 'A library to aid in vending test data for UW-IT IAM pronouns test cases.',
    'long_description': None,
    'author': 'Tom Thorogood',
    'author_email': 'tom@tomthorogood.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
