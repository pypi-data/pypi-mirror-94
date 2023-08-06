# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_s3_csv_2_sfdc']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.1.6,<4.0.0',
 'boto3>=1.17.3,<2.0.0',
 'simple-salesforce>=1.10.1,<2.0.0']

setup_kwargs = {
    'name': 'django-s3-csv-2-sfdc',
    'version': '0.1.0',
    'description': 'A set of helper functions for CSV to Salesforce procedures, with reporting in AWS S3, based in a Django project',
    'long_description': '# Overview\n\nTODO\n',
    'author': 'Alex Drozd',
    'author_email': 'drozdster@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/brno32/django-s3-csv-2-sfdc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
