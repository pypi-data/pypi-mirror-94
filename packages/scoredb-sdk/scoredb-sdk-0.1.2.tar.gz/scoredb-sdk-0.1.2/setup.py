# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scoredb', 'scoredb.client', 'scoredb.models']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'scoredb-sdk',
    'version': '0.1.2',
    'description': 'Python SDK of the ScoreDB v3 API Server.',
    'long_description': '# ScoreDB SDK for Python\n\nPython SDK of the ScoreDB v3 API Server.\n',
    'author': 'JingBh',
    'author_email': 'jingbohao@yeah.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ScoreDB/sdk-python.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
