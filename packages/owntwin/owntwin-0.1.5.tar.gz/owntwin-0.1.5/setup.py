# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['owntwin',
 'owntwin.builder',
 'owntwin.builtin_datasources',
 'owntwin.builtin_modules.base',
 'owntwin.sample_modules.bousai',
 'owntwin.sample_modules.jpsearch',
 'owntwin.viewer']

package_data = \
{'': ['*'],
 'owntwin.viewer': ['owntwin/asset-manifest.json',
                    'owntwin/asset-manifest.json',
                    'owntwin/index.html',
                    'owntwin/index.html',
                    'owntwin/static/css/*',
                    'owntwin/static/js/*']}

install_requires = \
['InquirerPy>=0.1.0,<0.2.0',
 'Pillow>=8.0.1,<9.0.0',
 'colorama>=0.4.4,<0.5.0',
 'geopandas>=0.8.1,<0.9.0',
 'geopy>=2.0.0,<3.0.0',
 'halo>=0.0.31,<0.0.32',
 'importlib-resources>=5.1.0,<6.0.0',
 'loguru>=0.5.3,<0.6.0',
 'mercantile>=1.1.6,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'scour>=0.38.1,<0.39.0',
 'svgwrite>=1.4,<2.0',
 'typer>=0.3.2,<0.4.0',
 'xdg>=5.0.1,<6.0.0']

entry_points = \
{'console_scripts': ['owntwin = owntwin.cli:app']}

setup_kwargs = {
    'name': 'owntwin',
    'version': '0.1.5',
    'description': 'User-driven digital twin framework.',
    'long_description': '# OwnTwin CLI\n\n[![PyPI](https://img.shields.io/pypi/v/owntwin.svg)](https://pypi.python.org/pypi/owntwin/)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/owntwin.svg)](https://pypistats.org/packages/owntwin)\n\nOwnTwin CLI is a toolchain for [OwnTwin](https://github.com/owntwin/owntwin), a user-driven digital twin framework.\n\n## Installation\n\n```\npip install owntwin\n```\n\n_Note for Windows users:_ [Fiona](https://github.com/Toblerity/Fiona#installation) is required to be preinstalled.\n\n## Usage\n\nSee the [documentation](https://beta.owntwin.com/docs/getting-started) for details.\n\n```\nowntwin init\nowntwin add-terrain\nowntwin add [module names...]\nowntwin export\nowntwin view\n```\n',
    'author': 'Kentaro Ozeki',
    'author_email': 'kentaro.ozeki+dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/owntwin/owntwin-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
