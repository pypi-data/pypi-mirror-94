# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kaigara', 'kaigara.model']

package_data = \
{'': ['*']}

install_requires = \
['kiwisolver>=1.3,<2.0',
 'numpy>=1.19,<2.0',
 'scipy>=1.5,<2.0',
 'sympy>=1.7,<2.0']

setup_kwargs = {
    'name': 'kaigara',
    'version': '0.0.1a2',
    'description': '',
    'long_description': '# kaigara\n\n**kaigara** is a library for morphological studies on molluscan shells.\n\nWebsite: []()\n\n## Installation\n\n\n## Usage\n\n\n## License\nThis project uses the following license: [ISC License](LICENSE).\n',
    'author': 'Noshita, Koji',
    'author_email': 'noshita@morphometrics.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/noshita/kaigara',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.9,<4.0',
}


setup(**setup_kwargs)
