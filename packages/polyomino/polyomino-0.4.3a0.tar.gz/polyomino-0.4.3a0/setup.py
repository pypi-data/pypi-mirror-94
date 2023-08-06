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
    'version': '0.4.3a0',
    'description': 'Solve polyomino tiling problems.',
    'long_description': "# POLYOMINO - a Python package for polyomino tiling problems\n\nThis is a package for manipulating polyominos and in particular, solving tiling problems. It uses the 'exact-cover' python package as the main engine for solving cover problems.\n\nTo solve a tiling problem, you need to create a 'board', the set of squares to be covered, and a 'tileset', the collection of polyominos which can be used. There are examples of the syntax to do this in examples/fluid.md The example file examples/gardner.md uses the package to solve a number of problems from the chapter on polyominos from Martin Gardner's book 'Mathematical Puzzles and Diversions'.\n\n## Design\nBoth polyominos and boards are represented internally as lists of integer tuples (x, y). There are constants defined for all polyominos up to pentominos in polyomino.constant\n",
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
