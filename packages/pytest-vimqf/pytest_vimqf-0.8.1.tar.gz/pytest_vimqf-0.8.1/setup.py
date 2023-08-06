# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_vimqf']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=6.2.2,<7.0.0']

entry_points = \
{'pytest11': ['vimqf = pytest_vimqf.main']}

setup_kwargs = {
    'name': 'pytest-vimqf',
    'version': '0.8.1',
    'description': 'A simple pytest plugin that will shrink pytest output when specified, to fit vim quickfix window.',
    'long_description': '[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/carlodepieri/pytest-vimqf/CI?logo=github)](https://github.com/CarloDePieri/pytest-vimqf/actions)\n[![PyPI](https://img.shields.io/pypi/v/pytest-vimqf)](https://pypi.python.org/pypi/pytest-vimqf)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-vimqf)](https://pypi.python.org/pypi/pytest-vimqf)\n[![Build system: poetry](https://img.shields.io/badge/build%20system-poetry-blue)](https://github.com/python-poetry/poetry)\n\nA simple pytest plugin that will shrink pytest output when specified, to fit the\nvim quickfix window.\n\n## The problem\n\nThe vim quickfix window prepends `||` to commands output lines, to differentiate\nfrom its actual fix elements. This behaviour is intended and not configurable.\n\nPytest default terminal reporter calculates the available terminal width and\norganize its layout accordingly, often printing characters to the far right of\nthe screen.\n\nWhen running pytest in vim (for example using [pytest-vim-compiler](https://github.com/CarloDePieri/pytest-vim-compiler)\ninside [vim-dispatch](https://github.com/tpope/vim-dispatch)),\nits output in the quickfix window will show a broken layout (since there\nactually are fewer columns available than pytest calculated).\n\nThis issue is exacerbated if `signcolumn` is set.\n\n<img src="https://user-images.githubusercontent.com/5459291/107146685-03f7cd00-694a-11eb-94b4-1efae06acb4d.png" width="400">\n\n## The solution\n\nPytest-vimqf simply trick pytest\'s terminal reporter in thinking the terminal is\nslightly smaller. This allows it to fit nicely in the vim quickfix window.\n\n<img src="https://user-images.githubusercontent.com/5459291/107146686-04906380-694a-11eb-8610-57a9292f4ce3.png" width="400">\n\n## Installation\n\nInstall using pip:\n\n```console\n# pip install pytest-vimqf\n```\n\n## Usage\n\nThe plugin is disabled by default, allowing pytest to use the whole terminal when\ncalled normally.\n\nFrom inside vim, simply add the flag `--vim-quickfix` to pytest. For example:\n\n```bash\n:Dispatch pytest --vim-quickfix\n```\n',
    'author': 'Carlo De Pieri',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CarloDePieri/pytest_vimqf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
