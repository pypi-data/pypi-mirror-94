# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['edfi_lms_extractor_lib',
 'edfi_lms_extractor_lib.api',
 'edfi_lms_extractor_lib.csv_generation',
 'edfi_lms_extractor_lib.helpers']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.3.19,<2.0.0', 'pandas>=1.1.1,<2.0.0', 'xxhash>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'edfi-lms-extractor-lib',
    'version': '1.0.0a1',
    'description': 'Shared functions library for Ed-Fi LMS Extractor projects',
    'long_description': None,
    'author': 'Ed-Fi Alliance, LLC, and contributors',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://techdocs.ed-fi.org/display/EDFITOOLS/LMS+Toolkit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
