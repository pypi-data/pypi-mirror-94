# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hypermodern_python_course']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'desert>=2020.11.18,<2021.0.0',
 'marshmallow>=3.10.0,<4.0.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['hypermodern-python-course = '
                     'hypermodern_python_course.console:main']}

setup_kwargs = {
    'name': 'hypermodern-python-course',
    'version': '0.1.0',
    'description': 'The hypermodern Python course',
    'long_description': '# Hypermodern-python-course\n![Tests](https://github.com/Vodolazskyi/hypermodern-python-course/workflows/Tests/badge.svg)\n[![Codecov](https://codecov.io/gh/Vodolazskyi/hypermodern-python-course/branch/master/graph/badge.svg)](https://codecov.io/gh/Vodolazskyi/hypermodern-python-course)\n',
    'author': 'Oleksandr Vodolazskyi',
    'author_email': 'oleksandr.vodolazskyi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Vodolazskyi/hypermodern-python-course',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
