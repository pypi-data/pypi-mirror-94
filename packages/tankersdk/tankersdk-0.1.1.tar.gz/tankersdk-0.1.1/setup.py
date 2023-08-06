# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tankersdk']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tankersdk',
    'version': '0.1.1',
    'description': 'Python client for Tanker',
    'long_description': ".. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg\n  :target: https://opensource.org/licenses/Apache-2.0\n.. image:: https://img.shields.io/badge/python-v3.7%20v3.8%20v3.9-blue.svg\n  :target: https://gitlab.com/TankerHQ/sdk-python\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n  :target: https://github.com/psf/black\n.. image:: https://img.shields.io/badge/mypy-checked-blue.svg\n   :target: https://mypy-lang.org\n.. image:: https://gitlab.com/TankerHQ/sdk-python/badges/master/pipeline.svg\n   :target: https://gitlab.com/TankerHQ/sdk-python/pipelines\n\nTanker Python SDK\n=================\n\nOverview\n--------\n\nThe `Tanker SDK <https://tanker.io>`_ provides an easy-to-use SDK allowing you to protect your users'\ndata.\n\nThis repository only contains Python3 bindings. The core library can be found in the `TankerHQ/sdk-native GitHub project <https://github.com/TankerHQ/sdk-native>`_.\n\nContributing\n------------\n\nWe are actively working to allow external developers to build and test this project\nfrom source. That being said, we welcome feedback of any kind. Feel free to\nopen issues or pull requests on the `GitLab project <https://gitlab.com/TankerHQ/sdk-python>`_.\n\nDocumentation\n-------------\n\nSee `API documentation <https://docs.tanker.io/latest/api/core/python>`_.\n\nLicense\n-------\n\nThe Tanker Python SDK is licensed under the `Apache License, version 2.0 <http://www.apache.org/licenses/LICENSE-2.0>`_.\n",
    'author': 'Tanker team',
    'author_email': 'tech@tanker.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/TankerHQ/sdk-python/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
