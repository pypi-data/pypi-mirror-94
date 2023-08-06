# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tryalot']

package_data = \
{'': ['*']}

install_requires = \
['zstandard>=0.14.1,<0.15.0']

setup_kwargs = {
    'name': 'tryalot',
    'version': '0.3.10',
    'description': 'Try a lot without worrying about the hassle.',
    'long_description': '# tryalot\n\nTry a lot without worrying about the hassle.\n\nThis is a fromework that helps you do a bunch of computational experiments.\n',
    'author': 'Yuta Taniguchi',
    'author_email': 'yuta.taniguchi.y.t@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yuttie/tryalot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
