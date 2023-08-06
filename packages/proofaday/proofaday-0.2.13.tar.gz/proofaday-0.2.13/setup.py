# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['proofaday']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.0,<2.0.0',
 'beautifulsoup4>=4.9.0,<5.0.0',
 'click>=7.1.0,<8.0.0',
 'pylatexenc>=2.8,<3.0',
 'python-daemon>=2.2.0,<3.0.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['dproofaday = proofaday.daemon_cli:main',
                     'proofaday = proofaday.proofaday:main']}

setup_kwargs = {
    'name': 'proofaday',
    'version': '0.2.13',
    'description': 'Print random proofs from ProofWiki',
    'long_description': '# proofaday\nPrint random proofs from ProofWiki\n',
    'author': 'Wolf Honoré',
    'author_email': 'wolfhonore@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whonore/proofaday',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
