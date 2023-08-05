# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pctap_annek']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'ldap3>=2.9,<3.0']

entry_points = \
{'console_scripts': ['pctap = pctap_annek.cli:main']}

setup_kwargs = {
    'name': 'pctap-annek',
    'version': '0.2.0',
    'description': 'Tap LDAP for PCs',
    'long_description': None,
    'author': 'Michael MacKenna',
    'author_email': 'mmackenna@unitedfiregroup.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
