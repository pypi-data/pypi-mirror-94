# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polyomino']

package_data = \
{'': ['*']}

install_requires = \
['exact-cover==0.4.3', 'numpy>=1.20,<2.0']

entry_points = \
{'console_scripts': ['doctest = run_tests:run_doctests',
                     'test = run_tests:run_tests']}

setup_kwargs = {
    'name': 'polyomino',
    'version': '0.4.1',
    'description': 'Solve polyomino tiling problems.',
    'long_description': None,
    'author': 'Jack Grahl',
    'author_email': 'jack.grahl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
