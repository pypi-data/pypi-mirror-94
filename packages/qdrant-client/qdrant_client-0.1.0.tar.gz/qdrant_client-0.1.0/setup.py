# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qdrant_client',
 'qdrant_openapi_client',
 'qdrant_openapi_client.api',
 'qdrant_openapi_client.apis',
 'qdrant_openapi_client.model',
 'qdrant_openapi_client.models']

package_data = \
{'': ['*'], 'qdrant_openapi_client': ['docs/*']}

install_requires = \
['httpx>=0.16.1,<0.17.0',
 'numpy>=1.20.1,<2.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'tqdm>=4.56.0,<5.0.0']

setup_kwargs = {
    'name': 'qdrant-client',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Andrey Vasnetsov',
    'author_email': 'andrey@vasnetsov.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
