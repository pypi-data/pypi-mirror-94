# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mozci',
 'mozci.data',
 'mozci.data.sources',
 'mozci.data.sources.activedata',
 'mozci.data.sources.hgmo',
 'mozci.data.sources.taskcluster',
 'mozci.data.sources.treeherder',
 'mozci.util']

package_data = \
{'': ['*'], 'mozci.data.sources.activedata': ['queries/*']}

install_requires = \
['appdirs>=1,<2',
 'cachy>=0,<1',
 'flake8>=3,<4',
 'loguru>=0,<1',
 'pyyaml>=5,<6',
 'requests>=2,<3',
 'taskcluster>=38',
 'taskcluster_urls>=13,<14',
 'tomlkit>=0,<1',
 'voluptuous>=0,<1']

extras_require = \
{'adr': ['adr>=0,<1']}

setup_kwargs = {
    'name': 'mozci',
    'version': '1.12.6',
    'description': '',
    'long_description': None,
    'author': 'Andrew Halberstadt',
    'author_email': 'ahal@mozilla.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
