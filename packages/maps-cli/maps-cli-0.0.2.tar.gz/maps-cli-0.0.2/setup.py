# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maps', 'maps.apis']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'geopy>=2.1.0,<3.0.0',
 'overpy>=0.4,<0.5',
 'requests>=2.25.1,<3.0.0',
 'simplejson>=3.17.2,<4.0.0']

entry_points = \
{'console_scripts': ['maps = maps.commands:maps']}

setup_kwargs = {
    'name': 'maps-cli',
    'version': '0.0.2',
    'description': 'A CLI for maps services.',
    'long_description': '# Maps CLI \n\n[![Main Actions Status](https://github.com/sackh/maps-cli/workflows/main/badge.svg)](https://github.com/sackh/maps-cli/actions)\n[![Documentation Status](https://readthedocs.org/projects/maps-cli/badge/?version=latest)](https://maps-cli.readthedocs.io/en/latest/?badge=latest)\n[![codecov](https://codecov.io/gh/sackh/maps-cli/branch/master/graph/badge.svg?token=98J9ILF6VG)](https://codecov.io/gh/sackh/maps-cli)\n[![PyPI - Python Version](https://img.shields.io/pypi/v/maps-cli.svg?logo=pypi)](https://pypi.org/project/maps-cli/)\n[![Downloads](https://pepy.tech/badge/maps-cli)](https://pepy.tech/project/maps-cli)\n[![PyPI - License](https://img.shields.io/pypi/l/maps-cli)](https://pypi.org/project/maps-cli/)\n[![GitHub contributors](https://img.shields.io/github/contributors/sackh/maps-cli)](https://github.com/sackh/maps-cli/graphs/contributors)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![commits since](https://img.shields.io/github/commits-since/sackh/maps-cli/latest.svg)](https://github.com/sackh/maps-cli/commits/master)\n\nA simple command line tool to access services of various map services providers.\n\n## Usage\n# ![demo](https://github.com/sackh/maps-cli/raw/master/gifs/demo.gif)\n\n## Installation\n```bash\n  pip install maps-cli\n```\n\n## Test Suite\n```bash\n  poetry install\n  pytest -v --durations=10 --cov=maps tests\n```\n\n### Commands\n\n```bash\n  maps -h\n  maps show\n```\n\n## Maps Service Providers\nCurrently, this library is supporting following providers.\n\n- [OSM](https://www.openstreetmap.org/)\n- [HERE](https://www.here.com/)\n- [MapBox](https://www.mapbox.com/)\n- [TomTom](https://www.tomtom.com/)\n\n\n## Services\nCurrently, all providers support forward and reverse geocoding services.\n',
    'author': 'Sachin Kharude',
    'author_email': 'sachinkharude10@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sackh/maps-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
