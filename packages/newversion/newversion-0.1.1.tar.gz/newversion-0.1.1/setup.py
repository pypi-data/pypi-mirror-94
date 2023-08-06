# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['newversion']

package_data = \
{'': ['*']}

install_requires = \
['packaging>=20.0,<21.0']

setup_kwargs = {
    'name': 'newversion',
    'version': '0.1.1',
    'description': 'Version manager compatible with packaging',
    'long_description': '# NewVersion - SemVer helpers for PEP440\n\n[![PyPI - newversion](https://img.shields.io/pypi/v/newversion.svg?color=blue&label=newversion)](https://pypi.org/project/newversion)\n[![Docs](https://img.shields.io/readthedocs/newversion.svg?color=blue&label=Builder%20docs)](https://newversion.readthedocs.io/)\n\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/newversion.svg?color=blue)](https://pypi.org/project/newversion)\n[![Coverage](https://img.shields.io/codecov/c/github/vemel/newversion)](https://codecov.io/gh/vemel/newversion)\n\nVersion manager compatible with packaging.\n\nHeavily inspired by [semver](https://pypi.org/project/semver/).\n\n## Installation\n\n```bash\npython -m pip install newversion\n```\n\n## Usage\n\n```python\nfrom newversion import Version\n\nversion = Version("1.2.3")\n\n# bump version same way as SemVer\nversion.dumps() # "1.2.3"\nversion.bump_micro().dumps() # "1.2.4"\nversion.bump_minor().dumps() # "1.3.0"\nversion.bump_major().dumps() # "2.0.0"\n\n# create and bump pre-releases\nversion.bump_minor().bump_prerelease().dumps() # "1.3.0rc1"\nversion.bump_prerelease("alpha").dumps() # "1.2.3a1"\nVersion("1.2.3b4").bump_prerelease().dumps() # "1.2.3b5"\nversion.get_devrelease(1234).dumps() # "1.2.3.dev1234"\n\n# and post-releases\nversion.bump_postrelease().dumps() # "1.2.3.post1"\nVersion("1.2.3.post3").bump_postrelease(2).dumps() # "1.2.3.post5"\n\n# easily check if this is a pre- or dev release or a stable version\nVersion("1.2.3").is_stable # True\nVersion("1.2.3a6").is_stable # False\nVersion("1.2.3.post3").is_stable # True\nVersion("1.2.3.post3").get_stable().dumps() # "1.2.3"\n```\n\n## Versioning\n\n`newversion` version follows [PEP 440](https://www.python.org/dev/peps/pep-0440/).\n\n## Latest changes\n\nFull changelog can be found in [Releases](https://github.com/vemel/newversion/releases).\n',
    'author': 'Vlad Emelianov',
    'author_email': 'vlad.emelianov.nz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vemel/newversion',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
