# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyopendart',
 'pyopendart.clients',
 'pyopendart.clients.dataframe',
 'pyopendart.clients.dict',
 'pyopendart.clients.namedtuple']

package_data = \
{'': ['*']}

install_requires = \
['furl>=2.1.0,<3.0.0',
 'pandas>=1.2.1,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.25.1,<3.0.0',
 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'pyopendart',
    'version': '0.2.0a1',
    'description': '인간 친화적인 전자공시시스템 DART 파이썬 API',
    'long_description': None,
    'author': 'Seonghyeon Kim',
    'author_email': 'self@seonghyeon.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NovemberOscar/pyOPENDART',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
