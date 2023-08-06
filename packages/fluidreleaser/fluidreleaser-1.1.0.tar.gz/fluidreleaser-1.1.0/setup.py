# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fluidreleaser', 'fluidreleaser.utils']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.12,<4.0.0', 'paramiko>=2.7.2,<3.0.0']

setup_kwargs = {
    'name': 'fluidreleaser',
    'version': '1.1.0',
    'description': 'ProjectFluid OTA releaser.',
    'long_description': '# ProjectFluid OTA releaser\n\n## Installation\n\n```\npip3 install fluidreleaser\n```\nThe module is supported on Python 3.6 and above.\n',
    'author': 'Sebastiano Barezzi',
    'author_email': 'barezzisebastiano@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Project-Fluid/fluidreleaser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
