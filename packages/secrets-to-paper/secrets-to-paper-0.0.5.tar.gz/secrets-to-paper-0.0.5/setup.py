# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['secrets_to_paper', 'secrets_to_paper.export', 'secrets_to_paper.generate']

package_data = \
{'': ['*'], 'secrets_to_paper': ['templates/*']}

install_requires = \
['cryptography>=2.9.2,<3.0.0',
 'jinja2>=2.11.2,<3.0.0',
 'pdfplumber>=0.5.21,<0.6.0',
 'pillow>=8.1.0,<9.0.0',
 'pyzbar>=0.1.8,<0.2.0',
 'qrcode>=6.1,<7.0',
 'weasyprint>=51,<52']

entry_points = \
{'console_scripts': ['stp = secrets_to_paper.core:stp']}

setup_kwargs = {
    'name': 'secrets-to-paper',
    'version': '0.0.5',
    'description': 'A command line tool to help with key-to-paper and paper-to-key.',
    'long_description': "# secrets-to-paper\n\n![Publish to PyPI](https://github.com/jaredvacanti/secrets-to-paper/workflows/Publish%20to%20PyPI/badge.svg)\n\nA command-line tool to convert secret keys to printable PDFs and to parse those\nPDFs back to usable secret keys.\n\nNote: Python 3.8+ is required to use this package. Python 3.8 introduced\na new computation for\n[modular inverses](https://docs.python.org/3/library/functions.html#pow).\n\n> Changed in version 3.8: For int operands, the three-argument form of pow now\n> allows the second argument to be negative, permitting computation of modular\n> inverses.\n\n## Dependencies\n\n[Paperkey](http://www.jabberwocky.com/software/paperkey/) is a command line tool\nto export GnuPG keys on paper. It reduces the size of the exported key, by\nremoving the public key parts from the private key. Paperkey also includes\nCRC-24 checksums in the key to allow the user to check whether their private key\nhas been restored correctly.\n\n- paperkey (for GPG keys)\n- zbar/libzbar0\n\n#### Ubuntu/Linux\n\n# Add PPA\n\n```\nsudo apt install software-properties-common\nsudo add-apt-repository ppa:jaredvacanti/security-dev\nsudo apt-get update\n\n# install the package\nsudo apt install python3-secrets-to-paper\n```\n\n#### MacOS X\n\n```\nbrew install zbar paperkey\n```\n\n### Usage\n\n```\nUsage: stp [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --debug / --no-debug\n  --help                Show this message and exit.\n\nCommands:\n  export      Helper functions for writing secret keys.\n  export-gpg  Helper function to generate archive of GPG keys.\n  gen-ecc     Helper function to generate ECC private key from A, B, and D.\n  gen-rsa     Helper function to generate RSA private key from P and Q.\n  parse       Helper functions to parse secret keys into PEM format.\n```\n\n\n## Development\n\n#### Initializing a virtual environment:\n\n```\n# requires >= python3.8\npyenv shell 3.8.3\n\n# init & activate virtualenvironment\npython -m venv .venv\nsource .venv/bin/activate\n\n# install poetry in venv, and use to install local package\npip install --upgrade pip\npip install poetry\npoetry install\n```\n\nThis makes an executable `stp` available in your `$PATH` after poetry\ninstallations. During development, it's often more convenient to run\n\n```\npoetry run stp ...\n```\n\ninstead of re-installing before invocations.\n\n## Testing\n\nYou can generate a private and public key for testing purposes using `openssl`.\n\n```\npoetry run tox\n```\n",
    'author': 'Jared Vacanti',
    'author_email': 'jaredvacanti@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jaredvacanti/secrets-to-paper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
