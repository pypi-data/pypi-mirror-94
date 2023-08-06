# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['schema_enforcer', 'schema_enforcer.instances', 'schema_enforcer.schemas']

package_data = \
{'': ['*']}

install_requires = \
['ansible>=2.8.0,<3.0.0',
 'click>=7.1.2,<8.0.0',
 'jinja2>=2.11.2,<3.0.0',
 'jsonref>=0.2,<0.3',
 'jsonschema>=3.2.0,<4.0.0',
 'pydantic>=1.6.1,<2.0.0',
 'rich>=9.5.1,<10.0.0',
 'ruamel.yaml>=0.16.10,<0.17.0',
 'termcolor>=1.1.0,<2.0.0',
 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['schema-enforcer = schema_enforcer.cli:main']}

setup_kwargs = {
    'name': 'schema-enforcer',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'Network to Code, LLC',
    'author_email': 'info@networktocode.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
