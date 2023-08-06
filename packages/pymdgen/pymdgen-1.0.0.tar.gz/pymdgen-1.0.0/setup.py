# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pymdgen']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pymdgen = pymdgen.cli:main'],
 'markdown.extensions': ['pymdgen = pymdgen.md:Extension']}

setup_kwargs = {
    'name': 'pymdgen',
    'version': '1.0.0',
    'description': 'python code markdown documentation generator',
    'long_description': None,
    'author': '20C',
    'author_email': 'code@20c.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
