# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['n_const']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=4.1,<5.0', 'numpy>=1.19,<2.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.8,<0.9']}

setup_kwargs = {
    'name': 'n-const',
    'version': '0.1.0',
    'description': 'Parse and declare NANTEN2/NASCO specific constants/parameters.',
    'long_description': '# N-CONST\n\n[![PyPI](https://img.shields.io/pypi/v/n-const.svg?label=PyPI&style=flat-square)](https://pypi.org/pypi/n-const/)\n[![Python](https://img.shields.io/pypi/pyversions/n-const.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/pypi/n-const/)\n[![Test](https://img.shields.io/github/workflow/status/nanten2/NASCO-tools/Test?logo=github&label=Test&style=flat-square)](https://github.com/nanten2/NASCO-tools/actions)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](LICENSE)\n\nNANTEN2/NASCO Constants and ObservatioN Specification Translator.\n\n## Features\n\nThis library provides:\n\n- constants of the telescope system as useful python objects\n- parsers for parameter files unique to NANTEN2/NASCO system\n\n## Installation\n\n```shell\npip install n-const\n```\n\n## Usage\n\nBe careful of the package name! Use underscore instead of hyphen.\n\n### Constants\n\nSolid constants such as location of the telescope are declared in `constants` module. To use the constants:\n\n```python\n>>> import n_const.constants as n2const\n>>> n2const.LOC_NANTEN2\nEarthLocation(2230866.39573496, -5440247.68222275, -2475554.41874542) m\n>>> n2const.XFFTS.ch_num\n32768\n```\n\n`Constants` objects support both keys and dot notations to access its components. So you can write:\n\n```python\n>>> n2consst.XFFTS[\'ch_num\']\n32768\n```\n\n### Parameters\n\n*Kisa* parameter (parameters to correct instrumental error) and observation parameters are formatted using `kisa` and `obsparam` modules respectively.\n\nTo get the formatted *kisa* parameters:\n\n```python\n>>> from n_const import kisa\n>>> params = kisa.RadioKisa.from_file("path/to/kisafile")\n>>> params.dAz\nQuantity 5314.24667547 arcsec\n\n# This module also support keys to access the components:\n\n>>> params[\'dAz\']\nQuantity 5314.24667547 arcsec\n```\n\nTo get the formatted observation parameters:\n\n```python\n>>> from n_const import obsparams\n>>> params = obsparams.OTFParams.from_file("path/to/obsfile")\n>>> params.offset_Az\nQuantity 0. deg\n>>> params[\'offset_Az\']\nQuantity 0. deg\n```\n\nFor conventional style obsfiles, this module provides a parser. This is a conventional one, so it provides very limited functionality;\n\n- Dot notation is not supported, keys only.\n- Return values are not combined with units.\n\n```python\n>>> params = obsparams.obsfile_parser("path/to/obsfile")\n>>> params[\'offset_Az\']\n0\n```\n\n---\n\n- This library uses [Semantic Versioning](https://semver.org).\n',
    'author': 'KaoruNishikawa',
    'author_email': 'k.nishikawa@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nanten2/N-CONST',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
